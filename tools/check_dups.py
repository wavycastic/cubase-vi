#!/usr/bin/env python3
"""Detect duplicate keys in a JSON translation map (last-wins silently)."""
import json, re, sys, collections
p = sys.argv[1]
raw = open(p, encoding='utf-8').read()

# find duplicates by scanning with object_pairs_hook
dups = []
def hook(pairs):
    c = collections.Counter(k for k, _ in pairs)
    for k, n in c.items():
        if n > 1:
            dups.append((k, n))
    return dict(pairs)
data = json.loads(raw, object_pairs_hook=hook)
if not dups:
    print('no duplicate keys')
else:
    print(f'{len(dups)} duplicate key(s):')
    for k, n in dups:
        print(f'  {k!r} x{n}')
    sys.exit(1)
print(f'{len(data)} entries, all unique')
