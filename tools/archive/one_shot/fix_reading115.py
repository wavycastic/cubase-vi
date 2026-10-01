#!/usr/bin/env python3
r"""Vòng 115: 110 chuỗi, #2051-2160 (kèm 1 chuỗi thuộc gia đình Skin ở #4300). Đọc tuần tự, không lọc.

Bảy lỗi được phát hiện và sửa theo gia đình:

1. `Invalid Skin File!` -> `không hợp lệ Skin File!`
   Lỗi trật tự từ nghiêm trọng: đảo ngược ngữ pháp tiếng Việt ("không hợp lệ" + "Skin File").
   Sửa thành `File Skin không hợp lệ!`, khớp hoàn toàn với anh em cùng nhóm:
       `Doesn't seem to be a valid skin file!` -> `Đây có vẻ không phải là file Skin hợp lệ!`
       `Skin Files` -> `Các file Skin`
   Và sửa luôn:
       `Could not save skin file!` -> `Không thể lưu file Skin!` (trước: `... skin file!`)

2. Lọt tiếng Anh nguyên xi "mount/unmount database":
   - `Could not mount database.`   -> `Không thể gắn kết cơ sở dữ liệu.` (trước: `... mount database.`)
   - `Could not unmount database.` -> `Không thể ngắt gắn kết cơ sở dữ liệu.` (trước: `... unmount database.`)
   Cả hai chuỗi đều dịch sót tiếng Anh thô trong khi các lệnh gắn kết ổ đĩa của MediaBay
   đã có thuật ngữ chuẩn mực:
       `Mount Volume Database`     -> `Gắn kết cơ sở dữ liệu ổ đĩa`
       `Unmount Volume Database...`-> `Ngắt gắn kết cơ sở dữ liệu ổ đĩa...`

3. `Could not import all tracks! The data is corrupted.`
   -> `Không thể Import tất cả Track! Dữ liệu bị hỏng.`
   (trước: `Không import được tất cả Track!...`)
   - Khớp 100% với chuỗi anh em sinh đôi:
       `Could not import the Clip Package! The data is corrupted.`
           -> `Không thể Import gói Clip! Dữ liệu bị hỏng.`
   - 88/94 chuỗi trong toàn bộ phần mềm đều viết hoa `Import` (AGENT.md §1: 70 từ cốt lõi).

4. Viết thường danh từ tiếng Việt và danh từ "file":
   - `Copy Color`   -> `Sao chép màu` (trước: `Sao chép Màu`)
     Toàn bộ hơn 18 chuỗi `Sao chép ...` chỉ viết hoa danh từ riêng/thuật ngữ tiếng Anh,
     danh từ tiếng Việt đều viết thường (`Sao chép file`, `Sao chép bắt đầu`...).
   - `Copied Files` -> `Các file đã sao chép` (trước: `Các File đã sao chép`)
     Viết thường chữ "file", khớp với `Sao chép file`, `Đang sao chép file...`.

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
    'Copy Color': 'Sao chép màu',
    'Copied Files': 'Các file đã sao chép',
    'Could not import all tracks! The data is corrupted.':
        'Không thể Import tất cả Track! Dữ liệu bị hỏng.',
    'Could not mount database.':
        'Không thể gắn kết cơ sở dữ liệu.',
    'Could not unmount database.':
        'Không thể ngắt gắn kết cơ sở dữ liệu.',
    'Could not save skin file!':
        'Không thể lưu file Skin!',
    'Invalid Skin File!':
        'File Skin không hợp lệ!',
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
    # 1. Skin
    ("Doesn't seem to be a valid skin file!", 'Đây có vẻ không phải là file Skin hợp lệ!'),
    ('Skin Files', 'Các file Skin'),
    # 2. Mount/Unmount
    ('Mount Volume Database', 'Gắn kết cơ sở dữ liệu ổ đĩa'),
    ('Unmount Volume Database...', 'Ngắt gắn kết cơ sở dữ liệu ổ đĩa...'),
    # 3. Could not import
    ('Could not import the Clip Package! The data is corrupt.',
     'Không thể Import gói Clip! Dữ liệu bị hỏng.'),
    ('Could not import all resources!',
     'Không thể Import tất cả tài nguyên!'),
    # 4. Copy ...
    ('Copy Files', 'Sao chép file'),
    ('Copy All Files to Project Folder', 'Sao chép tất cả file vào thư mục Project'),
    ('Copy Start', 'Sao chép bắt đầu'),
    ('Copy End', 'Sao chép kết thúc'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Skin files không còn cấu trúc ngược hoặc "skin file"
if after['Invalid Skin File!'] != 'File Skin không hợp lệ!':
    problems.append(f'Invalid Skin File! van sai: {after["Invalid Skin File!"]!r}')
if after['Could not save skin file!'] != 'Không thể lưu file Skin!':
    problems.append(f'Could not save skin file! van sai: {after["Could not save skin file!"]!r}')

# 2. Không còn "mount database" hoặc "unmount database" tiếng Anh
for k in ('Could not mount database.', 'Could not unmount database.'):
    if re.search(r'\b(mount|unmount)\b', after[k]):
        problems.append(f'{k!r} van con chu mount/unmount: {after[k]!r}')

# 3. Could not import all tracks viết hoa Import và có cấu trúc "Không thể Import"
if not after['Could not import all tracks! The data is corrupted.'].startswith('Không thể Import'):
    problems.append(f'Import all tracks khong bat dau bang "Không thể Import": {after["Could not import all tracks! The data is corrupted."]!r}')

# 4. Copy Color và Copied Files viết thường
if after['Copy Color'] != 'Sao chép màu':
    problems.append(f'Copy Color van sai: {after["Copy Color"]!r}')
if after['Copied Files'] != 'Các file đã sao chép':
    problems.append(f'Copied Files van sai: {after["Copied Files"]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Skin: sửa lỗi ngữ pháp đảo ngược trật tự từ "không hợp lệ Skin File!"')
print(f'[đối chiếu] Mount/Unmount database: chuyển thành "gắn kết/ngắt gắn kết cơ sở dữ liệu"')
print(f'[đối chiếu] Import: đồng bộ viết hoa "Import" và khớp câu song sinh')
print(f'[đối chiếu] Copy: viết thường "màu" và "file"')
print()
for k, v in changed.items():
    print(f'  {k[:44]!r}')
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
