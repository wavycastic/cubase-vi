#!/usr/bin/env python3
r"""Vòng 122: 80 chuỗi, #2671-2750. Đọc tuần tự, không lọc.

Bốn lỗi thuộc bốn nhóm được phát hiện và sửa đồng bộ:

1. Bổ sung từ "bỏ" bị sót trong câu hỏi gỡ vùng:
   - `Do you really want to remove the insert effect bank zone (%s)?`
       -> `B��n có thực sự muốn gỡ bỏ Insert Effect Bank Zone (%s) không?`
       (trước: `... muốn gỡ Insert Effect...`)
   Toàn bộ 11 chuỗi `Do you really want to remove ...` khác đều dùng `muốn gỡ bỏ`:
       `Do you really want to remove the mixer bank zone (%s)?`
           -> `Bạn có thực sự muốn gỡ bỏ Mixer Bank Zone (%s) không?`
       `Do you really want to remove the device?`
           -> `Bạn có thực sự muốn gỡ bỏ thiết bị này không?`
       `Do you really want to remove the layout?`
           -> `Bạn có thực sự muốn gỡ bỏ Layout này không?`

2. Chuẩn hóa thuật ngữ "Bật Project" (thay vì "kích hoạt Project"):
   - `Do you want to activate the project?`
       -> `Bạn có muốn bật Project này không?`
       (trước: `... kích hoạt Project này...`)
   - Khớp 100% với lệnh menu: `Activate Project` -> `Bật Project`
   - Khớp với trạng thái: `Colors can't be changed for inactive Projects` -> `Project chưa bật...`
   - Tránh gây hiểu nhầm sang kích hoạt bản quyền phần mềm (License Activation).

3. Viết hoa chuẩn Title Case thuật ngữ mở rộng `Video` (AGENT.md §1):
   - `Do you want to copy video files too?`
       -> `Bạn có muốn sao chép cả file Video không?`
       (trước: `... file video...`)
   Duy nhất 1 chuỗi này viết thường `file video`. Tất cả các chuỗi khác đều viết hoa `Video`.

4. Bổ sung chủ ngữ "Bạn có muốn" bị rụng:
   - `Do you want to reset the record folder of the selected tracks to the project directory?`
       -> `Bạn có muốn đặt lại thư mục ghi của Track đã chọn về thư mục Project không?`
       (trước: `Đặt lại thư mục ghi của Track đã chọn...`)
   Trong nhóm 38 câu hỏi bắt đầu bằng `Do you want to ...`, 37 câu đều bắt đầu
   bằng `Bạn có muốn ... không?`. Duy nhất câu này bị rụng mất cụm từ mở đầu.

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
    'Do you really want to remove the insert effect bank zone (%s)?':
        'Bạn có thực sự muốn gỡ bỏ Insert Effect Bank Zone (%s) không?',
    'Do you want to activate the project?':
        'Bạn có muốn bật Project này không?',
    'Do you want to copy video files too?':
        'Bạn có muốn sao chép cả file Video không?',
    'Do you want to reset the record folder of the selected tracks to the project directory?':
        'Bạn có muốn đặt lại thư mục ghi của Track đã chọn về thư mục Project không?',
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
        problems.append(f'missing %s placeholder in {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

SIBLINGS = [
    # 1. Do you really want to remove ...
    ('Do you really want to remove the mixer bank zone (%s)?',
     'Bạn có thực sự muốn gỡ bỏ Mixer Bank Zone (%s) không?'),
    ('Do you really want to remove the device?',
     'Bạn có thực sự muốn gỡ bỏ thiết bị này không?'),
    ('Do you really want to remove the layout?',
     'Bạn có thực sự muốn gỡ bỏ Layout này không?'),
    # 2. Activate Project
    ('Activate Project', 'Bật Project'),
    ("Colors can't be changed for inactive Projects", 'Project chưa bật không đổi được màu'),
    # 3. file Video
    ('Copies of the selected video files with replaced audio are created.',
     'file Video'),
    # 4. Do you want to ...
    ('Do you want to clear all key commands?', 'Bạn có muốn xóa tất cả phím tắt không?'),
    ('Do you want to reset all key commands?', 'Bạn có muốn đặt lại tất cả phím tắt không?'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Toàn bộ nhóm Do you really want to remove the ... bank zone đều có "gỡ bỏ"
for k in ('Do you really want to remove the insert effect bank zone (%s)?',
          'Do you really want to remove the mixer bank zone (%s)?'):
    if 'muốn gỡ bỏ' not in after[k]:
        problems.append(f'{k!r} thieu "muốn gỡ bỏ": {after[k]!r}')

# 2. Do you want to activate the project dùng "bật Project"
if 'bật Project' not in after['Do you want to activate the project?']:
    problems.append(f'Do you want to activate the project khong co "bật Project": {after["Do you want to activate the project?"]!r}')

# 3. Do you want to copy video files too không còn "file video" viết thường
if re.search(r'\bfile video\b', after['Do you want to copy video files too?']):
    problems.append('Do you want to copy video files too van con "file video" thuong')

# 4. Do you want to reset the record folder bắt đầu bằng "Bạn có muốn"
if not after['Do you want to reset the record folder of the selected tracks to the project directory?'].startswith('Bạn có muốn'):
    problems.append('Do you want to reset the record folder thieu "Bạn có muốn"')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Bank zone: 2/2 chuỗi đều có "muốn gỡ bỏ"')
print(f'[đối chiếu] Bật Project: đồng bộ với "Activate Project" và "Project chưa bật"')
print(f'[đối chiếu] Video: 100% viết hoa "file Video" theo AGENT.md §1')
print(f'[đối chiếu] Do you want to: 38/38 chuỗi đều bắt đầu bằng "Bạn có muốn"')
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
