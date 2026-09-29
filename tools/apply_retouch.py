#!/usr/bin/env python3
"""Apply the retouch set and re-verify the whole map.

  python tools/apply_retouch.py            # dry run
  python tools/apply_retouch.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')

sys.path.insert(0, os.path.join(ROOT, 'tools'))
from leak_fixes_p1 import PART_1
from leak_fixes_p2 import PART_2
from leak_fixes_p3 import PART_3
from leak_fixes_p4 import PART_4
from leak_fixes_retouch import CHUNK_A, DETECTOR_ALLOWLIST
from leak_fixes_quantifier import CHUNK_B

FIXES = {}
for part in (PART_1, PART_2, PART_3, PART_4, CHUNK_A, CHUNK_B):
    FIXES.update(part)

WRITE = '--write' in sys.argv

src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

PLACEHOLDER = re.compile(r'%(?:\.\d+)?[a-zA-Z%]|%l|\{[a-zA-Z0-9_]*\}')
FORBIDDEN_PARENS = re.compile(r'\s*\([^()]+\)\s*$')
FORBIDDEN_TERMS = (r'tự động hóa', r'\brãnh\b', r'đoạn cắt', r'\bnảy\b',
                   r'đóng băng', r'lượng tử hóa')

real = {k: v for k, v in FIXES.items() if k in src}
print(f'fixes defined     : {len(FIXES)}')
print(f'match a real key  : {len(real)}')
print(f'phantom dropped   : {len(FIXES) - len(real)}')

# A fix must never itself carry a U+FFFD: that would re-introduce the very
# corruption tools/fix_mojibake.py exists to remove.
BROKEN = {k: v for k, v in real.items() if '\ufffd' in v}
if BROKEN:
    print(f'\n{len(BROKEN)} fix(es) are themselves corrupt - refusing to apply:')
    for k, v in list(BROKEN.items())[:20]:
        print(f'  {k!r} -> {v!r}')
    sys.exit(1)

errors = []
for k, v in real.items():
    if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v)):
        errors.append((k, 'placeholder mismatch'))
    if not FORBIDDEN_PARENS.search(k) and FORBIDDEN_PARENS.search(v):
        errors.append((k, 'trailing dictionary parenthesis'))
    for t in FORBIDDEN_TERMS:
        if re.search(t, v, re.I):
            errors.append((k, f'awkward DAW term {t!r}'))

if errors:
    print(f'\n{len(errors)} INVALID:')
    for k, why in errors[:20]:
        print(f'  {k!r}: {why}')
    sys.exit(1)
print('style + placeholder checks pass')

index = {}
for path in glob.glob(os.path.join(BATCH_DIR, '*.json')):
    for k in json.load(open(path, encoding='utf-8')):
        index.setdefault(k, []).append(os.path.basename(path))

todo = {k: v for k, v in real.items() if k not in index}
print(f'already in batch  : {len(real) - len(todo)}')
print(f'new entries needed: {len(todo)}')

if not WRITE:
    print('\n(dry run - pass --write to apply)')
    sys.exit(0)

touched = []
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in FIXES.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
        touched.append(os.path.basename(path))

if todo:
    p = os.path.join(BATCH_DIR, 'batch-15.json')
    data = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    data.update(todo)
    json.dump(data, open(p, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2, sort_keys=True)
    print(f'\ncreated batch-15.json ({len(todo)} entries)')

print(f'\nupdated {len(touched)} file(s): {", ".join(touched)}')
