"""Disassembly and cross-references for x86-64 PE images.

Capstone is an optional dependency.  Importing this module never fails; call
`require_capstone()` (or use `Disassembler` / `XrefFinder`) and you get a clear
error message telling the user what to install.

Two things here exist because the ad-hoc versions got them wrong:

  * function boundaries come from `.pdata`, not from guessing where a function
    starts.  Decoding from an arbitrary address produces plausible-looking
    garbage; we either snap to a real boundary or say so.
  * every reported xref is verified by a real disassembler.  A raw scan for
    RIP-relative displacements finds plenty of false positives inside
    immediates and offsets, and a REX-prefix-only scan misses legitimate
    non-REX encodings entirely.
"""
from dataclasses import dataclass

from .pe import PE

RIP = 41          # capstone's X86_REG_RIP; kept as a named constant


class MissingCapstone(RuntimeError):
    pass


def require_capstone():
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import (X86_OP_MEM, X86_OP_IMM, X86_OP_REG,
                                  X86_REG_RIP)
    except ImportError as exc:                                  # pragma: no cover
        raise MissingCapstone(
            'capstone is required for disassembly and xrefs.\n'
            '    pip install -r requirements-dev.txt\n'
            '(original error: %s)' % exc) from exc
    return Cs, CS_ARCH_X86, CS_MODE_64, X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP


def have_capstone():
    try:
        require_capstone()
        return True
    except MissingCapstone:
        return False


@dataclass
class Insn:
    address: int
    offset: int
    size: int
    raw: bytes
    mnemonic: str
    op_str: str
    note: str = ''

    def format(self, width=22):
        return (f'  0x{self.address:X}  {self.raw.hex():<{width}} '
                f'{self.mnemonic:9} {self.op_str}{self.note}')


@dataclass
class Xref:
    """One verified reference from code to a data address."""
    insn_address: int
    insn_offset: int
    insn_mnemonic: str
    insn_op_str: str
    func_rva: tuple            # (begin, end) or None if outside .pdata

    @property
    def func_start(self):
        return self.func_rva[0] if self.func_rva else None


class Disassembler:
    def __init__(self, pe: PE, detail=True):
        Cs, arch, mode, self._op_mem, self._op_imm, self._op_reg, self._rip = \
            require_capstone()
        self.pe = pe
        self._Cs = Cs
        self.md = Cs(arch, mode)
        self.md.detail = detail
        self.md.skipdata = True

    # -- annotation --------------------------------------------------------
    def describe_va(self, va):
        """Render a code/data VA for an inline comment."""
        off = self.pe.va_to_off(va)
        if off is None:
            return f'        ; -> 0x{va:X} (unmapped)'
        wide = self.pe.bin.read_str(off, wide=True)
        ascii_ = self.pe.bin.read_str(off)
        if ascii_ and len(ascii_) >= 4:
            return f'        ; -> 0x{va:X} @0x{off:X}  A"{ascii_[:90]}"'
        if wide:
            return f'        ; -> 0x{va:X} @0x{off:X}  W"{wide[:90]}"'
        return f'        ; -> 0x{va:X} @0x{off:X}'

    def _annotate(self, ins):
        if not self.md.detail:
            return ''
        try:
            ops = list(ins.operands)
        except Exception:
            return ''
        for op in ops:
            if op.type == self._op_mem and op.mem.base == self._rip:
                return self.describe_va(ins.address + ins.size + op.mem.disp)
        if ops and ops[0].type == self._op_imm:
            t = ops[0].imm
            if self.pe.imagebase <= t < self.pe.imagebase + 0x100000000:
                note = self.describe_va(t)
                if '(unmapped)' not in note:
                    return '    ' + note.strip()
        return ''

    # -- ranges ------------------------------------------------------------
    def _resolve_start(self, off, align):
        """Snap `off` to a .pdata function start when that is sensible."""
        fn = self.pe.function_containing_off(off) if align else None
        if fn is None:
            return off, None, False
        fva = self.pe.imagebase + fn[0]
        foff = self.pe.rva_to_off(fn[0])
        return foff, fn, foff != off

    def disasm(self, off, length=0x300, align=True):
        """Decode from `off`, annotating RIP-relative operands with strings.

        With `align`, if `off` falls inside a known function the decode starts
        at that function's real start and the returned list includes the
        instructions before `off` - decoded correctly rather than as garbage.
        """
        off, fn, snapped = self._resolve_start(off, align)
        start_va = self.pe.off_to_va(off)
        if start_va is None:
            return [], fn, False
        out = []
        for ins in self.md.disasm(self.pe.bin.slice(off, length), start_va):
            out.append(Insn(ins.address, self.pe.va_to_off(ins.address), ins.size,
                            bytes(ins.bytes), ins.mnemonic, ins.op_str,
                            self._annotate(ins)))
        return out, fn, snapped

    def function(self, rva):
        """Decode exactly one .pdata function."""
        off = self.pe.rva_to_off(rva)
        if off is None:
            return [], None
        end = self.pe.rva_to_off(rva + 1)
        size = 0x400
        fn = self.pe.function_containing(rva)
        if fn:
            eoff = self.pe.rva_to_off(fn[1])
            if eoff and eoff > off:
                size = eoff - off
        va = self.pe.imagebase + rva
        out = []
        for ins in self.md.disasm(self.pe.bin.slice(off, size), va):
            out.append(Insn(ins.address, self.pe.va_to_off(ins.address), ins.size,
                            bytes(ins.bytes), ins.mnemonic, ins.op_str,
                            self._annotate(ins)))
        return out, fn

    def format(self, off, length=0x300, align=True):
        insns, fn, snapped = self.disasm(off, length, align)
        va = self.pe.off_to_va(off)
        head = [f'# {self.pe.bin.path}',
                f'# fileoff 0x{off:X}  VA {"None" if va is None else hex(va)}  '
                f'len 0x{length:X}']
        if fn:
            head.append(f'# .pdata function RVA 0x{fn[0]:X}..0x{fn[1]:X} '
                        f'(0x{fn[1] - fn[0]:X} bytes)'
                        + ('  [snapped to start]' if snapped else ''))
        else:
            head.append('# no .pdata entry covers this address; decoding linearly')
        return '\n'.join(head + [i.format() for i in insns])


