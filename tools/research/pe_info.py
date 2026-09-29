#!/usr/bin/env python3
"""Describe a PE image: headers, sections, data directories, functions, resources.

    python tools/research/pe_info.py <exe>
    python tools/research/pe_info.py <exe> --resources 20
    python tools/research/pe_info.py <exe> --find TRANSLATION.XML
    python tools/research/pe_info.py <exe> --at 0x7B79180
"""
import sys

import _bootstrap  # noqa: F401
from _bootstrap import need_argv

from cubelib.pe import PE

need_argv(2, 'pe_info.py <exe> [--resources N] [--find NAME] [--at OFFSET]')

pe = PE(sys.argv[1])
print(pe.describe())

if '--resources' in sys.argv:
    n = 20
    i = sys.argv.index('--resources')
    if i + 1 < len(sys.argv) and sys.argv[i + 1].lstrip('-').isdigit():
        n = int(sys.argv[i + 1])
    res = pe.resources()
    print(f'\nresources: {len(res)} leaves')
    print(f'  {"label":44} {"type":12} {"file offset":>12} {"size":>12}')
    for r in sorted(res, key=lambda r: -r.size)[:n]:
        print(f'  {r.label[:44]:44} {r.type_name:12} 0x{r.off:08X} {r.size:>12,}')

if '--find' in sys.argv:
    name = sys.argv[sys.argv.index('--find') + 1]
    r = pe.find_resource(name)
    if r is None:
        print(f'\nno resource named {name!r}')
    else:
        print(f'\n{name}: {r.label}  rva=0x{r.rva:X} off=0x{r.off:X} '
              f'size={r.size:,} codepage={r.codepage} lang={r.lang}')
        print('  head:', pe.bin.slice(r.off, 96))

if '--at' in sys.argv:
    value = int(sys.argv[sys.argv.index('--at') + 1], 16)
    off, kind = pe.resolve(value)
    if off is None:
        print(f'\n0x{value:X} is not inside the image')
    else:
        rva = pe.off_to_rva(off)
        print(f'\n0x{value:X} resolved as {kind} -> file offset 0x{off:X} '
              f'(RVA 0x{rva:X}, VA 0x{pe.imagebase + rva:X})')
        sec = next((s.name for s in pe.sections if s.contains_off(off)), '?')
        print(f'  section {sec}')
        for r in pe.resources():
            if r.off <= off < r.off + r.size:
                print(f'  inside resource {r.label} (declared size {r.size:,}, '
                      f'offset into it {off - r.off:,})')
        print(pe.bin.hexdump(off, 128))
