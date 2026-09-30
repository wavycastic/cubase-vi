"""Qt `.qm` translation catalogue reader **and writer**.

Steinberg's Score Editor ships its own localisation as `.qm` catalogues next to
`instrumentnames_XX.xml`, entirely separate from Cubase's `translation.xml`.
Reading and writing them means the Vietnamese Score Editor is a matter of
authoring a catalogue, not reverse-engineering one.

Format notes that are easy to get wrong:

  * block lengths are **big-endian**; reading them little-endian yields
    nonsense lengths that happen to look like plausible sizes
  * `Tag_Translation` (3) holds **UTF-16 big-endian**, and its length is
    *rejected* by Qt if odd (`if (len & 1) return QString()`).  The source
    (6), context (7) and comment (8) are 8-bit
  * the Hashes block is **not** an open-addressed table: it is a flat array of
    8-byte `(hash, offset)` pairs, big-endian, **sorted ascending by
    `(hash, offset)`**, which the reader binary-searches.  Each entry is one
    message, so dividing its size by 8 gives the entry count
  * the hash covers the **source and the comment only** - never the translation
    - which is what lets translations be replaced without re-deriving anything
  * `Tag_End` (1) is a bare byte with no length; every other tag is
    `tag(1) | len(4, BE) | payload`
  * a `Tag_Translation` whose declared length is `0xFFFFFFFF` is a no-payload
    sentinel (an unfinished numerus form) occupying exactly 5 bytes

The writer side (`assemble`, `build_catalogue`, `QM.dump`) reproduces
`lrelease` output byte-for-byte; `tools/tests/test_qm.py` asserts that against
every catalogue in a real Cubase install.
"""
import struct
from dataclasses import dataclass, field

MAGIC = bytes.fromhex('3cb86418caef9c95cd211cbf60a1bddd')

TAG_END = 1
TAG_SOURCE16 = 2
TAG_TRANSLATION = 3
TAG_CONTEXT16 = 4
TAG_OBSOLETE1 = 5
TAG_SOURCE = 6        # 8-bit source
TAG_CONTEXT = 7       # 8-bit context
TAG_COMMENT = 8
TAG_OBSOLETE2 = 9

# Tags whose payload is `len` bytes of 8-bit data with no interpretation.
TAG_SKIP = frozenset((TAG_OBSOLETE1, TAG_COMMENT, TAG_OBSOLETE2))
# Tags whose payload is `len` bytes of UTF-16.
TAG_UTF16 = frozenset((TAG_SOURCE16, TAG_TRANSLATION, TAG_CONTEXT16))

# A Tag_Translation may declare this length to mean "no payload at all"; it is
# Steinberg's null-translation / unfinished-numerus marker and still occupies
# the 5 bytes of tag + length.
SENTINEL_LEN = 0xFFFFFFFF

BLOCK_CONTEXTS = 0x2F
BLOCK_HASHES = 0x42
BLOCK_MESSAGES = 0x69
BLOCK_NUMERUS = 0x88
BLOCK_DEPENDENCIES = 0x96
# Qt 6 added 0xA7 "Language" (the locale name, UTF-8).  Steinberg's catalogues
# use it instead of 0x2F Contexts, so after masking the endianness bit the
# block is keyed as 0x27 and readers accept either spelling.
BLOCK_LANGUAGE = 0xA7
BLOCK_CONTEXTS_ALT = 0xA7 & 0x7F

BLOCK_NAMES = {BLOCK_CONTEXTS: 'Contexts', BLOCK_CONTEXTS_ALT: 'Contexts',
               BLOCK_HASHES: 'Hashes', BLOCK_MESSAGES: 'Messages',
               BLOCK_NUMERUS: 'NumerusRules',
               BLOCK_DEPENDENCIES: 'Dependencies'}


def block_key(tag):
    """Blocks are stored under `tag & 0x7F`.

    That is how 0xA7 (Qt 6 "Language") and 0x27 ("Contexts") end up sharing a
    slot, but it also means 0x88 and 0x96 do *not* live under their own tag -
    looking them up raw silently finds nothing.  Always go through this.
    """
    return tag & 0x7F


