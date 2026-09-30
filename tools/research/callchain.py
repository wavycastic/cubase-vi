#!/usr/bin/env python3
"""Walk the call graph *upward* from a function, and find every pointer to it.

    python tools/research/callchain.py <exe> <func-VA> [<func-VA> ...] [--depth N]
    python tools/research/callchain.py Cubase15.exe 0x141E9E140 --depth 3
    python tools/research/callchain.py Cubase15.exe 0x141E9B6F0 --jmps --no-ptrs

Why this exists
---------------
`xref.py --callers` disassembles **every** function in the image to find the
`call` instructions aimed at one address.  On `Cubase15.exe` (401.328 functions,
96 MB of `.text`) that costs minutes per query, and an upward walk needs one
query per level.  This tool answers the same question with one regex pass per
level - measured at 2.0 s over 96 MB / 2.009.724 `E8` sites.

A direct `call rel32` to `T` sitting at `p` is encoded as the four bytes
`T - (p + 5)`, so the pattern depends on `p` and cannot be searched for as one
fixed string.  Scanning for the opcode and recomputing the target per hit is
exact (opcode byte + 4-byte displacement = a decoded instruction), and cheap.

The half that matters more is the **pointer** scan.  Steinberg dispatches most
drawing through vtables, so a function with no direct caller is not dead - it is
reached through a slot.  A qword in `.rdata`/`.data` holding the VA is found
with `bytes.find` in milliseconds.  When one turns up, the tool expands the
surrounding run of code pointers (that run is the vtable) and prints the ASCII
string just before it: in these binaries the class-name string sits immediately
ahead of its vtable, which is what turns "slot +0x20 of a table at 0x145FFAC20"
into the name of a class.

Levels are counted from the seed: level +1 calls the seed, level +2 calls level
+1, and so on.  Climbing continues from the *start of the function* a reference
lives in, so a call site never re-enters the walk as its own parent.
"""
import argparse
import re
import struct
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE

MIN_NAME = 4          # shorter ASCII in front of a vtable is noise, not a class
CODE_SECTIONS = ('.text', 'IPPCODE')



def num(s):
    return int(s, 0)


def code_sections(pe):
    """Sections that hold code - only these are scanned for call sites."""
    want = set(CODE_SECTIONS)
    return [s for s in pe.sections
            if s.raw_size and (s.name in want or s.characteristics & 0x20000000)]


def data_sections(pe):
    """Sections that can hold pointers - everything mapped but code/.pdata/.rsrc."""
    return [s for s in pe.sections
            if s.raw_size and not s.characteristics & 0x20000000
            and s.name not in ('.pdata', '.rsrc')]


def call_sites(pe, targets, sections, with_jmp=False):
    """Direct rel32 call (and optionally jmp) sites aimed at any VA in `targets`.

    Returns {target_va: [(site_va, 'call'|'jmp'), ...]}.  Exact: the opcode byte
    plus its 4-byte displacement is a whole instruction, so the target
    recomputed from it cannot be an accident of neighbouring bytes.
    """
    opcode = rb'[\xe8\xe9]' if with_jmp else rb'\xe8'
    pat = re.compile(opcode + rb'(.{4})', re.S)
    found = {}
    for sec in sections:
        buf = pe.bin.data[sec.raw_ptr:sec.raw_ptr + sec.raw_size]
        base = pe.imagebase + sec.vaddr
        for m in pat.finditer(buf):
            site = base + m.start()
            rel = int.from_bytes(m.group(1), 'little', signed=True)
            tgt = site + 5 + rel
            if tgt in targets:
                found.setdefault(tgt, []).append(
                    (site, 'jmp' if buf[m.start()] == 0xE9 else 'call'))
    return found


def pointer_sites(pe, targets):
    """8-byte-aligned qwords in data sections whose value is one of `targets`.

    Absolute addresses in a PE file are stored as imagebase+RVA and fixed up at
    load, so scanning the file bytes finds vtable slots, functors and
    std::function heaps alike.  Returns [(slot_va, target_va), ...].
    """
    pat = re.compile(b'|'.join(re.escape(struct.pack('<Q', va))
                              for va in sorted(targets)))
    out = []
    for sec in data_sections(pe):
        buf = pe.bin.data[sec.raw_ptr:sec.raw_ptr + sec.raw_size]
        for m in pat.finditer(buf):
            va = pe.imagebase + sec.vaddr + m.start()
            if va % 8 == 0:
                out.append((va, struct.unpack('<Q', m.group(0))[0]))
    return out


def is_code(pe, va):
    rva = va - pe.imagebase
    return any(s.contains_rva(rva) for s in code_sections(pe))


def read_qword(pe, va):
    off = pe.va_to_off(va)
    return None if off is None else struct.unpack_from('<Q', pe.bin.data, off)[0]


def vtable_run(pe, slot_va):
    """Expand outward from a slot while entries still point into code.

    Returns (lo, hi) - the first and last slot VA of the table, inclusive.
    """
    lo = hi = slot_va
    while True:
        v = read_qword(pe, lo - 8)
        if v is None or not is_code(pe, v):
            break
        lo -= 8
    while True:
        v = read_qword(pe, hi + 8)
        if v is None or not is_code(pe, v):
            break
        hi += 8
    return lo, hi


