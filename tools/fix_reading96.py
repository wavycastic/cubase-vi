#!/usr/bin/env python3
r"""Vòng 96: 78 chuỗi, #523-600. Đọc tuần tự, không lọc.

Năm lỗi, tất cả là **lệch với anh em ngay bên cạnh**.

1. `Add String Above` -> `Thêm String phía trên`
   `Add String Below` -> `Thêm **dây** phía dưới`
   Cùng một từ, hai cách, hai chuỗi sát nhau.

2. `Add Selected as Database Slaves` -> `Thêm mục đã chọn làm Database Slave`
   `Add Selected as MMC Slaves`      -> `Thêm **các** mục đã chọn làm MMC Slave`
   `Add Selected as Remote Slaves`   -> `Thêm **các** mục đã chọn làm Remote Slave`
   Hai chuỗi sau có "các", riêng chuỗi đầu thì không.

3. **Nhóm `Filter`: KHÔNG sửa, và đây là câu hỏi mở.**

   Tôi định sửa `Add filter` -> `Thêm bộ lọc` thành `Thêm Filter`, vì cả bản
   dịch có 32 giá trị chứa "Filter" so với 17 chứa "bộ lọc". **Tự kiểm của
   vòng này chặn lại**, vì 15 chỗ "bộ lọc" còn lại tôi đã bỏ sót (lần quét
   đầu chỉ lọc key ngắn hơn 34 ký tự).

   Rồi tra cặp quyết định:

       Remove Filter  -> Gỡ bỏ **bộ lọc**
       Remove filter  -> Gỡ bỏ **bộ lọc**

   Cả hai đều "bộ lọc" - bản dịch **không** phân biệt hoa/thường như
   tiếng Anh. Vậy có hai cụm: khoá trần `Filter` -> `Filter`,
   `Activate/Deactivate Filter` -> `Bật/Tắt **Filter**`; còn
   `Input Filter`, `Rating Filter`, `Remove Filter`, `Add filter`... ->
   "**bộ lọc**".

   Có thể là quy ước có chủ đích (thuật ngữ có tên giữ tiếng Anh, danh từ
   thường thì dịch) - giống hệt `String`/`dây` ở mục 1. Cũng có thể là lệch.
   17 đứng 32 thì **không đủ để kết luận**, và sửa 17 chuỗi theo tỉ lệ
   51/49 chính là loại lỗi tôi đã mắc bốn lần. **Để nguyên**, ghi lại ở đây
   để lần sau biết đây là chỗ *chưa* quyết, không phải chỗ đã quết.

4. `Add User to Permission List`      -> `... vào **Danh sách** Permission`
   `Delete User from Permission List` -> `... từ **Danh sách** Permission`

   "Danh sách" hoa giữa câu. Trong 6 chỗ có "Danh sách", bốn chỗ còn lại đều
   ở đầu giá trị hoặc sau dấu gạch nối, nên hoa là đúng:
   `List` -> `Danh sách`, `Track List` -> `Danh sách Track`,
   `Chord Assistant - List` -> `... - Danh sách`,
   `Name (List of ...)` -> `Tên (Danh sách tên mục Punch-Log)`.
   Riêng hai chuỗi này "vào/từ Danh sách" nằm giữa câu. Chỉ bỏ hoa, giữ
   nguyên "từ" - đổi thêm từ nữa là mở rộng ngoài phạm vi.

**Không sửa, đã kiểm:** `Add Up` -> `Thêm lên` và `Add Down` -> `Thêm xuống`
trông lệch với `Add Above` -> `Thêm ở trên`. Nhưng *up/down* là **dời vị
trí** trong danh sách, còn *above/below* là **chèn cạnh**; hai menu khác nhau.
Tiếng Việt dùng "lên/xuống" cho cái trước và "ở trên/ở dưới" cho cái sau là
đúng. `Add Time` -> `Thêm thời gian` không có anh em để đối chiếu, nên để.

  python tools/fix_reading96.py
  python tools/fix_reading96.py --write
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
    # 1
    'Add String Below': 'Thêm String phía dưới',
    # 2
    'Add Selected as Database Slaves': 'Thêm các mục đã chọn làm Database Slave',
    # 3. nhóm Filter: để nguyên, xem docstring
    # 4. chỉ bỏ hoa "Danh sách", giữ nguyên "vào"/"từ"
    'Add User to Permission List': 'Thêm người dùng vào danh sách Permission',
    'Delete User from Permission List':
        'Xóa người dùng từ danh sách Permission',
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
    ('Add String Above', 'Thêm String'),              # 1
    ('Add Selected as MMC Slaves', 'các mục'),        # 2
    ('Add Selected as Remote Slaves', 'các mục'),
    ('List', 'Danh sách'),                             # 4: hoa ở đầu là đúng
    ('Track List', 'Danh sách'),
    # 3: nhóm Filter đang lệch, nhưng chưa quyết được - chỉ ghi nhận
    ('Filter', 'Filter'),
    ('Remove Filter', 'bộ lọc'),
    ('Remove filter', 'bộ lọc'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k[:40]!r} không chứa {must!r}')

after = dict(vi)
after.update(real)
if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

# Nhóm Filter: báo số liệu để lần sau không phải đo lại, nhưng KHÔNG chặn vòng
# này - 17/32 không đủ bằng chứng để chọn, mà sửa 17 chuỗi theo 51/49 thì
# chính là loại lỗi đã mắc bốn lần.
n_en = sum(1 for v in after.values() if re.search(r'\bFilter\b', v))
n_vi = sum(1 for v in after.values() if 'bộ lọc' in v.lower())
print(f'[ghi nhận] nhóm Filter còn lệch: {n_en} giá trị giữ "Filter", '
      f'{n_vi} giá trị dùng "bộ lọc" - chưa đủ bằng chứng, để nguyên')

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:42]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