#: block keys that carry either the locale name or the context hash table
CONTEXT_BLOCKS = (BLOCK_CONTEXTS, BLOCK_CONTEXTS_ALT)


class QMError(ValueError):
    pass


def _u16be(b, o):
    return struct.unpack_from('>H', b, o)[0]


def _u32be(b, o):
    return struct.unpack_from('>I', b, o)[0]


def decode_utf16(raw):
    """Qt hands UTF-16 to QString::fromUtf16 with endianness detection.

    For ASCII-ish text the first code unit settles it: little-endian puts the
    character in the low byte, big-endian in the high byte.
    """
    if not raw:
        return ''
    if raw[:2] == b'\xfe\xff':
        return raw[2:].decode('utf-16-be', 'replace')
    if raw[:2] == b'\xff\xfe':
        return raw[2:].decode('utf-16-le', 'replace')
    if len(raw) < 2:
        return raw.decode('latin-1', 'replace')
    if raw[1] == 0x00 and raw[0] != 0x00:
        return raw.decode('utf-16-le', 'replace')   # 'A' stored as 41 00
    if raw[0] == 0x00 and raw[1] != 0x00:
        return raw.decode('utf-16-be', 'replace')   # 'A' stored as 00 41
    return raw.decode('utf-16-be', 'replace')


def decode_8bit(raw):
    """8-bit payloads are Latin-1 in practice; tolerate UTF-8 too."""
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('latin-1')


@dataclass
class Message:
    context: str = ''
    source: str = ''
    translation: str = ''

    def __iter__(self):
        return iter((self.source, self.translation, self.context))


