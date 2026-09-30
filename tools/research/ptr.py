#!/usr/bin/env python3
"""Read pointers (and neighbouring words) at a VA / RVA / file offset.

    python tools/research/ptr.py <exe> <addr> [--count 8] [--data]
    python tools/research/ptr.py Cubase15.exe 0x14772F640 --count 4

Why this exists
---------------
Steinberg C++ hands out objects as `rcx`; the interesting part is then one
`[rcx+N]` or one vtable slot away.  Knowing the address of a class
registration table and being able to say "that slot points at a function in
.pdata RVA 0x16Bxxxx" is what turns a string reference into a map of methods.

Output per slot:

  * a VA inside the image -> RVA, file offset, and, when `.pdata` covers it,
    the owning function range (that is the method)
  * a VA outside the image  -> printed raw, so shared/other-module pointers
    are visible instead of being silently dropped
  * with `--data`, the ASCII/UTF-16LE string at the target, when there is one
"""
import argparse
import struct
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.pe import PE


def describe(pe, va, data):
    fn = None
    if va >= pe.imagebase:
        fn = pe.function_containing(va - pe.imagebase)
    bits = [f'0x{va:X}']
    if fn:
        bits.append(f'code  func RVA 0x{fn[0]:X}..0x{fn[1]:X} '
                    f'(+0x{va - pe.imagebase - fn[0]:X} into it)')
    else:
        bits.append('outside .pdata / not image')
    line = '  '.join(bits)
    off = pe.va_to_off(va)
    if off is not None and data:
        raw = pe.bin.slice(off, 64)
        s = pe.bin.read_str(off)
        if s:
            line += f'\n        -> "{s}"'
        elif raw[:2] == b'MZ':
            line += '\n        -> DOS header (module base)'
        else:
            line += '\n        -> ' + pe.bin.hexdump(off, 32).splitlines()[0]
    return line


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('exe')
    ap.add_argument('addr')
    ap.add_argument('-n', '--count', type=int, default=8)
    ap.add_argument('--data', action='store_true',
                    help='also show the string / bytes at each target')
    a = ap.parse_args()

    pe = PE(a.exe)
    value = int(a.addr, 16)
    off, kind = pe.resolve(value)
    if off is None:
        die(f'{a.addr} is not inside {a.exe}')

    rva = pe.off_to_rva(off)
    print(f'{a.addr} = {kind} -> file offset 0x{off:X}, RVA 0x{rva:X}, '
          f'VA 0x{pe.imagebase + rva:X}')
    sec = next((s for s in pe.sections if s.contains_off(off)), None)
    if sec:
        print(f'  section {sec.name}')
    print(f'  +0x00: {pe.bin.hexdump(off, 32)}')

    print(f'\n{pe.imagebase + rva:X} as {a.count} qword(s), stride 8:')
    for i in range(a.count):
        try:
            q = struct.unpack_from('<Q', pe.bin.data, off + i * 8)[0]
        except struct.error:
            break
        print(f'  +0x{i * 8:02X}  {describe(pe, q, a.data)}')
    pe.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
