#!/usr/bin/env python3
r"""Vòng 107: 62 chuỗi, #1339-1400. Đọc tuần tự, không lọc.

Hai lỗi, cùng một cơ: **thêm chữ vào bản dịch mà nguồn không có.**

    CC: Breath  -> `CC: Breath **Controller**`
    CC: Foot    -> `CC: Foot **Controller**`

Nhóm `CC: ...` có **51** chuỗi. Bỏ `CC: %d` (không so sánh được), còn **50**:
**46** giữ nguyên phần sau dấu hai chấm, **4** đổi, và trong 4 cái đổi đó:

    `CC: Attack Time`  -> `CC: Thời gian Attack`   (dịch, đúng)
    `CC: Release Time` -> `CC: Thời gian Release`  (dịch, đúng)
    `CC: Breath`       -> `CC: Breath Controller`  <- thêm chữ
    `CC: Foot`         -> `CC: Foot Controller`    <- thêm chữ

Hai cái đầu là **dịch** — "Attack Time" thành "Thời gian Attack" là bản dịch
bình thường. Hai cái sau **không dịch gì cả**, chỉ chèn thêm một chữ để "cho
đầy đủ". Đó là lỗi: bản dịch phải nói đúng những gì nguồn nói, không thêm ý.

Và chữ "Controller" ấy không vô nghĩa — nó làm nhãn đúng nghĩa hơn, vì
`CC 11 (Expression)`, `CC: BankSelect MSB` bên cạnh đều là *tên* chức năng
điều khiển. Người dịch có lý do khi làm vậy. Nhưng 46 chuỗi còn lại đều không,
và giữ nghĩa đúng là đủ. Sửa hai chỗ.

**Phát hiện thêm từ chính lần tra này:** `CC: Breath LSB` -> `CC: Breath LSB`
giữ nguyên, tức chính trong nhóm đó đã có cách viết không thêm chữ. Nên không
phải quy ước của nhóm mà chỉ là hai chỗ lệch.

**Không sửa, đã kiểm:** `Byte Position 0 (LSB)` -> `Vị trí byte 0 (LSB)` dùng
"byte" thường, còn `Byte Offset` -> `Byte Offset` giữ hoa. Và `Byte` -> `Byte`,
`Bytes` -> `Bytes` giữ nguyên cả hai. Nhưng đây là **nhãn vùng soạn thảo**
(`Byte Offset`) và **tên trường dữ liệu** (`Byte Position 0`), chỗ thì phải khớp
tên trường. Bảng không cho biết `Byte Offset` hiện ở đâu, nên để.

Lưu ý về lỗi của detector: lần đầu nó báo 3 chuỗi "được thêm chữ", trong đó 2
là **dịch đúng** và 1 (`CC: %d`) không so sánh được. Chỉ khi tách riêng "dịch"
khỏi "thêm chữ", rồi loại `%d`, mới còn đúng 2. Detector phải so **phần sau
dấu hai chấm**, không so cả chuỗi.

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
    'CC: Breath': 'CC: Breath',
    'CC: Foot': 'CC: Foot',
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
    # 1. chinh cau hoi cua vong nay: phan sau dau hai cham phai giu nguyen
    if v[3:].strip() != k[3:].strip():
        problems.append(f'phan sau "CC:" khac nguon: {k!r} -> {v!r}')
    if 'Controller' in v:
        problems.append(f'con them "Controller": {k!r}')


def cc_survey(m):
    """Chia phan sau 'CC:' thanh giu nguyen / da doi."""
    same, diff = [], []
    for k, v in m.items():
        if not k.startswith('CC:'):
            continue
        tail = k[3:].strip()
        if not tail or '%' in tail:
            continue
        (same if v[3:].strip() == tail else diff).append(k)
    return same, diff


same, diff = cc_survey(vi)
if len(same) < 40:
    problems.append(f'phep thu yeu: chi {len(same)} chuoi "CC: ..." giu nguyen, '
                    'mong doi >= 40')

# Hai anh em DUNG khi dich, phai con nguyen - tinh ca trong 4 chuoi da doi
KEEP = [('CC: Attack Time', 'CC: Thời gian Attack'),
        ('CC: Release Time', 'CC: Thời gian Release'),
        # chinh trong nhom da co cach viet khong them chu
        ('CC: Breath LSB', 'CC: Breath LSB'),
        ('CC: Expression', 'CC: Expression'),
        ('CC: Balance', 'CC: Balance'),
        ('CC: %d', 'CC: %d')]
for k, must in KEEP:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k!r}')
    elif vi[k] != must:
        problems.append(f'gia dinh sai: {k!r} la {vi[k]!r}, mong doi {must!r}')

after = dict(vi)
after.update(real)
same_a, diff_a = cc_survey(after)
# DAI phai CON: 'Attack Time' / 'Release Time' dich dung. Khong duoc gan
# 'con chuoi khac nguon' cho hai cai do - chung DICH, khong phai THEM CHU.
allowed = {'CC: Attack Time', 'CC: Release Time'}
bad = [k for k in diff_a if k not in allowed]
if bad:
    problems.append(f'con chuoi "CC: ..." khac nguon: {bad}')
if set(diff_a) != allowed:
    problems.append(f'cac chuoi da doi kha khac: {sorted(set(diff_a) - allowed)}')
if len(same_a) != len(same) + len(real):
    problems.append(f'so lieu khong cong: {len(same)} + {len(real)} '
                    f'=? {len(same_a)}')

# "Byte Offset" giu hoa, "Byte Position ..." dung thuong - de nguyen
if vi.get('Byte Offset') != 'Byte Offset':
    problems.append('ngoai le "Byte Offset" bi dong - xem docstring')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] "CC: ...": {len(same) + len(diff)} chuoi so sanh duoc, '
      f'truoc {len(same)} giu nguyen / {len(diff)} doi -> het doi')
print()
for k, v in changed.items():
    print(f'  {k!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