@dataclass
class QM:
    path: str
    blocks: dict = field(default_factory=dict)
    messages: list = field(default_factory=list)
    size: int = 0
    consumed: int = 0
    #: block key -> the tag byte exactly as stored, so `dump()` can re-emit
    #: 0xA7 rather than the 0x27 the key masks it down to
    raw_tags: dict = field(default_factory=dict)
    #: Messages block split into per-message record groups, kept verbatim so
    #: the writer can reproduce the file byte-for-byte
    records: list = field(default_factory=list)
    #: memoised `(hash, offset)` pairs; built on first lookup
    _pairs: list = field(default_factory=list, repr=False)

    # -- loading -----------------------------------------------------------
    @classmethod
    def load(cls, path):
        data = open(path, 'rb').read()
        return cls.loads(data, path=str(path))

    @classmethod
    def loads(cls, data, path='<bytes>'):
        if data[:16] != MAGIC:
            raise QMError('not a Qt .qm file (bad magic)')
        qm = cls(path=path, size=len(data))
        pos = 16
        while pos + 5 <= len(data):
            tag = data[pos]
            length = _u32be(data, pos + 1)
            if pos + 5 + length > len(data):
                break
            qm.blocks[block_key(tag)] = data[pos + 5:pos + 5 + length]
            qm.raw_tags[block_key(tag)] = tag
            pos += 5 + length
        qm.consumed = pos
        if BLOCK_MESSAGES in qm.blocks:
            qm.records = scan_records(qm.blocks[BLOCK_MESSAGES])
            qm.messages = parse_messages(qm.blocks[BLOCK_MESSAGES])
        return qm

    # -- writing -----------------------------------------------------------
    def dump(self, language=None):
        """Re-serialise this catalogue, optionally renaming the locale.

        With no argument the existing locale block is copied through verbatim,
        whatever tag it happens to use.  Passing a name replaces it with a
        0xA7 Language block, which is what Steinberg's own catalogues use.

        Round-trips byte-for-byte on every catalogue Steinberg ships, which is
        the regression test that the writer really is an `lrelease`.
        """
        numerus = self.blocks.get(block_key(BLOCK_NUMERUS))
        groups = group_messages(self.records)
        if language is None:
            pre = [(self.raw_tags[k], self.blocks[k])
                   for k in CONTEXT_BLOCKS if k in self.blocks]
        else:
            pre = [(BLOCK_LANGUAGE, encode_8bit(language))] if language else ()
        return assemble(groups, numerus=numerus, pre_blocks=pre)

    def save(self, path, language=None):
        data = self.dump(language=language)
        with open(path, 'wb') as fh:
            fh.write(data)
        return len(data)

    # -- introspection -----------------------------------------------------
    @property
    def language(self):
        """The locale name from the 0xA7 Language block, e.g. "de_DE".

        Qt treats this as informational only - lookup never consults it - but
        it is how the catalogue names itself, so `dump()` preserves it.
        """
        blob = self.blocks.get(BLOCK_CONTEXTS_ALT)
        return decode_8bit(blob) if blob else ''

    @property
    def contexts(self):
        """The Contexts block, which holds the locale name(s).

        With a single context the block is the raw locale string and nothing
        else - no length prefix.  Multi-context catalogues frame each entry
        with a 2-byte length, so try that first and fall back.
        """
        blob = None
        for tag in (BLOCK_CONTEXTS, BLOCK_CONTEXTS_ALT):
            if tag in self.blocks:
                blob = self.blocks[tag]
                break
        if not blob:
            return []
        out, i = [], 0
        while i + 2 <= len(blob):
            n = _u16be(blob, i)
            if n == 0 or i + 2 + 2 * n > len(blob):
                break
            out.append(decode_utf16(blob[i + 2:i + 2 + 2 * n]))
            i += 2 + 2 * n
        if i == len(blob) and out:
            return out
        # single unframed locale name
        return [decode_8bit(blob)]

    @property
    def hash_slots(self):
        """Number of `(hash, offset)` entries - one per message, no slack."""
        blob = self.blocks.get(block_key(BLOCK_HASHES))
        return len(blob) // 8 if blob else 0

    @property
    def hash_used(self):
        return self.hash_slots

    @property
    def expected_messages(self):
        """How many messages the hash table says the catalogue should hold."""
        return self.hash_slots

    @property
    def complete(self):
        """Did we recover as many messages as the hash table implies?"""
        if not self.expected_messages:
            return True
        return len(self.messages) >= self.expected_messages

    def block_summary(self):
        rows = []
        for key, blob in sorted(self.blocks.items()):
            tag = self.raw_tags.get(key, key)
            name = BLOCK_NAMES.get(key, f'0x{tag:02X}')
            extra = ''
            if key == BLOCK_CONTEXTS_ALT:
                extra = ' ' + (self.language or '(empty)')
            elif key == block_key(BLOCK_HASHES):
                extra = f' {self.hash_used} entries'
            elif key == block_key(BLOCK_MESSAGES):
                extra = f' {len(self.messages)} messages'
            rows.append(f'  {name:14} 0x{tag:02X} {len(blob):>10,} bytes{extra}')
        if self.expected_messages:
            rows.append(f'  {"":14} {"":4} {len(self.messages):>10,} parsed'
                        + ('' if self.complete else '  <-- INCOMPLETE'))
        return '\n'.join(rows)

    def pairs(self):
        """(source, translation) pairs, skipping the disambiguating context."""
        return [(m.source, m.translation) for m in self.messages if m.source]

    def catalogue(self):
        return {m.source: m.translation for m in self.messages if m.source}

    def lookup(self, context, source, comment=''):
        """Resolve one string the way Qt's `do_translate` would.

        This is the check that matters for a catalogue we *wrote*: a file can
        round-trip perfectly and still be unreachable if the hash table is
        wrong, because nothing reads the Messages block sequentially at
        runtime.  Mirrors the reader's binary search and `getMessage` walk,
        including its "try again with an empty comment" fallback and the odd
        length guard that silently drops a translation.
        """
        blob = self.blocks.get(block_key(BLOCK_HASHES))
        if not blob:
            return None
        if not self._pairs:
            self._pairs = [struct.unpack_from('>II', blob, i)
                           for i in range(0, len(blob), 8)]
        pairs = self._pairs

        def find(h):
            """Binary search, then run forward over equal hashes."""
            lo, hi = 0, len(pairs) - 1
            found = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if pairs[mid][0] == h:
                    found = mid
                    break
                if pairs[mid][0] < h:
                    lo = mid + 1
                else:
                    hi = mid - 1
            if found < 0:
                return []
            while found > 0 and pairs[found - 1][0] == h:
                found -= 1
            out = []
            while found < len(pairs) and pairs[found][0] == h:
                out.append(pairs[found][1])
                found += 1
            return out

        body = self.blocks.get(block_key(BLOCK_MESSAGES), b'')
        src_b = encode_8bit(source)
        cmt_b = encode_8bit(comment)
        cmt = comment
        for _ in range(2):
            for offset in find(elf_hash(src_b, encode_8bit(cmt))):
                got = _read_message(body, offset, context, source, comment)
                if got is not None:
                    return got
            if not cmt:
                break
            cmt = ''
        return None


