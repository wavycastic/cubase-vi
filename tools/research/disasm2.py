#!/usr/bin/env python3
"""Disassemble a function, re-synchronising when a decode goes wrong.

    python tools/research/disasm2.py <exe> <VA|RVA|offset>
    python tools/research/disasm2.py Cubase15.exe 0x1274E40
    python tools/research/disasm2.py Cubase15.exe 0x1274E40 --until 0x1280000

Why this exists
---------------
`disasm.py` decodes linearly from a function's `.pdata` start.  That is fine for
straight-line code, but a Delphi routine with an inline `case` jump table (a run
of dwords that capstone happily decodes as instructions) desynchronises the
stream, and from then on every `call rel32` points at an address that is not in
any section - which is how you notice it.

This tool decodes one instruction at a time and *validates* it:

  * `call` / `jmp` targets must land in a section;
  * `ret` ends the walk (plus a few bytes of `int3` padding);
  * conditional branches must land inside the same function.

When validation fails the address is reported as `??` and decoding resumes at the
next byte, so the gaps are visible instead of silently poisoning everything after
them.  Lines marked `#` are annotation only, not code.
"""
import argparse
import re
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
except ImportError:                                        # pragma: no cover
    die('capstone is required\n    pip install -r requirements-dev.txt')

BRANCH = re.compile(r'^(j\w+|call|loop\w*)$')


def in_image(pe, va):
    return pe.va_to_off(va) is not None


def describe(pe, va):
    off = pe.va_to_off(va)
    if off is None:
        return f'        ; -> 0x{va:X} (unmapped)'
    wide = pe.bin.read_str(off, wide=True)
    ascii_ = pe.bin.read_str(off)
    if wide:
        return f'        ; -> 0x{va:X} @0x{off:X}  W"{wide[:70]}"'
    if ascii_ and len(ascii_) >= 4:
        return f'        ; -> 0x{va:X} @0x{off:X}  A"{ascii_[:70]}"'
    return f'        ; -> 0x{va:X} @0x{off:X}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('exe')
    ap.add_argument('addr')
    ap.add_argument('--va', action='store_true',
                    help='treat ADDR as a VA, not a file offset (PE.resolve '
                         'prefers file offsets, which silently misreads a VA '
                         'that happens to be a valid offset)')
    ap.add_argument('--until', help='stop at this VA (default: end of .pdata entry)')
    ap.add_argument('--max', type=int, default=0, help='cap on instruction count')
    a = ap.parse_args()

    pe = PE(a.exe)
    value = int(a.addr, 16)
    if a.va:
        off, kind = pe.va_to_off(value), 'va'
    else:
        off, kind = pe.resolve(value)
    if off is None:
        die(f'{a.addr} is not inside {a.exe}')
    start_rva = pe.off_to_rva(off)
    fn = pe.function_containing(start_rva)
    if fn:
        lo, hi = fn
        start_va = pe.imagebase + lo
        stop_va = pe.imagebase + hi
    else:
        start_va = pe.imagebase + start_rva
        stop_va = start_va + 0x400
    if a.until:
        stop_va = int(a.until, 16)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    md.skipdata = False

    print(f'# {a.exe}')
    if fn:
        print(f'# .pdata function RVA 0x{lo:X}..0x{hi:X} '
              f'({hi - lo} bytes), VA 0x{start_va:X}')
    else:
        print(f'# no .pdata entry; decoding from VA 0x{start_va:X}')
    print(f'# stop at VA 0x{stop_va:X}   (input given as {kind})\n')

    va = start_va
    count = 0
    gaps = 0
    while va < stop_va:
        off = pe.va_to_off(va)
        if off is None:
            break
        chunk = pe.bin.slice(off, min(0x10, stop_va - va))
        decoded = list(md.disasm(chunk, va, count=1))
        bad = None
        if not decoded:
            bad = 'no decode'
        else:
            ins = decoded[0]
            if ins.size == 0:
                bad = 'zero length'
            if BRANCH.match(ins.mnemonic) and ins.operands:
                op = ins.operands[0]
                if op.type == X86_OP_IMM and not in_image(pe, op.imm):
                    bad = f'{ins.mnemonic} target 0x{op.imm:X} unmapped'
                elif op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    if not in_image(pe, ins.address + ins.size + op.mem.disp):
                        bad = 'rip target unmapped'
        if bad:
            gaps += 1
            print(f'?? 0x{va:X}  <-- desync: {bad}; resyncing +1 byte')
            va += 1
            continue
        ins = decoded[0]
        note = ''
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                note = describe(pe, ins.address + ins.size + op.mem.disp)
        print(f'  0x{ins.address:X}  {ins.bytes.hex():<22} {ins.mnemonic:8} '
              f'{ins.op_str}{note}')
        va = ins.address + ins.size
        count += 1
        if ins.mnemonic == 'ret':
            # Delphi pads with int3; stop once we only see padding
            probe = pe.bin.slice(pe.va_to_off(va), 8)
            if probe and all(b == 0xCC for b in probe[:4]):
                break
        if a.max and count >= a.max:
            break

    print(f'\n# {count} instruction(s), {gaps} resync(s)')
    pe.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
