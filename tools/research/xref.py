#!/usr/bin/env python3
"""Find xrefs (RIP-relative lea/mov) from .text to given target file offsets."""
import struct, sys

path = sys.argv[1]
raw = open(path, 'rb').read()
targets = [int(t, 16) for t in sys.argv[2:]]

e_lfanew = struct.unpack_from('<I', raw, 0x3C)[0]
coff = e_lfanew + 4
_, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', raw, coff)
opt = coff + 20
imagebase = struct.unpack_from('<Q', raw, opt + 24)[0]
sec_off = opt + optsz
sections = []
for i in range(nsec):
    o = sec_off + i*40
    name = raw[o:o+8].rstrip(b'\0').decode('latin-1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', raw, o+8)
    sections.append((name, va, vsz, ptr, rsz))

def off2va(off):
    for name, va, vsz, ptr, rsz in sections:
        if ptr <= off < ptr + rsz:
            return imagebase + va + (off - ptr)
    return None

def va2off(va):
    for name, vva, vsz, ptr, rsz in sections:
        if vva <= va < vva + max(vsz, rsz):
            return ptr + (va - vva)
    return None

tvas = {off2va(t): t for t in targets}
print(f'ImageBase = 0x{imagebase:X}')
for va, off in tvas.items():
    print(f'  target fileoff 0x{off:X} -> VA 0x{va:X}')
print()

tname = next((n for n, va, vsz, ptr, rsz in sections if n == '.text'), None)
tva, tptr, trsz = next(((va, ptr, rsz) for n, va, vsz, ptr, rsz in sections if n == '.text'))
code = raw[tptr:tptr+trsz]
print(f'scanning .text  {trsz:,} bytes @ file 0x{tptr:X}')

hits = {}
# lea/mov with RIP-relative: REX.W/REX.R prefix + 8D/8B + modrm(mod=00,rm=101) + disp32
i = 0
n = len(code)
while i < n - 7:
    b = code[i]
    is_rex = (b & 0xF0) == 0x40
    len_prefix = 1 if is_rex else 0
    op = code[i+len_prefix]
    if op in (0x8D, 0x8B):
        modrm = code[i+len_prefix+1]
        if (modrm & 0xC7) == 0x05:  # mod=00, rm=101 (RIP-relative)
            disp = struct.unpack_from('<i', code, i+len_prefix+2)[0]
            rip = (tva + i + len_prefix + 6)
            tva_r = imagebase + rip + disp
            for want_va, want_off in tvas.items():
                if tva_r == want_va:
                    hits.setdefault(want_off, []).append(tptr + i)
    i += 1

for off, addrs in hits.items():
    print()
    print(f'=== xrefs to fileoff 0x{off:X} (VA 0x{off2va(off):X}) : {len(addrs)} ===')
    for a in addrs:
        # find the containing function start heuristically: scan back for padding/int3 run
        fstart = a
        while fstart > tptr and raw[fstart-1] not in (0xCC, 0xC3, 0x90, 0x00):
            fstart -= 1
        fstart += 1
        print(f'  xref @file 0x{a:X}  (VA 0x{off2va(a):X})   ~func start 0x{fstart:X}')
        seg = raw[fstart:fstart+0x180]
        for m in __import__('re').finditer(rb'[\x20-\x7e]{4,}', seg):
            print(f'        str +0x{m.start():03X}: {m.group().decode("latin-1")}')
        for m in __import__('re').finditer(rb'(?:[\x20-\x7e]\x00){3,}', seg):
            print(f'        w16 +0x{m.start():03X}: {m.group().decode("utf-16-le")}')
