#!/usr/bin/env python3
r"""Vòng 94: 72 chuỗi, #373-444. Đọc tuần tự, không lọc.

Ba lỗi.

1. `Activated Marker Track: %s` -> `Đã kích hoạt Marker Track: %s`
2. `Activated: %s`              -> `Đã kích hoạt: %s`

   Nhóm `Activated:` có bốn thành viên và đang **hai kiểu**:

       Activated Marker Track: %s          -> Đã **kích hoạt**
       Activated: %s                       -> Đã **kích hoạt**
       Activated: Cycle follows when ...   -> Đã **bật**
       Deactivated: %s                     -> Đã **tắt**
       Deactivated: Cycle follows when ... -> Đã **tắt**

   Cặp `Cycle follows` khớp nhau, và khớp với `Activate` -> `Bật` mà vòng 93
   vừa sửa. Hai chuỗi kia là thành viên lạc.

3. `Adaptive Voicings` -> `Adaptive Voicings`

   Giữ nguyên số nhiều tiếng Anh, trong khi anh em đã bỏ:
   `Voicings, Tensions and Transposes` -> `Voicing, Tension và Transpose`.
   Cùng một mục, hai cách.

**Nghi sai một lần nữa, ghi lại để không lặp.** `Send 'Still' instead of
'Stop'` dịch `'Stop'` thành `'Dừng'` còn `'Still'` giữ tiếng Anh - trông như
lệch, nhưng tôi tưởng hai chuỗi trong nhóm RS422 không thống nhất. Tra ra thì
**cả hai đều giống nhau**:

    Send 'Still' instead of 'Stop'                 -> Gửi 'Still' thay cho 'Dừng'
    Activate this to send a 'Still' command ...    -> Bật để gửi 'Still' thay vì 'Dừng'

Không sửa. Có thể đáng bàn (đây là tên lệnh giao thức, thiết bị nhận đúng
chữ "Stop"), nhưng hai chuỗi **đã thống nhất với nhau**, nên đó là lựa chọn
chứ không phải lỗi. Đổi cả hai là một vòng riêng, không gộp vào đây.

  python tools/fix_reading94.py
  python tools/fix_reading94.py --write
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
    'Activated Marker Track: %s': 'Đã bật Marker Track: %s',
    'Activated: %s': 'Đã bật: %s',
    'Adaptive Voicings': 'Adaptive Voicing',
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
    if v.rstrip().endswith(':') and not src[k].rstrip().endswith(':'):
        problems.append(f'thêm dấu hai chấm không có trong nguồn: {k[:46]!r}')

SIBLINGS = [
    ('Activate', 'Bật'),                                # vòng 93
    ('Deactivated: %s', 'Đã tắt'),                      # cặp đối xứng
    ('Deactivated: Cycle follows when locating to Markers', 'Đã tắt'),
    ('Activated: Cycle follows when locating to Markers', 'Đã bật'),
    ('Activate remote control for Voicings, Tensions and Transpose',
     'Voicing, Tension'),                             # 3
    ('Adaptive Voicing', 'Adaptive Voicing'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy {k!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k!r} không chứa {must!r}')

# Sau khi sửa, nhóm "Activated:"/"Deactivated:" phải chỉ còn Đã bật/Đã tắt.
after = dict(vi)
after.update(real)
for k, v in after.items():
    if k.startswith(('Activated', 'Deactivated')) and 'kích hoạt' in v:
        problems.append(f'còn sót "kích hoạt" trong nhóm: {k[:44]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:40]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
