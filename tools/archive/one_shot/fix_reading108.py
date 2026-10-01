#!/usr/bin/env python3
r"""Vòng 108: 60 chuỗi, #1401-1460. Đọc tuần tự, không lọc.

Một lỗi: `CCMode: Reset All Controllers` -> `CCMode: Reset All Controller`

`CCMode:` là **tên lệnh MIDI theo đặc tả**, không phải văn xuôi:

    CCMode: All Notes Off          -> giữ nguyên
    CCMode: All Sound Off          -> giữ nguyên
    CCMode: MONO                   -> giữ nguyên
    CCMode: OMNI Off / OMNI On     -> giữ nguyên
    CCMode: POLY                   -> giữ nguyên
    CCMode: Reset All Controllers  -> bỏ chữ "s"   <- lạc

Sáu anh em giữ nguyên, một cái bị bỏ số nhiều. "Reset All Controllers" là
CC 121 trong đặc tả MIDI — tên của một lệnh, nên phải giữ **nguyên văn**. Và
đây cũng là nghịch lý thật của quy tắc "bỏ số nhiều": bỏ số nhiều đúng cho
`Hitpoints` (50 chuỗi, không chuỗi nào giữ "Hitpoints") nhưng **sai** ở đây,
vì đây là danh từ riêng của một lệnh.

Cùng cơ đó, `Hitpoint` đã đúng: 50 chuỗi, **0** giữ số nhiều — kể cả khi nguồn
là `Create Markers from Hitpoints` -> `Tạo Marker từ các Hitpoint` (bỏ "s", thêm
"các"), và `Edit Hitpoints` -> `Sửa các Hitpoint`. Nên `Hitpoint` là tiếng Việt
đã bỏ số nhiều đúng quy tắc.

**Không sửa, đã kiểm:** `CC: Breath` -> `CC: Breath` và `CC: Foot` -> `CC: Foot`
là chính hai chỗ đợt 107 vừa bỏ chữ "Controller" thừa. Nay nhìn lại thấy chỗ
này **giữ số nhiều** đúng: `CC: Breath` là *tên chức năng điều khiển* (CC 2 =
Breath Controller trong đặc tả), nên giữ nguyên, không bỏ s. Đợt 107 chỉ xóa
chữ thêm, không đụng tới số nhiều — và đó là đúng. Ghi lại để không ai đọc
nhầm là đợt 107 bỏ số nhiều.

Cùng lý do đó, `Type of New Controller Events: Toggle Step/Ramp` ->
`Loại Event Controller mới: Bật/tắt Step/Ramp` là đúng: "Controller Events" ở
đây là danh từ ghép, không phải "Controller" + số nhiều.

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
    'CCMode: Reset All Controllers': 'CCMode: Reset All Controllers',
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
    if v[7:].strip() != k[7:].strip():
        problems.append(f'phan sau "CCMode:" khac nguon: {k!r} -> {v!r}')

# MOI chuoi "CCMode:" deu phai giu nguyen - day la ten lenh MIDI
ccmode = {k: vi[k] for k in vi if k.startswith('CCMode')}
if len(ccmode) != 7:
    problems.append(f'gia dinh "CCMode:" co {len(ccmode)} chuoi, mong doi 7')
for k, v in ccmode.items():
    if k in real:
        continue
    if v[7:].strip() != k[7:].strip():
        problems.append(f'anh em khong giu nguyen: {k!r} -> {v!r}')

# "Hitpoint" phai bo so nhieu o 50 chuoi - KHONG duoc sua
hp = [k for k in vi if re.search(r'Hitpoints?\b', k, re.I)]
if len(hp) < 45:
    problems.append(f'gia dinh Hitpoint chi {len(hp)} chuoi - mong doi >= 45')
n_hp_pl = sum(1 for k in hp if re.search(r'\bHitpoints\b', vi[k]))
if n_hp_pl:
    problems.append(f'Hitpoint con giu so nhieu o {n_hp_pl} chuoi: '
                    f'{[k for k in hp if re.search(chr(92)+"bHitpoints" + chr(92)+"b", vi[k])][:4]}')

# Dong 107: "CC: Breath"/"CC: Foot" giu so nhieu la DUNG (ten chuc nang MIDI).
for k, must in [('CC: Breath', 'CC: Breath'), ('CC: Foot', 'CC: Foot'),
                ('CC: Breath LSB', 'CC: Breath LSB')]:
    if vi.get(k) != must:
        problems.append(f'ket qua dong 107 bi bao loi: {k!r} -> {vi.get(k)!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] "CCMode:": {len(ccmode)} chuoi, 7/7 giu nguyen')
print(f'[doi chieu] Hitpoint: {len(hp)} chuoi, 0 giu so nhieu (khong sua)')
print()
for k, v in changed.items():
    print(f'  {k!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
