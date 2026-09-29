#!/usr/bin/env python3
"""Read long values (real sentences), where the awkwardness lives.

Short labels are almost always fine; the defects cluster in full sentences,
which is what a user actually complains about reading.

  python tools/read_long.py general 0 70
  python tools/read_long.py all 0 70
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

sys.path.insert(0, os.path.join(ROOT, 'tools'))
from sample_domain import domain


def longval(k, v, minlen):
    # a sentence, or a label with real words in it - not a bare term
    words = re.findall(r'[A-Za-z\u00c0-\u1ef9]+', v)
    return len(v) >= minlen and (len(words) >= 6 or '\\n' in v)


want = sys.argv[1] if len(sys.argv) > 1 else 'all'
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
count = int(sys.argv[3]) if len(sys.argv) > 3 else 70
minlen = int(sys.argv[4]) if len(sys.argv) > 4 else 45

items = [(k, v) for k, v in vi.items()
         if longval(k, v, minlen) and (want == 'all' or domain(k) == want)]
items.sort()
print(f'## {want}  {len(items)} long values  (showing {start}..{start+count})\n')
for k, v in items[start:start + count]:
    print(f'EN: {src.get(k, "?")}')
    print(f'VI: {v}')
    print()
