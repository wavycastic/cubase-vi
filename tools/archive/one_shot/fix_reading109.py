#!/usr/bin/env python3
r"""Vòng 109: 60 chuỗi, #1461-1520. Đọc tuần tự, không lọc.

Một lỗi, mà lỗi này chỉ thấy được khi đặt 10 chuỗi cạnh nhau — mỗi cái đọt
riêng đều **đúng**.

Nói "đã đạt giới hạn" mà không nói *cái gì* đã đạt giới hạn thì câu bị cụt. Và
trong nhóm `Cannot add more tracks...` có **mười** chuỗi, chín đúng **một** sai:

    ... The MIDI track count is at the limit.
        -> `... **Số** MIDI Track đã đạt giới hạn.`      CO
    ... The VCA track count ...
        -> `... **Số** VCA Track đã đạt giới hạn.`       CO
    ... The audio track count ...
        -> `... **Số** Audio Track đã đạt giới hạn.`     CO
    ... The chord track count ...
        -> `... Chord Track đã đạt giới hạn.`             <- THIEU "So"
    ... The effect / group / instrument / marker /
        video track count ...
        -> `... **Số** ... Track đã đạt giới hạn.`       CO
    ... The track count for this track type ...
        -> `... **Số** Track loại này đã đạt giới hạn.`  CO

Mẫu chung là `Số <loại> Track`, và chỉ `chord` rơi khỏi mẫu. Chữ "Số" là danh
từ đếm, mà động từ "đã đạt" cần chủ ngữ — `Chord Track đã đạt giới hạn` đọc
như bản dịch sơ sài, còn chín cái kia đọc như câu hoàn chỉnh.

Đây là lớp lỗi mà §8.10 nói rõ: **đọc tay là bước cuối**. Một bộ dò tên nhóm
sẽ không bắt được nó, vì `Cannot add more tracks. The chord track count is at
the limit.` và bản dịch của nó đều không sai *cấu trúc* — chỉ thiếu một từ mà
chín cái anh em đều có.

**Không sửa, đã kiểm:** nhóm `Center` chia hai cách nhưng chia theo nghĩa, và
cách chia đúng:
    nút bấm / vị trí -> `Center` -> `Giữa`, `Center (64)` -> `Giữa (64)`
    tham số stereo    -> `Center Width` -> `Độ rộng trung tâm`
    **tên bảng bên cạnh** -> `Center Neutral` -> `Center Neutral`,
        `Center channel` -> `Center Channel`
Cái sau giữ tiếng Anh vì là nhãn trong bảng. `Center L/R channels` ->
`Căn giữa Channel Trái/Phải` là động từ (`Căn`), khác hẳn. `Catch` giữ nguyên
cả 6 chuỗi — nhất quán.

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
    'Cannot add more tracks. The chord track count is at the limit.':
        'Không thêm được Track. Số Chord Track đã đạt giới hạn.',
}

# ------------------------------------------------------------------ tu kiem
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
    # 1. ve sau dau cham phai bat dau bang danh tu dem
    if not re.search(r'\. Số \S+ Track', v):
        problems.append(f'thieu danh tu dem "So": {k[:40]!r} -> {v!r}')

# MUOI chuoi trong nhom: sau khi sua, KHONG con ve nao thieu "So"
fam = [k for k in vi if k.startswith('Cannot add more tracks')]
if len(fam) != 10:
    problems.append(f'gia dinh "Cannot add more tracks" co {len(fam)} chuoi, '
                    'mong doi 10')
for k in fam:
    v = (dict(vi, **real)).get(k)
    if '. ' not in v:
        problems.append(f'khong tach duoc ve sau dau cham: {k[:40]!r}')
        continue
    tail = v.split('. ', 1)[1]
    if not tail.startswith('Số '):
        problems.append(f've sau van thieu "So": {k[:44]!r} -> {tail[:40]!r}')

# Anh em: 9 cai da dung, phai con nguyen
SIBLINGS = [
    'Cannot add more tracks. The MIDI track count is at the limit.',
    'Cannot add more tracks. The VCA track count is at the limit.',
    'Cannot add more tracks. The audio track count is at the limit.',
    'Cannot add more tracks. The effect track count is at the limit.',
    'Cannot add more tracks. The group track count is at the limit.',
    'Cannot add more tracks. The instrument track count is at the limit.',
    'Cannot add more tracks. The marker track count is at the limit.',
    'Cannot add more tracks. The video track count is at the limit.',
    'Cannot add more tracks. The track count for this track type is at the limit.',
]
for k in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:56]!r}')
    elif not vi[k].split('. ', 1)[-1].startswith('Số '):
        problems.append(f'anh em da khac: {k[:44]!r} -> {vi[k][-40:]!r}')

# Nhom "Center" phai giu nguyen phan "Center Channel" / "Center Neutral"
for k, must in [('Center channel', 'Center Channel'),
                ('Center Neutral', 'Center Neutral'),
                ('Center', 'Giữa'), ('Center (64)', 'Giữa (64)')]:
    if k not in vi:
        problems.append(f'khong thay {k!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k!r} khong chua {must!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] "Cannot add more tracks": {len(fam)} chuoi, '
      've sau deu bat dau bang "So"')
print()
for k, v in changed.items():
    print(f'  {k[:56]!r}')
    print(f'      {vi.get(k, "")!r}')
    print(f'   -> {v!r}')

if not WRITE:
    print('\n(chay thu - them --write de ghi)')
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
print(f'\nda ghi {n} thay doi vao batches')
