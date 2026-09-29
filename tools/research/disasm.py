#!/usr/bin/env python3
"""Disassemble a region, annotating RIP-relative operands with string literals.

    python tools/research/disasm.py <exe> <offset|VA> [length]
    python tools/research/disasm.py <exe> 0x1445600B0 0xB0
    python tools/research/disasm.py <exe> --func 0x14455FF90

The start address may be a file offset, an RVA or a VA - the tool works out
which.  If it lands inside a function listed in `.pdata`, decoding starts at
that function's real entry point and says so, because decoding from a guessed
mid-function address produces convincing nonsense.
"""
import sys

import _bootstrap  # noqa: F401
from _bootstrap import need_argv, die

from cubelib.pe import PE
from cubelib.x86 import Disassembler, MissingCapstone

if len(sys.argv) < 2:
    die('usage: disasm.py <exe> <offset|VA> [length] | disasm.py <exe> --func <VA>')

try:
    from cubelib.x86 import require_capstone
    require_capstone()
except MissingCapstone as exc:
    die(str(exc))

pe = PE(sys.argv[1])

if '--func' in sys.argv:
    i = sys.argv.index('--func')
    if i + 1 >= len(sys.argv):
        die('--func needs a target VA or RVA')
    value = int(sys.argv[i + 1], 16)
    off, kind = pe.resolve(value)
    if off is None:
        die(f'0x{value:X} is not inside the image')
    rva = pe.off_to_rva(off)
    fn = pe.function_containing(rva)
    if fn is None:
        die(f'RVA 0x{rva:X} is not covered by any .pdata entry')
    dis = Disassembler(pe)
    insns, _ = dis.function(fn[0])
    print(f'# {pe.bin.path}')
    print(f'# .pdata function RVA 0x{fn[0]:X}..0x{fn[1]:X} '
          f'({fn[1] - fn[0]} bytes), VA 0x{pe.imagebase + fn[0]:X}')
    for ins in insns:
        print(ins.format())
    pe.close()
    raise SystemExit(0)

need_argv(3, 'disasm.py <exe> <offset|VA> [length]')
value = int(sys.argv[2], 16)
length = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x300
off, kind = pe.resolve(value)
if off is None:
    die(f'0x{value:X} is not inside the image')

dis = Disassembler(pe)
print(dis.format(off, length))
print(f'\n# note: input given as {kind}')
pe.close()
