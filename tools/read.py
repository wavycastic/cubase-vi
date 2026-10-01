#!/usr/bin/env python3
"""Read the Vietnamese map by hand — the last step AGENT.md §8.9 insists on.

  python tools/read.py long  [domain] [start] [count] [minlen]
  python tools/read.py short [domain] [start] [count] [maxlen]

`long`  = full sentences. That is where awkwardness lives and what a user
          actually complains about reading.
`short` = menu labels and button names, ~9,000 of one to six words. That is
          where term drift lives, because a label has no sentence to carry the
          meaning and is the first thing an automated pass gets wrong.

`domain` is any name from tools/sample_domain.py, or `all`.
Short values also print the real key when it differs from the English text,
because every fix table is keyed by the key — otherwise it silently misses and
reports "NOT IN CUBASE" for a string that plainly exists.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from sample_domain import domain

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u


def words(v):
    return re.findall(r'[A-Za-zÀ-ỹ]+', v)


def run_long():
    want = sys.argv[2] if len(sys.argv) > 2 else 'all'
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 70
    minlen = int(sys.argv[5]) if len(sys.argv) > 5 else 45
    items = [(k, v) for k, v in vi.items()
             if len(v) >= minlen and (len(words(v)) >= 6 or '\\n' in v)
             and (want == 'all' or domain(k) == want)]
    items.sort()
    print(f'## {want}  {len(items)} long values  (showing {start}..{start+count})\n')
    for k, v in items[start:start + count]:
        print(f'EN: {src.get(k, "?")}')
        print(f'VI: {v}')
        print()


def run_short():
    want = sys.argv[2] if len(sys.argv) > 2 else 'all'
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 90
    maxlen = int(sys.argv[5]) if len(sys.argv) > 5 else 44
    items = [(k, v) for k, v in vi.items()
             if not (len(v) >= 45 and (len(words(v)) >= 6 or '\\n' in v))
             and len(v) <= maxlen
             and (want == 'all' or domain(k) == want)]
    items.sort()
    print(f'## {want}  {len(items)} short values  (showing {start}..{start+count})\n')
    for k, v in items[start:start + count]:
        en = src.get(k, '?')
        print(f'{en}\n    {v}')
        if k != en:
            print(f'    <key: {k}>')
        print()


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'long'
    if mode == 'long':
        run_long()
    elif mode == 'short':
        run_short()
    else:
        print(__doc__)
        sys.exit(2)