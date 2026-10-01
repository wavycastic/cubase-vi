#!/usr/bin/env python3
"""Final consistency pass: make equivalent Cubase keys share one wording.

Cubase ships several keys for the same label that differ only by case, a
trailing dot, or an ellipsis. Those must not drift apart.

Legitimate differences that are intentionally preserved:
  DRY / Dry, PRE / Pre, OFFLINE / Offline, Db / dB  - distinct UI elements
  In / in                                          - "vào" vs "trong"
  Keep History[RM]                                 - marker is part of the label
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

FIXES = {
    # agree on one wording per family
    'Auto Fades Settings': 'Cài đặt Auto Fades',
    'Cleanup...': 'Dọn dẹp...',
    'Print...': 'In ấn...',
    'Processing...': 'Đang xử lý...',
    'Profile Manager': 'Trình quản lý Profile',
    'Profile Manager...': 'Trình quản lý Profile...',
    'Project Logical Editor...': 'Project Logical Editor...',
    'Record In Editor': 'Ghi trong Editor',
    'Record in Editor': 'Ghi trong Editor',
    'Remove Filter': 'Gỡ bỏ Filter',
    'Remove filter': 'Gỡ bỏ Filter',
    'Save as Template': 'Lưu thành mẫu',
    'Save as Template...': 'Lưu thành mẫu...',
    'Scores': 'Score',
    'Scores...': 'Score...',
    'Set Marker Start to Cursor': 'Đặt đầu Marker tại con trỏ',
    'Set marker start to cursor': 'Đặt đầu Marker tại con trỏ',
    'Tempo Track...': 'Tempo Track...',
    'Transpose Notes': 'Transpose Note',
    'Transpose notes': 'Transpose Note',
    'Unavailable': 'Không khả dụng',
    'unavailable': 'Không khả dụng',
}

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

from cubelib.placeholders import PLACEHOLDER  # one pattern; see cubelib/placeholders.py
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

real = {k: v for k, v in FIXES.items() if k in src}
print(f'fixes defined : {len(FIXES)}')
print(f'real keys     : {len(real)}')

bad = []
noop = []
for k, v in real.items():
    if k not in vi:
        continue
    if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v)):
        bad.append((k, 'placeholder mismatch'))
    if vi[k] == v:
        noop.append(k)          # already correct, nothing to write

if bad:
    print('\nPROBLEMS:')
    for k, why in bad:
        print(f'  {k!r}: {why}')
    sys.exit(1)
if noop:
    print(f'already correct, skipped: {len(noop)}')

if not WRITE:
    print('\n(dry run - pass --write to apply)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in real.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'applied {n} change(s)')
