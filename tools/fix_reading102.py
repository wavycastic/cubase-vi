#!/usr/bin/env python3
r"""Vòng 102: 74 chuỗi, #973-1046. Đọc tuần tự, không lọc.

Hai lỗi, một quy ước: **khoá `"X - Y"` thì giá trị phải còn dấu ` - `.**

    Audio - Assets                 -> `Tài nguyên Audio`      <- mat dau gach
    Audio - Properties            -> `Thuộc tính Audio`       <- mat dau gach
    Audio - Snap to Zero Crossing -> `Audio - Snap vào ...`   <- giu

Cả bảng có 36 nhóm `"X - Y"`, tổng **93** chuỗi: **91 giữ dấu gạch, 2 mất**,
và hai cái mất nằm ngay trong nhóm của nhau. Quy ước không chỉ ở chỗ tiền tố
phải giữ tiếng Anh:

    Arranger - Remove All          -> `Arranger - Gỡ bỏ tất cả`      (giu)
    Automation Mode - Auto-Latch  -> `Chế độ Automation - Auto-Latch` (dich tien to, giu gach)
    Auto Fades - Project: %s      -> `Fade tự động - Project: %s`    (dich tien to, giu gach)
    Chord Editing - Inversions... -> `Chỉnh sửa hợp âm - Đảo: ...`   (dich, giu gach)

Nghĩa là **dịch tiền tố nhưng giữ cấu trúc**, không phải "giữ tiếng Anh cho
chắc". `Audio` vốn đã là thuật ngữ giữ nguyên, nên sửa thành
`Audio - Tài nguyên` và `Audio - Thuộc tính`.

**Một phép thử của tôi hỏng trước khi tới kết luận.** Tôi xếp nhóm theo câu
"giá trị có bắt đầu bằng tiền tố không", và điều đó **không** phân biệt được
hai thứ khác nhau: *dịch tiền tố* (`Auto Fades` -> `Fade tự động`) và *bỏ hẳn
dấu gạch*. Kết quả là 15 nhóm bị dán nhãn "mất" oan. Câu hỏi đúng phải là
"**giá trị có còn dấu ` - ` không**", và khi hỏi đúng thì ra 91/2 rõ ràng.
Tỉ lệ 91/2 mà đo sai thành 36 nhóm "loạn" thì bằng không thông tin.

**Không sửa, đã kiểm:**

*`Audio Part Editor: `* kết thúc bằng **dấu cách**, trông như lỗi — nhưng
dấu cách nằm trong **chính khoá**: `repr` cho `'Audio Part Editor: '`. Giữ nó
là đúng, y như `Channel` cạnh `Channel `.

*Nhóm `Audio Performance`* đang lệch nhưng bằng chứng thật sự **chia đều**:

    Audio Performance        -> `Hiệu năng Audio`      (dich)
    VST Performance          -> `VST Hiệu năng`        (dich)
    ...Click to Show Audio Performance... -> `...Bảng Hiệu năng Audio`  (dich)
    Audio Performance Meter  -> `Audio Performance Meter`  (giu)
    Audio Performance Monitor-> `Audio Performance Monitor`(giu)

Ba dịch, hai giữ — và hai cái giữ là **tên bảng cửa sổ có tên** trong Cubase,
nên giữ có lý do riêng. 3/2 không phải bằng chứng. **Để nguyên**, ghi ở đây.

"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

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
    'Audio - Assets': 'Audio - Tài nguyên',
    'Audio - Properties': 'Audio - Thuộc tính',
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
    # 1. chinh quy uoc cua vong nay: khoa "X - Y" phai giu dau gach
    if ' - ' not in v:
        problems.append(f'gia tri bo dau gach: {k[:44]!r} -> {v!r}')

# Cac anh em giu cau truc. Phe "dich tien to, giu gach" phai con nguyen.
SIBLINGS = [
    ('Audio - Snap to Zero Crossing', ' - '),
    ('Arranger - Remove All', ' - '),
    ('Automation Mode - Auto-Latch', ' - '),
    ('Auto Fades - Project: %s', ' - '),
    ('Chord Editing - Inversions: Move Up', ' - '),
    ('Absolute Mode - Force all parameters to the same value', ' - '),
    ('Browse Project - %s', ' - '),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'anh em khong ton tai: {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')


def dash_survey(m):
    """Chia khoa 'X - Y' thanh giu dau gach / mat dau gach."""
    g = defaultdict(lambda: {'dash': 0, 'nodash': 0})
    for k, v in m.items():
        mm = re.match(r'^([A-Z][\w ]{0,20}?) - ', k)
        if mm:
            g[mm.group(1).strip()]['dash' if ' - ' in v else 'nodash'] += 1
    return g


after = dict(vi)
after.update(real)
g = dash_survey(after)
n_dash = sum(x['dash'] for x in g.values())
n_nodash = sum(x['nodash'] for x in g.values())

# Phai co it nhat 90 chuoi giu dau gach - neu phep thu chay rong thi fail
if len(g) < 30:
    problems.append(f'phep thu yeu: chi thay {len(g)} nhom "X - Y", mong doi >= 30')
if n_dash < 85:
    problems.append(f'phep thu yeu: chi thay {n_dash} chuoi giu dau gach, '
                    'mong doi >= 85')
# Sau khi sua, KHONG con chuoi nao mat dau gach
if n_nodash:
    bad = [k for k, v in after.items()
           if re.match(r'^[A-Z][\w ]{0,20}? - ', k) and ' - ' not in v]
    problems.append(f'con {n_nodash} chuoi mat dau gach: {bad}')

# Khoa "Audio Part Editor: " giu dau cach trong khoa - khong duoc lam sai.
sk = 'Audio Part Editor: '
if sk not in vi:
    problems.append('khong thay khoa "Audio Part Editor: " co dau cach thua')
elif not vi[sk].endswith(' '):
    problems.append(f'khoa co dau cach thua nhung gia tri bi cat - '
                    f'{sk!r} -> {vi[sk]!r}')

# Nhom "Audio Performance" phai giu nguyen ca 3 chuoi (chua quyet)
ap = [k for k in vi if 'Audio Performance' in k and 'Click to Show' not in k]
if len(ap) != 3:
    problems.append(f'phep thu yeu: nhom "Audio Performance" co {len(ap)} '
                    'chuoi, mong doi 3')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] "X - Y": {len(g)} nhom, {n_dash} giu dau gach, '
      f'{n_nodash} mat')
print(f'[ghi nhan] "Audio Performance": {len(ap)} chuoi, 3 dich / 2 giu - '
      'chua quyet, de nguyen')
print()
for k, v in changed.items():
    print(f'  {k[:30]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
