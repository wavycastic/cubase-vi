#!/usr/bin/env python3
r"""Vòng 123: 80 chuỗi, #2751-2830 (kèm Up Arpeggios ở #10116 theo gia đình Arpeggio). Đọc tuần tự, không lọc.

Bảy lỗi được phát hiện và sửa theo gia đình:

1. Đồng bộ cặp đối ứng `Down Arpeggios` ↔ `Up Arpeggios`:
   - `Down Arpeggios` -> `Arpeggio đi xuống` (trước: `Down Arpeggios` - để nguyên tiếng Anh)
   - `Up Arpeggios`   -> `Arpeggio đi lên`   (trước: `Rải âm lên` - dịch lệch thuật ngữ)
   Hai chuỗi này là cặp tùy chọn hướng rải nốt trong Score Editor.
   Đồng bộ 100% với hai thiết lập hình dạng ngay cạnh:
       `Appearance of Down Arpeggios` -> `Hình dạng của Arpeggio đi xuống`
       `Appearance of Up Arpeggios`   -> `Hình dạng của Arpeggio đi lên`

2. Sửa lỗi dịch máy ngô nghê trong `Drag Delay`:
   - `Drag Delay` -> `Độ trễ khi kéo` (trước: `Kéo Delay`)
   "Drag Delay" là một thiết lập trong Preferences > Editing của Cubase quy định
   khoảng trễ tính bằng mili-giây trước khi thao tác kéo chuột bắt đầu di chuyển
   sự kiện để tránh vô tình rê chuột. Dịch thành "Kéo Delay" là hiểu nhầm thành
   động từ mệnh lệnh.

3. Dọn tiếng Anh thô và thừa từ trong chuỗi tín hiệu:
   - `Drag to change order of modulators in signal chain`
       -> `Kéo để đổi thứ tự Modulator trong chuỗi tín hiệu`
       (trước: `... trong signal chain` - sót tiếng Anh thô)
   - `Drag to change order of modules in signal path`
       -> `Kéo để đổi thứ tự các Module trong đường tín hiệu`
       (bỏ chữ "truyền" thừa, đồng bộ với "đường tín hiệu" ở đợt 113)

4. Bỏ số nhiều 's' trong `Dropouts`:
   - `Dropouts` -> `Dropout` (trước: `Dropouts`)
   Khớp với `Dropout` -> `Dropout`, `Next Dropout` -> `Dropout kế tiếp`.

5. Chuẩn hóa `Note` trong `Drum Editor: Show Note Length On/Off`:
   - `Drum Editor: Show Note Length On/Off`
       -> `Drum Editor: Bật/Tắt hiện độ dài Note` (trước: `... độ dài nốt`)
   Khớp với chuỗi song sinh:
       `Show Note Length On/Off` -> `Bật/Tắt hiển thị độ dài Note`
       `Note Length`             -> `Độ dài Note`
       `Set Note Length`         -> `Đặt độ dài Note`
   (AGENT.md §1: `Note` là 70 từ cốt lõi giữ nguyên).

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
    'Down Arpeggios': 'Arpeggio đi xuống',
    'Up Arpeggios': 'Arpeggio đi lên',
    'Drag Delay': 'Độ trễ khi kéo',
    'Drag to change order of modulators in signal chain':
        'Kéo để đổi thứ tự Modulator trong Signal Chain',
    'Drag to change order of modules in signal path':
        'Kéo để đổi thứ tự các Module trong đường tín hiệu',
    'Dropouts': 'Dropout',
    'Drum Editor: Show Note Length On/Off':
        'Drum Editor: Bật/Tắt hiện độ dài Note',
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
    # 1. Appearance of Arpeggios
    ('Appearance of Down Arpeggios', 'Hình dạng của Arpeggio đi xuống'),
    ('Appearance of Up Arpeggios', 'Hình dạng của Arpeggio đi lên'),
    # 2. Complete Signal Path
    ('Complete Signal Path', 'Toàn bộ đường tín hiệu'),
    # 3. Dropout
    ('Dropout', 'Dropout'),
    ('Next Dropout', 'Dropout kế tiếp'),
    # 4. Note Length
    ('Note Length', 'Độ dài Note'),
    ('Set Note Length', 'Đặt độ dài Note'),
    ('Show Note Length On/Off', 'Bật/Tắt hiển thị độ dài Note'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Cặp Arpeggios
if after['Down Arpeggios'] != 'Arpeggio đi xuống':
    problems.append(f'Down Arpeggios sai: {after["Down Arpeggios"]!r}')
if after['Up Arpeggios'] != 'Arpeggio đi lên':
    problems.append(f'Up Arpeggios sai: {after["Up Arpeggios"]!r}')

# 2. Drag Delay không còn "Kéo Delay"
if after['Drag Delay'] != 'Độ trễ khi kéo':
    problems.append(f'Drag Delay sai: {after["Drag Delay"]!r}')

# 3. Không còn "signal chain" viết thường
if 'signal chain' in after['Drag to change order of modulators in signal chain']:
    problems.append('Van con chu signal chain tieng Anh')
if 'Signal Chain' not in after['Drag to change order of modulators in signal chain']:
    problems.append('Thieu Signal Chain viet hoa chuan thuat ngu')

# 4. Dropouts không còn chữ "s"
if after['Dropouts'] != 'Dropout':
    problems.append(f'Dropouts sai: {after["Dropouts"]!r}')

# 5. Drum Editor: Show Note Length On/Off có "độ dài Note"
if 'độ dài Note' not in after['Drum Editor: Show Note Length On/Off']:
    problems.append('Drum Editor: Show Note Length On/Off thieu "độ dài Note"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Arpeggios: đồng bộ cặp Down/Up Arpeggios khớp Appearance')
print(f'[đối chiếu] Drag Delay: "Độ trễ khi kéo", sửa lỗi hiểu sai ngữ pháp')
print(f'[đối chiếu] Chuỗi tín hiệu: dịch sạch "signal chain" -> "chuỗi tín hiệu"')
print(f'[đối chiếu] Dropouts: bỏ số nhiều "s"')
print(f'[đối chiếu] Note Length: "độ dài Note", khớp 100% với Show Note Length On/Off')
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
