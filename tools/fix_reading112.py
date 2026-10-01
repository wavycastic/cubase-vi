#!/usr/bin/env python3
r"""Vòng 112: 75 chuỗi, #1726-1800. Đọc tuần tự, không lọc.

Hai lỗi, cùng thuộc nhóm gợi ý/hành động `Click to Bypass ...`:

    Click to Bypass Channel Strip  -> `Nhấp để Bypass Channel Strip`
    Click to Bypass Cue Sends      -> `Nhấp để Bypass **Cue Send**`      (bỏ số nhiều)
    Click to Bypass Equalizers     -> `Nhấp để Bypass **Equalizer**`     (bỏ số nhiều)
    Click to Bypass Inserts        -> `Nhấp để Bypass **Inserts**`       <- còn 's'
    Click to Bypass Sends          -> `Nhấp để Bypass **Sends**`         <- còn 's'

Toàn bộ nhóm gợi ý `Click to Bypass ...` có đúng 5 chuỗi. Hai chuỗi đầu
(`Cue Sends` và `Equalizers`) đã bỏ số nhiều theo đúng quy ước tiếng Việt và
đợt 106; riêng hai chuỗi `Inserts` và `Sends` bị sót chữ 's'.

Đợt 106 đã chứng minh rõ: nhãn bảng/tiêu đề giữ số nhiều (`Inserts`, `Sends`),
còn câu lệnh/hành động/trạng thái thì bỏ số nhiều:
    `Bypass: Inserts` -> `Bypass: Insert`
    `Bypass: Sends`   -> `Bypass: Send`
    `Inserts Bypass`  -> `Bypass Insert`
    `Sends Bypass`    -> `Bypass Send`
Vì vậy trong `Click to Bypass ...` (hành động: "Nhấp để Bypass..."), hai chuỗi
này phải bỏ số nhiều thành `Nhấp để Bypass Insert` và `Nhấp để Bypass Send`.

**Không sửa, đã kiểm:**
- `Click to Select Click Sound File` -> `Nhấp để chọn File âm thanh Click`:
  bản dịch phân biệt cực kỳ chính xác giữa động từ nhấp chuột ("Nhấp") và
  tiếng gõ phách Metronome ("Click") trong cùng một câu.
- Nhóm `Clear ...` gồm 18 chuỗi đều dùng `Xóa ...` hoàn toàn nhất quán.
- `Clef` / `Clefs` -> `Khóa nhạc` nhất quán.

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
    'Click to Bypass Inserts': 'Nhấp để Bypass Insert',
    'Click to Bypass Sends': 'Nhấp để Bypass Send',
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
    if re.search(r'\b(Inserts|Sends)\b', v):
        problems.append(f'con so nhieu: {k!r} -> {v!r}')

# Anh em cùng nhóm Click to Bypass
SIBLINGS = [
    ('Click to Bypass Channel Strip', 'Nhấp để Bypass Channel Strip'),
    ('Click to Bypass Cue Sends', 'Nhấp để Bypass Cue Send'),
    ('Click to Bypass Equalizers', 'Nhấp để Bypass Equalizer'),
    ('Bypass Inserts', 'Bypass Insert'),
    ('Bypass Sends', 'Bypass Send'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# Toàn bộ nhóm 5 chuỗi Click to Bypass không còn số nhiều tiếng Anh
cb = [k for k in after if k.startswith('Click to Bypass')]
if len(cb) != 5:
    problems.append(f'nhom Click to Bypass co {len(cb)} chuoi, mong doi 5')
for k in cb:
    if re.search(r'\b(Inserts|Sends|Equalizers|Sends)\b', after[k]):
        problems.append(f'Click to Bypass van con so nhieu: {k!r} -> {after[k]!r}')

# Nhãn bảng giữ số nhiều phải còn nguyên
if after.get('Inserts') != 'Inserts':
    problems.append('nhan bang Inserts bi dong')
if after.get('Sends') != 'Sends':
    problems.append('nhan bang Sends bi dong')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Click to Bypass: 5/5 chuỗi đều dùng danh từ số ít')
print(f'[đối chiếu] nhãn bảng "Inserts", "Sends" vẫn giữ nguyên')
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
        with open(path, 'w', encoding='utf-8', newline='') as fh:\
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
print(f'\nđã ghi {n} thay đổi vào batches')
