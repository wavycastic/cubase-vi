#!/usr/bin/env python3
"""Statistics for a Steinberg-style string XML, either standalone or embedded.

    python tools/research/scan_xml.py <file>
    python tools/research/scan_xml.py <file> --offset 0x07B79180 --size 4874598
    python tools/research/scan_xml.py <file> --strings

With no --offset the whole file is scanned, which is what you want for an
extracted translation.xml.  With --offset/--size it works directly on the PE.
"""
import argparse
import collections
import re
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.binary import Binary

LANG_TAG = re.compile(rb'<([a-z]{2,3})>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--offset', type=lambda s: int(s, 0))
    ap.add_argument('--size', type=lambda s: int(s, 0))
    ap.add_argument('--strings', action='store_true',
                    help='print the first N String entries')
    ap.add_argument('--limit', type=int, default=25)
    a = ap.parse_args()

    with Binary(a.file) as b:
        lo = a.offset or 0
        hi = min(b.size, lo + a.size) if a.size else b.size
        if lo >= b.size:
            die(f'offset 0x{lo:X} is past the end of the file ({b.size:,} bytes)')

        print(f'{a.file}: scanning 0x{lo:X}..0x{hi:X} ({hi - lo:,} bytes)')

        xml_starts = b.find(b'<?xml', lo)
        print(f'\n"<?xml" occurrences: {len(xml_starts)}')
        for i in xml_starts[:a.limit]:
            seg = b.slice(i, 160)
            end = seg.find(b'?>')
            print(f'  @0x{i:08X}  {seg[:end + 2 if end > 0 else 120]!r}')

        keys = b.find(b'<String Key=', lo)
        if keys:
            print(f'\n"<String Key=" count: {len(keys):,}'
                  f'\n  first @0x{keys[0]:08X}   last @0x{keys[-1]:08X}')
        else:
            print('\nno <String Key= entries in range')

        ends = b.find(b'</String>', lo)
        print(f'"</String>" count: {len(ends):,}')

        if keys:
            tags = collections.Counter()
            for m in LANG_TAG.finditer(b.slice(max(lo, keys[0] - 8192),
                                                min(b.size, keys[-1] + 8192))):
                tags[m.group(1).decode()] += 1
            print('\nchild tag frequency in the string-table region:')
            for t, c in tags.most_common(20):
                print(f'  <{t}> : {c:,}')

        if a.strings and keys:
            seg = b.slice(keys[0], min(hi, keys[0] + 400000))
            print(f'\nfirst {a.limit} String entries:')
            for m in list(re.finditer(
                    rb'<String Key="((?:[^"]|"(?!>))*)">\s*<us>(.*?)</us>',
                    seg, re.S))[:a.limit]:
                key = m.group(1).decode('utf-8', 'replace')
                us = m.group(2).decode('utf-8', 'replace')
                print(f'  {us[:56]:58} key={key!r}')


if __name__ == '__main__':
    main()