def _read_message(blob, offset, context, source, comment):
    """Qt's `getMessage`: walk one message's records, checking each field.

    Deliberately as strict as Qt.  `Tag_SourceText16` (2), `Tag_Context16` (4)
    and `Tag_Obsolete2` (9) have no case in Qt's switch and fall through to
    `default: return QString()`, so a message carrying one is unreachable -
    accepting it here would let us "verify" a catalogue the engine would drop.
    `Tag_Obsolete1` (5) is a bare 4-byte value with no length of its own.
    """
    pos, n = offset, len(blob)
    tn, tn_len = None, 0
    src_b, ctx_b, cmt_b = encode_8bit(source), encode_8bit(context), encode_8bit(comment)
    while pos < n:
        tag = blob[pos]
        pos += 1
        if tag == TAG_END:
            break
        if tag == TAG_OBSOLETE1:
            pos += 4
            continue
        if pos + 4 > n:
            return None
        ln = _u32be(blob, pos)
        pos += 4
        if tag == TAG_TRANSLATION:
            if ln & 1:
                return None                      # Qt rejects odd lengths
            if tn is None:
                tn, tn_len = pos, ln
        elif tag == TAG_SOURCE:
            if blob[pos:pos + ln] != src_b:
                return None
        elif tag == TAG_CONTEXT:
            if blob[pos:pos + ln] != ctx_b:
                return None
        elif tag == TAG_COMMENT:
            # Qt skips the comparison when the payload starts with a NUL
            if ln and blob[pos] != 0 and blob[pos:pos + ln] != cmt_b:
                return None
        else:
            return None
        pos += ln
    if tn is None:
        return None
    raw = blob[tn:tn + tn_len]
    if not raw:
        return None                              # empty -> a null QString
    return decode_utf16(raw)


# -- record-level reading --------------------------------------------------

@dataclass
class Record:
    """One Messages-block record: a tag plus its exact payload bytes.

    Kept as raw bytes rather than decoded text so that a parse/serialise cycle
    is lossless - which is what makes `dump()` byte-comparable to the original.

    `raw_len` preserves a declared length that disagrees with the payload, in
    practice the `0xFFFFFFFF` sentinel of an unfinished numerus form.  It is
    5 bytes on disk like any other empty record, but rewriting it as a plain
    zero would quietly change the file.
    """
    tag: int
    payload: bytes = b''
    raw_len: int = None

    @property
    def size(self):
        return 1 if self.tag == TAG_END else 5 + len(self.payload)

    @property
    def declared_len(self):
        return len(self.payload) if self.raw_len is None else self.raw_len

    def __iter__(self):
        return iter((self.tag, self.payload))


def scan_records(blob):
    """Split a Messages block into a flat list of `Record`s.

    Raises QMError rather than clamping when the stream is truncated, because
    a writer cannot faithfully re-emit a block it failed to understand.
    """
    out = []
    pos, n = 0, len(blob)
    while pos < n:
        tag = blob[pos]
        if tag == TAG_END:
            out.append(Record(tag))
            pos += 1
            continue
        if pos + 5 > n:
            raise QMError(f'Messages block truncated at +0x{pos:X}')
        raw = _u32be(blob, pos + 1)
        if raw == SENTINEL_LEN:
            # No payload at all, but the declared length must survive verbatim.
            out.append(Record(tag, b'', raw_len=SENTINEL_LEN))
            pos += 5
            continue
        ln = raw & 0x7FFFFFFF
        if pos + 5 + ln > n:
            raise QMError(f'Tag 0x{tag:02X} at +0x{pos:X} declares '
                          f'0x{raw:08X} bytes, past the end of the block')
        out.append(Record(tag, blob[pos + 5:pos + 5 + ln]))
        pos += 5 + ln
    return out


