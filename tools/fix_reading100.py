#!/usr/bin/env python3
r"""Vòng 100: 72 chuỗi, #827-898. Đọc tuần tự, không lọc.

Bốn lỗi, tất cả là **đảo trật tự cụm `Logical Preset`**.

**Quy ước nhà, đã tra và thấy cố ý — phải nắm trước khi sửa.** Có hai kiểu:

    X **Presets** (số nhiều, nghĩa "tập hợp")  ->  **Preset** X
        Mixer Presets      -> Preset của Mixer
        Strip Presets      -> Preset của Strip
        Downmix Presets    -> Preset Downmix
        Track Presets      -> Preset Track

    X **Preset** (số ít, là *thuật ngữ*)       ->  X **Preset** (giữ nguyên)
        Logical Preset     -> Logical Preset
        Algorithm Preset   -> Algorithm Preset
        Encoder Preset     -> Encoder Preset

Vì vậy `Apply Crossfade Preset` -> `Áp dụng Preset Crossfade` **đúng**, đúng
theo cái thứ nhất (`Default Preset` -> `Preset mặc định`, `New Preset` ->
`Preset mới` cũng vậy). Tôi định sửa nó, tra thêm thì thấy mình sai — ghi ở
đây để lần sau khỏi lặp.

Với **thuật ngữ `Logical Preset` riêng**, số đo là 5 giữ, 3 đảo, và khoá
trần `Logical Preset` -> `Logical Preset` nằm trong phe "giữ":

1. `Apply Logical Preset`    -> `Áp dụng **Preset Logical**`   ->  `Áp dụng Logical Preset`
2. `Apply Logical Preset...` -> `Áp dụng **Preset Logical**...` -> `Áp dụng Logical Preset...`
3. `Apply Logical Presets`   -> `Áp dụng các **Preset Logical**` -> `Áp dụng các Logical Preset`

4. `Apply Project Logical Preset...` -> `Áp dụng **Preset Project Logical**...`

   Chỗ này **lệch cả hai quy ước**: "Project" chen giữa "Preset" và "Logical",
   để lại "Logical" lơ lửng. Hai anh em đã đúng nằm ngay cạnh:
       `Apply Project Logical Preset`  -> Áp dụng **Logical Preset cho Project**
       `Apply Project Logical Presets` -> Áp dụng các **Logical Preset cho Project**
   Sửa theo đúng hai anh em.

**Không sửa, đã kiểm:** `Logical Editor Presets` -> `Preset Logical Editor` và
`Project Logical Editor Presets` -> `Preset Project Logical Editor`. Hai cái này
là "tập hợp preset của Logical Editor", nên theo quy ước thứ nhất là
`Preset` + tên (`Preset của Mixer`, `Preset của Strip`). Còn
`Áp dụng Preset Project Logical...` thì "Logical" không thuộc về tên nào cả —
đó là chỗ hỏng. Nhóm "Are you sure you want to remove ..." chia hai cách theo
đúng quy tắc: *remove **all*** -> `gỡ hết`, *remove **this*** -> `gỡ bỏ`.
Nhóm hợp âm `Apply ... chord to selection` thống nhất cả 17 chuỗi.

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
    'Apply Logical Preset': 'Áp dụng Logical Preset',
    'Apply Logical Preset...': 'Áp dụng Logical Preset...',
    'Apply Logical Presets': 'Áp dụng các Logical Preset',
    'Apply Project Logical Preset...':
        'Áp dụng Logical Preset cho Project...',
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

# 1-3. Phe GIU cua thuat ngu "Logical Preset" phai ton tai.
SIBLINGS = [
    ('Logical Preset', 'Logical Preset'),                    # khoa tran, phe giu
    ('Logical Presets', 'Logical Preset'),
    ('Process Logical Preset', 'Logical Preset'),
    ('Apply Project Logical Preset', 'Logical Preset cho Project'),   # 4
    ('Apply Project Logical Presets', 'Logical Preset cho Project'),  # 4
    # quy uoc nha: "X Presets" (tap hop) -> "Preset X"
    ('Mixer Presets', 'Preset'),
    ('Strip Presets', 'Preset'),
    ('Downmix Presets', 'Preset'),
    # va "X Preset" (thuat ngu) -> giu nguyen. Khong duoc sua nham lan.
    ('Algorithm Preset', 'Algorithm Preset'),
    ('Encoder Preset', 'Encoder Preset'),
    # KHONG duoc sua: nhung cai nay theo quy uoc "tap hop"
    ('Logical Editor Presets', 'Preset Logical Editor'),
    ('Project Logical Editor Presets', 'Preset Project Logical Editor'),
    ('Apply Crossfade Preset', 'Preset Crossfade'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1-3. Khong con "Ap dung ... Preset Logical"
bad1 = {k: v for k, v in after.items() if 'Preset Logical' in v
        and 'Logical Editor' not in v}
if bad1:
    problems.append(f'con "Preset Logical" ngoai Logical Editor: {bad1}')

# 4. "Preset" + "Project" + "Logical" ma "Logical" khong thuoc ve ten nao.
# Phai loai "Preset Project Logical Editor" - doi do "Project Logical Editor"
# la TEN, dung quy uoc tap hop.
bad4 = {k: v for k, v in after.items()
        if re.search(r'Preset\s+Project\s+Logical(?!\s+Editor)', v)}
if bad4:
    problems.append(f'con chen "Project" giua Preset va Logical: {bad4}')

# chong pho thu chay rong
n_lp = sum(1 for v in after.values() if 'Logical Preset' in v)
if n_lp < 8:
    problems.append(f'phep thu yeu: chi thay {n_lp} gia tri "Logical Preset", '
                    'mong doi >= 8')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] thuat ngu "Logical Preset": {n_lp} gia tri, het ca hai')
print(f'[doi chieu] "Preset Logical Editor" / "Preset Project Logical Editor" '
      'van con - dung quy uoc tap hop, khong sua')
print()
for k, v in changed.items():
    print(f'  {k[:38]!r}')
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
