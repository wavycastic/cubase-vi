#!/usr/bin/env python3
r"""Vòng 118: 120 chuỗi, #2401-2520 (kèm 3 chuỗi thuộc gia đình lệnh Pool Audio Files ở #5118, #5119, #7698). Đọc tuần tự, không lọc.

Bảy lỗi nghiêm trọng được phát hiện và sửa theo gia đình:

1. Nhóm lệnh thao tác file trong cửa sổ Pool bị dịch đảo ngược ngữ pháp và sót tiếng Anh:
   - `Minimize File`            -> `Thu nhỏ file`             (trước: `File Minimize`)
   - `Minimize Audio Files`     -> `Thu nhỏ file Audio`       (trước: `File Minimize Audio`)
   - `Search Audio Files...`    -> `Tìm kiếm file Audio...`   (trước: `File Search Audio...`)
   - `Delete Unused Audio Files`-> `Xóa file Audio không dùng`(trước: `Xóa Audio File không dùng`)
   - `Delete Files`             -> `Xóa file`                 (trước: `Xóa Files`)

   Người dịch cũ hiểu lầm động từ "Minimize" và "Search" thành tính từ bổ nghĩa cho "File",
   dẫn đến các chuỗi dịch máy đảo ngược: "File Minimize", "File Minimize Audio", "File Search Audio...".
   Đây là các câu lệnh menu mệnh lệnh trong cửa sổ Pool của Cubase:
       `Minimize`     -> `Thu nhỏ` (khớp `Minimize All` -> `Thu nhỏ tất cả`)
       `Search Pool`  -> `Tìm kiếm Pool`
       `Audio Files`  -> `file Audio` (khớp `Import file Audio`, `File Audio...`)
       `Delete Files` -> `Xóa file` (khớp `Sao chép file`, `Đang xóa file...`)

2. Bỏ số nhiều tiếng Anh trong nhóm `Default ...`:
   - `Default Items`       -> `Mục mặc định`          (trước: `Items mặc định`)
     Khớp với `Set up Items` -> `Thiết lập mục`, `Show All Items` -> `Hiện tất cả mục`.
   - `Default Permissions` -> `Permission mặc định`   (trước: `Permissions mặc định`)
     Bỏ số nhiều 's', khớp với thuật ngữ chuẩn `Permission` theo AGENT.md §1
     và các anh em: `Permission Status` -> `Trạng thái Permission`,
     `Add Permission Preset` -> `Thêm Preset Permission`.

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
    'Delete Files': 'Xóa file',
    'Delete Unused Audio Files': 'Xóa file Audio không dùng',
    'Minimize File': 'Thu nhỏ file',
    'Minimize Audio Files': 'Thu nhỏ file Audio',
    'Search Audio Files...': 'Tìm kiếm file Audio...',
    'Default Items': 'Mục mặc định',
    'Default Permissions': 'Permission mặc định',
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
    # 1. Pool & Minimize & Search
    ('Minimize', 'Thu nhỏ'),
    ('Minimize All', 'Thu nhỏ tất cả'),
    ('Search Pool', 'Tìm kiếm Pool'),
    ('Import Audio Files', 'Import file Audio'),
    ('Copy Files', 'Sao chép file'),
    ('Deleting Files...', 'Đang xóa file...'),
    # 2. Items -> mục
    ('Show All Items', 'Hiện tất cả mục'),
    ('Set up Items', 'Thiết lập mục'),
    # 3. Permission
    ('Permission Status', 'Trạng thái Permission'),
    ('Add Permission Preset', 'Thêm Preset Permission'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Không còn "File Minimize" hoặc "File Search Audio"
if after['Minimize File'] != 'Thu nhỏ file':
    problems.append(f'Minimize File van sai: {after["Minimize File"]!r}')
if after['Minimize Audio Files'] != 'Thu nhỏ file Audio':
    problems.append(f'Minimize Audio Files van sai: {after["Minimize Audio Files"]!r}')
if after['Search Audio Files...'] != 'Tìm kiếm file Audio...':
    problems.append(f'Search Audio Files... van sai: {after["Search Audio Files..."]!r}')
if after['Delete Unused Audio Files'] != 'Xóa file Audio không dùng':
    problems.append(f'Delete Unused Audio Files van sai: {after["Delete Unused Audio Files"]!r}')
if after['Delete Files'] != 'Xóa file':
    problems.append(f'Delete Files van sai: {after["Delete Files"]!r}')

# 2. Không còn "Items mặc định" hoặc "Permissions mặc định"
if 'Items' in after['Default Items']:
    problems.append('Default Items van con "Items"')
if 'Permissions' in after['Default Permissions']:
    problems.append('Default Permissions van con "Permissions"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Lệnh Pool: sửa dứt điểm trật tự từ ngược "File Minimize", "File Search Audio"')
print(f'[đối chiếu] Audio Files: đồng nhất "Xóa file Audio không dùng" khớp Import file Audio')
print(f'[đối chiếu] Default: "Mục mặc định" và "Permission mặc định", sạch số nhiều tiếng Anh')
print()
for k, v in changed.items():
    print(f'  {k[:34]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
