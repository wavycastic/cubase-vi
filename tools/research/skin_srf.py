#!/usr/bin/env python3
"""Unpack a Steinberg Resource File such as Skins/skin.srf.

    python tools/research/skin_srf.py <skin.srf>
    python tools/research/skin_srf.py <skin.srf> --extract out/
    python tools/research/skin_srf.py <skin.srf> --templates
    python tools/research/skin_srf.py <skin.srf> --names

The container holds every window template, colour, metric and icon that makes
up the Cubase interface.  Text inside it is not a second translation surface -
the `title=` attributes are keys looked up in translation.xml - so theming
changes and the Vietnamese pipeline stays independent.
"""
import argparse
import os
import re
import sys
from collections import Counter

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.srf import SRF, SRFError

TEMPLATE = re.compile(rb'<template\s+name="([^"]+)"')
TEXT_ATTR = re.compile(rb'\b(?:title|label|text|tooltip|caption)="([^"]{2,90})"')
TOP = Counter()


def templates(xml):
    return [m.group(1).decode('utf-8', 'replace') for m in TEMPLATE.finditer(xml)]


def texts(xml):
    out = []
    for m in TEXT_ATTR.finditer(xml):
        v = m.group(1).decode('utf-8', 'replace')
        if v not in out:
            out.append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--extract', metavar='DIR',
                    help='write every member to DIR, numbered by kind')
    ap.add_argument('--templates', action='store_true',
                    help='list window template names')
    ap.add_argument('--texts', action='store_true',
                    help='list text-bearing attributes from the skin XML')
    ap.add_argument('--names', action='store_true',
                    help='strings from the trailing name table')
    a = ap.parse_args()

    try:
        srf = SRF.load(a.path)
    except (SRFError, OSError) as exc:
        die(str(exc))

    print(srf.summary())
    xml = srf.skin_xml()
    if xml:
        print(f'\nskin XML: {len(xml):,} bytes')
        for tag, n in Counter(t.decode() for t in
                              re.findall(rb'<([A-Za-z_][\w:.-]*)', xml)).most_common(12):
            print(f'  <{tag}> {n:,}')

    dims = srf.image_dimensions()
    if dims:
        print(f'\nimage sizes (most common):')
        for (w, h), n in dims.most_common(10):
            print(f'  {n:>4} x  {w}x{h}')

    names = srf.names()
    if a.names or (names and not (a.templates or a.texts)):
        print(f'\ntrailing name table ({len(names)} strings, first 60):')
        for n in names[:60]:
            print(f'  {n}')

    if a.templates:
        t = templates(xml)
        print(f'\ntemplates ({len(t)}):')
        for name in t:
            print(f'  {name}')

    if a.texts:
        t = texts(xml)
        print(f'\ntext attributes ({len(t)} unique) - these are keys into '
              f'translation.xml, not literals to translate:')
        for v in t:
            print(f'  {v}')

    if a.extract:
        root = a.extract
        for m in srf:
            sub = os.path.join(root, m.kind)
            os.makedirs(sub, exist_ok=True)
            ext = {'png': '.png', 'bmp': '.bmp', 'dib': '.dib',
                   'svg': '.svg'}.get(m.kind, '.xml' if m.kind in ('xml', 'skin') else '.bin')
            name = f'{m.index:04d}_{m.kind}{ext}'
            with open(os.path.join(sub, name), 'wb') as fh:
                fh.write(m.payload)
        print(f'\nextracted {len(srf)} members into {root}/<kind>/')
        if xml:
            with open(os.path.join(root, 'skin_all.xml'), 'wb') as fh:
                fh.write(xml)
            print(f'combined skin XML -> {os.path.join(root, "skin_all.xml")}')


if __name__ == '__main__':
    main()
