#!/usr/bin/env python3
"""List PE resource leaves with their file offsets and sizes.

    python tools/research/res_names.py <exe> [N]

Kept as a separate entry point because it is the quickest way to answer "what
else is embedded in this binary?".  For headers and the data directories use
pe_info.py instead.
"""
import sys

import _bootstrap  # noqa: F401
from _bootstrap import need_argv

from cubelib.pe import PE

need_argv(2, 'res_names.py <exe> [N]')
pe = PE(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 60

res = pe.resources()
print(f'{len(res)} resource leaves in {pe.bin.path}\n')
print(f'{"label":46} {"type":12} {"file offset":>12} {"size":>12}  head')
for r in sorted(res, key=lambda r: r.off)[:n]:
    head = pe.bin.slice(r.off, 24)
    print(f'  {r.label[:46]:46} {r.type_name:12} 0x{r.off:08X} {r.size:>12,}  {head!r}')

named = [r for r in res if any(isinstance(p, str) for p in r.path)]
if named:
    print(f'\nnamed resources ({len(named)}):')
    for r in sorted(named, key=lambda r: r.off):
        print(f'  {r.label:40} {r.size:>12,}  at 0x{r.off:08X}')
pe.close()
