#!/usr/bin/env python3
"""Decode a Steinberg runtime-deobfuscated string.

    python tools/research/deobf_str.py <exe> <seed> --key f0x5FF9350:16 \
        --key x91c169c8 ...
    python tools/research/deobf_str.py Cubase15.exe 0xDC1BE0D5 --len 61

Why this exists
---------------
Some Steinberg strings are not in the binary in plain form.  Instead the code
assembles a key blob from immediates plus a few `.rdata` constants, then decodes
it with an LCG:

    out[i] = (state & 0xFF) ^ key[i]
    state  = (state * 0xBC8F) % 0x7FFFFFFF

The modulus is applied in the original with the usual "divide by 0x7FFFFFFF
without a divide" trick - `edx = high32(n * 3)`, then
`n -= (((n - edx) >> 1) + edx) >> 30) * 0x7FFFFFFF` - which only fires once the
state exceeds 2^31, so this tool replays the instructions exactly instead of
writing `n % 0x7FFFFFFF` (that would fold differently and decode to garbage).

The key blob is usually *not contiguous* in the file, so it is given as an
ordered list of parts:

  * `--key f<HEXOFF>:<LEN>`   LEN bytes read from that file offset
  * `--key x<HEXBYTES>`       bytes written as immediates in the code
    (little endian, the way the immediates land in memory)

`--len` says how many bytes the decoder consumes (the loop bound, e.g. the
`r9d = 0x3d` counter).
"""
import argparse
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.binary import Binary


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('exe')
    ap.add_argument('seed', type=lambda s: int(s, 0))
    ap.add_argument('--key', action='append', default=[], metavar='PART',
                    help='f<fileoff>:<len> file bytes, x<hex> immediates')
    ap.add_argument('--len', type=lambda s: int(s, 0), default=0,
                    help='bytes the decoder loop consumes (default: key size)')
    a = ap.parse_args()

    if not a.key:
        die('need at least one --key part')

    try:
        b = Binary(a.exe)
    except OSError as exc:
        die(str(exc))

    key = bytearray()
    for part in a.key:
        if part.startswith('f'):
            off_s, _sep, len_s = part[1:].partition(':')
            if not _sep:
                off_s, len_s = part[1:], '16'
            off, ln = int(off_s, 0), int(len_s, 0)
            chunk = b.slice(off, ln)
            if len(chunk) < ln:
                die(f'only {len(chunk)} bytes at 0x{off:X}, need {ln}')
            key += chunk
        elif part.startswith('x'):
            key += bytes.fromhex(part[1:])
        else:
            die(f'--key part must start with f or x, got {part!r}')

    n = a.len or len(key)
    if n > len(key):
        die(f'decoder wants {n} key bytes but only {len(key)} were given')

    state = a.seed & 0xFFFFFFFF
    out = bytearray()
    for i in range(n):
        out.append((state & 0xFF) ^ key[i])
        state = (state * 0xBC8F) & 0xFFFFFFFF
        edx = ((state * 3) >> 32) & 0xFFFFFFFF
        eax = ((state - edx) & 0xFFFFFFFF) >> 1
        eax = ((eax + edx) & 0xFFFFFFFF) >> 30
        state = (state - eax * 0x7FFFFFFF) & 0xFFFFFFFF

    print(f'key ({len(key)} bytes): {key.hex(" ")}')
    print(f'seed 0x{a.seed:X}, {n} bytes decoded, final state 0x{state:X}')
    print(f'raw   : {out.hex(" ")}')
    try:
        text = out.decode('ascii')
    except UnicodeDecodeError:
        print('text  : (not printable ascii)')
    else:
        print(f'text  : {text!r}')
    b.close()


if __name__ == '__main__':
    sys.exit(main())