def name_before(pe, va, minlen=MIN_NAME):
    """The ASCII string immediately preceding `va`, if any.

    Steinberg's MSVC layout puts the class-name string right before the vtable
    it belongs to (WAVEFORM.md sec 12, trap 3): the tail of a run of function
    pointers in .rdata starts with its own name.
    """
    off = pe.va_to_off(va)
    if off is None:
        return None
    d = pe.bin.data
    i = off - 1
    if i < 0 or d[i] != 0:
        return None
    i -= 1
    while i >= 0 and 0x20 <= d[i] < 0x7F:
        i -= 1
    s = d[i + 1:off].decode('ascii', 'replace')
    return s if len(s) >= minlen else None


def describe(pe, fn, site, kind):
    """One line for a reference: who owns it and how it got there."""
    if fn is None:
        return f'  0x{site:016X}  {kind} (outside .pdata - thunk or gap)'
    return (f'  func 0x{pe.imagebase + fn[0]:016X}..'
            f'0x{pe.imagebase + fn[1]:016X} ({fn[1] - fn[0]:,} bytes)'
            f'  {kind}@0x{site:016X}')


def show_pointers(pe, targets, indent='      '):
    """Report vtable/data pointers to `targets`, naming the table where possible."""
    for slot, tgt in pointer_sites(pe, targets):
        lo, hi = vtable_run(pe, slot)
        nslots = (hi - lo) // 8 + 1
        name = name_before(pe, lo)
        kind = 'vtable' if nslots >= 3 else 'pointer'
        print(f'{indent}{kind} slot 0x{slot:016X} -> 0x{tgt:016X}  '
              f'table 0x{lo:016X}..0x{hi:016X} ({nslots} slots, '
              f'slot +0x{slot - lo:X})  name={name!r}')


def walk(pe, seed, depth, with_jmp, want_ptrs, verbose):
    fn = pe.function_containing(seed - pe.imagebase)
    if fn is None:
        print(f'!! 0x{seed:X} is not inside a .pdata function - results will be '
              f'partial (thunks and jump tables have no boundary to report)')
    print(f'\n=== upward from 0x{seed:016X} '
          f'(func 0x{pe.imagebase + fn[0]:X}..0x{pe.imagebase + fn[1]:X}) ===')
    seen = {seed}
    frontier = {seed}
    for level in range(1, depth + 1):
        refs = call_sites(pe, frontier, code_sections(pe), with_jmp)
        ptrs = pointer_sites(pe, frontier) if want_ptrs else []
        nxt = set()
        if not refs and not ptrs:
            print(f'  level +{level}: nothing references level +{level - 1} '
                  f'-> seed has no static caller at this depth')
            break
        print(f'  level +{level}:')
        for tgt in sorted(refs):
            for site, kind in refs[tgt]:
                owner = pe.function_containing(site - pe.imagebase)
                print(f'    0x{tgt:016X} <- ' + describe(pe, owner, site, kind)[2:])
                if owner is not None:
                    head = pe.imagebase + owner[0]
                    if head not in seen:
                        seen.add(head)
                        nxt.add(head)
                    elif head not in frontier:
                        print(f'      (already visited, not climbed again)')
        for slot, tgt in ptrs:
            lo, hi = vtable_run(pe, slot)
            nslots = (hi - lo) // 8 + 1
            print(f'    0x{tgt:016X} <- data qword @0x{slot:016X}  '
                  f'table 0x{lo:016X}..0x{hi:016X} '
                  f'({nslots} slots, slot +0x{slot - lo:X})  '
                  f'name={name_before(pe, lo)!r}')
        frontier = nxt
        if not frontier:
            print(f'    (no direct callers to climb from; indirect dispatch '
                  f'or end of chain)')
            break


def main():
    ap = argparse.ArgumentParser(
        description='walk the call graph upward from one or more functions')
    ap.add_argument('exe', help='PE to analyse (Cubase15.exe)')
    ap.add_argument('va', nargs='+', type=num,
                    help='function VA(s) - absolute (0x14...) or RVA (0x1E9E140)')
    ap.add_argument('--depth', type=int, default=3,
                    help='levels to climb (default 3)')
    ap.add_argument('--jmps', action='store_true',
                    help='also treat rel32 jmp (tail calls, jump tables) as a reference')
    ap.add_argument('--no-ptrs', dest='ptrs', action='store_false',
                    help='skip the vtable/data-pointer scan')
    ap.add_argument('--show-ptrs', action='store_true',
                    help='expand and name the table every pointer belongs to')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    if not args.exe.lower().endswith(('.exe', '.dll')):
        die('exe argument must be a PE (.exe/.dll)')

    with PE.open(args.exe) as pe:
        seeds = set()
        for va in args.va:
            if va < pe.imagebase:                  # looks like an RVA, not a VA
                va += pe.imagebase
            if pe.va_to_off(va) is None:
                die(f'0x{va:X} (rva 0x{va - pe.imagebase:X}) is not mapped in '
                    f'the image - check the address, or pass the RVA form')
            seeds.add(va)
        print(f'{pe.bin.path}\nimagebase 0x{pe.imagebase:X}  '
              f'functions {len(pe.functions()):,}  depth {args.depth}')
        for seed in sorted(seeds):
            walk(pe, seed, args.depth, args.jmps, args.ptrs, args.verbose)
        if args.show_ptrs:
            print('\n=== pointer detail ===')
            show_pointers(pe, seeds)


if __name__ == '__main__':
    main()
