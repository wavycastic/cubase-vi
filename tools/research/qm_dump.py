#!/usr/bin/env python3
"""Read a Qt .qm translation catalogue.

    python tools/research/qm_dump.py <file.qm>
    python tools/research/qm_dump.py <file.qm> --list 40
    python tools/research/qm_dump.py <file.qm> --context AboutDialog
    python tools/research/qm_dump.py <file.qm> --search "Bork"
    python tools/research/qm_dump.py <l10n-dir>          # every .qm in a folder

The Score Editor localises itself with these catalogues, entirely separately
from Cubase's translation.xml.  Reading them is what makes a Vietnamese Score
Editor an authoring job rather than a reverse-engineering one.
"""
import argparse
import glob
import os
import sys

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.qm import QM, QMError


def show(qm, args):
    print(f'=== {qm.path}')
    print(f'  {qm.size:,} bytes, parsed {qm.consumed:,}')
    print(qm.block_summary())
    if not qm.complete:
        print('  !! incomplete - some tags are not understood; see RESEARCH.md')
    print()

    rows = qm.messages
    if args.context:
        rows = [m for m in rows if args.context.lower() in (m.context or '').lower()]
        print(f'-- context matches for {args.context!r}: {len(rows)}')
    if args.search:
        needle = args.search.lower()
        rows = [m for m in rows
                if needle in (m.source or '').lower()
                or needle in (m.translation or '').lower()]
        print(f'-- text matches for {args.search!r}: {len(rows)}')

    for m in rows[:args.list]:
        tr = m.translation
        ratio = ''
        if m.source and tr:
            ratio = f'  x{len(tr) / len(m.source):.2f}'
        print(f'  [{m.context[:18]:18}] {m.source[:44]!r:46} -> {tr[:52]!r}{ratio}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('--list', type=int, default=25, help='entries to print')
    ap.add_argument('--context')
    ap.add_argument('--search')
    ap.add_argument('--csv', help='write source<TAB>translation to this file')
    a = ap.parse_args()

    if os.path.isdir(a.target):
        files = sorted(glob.glob(os.path.join(a.target, '*.qm')))
        if not files:
            die(f'no .qm files in {a.target}')
        print(f'{len(files)} catalogue(s) in {a.target}\n')
        print(f'{"file":24} {"size":>10} {"contexts":>9} {"implied":>8} '
              f'{"parsed":>7} {"pct":>5}')
        for f in files:
            try:
                qm = QM.load(f)
            except (QMError, OSError) as exc:
                print(f'{os.path.basename(f):24} ERROR {exc}')
                continue
            exp = qm.expected_messages
            pct = 100 * len(qm.messages) / max(1, exp) if exp else 0
            print(f'{os.path.basename(f):24} {qm.size:>10,} {len(qm.contexts):>9} '
                  f'{exp:>8,} {len(qm.messages):>7,} {pct:>4.0f}%'
                  + ('' if qm.complete else '  <-- incomplete'))
        return

    try:
        qm = QM.load(a.target)
    except (QMError, OSError) as exc:
        die(str(exc))
    show(qm, a)
    if a.csv:
        with open(a.csv, 'w', encoding='utf-8', newline='') as fh:
            for src, tr in qm.pairs():
                fh.write(f'{src}\t{tr}\n')
        print(f'\nwrote {a.csv} ({len(qm.pairs()):,} rows)')


if __name__ == '__main__':
    main()
