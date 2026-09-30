#!/usr/bin/env python3
"""Inspect the Score Editor's own localisation tree.

    python tools/research/scoring_l10n.py
    python tools/research/scoring_l10n.py --install "E:/Steinberg/Cubase 15"
    python tools/research/scoring_l10n.py --diff en de

Why this exists
---------------
The Score Editor (Steinberg's Dorico engine, embedded as ScoringEngine.dll)
does not use translation.xml.  It ships its own catalogues in
Components/ScoringEngine/l10n:

    instrumentnames_XX.xml   624 instrument-name entities per language
    strings_XX.qm            Qt translation catalogues

Both are discovered by globbing the folder, and the engine's language enum
already contains kVietnamese, so a Vietnamese file is a matter of authoring -
not patching.  What this tool answers is the practical question: exactly what
has to be produced, and what is already there.
"""
import argparse
import difflib
import os
import re
import sys
import xml.etree.ElementTree as ET

import _bootstrap  # noqa: F401
from _bootstrap import die

from cubelib.cubase import Install, SCORING_INSTRUMENT_FILES
from cubelib.qm import QM, QMError

LANG_IN_FILE = re.compile(r'<language>([^<]*)</language>')
ENTITY = re.compile(r'<InstrumentNameEntityDefinition>')
UINAME = re.compile(r'<uiName>([^<]*)</uiName>')


def instrument_file(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    lang = LANG_IN_FILE.search(text)
    return {
        'path': path,
        'language': lang.group(1) if lang else None,
        'entities': len(ENTITY.findall(text)),
        'uinames': len(UINAME.findall(text)),
        'size': os.path.getsize(path),
    }


def catalogue(path):
    """Return the QM, or raise.  Callers decide how loud a failure is."""
    return QM.load(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--install', default=Install().root,
                    help='Cubase installation directory')
    ap.add_argument('--diff', nargs=2, metavar=('A', 'B'),
                    help='diff instrument names between two languages')
    a = ap.parse_args()

    inst = Install(a.install)
    if not os.path.isdir(inst.scoring_l10n):
        print(inst.describe())
        die(f'not found: {inst.scoring_l10n}')

    l10n = inst.scoring_l10n
    print(f'l10n directory: {l10n}\n')

    inst_files = sorted(f for f in os.listdir(l10n)
                        if f.startswith('instrumentnames_') and f.endswith('.xml'))
    print(f'instrument name files ({len(inst_files)}):')
    print(f'  {"file":28} {"<language>":14} {"entities":>9} {"uiName":>7} {"size":>10}')
    rows = []
    for f in inst_files:
        info = instrument_file(os.path.join(l10n, f))
        rows.append((f, info))
        print(f'  {f:28} {str(info["language"]):14} {info["entities"]:>9,} '
              f'{info["uinames"]:>7,} {info["size"]:>10,}')

    have = {info['language'] for _f, info in rows if info['language']}
    counts = {info['entities'] for _f, info in rows}
    print(f'\n  distinct languages: {len(have)} -> {sorted(have)}')
    if len(counts) == 1:
        print(f'  every file has {counts.pop():,} entities '
              f'(expected {SCORING_INSTRUMENT_FILES:,})')
    else:
        print(f'  !! entity counts differ between files: {sorted(counts)}')

    qm_files = sorted(f for f in os.listdir(l10n)
                      if f.startswith('strings_') and f.endswith('.qm'))
    print(f'\ncatalogues ({len(qm_files)}):')
    print(f'  {"file":24} {"size":>10} {"contexts":>9} {"implied":>8} {"parsed":>7}')
    for f in qm_files:
        try:
            qm = catalogue(os.path.join(l10n, f))
        except (QMError, OSError) as exc:
            print(f'  {f:24} ERROR {exc}')
            continue
        exp = qm.expected_messages
        flag = '' if qm.complete else '  <-- incomplete'
        print(f'  {f:24} {qm.size:>10,} {len(qm.contexts):>9} {exp:>8,} '
              f'{len(qm.messages):>7,}{flag}')

    if 'kVietnamese' in have:
        print('\nkVietnamese: already present')
    else:
        print(f'\nto add Vietnamese, produce instrumentnames_vi.xml with '
              f'<language>kVietnamese</language> and {SCORING_INSTRUMENT_FILES:,} '
              f'entities, plus strings_vi.qm.\n'
              f'the engine globs the folder, so no binary patch is needed - but '
              f'whether Cubase ever asks for kVietnamese is a question for a '
              f'running Cubase, not for static analysis (see RESEARCH.md).')

    if a.diff:
        ta, tb = a.diff
        pa, pb = inst.instrument_names(ta), inst.instrument_names(tb)
        for p in (pa, pb):
            if not os.path.exists(p):
                die(f'missing {p}')
        root_a = ET.parse(pa).getroot()
        root_b = ET.parse(pb).getroot()

        def collect(root):
            out = {}
            for e in root.iter('InstrumentNameEntityDefinition'):
                eid = e.findtext('entityID')
                if eid:
                    out[eid] = (e.findtext('name') or '').strip()
            return out

        na, nb = collect(root_a), collect(root_b)
        only_a = sorted(set(na) - set(nb))
        only_b = sorted(set(nb) - set(na))
        same = [k for k in na if k in nb and na[k] == nb[k]]
        print(f'\n{ta} vs {tb}: {len(na)} / {len(nb)} entities, '
              f'{len(same)} identical names, '
              f'{len(only_a)} only in {ta}, {len(only_b)} only in {tb}')
        for label, keys, names in ((f'only in {ta}', only_a, na),
                                   (f'only in {tb}', only_b, nb)):
            if keys:
                print(f'  {label}: {len(keys)}')
                for k in keys[:20]:
                    print(f'    {k:44} {names[k]!r}')
        sample = [k for k in na if k in nb and na[k] != nb[k]][:25]
        if sample:
            print(f'  differing names (first {len(sample)}):')
            for k in sample:
                print(f'    {k:44} {na[k]!r} -> {nb[k]!r}')
        # overlap is the practical measure of how much work a new language is
        if na and nb:
            same_text = sum(1 for k in nb if na.get(k) == nb[k])
            print(f'  {ta} names reusable verbatim in {tb}: '
                  f'{same_text}/{len(nb)} ({100 * same_text / len(nb):.0f}%)')


if __name__ == '__main__':
    main()
