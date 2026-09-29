#!/usr/bin/env python3
"""Extract the TRANSLATION.XML resource from a Steinberg PE and dump stats."""
import struct, sys, re, os, json, collections

path = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else 'translation.xml'
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

rrva, _ = struct.unpack_from('<II', raw, dirs_off + 2*8)
rbase = rva_to_off(rrva)

def rname(nameoff):
    if nameoff & 0x80000000:
        o = rbase + (nameoff & 0x7FFFFFFF)
        ln = struct.unpack_from('<H', raw, o)[0]
        return raw[o+2:o+2+ln*2].decode('utf-16-le')
    return None

found = None
def walk(off, names=()):
    global found
    nnamed, nid = struct.unpack_from('<HH', raw, off+12)
    for i in range(nnamed+nid):
        e = off + 16 + i*8
        no, do = struct.unpack_from('<II', raw, e)
        nm = rname(no)
        names2 = names + ((nm,) if nm else ())
        if do & 0x80000000:
            walk(rbase + (do & 0x7FFFFFFF), names2)
        else:
            drva, dsz, dcp, _ = struct.unpack_from('<IIII', raw, rbase + do)
            doff = rva_to_off(drva)
            if any((n or '').upper() == 'TRANSLATION.XML' for n in names2):
                found = (doff, dsz, names2)
walk(rbase)

if not found:
    raise SystemExit('TRANSLATION.XML resource not found')
doff, dsz, path = found
print(f'resource path: {path}')
xml = raw[doff:doff+dsz]
print(f'resource at file 0x{doff:X}, {dsz:,} bytes')
print(f'starts: {xml[:60]!r}')
print(f'ends  : {xml[-40:]!r}')

open(out, 'wb').write(xml)
print(f'wrote {out} ({os.path.getsize(out):,} bytes)')

txt = xml.decode('utf-8')
langs = re.findall(r'<language key="([^"]+)">([^<]*)</language>', txt)
print(f'\nlanguages ({len(langs)}): {langs}')

strings = re.findall(r'<String Key="((?:[^"]|"(?!>))*?)">', txt)
print(f'String entries: {len(strings):,}')

# how often does Key equal the <us> value?
m = re.findall(r'<String Key="(.*?)">\s*<us>(.*?)</us>', txt, re.S)
same = sum(1 for k, u in m if k == u)
print(f'Key == us  : {same:,} / {len(m):,}  ({same*100//max(1,len(m))}%)')

# look for the main top-level menus
print('\n--- main menus present? ---')
for probe in ['File', 'Edit', 'Project', 'Audio', 'MIDI', 'Media', 'Transport',
              'Devices', 'Window', 'Help', 'Studio', 'Scores', 'Plug-ins', 'Nudge',
              'Mixer', 'VST Connections', 'Audio Connections']:
    hit = re.search(r'<String Key="' + re.escape(probe) + r'">\s*<us>([^<]*)</us>', txt)
    print(f'  {probe:20} -> {"HIT: " + hit.group(1) if hit else "not found as exact key"}')
