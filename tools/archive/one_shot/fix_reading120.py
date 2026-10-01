#!/usr/bin/env python3
r"""Vòng 120: 75 chuỗi, #2521-2595. Đọc tuần tự, không lọc.

Sáu lỗi thuộc ba nhóm rõ rệt:

1. Đồng bộ cặp đối ứng "Source Track" ↔ "Destination Track":
   - `Reset Destination Tracks` -> `Đặt lại Destination Track` (trước: `... Track đích`)
   - `Select Matching Destination Tracks` -> `Chọn Destination Track khớp` (trước: `... Track đích...`)
   - `Destination track already contains chord events.`
       -> `Destination Track đã chứa Chord Event.` (trước: `Track đích...`)

   Toàn bộ 11 chuỗi chứa "Source Track" đều giữ nguyên tiếng Anh `Source Track`
   (`Source Track`, `Delete Source Tracks`, `Deselect All Source Tracks`,
   `Select All Source Tracks`, `Mute Source Tracks`...).
   Hai cột của cùng một hộp thoại Import Track đối xứng nhau: Source Track ↔ Destination Track.
   Khóa `Destination Track` đã giữ tiếng Anh, nhưng 3 chuỗi thao tác liên quan lại dịch
   lệch thành "Track đích". Sửa đồng bộ thành `Destination Track`.

2. Nhóm `Device` (Thiết bị) bị lọt tiếng Anh:
   - `Device Panels` -> `Bảng thiết bị` (trước: `Bảng Device`)
     Khớp 100% với `Device Panel` -> `Bảng thiết bị`, `Select Device Panel` -> `Chọn Bảng thiết bị`,
     `Open Device Panel` -> `Mở Bảng thiết bị`.
   - `Device failed to open!` -> `Không thể mở thiết bị!` (trước: `... mở Device!`)
     Khớp với `Device` -> `Thiết bị`, `Devices` -> `Thiết bị`, `Device Setup...` -> `Thiết lập thiết bị...`.

3. Quãng nhạc lý bị sót tiếng Anh:
   - `Dim. Fifth` -> `Quãng 5 giảm` (trước: `Dim. Fifth`)
     Cặp đối ứng đối cực trực tiếp trong nhạc lý:
         `Aug. Fifth` (Augmented Fifth)  -> `Quãng 5 tăng`
         `Dim. Fifth` (Diminished Fifth) -> `Quãng 5 giảm`
     `Aug. Fifth` đã dịch chuẩn, trong khi `Dim. Fifth` bị bỏ quên nguyên xi tiếng Anh.

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
    'Reset Destination Tracks': 'Đặt lại Destination Track',
    'Select Matching Destination Tracks': 'Chọn Destination Track khớp',
    'Destination track already contains chord events.':
        'Destination Track đã chứa Chord Event.',
    'Device Panels': 'Bảng thiết bị',
    'Device failed to open!': 'Không thể mở thiết bị!',
    'Dim. Fifth': 'Quãng 5 giảm',
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
    # 1. Source Track vs Destination Track
    ('Source Track', 'Source Track'),
    ('Select All Source Tracks', 'Source Track'),
    ('Destination Track', 'Destination Track'),
    # 2. Device Panel
    ('Device Panel', 'Bảng thiết bị'),
    ('Select Device Panel', 'Bảng thiết bị'),
    ('Device', 'Thiết bị'),
    ('Device Setup...', 'thiết bị'),
    # 3. Quãng nhạc lý
    ('Aug. Fifth', 'Quãng 5 tăng'),
    ('Maj. Seventh', 'Quãng bảy trưởng'),
    ('Min. Seventh', 'Quãng bảy thứ'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Không còn "Track đích"
for k in ('Reset Destination Tracks', 'Select Matching Destination Tracks', 'Destination track already contains chord events.'):
    if 'Track đích' in after[k]:
        problems.append(f'{k!r} van con chu "Track đích"')
    if 'Destination Track' not in after[k]:
        problems.append(f'{k!r} thieu "Destination Track"')

# 2. Device Panels và Device failed to open dùng "thiết bị"
if 'Bảng thiết bị' not in after['Device Panels']:
    problems.append('Device Panels khong phai "Bảng thiết bị"')
if 'mở thiết bị' not in after['Device failed to open!']:
    problems.append('Device failed to open! khong chua "mở thiết bị"')

# 3. Dim. Fifth là "Quãng 5 giảm"
if after['Dim. Fifth'] != 'Quãng 5 giảm':
    problems.append(f'Dim. Fifth sai: {after["Dim. Fifth"]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Destination Track: đồng bộ 100% với Source Track')
print(f'[đối chiếu] Thiết bị: dọn sạch tiếng Anh trong Device Panels và Device failed')
print(f'[đối chiếu] Quãng nhạc lý: Dim. Fifth -> "Quãng 5 giảm", đối xứng Aug. Fifth')
print()
for k, v in changed.items():
    print(f'  {k[:42]!r}')
    print(f'      {vi.get(k, "")!r}')
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
