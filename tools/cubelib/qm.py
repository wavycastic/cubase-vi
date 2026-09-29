"""Qt `.qm` translation catalogue reader.

Steinberg's Score Editor ships its own localisation as `.qm` catalogues next to
`instrumentnames_XX.xml`, entirely separate from Cubase's `translation.xml`.
Being able to read them means the Vietnamese Score Editor is a matter of
authoring a catalogue, not reverse-engineering one.

Format notes that are easy to get wrong:

  * block lengths are **big-endian**; reading them little-endian yields
    nonsense lengths that happen to look like plausible sizes
  * `Tag_Translation` (3) holds **UTF-8**, while `Tag_SourceText16` (2) and
    `Tag_Context16` (4) hold UTF-16 with runtime endianness detection
  * the Hashes block is an open-addressed table of 4-byte slots, so dividing
    its size by 4 gives the number of translatable entries
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

BLOCK_CONTEXTS = 0x2F
BLOCK_HASHES = 0x42
BLOCK_MESSAGES = 0x69
BLOCK_NUMERUS = 0x88
BLOCK_DEPENDENCIES = 0x96

BLOCK_NAMES = {BLOCK_CONTEXTS: 'Contexts', BLOCK_HASHES: 'Hashes',
               BLOCK_MESSAGES: 'Messages', BLOCK_NUMERUS: 'NumerusRules',
               BLOCK_DEPENDENCIES: 'Dependencies'}


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
            qm.blocks[tag & 0x7F] = data[pos + 5:pos + 5 + length]
            pos += 5 + length
        qm.consumed = pos
        if BLOCK_MESSAGES in qm.blocks:
            qm.messages = parse_messages(qm.blocks[BLOCK_MESSAGES])
        return qm

    # -- introspection -----------------------------------------------------
    @property
    def contexts(self):
        blob = self.blocks.get(BLOCK_CONTEXTS)
        if not blob:
            return []
        out, i = [], 0
        while i + 2 <= len(blob):
            n = _u16be(blob, i)
            s = blob[i + 2:i + 2 + n]
            if len(s) < n:
                break
            out.append(decode_utf16(s))
            i += 2 + n
        return out

    @property
    def hash_slots(self):
        blob = self.blocks.get(BLOCK_HASHES)
        return len(blob) // 4 if blob else 0

    @property
    def hash_used(self):
        blob = self.blocks.get(BLOCK_HASHES)
        if not blob:
            return 0
        empty = sum(1 for i in range(0, len(blob) - 3, 4)
                    if _u32be(blob, i) == 0)
        return self.hash_slots - empty

    @property
    def expected_messages(self):
        """Qt sizes the hash table at roughly 2x the number of entries."""
        return self.hash_slots // 2

    @property
    def complete(self):
        """Did we recover about as many messages as the hash table implies?"""
        if not self.expected_messages:
            return True
        return len(self.messages) >= self.expected_messages * 0.98

    def block_summary(self):
        rows = []
        for tag, blob in sorted(self.blocks.items()):
            name = BLOCK_NAMES.get(tag, f'0x{tag:02X}')
            extra = ''
            if tag == BLOCK_CONTEXTS:
                extra = ' ' + ', '.join(self.contexts)
            elif tag == BLOCK_HASHES:
                extra = f' {self.hash_used}/{self.hash_slots} slots used'
            elif tag == BLOCK_MESSAGES:
                extra = f' {len(self.messages)} messages'
            rows.append(f'  {name:14} 0x{tag:02X} {len(blob):>10,} bytes{extra}')
        if self.expected_messages:
            pct = 100 * len(self.messages) / self.expected_messages
            rows.append(f'  {"":14} {"":4} {len(self.messages):>10,} parsed '
                        f'({pct:.0f}% of ~{self.expected_messages:,} implied by '
                        f'the hash table)')
        return '\n'.join(rows)

    def pairs(self):
        """(source, translation) pairs, skipping the disambiguating context."""
        return [(m.source, m.translation) for m in self.messages if m.source]

    def catalogue(self):
        return {m.source: m.translation for m in self.messages if m.source}


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
