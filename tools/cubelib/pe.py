"""PE32 / PE32+ parsing.

Covers what reverse engineering a Steinberg binary actually needs:

  * section table and RVA <-> file-offset translation (both directions)
  * data directories, including the exception directory (`.pdata`) that gives
    exact function boundaries on x64
  * the resource tree, so RCDATA payloads such as `TRANSLATION.XML` can be
    located by name instead of a hardcoded offset

Nothing here is x86 specific and nothing is Cubase specific.
"""
import struct
from dataclasses import dataclass

from .binary import Binary

DATA_DIRS = ['Export', 'Import', 'Resource', 'Exception', 'Certificate',
             'BaseReloc', 'Debug', 'Architecture', 'GlobalPtr', 'TLS',
             'LoadConfig', 'BoundImport', 'IAT', 'DelayImport', 'CLR',
             'Reserved']

RES_TYPES = {1: 'CURSOR', 2: 'BITMAP', 3: 'ICON', 4: 'MENU', 5: 'DIALOG',
             6: 'STRING', 7: 'FONTDIR', 8: 'FONT', 9: 'ACCELERATOR',
             10: 'RCDATA', 11: 'MESSAGETABLE', 12: 'GROUP_CURSOR',
             14: 'GROUP_ICON', 16: 'VERSION', 24: 'MANIFEST'}


class PEError(ValueError):
    """The file is not a PE image we can parse."""


@dataclass(frozen=True)
class Section:
    name: str
    vaddr: int
    vsize: int
    raw_ptr: int
    raw_size: int
    characteristics: int

    @property
    def span(self):
        return max(self.vsize, self.raw_size)

    def contains_rva(self, rva):
        return self.vaddr <= rva < self.vaddr + self.span

    def contains_off(self, off):
        return self.raw_ptr <= off < self.raw_ptr + self.raw_size


@dataclass(frozen=True)
class Resource:
    path: tuple          # (type, name-or-id, name-or-id, lang)
    rva: int
    off: int
    size: int
    codepage: int
    lang: int

    @property
    def type_name(self):
        first = self.path[0] if self.path else None
        if isinstance(first, int):
            return RES_TYPES.get(first, f'#{first}')
        return str(first)

    @property
    def label(self):
        return '/'.join(str(p) for p in self.path)

    def __iter__(self):
        """Unpack as (label, rva, off, size) - matches the old scripts' tuples."""
        return iter((self.label, self.rva, self.off, self.size))


