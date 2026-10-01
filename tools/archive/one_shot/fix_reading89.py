#!/usr/bin/env python3
"""Vòng 89: sửa theo GIA ĐÌNH, không theo chuỗi lẻ.

Vòng 88 lọc bằng tỉ lệ từ. Cách đó sai: nó ra một danh sách chuỗi dài, và độ
dài không phải lỗi. Vòng này làm ngược lại - đi tìm những chuỗi nói **cùng
một thứ** rồi so chúng với nhau.

Cơ: key của bảng dịch chính là **chuỗi tiếng Anh**, không có id, không có
đường dẫn, không có vai trò. Nên "gia đình" là những chuỗi cùng nói một thứ:
`Import Audio File` và `Import Audio Files` là hai phần tử khác nhau của cùng
một nút. Xem riêng lẻ, cả hai đều đọc được. Đặt cạnh nhau thì thấy lệch.

Đo thêm một điều trước khi sửa, để không sửa nhầm: **83 chuỗi Anh dùng ở
nhiều hơn một entry, và không chuỗi nào khác vai trò.** Nên mất ngữ cảnh KHÔNG
phải lý do bản dịch cứng. Giả thuyết đó sai.

Sáu lỗi thật:

1. `Import Audio File` -> `Import file Audio` nhưng `Import Audio Files` ->
   `Import File Audio`. Một chữ "File" thường, một chữ hoa.

2. `Side-Chain Input` -> `Side-Chain Input` nhưng `Side-chain Inputs` ->
   `Side-chain Input`. C với c.

3. `-oo dB` và `-inf dB` là **hai ký hiệu cho cùng một thứ** trong cùng một
   file: âm vô cùng. Cubase tự viết `-oo dB` ở một chỗ và `-inf dB` ở chỗ
   khác. Cả hai nên ra `-∞ dB` - ký hiệu mà một mixer thật sự dùng, và mà
   tiếng Việt không cần dịch.

4. `% Full` -> `% Đầy`. Sai nghĩa: trong meter, "Full" là **toàn dải**, không
   phải "đầy" (= đầy bển/disk full).

5. `1 foot` -> `1 Foot`. Đơn vị đo không hoa chữ đầu. Cùng nhóm còn
   `Centimeters (cm)` -> `Centimét (cm)`, cái đó đúng.

6. Hai chuỗi bỏ trống: `Full Score` còn nguyên tiếng Anh, `Full Position` dịch
   nửa (`Vị trí Full`). Cùng nhóm `Full` còn ~25 chuỗi đã dịch đúng.

Không sửa, có chủ đích:

  * `Channel` / `Channel ` — HAI key khác nhau, chỉ khác khoảng trắng cuối.
    Giữ nguyên khoảng trắng là đúng, nếu bỏ thì hai chuỗi dịch trùng nhau
    trong khi Cubase tra hai key khác nhau.
  * `Db` / `dB` — Cubase tự viết `Db` ở một key. Không phải việc của ta sửa
    lỗi chính Steinberg.
  * `DRY`/`Dry`, `OFFLINE`/`Offline`, `PRE`/`Pre` — tiếng Anh gốc đã phân biệt.

  python tools/fix_reading89.py
  python tools/fix_reading89.py --write
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
    # ---- 1 + 2. gia đình lệch hoa/thường
    'Import Audio File': 'Import file Audio',
    'Import Audio Files': 'Import file Audio',
    'Side-Chain Input': 'Side-Chain Input',
    'Side-chain Inputs': 'Side-Chain Input',

    # ---- 3. hai ký hiệu cho âm vô cùng -> một
    '-oo dB': '-∞ dB',
    'Export Muted Events with Volume -inf dB':
        'Export Event bị Mute với Volume -∞ dB',

    # ---- 4. sai nghĩa
    '% Full': '% toàn dải',

    # ---- 5. đơn vị đo không hoa
    '1 foot': '1 foot',

    # ---- 6. bỏ trống / dịch nửa trong nhóm Full
    'Full Score': 'Bản nhạc đầy đủ',
    'Full Position': 'Vị trí đầy đủ',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    ph = lambda s: sorted(re.findall(r'%[sd]|%\.\d+f|\{\w*\}', s))
    if ph(v) != ph(src[k]):
        problems.append(f'placeholder: {k[:46]!r} {ph(src[k])} -> {ph(v)}')
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r}')
    # khoảng trắng đầu/cuối phải y hệt nguồn
    lead = lambda s: s[:len(s) - len(s.lstrip())]
    trail = lambda s: s[len(s.rstrip()):]
    if (lead(v), trail(v)) != (lead(src[k]), trail(src[k])):
        problems.append(f'surrounding space: {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')

# Gia đình phải thống nhất sau khi sửa: hai thành viên cùng nói một thứ thì
# phải cho cùng một câu chữ.
FAMILY_PAIRS = [
    ('Import Audio File', 'Import Audio Files'),
    ('Side-Chain Input', 'Side-chain Inputs'),
]
for a, b in FAMILY_PAIRS:
    va = WORDING.get(a, vi.get(a))
    vb = WORDING.get(b, vi.get(b))
    if va != vb:
        problems.append(f'family split: {a!r}={va!r} but {b!r}={vb!r}')

# Âm vô cùng phải dùng đúng một ký hiệu trong cả bản dịch.
after = dict(vi)
after.update(real)
inf_keys = [k for k, v in after.items() if '-oo' in k or '-inf' in k]
bad_inf = [k for k in inf_keys
           if ('-oo' in k or '-inf' in k) and '-∞' not in after[k]]
if bad_inf:
    problems.append(f'âm vô cùng viết hai kiểu: {bad_inf[:5]}')

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
    print(f'  {k[:54]!r}')
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
