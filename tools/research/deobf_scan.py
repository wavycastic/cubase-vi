#!/usr/bin/env python3
"""Find and decode every runtime-deobfuscated string in a code range.

    python tools/research/deobf_scan.py <exe> <start> <end> [--min 6]
    python tools/research/deobf_scan.py Cubase15.exe 0x1421F2000 0x1421F8000
    python tools/research/deobf_scan.py Cubase15.exe --func 0x1421F5FC0

Why this exists
---------------
`deobf_str.py` needs the seed, the key parts and the length typed in by hand,
which is fine for the one string you already know about and useless for the
3,965 sites in `Cubase15.exe` that use the same scheme.  The shape is regular
enough to recognise mechanically.  A decoder site looks like this (real bytes
from `0x1421F5FC0`):

    mov  ecx, 0xDC1BE0D5                 ; seed
    mov  dword [rbp - 0x49], ecx         ; spill of the seed, NOT key material
    mov  dword [rbp - 0x45], 0xC869C191  ; key[0..3]
    mov  dword [rbp - 0x41], 0xD462F014  ; key[4..7]
    mov  dword [rbp - 0x3D], 0xB8198004  ; key[8..11]
    movdqa xmm0, [rip + ...]             ; key[12..27]
    movdqa [rbp - 0x39], xmm0
    ...
    mov  byte  [rbp - 0x09], 0x55        ; key[60]
    mov  r9d, 0x3D                       ; length = 61 = exactly the key span
    loop:
      xor   al, byte ptr [rbp + r8 - 0x45]   ; <- key base displacement
      imul  ecx, ecx, 0xBC8F                  ; <- the LCG the tool replays

So: seed = the `mov ecx, imm32`, key = every stack write ordered by its
displacement, key base = the displacement in the loop's `xor`, length = the
`mov r9d, imm32` (or the span the writes cover).  The seed spill uses opcode
`89` (`mov r/m, reg`) and is therefore never mistaken for key material, which
uses `c7` / `c6` / `66 0f 7f`.

A candidate is only reported when the decoded bytes are printable ASCII, so the
scanner can be pointed at a whole section without hand-filtering: real strings
decode, and everything else is dropped.
"""
import argparse
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import (X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_ECX,
                              X86_REG_RBP, X86_REG_RIP, X86_REG_RSP)
except ImportError:                                        # pragma: no cover
    die('capstone is required\n    pip install -r requirements-dev.txt')

AHEAD = 48          # instructions to look ahead for the rest of the blob
LCG_MULT = 0xBC8F
LCG_MOD = 0x7FFFFFFF
STACK = (X86_REG_RBP, X86_REG_RSP)   # frames in these sites use either


def lcg(state):
    """One LCG step, replayed the way the compiler emitted it.

    `n % 0x7FFFFFFF` is done as `edx = high32(n * 3)` then a shift sequence, so
    it only matches Python's `%` once the state passes 2**31.  Reproducing the
    instructions keeps every site decoding to the same bytes (see trap 4 in
    docs/WAVEFORM.md).
    """
    state = (state * LCG_MULT) & 0xFFFFFFFF
    edx = ((state * 3) >> 32) & 0xFFFFFFFF
    eax = ((state - edx) & 0xFFFFFFFF) >> 1
    eax = ((eax + edx) & 0xFFFFFFFF) >> 30
    return (state - eax * LCG_MOD) & 0xFFFFFFFF


def decode(seed, key, n):
    state, out = seed & 0xFFFFFFFF, bytearray()
    for i in range(n):
        out.append((state & 0xFF) ^ key[i])
        state = lcg(state)
    return bytes(out), state


def disp_of(insn):
    """Signed stack displacement of a [rbp + disp] / [rsp + disp] operand.

    None for anything else, including the indexed `[rbp + r8 + disp]` form the
    decode loop itself uses - that one is read as the key base separately.
    """
    for op in insn.operands:
        if op.type == X86_OP_MEM and op.mem.base in STACK and op.mem.index == 0:
            return op.mem.disp
    return None


def rip_target(pe, insn):
    for op in insn.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return insn.address + insn.size + op.mem.disp
    return None


def printable(raw):
    """True when the decoded bytes are text.

    The decoded length is the key span, which includes the terminating NUL, so
    trailing NULs are dropped before the check rather than rejected by it.
    """
    body = raw.rstrip(b'\0')
    return bool(body) and all(0x20 <= b < 0x7F or b in (0x09, 0x0A, 0x0D)
                              for b in body)


def imm_width(insn):
    """Bytes of immediate stored by a `mov [rbp+d], imm` instruction.

    Taken from the encoding rather than the mnemonic: `c7` always carries a
    32-bit immediate, `c6` an 8-bit one, and a `66` prefix makes either 16-bit.
    """
    raw = insn.bytes
    i = 1 if raw[:1] == b'\x66' else 0
    op = raw[i]
    if op not in (0xC6, 0xC7):
        return 0
    width = 1 if op == 0xC6 else 4
    if raw[:1] == b'\x66':
        width = 2
    return width


