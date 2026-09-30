"""Read-only, mmap-backed access to a binary file.

Every research tool needs the same three things: find a byte pattern, dump a
hex range, and pull a NUL-terminated string.  Centralising them here keeps the
tools themselves short and keeps the "which encoding?" decisions in one place.
"""
import mmap
import re

# Printable-ASCII runs.  Deliberately conservative: we annotate disassembly with
# these, and a wrong annotation is worse than none.
_ASCII_RUN = re.compile(rb'[\x20-\x7e]{4,}')
_UTF16LE_RUN = re.compile(rb'(?:[\x20-\x7e]\x00){3,}')

# Zlib streams as produced by .NET / Qt / Steinberg packers.
_ZLIB = re.compile(rb'\x78[\x01\x5e\x9c\xda]')


class Binary:
    """A binary file opened read-only and memory-mapped."""

    def __init__(self, path):
        self.path = str(path)
        self._fh = open(self.path, 'rb')
        self.size = 0
        try:
            self._mm = mmap.mmap(self._fh.fileno(), 0, access=mmap.ACCESS_READ)
            self.size = len(self._mm)
        except ValueError:            # empty file
            self._mm = b''
        self.data = self._mm

    # -- lifecycle ---------------------------------------------------------
    def close(self):
        if isinstance(self._mm, mmap.mmap):
            self._mm.close()
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def __len__(self):
        return self.size

    # -- slicing -----------------------------------------------------------
    def __getitem__(self, key):
        return self.data[key]

    def slice(self, off, length):
        """Clamped read; returns b'' past EOF instead of raising."""
        if off < 0 or off >= self.size:
            return b''
        return self.data[off:min(self.size, off + length)]

    # -- searching ---------------------------------------------------------
    def find(self, pattern, start=0, limit=None):
        """Every file offset where `pattern` occurs."""
        out, pos = [], max(0, start)
        while True:
            i = self.data.find(pattern, pos)
            if i < 0:
                return out
            out.append(i)
            pos = i + 1
            if limit and len(out) >= limit:
                return out

    def find_all(self, pattern, start=0, limit=None):
        return self.find(pattern, start, limit)

    def rfind_enclosing(self, offset, pattern):
        """Last occurrence of `pattern` at or before `offset` (-1 if none)."""
        return self.data.rfind(pattern, 0, offset + len(pattern))

    def zlib_starts(self, start=0, limit=None):
        """Offsets that plausibly begin a zlib stream."""
        out = []
        for m in _ZLIB.finditer(self.data, start):
            out.append(m.start())
            if limit and len(out) >= limit:
                break
        return out

    # -- strings -----------------------------------------------------------
    def cstr(self, off, encoding='ascii', maxlen=256):
        """NUL-terminated string at `off`, or None."""
        if not (0 <= off < self.size):
            return None
        end = self.data.find(b'\x00', off, off + maxlen)
        if end < 0:
            return None
        raw = self.data[off:end]
        if not raw:
            return ''
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            return None

    def read_str(self, off, wide=False, maxn=200):
        """Best-effort printable string at `off` (ASCII or UTF-16LE)."""
        if not (0 <= off < self.size):
            return None
        if wide:
            m = _UTF16LE_RUN.match(self.data[off:off + maxn * 2])
            if m:
                return m.group().decode('utf-16-le')
            return None
        m = _ASCII_RUN.match(self.data[off:off + maxn])
        return m.group().decode() if m else None

    def strings_ascii(self, lo, hi, minlen=4):
        return [(m.start(), m.group().decode('latin-1'))
                for m in _ASCII_RUN.finditer(self.data, lo, hi)
                if len(m.group()) >= minlen]

    def strings_utf16(self, lo, hi, minlen=3):
        pat = re.compile(rb'(?:[\x20-\x7e]\x00){%d,}' % minlen)
        return [(m.start(), m.group().decode('utf-16-le'))
                for m in pat.finditer(self.data, lo, hi)]

    # -- display -----------------------------------------------------------
    def hexdump(self, off, length, width=16, base=0):
        lines = []
        for i in range(0, length, width):
            chunk = self.slice(off + i, width)
            if not chunk:
                break
            hexpart = ' '.join(f'{c:02x}' for c in chunk).ljust(width * 3)
            text = ''.join(chr(c) if 32 <= c < 127 else '.' for c in chunk)
            lines.append(f'{base + off + i:08X}  {hexpart}  {text}')
        return '\n'.join(lines)

    def printable(self, off, length=64, wide=False):
        chunk = self.slice(off, length * (2 if wide else 1))
        if wide:
            return chunk.decode('utf-16-le', 'replace')
        return ''.join(chr(c) if 32 <= c < 127 else '.' for c in chunk)
