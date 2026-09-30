#!/usr/bin/env python3
"""Dump every value that carries a long verbatim English run from its source.

Companion to find_english_frame.py, which reports the same thing. This one
prints in a compact form for reading - the whole list of suspects, longest
run first, so the reading pass can be done against one screenful.

  python tools/dump_frames.py [minrun]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 4

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
rows = []
for k, v in vi.items():
    en = src.get(k, '')
    if not en:
        continue
    low = set(w.lower() for w in WORD.findall(en))
    w = WORD.findall(v)
    best = cur = 0
    at = st = 0
    for i, x in enumerate(w):
        if x.lower() in low:
            if cur == 0:
                st = i
            cur += 1
            if cur > best:
                best, at = cur, st
        else:
            cur = 0
    if best >= MIN:
        rows.append((best, k, v, ' '.join(w[at:at + best])))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'TOTAL {len(rows)}')
for b, k, v, r in rows:
    print(f'[{b}] {k}')
    print(f'    {v}')
    print(f'    > {r}')
