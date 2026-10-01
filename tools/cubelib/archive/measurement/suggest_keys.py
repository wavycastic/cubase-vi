#!/usr/bin/env python3
"""Suggest real <String Key> values close to wanted-but-missing keys."""
import re, sys, json, difflib

tsv = sys.argv[1]
want = set(json.load(open(sys.argv[2], encoding='utf-8')))
txt = open(tsv, encoding='utf-8').read()
rows = [l.split('\t') for l in txt.splitlines()[1:] if '\t' in l]
keys = [k for k, u in rows]
keyset = set(keys)
low = {}
for k in keys:
    low.setdefault(k.lower(), k)

print(f'{len(keys):,} keys in table\n')
out = {}
for w in sorted(want):
    if w in keyset:
        continue
    hit = low.get(w.lower())
    if hit:
        out[w] = hit
        continue
    cands = difflib.get_close_matches(w, keys, n=4, cutoff=0.72)
    out[w] = cands

json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for w, c in out.items():
    print(f'  {w!r:36} -> {c}')
