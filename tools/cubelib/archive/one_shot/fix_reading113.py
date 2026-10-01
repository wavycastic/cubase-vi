#!/usr/bin/env python3
r"""Vòng 113: 130 chuỗi, #1801-1930. Đọc tuần tự, không lọc.

Tám lỗi thuộc bốn nhóm rõ rệt:

1. Trùng lặp làm mất phân biệt "Connected" vs "Linked":
   - `Combine Automation of VCA and Connected Channels`
       -> `Gộp Automation của VCA và Channel **đã kết nối**` (trước: `đã nối`)
   - `Combine Automation of VCA and Linked Channels`
       -> `Gộp Automation của VCA và Channel **đã liên kết**` (trước: `đã nối`)
   Trong Cubase, VCA fader có thể điều khiển channel qua kết nối VCA ("Connected")
   hoặc qua nhóm liên kết ("Linked"). Bản dịch cũ dịch cả hai giống hệt nhau
   thành "Channel đã nối", làm người dùng không thể phân biệt hai chức năng.
   Khôi phục đúng thuật ngữ theo `Connected` -> `Đã kết nối` và `Linked` -> `Đã liên kết`.

2. Bỏ sót tiếng Anh trong nhóm `Commit` (Xác nhận):
   - `Commit Failed.`     -> `Không thể xác nhận.` (trước: `Không thể Commit.`)
   - `Nothing to commit.` -> `Không có gì để xác nhận.` (trước: `Không có gì để commit.`)
   Toàn bộ đường tín hiệu` (trước: `... đường truyền tín hiệu`)
   Ba tùy chọn đi cùng đ��u dùng "Toàn bộ đường tín hiệu":
       `Complete Signal Path + Master Effects`
           -> `Toàn bộ đường tín hiệu + Master Effect`
       `Complete Signal Path Including Groups and Sends`
           -> `Toàn bộ đường tín hiệu gồm Group và Send`
       `Complete Signal Path Including Groups and Sends, and Master FX`
           -> `Toàn bộ đường tín hiệu gồm Group, Send và Master FX`
   Bỏ chữ "truyền" thừa ở tùy chọn đầu tiên để 4 nút chọn đồng nhất 100%.

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
    'Combine Automation of VCA and Connected Channels':
        'Gộp Automation của VCA và Channel đã kết nối',
    'Combine Automation of VCA and Linked Channels':
        'Gộp Automation của VCA và Channel đã liên kết',
    'Commit Failed.':
        'Không thể xác nhận.',
    'Nothing to commit.':
        'Không có gì để xác nhận.',
    'Command Categories':
        'Danh mục lệnh',
    'Open Command Destination':
        'Mở nơi nhận của lệnh',
    'Remove Command from Macro':
        'Gỡ bỏ lệnh khỏi Macro',
    'Complete Signal Path':
        'Toàn bộ đường tín hiệu',
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
    # 1. Connected vs Linked
    ('Connected', 'Đã kết nối'),
    ('Linked', 'Đã liên kết'),
    ('Channel is Linked in Group %d', 'Channel đã liên kết trong Group %d'),
    # 2. Commit -> Xác nhận
    ('Commit', 'Xác nhận'),
    ('Commit Changes', 'Xác nhận thay đổi'),
    ('Commit changes on this track', 'Xác nhận các thay đổi trên Track này'),
    # 3. Macro commands viết thường
    ('Add Command to Macro', 'Thêm lệnh vào Macro'),
    ('Move Command Down in Macro', 'Chuyển lệnh xuống trong Macro'),
    ('Template Category', 'Danh mục mẫu'),
    # 4. Signal Path options
    ('Complete Signal Path + Master Effects', 'Toàn bộ đường tín hiệu + Master Effect'),
    ('Complete Signal Path Including Groups and Sends', 'Toàn bộ đường tín hiệu gồm Group và Send'),
    ('Complete Signal Path Including Groups and Sends, and Master FX', 'Toàn bộ đường tín hiệu gồm Group, Send và Master FX'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Connected Channels và Linked Channels phải khác nhau
if after['Combine Automation of VCA and Connected Channels'] == after['Combine Automation of VCA and Linked Channels']:
    problems.append('Connected va Linked van bi trung nhau')

# 2. Toàn bộ nhóm Commit không còn từ tiếng Anh "commit"
commit_en = [k for k, v in after.items() if re.search(r'\bcommit\b', v, re.I)]
if commit_en:
    problems.append(f'van con tu commit tieng Anh: {commit_en}')

# 3. Không còn chữ "Lệnh" viết hoa giữa câu trong toàn bộ bản dịch
mid_lenh = [k for k, v in after.items() if re.search(r'\S\s+Lệnh\b', v)]
if mid_lenh:
    problems.append(f'van con chu Lenh viet hoa giua cau: {mid_lenh}')

# 4. Cả 4 tùy chọn Complete Signal Path đều bắt đầu bằng "Toàn bộ đường tín hiệu"
for k in ('Complete Signal Path',
          'Complete Signal Path + Master Effects',
          'Complete Signal Path Including Groups and Sends',
          'Complete Signal Path Including Groups and Sends, and Master FX'):
    if not after[k].startswith('Toàn bộ đường tín hiệu'):
        problems.append(f'Signal path khong dong nhat: {k!r} -> {after[k]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Connected ("đã kết nối") vs Linked ("đã liên kết"): phân biệt rõ')
print(f'[đối chiếu] Commit: 5/5 chuỗi đều dùng "xác nhận", sạch tiếng Anh')
print(f'[đối chiếu] Danh mục / Macro: 0 chữ "Lệnh" viết hoa giữa câu')
print(f'[đối chiếu] Complete Signal Path: 4/4 tùy chọn Export đồng nhất')
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