def site_at(pe, insns, i):
    """Try to read one decoder site starting at `insns[i]`.

    Returns (seed, key, length) or None.  The length is the span the key
    writes cover, which in every site seen so far equals the `mov r9d, imm32`
    loop bound exactly.
    """
    ins = insns[i]
    if ins.mnemonic != 'mov' or len(ins.operands) != 2:
        return None
    dst, src = ins.operands
    if src.type != X86_OP_IMM or dst.type != X86_OP_REG or dst.reg != X86_REG_ECX:
        return None
    seed = src.imm & 0xFFFFFFFF

    parts, pending = {}, {}
    for insn in insns[i + 1:i + AHEAD]:
        m, mn = insn.mnemonic, insn.operands
        if not m.startswith('mov') or len(mn) != 2:
            continue
        d = disp_of(insn)
        if mn[0].type == X86_OP_REG and mn[1].type == X86_OP_MEM:
            # movdqa xmm, [rip + rel] - half of a key part, wait for its store
            if mn[1].mem.base == X86_REG_RIP and d is None:
                pending[mn[0].reg] = rip_target(pe, insn)
        elif mn[0].type == X86_OP_MEM and mn[1].type == X86_OP_REG:
            # movdqa [rbp + disp], xmm - the store that completes the key part
            if mn[0].mem.base in STACK and d is not None and \
                    mn[1].reg in pending and insn.bytes[0] == 0x66:
                off = pe.va_to_off(pending.pop(mn[1].reg))
                if off is not None:
                    parts[d] = pe.bin.slice(off, 16)
        elif mn[0].type == X86_OP_MEM and mn[1].type == X86_OP_IMM and d is not None:
            width = imm_width(insn)
            if width:
                parts[d] = (mn[1].imm & 0xFFFFFFFF).to_bytes(4, 'little')[:width]

    if len(parts) < 2:
        return None
    base = min(parts)
    key, end = bytearray(), base
    for d in sorted(parts):
        if d < end or d - end > 8:          # overlapping or wildly gapped writes
            return None
        key += b'\0' * (d - end) + parts[d]
        end = d + len(parts[d])
    n = end - base
    if n < 4 or n > 512:
        return None
    return seed, bytes(key), n


def scan(pe, start, end, minlen):
    """Scan every `.pdata` function overlapping [start, end) for decoder sites.

    Walking function boundaries from the exception directory - rather than
    disassembling the range as one stream - keeps the instruction stream in
    sync, so a site is never half-recognised because decoding started inside
    another instruction.  Functions the directory does not cover are skipped;
    those are leaf thunks, which never hold a string.
    """
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    md.skipdata = False
    lo_rva, hi_rva = start - pe.imagebase, end - pe.imagebase
    found = []
    for beg, fin in pe.functions():
        if fin <= lo_rva or beg >= hi_rva:
            continue
        off = pe.rva_to_off(beg)
        if off is None:
            continue
        insns = [i for i in md.disasm(pe.bin.slice(off, fin - beg), pe.imagebase + beg)
                 if i.id != 0]
        for i, insn in enumerate(insns):
            if insn.bytes[0] != 0xB9:
                continue
            site = site_at(pe, insns, i)
            if site is None:
                continue
            seed, key, n = site
            raw, final = decode(seed, key, n)
            if len(raw) >= minlen and printable(raw):
                found.append((insn.address, seed, n, raw, final, key, (beg, fin)))
    found.sort()
    return found


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('exe')
    ap.add_argument('start', nargs='?', help='start VA (default: with --func)')
    ap.add_argument('end', nargs='?')
    ap.add_argument('--func', help='scan just this one .pdata function')
    ap.add_argument('--min', type=int, default=6,
                    help='ignore decoded strings shorter than this')
    a = ap.parse_args()

    pe = PE(a.exe)
    if a.func:
        value = int(a.func, 16)
        off = pe.va_to_off(value) if value >= pe.imagebase else pe.rva_to_off(value)
        rva = pe.off_to_rva(off)
        fn = pe.function_containing(rva)
        if fn is None:
            die(f'RVA 0x{rva:X} is not covered by any .pdata entry')
        start, end = pe.imagebase + fn[0], pe.imagebase + fn[1]
    else:
        if not (a.start and a.end):
            die('need <start> <end>, or --func <VA>')
        start = int(a.start, 16)
        end = int(a.end, 16)
        if start < pe.imagebase:
            start += pe.imagebase
        if end < pe.imagebase:
            end += pe.imagebase

    hits = scan(pe, start, end, a.min)
    print(f'# {a.exe}')
    print(f'# range VA 0x{start:X}..0x{end:X}  ({end - start} bytes)\n')
    if not hits:
        print('# no obfuscated string decoded in this range')
    for addr, seed, n, raw, final, key, fn in hits:
        where = f'RVA 0x{fn[0]:X}..0x{fn[1]:X}'
        print(f'0x{addr:X}  {where}')
        print(f'  seed 0x{seed:08X}  len {n}  key {len(key)} byte(s)  '
              f'final 0x{final:X}')
        print(f"  {raw.rstrip(b'\0').decode('ascii', 'replace')!r}")
        print()
    print(f'# {len(hits)} string(s)')
    pe.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
