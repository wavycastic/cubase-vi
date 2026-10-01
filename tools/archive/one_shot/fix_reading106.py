#!/usr/bin/env python3
r"""Vòng 106: 74 chuỗi, #1265-1338. Đọc tuần tự, không lọc.

Một lỗi: `Bypass Inserts of All Visible Channels` giữ **số nhiều** trong khi
cả nhóm bỏ.

Có **năm** chuỗi cùng khuôn `"... of All Visible Channels"`, và chỉ hai trong
đó bỏ số nhiều:

    Bypass Channel Strip of All Visible Channels -> `Bypass Channel Strip mọi...`
    Bypass EQs of All Visible Channels           -> `Bypass **EQ** của tất cả...`
    Bypass **Inserts** of All Visible Channels   -> `Bypass **Inserts** của...`  <- lạc
    Bypass Modulators of All Visible Channels    -> `Bypass **Modulator** của...`
    Bypass **Sends** of All Visible Channels     -> `Bypass **Sends** của...`    <- lạc

Nhưng bằng chứng quyết định nằm ở **chính các danh từ** của chúng, mỗi từ có
nhiều chuỗi hơn một:

    `Insert`  : `Bypass Insert` -> `Bypass Insert`, `Bypass: Inserts` ->
                `Bypass: Insert`, `Bypass: Inserts on Main Mix` ->
                `Bypass: Insert trên Main Mix`, `Bypass Inserts` -> `Bypass Insert`
    `Modulator`: `Bypass Modulators` -> `Bypass Modulator`, `Bypass: Modulators` ->
                `Bypass: Modulator`
    `Send`    : `Bypass Send` -> `Bypass Send`, `Bypass Sends` -> `Bypass Send`,
                `Bypass: Sends` -> `Bypass: Send`

**Mười chuỗi, không chuỗi nào giữ số nhiều.** Nên `Bypass Inserts of All Visible
Channels` giữ là lỗi, và `Bypass Sends of All Visible Channels` cũng vậy — nó
đứng cùng hàng với cái kia trong năm chuỗi trên, không có lý do để một cái được
miễn.

Về `Sends`: trong năm chuỗi "of All Visible Channels" có **hai** cái giữ số
nhiều (`Inserts`, `Sends`) và **ba** cái bỏ. Nếu chỉ nhìn riêng hàng đó thì
2/3 chưa đủ. Nhưng `Send` số ít đã được chốt ở **mười** chuỗi khác, nên kết
luận lấy từ đó, không lấy từ hàng này. Đây là chỗ mà số đo cục bộ ngược với
bằng chứng toàn cục, và bằng chứng toàn cục mới là cái đúng.

**Không sửa, đã kiểm:** `Bypass Inserts` -> `Bypass Insert` và
`Bypass Sends` -> `Bypass Send` — hai khoá khác nhau nhưng cùng nghĩa; giữ
nguyên là đúng, y như `Channel` cạnh `Channel `.

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
    'Bypass Inserts of All Visible Channels':
        'Bypass Insert của tất cả Channel đang hiện',
    'Bypass Sends of All Visible Channels':
        'Bypass Send của tất cả Channel đang hiện',
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
    if re.search(r'\b(Inserts|Sends)\b', v):
        problems.append(f'con so nhieu: {k[:40]!r} -> {v!r}')

# Phan biet HAI loai chuoi, va do la ly do giu so nhieu van dung o noi nao:
#   - NHAN PANEL / tieu de muc  -> giu so nhieu
#       `Inserts` -> `Inserts`, `Inserts (Control Room)` -> giu,
#       `Sends` -> `Sends`, `Sends (Pre-Fader)` -> giu,
#       `Expand: Inserts` -> `Mở rộng: Inserts`, `Views: Inserts` -> giu
#   - HANH DONG / TRANG THAI   -> bo so nhieu
#       `Inserts Bypass` -> `Bypass Insert`, `Inserts Reset` -> `Đặt lại Insert`,
#       `Inserts State (...)` -> `Trạng thái Insert`, `Inserts [short]` -> `Insert`,
#       `Sends Bypass` -> `Bypass Send`, `Sends Reset` -> `Đặt lại Send`
#       `Sends [short]` -> `Send`, `Sends State (...)` -> `Trạng thái Send`
# => phai kiem CHI nhanh "Bypass ...", khong kiem ca ban dich.

# Bang chung QUYET DINH: 10 chuoi danh tu so it, 0 giu so nhieu.
# Bang chung quyet dinh lay tu CHINH cac chuoi hanh dong, 10 chuoi, 0 giu
# so nhieu. KHONG lay tu nhan panel (nhan panel giu so nhieu la dung).
NOUN_SG = [('Insert', 'Insert'), ('Modulator', 'Modulator'), ('Send', 'Send'),
           ('EQ', 'EQ')]
n_ev = 0
for w, sg in NOUN_SG:
    # phai giu ca hai dang: "Bypass X" va "Bypass: X". Chi loc 'Bypass '
    # thi bo mat 4 chuoi co dau hai cham.
    keys = [k for k in vi if re.match(r'^Bypass[: ]', k)
            and re.search(rf'\b{w}s\b', k)]
    if len(keys) < 3:
        problems.append(f'"{w}s" sau "Bypass ": chi {len(keys)} chuoi - '
                        'bang chung qua yeu')
    for k in keys:
        if k in real:
            continue          # hai chuoi dang sua, khong tinh la anh em
        n_ev += 1
        if re.search(rf'\b{w}s\b', vi[k]):
            problems.append(f'anh em giu so nhieu "{w}s": {k!r} -> {vi[k]!r}')
if n_ev < 8:
    problems.append(f'chi thay {n_ev} chuoi "Bypass ...s" lam bang chung, '
                    'mong doi >= 8')

# Phai ton tai ca hai loai chuoi, va loai giu so nhieu phai CON nguyen
for k, must in [('Inserts', 'Inserts'),
                ('Inserts (Control Room)', 'Inserts'),
                ('Sends (Pre-Fader)', 'Sends'),
                ('Expand: Inserts', 'Inserts'),
                ('Inserts [short]', 'Insert'),
                ('Sends [short]', 'Send'),
                ('Inserts Reset', 'Đặt lại Insert'),
                ('Sends State (Bypass Sends with click... )', None)]:
    if must is None:
        continue
    if k not in vi:
        problems.append(f'khong thay {k!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k!r} khong chua {must!r}')

# Giu nguyen: hai khoa khac nhau cung nghia, va 3 chuoi trong cung hang
# dang BANG SAI phai duoc sua
SIBLINGS = [
    ('Bypass Channel Strip of All Visible Channels',
     'Bypass Channel Strip mọi Channel đang hiện'),   # da dung
    ('Bypass EQs of All Visible Channels',
     'Bypass EQ của tất cả Channel đang hiện'),       # da dung
    ('Bypass Modulators of All Visible Channels',
     'Bypass Modulator của tất cả Channel đang hiện'),  # da dung
    ('Bypass Inserts', 'Bypass Insert'),               # hai khoa, mot nghia
    ('Bypass Sends', 'Bypass Send'),
    ('Bypass: Inserts', 'Bypass: Insert'),
    ('Bypass: Sends', 'Bypass: Send'),
    ('Bypass Insert', 'Bypass Insert'),
    ('Bypass Modulators', 'Bypass Modulator'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)
left = {k: v for k, v in after.items()
        if re.match(r'^Bypass[: ]', k)
        and re.search(r'\b(Inserts|Sends|Modulators|EQs)\b', v)}
if left:
    problems.append(f'chuoi "Bypass ..." con so nhieu: {left}')
# va nhan panel phai van con so nhieu
keep = [k for k in ('Inserts', 'Sends', 'Inserts (Control Room)')
        if 'Inserts' in after[k] or 'Sends' in after[k]]
if len(keep) != 3:
    problems.append(f'phep thu yeu: nhan panel giu so nhieu con {len(keep)}/3')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[buc chung] {n_ev} chuoi "Bypass ...s" lam bang chung, 0 giu so nhieu')
print()
for k, v in changed.items():
    print(f'  {k[:44]!r}')
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
