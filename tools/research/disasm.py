#!/usr/bin/env python3
"""Disassemble a region of a PE64, annotating RIP-relative references with string literals.
Usage: disasm.py <exe> <start-fileoff-or-VA> [length]"""
import struct, sys, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

path = sys.argv[1]
arg0 = int(sys.argv[2], 16)
length = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x300
raw = open(path, 'rb').read()

# ---- PE ----
e_lfanew = struct.unpack_from('<I', raw, 0x3C)[0]
coff = e_lfanew + 4
_, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', raw, coff)
opt = coff + 20
imagebase = struct.unpack_from('<Q', raw, opt + 24)[0]
sec_off = opt + optsz
sections = []
for i in range(nsec):
    o = sec_off + i*40
    name = raw[o:o+8].rstrip(b'\0').decode('latin-1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', raw, o+8)
    sections.append((name, va, vsz, ptr, rsz))

def va2off(va):
    rva = va - imagebase
    for name, vva, vsz, ptr, rsz in sections:
        if vva <= rva < vva + max(vsz, rsz):
            return ptr + (rva - vva)
    return None

def off2va(off):
    for name, vva, vsz, ptr, rsz in sections:
        if ptr <= off < ptr + rsz:
            return imagebase + vva + (off - ptr)
    return None

def read_str(off, wide=False, maxn=200):
    if off is None or off < 0 or off >= len(raw):
        return None
    if wide:
        m = re.match(rb'(?:[\x20-\x7e]\x00){3,}', raw[off:off+maxn*2])
        return m.group().decode('utf-16-le') if m else None
    m = re.match(rb'[\x20-\x7e]{4,}', raw[off:off+maxn])
    return m.group().decode() if m else None

# ---- resolve start ----
start = arg0
if start >= len(raw):                      # looks like a VA
    start = va2off(start)
    if start is None:
        raise SystemExit(f'VA 0x{arg0:X} not mapped')

va0 = off2va(start)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
md.skipdata = True

print(f'# {path}\n# fileoff 0x{start:X}  VA 0x{va0:X}  len 0x{length:X}\n')
for ins in md.disasm(raw[start:start+length], va0):
    ann = ''
    try:
        ops = list(ins.operands)
    except Exception:
        ops = []
    if len(ops) == 2 and ops[1].type == X86_OP_MEM and ops[1].mem.base == 41:  # mod=00 rm=101 => RIP
        tgt = ins.address + ins.size + ops[1].mem.disp
        off = va2off(tgt)
        if off is None:
            ann = f'        ; -> 0x{tgt:X} (unmapped)'
        else:
            s, w = read_str(off), read_str(off, wide=True)
            if s:   ann = f'        ; -> 0x{tgt:X} @0x{off:X}  A"{s[:90]}"'
            elif w: ann = f'        ; -> 0x{tgt:X} @0x{off:X}  W"{w[:90]}"'
            else:   ann = f'        ; -> 0x{tgt:X} @0x{off:X}'
    elif ops and ops[0].type == X86_OP_IMM:
        t = ops[0].imm
        if imagebase <= t < imagebase + 0x100000000:
            off = va2off(t)
            if off is not None:
                s = read_str(off) or read_str(off, wide=True)
                if s: ann = f'        ; 0x{t:X} @0x{off:X} "{s[:90]}"'
    print(f'  0x{ins.address:X}  {ins.bytes.hex():<24} {ins.mnemonic:9} {ins.op_str}{ann}')
