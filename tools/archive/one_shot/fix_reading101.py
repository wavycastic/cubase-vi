#!/usr/bin/env python3
r"""Vòng 101: 74 chuỗi, #899-972. Đọc tuần tự, không lọc.

Ba lỗi, một gia đình: `Articulations` — **giữ số nhiều tiếng Anh** trong khi
cả nhóm bỏ.

    Articulations                          -> **Articulations**           <- lạc
    Articulations in Group                 -> **Articulations** trong Group  <- lạc
    Custom Articulations                   -> **Articulations** tùy chỉnh <- lạc

so với 22 chuỗi còn lại đã bỏ:

    Expression Map: Articulations        -> Expression Map: **Articulation**
    Select one or multiple Articulations -> Chọn một hoặc nhiều **Articulation**
    Articulations & Mutual Exclusion Group-> **Articulation** & nhóm loại trừ lẫn nhau
    Convert MIDI to Articulations        -> Chuyển đổi MIDI sang **Articulation**
    Jazz Articulations                   -> **Articulation** kiểu Jazz
    Add Custom Articulation              -> Thêm **Articulation** tùy chỉnh

Riêng cặp cuối đáng chú ý: `Add Custom Articulation` (số ít) đã bỏ, còn
`Custom Articulations` (số nhiều) thì giữ — **cùng một cụm, hai cách**, và
cái sai nằm ở bản số nhiều.

Đây **không phải** kiểu 51/49 như cụm `Filter` ở đợt 96 (17/32, đã bỏ qua).
22 đứng 3 là áp đảo, và khoá trần `Articulation` -> `Articulation` đã chốt
dạng số ít của thuật ngữ.

**Không sửa, đã kiểm:** cụm `Arm` / `Record Enable` **đang tách hai khái niệm
Steinberg**, và cách tách đó hợp lý:
    `Arm`             -> **sẵn sàng ghi**   (`Arm All Tracks` -> `Bật sẵn sàng
                                              ghi tất cả Track`,
                                              `Test Record Arming` -> `Kiểm tra
                                              sẵn sàng ghi âm`)
    `Record Enable`   -> **ghi**            (`Record Enable On/Off` -> `Bật/Tắt
                                              ghi`, `Record Enable/Monitor` ->
                                              `Bật ghi/Monitor`)
`Activate Record Enable for All Audio Tracks` trộn hai cách, nhưng bảng chỉ
có một chuỗi kiểu đó và không có cách nào chứng minh nên chọn, nên để.
`Assign selected map to active track` có **hai** khoá chỉ khác dòng cuối, và
hai giá trị cũng khác đúng dòng đó — kiểm rồi, không lỗi.

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
    'Articulations': 'Articulation',
    'Articulations in Group': 'Articulation trong Group',
    'Custom Articulations': 'Articulation tùy chỉnh',
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

SIBLINGS = [
    ('Articulation', 'Articulation'),                      # khoa tran: so it
    ('Add Custom Articulation', 'Articulation tùy chỉnh'),  # cặp sat nhanh
    ('Expression Map: Articulations', 'Articulation'),
    ('Select one or multiple Articulations', 'Articulation'),
    ('Articulations & Mutual Exclusion Groups', 'Articulation'),
    ('Convert MIDI to Articulations', 'Articulation'),
    ('Jazz Articulations', 'Articulation'),
    ('Articulation Combinations', 'Tổ hợp Articulation'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

# Sau khi sua, KHONG con gia tri nao giu "Articulations" (so nhieu tieng Anh).
# Chu khong duoc dung trong gia tri - "Articulations" chi duoc phep trong KHOA.
after = dict(vi)
after.update(real)
left = {k: v for k, v in after.items() if 'Articulations' in v}
if left:
    problems.append(f'van con giu so nhieu trong gia tri: {left}')

# Chong pho thu chay rong: gia dinh phai lon, va phai co it nhat 20 gia tri
# dang bo so nhieu truoc khi sua - neu khong con thi pho thu vo nghia.
fam = [k for k in vi if re.search(r'Articulation', k, re.I)]
if len(fam) < 20:
    problems.append(f'gia dinh Articulation chi {len(fam)} chuoi - mong doi >= 20')
n_drop = sum(1 for k in fam if 'Articulations' not in vi[k])
if n_drop < 15:
    problems.append(f'chi thay {n_drop} gia tri bo so nhieu truoc khi sua - '
                    'khong du bang chung de chon')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] gia dinh Articulation: {len(fam)} chuoi, '
      f'{n_drop + len(changed)} bo so nhieu, 0 giu so nhieu')
print()
for k, v in changed.items():
    print(f'  {k[:36]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
