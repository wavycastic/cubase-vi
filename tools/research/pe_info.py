#!/usr/bin/env python3
import struct, sys, mmap, re, collections

path = sys.argv[1]
raw = open(path, 'rb').read()
print(f'file size = {len(raw):,}  (0x{len(raw):X})')

# ---- DOS header ----
assert raw[:2] == b'MZ'
e_lfanew = struct.unpack_from('<I', raw, 0x3C)[0]
assert raw[e_lfanew:e_lfanew+4] == b'PE\0\0', 'not a PE'

# ---- COFF ----
coff = e_lfanew + 4
machine, nsec, tds, psym, nsym, optsz, chars = struct.unpack_from('<HHIIIHH', raw, coff)
opt = coff + 20
magic = struct.unpack_from('<H', raw, opt)[0]
pe32plus = (magic == 0x20B)
print(f'machine=0x{machine:04X} sections={nsec} optmagic=0x{magic:04X} ({"PE32+" if pe32plus else "PE32"})')

# data directories
if pe32plus:
    ndirs = struct.unpack_from('<I', raw, opt + 108)[0]
    dirs_off = opt + 112
else:
    ndirs = struct.unpack_from('<I', raw, opt + 92)[0]
    dirs_off = opt + 96
DIRNAMES = ['Export','Import','Resource','Exception','Certificate','BaseReloc',
            'Debug','Architecture','GlobalPtr','TLS','LoadConfig','BoundImport',
            'IAT','DelayImport','CLR','Reserved']
print(f'data directories = {ndirs}')
rva2size = {}
for i in range(min(ndirs, 16)):
    rva, size = struct.unpack_from('<II', raw, dirs_off + i*8)
    rva2size[i] = (rva, size)
    if size:
        print(f'  [{i:2}] {DIRNAMES[i]:14} rva=0x{rva:08X} size={size:,}')

sec_off = opt + optsz
sections = []
print()
print('--- sections ---')
for i in range(nsec):
    o = sec_off + i*40
    name = raw[o:o+8].rstrip(b'\0').decode('latin-1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', raw, o+8)
    schar = struct.unpack_from('<I', raw, o+36)[0]
    sections.append((name, va, vsz, ptr, rsz))
    print(f'  {name:9} VirtAddr=0x{va:08X} VirtSize=0x{vsz:08X}  RawPtr=0x{ptr:08X} RawSize=0x{rsz:08X}')

def rva_to_off(rva):
    for name, va, vsz, ptr, rsz in sections:
        if va <= rva < va + max(vsz, rsz):
            return ptr + (rva - va)
    return None

TARGET = 0x07B79180
print()
print(f'--- which section holds XML @0x{TARGET:08X} ? ---')
for name, va, vsz, ptr, rsz in sections:
    if ptr <= TARGET < ptr + rsz:
        off_in = TARGET - ptr
        print(f'  section {name}: file offset {ptr} + {off_in} = {TARGET}  (section ends @0x{ptr+rsz:X})')
        print(f'  bytes from XML start to end of section = {ptr+rsz-TARGET:,}')

# ---- resource dir: enumerate leaf data entries ----
print()
print('--- PE resource leaf data entries (large / containing XML) ---')
rrva, rsize = rva2size.get(2, (0,0))
if rrva:
    rbase = rva_to_off(rrva)
    print(f'  .rsrc dir rva=0x{rrva:08X} -> file 0x{rbase:X}, total size {rsize:,}')
    leaves = []
    def resdir(off, level=0, prefix=''):
        nnamed, nid = struct.unpack_from('<HH', raw, off+12)
        n = nnamed + nid
        for i in range(n):
            e = off + 16 + i*8
            nameoff, dataoff = struct.unpack_from('<II', raw, e)
            if nameoff & 0x80000000:
                label = 'NAMED'
            else:
                label = str(nameoff)
            if dataoff & 0x80000000:
                resdir(rbase + (dataoff & 0x7FFFFFFF), level+1, prefix + '/' + label)
            else:
                leaf = rbase + dataoff
                drva, dsz, dcp, _ = struct.unpack_from('<IIII', raw, leaf)
                doff = rva_to_off(drva)
                leaves.append((prefix+'/'+label, drva, doff, dsz, dcp))
    resdir(rbase)
    print(f'  total leaf resources: {len(leaves)}')
    TARGET = 0x07B79180
    for lbl, drva, doff, dsz, dcp in sorted(leaves, key=lambda x: -(x[3] or 0))[:15]:
        hit = '  <== CONTAINS XML' if (doff is not None and doff <= TARGET < doff + dsz) else ''
        print(f'  {lbl:28} rva=0x{drva:08X} off=0x{(doff or 0):X} size={dsz:>10,}{hit}')
    print()
    for lbl, drva, doff, dsz, dcp in leaves:
        if doff is not None and doff <= TARGET < doff + dsz:
            print(f'  *** resource {lbl}: declared size {dsz:,}, cp={dcp}')
            print(f'      first 64 bytes: {raw[doff:doff+64]!r}')
            print(f'      last  64 bytes: {raw[doff+dsz-64:doff+dsz]!r}')
            slack_to_next = None
            nxt = min([l[2] for l in leaves if l[2] and l[2] > doff] or [None])
            if nxt: print(f'      bytes to next resource: {nxt - doff:,}  (slack after this one: {nxt - (doff+dsz):,})')
            print(f'      tail zero padding inside declared size: {dsz - len(raw[doff:doff+dsz].rstrip(b"\0")):,}')
