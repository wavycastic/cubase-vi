#!/usr/bin/env python3
"""Build a prioritised worklist of not-yet-translated Cubase strings.

Usage: python tools/worklist.py [A|B|C|D] [limit]
  A  short UI labels (<=22 chars, no placeholders)   - highest value
  B  medium (23-45 chars)
  C  long (46-90 chars)
  D  contains %-placeholders
"""
import re, json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
MAP = os.path.join(ROOT, 'translations', 'vi.json')

if not os.path.exists(TSV):
    sys.exit(f'missing {TSV}\nrun: python tools/list_strings.py keys\\translation_original.xml keys\\all_strings.tsv')
have = set(json.load(open(MAP, encoding='utf-8')))

rows = [l.split('\t', 1) for l in open(TSV, encoding='utf-8').read().splitlines()[1:] if '\t' in l]
untr = [(k, u) for k, u in rows if k not in have]
print(f'total {len(rows):,}  translated {len(rows)-len(untr):,}  remaining {len(untr):,}\n')

def has_ph(s):
    return bool(re.search(r'%[0-9dsfx]|%l|\{', s))

buckets = {
    'A. short UI labels (<=22 chars, no placeholders)': lambda k, u: len(u) <= 22 and not has_ph(u),
    'B. medium (23-45 chars, no placeholders)':          lambda k, u: 23 <= len(u) <= 45 and not has_ph(u),
    'C. long (46-90, no placeholders)':                  lambda k, u: 46 <= len(u) <= 90 and not has_ph(u),
    'D. with placeholders':                              lambda k, u: has_ph(u) and len(u) <= 80,
}
sel = {}
for name, f in buckets.items():
    sel[name] = [(k, u) for k, u in untr if f(k, u)]
    print(f'{name:44} {len(sel[name]):,}')

what = sys.argv[1] if len(sys.argv) > 1 else 'A'
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 400
key = next((n for n in sel if n.startswith(what)), None)
items = sel.get(key, [])
print(f'\n--- {key}: showing {min(limit, len(items))} of {len(items)} ---')
for k, u in items[:limit]:
    print(f'{u}')
