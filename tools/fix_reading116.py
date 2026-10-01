#!/usr/bin/env python3
r"""Vòng 116: 130 chuỗi, #2161-2290. Đọc tuần tự, không lọc.

Bảy lỗi thuộc bốn nhóm được sửa đồng bộ:

1. Bỏ số nhi��u tiếng Anh trong nhóm `Chord Events`:
   - `Create Chord Events`            -> `Tạo Chord Event`            (trước: `... Events`)
   - `Create Chord Events from Audio` -> `Tạo Chord Event từ Audio`   (trước: `... Events...`)
   - `Insert Chord Events`            -> `Chèn Chord Event`           (trước: `... Events`)
   Ba chuỗi này sót số nhiều 's', trong khi tất cả các anh em khác đã chuẩn hóa số ít:
       `Chord Track - Create Chord Events` -> `Chord Track - Tạo Chord Event`
       `Drop Chord Events from Chord Track...` -> `Thả Chord Event từ Chord Track...`
       `Show/Hide Drop Area for Chord Events...` -> `Hiện/Ẩn vùng thả cho Chord Event...`

2. Viết hoa chuẩn Title Case thuật ngữ mở rộng (AGENT.md §1):
   - `Create part using regions?` -> `Tạo Part bằng các Region?` (trước: `... region?`)
     Duy nhất 1 chuỗi này viết thường `region` trong toàn bộ cơ sở dữ liệu.
     Tất cả chuỗi khác đều viết hoa `Region`.
   - `Creating mixdown...` -> `Đang tạo Mixdown...` (trước: `... mixdown...`)
     Duy nhất 1 chuỗi này viết thường `mixdown` trong toàn bộ cơ sở dữ liệu (13/14 viết hoa `Mixdown`).

3. Viết thường danh từ tiếng Việt giữa cụm từ:
   - `Create Subfolder for Artist` -> `Tạo thư mục con cho nghệ sĩ` (trước: `... Nghệ sĩ`)
     Các anh em: `Enter Artist` -> `Nhập nghệ sĩ`, `Include Artist in File Name` -> `Đưa tên nghệ sĩ vào tên file`.

4. Viết thường danh từ "file":
   - `Create Unique File Name` -> `Tạo tên file duy nhất` (trước: `... File...`)
     Khớp với `Create Unique Name` -> `Tạo tên duy nhất` và toàn bộ các chuỗi `file`.

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
    'Create Chord Events': 'Tạo Chord Event',
    'Create Chord Events from Audio': 'Tạo Chord Event từ Audio',
    'Insert Chord Events': 'Chèn Chord Event',
    'Create Subfolder for Artist': 'Tạo thư mục con cho nghệ sĩ',
    'Create Unique File Name': 'Tạo tên file duy nhất',
    'Create part using regions?': 'Tạo Part bằng các Region?',
    'Creating mixdown...': 'Đang tạo Mixdown...',
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
    # 1. Chord Events số ít
    ('Chord Track - Create Chord Events', 'Chord Track - Tạo Chord Event'),
    ('Drop Chord Events from Chord Track or MIDI Parts here',
     'Thả Chord Event từ Chord Track hoặc MIDI Part vào đây'),
    # 2. Region và Mixdown viết hoa
    ('Create Regions', 'Tạo Region'),
    ('Create Regions from Hitpoints', 'Tạo Region từ các Hitpoint'),
    ('Complete Signal Path', 'Toàn bộ đường tín hiệu'),
    # 3. Nghệ sĩ viết thường
    ('Enter Artist', 'Nhập nghệ sĩ'),
    ('Include Artist in File Name', 'Đưa tên nghệ sĩ vào tên file'),
    # 4. File name
    ('Create Unique Name', 'Tạo tên duy nhất'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Toàn bộ nhóm Chord Events không còn chữ "Chord Events" số nhiều
ce_pl = [k for k, v in after.items() if 'Chord Events' in v]
if ce_pl:
    problems.append(f'van con "Chord Events" so nhieu: {ce_pl}')

# 2. Không còn "region" hoặc "mixdown" viết thường
if re.search(r'\bregion\b', after['Create part using regions?']):
    problems.append('Create part using regions? van con "region" thuong')
if re.search(r'\bmixdown\b', after['Creating mixdown...']):
    problems.append('Creating mixdown... van con "mixdown" thuong')

# 3. Create Subfolder for Artist không còn chữ "Nghệ sĩ" viết hoa
if 'Nghệ sĩ' in after['Create Subfolder for Artist']:
    problems.append('Create Subfolder for Artist van con "Nghệ sĩ" hoa')

# 4. Create Unique File Name không còn chữ "File" viết hoa
if 'File' in after['Create Unique File Name']:
    problems.append('Create Unique File Name van con "File" hoa')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Chord Event: sạch 100% số nhiều tiếng Anh "Chord Events"')
print(f'[đối chiếu] Region & Mixdown: 100% chuẩn Title Case theo AGENT.md §1')
print(f'[đối chiếu] Nghệ sĩ & file: viết thường chuẩn ngữ pháp tiếng Việt')
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
