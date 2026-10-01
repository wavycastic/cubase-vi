#!/usr/bin/env python3
r"""Vòng 95: 78 chuỗi, #445-522. Đọc tuần tự, không lọc.

Hai lỗi.

1. `Add Command` -> `Thêm lệnh` nhưng `Add Command to Macro` -> `Thêm **Lệnh** vào
   Macro`. Hai chuỗi cạnh nhau, một chữ "lệnh", một chữ "Lệnh".

2. `Direction [musical performance direction]` -> `Chỉ dẫn diễn tấu`

   Vòng 88 đã sửa `Attributes apply to individual notes, directions apply to
   all following notes` từ "chỉ dẫn diễn tấu" thành "chỉ dẫn", và **bỏ sót
   chỗ này**. Giờ còn đúng một chỗ, nằm giữa hai anh em:

       Attributes apply to individual notes, ...  -> chỉ dẫn áp dụng cho ...
       Score Direction                            -> Chỉ dẫn trong Score
       Direction [musical performance direction]  -> Chỉ **dien tau**   <- lạc

   Còn "hướng" thì giữ riêng, và đúng: `Direction [direction of a stem]` ->
   `Hướng của thân nốt`, cùng `Direction of reanalysis...` -> `Hướng phân tích
   lại`. Hai nghĩa khác nhau - hướng vật lý, và chỉ dẫn ghi trong bản nhạc -
   nên tách là đúng. Chỉ cái đuôi "diễn tấu" là thừa.

**Một kiểm tra lại hỏng, ghi lại.** Tôi tìm "chỉ dẫn diễn tấu" trong
`vi.json` và nhận **0**, nên tưởng vòng 88 đã sạch. Thực ra giá trị bắt đầu
bằng chữ `Chỉ` hoa, còn tôi tìm chuỗi viết thường. Kiểm tra phân biệt hoa
thường thì ra **1**. Đây là lần thứ nhiều một phép thử âm thầm không khớp
gì và tôi đọc kết quả đó là sự thật - lần trước là `dict` khoá số, tra ký tự
vào. Nay script có `assert hits` để phép thử rỗng thì phải báo lỗi chứ
không được âm thầm trả về 0.

**Không sửa, đã kiểm:** `Add Next to Selection` -> `Thêm ngay sau vùng chọn`
và `Add Previous to Selection` -> `Thêm ngay trước vùng chọn`. "Next to" ở đây
là **thứ tự** trong danh sách, không phải vị trí không gian, nên "sau"/"trước"
đúng. Còn `Subfolder Next to Exported File` -> `... bên cạnh file Export` dùng
"bên cạnh" vì nghĩa là anh em cùng thư mục. Hai nghĩa khác nhau, cả hai đúng.

  python tools/fix_reading95.py
  python tools/fix_reading95.py --write
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
    'Add Command to Macro': 'Thêm lệnh vào Macro',
    'Direction [musical performance direction]': 'Chỉ dẫn',
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
    ('Add Command', 'Thêm lệnh'),                       # 1
    ('Attributes apply to individual notes, directions apply to all '
     'following notes', 'chỉ dẫn'),                   # 2, vòng 88
    ('Score Direction', 'Chỉ dẫn'),                     # 2
    # "hướng" phải GIỮ cho nghĩa hướng vật lý
    ('Direction [direction of a stem]', 'Hướng'),      # 2
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy {k[:50]!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k[:46]!r} không chứa {must!r}')

# Sau khi sửa, "chỉ dẫn diễn tấu" phải biến mất khỏi cả bản dịch.
# So KHÔNG phân biệt hoa thường, và assert để phép thử rỗng bị báo lỗi chứ
# không âm thầm trả 0.
after = dict(vi)
after.update(real)
left = [k for k, v in after.items() if 'chỉ dẫn diễn tấu' in v.lower()]
if left:
    problems.append(f'vẫn còn "chỉ dẫn diễn tấu": {left}')
# đối chiếu: phép thử này PHẢI bắt được thứ gì đó trước khi sửa
if not any('chỉ dẫn diễn tấu' in v.lower() for v in vi.values()):
    problems.append('phép thử rỗng - "chỉ dẫn diễn tấu" đã hết trước khi sửa, '
                    'có lẽ đã hết sạch từ vòng trước')

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
    print(f'  {k[:50]!r}')
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
