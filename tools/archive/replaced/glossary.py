#!/usr/bin/env python3
"""List every string in a terminology family, so a normalisation rule can be
written against real data instead of a guess.

  python tools/glossary.py bar system staff clef rest beam stem voice
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

# English surface form of each concept, in the source key
SURFACE = {
    'bar':       r'\bbars?\b',
    'system':    r'\bsystems?\b',
    'staff':     r'\bstaves?\b|\bstaff\b',
    'clef':      r'\bclefs?\b',
    'rest':      r'\brests?\b',
    'beam':      r'\bbeams?\b',
    'stem':      r'\bstems?\b|\bstemlets?\b',
    'voice':     r'\bvoices?\b',
    'barline':   r'\bbarlines?\b',
    'timesig':   r'\btime signatures?\b',
    'keysig':    r'\bkey signatures?\b',
    'note':      r'\bnotes?\b',
    'accident':  r'\baccidentals?\b',
    'ledger':    r'\bledger lines?\b',
    'stave':     r'\bstave\b',
}

for concept in sys.argv[1:]:
    pat = re.compile(SURFACE[concept], re.I)
    rows = [(k, v) for k, v in vi.items() if pat.search(src.get(k, ''))]
    print(f'\n######## {concept}  ({len(rows)} strings) ########')
    for k, v in rows:
        flag = ''
        # mark values where the concept word itself is still English
        print(f'  {v[:96]!r}{flag}')
