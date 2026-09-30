#!/usr/bin/env python3
"""Vòng 90: 130 chuỗi đầu, đọc tuần tự.

Không lọc. Đọc hết, đánh giá từng cặp. 55 chuỗi đầu **không có lỗi thật** —
bảng đầu đã qua 89 vòng nên sạch. Sáu lỗi nằm ở 90 chuỗi kế.

Và một cảnh báo, vì tôi suýt phá 9 chuỗi tốt:

`%s Settings` -> `Cài đặt %s` trông như **sai** — `%s` ở đầu, đặt cuối thì
lạ. Tôi định sửa cả 9 chuỗi `%s ...` như vậy. Kiểm cả nhóm thì ngược lại:

    Audio Settings        -> Cài đặt Audio
    Automation Settings   -> Cài đặt Automation
    Edit Channel Settings -> Sửa cài đặt Channel

`%s` ở đây là **tính ngữ**, đứng sau "Cài đặt", đúng với 40 chuỗi anh em. Bản
dịch cũ **đúng**. Đây là lần thứ ba tôi kết luận từ mẫu bề mặt rồi phải lật
lại: lần trước là "dài", lần nữa là "mất ngữ cảnh", lần này là "`%s` là động
từ". **Suy đoán về placeholder mà không tra cả nhóm thì đừng làm.**

Sáu lỗi thật, tất cả đều là **lệch với chính anh em của nó**:

1. `"%s" not possible for write protected tracks` -> `...với Track chống ghi`
   - "Track chống ghi" là dịch sát. Hai chuỗi anh em trong cùng nhóm
     (`"Create Versions from Lanes" not possible for write protected tracks`)
     đã dùng `các Track bị bảo vệ ghi`. Và hai chuỗi `... for frozen tracks`
     / `... that are recording` đều có "các", riêng chuỗi này thì không.
   - Sửa thành `Không thể "%s" với các Track bị bảo vệ ghi`.

2. Hai chuỗi `"Pitch Visibility: ..." not possible` dùng **hai cách**:
   `không khả dụng vì` và `Không thể ... vì`. Cả nhóm Cubase dùng "không khả
   dụng". Đồng nhất.

3. `(Click to Open/Close Editor)` -> `(Nhấp để Mở/Đóng Editor)`. Hoa giữa câu.
   Tiếng Việt không hoa chữ đóc giữa câu.

4. `(externally clocked)` -> `(Externally Clocked)`. Hoa chữ đầu trong ngoặc,
   trong khi nguồn viết thường. **Không** dịch: cả nhóm đã quyết giữ `Clock` là
   thuật ngữ DAW (`Word Clock`, `Clock Source` -> `Nguồn Clock`).

5. `- Reset complex transitions to linear transitions` -> `transition` để
   thô, viết thường, hai lần. Nhóm anh em dùng `Chuyển tiếp`
   (`EQ/Filter Transition` -> `Chuyển tiếp EQ/Filter`). Đây là Cubase's
   Transition = chuyển tiếp âm thanh.

6. `sample-precise` -> `chính xác đến Sample`. "đến Sample" đọc cụt; tiếng
   Việt cần "tới từng".

  python tools/fix_reading90.py
  python tools/fix_reading90.py --write
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
    # 1. đồng nhất với hai chuỗi anh em cùng câu hình "%s not possible for ..."
    '"%s" not possible for write protected tracks':
        'Không thể "%s" với các Track bị bảo vệ ghi',

    # 2. hai chuỗi CÙNG câu hình, đang dùng hai cách
    '"Pitch Visibility: Select Next Option" not possible because there are no '
    'note events in the editor':
        '"Hiển thị Pitch: Chọn tùy chọn kế tiếp" không khả dụng vì Editor '
        'không có Note Event nào',

    # 3. tiếng Việt không hoa giữa câu
    '(Click to Open/Close Editor)': '(Nhấp để mở/đóng Editor)',

    # 4. giữ tiếng Anh - cả nhóm đã giữ "Clock" là thuật ngữ DAW - nhưng bỏ hoa
    '(externally clocked)': '(externally clocked)',

    # 5. "Transition" của Cubase = chuyển tiếp âm thanh; nhóm anh em đã dịch
    '- Reset complex transitions to linear transitions':
        '- Đặt lại chuyển tiếp phức tạp thành chuyển tiếp tuyến tính',

    # 6. "chính xác đến Sample" đọc cụt
    '- Maximum project duration for sample-precise object positions exceeded':
        '- Vượt quá thời lượng Project tối đa cho vị trí đối tượng chính xác '
        'tới từng Sample',
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
    lead = lambda s: s[:len(s) - len(s.lstrip())]
    trail = lambda s: s[len(s.rstrip()):]
    if (lead(v), trail(v)) != (lead(src[k]), trail(src[k])):
        problems.append(f'surrounding space: {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')

# Đối chiếu với anh em THẬT, viết bằng key đúng. Lần trước tôi đoán key nên
# tự kiểm báo "giả định sai" - đúng, nhưng phải tra key thật chứ không sửa
# luôn con số cho vừa.
after = dict(vi)
after.update(real)
SIBLINGS = [
    # cùng câu hình "%s not possible for <trạng thái>"
    ('"%s" not possible for frozen tracks', 'với các Track'),
    ('"%s" not possible for tracks that are recording', 'với các Track'),
    ('"Create Versions from Lanes" not possible for write protected tracks',
     'bảo vệ ghi'),
    # cùng câu hình '"Pitch Visibility: Select Next Option" not possible ...'
    ('"Pitch Visibility: Select Next Option" not possible because no '
     'compatible instrument is connected', 'không khả dụng vì'),
    # nhóm Transition đã dịch
    ('EQ/Filter Transition: Quick', 'Chuyển tiếp'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: key anh em không tồn tại: {k[:52]!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k[:46]!r} không chứa {must!r}')

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
    print(f'  {k[:56]!r}')
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
