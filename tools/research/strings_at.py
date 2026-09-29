#!/usr/bin/env python3
"""Dump printable strings in a file-offset range.

    python tools/research/strings_at.py <file> <lo> <hi>
    python tools/research/strings_at.py <file> 0x659E400 0x659E700
    python tools/research/strings_at.py <file> 0x659E400 0x200 --utf16

`lo` and `hi` are FILE OFFSETS (hex or decimal), not lengths.  The tool refuses
to run when hi <= lo, because that mistake is easy to make and previously
produced silent empty output.
"""
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.binary import Binary

USAGE = 'strings_at.py <file> <lo> <hi> [--utf16] [--min N]'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = {a for a in sys.argv[1:] if a.startswith('--')}
    if len(args) < 3:
        die(f'usage: {USAGE}')

    path, lo_s, hi_s = args[0], args[1], args[2]
    lo = int(lo_s, 0)
    hi = int(hi_s, 0)
    if hi <= lo:
        die(f'hi (0x{hi:X}) must be greater than lo (0x{lo:X}) - '
            f'both are file offsets, not lengths\nusage: {USAGE}')
    minlen = 4
    if '--min' in flags:
        i = sys.argv.index('--min')
        if i + 1 < len(sys.argv):
            minlen = int(sys.argv[i + 1])

    with Binary(path) as b:
        hi = min(hi, b.size)
        print(f'{path}: 0x{lo:X}..0x{hi:X}  ({hi - lo:,} bytes)')
        found = b.strings_ascii(lo, hi, minlen)
        if '--utf16' not in flags:
            print(f'\nASCII ({len(found)}):')
            for off, s in found:
                print(f'  +0x{off - lo:05X}  abs 0x{off:08X}  {s}')
        wide = b.strings_utf16(lo, hi, max(3, minlen - 1))
        if found or '--utf16' in flags:
            print(f'\nUTF-16LE ({len(wide)}):')
        for off, s in wide:
            print(f'  +0x{off - lo:05X}  abs 0x{off:08X}  {s}')


if __name__ == '__main__':
    main()
