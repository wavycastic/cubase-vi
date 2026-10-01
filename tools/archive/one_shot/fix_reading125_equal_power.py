#!/usr/bin/env python3
r"""Vòng 125: Sửa thuật ngữ kỹ thuật Equal Power trong Stereo Pan Law.

Theo phản hồi trực tiếp từ người dùng với ảnh chụp màn hình menu Stereo Pan Law:
- `Equal Power` -> `Equal Power` (trước: `Bằng công suất`)

Trong kỹ thuật mixing âm thanh chuyên nghiệp:
- `Equal Power` (Equal Power Pan Law / Equal Power Crossfade) là định luật bù năng lượng
  khi pan tín hiệu âm thanh giữa 2 loa trái-phải (tương tự như `Equal Gain`).
- Bản dịch cũ dịch máy thành "Bằng công suất" tạo cảm giác ngành điện lực, thô kệch
  và tối nghĩa trong môi trường DAW.
- Giữ nguyên tiếng Anh chuyên ngành `Equal Power`, đồng bộ trực tiếp với `Equal Gain`.

"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
MAP = os.path.join(ROOT, 'translations', 'vi.json')
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
WRITE = '--write' in sys.argv

vi = json.load(open(MAP, encoding='utf-8'))
src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

WORDING = {
    'Equal Power': 'Equal Power',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

SIBLINGS = [
    ('Equal Gain', 'Equal Gain'),
    ('Stereo Pan Law', 'Quy tắc Pan Stereo'),
    ('Project Pan Law', 'Quy tắc Pan của Project'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

if after['Equal Power'] != 'Equal Power':
    problems.append(f'Equal Power sai: {after["Equal Power"]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Stereo Pan Law: \"Equal Power\" đồng bộ trực tiếp với \"Equal Gain\"')
print()
for k, v in changed.items():
    cur = vi.get(k, '')
    print(f'  {k[:42]!r}')
    print(f'      {cur!r}')
    print(f'   -> {v!r}')

if not WRITE:
    print('\n(chạy thử - thêm --write để ghi)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changed.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
print(f'\nđã ghi {n} thay đổi vào batches')
