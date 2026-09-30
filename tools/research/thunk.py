#!/usr/bin/env python3
"""Delphi 6-byte thunk tables, and resolved call graphs for one function.

    python tools/research/thunk.py <exe> find
    python tools/research/thunk.py <exe> resolve 0x1AB57A4
    python tools/research/thunk.py <exe> calls 0x1274E40 [--va] [--until VA]

Why this exists
---------------
`FLEngine_x64.dll` is Delphi, and Delphi x64 routes calls to procedures that
other units use through a **jump-stub table**: a contiguous run of 6-byte
entries, each `E9 rel32` plus one padding byte, sitting in a section whose name
says nothing useful (in this binary the run lives inside the section named
`.pdata`, which is *not* the exception directory - the real one is at
RVA 0x19A8980).

That matters because a linear disassembly of any large Delphi routine is full of
`call 0x1AB5xxx`, an address nowhere near anything readable.  Resolving each of
those through the stub gives the real target, which is what you actually want to
read.

Detecting the table
-------------------
A naive scan for `E9` finds hundreds of thousands of false positives, because
almost any instruction whose byte happens to be `E9` matches.  The reliable
signal is **contiguity**: a real table is a long run of back-to-back 6-byte
entries that all jump into a code section.  `find` reports only runs of at least
`--min` (default 16) such entries, which in this binary finds exactly one table.
"""
import argparse
import struct
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE

CODE_FLAGS = 0x20000000 | 0x20  # IMAGE_SCN_CNT_CODE | IMAGE_SCN_MEM_EXECUTE
STRIDE = 6


def code_ranges(pe):
    out = []
    for s in pe.sections:
        if s.characteristics & CODE_FLAGS and s.raw_size:
            out.append((s.vaddr, s.vaddr + s.span))
    return out


def is_code(pe, rva):
    return any(lo <= rva < hi for lo, hi in code_ranges(pe))


def stub_target(pe, va):
    """Return the jump target of the stub at `va`, or None."""
    off = pe.va_to_off(va)
    if off is None:
        return None
    b = pe.bin.slice(off, STRIDE)
    if len(b) < 5 or b[0] != 0xE9:
        return None
    tgt = va + 5 + struct.unpack_from('<i', b, 1)[0]
    if tgt < pe.imagebase or not is_code(pe, tgt - pe.imagebase):
        return None
    return tgt


def find_runs(pe, minimum):
    """Every contiguous run of >= `minimum` 6-byte stubs, as (start_va, count)."""
    base = pe.imagebase
    runs = []
    for s in pe.sections:
        if s.characteristics & CODE_FLAGS or s.raw_size:
            data = pe.bin.slice(s.raw_ptr, s.raw_size)
        else:
            continue
        i, n = 0, len(data)
        while i + STRIDE <= n:
            if data[i] == 0xE9:
                va = s.vaddr + i + base
                cnt = 0
                while stub_target(pe, va + cnt * STRIDE) is not None:
                    cnt += 1
                if cnt >= minimum:
                    runs.append((va, cnt))
                    i += cnt * STRIDE
                    continue
            i += 1
    return runs


def build_map(pe, minimum=16):
    """(address -> target) for every stub, plus the runs it was built from."""
    runs = find_runs(pe, minimum)
    table = {}
    for start, count in runs:
        for k in range(count):
            va = start + k * STRIDE
            t = stub_target(pe, va)
            if t is not None:
                table[va] = t
    return table, runs


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('exe')
    ap.add_argument('mode', choices=['find', 'resolve', 'calls'])
    ap.add_argument('addr', nargs='?')
    ap.add_argument('--va', action='store_true',
                    help='ADDR is a VA (PE.resolve prefers file offsets)')
    ap.add_argument('--until', help='stop at this VA when walking calls')
    ap.add_argument('--min', type=int, default=16,
                    help='shortest stub run to report (default 16)')
    a = ap.parse_args()

    pe = PE(a.exe)
    base = pe.imagebase

    if a.mode == 'find':
        for s in pe.sections:
            print(f'  {s.name:9} vaddr=0x{s.vaddr:08X} vsize=0x{s.vsize:08X} '
                  f'rsize=0x{s.raw_size:08X} chars=0x{s.characteristics:08X}'
                  f'{"  <- code" if s.characteristics & CODE_FLAGS else ""}')
        runs = find_runs(pe, a.min)
        print(f'\nstub runs of >= {a.min} entries: {len(runs)}')
        for start, cnt in runs:
            print(f'  VA 0x{start:X} .. 0x{start + cnt * STRIDE:X}   {cnt} stubs')
            lo = stub_target(pe, start)
            hi = stub_target(pe, start + (cnt - 1) * STRIDE)
            print(f'      targets RVA 0x{lo - base:X} .. 0x{hi - base:X}')
        pe.close()
        return 0

    if not a.addr:
        die('resolve/calls need an address')
    value = int(a.addr, 16)
    off = pe.va_to_off(value) if a.va else pe.resolve(value)[0]
    if off is None:
        die(f'0x{value:X} is not inside {a.exe}')
    start_rva = pe.off_to_rva(off)

    table, runs = build_map(pe, a.min)
    if a.mode == 'resolve':
        want = base + start_rva
        t = table.get(want) or stub_target(pe, want)
        if t is None:
            print(f'0x{want:X} (RVA 0x{start_rva:X}) is not a stub')
            pe.close()
            return 1
        f = pe.function_containing(t - base)
        note = f'RVA 0x{f[0]:X}..0x{f[1]:X} ({f[1] - f[0]} bytes)' if f else 'no .pdata'
        print(f'0x{want:X} -> VA 0x{t:X}  RVA 0x{t - base:X}   {note}')
        pe.close()
        return 0

    # -- calls -------------------------------------------------------------
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import X86_OP_IMM
    except ImportError:
        die('capstone is required for mode "calls"')
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    fn = pe.function_containing(start_rva)
    lo = fn[0] if fn else start_rva
    hi = (fn[1] if fn else start_rva + 0x400)
    if a.until:
        hi = int(a.until, 16) - base
    o = pe.rva_to_off(lo)
    calls = {}
    for ins in md.disasm(pe.bin.slice(o, pe.rva_to_off(hi) - o), base + lo):
        if ins.mnemonic == 'call' and ins.operands:
            op = ins.operands[0]
            if op.type == X86_OP_IMM:
                calls[op.imm] = calls.get(op.imm, 0) + 1

    resolved = sum(1 for t in calls if t in table)
    print(f'# {a.exe}')
    print(f'# function RVA 0x{lo:X}..0x{hi:X} ({hi - lo} bytes), '
          f'{len(calls)} distinct direct calls')
    print(f'# stub runs: {len(runs)}; {resolved}/{len(calls)} calls go through a stub\n')
    print(f'{"via stub":>12} {"real target":>12} {"RVA":>10}  {"function":>22} '
          f'{"bytes":>6}  n')
    for t in sorted(calls, key=lambda k: -calls[k]):
        tgt = table.get(t, t)
        f = pe.function_containing(tgt - base)
        note = f'0x{f[0]:X}..0x{f[1]:X}' if f else '-'
        site = f'0x{t:X}' if t in table else ''
        print(f'{site:>12} {tgt:>12} {tgt - base:>10}  {note:>22} '
              f'{f[1] - f[0] if f else 0:>6}  {calls[t]}')
    pe.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())