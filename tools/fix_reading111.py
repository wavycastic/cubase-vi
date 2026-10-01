#!/usr/bin/env python3
r"""Vòng 111: 125 chuỗi, #1601-1725. Đọc tuần tự, không lọc.

Bốn lỗi, mỗi lỗi đều được đối chiếu bằng cả gia đình anh em:

1. `Chord Editing - Add to Chord Track` -> `Sửa hợp âm - Thêm vào Chord Track`
   Bảy anh em trong nhóm `Chord Editing` đều dùng `Chỉnh sửa hợp âm`:
       `Chord Editing`                        -> `Chỉnh sửa hợp âm`
       `Chord Editing - Drop 2`               -> `Chỉnh sửa hợp âm - Drop 2`
       `Chord Editing - Drop 2 + 4`           -> `Chỉnh sửa hợp âm - Drop 2 + 4`
       `Chord Editing - Drop 3`               -> `Chỉnh sửa hợp âm - Drop 3`
       `Chord Editing - Inversions: Move Down`-> `Chỉnh sửa hợp âm - Đảo: Xuống`
       `Chord Editing - Inversions: Move Up`  -> `Chỉnh sửa hợp âm - Đảo: Lên`
       `Chord Editing - Match with Chord Track`-> `Chỉnh sửa hợp âm - Đối chiếu...`
   Duy nhất chuỗi này rút gọn thành `Sửa hợp âm`. Sửa lại để thống nhất toàn bộ.

2. `Choose a Volume Mode` -> `Chọn một chế độ **âm lượng**`
   Cả bộ ba chế độ trích xuất/xử lý và khóa trần đều giữ thuật ngữ tiếng Anh:
       `Choose a Pitch Extraction Mode` -> `Chọn một chế độ trích xuất Pitch`
       `Choose a Velocity Mode`         -> `Chọn một chế độ Velocity`
       `Volume Mode` (khóa trần)        -> `Chế độ Volume`
   Sửa thành `Chọn một chế độ Volume`, đồng nhất với bộ ba và khóa trần.

3. `Chord Type` -> `Loại **Chord**`
   Tất cả thuộc tính của hợp âm âm nhạc đều dịch là `hợp âm`:
       `Chord`                         -> `Hợp âm`
       `Chord Data`                    -> `Dữ liệu hợp âm`
       `Chord Font`                    -> `Font hợp âm`
       `Chord Modifiers`               -> `Modifier hợp âm`
       `Chord Note Distribution`       -> `Phân bố nốt của hợp âm`
       `Chord Notes`                   -> `Nốt của hợp âm`
       `Chord Symbol`                  -> `Ký hiệu hợp âm`
       `Chord Symbols Preset`          -> `Preset ký hiệu hợp âm`
       `Chord type of selected notes`  -> `Loại hợp âm của các nốt đã chọn`
   Chỉ khi "Chord" đi cùng tên riêng của thành phần giao diện (Chord Track,
   Chord Pad, Chord Assistant, Chord Editor, Chord Event, Chord Tool) thì mới
   giữ `Chord`. Ở đây "Chord Type" là loại hợp âm (Trưởng, Thứ...), ngay cạnh
   `Chord type of selected notes`. Sửa thành `Loại hợp âm`.

4. `Chords & Pitches` -> `Hợp âm & **cao độ**`
   - Cặp song hành ngay cạnh:
       `Chords & Scales`  -> `Hợp âm & Scale`  (giữ Scale)
       `Chords & Pitches` -> `Hợp âm & cao độ` <- lọt dịch
   - 11/12 chuỗi chứa `Pitches` đều dịch sang `Pitch`:
       `Quantize Pitches`          -> `Quantize Pitch`
       `Quantize Pitches to Scale` -> `Quantize Pitch theo Scale`
       `Filter Pitches Above`      -> `Lọc Pitch phía trên`
   - AGENT.md §1: `Pitch` nằm trong 70 từ cốt lõi giữ nguyên.
   Sửa thành `Hợp âm & Pitch`.

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
    'Chord Editing - Add to Chord Track':
        'Chỉnh sửa hợp âm - Thêm vào Chord Track',
    'Choose a Volume Mode':
        'Chọn một chế độ Volume',
    'Chord Type':
        'Loại hợp âm',
    'Chords & Pitches':
        'Hợp âm & Pitch',
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
    # 1. Chord Editing
    ('Chord Editing', 'Chỉnh sửa hợp âm'),
    ('Chord Editing - Drop 2', 'Chỉnh sửa hợp âm - Drop 2'),
    ('Chord Editing - Drop 3', 'Chỉnh sửa hợp âm - Drop 3'),
    ('Chord Editing - Inversions: Move Down', 'Chỉnh sửa hợp âm - Đảo: Xuống'),
    ('Chord Editing - Match with Chord Track', 'Chỉnh sửa hợp âm - Đối chiếu với Chord Track'),
    # 2. Volume Mode
    ('Volume Mode', 'Chế độ Volume'),
    ('Choose a Pitch Extraction Mode', 'Chọn một chế độ trích xuất Pitch'),
    ('Choose a Velocity Mode', 'Chọn một chế độ Velocity'),
    # 3. Chord Type vs Chord type of selected notes
    ('Chord type of selected notes', 'Loại hợp âm của các nốt đã chọn'),
    ('Chord Data', 'Dữ liệu hợp âm'),
    ('Chord Symbol', 'Ký hiệu hợp âm'),
    # 4. Pitches -> Pitch
    ('Chords & Scales', 'Hợp âm & Scale'),
    ('Quantize Pitches', 'Quantize Pitch'),
    ('Filter Pitches Above', 'Lọc Pitch phía trên'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Nhóm Chord Editing phải 100% bắt đầu bằng "Chỉnh sửa hợp âm"
ce = [k for k in after if k.startswith('Chord Editing')]
if len(ce) != 8:
    problems.append(f'nhom Chord Editing co {len(ce)} chuoi, mong doi 8')
for k in ce:
    if not after[k].startswith('Chỉnh sửa hợp âm'):
        problems.append(f'Chord Editing van con lech: {k!r} -> {after[k]!r}')

# 2. Choose a Volume Mode có "chế độ Volume"
if 'chế độ Volume' not in after['Choose a Volume Mode']:
    problems.append('Choose a Volume Mode khong chua "chế độ Volume"')

# 3. Chord Type là "Loại hợp âm"
if after['Chord Type'] != 'Loại hợp âm':
    problems.append(f'Chord Type sai: {after["Chord Type"]!r}')

# 4. Chords & Pitches là "Hợp âm & Pitch"
if after['Chords & Pitches'] != 'Hợp âm & Pitch':
    problems.append(f'Chords & Pitches sai: {after["Chords & Pitches"]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Chord Editing: 8/8 đều dùng "Chỉnh sửa hợp âm"')
print(f'[đối chiếu] Choose a Volume Mode: đồng nhất với Pitch, Velocity và Volume Mode')
print(f'[đối chiếu] Chord Type: "Loại hợp âm", khớp Chord type of selected notes')
print(f'[đối chiếu] Chords & Pitches: "Hợp âm & Pitch", khớp Chords & Scales')
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
        with open(path, 'w', encoding='utf-8', newline='') as fh:\
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
print(f'\nđã ghi {n} thay đổi vào batches')