class PE:
    """A parsed PE image backed by a read-only mmap."""

    def __init__(self, source):
        self.bin = source if isinstance(source, Binary) else Binary(source)
        self._parse_headers()
        self._resources = None
        self._functions = None

    # -- construction ------------------------------------------------------
    @classmethod
    def open(cls, path):
        return cls(Binary(path))

    def close(self):
        self.bin.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def _u16(self, off):
        return struct.unpack_from('<H', self.bin.data, off)[0]

    def _u32(self, off):
        return struct.unpack_from('<I', self.bin.data, off)[0]

    def _u64(self, off):
        return struct.unpack_from('<Q', self.bin.data, off)[0]

    def _parse_headers(self):
        d = self.bin.data
        if d[:2] != b'MZ':
            raise PEError('not a PE image (missing MZ)')
        e_lfanew = self._u32(0x3C)
        if d[e_lfanew:e_lfanew + 4] != b'PE\0\0':
            raise PEError('missing PE signature')

        coff = e_lfanew + 4
        (self.machine, self.nsec, _tds, _psym, _nsym,
         optsz, self.characteristics) = struct.unpack_from('<HHIIIHH', d, coff)

        opt = coff + 20
        magic = self._u16(opt)
        if magic == 0x20B:
            self.is_pe32plus = True
            self.imagebase = self._u64(opt + 24)
            self.ndatadirs = self._u32(opt + 108)
            self._dirs_off = opt + 112
        elif magic == 0x10B:
            self.is_pe32plus = False
            self.imagebase = self._u32(opt + 28)
            self.ndatadirs = self._u32(opt + 92)
            self._dirs_off = opt + 96
        else:
            raise PEError(f'unknown optional header magic 0x{magic:04X}')

        self.sections = []
        sec_off = opt + optsz
        for i in range(self.nsec):
            o = sec_off + i * 40
            name = d[o:o + 8].rstrip(b'\0').decode('latin-1')
            vsz, va, rsz, ptr = struct.unpack_from('<IIII', d, o + 8)
            chars = self._u32(o + 36)
            self.sections.append(Section(name, va, vsz, ptr, rsz, chars))

    # -- addresses ---------------------------------------------------------
    def section(self, name):
        for s in self.sections:
            if s.name == name:
                return s
        return None

    def rva_to_off(self, rva):
        for s in self.sections:
            if s.contains_rva(rva):
                return s.raw_ptr + (rva - s.vaddr)
        return None

    def off_to_rva(self, off):
        for s in self.sections:
            if s.contains_off(off):
                return s.vaddr + (off - s.raw_ptr)
        return None

    def va_to_off(self, va):
        if va is None or va < self.imagebase:
            return None
        return self.rva_to_off(va - self.imagebase)

    def off_to_va(self, off):
        rva = self.off_to_rva(off)
        return None if rva is None else self.imagebase + rva

    def resolve(self, value):
        """Interpret `value` as a file offset, RVA or VA and return (off, kind).

        Lets the CLI accept whatever the user has in front of them without
        caring which addressing mode a given tool expects.
        """
        if value is None:
            return None, None
        if 0 <= value < self.bin.size and self.off_to_rva(value) is not None:
            return value, 'offset'
        off = self.va_to_off(value)
        if off is not None:
            return off, 'va'
        off = self.rva_to_off(value)
        if off is not None:
            return off, 'rva'
        return None, None

    # -- data directories --------------------------------------------------
    def data_dirs(self):
        out = {}
        for i in range(min(self.ndatadirs, len(DATA_DIRS))):
            rva, size = struct.unpack_from('<II', self.bin.data,
                                           self._dirs_off + i * 8)
            out[DATA_DIRS[i]] = (rva, size)
        return out

    def data_dir(self, name):
        return self.data_dirs().get(name, (0, 0))

    # -- functions (x64 exception directory) -------------------------------
    def functions(self):
        """(begin_rva, end_rva) for every function listed in .pdata.

        This is the authoritative function map on x64: it is what the loader
        itself uses for unwinding, so it is exact rather than heuristic.
        Returns [] for 32-bit images.
        """
        if self._functions is not None:
            return self._functions
        rva, size = self.data_dir('Exception')
        out = []
        if rva and size:
            base = self.rva_to_off(rva)
            if base is not None:
                d = self.bin.data
                for o in range(base, base + size - 11, 12):
                    beg, end, _unwind = struct.unpack_from('<III', d, o)
                    if 0 < beg < end:
                        out.append((beg, end))
        out = sorted(set(out))
        self._functions = out
        return out

    def function_containing(self, rva):
        """Smallest .pdata function whose range covers `rva`, else None."""
        best = None
        for beg, end in self.functions():
            if beg <= rva < end:
                if best is None or (end - beg) < (best[1] - best[0]):
                    best = (beg, end)
        return best

    def function_containing_off(self, off):
        rva = self.off_to_rva(off)
        return None if rva is None else self.function_containing(rva)

    # -- resources ---------------------------------------------------------
    def resources(self):
        """Every resource leaf, as Resource(path, rva, off, size, ...)."""
        if self._resources is not None:
            return self._resources
        rva, _size = self.data_dir('Resource')
        if not rva:
            self._resources = []
            return self._resources
        base = self.rva_to_off(rva)
        if base is None:
            self._resources = []
            return self._resources

        out = []

        def name_of(nameoff):
            if not (nameoff & 0x80000000):
                return nameoff
            o = base + (nameoff & 0x7FFFFFFF)
            n = self._u16(o)
            return self.bin.data[o + 2:o + 2 + n * 2].decode('utf-16-le', 'replace')

        def walk(off, path):
            nnamed, nid = struct.unpack_from('<HH', self.bin.data, off + 12)
            for i in range(nnamed + nid):
                nameoff, dataoff = struct.unpack_from(
                    '<II', self.bin.data, off + 16 + i * 8)
                child = name_of(nameoff) if (nameoff & 0x80000000) else nameoff
                sub = path + (child,)
                if dataoff & 0x80000000:
                    walk(base + (dataoff & 0x7FFFFFFF), sub)
                else:
                    leaf = base + dataoff
                    drva, dsz, dcp, _rs = struct.unpack_from('<IIII', self.bin.data, leaf)
                    doff = self.rva_to_off(drva)
                    if doff is not None:
                        out.append(Resource(sub, drva, doff, dsz, dcp,
                                            sub[-1] if isinstance(sub[-1], int) else 0))

        walk(base, ())
        self._resources = out
        return self._resources

    def find_resource(self, name, type_=None):
        """First resource whose path component matches `name` (case-insensitive)."""
        want = name.upper()
        for r in self.resources():
            if any(str(p).upper() == want for p in r.path):
                if type_ is None or r.type_name == type_:
                    return r
        return None

    def resource_bytes(self, name):
        r = self.find_resource(name)
        return None if r is None else self.bin.slice(r.off, r.size)

    def iter_resources_by_size(self, limit=20):
        return sorted(self.resources(), key=lambda r: -r.size)[:limit]

    # -- summary -----------------------------------------------------------
    def describe(self):
        d = self.bin
        lines = [f'{self.bin.path}',
                 f'  size {len(d):,} (0x{len(d):X})',
                 f'  machine 0x{self.machine:04X}  sections {self.nsec}  '
                 f'{"PE32+" if self.is_pe32plus else "PE32"}',
                 f'  imagebase 0x{self.imagebase:X}']
        lines.append('  sections:')
        for s in self.sections:
            lines.append(f'    {s.name:9} vaddr=0x{s.vaddr:08X} vsize=0x{s.vsize:08X} '
                         f'ptr=0x{s.raw_ptr:08X} rsize=0x{s.raw_size:08X}')
        lines.append('  data directories:')
        for name, (rva, size) in self.data_dirs().items():
            if size:
                lines.append(f'    {name:12} rva=0x{rva:08X} size={size:,}')
        fns = self.functions()
        if fns:
            lines.append(f'  functions from .pdata: {len(fns):,}')
        return '\n'.join(lines)
