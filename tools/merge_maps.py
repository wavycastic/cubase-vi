#!/usr/bin/env python3
"""Merge translations/batches/*.json into translations/vi.json (the single source of truth).

Later files win on conflict; duplicate keys inside one file are reported.
Usage:  python tools/merge_maps.py [--check]
"""
import json, glob, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
OUT = os.path.join(ROOT, 'translations', 'vi.json')

check_only = '--check' in sys.argv

files = sorted(glob.glob(os.path.join(BATCH_DIR, '*.json')))
if not files:
    print(f'no batch files in {BATCH_DIR}')
    sys.exit(1)

merged, conflicts, intra = {}, [], []
for path in files:
    name = os.path.basename(path)
    found = []
    data = json.loads(open(path, encoding='utf-8').read(),
                      object_pairs_hook=lambda p: (found.extend(
                          k for k, n in collections.Counter(k for k, _ in p).items() if n > 1),
                          dict(p))[1])
    for d in found:
        intra.append((name, d))
    for k, v in data.items():
        if k in merged and merged[k] != v:
            conflicts.append((k, merged[k], v, name))
        merged[k] = v

print(f'{len(files)} batch file(s) -> {len(merged)} unique entries')
for name, d in intra:
    print(f'  !! duplicate key inside {name}: {d!r}')
if conflicts:
    print(f'{len(conflicts)} conflict(s), last file wins:')
    for k, a, b, f in conflicts[:20]:
        print(f'  {k!r}: {a!r} -> {b!r}   ({f})')
else:
    print('no conflicts')

if not check_only:
    json.dump(merged, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'wrote {os.path.relpath(OUT, ROOT)}')
sys.exit(1 if (intra or conflicts) else 0)