def group_messages(records):
    """Group a flat record list into one list of records per message."""
    groups, cur = [], []
    for rec in records:
        cur.append(rec)
        if rec.tag == TAG_END:
            groups.append(cur)
            cur = []
    if cur:
        raise QMError('Messages block ends without a Tag_End record')
    return groups


def message_parts(group):
    """(translations, source_bytes, context_bytes, comment_bytes) for a group.

    The source and comment are returned as bytes because the Qt hash is
    computed over them *raw*, exactly as the application passes them to
    `QCoreApplication::translate()`.
    """
    translations, source, context, comment = [], b'', b'', b''
    for rec in group:
        if rec.tag == TAG_TRANSLATION:
            translations.append(rec.payload)
        elif rec.tag in (TAG_SOURCE, TAG_SOURCE16):
            source = rec.payload
        elif rec.tag in (TAG_CONTEXT, TAG_CONTEXT16):
            context = rec.payload
        elif rec.tag == TAG_COMMENT:
            comment = rec.payload
    return translations, source, context, comment


# -- writing ---------------------------------------------------------------

MASK32 = 0xFFFFFFFF


def elf_hash(source, comment=b''):
    """Qt's hash, byte for byte.

    `elfHash_continue` folds each byte in and stops at the first NUL of each
    part, so the source and the comment are hashed independently; `elfHash_
    finish` maps 0 to 1 so that the empty string still gets a slot.  Only the
    source and comment participate - never the translation.
    """
    h = 0
    for part in (source, comment):
        for b in part:
            if b == 0:
                break
            h = ((h << 4) + b) & MASK32
            g = h & 0xF0000000
            if g:
                h ^= g >> 24
            h &= ~g & MASK32
    return 1 if h == 0 else h


def encode_utf16be(text):
    """Qt drops a translation whose length is odd, so a lone surrogate would
    silently blank the string.  Fail here instead, where it is still fixable."""
    try:
        raw = text.encode('utf-16-be')
    except UnicodeEncodeError as exc:
        raise QMError(f'not encodable as UTF-16: {text!r} ({exc})') from None
    if len(raw) % 2:
        raise QMError(f'translation is not whole UTF-16 code units: {text!r}')
    return raw


def encode_8bit(text):
    """8-bit payloads are UTF-8 in practice; Latin-1 is the safety net."""
    try:
        return text.encode('utf-8')
    except UnicodeEncodeError:
        return text.encode('latin-1', 'replace')


def _block(tag, payload):
    return bytes([tag]) + struct.pack('>I', len(payload)) + payload


def _serialise(records):
    out = []
    for rec in records:
        if rec.tag == TAG_END:
            out.append(b'\x01')
        else:
            out.append(bytes([rec.tag])
                       + struct.pack('>I', rec.declared_len) + rec.payload)
    return b''.join(out)


def build_hash_block(groups, offsets):
    """The `(hash, offset)` table, sorted ascending by `(hash, offset)`.

    Qt binary-searches this array, so the ordering is load-bearing rather than
    cosmetic; a stable sort on the pair is what `lrelease` emits and what the
    Steinberg files contain.
    """
    pairs = []
    for group, offset in zip(groups, offsets):
        _, source, _, comment = message_parts(group)
        pairs.append((elf_hash(source, comment), offset))
    pairs.sort()
    return b''.join(struct.pack('>II', h, o) for h, o in pairs)


