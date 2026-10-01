#!/usr/bin/env python3
r"""Vòng 117: 110 chuỗi, #2291-2400. Đọc tuần tự, không lọc.

Bảy lỗi được phát hiện và sửa theo gia đình:

1. Toàn bộ nhóm màu "Dark <Màu>" bị dịch ngược trật tự từ:
   - `Dark Blue`    -> `Xanh dương đậm`     (trước: `Tối Xanh dương`)
   - `Dark Green`   -> `Xanh lá đậm`        (trước: `Tối Xanh lá`)
   - `Dark Red`     -> `Đỏ đậm`             (trước: `Tối Đỏ`)
   - `Dark Yellow`  -> `Vàng đậm`           (trước: `Tối Vàng`)
   - `Dark Orange`  -> `Cam đậm`            (trước: `Tối Cam`)
   - `Dark Magenta` -> `Hồng cánh sen đậm`  (trước: `Tối Đỏ tươi`)

   Đối chiếu với nhóm màu "Light <Màu>":
       `Light Blue`    -> `Xanh dương nhạt`
       `Light Green`   -> `Xanh lá nhạt`
       `Light Red`     -> `Đỏ nhạt`
       `Light Yellow`  -> `Vàng nhạt`
       `Light Orange`  -> `Cam nhạt`
       `Light Magenta` -> `Hồng cánh sen nhạt`
   Cả 6 màu "Light" đều theo trật tự tự nhiên của tiếng Việt: `[Tên màu] + nhạt`.
   Nhưng 6 màu "Dark" lại bị dịch máy thô thiển đưa từ "Tối" lên đầu cụm từ.
   Hơn nữa, `Magenta` vốn là `Hồng cánh sen` (khớp cả `Magenta` và `Light Magenta`),
   nhưng `Dark Magenta` lại dịch sai tên màu thành `Đỏ tươi`.
   Sửa toàn bộ về `[Tên màu] + đậm`, tạo thành hệ thống màu chuẩn xác:
   nhạt ↔ đậm.

2. Bỏ số nhiều 's' trong `Current MIDI Loops`:
   - `Current MIDI Loops` -> `MIDI Loop hiện tại` (trước: `MIDI Loops...`)
   Tất cả các anh em chứa `Loops` đều đã bỏ số nhiều:
       `MIDI Loops`      -> `MIDI Loop`
       `Loops & Samples` -> `Loop & Sample`

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
    'Dark Blue': 'Xanh dương đậm',
    'Dark Green': 'Xanh lá đậm',
    'Dark Red': 'Đỏ đậm',
    'Dark Yellow': 'Vàng đậm',
    'Dark Orange': 'Cam đậm',
    'Dark Magenta': 'Hồng cánh sen đậm',
    'Current MIDI Loops': 'MIDI Loop hiện tại',
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
    # 1. Các màu Light tương ứng
    ('Light Blue', 'Xanh dương nhạt'),
    ('Light Green', 'Xanh lá nhạt'),
    ('Light Red', 'Đỏ nhạt'),
    ('Light Yellow', 'Vàng nhạt'),
    ('Light Orange', 'Cam nhạt'),
    ('Light Magenta', 'Hồng cánh sen nhạt'),
    ('Magenta', 'Hồng cánh sen'),
    # 2. Loops số ít
    ('MIDI Loops', 'MIDI Loop'),
    ('Loops & Samples', 'Loop & Sample'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Không còn màu nào bắt đầu bằng "Tối "
bad_dark = [k for k in ('Dark Blue', 'Dark Green', 'Dark Red', 'Dark Yellow', 'Dark Orange', 'Dark Magenta')
            if after[k].startswith('Tối ')]
if bad_dark:
    problems.append(f'van con mau bat dau bang "Tối ": {bad_dark}')

# 2. Cả 6 màu Dark đều kết thúc bằng "đậm"
for k in ('Dark Blue', 'Dark Green', 'Dark Red', 'Dark Yellow', 'Dark Orange', 'Dark Magenta'):
    if not after[k].endswith('đậm'):
        problems.append(f'{k!r} khong ket thuc bang "đậm": {after[k]!r}')

# 3. Magenta phải là Hồng cánh sen
if 'Hồng cánh sen' not in after['Dark Magenta']:
    problems.append(f'Dark Magenta sai mau: {after["Dark Magenta"]!r}')

# 4. Current MIDI Loops không còn chữ "Loops"
if 'Loops' in after['Current MIDI Loops']:
    problems.append('Current MIDI Loops van con "Loops"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Màu Dark: 6/6 màu chuyển từ "Tối [Màu]" sang "[Màu] đậm"')
print(f'[đối chiếu] Dark Magenta: sửa cả trật tự từ lẫn tên màu chuẩn "Hồng cánh sen"')
print(f'[đối chiếu] MIDI Loop: bỏ số nhiều "Loops" đồng nhất với MIDI Loops')
print()
for k, v in changed.items():
    print(f'  {k[:30]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
