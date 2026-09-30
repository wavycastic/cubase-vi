"""Steinberg Resource File (`.srf`) reader.

`Skins/skin.srf` ships the entire Cubase interface skin - window templates,
colours, geometry and every icon - as one 20 MB blob.  It is not encrypted and
not obfuscated: it is a flat sequence of members, each preceded by a leftover
name line and then either a zlib stream or a stored image.

Being able to unpack it means the whole visual design of Cubase is editable.
Text is *not* a separate translation surface: the `title="..."` attributes in
the skin XML are keys looked up in `translation.xml`, so the existing
Vietnamese pipeline keeps working while the theme changes around it.
"""
import struct
import zlib
from collections import Counter
from dataclasses import dataclass, field

SRF_MAGIC = b'Steinberg Resource File'
# Steinberg's packer writes this name before every member regardless of what the
# member actually is; it is a build artefact, not a real per-file name.
LEFTOVER_NAME = b'/Thumbs.db\r\n'

KIND_XML = 'xml'
KIND_SKIN = 'skin'
KIND_PNG = 'png'
KIND_BMP = 'bmp'
KIND_DIB = 'dib'
KIND_SVG = 'svg'
KIND_OTHER = 'other'


class SRFError(ValueError):
    pass


@dataclass
class Member:
    index: int
    offset: int             # file offset of the member body
    stored_size: int        # bytes occupied in the file
    size: int               # decoded size
    kind: str
    detail: str = ''
    payload: bytes = field(default=b'', repr=False)

    @property
    def compressed(self):
        return self.stored_size < self.size

    def head(self, n=24):
        return self.payload[:n]


def _classify(blob):
    head = blob[:8]
    if head[:4] == b'\x89PNG':
        return KIND_PNG, ''
    if head[:2] == b'BM':
        return KIND_BMP, ''
    # A bare DIB: BITMAPINFOHEADER with biSize == 40 and no file header.
    if len(blob) >= 4 and struct.unpack_from('<I', blob, 0)[0] == 40:
        return KIND_DIB, ''
    # The skin chunks are XML but may open with comments, a blank line or a
    # BOM, so classify on the first non-whitespace character.
    text = blob.lstrip(b'\xef\xbb\xbf \t\r\n')
    if text[:1] == b'<':
        if text[:5] == b'<skin':
            return KIND_SKIN, ''
        if text[:4] == b'<svg':
            return KIND_SVG, ''
        if text[:5] == b'<?xml':
            return KIND_XML, ''
        # A comment-only fragment is still part of the skin description
        if text[:4] == b'<!--':
            return KIND_XML, ''
        return KIND_XML, ''
    return KIND_OTHER, head[:8].hex(' ')


def png_size(blob):
    i = blob.find(b'IHDR')
    if i < 0 or i + 12 > len(blob):
        return None
    w, h = struct.unpack_from('>II', blob, i + 4)
    return w, h


class SRF:
    """A parsed Steinberg Resource File."""

    def __init__(self, data, path='<bytes>'):
        self.data = data
        self.path = path
        self.members = []
        self.trailing = b''
        self.trailing_offset = 0

    @classmethod
    def load(cls, path):
        return cls(open(path, 'rb').read(), path=str(path))

    # -- parsing -----------------------------------------------------------
    def _parse(self):
        d = self.data
        if not d.startswith(SRF_MAGIC):
            raise SRFError('not a Steinberg Resource File')
        pos = d.find(LEFTOVER_NAME)
        pos = len(SRF_MAGIC) if pos < 0 else pos + len(LEFTOVER_NAME)
        index = 0
        while pos < len(d):
            if d[pos:pos + len(LEFTOVER_NAME)] == LEFTOVER_NAME:
                pos += len(LEFTOVER_NAME)
                if pos >= len(d):
                    break
            if d[pos:pos + 4] == b'\x89PNG':
                end = d.find(b'IEND', pos)
                if end < 0:
                    break
                end += 8
                payload = d[pos:end]
                kind, detail = KIND_PNG, ''
                stored = end - pos
            elif d[pos:pos + 2] in (b'\x78\x9c', b'\x78\xda', b'\x78\x01', b'\x78\x5e'):
                do = zlib.decompressobj()
                try:
                    payload = do.decompress(d[pos:])
                except zlib.error:
                    pos += 1
                    continue
                kind, detail = _classify(payload)
                stored = len(d) - pos - len(do.unused_data)
            else:
                break
            self.members.append(Member(index, pos, stored, len(payload), kind,
                                       detail, payload))
            index += 1
            pos += stored
        self.trailing_offset = pos
        self.trailing = d[pos:]
        return self.members

    def __iter__(self):
        if not self.members and not self.trailing:
            self._parse()
        return iter(self.members)

    def __len__(self):
        if not self.members and not self.trailing:
            self._parse()
        return len(self.members)

    # -- queries -----------------------------------------------------------
    def by_kind(self, kind):
        return [m for m in self if m.kind == kind]

    def xml_members(self):
        return [m for m in self if m.kind in (KIND_XML, KIND_SKIN)]

    def skin_xml(self):
        """All XML payloads concatenated, in file order."""
        return b''.join(m.payload for m in self if m.kind in (KIND_XML, KIND_SKIN))

    def images(self):
        return [m for m in self if m.kind in (KIND_PNG, KIND_BMP, KIND_DIB)]

    def image_dimensions(self):
        """Counter of (width, height) -> number of images."""
        out = Counter()
        for m in self.images():
            if m.kind == KIND_PNG:
                wh = png_size(m.payload)
            elif m.kind == KIND_BMP:
                wh = bmp_size(m.payload)
            else:
                wh = dib_size(m.payload)
            if wh and wh[0] and wh[1]:
                out[wh] += 1
        return out

    def names(self):
        """Strings from the trailing name table, if one is present."""
        import re
        return [m.group().decode('latin-1')
                for m in re.finditer(rb'[\x20-\x7e]{3,60}', self.trailing)]

    # -- reporting ---------------------------------------------------------
    def summary(self):
        lines = [f'{self.path}',
                 f'  {len(self.data):,} bytes, {len(self)} members, '
                 f'{len(self.trailing):,} trailing bytes at 0x{self.trailing_offset:X}']
        agg = {}
        for m in self:
            a = agg.setdefault(m.kind, [0, 0, 0])
            a[0] += 1
            a[1] += m.stored_size
            a[2] += m.size
        lines.append('  kind      count      stored          decoded')
        for k, (c, st, dec) in sorted(agg.items(), key=lambda kv: -kv[1][2]):
            lines.append(f'  {k:9} {c:>6} {st:>13,} {dec:>15,}')
        pct = 100 * sum(m.stored_size for m in self) / max(1, len(self.data))
        lines.append(f'  accounted for {pct:.1f}% of the file')
        return '\n'.join(lines)


def bmp_size(blob):
    if len(blob) < 26:
        return None
    w, h = struct.unpack_from('<ii', blob, 18)
    return abs(w), abs(h)


def dib_size(blob):
    if len(blob) < 20:
        return None
    w, h = struct.unpack_from('<ii', blob, 4)
    return abs(w), abs(h)