def assemble(groups, numerus=None, pre_blocks=()):
    """Serialise message groups into a complete `.qm`.

    `groups` is a list of per-message record lists (see `group_messages`), so
    anything the reader preserved - numerus forms, comments, sentinel records,
    the record order itself - survives untouched.  `pre_blocks` is an iterable
    of `(raw_tag, payload)` emitted verbatim between the magic and the hash
    table, which is how a locale or context block is carried through unchanged.
    """
    # A zero-length block terminates parsing in Qt's loader, so never emit one.
    out = [MAGIC]
    for tag, payload in pre_blocks:
        if payload:
            out.append(_block(tag, payload))
    body, offsets, pos = [], [], 0
    for group in groups:
        offsets.append(pos)
        blob = _serialise(group)
        body.append(blob)
        pos += len(blob)
    if groups:
        out.append(_block(BLOCK_HASHES, build_hash_block(groups, offsets)))
        out.append(_block(BLOCK_MESSAGES, b''.join(body)))
    if numerus:
        out.append(_block(BLOCK_NUMERUS, numerus))
    return b''.join(out)


def make_message(context, source, translation, comment='', wide=False):
    """Build one message's record group in `lrelease`'s field order.

    Translation first, then comment, source, context, end - the order every
    Steinberg catalogue uses.  `translation` may be a list to emit numerus
    forms; an empty entry becomes the 5-byte no-payload sentinel.
    """
    forms = translation if isinstance(translation, (list, tuple)) else [translation]
    group = []
    for form in forms:
        if form:
            group.append(Record(TAG_TRANSLATION, encode_utf16be(form)))
        else:
            group.append(Record(TAG_TRANSLATION))
    if comment:
        group.append(Record(TAG_COMMENT, encode_8bit(comment)))
    if source:
        if wide:
            group.append(Record(TAG_SOURCE16, encode_utf16be(source)))
        else:
            group.append(Record(TAG_SOURCE, encode_8bit(source)))
    if context:
        if wide:
            group.append(Record(TAG_CONTEXT16, encode_utf16be(context)))
        else:
            group.append(Record(TAG_CONTEXT, encode_8bit(context)))
    group.append(Record(TAG_END))
    return group


def build_catalogue(entries, language='vi_VN', numerus=None):
    """Build a whole catalogue from `(context, source, translation)` triples.

    `numerus` defaults to the single-rule block every Steinberg catalogue
    carries (`01 01`).
    """
    if numerus is None:
        numerus = b'\x01\x01'
    groups = [make_message(ctx, src, tr) for ctx, src, tr in entries]
    pre = [(BLOCK_LANGUAGE, encode_8bit(language))] if language else ()
    return assemble(groups, numerus=numerus, pre_blocks=pre)


def _translation_index(qm):
    """Map lookup keys to message identities, refusing ambiguous ones.

    The Qt hash covers source and comment but *not* context, so a catalogue can
    legitimately hold several entries that differ only by comment - Steinberg's
    Score Editor has 70 of them in 53 contexts, 10 of which share a source
    within one context.  Keying on `(context, source)` alone would collapse
    those onto one row, so a key is only accepted when it resolves to exactly
    one message.
    """
    triple, pair, single = {}, {}, {}
    for i, group in enumerate(group_messages(qm.records)):
        _, source, context, comment = message_parts(group)
        src_txt, ctx_txt, cmt_txt = (decode_8bit(source),
                                     decode_8bit(context),
                                     decode_8bit(comment))
        triple[(ctx_txt, src_txt, cmt_txt)] = i
        pair.setdefault((ctx_txt, src_txt), set()).add(i)
        single.setdefault(src_txt, set()).add(i)
    return triple, pair, single


