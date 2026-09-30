"""Synthetic Qt .qm builder, so the reader can be tested without Cubase."""
import struct

MAGIC = bytes.fromhex('3cb86418caef9c95cd211cbf60a1bddd')

TAG_END = 1
TAG_SOURCE16 = 2
TAG_TRANSLATION = 3
TAG_CONTEXT16 = 4
TAG_SOURCE = 6
TAG_CONTEXT = 7
TAG_COMMENT = 8


def block(tag, payload):
    """One block.  Lengths are big-endian - getting this wrong yields
    plausible-looking but wildly wrong sizes."""
    return bytes([tag]) + struct.pack('>I', len(payload)) + payload


def utf16(s):
    return s.encode('utf-16-be')


def message(source, translation, context='', wide=True, comment=''):
    """One Messages-block record.

    `Tag_Translation` is always UTF-16 in the Qt format; `wide` only controls
    whether the source and context use the 16-bit tags or the 8-bit ones, which
    is the mix real catalogues actually contain.
    """
    out = b''
    if translation:
        out += bytes([TAG_TRANSLATION]) + struct.pack('>I', len(utf16(translation))) \
            + utf16(translation)
    if source:
        if wide:
            out += bytes([TAG_SOURCE16]) + struct.pack('>I', len(utf16(source))) \
                + utf16(source)
        else:
            out += bytes([TAG_SOURCE]) + struct.pack('>I', len(source)) \
                + source.encode('utf-8')
    if context:
        if wide:
            out += bytes([TAG_CONTEXT16]) + struct.pack('>I', len(utf16(context))) \
                + utf16(context)
        else:
            out += bytes([TAG_CONTEXT]) + struct.pack('>I', len(context)) \
                + context.encode('utf-8')
    if comment:
        out += bytes([TAG_COMMENT]) + struct.pack('>I', len(comment)) \
            + comment.encode('utf-8')
    return out + bytes([TAG_END])


def catalogue(messages, context='TestDialog', slots=None, raw_messages=None):
    """Build a complete .qm.  `messages` is a list of (source, translation).

    lrelease sizes the hash table at exactly twice the number of entries, with
    a single empty slot - which is what lets the reader sanity-check that it
    recovered everything.  The Contexts block is the raw locale name with no
    length prefix, matching what the real Steinberg catalogues contain.
    """
    if raw_messages is not None:
        msg_block = raw_messages
    else:
        msg_block = b''.join(
            message(src, tr, context if i == 0 else '')
            for i, (src, tr) in enumerate(messages))
    if slots is None:
        slots = 2 * len(messages)
    hashes = b''.join(struct.pack('>I', i + 1) for i in range(len(messages)))
    hashes += b'\x00\x00\x00\x00' * (slots - len(messages))
    out = MAGIC
    if context:
        out += block(0x2F, context.encode('utf-8'))
    out += block(0x42, hashes)
    out += block(0x69, msg_block)
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
