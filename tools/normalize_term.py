#!/usr/bin/env python3
"""Normalise a term across every batch file so the whole map agrees.

  python tools/normalize_term.py --from Tệp --to File
"""
import json, glob, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')

args = sys.argv[1:]
old = args[args.index('--from') + 1]
new = args[args.index('--to') + 1]
# whole-word only, so 'File' never touches 'Files' or 'Filename'
pat = re.compile(rf'(?<![\w]){re.escape(old)}(?![\w])', re.UNICODE)

total = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in list(data.items()):
        if isinstance(v, str) and pat.search(v):
            nv = pat.sub(new, v)
            if nv != v:
                data[k] = nv
                dirty = True
                total += 1
                print(f'  {k!r}\n      {v!r}\n   -> {nv!r}')
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)

print(f'\n{total} value(s) normalised: {old!r} -> {new!r}')
