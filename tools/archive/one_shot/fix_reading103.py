#!/usr/bin/env python3
r"""Vòng 103: 74 chuỗi, #1047-1120. Đọc tuần tự, không lọc.

Bốn lỗi, đều là **giữ số nhiều tiếng Anh** trong khi cả nhóm bỏ. Tiếng Việt
không có số nhiều, và hai nhóm đều đã bỏ ở hàng chục chỗ.

1. `Auto Crossfades` -> `Crossfades tự động`

   Nhóm Crossfade có **27** chuỗi, đúng **1** giữ số nhiều — chỉ có chỗ này:
   `Audition Crossfade`, `Crossfade`, `Crossfade Editor`, `Create Crossfade...`,
   `Move Crossfade`, `Post-Crossfade`, `Pre-Crossfade`, `Symmetric Crossfade`...
   đều số ít. Sửa theo `Auto Fades` -> `Fade tự động` ngay cạnh.

2. `Automatic Voicings` -> `Voicings tự động`
3. `Update Voicings`      -> `Cập nhật Voicings`
4. `Voicings`             -> `Voicings`

   Nhóm Voicing có **35** giá trị dùng "Voicing" số ít, **3** giá trị giữ
   "Voicings" — và ba cái đó chính là ba chỗ này. Đợt 94 đã sửa
   `Adaptive Voicings` -> `Adaptive Voicing` đúng theo luật này; nay dọn nốt
   ba chỗ còn lại của cùng một gia đình.

**Không sửa, đã kiểm:** cụm `Auto X` có cả hai kiểu song song —
`Auto Fade In` -> `Auto Fade In` (giữ trọn), `Auto Join` -> `Auto Join`,
`Auto Punch` -> `Auto Punch`, nhưng `Auto Fades` -> `Fade tự động`,
`Auto Zoom` -> `Zoom tự động`, `Auto LFO` -> `LFO tự động`. Đây là các nhãn
menu ở hộp thoại khác nhau; bảng không cho biết cái nào ở đâu, nên không có
cách biết quy ước nào đúng. `Automatically Resolve Collisions...` ->
`Tự xử lý chồng lấn...` khác `Tự động` ở nhóm kia là vì động từ khác
(`Resolve` = "xử lý", `Adjust` = "chỉnh"), không phải lệch quy tắc.

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
    'Auto Crossfades': 'Crossfade tự động',
    'Automatic Voicings': 'Voicing tự động',
    'Update Voicings': 'Cập nhật Voicing',
    'Voicings': 'Voicing',
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
    # chinh cau hoi cua vong nay: khong con so nhieu tieng Anh
    if re.search(r'\b(Crossfades|Voicings)\b', v):
        problems.append(f'con so nhieu: {k[:40]!r} -> {v!r}')

# 1. Phe so it cua nhom Crossfade phai ton tai (>= 20 chuoi)
cf = [k for k in vi if re.search(r'\bCrossfade', k, re.I)]
if len(cf) < 20:
    problems.append(f'gia dinh Crossfade chi {len(cf)} chuoi - mong doi >= 20')
if sum(1 for k in cf if 'Crossfades' not in vi[k]) < 20:
    problems.append('khong du anh em so it trong nhom Crossfade')

# 2-4. Phe da bo so nhieu cua nhom Voicing phai lon hon phe giu TRUOC khi sua
vo = [k for k in vi if re.search(r'\bVoicing', k, re.I)]
if len(vo) < 30:
    problems.append(f'gia dinh Voicing chi {len(vo)} chuoi - mong doi >= 30')
n_sg = sum(1 for k in vo if 'Voicing' in vi[k] and 'Voicings' not in vi[k])
n_pl = sum(1 for k in vo if 'Voicings' in vi[k])
if n_sg < 25:
    problems.append(f'chi {n_sg} gia tri so it truoc khi sua - khong du bang '
                    'chung de chon')
if n_pl != 3:
    problems.append(f'truoc khi sua co {n_pl} gia tri giu so nhieu, '
                    'vong nay sua 3 - so lieu khong khop')

# ANH EM: dong ca phe giu, phai ton tai nguyen
SIBLINGS = [
    ('Adaptive Voicings', 'Adaptive Voicing'),   # vong 94 - cung gia dinh
    ('Activate remote control for Voicings, Tensions and Transpose', 'Voicing'),
    ('Custom Voicing', 'Voicing tùy chỉnh'),
    ('Chord Pads - Next Voicing', 'Voicing kế tiếp'),
    ('Auto Fades', 'Fade tự động'),              # 1: mau cau truc
    ('Crossfade', 'Crossfade'),
    ('Audition Crossfade', 'Crossfade'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)
left_cf = [k for k, v in after.items() if re.search(r'\bCrossfades\b', v)]
if left_cf:
    problems.append(f'con "Crossfades": {left_cf}')
left_vo = [k for k, v in after.items() if re.search(r'\bVoicings\b', v)]
if left_vo:
    problems.append(f'con "Voicings": {left_vo}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] Crossfade: {len(cf)} chuoi, het so nhieu')
n_sg_after = sum(1 for k in vo if 'Voicing' in after[k]
                and 'Voicings' not in after[k])
assert n_sg_after == len(vo), 'so luong phep thu khong cong'
print(f'[doi chieu] Voicing: {len(vo)} chuoi, {n_sg_after} so it / '
      f'{len(vo) - n_sg_after} so nhieu (truoc: {n_sg}/{n_pl})')
print()
for k, v in changed.items():
    print(f'  {k[:34]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
