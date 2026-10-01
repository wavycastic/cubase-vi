#!/usr/bin/env python3
r"""Vòng 92: 76 chuỗi, #227-302. Đọc tuần tự, không lọc.

1. `About %s` -> `Về %s...`

   "Về" nghĩa là "về chuyện này", là **dịch sát** của "about" trong nghĩa
   văn bản. Trong menu phần mềm, "About" là **"Giới thiệu"** - đó là cách
   gọi của mọi phần mềm tiếng Việt, và Cubase có đúng một chuỗi này nên
   không có anh em để đối chiếu; nhưng đây là thuật ngữ giao diện quy chuẩn,
   không phải suy đoán.

2. `A file name cannot contain any of the following characters` ->
   `Tên file không chứa ký tự sau`

   Cặp song sinh `A profile name cannot contain any of the following
   characters: \ / : * ? " < > |` đã dịch là `không thể chứa bất kỳ ký tự nào
   sau đây`. Cùng một cấu trúc tiếng Anh, hai cách tiếng Việt. Đồng nhất theo
   cặp.

   **Giữ nguyên việc không có dấu hai chấm**: khoá của cặp này *không* kèm
   danh sách ký tự, còn khoá của cặp kia *có*. Nên bản dịch cũng không được
   thêm dấu hai chấm — thêm vào thì nhãn bị cắt ngang, và đó là loại lỗi
   tôi đã mắc ở vòng 88 (thêm `(%s)` không có trong nguồn).

3. `A file named\n%s\nalready exists in the Pool...` -> `File tên\n%s\n...`

   "File tên" đọc cụt. Đây là **nhận định**, không phải lỗi chứng minh được:
   bảng không có chuỗi anh em nào khác, nên không có cái gì để đối chiếu.
   Nhưng `File có tên` là cách nói tiếng Việt bình thường, và sai thì tệ hơn
   bản cũ. Ghi rõ ở đây để sau này ai đó biết chỗ này là chỗ tôi *thấy là*
   đọc khó chịu, không phải chỗ tôi chứng minh được.

**Không sửa, có lý do:** `ASIO-Guard has been disabled...` có dẫn đường dẫn
menu `Studio > Thiết lập Studio > VST Audio System` — đã tra, `Studio Setup`
dịch là `Thiết lập Studio`, nên đường dẫn khớp. `Accent`, `ADR`, `Abs` giữ
tiếng Anh, đúng nhóm thuật ngữ. `Above Top Staff of System` đọc hơi cụt
("Phía trên khuông nhạc **trên cùng**") nhưng cả nhóm `Above ...` đều cấu
trúc đó, sửa riêng nó sẽ lệch khỏi anh em.

  python tools/fix_reading92.py
  python tools/fix_reading92.py --write
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
    # 1. About trong menu = Giới thiệu, không phải "Về"
    'About %s': 'Giới thiệu %s...',

    # 2. đồng nhất với cặp "A profile name cannot contain..."
    'A file name cannot contain any of the following characters':
        'Tên file không thể chứa bất kỳ ký tự nào sau đây',

    # 3. nhận định, xem docstring
    'A file named\\n%s\\nalready exists in the Pool.\\nIt is not possible to '
    'replace it.\\nPlease use another name or another location.':
        'File có tên\\n%s\\nđã có trong Pool.\\nKhông thay được file này.\\n'
        'Dùng tên khác hoặc vị trí khác.',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r} '
                        f'{src[k].count(chr(10))} -> {v.count(chr(10))}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

# 2. KHÔNG được thêm dấu hai chấm khi nguồn không có. Đã mắc lỗi này ở vòng 88.
for k, v in real.items():
    if v.rstrip().endswith(':') and not src[k].rstrip().endswith(':'):
        problems.append(f'thêm dấu hai chấm không có trong nguồn: {k[:46]!r}')

# 2. cặp song sinh phải dùng cùng cách diễn đạt
twin = 'A profile name cannot contain any of the following characters: \\ / : * ? " < > |'
if twin not in vi:
    problems.append('giả định sai: không thấy cặp song sinh của file name')
elif 'không thể chứa bất kỳ ký tự nào sau đây' not in vi[twin]:
    problems.append('giả định sai: cặp song sinh không dùng cách diễn đạt này')

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
    print(f'  {k[:58]!r}')
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
