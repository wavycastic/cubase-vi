"""Synthetic Qt .qm builder, so the reader and writer can be tested without
Cubase.

This is an *independent* implementation of the format: it hashes and orders
the table its own way, so agreeing with `cubelib.qm` is evidence rather than a
tautology.  The real ground truth is elsewhere - `test_qm.py` asserts a
byte-exact round-trip against every catalogue Steinberg actually ships.
"""
import struct

MAGIC = bytes.fromhex('3cb86418caef9c95cd211cbf60a1bddd')

TAG_END = 1
TAG_SOURCE16 = 2
TAG_TRANSLATION = 3
TAG_CONTEXT16 = 4
TAG_OBSOLETE1 = 5
TAG_SOURCE = 6
TAG_CONTEXT = 7
TAG_COMMENT = 8

BLOCK_LANGUAGE = 0xA7
BLOCK_CONTEXTS = 0x2F
BLOCK_HASHES = 0x42
BLOCK_MESSAGES = 0x69
BLOCK_NUMERUS = 0x88


def block(tag, payload):
    """One block.  Lengths are big-endian - getting this wrong yields
    plausible-looking but wildly wrong sizes."""
    return bytes([tag]) + struct.pack('>I', len(payload)) + payload


def utf16(s):
    return s.encode('utf-16-be')


def elf_hash(source, comment=b''):
    """Qt's hash: fold bytes in, stop each part at its first NUL, 0 maps to 1."""
    h = 0
    for part in (source, comment):
        for b in part:
            if b == 0:
                break
            h = (h << 4) + b
            g = h & 0xF0000000
            if g:
                h ^= g >> 24
            h &= ~g & 0xFFFFFFFF
    return 1 if h == 0 else h


def record(tag, payload):
    return bytes([tag]) + struct.pack('>I', len(payload)) + payload


def message(source, translation, context='', wide=True, comment=''):
    """One message's records, in lrelease's field order.

    `Tag_Translation` is always UTF-16 in the Qt format; `wide` only controls
    whether the source and context use the 16-bit tags or the 8-bit ones, which
    is the mix real catalogues can contain.
    """
    out = b''
    if translation:
        out += record(TAG_TRANSLATION, utf16(translation))
    if comment:
        out += record(TAG_COMMENT, comment.encode('utf-8'))
    if source:
        if wide:
            out += record(TAG_SOURCE16, utf16(source))
        else:
            out += record(TAG_SOURCE, source.encode('utf-8'))
    if context:
        if wide:
            out += record(TAG_CONTEXT16, utf16(context))
        else:
            out += record(TAG_CONTEXT, context.encode('utf-8'))
    return out + bytes([TAG_END])


def hash_table(groups):
    """The `(hash, offset)` table: 8 bytes per entry, sorted by (hash, offset).

    Qt binary-searches it, so the ordering is load-bearing.
    """
    pairs, pos = [], 0
    for group in groups:
        pairs.append((elf_hash(group[1], group[3]), pos))
        pos += len(group[0])
    pairs.sort()
    return b''.join(struct.pack('>II', h, o) for h, o in pairs)


def _split(raw):
    """Recover (serialised bytes, source, comment) per message group."""
    out, i = [], 0
    while i < len(raw):
        start = i
        source = comment = b''
        while True:
            tag = raw[i]
            i += 1
            if tag == TAG_END:
                break
            ln = struct.unpack_from('>I', raw, i)[0]
            if ln == 0xFFFFFFFF:
                i += 4              # sentinel: length word only, no payload
                continue
            payload = raw[i + 4:i + 4 + ln]
            i += 4 + ln
            if tag in (TAG_SOURCE, TAG_SOURCE16):
                source = payload
            elif tag == TAG_COMMENT:
                comment = payload
        out.append((raw[start:i], source, b'', comment))
    return out


def catalogue(messages, context='TestDialog', raw_messages=None, pad_entries=0,
              language_block=True):
    """Build a complete .qm.  `messages` is a list of (source, translation).

    `raw_messages` bypasses `message()` so a test can splice in hand-built
    records.  `pad_entries` declares extra hash-table entries that no message
    points at, which is how the reader's `complete` check gets exercised.
    """
    if raw_messages is not None:
        groups = _split(raw_messages)
    else:
        groups = []
        for i, (src, tr) in enumerate(messages):
            body = message(src, tr, context if i == 0 else '', wide=False)
            groups.append((body, src.encode('utf-8'), b'', b''))
    tables = hash_table(groups)
    if pad_entries:
        # Entries pointing at offset 0 that no message resolves to, so the
        # reader sees a hash table larger than the message stream.
        extra = [(elf_hash(b'pad-entry-%d' % i), 0) for i in range(pad_entries)]
        pairs = [(struct.unpack_from('>II', tables, i)[0],
                  struct.unpack_from('>II', tables, i)[1])
                 for i in range(0, len(tables), 8)]
        tables = b''.join(struct.pack('>II', h, o)
                          for h, o in sorted(pairs + extra))
    out = MAGIC
    if language_block and context:
        out += block(BLOCK_LANGUAGE, context.encode('utf-8'))
    if groups:
        out += block(BLOCK_HASHES, tables)
        out += block(BLOCK_MESSAGES, b''.join(g[0] for g in groups))
    out += block(BLOCK_NUMERUS, b'\x01\x01')
    return out


def sentinel_message():
    """A record whose declared length is 0xFFFFFFFF, the null-translation
    marker Steinberg's catalogues contain.  A reader that trusts the length
    instead of clamping loses every following message."""
    out = b''
    out += bytes([TAG_TRANSLATION]) + struct.pack('>I', 0xFFFFFFFF)
    out += bytes([TAG_COMMENT]) + struct.pack('>I', 0)
    out += bytes([TAG_SOURCE]) + struct.pack('>I', 0)
    out += bytes([TAG_CONTEXT]) + struct.pack('>I', 7) + b'AboutDi'
    out += bytes([TAG_END])
    return out
