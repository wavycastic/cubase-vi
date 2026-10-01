#!/usr/bin/env python3
r"""Vòng 114: 120 chuỗi, #1931-2050. Đọc tuần tự, không lọc.

Năm lỗi thuộc bốn nhóm rõ rệt:

1. `Constrain Delay Compensation` -> `Giới hạn bù trễ Delay`
   Bản dịch cũ thừa chữ "Delay" ("trễ Delay" lặp nghĩa).
   Toàn bộ các anh em trong nh��m đều dịch `Delay Compensation` là `bù trễ` hoặc `bù độ trễ`:
       `Delay Compensation Constrained` -> `Bù trễ đã bị giới hạn`
       `Delay Compensation Threshold (for Recording)` -> `Ngưỡng bù trễ (Dùng khi ghi âm)`
       `Track Delay Compensation` -> `Bù độ trễ Track`
   Sửa thành `Giới hạn bù trễ`, khớp hoàn toàn với `Bù trễ đã bị giới hạn`.

2. Thuộc tính Control trong MIDI Remote:
   - `Control Value (14Bit)` -> `Giá trị Control (14Bit)` (trước: `... điều khiển ...`)
   - `Control Value (7Bit)`  -> `Giá trị Control (7Bit)`  (trước: `... điều khiển ...`)
   Tất cả thuộc tính khác của Control đều giữ thuật ngữ `Control`:
       `Control Name` -> `Tên Control`
       `Control No.`  -> `Số Control`
       `Control Type` -> `Loại Control`
       `Control Settings` -> `Cài đặt Control`
       `Invert Control Value` -> `Đảo giá trị Control`
   Chỉ có 2 chuỗi này dịch sang "điều khiển" làm mất liên kết với `Invert Control Value`.

3. `Conversion Settings` -> `Cài đặt chuyển đổi` (trước: `Cài đặt Conversion`)
   Mọi chuỗi khác đều dịch `Conversion` là `chuyển đổi`:
       `Conversion failed!` -> `Chuyển đổi không thành công!`
       `Convert Options`    -> `Tùy chọn chuyển đổi`
       `O-Note Conversion`  -> `Chuyển đổi O-Note`
   Chỉ chuỗi này giữ nguyên tiếng Anh "Conversion".

4. `Convert Files...` -> `Chuyển đổi file...` (trước: `Chuyển đổi Files...`)
   - Bỏ chữ 's' số nhiều tiếng Anh và viết thường chữ "file".
   - Khớp với `Converter` (tên hiển thị `Convert Files`) -> `Chuyển đổi file`.
   - Khớp với tất cả lệnh Convert khác đều bỏ số nhiều:
       `Convert Channels...` -> `Chuyển đổi Channel...`
       `Convert Tracks`      -> `Chuyển đổi Track`
       `Convert Program List To VST Presets` -> `Chuyển danh sách Program sang VST Preset`

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
    'Constrain Delay Compensation': 'Giới hạn bù trễ',
    'Control Value (14Bit)': 'Giá trị Control (14Bit)',
    'Control Value (7Bit)': 'Giá trị Control (7Bit)',
    'Conversion Settings': 'Cài đặt chuyển đổi',
    'Convert Files...': 'Chuyển đổi file...',
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
    # 1. Delay Compensation
    ('Delay Compensation Constrained', 'Bù trễ đã bị giới hạn'),
    ('Delay Compensation Threshold (for Recording)', 'Ngưỡng bù trễ (Dùng khi ghi âm)'),
    ('Track Delay Compensation', 'Bù độ trễ Track'),
    # 2. Control Value vs Invert Control Value
    ('Invert Control Value', 'Đảo giá trị Control'),
    ('Control Name', 'Tên Control'),
    ('Control Type', 'Loại Control'),
    ('Control Settings', 'Cài đặt Control'),
    # 3. Conversion
    ('Conversion failed!', 'Chuyển đổi không thành công!'),
    ('Convert Options', 'Tùy chọn chuyển đổi'),
    # 4. Convert ... (số ít)
    ('Convert Channels...', 'Chuyển đổi Channel...'),
    ('Convert Tracks', 'Chuyển đổi Track'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Constrain Delay Compensation không còn chữ "Delay" lặp
if 'Delay' in after['Constrain Delay Compensation']:
    problems.append('Constrain Delay Compensation van con chu Delay')

# 2. Control Value dùng "Control", không dùng "điều khiển"
for k in ('Control Value (14Bit)', 'Control Value (7Bit)'):
    if 'điều khiển' in after[k]:
        problems.append(f'{k!r} van con chu "điều khiển"')
    if 'Control' not in after[k]:
        problems.append(f'{k!r} thieu chu "Control"')

# 3. Conversion Settings là "Cài đặt chuyển đổi"
if after['Conversion Settings'] != 'Cài đặt chuyển đổi':
    problems.append(f'Conversion Settings sai: {after["Conversion Settings"]!r}')

# 4. Convert Files... không còn chữ "Files"
if 'Files' in after['Convert Files...']:
    problems.append('Convert Files... van con chu "Files"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Constrain Delay Compensation: "Giới hạn bù trễ", hết lặp từ')
print(f'[đối chiếu] Control Value: đồng nhất với Invert Control Value và Control Name')
print(f'[đối chiếu] Conversion Settings: "Cài đặt chuyển đổi", sạch tiếng Anh')
print(f'[đối chiếu] Convert Files...: "Chuyển đổi file...", bỏ số nhiều tiếng Anh')
print()
for k, v in changed.items():
    print(f'  {k[:36]!r}')
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
