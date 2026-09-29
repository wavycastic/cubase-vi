#!/usr/bin/env python3
import struct, sys, re

path = sys.argv[1]
raw = open(path, 'rb').read()

e_lfanew = struct.unpack_from('<I', raw, 0x3C)[0]
coff = e_lfanew + 4
_, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', raw, coff)
opt = coff + 20
pe32plus = struct.unpack_from('<H', raw, opt)[0] == 0x20B
dirs_off = opt + (112 if pe32plus else 96)
sec_off = opt + optsz
sections = []
for i in range(nsec):
    o = sec_off + i*40
    name = raw[o:o+8].rstrip(b'\0').decode('latin-1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', raw, o+8)
    sections.append((name, va, vsz, ptr, rsz))

def rva_to_off(rva):
    for name, va, vsz, ptr, rsz in sections:
        if va <= rva < va + max(vsz, rsz):
            return ptr + (rva - va)
    return None

rrva, rsize = struct.unpack_from('<II', raw, dirs_off + 2*8)
rbase = rva_to_off(rrva)

def rname(raw, nameoff):
    if nameoff & 0x80000000:
        o = rbase + (nameoff & 0x7FFFFFFF)
        ln = struct.unpack_from('<H', raw, o)[0]
        return raw[o+2:o+2+ln*2].decode('utf-16-le')
    return None

TYPES = {1:'CURSOR',2:'BITMAP',3:'ICON',4:'MENU',5:'DIALOG',6:'STRING',7:'FONTDIR',
         8:'FONT',9:'ACCELERATOR',10:'RCDATA',11:'MESSAGETABLE',12:'GROUP_CURSOR',
         14:'GROUP_ICON',16:'VERSION',24:'MANIFEST'}

rows = []
def walk(off, prefix):
    nnamed, nid = struct.unpack_from('<HH', raw, off+12)
    for i in range(nnamed+nid):
        e = off + 16 + i*8
        no, do = struct.unpack_from('<II', raw, e)
        tname = rname(raw, no) or TYPES.get(prefix[0] if prefix else 0, f'{prefix[0] if prefix else 0}')
        if do & 0x80000000:
            walk(rbase + (do & 0x7FFFFFFF), prefix + [tname])
        else:
            drva, dsz, dcp, _ = struct.unpack_from('<IIII', raw, rbase + do)
            rows.append(('/'.join(map(str,prefix))+('/'+tname if tname else ''), rva_to_off(drva), dsz, tname))

walk(rbase, [])
print('--- all resources (sorted by file offset) ---')
for lbl, off, dsz, tname in sorted(rows, key=lambda r: r[1] or 0):
    head = raw[off:off+48]
    pv = head[:24]
    print(f'  {lbl:24} type={tname:12} off=0x{off:X} size={dsz:>10,}  head={pv!r}')

print()
print('=== hunting for external-language-file support in .rdata/.data ===')
pats = [b'Translation', b'translation.xml', b'.xml', b'l10n', b'LanguageTable',
        b'StringTable', b'Localization', b'localization', b'LocalizationFile',
        b'\\\\lang', b'AppLang', b'UILang']
for p in pats:
    idxs, pos = [], 0
    while len(idxs) < 8:
        i = raw.find(p, pos)
        if i < 0: break
        idxs.append(i); pos = i+1
    if idxs:
        print(f'  {p!r}: {len(idxs)} hit(s) -> {[hex(i) for i in idxs[:8]]}')
        for i in idxs[:3]:
            seg = raw[max(0,i-70):i+90]
            txt = ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg)
            print(f'      {txt}')
