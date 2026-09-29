#!/usr/bin/env python3
"""Apply per-string wording decisions and report anything that does not match.

  python tools/apply_glossary.py            # dry run, lists unknown keys
  python tools/apply_glossary.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import glossary_notation
import glossary_notation2
import glossary_noteduration
import glossary_untranslated
import glossary_reorder
import glossary_verbs

FIXES = {}
for mod in (glossary_notation, glossary_notation2, glossary_noteduration,
            glossary_untranslated, glossary_reorder, glossary_verbs):
    for name in dir(mod):
        if name.isupper():
            FIXES.update(getattr(mod, name))

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

PLACEHOLDER = re.compile(r'%(?:\.\d+)?[a-zA-Z%]|%l')

unknown = sorted(k for k in FIXES if k not in src)
known = {k: v for k, v in FIXES.items() if k in src}

print(f'decisions defined : {len(FIXES)}')
print(f'match a real key  : {len(known)}')
if unknown:
    print(f'\n{len(unknown)} key(s) not in Cubase - dropped:')
    for k in unknown:
        print(f'  {k!r}')

bad = []
for k, v in known.items():
    if '\ufffd' in v:
        bad.append((k, 'value contains U+FFFD'))
    if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v)):
        bad.append((k, f'placeholder {sorted(PLACEHOLDER.findall(src[k]))} '
                       f'!= {sorted(PLACEHOLDER.findall(v))}'))
if bad:
    print(f'\n{len(bad)} problem(s):')
    for k, why in bad:
        print(f'  {k!r}: {why}')
    sys.exit(1)

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))
changes = {k: v for k, v in known.items() if vi.get(k) != v}
print(f'\nvalues to change  : {len(changes)}')
for k, v in list(changes.items())[:15]:
    print(f'  {k!r}\n      {vi.get(k)!r}\n   -> {v!r}')
if len(changes) > 15:
    print(f'  ... and {len(changes) - 15} more')

if not WRITE:
    print('\n(dry run - pass --write)')
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
print(f'\napplied {n} change(s)')