def translate(qm, mapping, language=None):
    """Return a copy of `qm` with translations replaced.

    `mapping` may be keyed by `(context, source, comment)`, by
    `(context, source)`, or by bare `source`, most specific first.  A key that
    matches more than one message is refused rather than guessed at, and
    counted in `stats['ambiguous']` - silently collapsing the comment-
    disambiguated entries would drop 70 strings from the Score Editor.

    Messages with no entry keep their original translation.  The hash table is
    rebuilt from scratch, because a different translation is a different length
    and every later message therefore moves.
    """
    triple, pair, single = _translation_index(qm)
    groups, stats = [], {'hit': 0, 'context': 0, 'source': 0,
                         'ambiguous': 0, 'miss': 0}
    for group in group_messages(qm.records):
        _, source, context, comment = message_parts(group)
        src_txt, ctx_txt, cmt_txt = (decode_8bit(source),
                                     decode_8bit(context),
                                     decode_8bit(comment))
        chosen = None
        for key, kind in (((ctx_txt, src_txt, cmt_txt), 'hit'),
                          ((ctx_txt, src_txt), 'context'),
                          (src_txt, 'source')):
            if key not in mapping:
                continue
            pool = triple.get(key)
            if pool is None:
                pool = pair.get(key, single.get(key))
            if isinstance(pool, set) and len(pool) > 1:
                stats['ambiguous'] += 1
                continue
            if isinstance(pool, set):
                stats['ambiguous'] += 1
                continue
            if pool is None:
                continue
            chosen = mapping[key]
            stats[kind] += 1
            break
        if chosen is None:
            stats['miss'] += 1
            groups.append(group)
            continue
        forms = list(chosen) if isinstance(chosen, (list, tuple)) else [chosen]
        replaced = [Record(TAG_TRANSLATION,
                           encode_utf16be(f) if f else b'') for f in forms]
        # keep any leading non-translation records in their original position
        rebuilt, inserted = [], False
        for rec in group:
            if rec.tag == TAG_TRANSLATION:
                if not inserted:
                    rebuilt.extend(replaced)
                    inserted = True
                continue
            rebuilt.append(rec)
        if not inserted:
            rebuilt = replaced + rebuilt
        groups.append(rebuilt)
    if language is None:
        pre = [(qm.raw_tags[k], qm.blocks[k])
               for k in CONTEXT_BLOCKS if k in qm.blocks]
    else:
        pre = [(BLOCK_LANGUAGE, encode_8bit(language))] if language else ()
    data = assemble(groups,
                    numerus=qm.blocks.get(block_key(BLOCK_NUMERUS)),
                    pre_blocks=pre)
    return QM.loads(data, path=qm.path), stats


def parse_messages(blob):
    """Walk the Messages block into Message records.

    Layout per tag: one tag byte, a 4-byte **big-endian** payload length in
    bytes, then the payload.  Tags 2/3/4 carry UTF-16, 6/7 carry 8-bit text,
    5/8/9 are skipped, and 1 terminates one message.  Messages are laid
    end-to-end with no padding.
    """
    out = []
    cur = Message()
    pos = 0
    n = len(blob)
    anomalies = []

    def flush():
        nonlocal cur
        if cur.source or cur.translation or cur.context:
            out.append(cur)
        cur = Message()

    while pos < n:
        tag = blob[pos]
        if tag == TAG_END:
            flush()
            pos += 1
            continue
        if pos + 5 > n:
            break
        raw_len = _u32be(blob, pos + 1)
        ln = raw_len & 0x7FFFFFFF
        if pos + 5 + ln > n:
            # Steinberg's catalogues contain records whose declared length is
            # 0xFFFFFFFF - a null-translation sentinel, not a real payload.
            # Clamp instead of desynchronising the whole walk.
            anomalies.append((len(out), pos, tag, raw_len))
            ln = 0
        payload = blob[pos + 5:pos + 5 + ln]
        if tag == TAG_SOURCE16:
            cur.source = decode_utf16(payload)
        elif tag == TAG_TRANSLATION:
            if ln:
                cur.translation = decode_utf16(payload)
        elif tag == TAG_CONTEXT16:
            cur.context = decode_utf16(payload)
        elif tag == TAG_SOURCE:
            cur.source = decode_8bit(payload)
        elif tag == TAG_CONTEXT:
            cur.context = decode_8bit(payload)
        elif tag in TAG_SKIP:
            pass
        else:
            # Unknown tag: we cannot know its payload width, so resync by
            # treating the next byte as a fresh tag.
            anomalies.append((len(out), pos, tag, raw_len))
            pos += 1
            continue
        pos += 5 + ln
    flush()
    Message.anomalies = anomalies
    return out


def pseudo_width(text):
    """Rough rendered width of a pseudo-localised string, for overflow triage.

    Steinberg's own pseudo pass roughly doubles the glyph count, so comparing
    widths against the real translation is a cheap proxy for "will this fit".
    """
    return len(text) + text.count('o') * 0.5 + text.count('0')
