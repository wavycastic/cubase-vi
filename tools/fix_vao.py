#!/usr/bin/env python3
"""Last two of the "redundant vào" family, then re-verify everything.

  python tools/fix_vao.py
  python tools/fix_vao.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

WORDING = {
    'Scroll to Selected Channel': 'Cuộn tới Channel đã chọn',
    'Scroll to selected ...': 'Cuộn tới mục đã chọn...',
}

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
from cubelib.placeholders import PLACEHOLDER  # one pattern; see cubelib/placeholders.py

real = {k: v for k, v in WORDING.items() if k in src}
print(f'defined : {len(WORDING)}   real keys : {len(real)}')
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'not in Cubase: {missing}')

bad = [(k, v) for k, v in real.items()
       if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v))
       or '\ufffd' in v]
if bad:
    print('PROBLEM:')
    for k, v in bad:
        print(f'  {k!r}: {v!r}')
    sys.exit(1)

changes = {k: v for k, v in real.items() if vi.get(k) != v}
for k, v in changes.items():
    print(f'  {k!r}\n      {vi.get(k)!r}\n   -> {v!r}')

if not WRITE:
    print(f'\n(dry run - {len(changes)} change(s))')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changes.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'applied {n} change(s)')
