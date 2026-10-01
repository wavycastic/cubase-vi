#!/usr/bin/env python3
r"""Vòng 119: Chuẩn hóa toàn bộ bảng màu (Color Palette / Color Setup) giữ nguyên tiếng Anh.

Theo yêu cầu trực tiếp từ người dùng: "bảng màu yêu cầu giữ nguyên" -> Giữ nguyên tiếng Anh
cho toàn bộ các tên màu trong bảng màu mặc định và hệ thống sắc độ (32 chuỗi).

Trong sản xuất âm nhạc và môi trường phòng thu chuyên nghiệp, các tên màu trong
Color Setup (Color Palette) của Cubase được giữ nguyên tiếng Anh (Red, Blue, Green,
Dark Blue, Light Blue...) để đồng bộ với tài liệu kỹ thuật, video hướng dẫn quốc tế
và quy ước phối màu track tiêu chuẩn:

1. 8 màu cơ bản:
   - `White`   -> `White`
   - `Black`   -> `Black`
   - `Red`     -> `Red`
   - `Green`   -> `Green`
   - `Blue`    -> `Blue`
   - `Yellow`  -> `Yellow`
   - `Orange`  -> `Orange`
   - `Magenta` -> `Magenta`

2. 6 màu sáng (Light):
   - `Light Blue`    -> `Light Blue`
   - `Light Green`   -> `Light Green`
   - `Light Red`     -> `Light Red`
   - `Light Yellow`  -> `Light Yellow`
   - `Light Orange`  -> `Light Orange`
   - `Light Magenta` -> `Light Magenta`

3. 6 màu tối (Dark):
   - `Dark Blue`    -> `Dark Blue`
   - `Dark Green`   -> `Dark Green`
   - `Dark Red`     -> `Dark Red`
   - `Dark Yellow`  -> `Dark Yellow`
   - `Dark Orange`  -> `Dark Orange`
   - `Dark Magenta` -> `Dark Magenta`

4. 12 sắc độ xám / đen (tints):
   - `Black 50`, `Black 70`
   - `Gray 5`, `Gray 10`, `Gray 20`, `Gray 30`, `Gray 40`, `Gray 50`, `Gray 60`, `Gray 70`, `Gray 80`, `Gray 90`

Các nhãn giao diện mô tả chức năng màu vẫn giữ tiếng Việt chuẩn mực:
`Color` -> `Màu`, `Colors` -> `Màu sắc`, `Colorize` -> `Tô màu`, `Track Color` -> `Màu Track`,
`Phím trắng` -> `White Keys`, `Phím đen` -> `Black Keys`.

"""

import glob
import json
import os
import re
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
    'White': 'White',
    'Black': 'Black',
    'Red': 'Red',
    'Green': 'Green',
    'Blue': 'Blue',
    'Yellow': 'Yellow',
    'Orange': 'Orange',
    'Magenta': 'Magenta',
    'Light Blue': 'Light Blue',
    'Light Green': 'Light Green',
    'Light Red': 'Light Red',
    'Light Yellow': 'Light Yellow',
    'Light Orange': 'Light Orange',
    'Light Magenta': 'Light Magenta',
    'Dark Blue': 'Dark Blue',
    'Dark Green': 'Dark Green',
    'Dark Red': 'Dark Red',
    'Dark Yellow': 'Dark Yellow',
    'Dark Orange': 'Dark Orange',
    'Dark Magenta': 'Dark Magenta',
    'Black 50': 'Black 50',
    'Black 70': 'Black 70',
    'Gray 5': 'Gray 5',
    'Gray 10': 'Gray 10',
    'Gray 20': 'Gray 20',
    'Gray 30': 'Gray 30',
    'Gray 40': 'Gray 40',
    'Gray 50': 'Gray 50',
    'Gray 60': 'Gray 60',
    'Gray 70': 'Gray 70',
    'Gray 80': 'Gray 80',
    'Gray 90': 'Gray 90',
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

# Các nhãn giao diện chức năng màu PHẢI giữ tiếng Việt chuẩn mực
UI_LABELS = [
    ('Color', 'Màu'),
    ('Colors', 'Màu sắc'),
    ('Color Menu', 'Menu màu'),
    ('Color Name', 'Tên màu'),
    ('Color Selector', 'Bộ chọn màu'),
    ('Color Set', 'Bảng màu'),
    ('Color Setup', 'Thiết lập màu'),
    ('Colorize', 'Tô màu'),
    ('Choose Track Color', 'Chọn màu Track'),
    ('White Keys', 'Phím trắng'),
    ('Black Keys', 'Phím đen'),
]
for k, must in UI_LABELS:
    if k not in vi:
        problems.append(f'nhan giao dien khong thay: {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'nhan giao dien bi sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# Toàn bộ 32 tên màu trong bảng màu phải trùng khớp 100% với khóa tiếng Anh
for k, v in real.items():
    if after[k] != k:
        problems.append(f'ten mau chua giu nguyen tieng Anh: {k!r} -> {after[k]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Bảng màu: 32/32 tên màu đã giữ nguyên tiếng Anh chuẩn phòng thu')
print(f'[đối chiếu] Nhãn chức năng màu: "Màu", "Tô màu", "Phím trắng/đen" vẫn tiếng Việt')
print()
for k, v in changed.items():
    print(f'  {k[:20]!r:22} {vi.get(k, "")!r:25} -> {v!r}')

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
