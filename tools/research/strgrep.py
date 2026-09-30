#!/usr/bin/env python3
"""Regex-grep printable strings in a binary, in any encoding.

    python tools/research/strgrep.py <file> <regex> [--enc ascii|utf16|both]
    python tools/research/strgrep.py Cubase15.exe 'Wave(Cache|Peak)'

Why this exists
---------------
`binfind.py` finds one literal in every encoding, which is the right tool for
"where is this string".  This one greps *shapes* of strings across a 135 MB
image - e.g. every RTTI-ish name containing "Wave" - and prints the offsets so
they can be fed into `xref.py`.  It decodes ASCII and UTF-16LE runs, so a
Steinberg `L"..."` literal and a std::string key are both covered.

Strings are NUL/UTF16-NUL terminated in practice, so runs are split on any
non-printable byte rather than on whitespace: `Show Waveforms` must survive
intact while `PEAKchunk` in a chunk-id table must show up as one token.
"""
import argparse
import re
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.binary import Binary

ASCII_RUN = re.compile(rb'[\x20-\x7e]{4,}')
UTF16_RUN = re.compile(rb'(?:[\x20-\x7e]\x00){3,}')


def scan(b, pattern, encodings, minlen, limit):
    rx = re.compile(pattern, re.IGNORECASE)
    total = 0
    for enc, run in encodings:
        hits = []
        for m in run.finditer(b.data):
            raw = m.group()
            if len(raw) < minlen:
                continue
            try:
                s = raw.decode('latin-1' if enc == 'ascii' else 'utf-16-le')
            except UnicodeDecodeError:
                continue
            if rx.search(s):
                hits.append((m.start(), s))
                if limit and len(hits) >= limit:
                    break
        note = f', stopped at {limit}' if limit and len(hits) >= limit else ''
        print(f'=== {enc}: {len(hits)} match(es){note} ===')
        for off, s in hits:
            print(f'  0x{off:08X}  {s}')
        total += len(hits)
    return total


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('file')
    ap.add_argument('regex')
    ap.add_argument('--enc', choices=('ascii', 'utf16', 'both'),
                    default='ascii',
                    help='which string runs to grep (default: ascii)')
    ap.add_argument('--min', type=int, default=4)
    ap.add_argument('-n', '--max', type=int, default=0,
                    help='stop after N matches per encoding (0 = no limit)')
    a = ap.parse_args()

    try:
        b = Binary(a.file)
    except OSError as exc:
        die(str(exc))

    encs = []
    if a.enc in ('ascii', 'both'):
        encs.append(('ascii', ASCII_RUN))
    if a.enc in ('utf16', 'both'):
        encs.append(('utf16le', UTF16_RUN))

    if not scan(b, a.regex, encs, a.min, a.max):
        print(f'no string matched {a.regex!r}')
    b.close()


if __name__ == '__main__':
    sys.exit(main())
