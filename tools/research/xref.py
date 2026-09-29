#!/usr/bin/env python3
"""Find code references to a data address, verified against real instructions.

    python tools/research/xref.py <exe> <target-offset|VA>
    python tools/research/xref.py <exe> 0x4FAEBF0 --disasm
    python tools/research/xref.py <exe> --callers <VA>

Why this is not a byte scan
---------------------------
RIP-relative displacements appear inside immediates and inside other
instructions' operand bytes, so a naive scan reports plenty of false positives.
A REX-prefix-only scan goes the other way and misses real references.  This
tool takes the function list from the exception directory (`.pdata`), prefilters
cheaply, then confirms every hit with capstone.  Requires capstone.
"""
import sys

import _bootstrap  # noqa: F401
from _bootstrap import need_argv, die

from cubelib.pe import PE
from cubelib.x86 import XrefFinder, Disassembler, MissingCapstone

USAGE = ('xref.py <exe> <target-offset|VA> [--disasm] [--func] | '
         'xref.py <exe> --callers <VA>')

if len(sys.argv) < 3:
    die(f'usage: {USAGE}')
try:
    from cubelib.x86 import require_capstone
    require_capstone()
except MissingCapstone as exc:
    die(str(exc))

pe = PE(sys.argv[1])
finder = XrefFinder(pe)

if '--callers' in sys.argv:
    i = sys.argv.index('--callers')
    if i + 1 >= len(sys.argv):
        die(f'usage: {USAGE}')
    target = int(sys.argv[i + 1], 16)
    if target < pe.imagebase:
        target += pe.imagebase
    hits = finder.callers(target)
    print(f'direct callers of 0x{target:X}: {len(hits)}')
    for h in hits:
        fr = f'RVA 0x{h.func_rva[0]:X}..0x{h.func_rva[1]:X}' if h.func_rva else '-'
        print(f'  0x{h.insn_address:X}  {h.insn_mnemonic:6} {h.insn_op_str:20}  {fr}')
    pe.close()
    raise SystemExit(0)

value = int(sys.argv[2], 16)
off, kind = pe.resolve(value)
if off is None:
    die(f'0x{value:X} is not inside {sys.argv[1]}')
rva = pe.off_to_rva(off)
print(f'target: given 0x{value:X} ({kind}) -> file offset 0x{off:X}, '
      f'RVA 0x{rva:X}, VA 0x{pe.imagebase + rva:X}')
print('        content:', pe.bin.slice(off, 48))
print(f'functions indexed from .pdata: {len(pe.functions()):,}')

hits = finder.find(off)
print(f'\nverified xrefs: {len(hits)}')
for h in hits:
    fr = f'RVA 0x{h.func_rva[0]:X}..0x{h.func_rva[1]:X}' if h.func_rva else 'no .pdata'
    print(f'  0x{h.insn_address:X}  {h.insn_mnemonic:8} {h.insn_op_str:36}  {fr}')

if '--disasm' in sys.argv:
    dis = Disassembler(pe)
    for h in hits:
        print(f'\n--- function at RVA 0x{h.func_rva[0]:X} ---' if h.func_rva
              else '\n--- instruction ---')
        rva0 = h.func_rva[0] if h.func_rva else pe.off_to_rva(h.insn_offset)
        insns, _fn = dis.function(rva0)
        for ins in insns:
            mark = '>>' if ins.address == h.insn_address else '  '
            print(f'{mark}{ins.format()}')

pe.close()
