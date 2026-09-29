#!/usr/bin/env python3
"""Search a binary for a pattern in every common encoding.

    python tools/research/binfind.py <file> <pattern> [-n MAX] [-c CONTEXT]
    python tools/research/binfind.py Cubase15.exe PSEUDO_LOCALIZATION

Reports one hit list per encoding that matched, so a hit in UTF-16LE and a hit
in ASCII are never confused for one another.
"""
import argparse
import re
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.binary import Binary

ENCODINGS = {
    'ascii': lambda s: s.encode('latin-1', 'ignore'),
    'utf8': lambda s: s.encode('utf-8'),
    'utf16le': lambda s: s.encode('utf-16-le'),
    'utf16be': lambda s: s.encode('utf-16-be'),
}

PRINTABLE = re.compile(rb'[\x20-\x7e]')


def context(chunk):
    return ''.join(chr(c) if 32 <= c < 127 else
                   ('\u00b7' if c > 255 else '.') for c in chunk)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('file')
    ap.add_argument('pattern')
    ap.add_argument('-n', '--max', type=int, default=20)
    ap.add_argument('-c', '--context', type=int, default=160)
    a = ap.parse_args()

    try:
        b = Binary(a.file)
    except OSError as exc:
        die(str(exc))

    total = 0
    for name, enc in ENCODINGS.items():
        pat = enc(a.pattern)
        if not pat:
            continue
        hits = b.find(pat, limit=a.max)
        if not hits:
            continue
        total += len(hits)
        print(f'=== {name}  ({len(hits)} hit(s), showing <= {a.max}) ===')
        half = a.context // 2
        for i in hits:
            lo = max(0, i - half)
            hi = min(b.size, i + half + len(pat))
            print(f'  @0x{i:08X} (dec {i})')
            print('   ', context(b.slice(lo, hi - lo)))
    if not total:
        print(f'no hits for {a.pattern!r} in any encoding')
    b.close()


if __name__ == '__main__':
    main()
