#!/usr/bin/env python3
"""Disassemble an absolute VA range straight from the file - no indexing, ~0 s.

    python tools/research/dis.py <exe> <lo-VA> <hi-VA|count> [--intel] [--bytes]
    python tools/research/dis.py Cubase15.exe 0x141E9B6F0 0x141E9B7C0
    python tools/research/dis.py Cubase15.exe 0x141E9B6F0 40          # 40 insns

Why this exists next to `deobf_scan.py`: that tool builds the whole `.pdata`
function index (401.328 entries) before decoding a single instruction, which is
the right thing for a prologue scan and the wrong thing when you already know
the address and want to read 30 instructions - it costs ~40 s either way.

Decoding runs forward from `lo`, so `lo` should be a real instruction boundary
(`deobf_scan.py --prologues` / `.pdata` are the way to find one).  Every
RIP-relative operand and every 64-bit immediate is annotated with what it
points at - string, or the first bytes of the object - because in a stripped
image that annotation *is* the variable name.
"""
import argparse
import struct
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE


def annotate(pe, va):
    """Describe the object at a referenced VA, for an inline comment."""
    off = pe.va_to_off(va)
    if off is None:
        return f'0x{va:X} (unmapped)'
    d = pe.bin.data
    ascii_ = pe.bin.read_str(off)
    if ascii_ and len(ascii_) >= 3:
        return f'0x{va:X} A"{ascii_[:100]}"'
    wide = pe.bin.read_str(off, wide=True)
    if wide and len(wide) >= 3:
        return f'0x{va:X} W"{wide[:100]}"'
    tail = bytes(d[off:off + 16])
    return f'0x{va:X} [{tail.hex()}]'


def main():
    ap = argparse.ArgumentParser(description='fast targeted disassembly')
    ap.add_argument('exe')
    ap.add_argument('lo', type=lambda s: int(s, 0),
                    help='first VA (or RVA - values below the imagebase get rebased)')
    ap.add_argument('hi', type=lambda s: int(s, 0),
                    help='last VA exclusive, or an instruction count when < 0x1000 '
                         'and --count is not given')
    ap.add_argument('n', nargs='?', type=int, default=None,
                    help='explicit instruction count (wins over hi)')
    ap.add_argument('--count', action='store_true',
                    help='treat hi as an instruction count')
    ap.add_argument('--bytes', action='store_true', help='print raw opcode bytes')
    ap.add_argument('--no-annot', action='store_true')
    args = ap.parse_args()

    if not args.exe.lower().endswith(('.exe', '.dll')):
        die('exe argument must be a PE (.exe/.dll)')

    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

    with PE.open(args.exe) as pe:
        lo = args.lo if args.lo >= pe.imagebase else pe.imagebase + args.lo
        if pe.va_to_off(lo) is None:
            die(f'0x{lo:X} is not mapped')

        if args.n is not None:
            count, end = args.n, None
        elif args.count:
            count, end = args.hi, None
        else:
            hi = args.hi if args.hi >= pe.imagebase else pe.imagebase + args.hi
            count, end = None, hi

        off = pe.va_to_off(lo)
        room = (end - lo) if end else 16 * (count or 64)
        buf = pe.bin.slice(off, max(16, min(room, 1 << 20)))

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        md.skipdata = True
        printed = 0
        for ins in md.disasm(buf, lo):
            note = ''
            if not args.no_annot:
                for op in ins.operands:
                    if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                        tgt = ins.address + ins.size + op.mem.disp
                        note = f'          ; -> {annotate(pe, tgt)}'
                        break
                    if op.type == X86_OP_IMM and op.imm > 0x10000 and \
                            pe.va_to_off(op.imm & 0xFFFFFFFFFFFFFFFF) is not None \
                            and ins.mnemonic in ('mov', 'movabs', 'lea', 'and'):
                        if (op.imm & 0xFFFF000000000000) in (0x140000000000, 0):
                            note = f'          ; -> {annotate(pe, op.imm)}'
                            break
            raw = f'  {ins.bytes.hex():<20}' if args.bytes else ''
            print(f'  0x{ins.address:016X}{raw} {ins.mnemonic:<9} '
                  f'{ins.op_str}{note}')
            printed += 1
            if end is not None and ins.address + ins.size >= end:
                break
            if count is not None and printed >= count:
                break
        if printed == 0:
            die('capstone decoded nothing at that address')


if __name__ == '__main__':
    main()