class XrefFinder:
    """Find code references to a data address, verified by disassembly."""

    def __init__(self, pe: PE):
        self.pe = pe
        Cs, arch, mode, self._op_mem, self._op_imm, self._op_reg, self._rip = \
            require_capstone()
        self.md = Cs(arch, mode)
        self.md.detail = True
        self.md.skipdata = True

    def _candidate_functions(self, target_va, functions=None):
        """Cheap prefilter: which functions contain a disp32 that could hit us?"""
        d = self.pe.bin.data
        out = []
        for beg, end in (functions if functions is not None else self.pe.functions()):
            o = self.pe.rva_to_off(beg)
            e = self.pe.rva_to_off(end)
            if o is None or e is None or e <= o:
                continue
            seg = d[o:e]
            hit = False
            for i in range(len(seg) - 4):
                if self.pe.imagebase + beg + i + 4 + \
                        int.from_bytes(seg[i:i + 4], 'little', signed=True) == target_va:
                    hit = True
                    break
            if hit:
                out.append((beg, end))
        return out

    def find(self, target_off, functions=None):
        """All verified code references to the data at file offset `target_off`."""
        va = self.pe.off_to_va(target_off)
        if va is None:
            return []
        results = []
        for beg, end in self._candidate_functions(va, functions):
            o = self.pe.rva_to_off(beg)
            e = self.pe.rva_to_off(end)
            for ins in self.md.disasm(self.pe.bin.slice(o, e - o), self.pe.imagebase + beg):
                if not self.md.detail:
                    break
                for op in ins.operands:
                    if op.type == self._op_mem and op.mem.base == self._rip:
                        if ins.address + ins.size + op.mem.disp == va:
                            results.append(Xref(ins.address, o + (ins.address -
                                                (self.pe.imagebase + beg)),
                                                ins.mnemonic, ins.op_str, (beg, end)))
        return results

    def find_va(self, target_va, functions=None):
        """Same as `find` but the target is a VA (for code targets)."""
        results = []
        for beg, end in self._candidate_functions(target_va, functions):
            o = self.pe.rva_to_off(beg)
            e = self.pe.rva_to_off(end)
            for ins in self.md.disasm(self.pe.bin.slice(o, e - o), self.pe.imagebase + beg):
                if not self.md.detail:
                    break
                for op in ins.operands:
                    if op.type == self._op_mem and op.mem.base == self._rip:
                        if ins.address + ins.size + op.mem.disp == target_va:
                            results.append(Xref(ins.address,
                                                o + (ins.address - (self.pe.imagebase + beg)),
                                                ins.mnemonic, ins.op_str, (beg, end)))
        return results

    def callers(self, func_va, functions=None):
        """Direct `call` instructions targeting `func_va`."""
        out = []
        for beg, end in (functions if functions is not None else self.pe.functions()):
            o = self.pe.rva_to_off(beg)
            e = self.pe.rva_to_off(end)
            if o is None or e is None:
                continue
            for ins in self.md.disasm(self.pe.bin.slice(o, e - o), self.pe.imagebase + beg):
                if ins.mnemonic == 'call' and ins.op_str.startswith('0x'):
                    try:
                        t = int(ins.op_str, 16)
                    except ValueError:
                        continue
                    if t == func_va:
                        out.append(Xref(ins.address,
                                        o + (ins.address - (self.pe.imagebase + beg)),
                                        ins.mnemonic, ins.op_str, (beg, end)))
        return out
