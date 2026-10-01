#!/usr/bin/env python3
r"""Vòng 110: 80 chuỗi, #1521-1600. Đọc tuần tự, không lọc.

Sáu lỗi, chia thành bốn nhóm rõ ràng:

1. `Channel "%s" - Panner` -> `Panner của Channel "%s"`
   Cả bốn anh em cùng khuôn `Channel "%s" - ...` đều giữ nguyên cấu trúc:
       `Channel "%s" - Ins. %d`        -> `Channel "%s" - Insert %d`
       `Channel "%s" - Send Panner %d` -> `Channel "%s" - Send Panner %d`
       `Channel "%s" - Strip %d`       -> `Channel "%s" - Strip %d`
       `Channel "%s" - Synth`          -> `Channel "%s" - Synth`
   Riêng Panner bị đảo và mất dấu ` - ` (vi phạm quy ước khóa "X - Y" ở đợt 102).
   Sửa thành `Channel "%s" - Panner`.

2. Chữ hoa giữa cụm từ sau động từ "Đổi":
   - `Change Marker Attribute Name` -> `Đổi **Tên** Marker Attribute` -> `Đổi tên ...`
   - `Change Marker Attribute Type` -> `Đổi **Loại** Marker Attribute` -> `Đổi loại ...`
   - `Change Tempo Type`            -> `Đổi **Loại** Tempo`            -> `Đổi loại ...`
   Toàn bộ hơn 35 chuỗi `Rename ...` đều dùng `Đổi tên ...` (viết thường).
   Tất cả các chuỗi `Change ... Type` khác đều dùng `Đổi loại ...` (viết thường):
       `Change Instrument Type` -> `Đổi loại Instrument`
       `Change Type...`         -> `Đổi loại...`
   Chỉ có 3 chuỗi này viết hoa chữ cái đầu của danh từ tiếng Việt theo kiểu title case.

3. `Change channel of notes` -> `Đổi Channel của **các nốt**`
   Bộ ba lệnh đi cùng nhau trong menu MIDI / Logical Editor:
       `Change channel of notes`  -> `Đổi Channel của các nốt`  <- lọt tiếng Việt
       `Change length of notes`   -> `Đổi độ dài Note`          <- giữ Note
       `Change velocity of notes` -> `Đổi Velocity của Note`    <- giữ Note
   AGENT.md §1 quy định `Note` nằm trong 70 từ cốt lõi giữ tiếng Anh.
   Sửa thành `Đổi Channel của Note`, đồng nhất với `Đổi Velocity của Note`.

4. `Centered on Barline` -> `Căn theo vạch nhịp`
   Cặp thiết lập số Bar (Bar Numbers):
       `Centered on Bar`     -> `Căn giữa trong Bar`
       `Centered on Barline` -> `Căn theo vạch nhịp`  <- mất "giữa"
   "Centered" là "căn giữa", không phải chỉ là "căn" (align).
   Sửa thành `Căn giữa trên vạch nhịp`, đồng bộ với `Căn giữa trong Bar`.

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
    'Channel "%s" - Panner': 'Channel "%s" - Panner',
    'Change Marker Attribute Name': 'Đổi tên Marker Attribute',
    'Change Marker Attribute Type': 'Đổi loại Marker Attribute',
    'Change Tempo Type': 'Đổi loại Tempo',
    'Change channel of notes': 'Đổi Channel của Note',
    'Centered on Barline': 'Căn giữa trên vạch nhịp',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r}')
    if '%s' in src[k] and '%s' not in v:
        problems.append(f'missing placeholder %s in {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

# Anh em của từng nhóm
SIBLINGS = [
    # 1. Cấu trúc Channel "%s" - ...
    ('Channel "%s" - Ins. %d', 'Channel "%s" - Insert %d'),
    ('Channel "%s" - Send Panner %d', 'Channel "%s" - Send Panner %d'),
    ('Channel "%s" - Strip %d', 'Channel "%s" - Strip %d'),
    ('Channel "%s" - Synth', 'Channel "%s" - Synth'),
    # 2. Viết thường tên / loại sau Đổi
    ('Change Instrument Type', 'Đổi loại Instrument'),
    ('Change Type...', 'Đổi loại...'),
    ('Rename Layout', 'Đổi tên Layout'),
    ('Rename Track Version', 'Đổi tên Track Version'),
    # 3. Note trong bộ ba Change ... of notes
    ('Change length of notes', 'Đổi độ dài Note'),
    ('Change velocity of notes', 'Đổi Velocity của Note'),
    # 4. Centered on
    ('Centered on Bar', 'Căn giữa trong Bar'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Toàn bộ nhóm Channel "%s" - ... phải có dấu " - "
ch_p = [k for k in after if k.startswith('Channel "%s" -')]
if len(ch_p) != 5:
    problems.append(f'nhom Channel "%s" - co {len(ch_p)} chuoi, mong doi 5')
for k in ch_p:
    if ' - ' not in after[k]:
        problems.append(f'chuoi mat dau " - ": {k!r} -> {after[k]!r}')

# 2. Không còn "Đổi Tên" hoặc "Đổi Loại" viết hoa
bad_caps = [k for k, v in after.items() if re.match(r'^Đổi (Tên|Loại)\b', v)]
if bad_caps:
    problems.append(f'con viet hoa danh tu sau Doi: {bad_caps}')

# 3. Bộ ba of notes không còn "các nốt"
if 'các nốt' in after['Change channel of notes']:
    problems.append('Change channel of notes van con "các nốt"')

# 4. Centered on Barline có "Căn giữa"
if not after['Centered on Barline'].startswith('Căn giữa'):
    problems.append('Centered on Barline khong co "Căn giữa"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Channel "%s" - ...: 5/5 đều giữ cấu trúc')
print(f'[đối chiếu] "Đổi tên/loại": không còn viết hoa giữa cụm')
print(f'[đối chiếu] bộ ba "Change ... of notes": đều dùng "Note"')
print(f'[đối chiếu] Centered on: 2/2 đều là "Căn giữa..."')
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
