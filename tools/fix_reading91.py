#!/usr/bin/env python3
"""Vòng 91: 82 chuỗi, #145-226. Đọc tuần tự, không lọc.

Bốn lỗi, tất cả nằm ở **một gia đình duy nhất**: nhóm "mẫu số".

1. `1/64 Note (Hemidemisemiquaver)` -> `Note 1/64, nốt móc tư`
   Dấu phẩy thay cho ngoặc. Cả 4 anh em dùng ngoặc:
   `Note 1/16 (nốt móc kép)`, `Note 1/32 (nốt móc ba)`, `Note 1/4 (nốt đen)`,
   `Note 1/2 (nốt trắng)`. Một cái lệch kiểu là lỗi, không phải lựa chọn.

2. Nhóm "mẫu số" (5 thành viên) dùng **hai cách**:

       1/16 Notes (Semiquavers) in 1/8 Note    -> mẫu số **nốt** 1/8
       1/32 Notes (Demisemiquavers) in 1/16...-> mẫu số **nốt** 1/16
       1/8 Notes (Quavers) in 1/4 Note        -> mẫu số **Note** 1/4
       Beaming 1/8 Notes (Quavers) Together... -> mẫu số **Note** 1/4
       Quarter Note (Crotchet) Denominator ... -> mẫu số **Note** 1/4

   Hai cái viết "nốt", ba cái để thô "Note". Đa số và cái **đúng** là "nốt" -
   tiếng Việt, và khớp hai anh em kia. Ba cái kia lọt tiếng Anh giữa câu
   tiếng Việt. Sửa ba.

3. `Quarter Note (Crotchet) Denominator Time Signatures With Half-Bars` ->
   `Số chỉ nhịp mẫu số Note 1/4` - ngoài lỗi "Note" còn **lặp chữ**: "số chỉ
   nhịp ... mẫu số Note 1/4", trong khi `1/8 Notes ... in 1/4 Note` dùng "với
   mẫu số nốt 1/4". Cùng khái niệm, hai cách viết câu.

**Không sửa, có chủ đích:** `1st`..`5th` -> `Thứ nhất`..`Thứ năm`, dù
`1st Inversion` -> `Thể đảo 1`. Nghe như lệch, nhưng `1st` đứng một mình
**không** cùng họ với `1st Inversion`: không có `2nd Inversion`, không có
`3rd Inversion` trong bảng. Đây là danh sách chọn nào đó, còn `Inversion` là
thuật ngữ đảo hợp âm. Hai ngữ cảnh khác nhau, nên giữ. Đổi sang `1` cần biết
nó hiện ở đâu - mà bảng không có thông tin đó.

  python tools/fix_reading91.py
  python tools/fix_reading91.py --write
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
    # 1. ngoặc, không phải dấu phẩy
    '1/64 Note (Hemidemisemiquaver)': 'Note 1/64 (nốt móc tư)',

    # 2 + 3. nhóm "mẫu số": ba chỗ lọt "Note" trong câu tiếng Việt
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nốt 1/8 (nốt móc đơn) với mẫu số nốt 1/4 (nốt đen)',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) Denominator '
    'Time Signatures':
        'Nối chung đuôi nốt 1/8 với mẫu số nốt 1/4 (nốt đen)',
    'Quarter Note (Crotchet) Denominator Time Signatures With Half-Bars':
        'Số chỉ nhịp có mẫu số nốt 1/4 (nốt đen) kèm nửa Bar',
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

# Sau khi sửa, KHÔNG được còn "mẫu số Note" ở bất kỳ chỗ nào.
after = dict(vi)
after.update(real)
leak = [k for k, v in after.items() if 'mẫu số Note' in v]
if leak:
    problems.append(f'vẫn còn "mẫu số Note": {leak}')

# Và nhóm nốt phải thống nhất dùng ngoặc.
for k in ('1/16 Note (Semiquaver)', '1/32 Note (Demisemiquaver)',
          '1/4 Note (Crotchet)', '1/2 Note (Minim)'):
    if k in vi and not re.search(r'\([^)]*\)', vi[k]):
        problems.append(f'giả định sai: anh em {k!r} không dùng ngoặc')

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
    print(f'  {k[:60]!r}')
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
