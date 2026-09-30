#!/usr/bin/env python3
r"""Vòng 99: 74 chuỗi, #753-826. Đọc tuần tự, không lọc.

Hai lỗi.

1. `Append Selected In Arranger Chain` -> `Thêm mục đã chọn vào Arranger Chain`

   Sáu anh em dùng "Nối thêm":
       `Append` -> `Nối thêm`, `Append Automation Track` -> `Nối thêm Automation Track`,
       `Append Chain Name`, `Append Clip Name to Event Name`,
       `Append Numbers to a Marker Attribute`, `Append Filter`.
   Riêng chuỗi này dùng "Thêm" - dùng cho `Add ...` (`Add to Chord Track` ->
   `Thêm vào Chord Track`). Với "Append" thì "Nối thêm" mới đúng nghĩa: nối
   vào cuối, không phải chèn.

2. `Altered Jazz` -> `Jazz biến âm`

   Đây là **tên thư viện**, và tên thư viện trong danh sách này giữ tiếng Anh
   hết: `Blues 1`, `Blues 2`, `Blues 3`, `Pop 1`, `Pop 2` giữ nguyên cả tên
   lẫn số, `Modern Jazz` -> `Modern Jazz`, `Rock/Easy Jazz` -> giữ,
   `Pop Jazz (3/5/7)` -> giữ, `4-note chords (Open Jazz)` -> giữ.

   Người dùng mở danh sách này để tìm file; tên trên đĩa là tiếng Anh. Dịch
   một nửa thành "Jazz biến âm" là **tệ nhất**: mọi mục khác đều tiếng Anh,
   riêng cái này lọt tiếng Việt, nên nó vừa không khớp tên file vừa đọc lạ.

**Không sửa, đã kiểm:** `AppKey[Key]` -> `Phím Menu` nghe như thừa chữ
"Phím", nhưng đó là đúng: `AppKey` là tên lệnh bàn phím của phím Menu, và
"Phím Menu" là cách gọi đúng. Nhóm này chỉ có một chuỗi nên không có anh em,
nhưng bản dịch không sai nghĩa. Nhóm `Appearance` thì tách theo nghĩa và cái
tách đúng: `Appearance` / `Follow Chord Track Appearance` /
`Sustain Pedal Appearance` nói về **việc hiện** ra (`Hiển thị`), còn
`Appearance of Up/Down Arpeggios` nói về **hình dạng** nốt (`Hình dạng`).
`Opera Gong` -> `Cồng Opera` dịch vì "cồng" là từ tiếng Việt có thật cho nhạc
cụ, khác hẳn tên thư viện.

**Hai phép thử hỏng trong vòng này — một lần rỗng, một lần pass giả.**

*Phép thử rỗng:* quét thể loại bằng điều kiện "giá trị **không** chứa từ thể
loại" và in ra không dòng nào. Đó có thể là "đã sạch" hoặc là "gia đình rỗng" —
hai thứ khác hành hoàn toàn. Đếm gia đình trước: **25** chuỗi, không rỗng.
Nay có `assert fam` để rỗng thì báo lỗi.

*Phép thử pass giả:* sau khi có 25, điều kiện "giữ nguyên thể loại" ra
**25/25** — nghe như sạch tuyệt đối. Nhưng nó chỉ kiểm **một chữ** trong tên
hai chữ. `Jazz biến âm` chứa chữ `Jazz` nên vẫn được tính là "giữ nguyên",
dù `Altered` đã bị dịch. **Phép thử một phần từ khóa là phép thử không
đáng tin** — phải kiểm *cả* tên, không kiểm một từ của nó.

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
    'Append Selected In Arranger Chain': 'Nối thêm mục đã chọn vào Arranger Chain',
    'Altered Jazz': 'Altered Jazz',
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
    ('Append', 'Nối thêm'),                     # 1
    ('Append Automation Track', 'Nối thêm'),
    ('Append Chain Name', 'Nối thêm'),
    ('Append Clip Name to Event Name', 'Nối thêm'),
    ('Append Numbers to a Marker Attribute', 'Nối thêm'),
    # 2: ten thu vien giu nguyen ca ten
    ('Blues 1', 'Blues 1'),
    ('Pop 1', 'Pop 1'),
    ('Modern Jazz', 'Modern Jazz'),
    ('Rock/Easy Jazz', 'Rock/Easy Jazz'),
    ('4-note chords (Open Jazz)', 'Open Jazz'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

# 1. Sau khi sua, moi chuoi "Append ..." deu bat dau bang "Noi them".
after = dict(vi)
after.update(real)
ap = {k: v for k, v in after.items() if k.startswith('Append')}
odd = {k: v for k, v in ap.items() if not v.startswith('Nối thêm')}
if odd:
    problems.append(f'"Append ..." con chuoi khong bat dau "Noi them": {odd}')
if len(ap) < 6:
    problems.append(f'phep thu yeu: chi thay {len(ap)} chuoi "Append", mong doi 6')

# 2. PHEP THU DAY THAT - kiem CA ten, khong kiem mot tu.
#    Pha cu "25/25 giu nguyen" o ban nhat la say: "Jazz bien am" van chua
#    chu "Jazz" nen duoc tinh la giu nguyen, du "Altered" da bi dich.
#    Nay phai kiem gia tri co DUNG chuoi khoa cua ten thu vien.
GENRE = re.compile(r'\b(Jazz|Funk|Rock|Pop|Bebop|Bossa|Swing|Salsa|Ragtime|'
                   r'Ballad|Blues|Country|Disco|Dub|Fusion|Gospel|Grime|'
                   r'Hip Hop|Latin|Mambo|Metal|New Age|Opera|Rap|Reggae|'
                   r'Ska|Soul|Techno|Waltz)\b')
fam = [k for k in vi if GENRE.search(k) and len(k) < 40]
if len(fam) < 20:
    problems.append(f'gia dinh the loai chi {len(fam)} chuoi - co the phep thu '
                    'rong, phai la >= 20')

# Ten thu vien = con so hoac dau ngoac theo sau, dich hoac khong deu dung
# (vi do la ten file), nen CHI danh gia "Co phai chuoi le loi khong".
lib = {k: vi[k] for k in fam if re.match(r'^\w[\w\- ]*\s+\d+$', k)}
odd = {k: v for k, v in lib.items() if not GENRE.search(v)}
if odd:
    problems.append(f'ten thu vien co so bi dich: {odd}')
if len(lib) < 5:
    problems.append(f'phep thu yeu: chi thay {len(lib)} ten thu vien co so, '
                    'mong doi >= 5')

# "Opera Gong" -> "Cong Opera" la ngoai le legitimate: "cong" la tu Viet cho
# nhay cu, khac hanh ten thu vien. Phai con nguyen.
if vi.get('Opera Gong') != 'Cồng Opera':
    problems.append('ngoai le "Opera Gong" bi dong - xem docstring')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] "Append ...": {len(ap)} chuỗi, tất cả "Nối thêm..."')
print(f'[đối chiếu] thể loại: gia đình {len(fam)} chuỗi (không rỗng), '
      f'{len(lib)} tên thư viện có số, không cái nào bị dịch')
print()
for k, v in changed.items():
    print(f'  {k[:44]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
