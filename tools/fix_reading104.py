#!/usr/bin/env python3
r"""Vòng 104: 72 chuỗi, #1121-1192. Đọc tuần tự, không lọc.

Hai lỗi.

1. `Background Color` -> `Màu **Background**`

   Nhóm Background có 9 chuỗi: **8** dùng "nền", đúng **1** giữ tiếng Anh, và
   đó là chỗ này:
       `Background`                  -> `Hình nền`
       `Background[Picture or situation]` -> `Hình nền`
       `Backgrounds`                 -> `Hình nền`
       `Background Color Modulation` -> `Modulation màu nền`
       `Background Texture`          -> `Vân nền`
       `To Background`               -> `Về nền`
       `Select Track on Background Click` -> `Chọn Track khi nhấp vào nền`
       `Release Driver when Application is in Background` -> `... chạy nền`

2. `Activate Automation Passes` -> `Bật **Automation Passes**`

   Nhóm có đúng ba chuỗi, và **hai** đã dùng "lượt" - trong đó có khoá trần:
       `Automation Pass` -> `Lượt Automation`
       `Use Undo Branches for Edit History and Automation Passes`
           -> `... và **lượt** Automation`
       `Activate Automation Passes` -> `Bật Automation Passes`   <- lạc

   Khoá trần đã định nghĩa thuật ngữ là "lượt Automation", nên chuỗi ghép
   phải theo. Và bỏ số nhiều "Passes" theo đúng luật đợt 101.

**Không sửa, đã kiểm:** nhóm `BWF` có **hai** kiểu cấu trúc, và cả hai đúng:

    BWF Loudness Range  -> `Vùng BWF Loudness`        (giữ BWF tại chỗ)
    BWF Max. True Peak Level -> `Mức True Peak tối đa của BWF`  (BWF chuyển cuối)

Khi không có gì chen giữa thì "BWF" dính liền danh từ; khi có "Max." chen
vào thì phải chuyển "BWF" ra sau bằng "của". Không phải lệch. Nhóm này còn có
hai bộ khoá song song — `BWF Max Momentary...` (không dấu chấm) và
`BWF Max. Momentary...` (có dấu chấm) — 6 chuỗi, cùng một cách dịch.

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
    'Background Color': 'Màu nền',
    'Activate Automation Passes': 'Bật lượt Automation',
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

# 1. Phe "nen" cua nhom Background phai la da so
bg = [k for k in vi if re.search(r'\bBackgrounds?\b', k)]
if len(bg) < 8:
    problems.append(f'gia dinh Background chi {len(bg)} chuoi - mong doi >= 8')
n_vi = sum(1 for k in bg if 'nền' in vi[k].lower())
n_en = sum(1 for k in bg if 'Background' in vi[k])
if n_vi < 7:
    problems.append(f'chi {n_vi} gia tri dung "nen" truoc khi sua - khong du '
                    'bang chung')

# 2. Phe "luot" cua nhom Automation Pass
ap = [k for k in vi if re.search(r'Automation Pass', k, re.I)]
if len(ap) != 3:
    problems.append(f'gia dinh "Automation Pass" co {len(ap)} chuoi, mong doi 3')
# KHONG phan biet hoa/thuong: 'Luot' hoa o dau gia tri khong khop
# chuoi 'luot' thuong. Day la lan thu tu pho thu phan biet hoa thuong
# lam FAIL (vong 95 la lan dau).
n_luot = sum(1 for k in ap if 'lượt' in vi[k].lower())
if n_luot != 2:
    problems.append(f'truoc khi sua co {n_luot} gia tri dung "luot", vong nay '
                    'sua 1 - so lieu khong khop')

SIBLINGS = [
    ('Background', 'Hình nền'),                       # 1: khoa tran
    ('Backgrounds', 'Hình nền'),
    ('Background Color Modulation', 'màu nền'),
    ('Background Texture', 'Vân nền'),
    ('To Background', 'Về nền'),
    ('Automation Pass', 'Lượt Automation'),           # 2: khoa tran
    ('Use Undo Branches for Edit History and Automation Passes', 'lượt'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:52]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

left_bg = [k for k, v in after.items()
           if re.search(r'Background', k) and 'Background' in v]
if left_bg:
    problems.append(f'con giu "Background" trong gia tri cua chinh nhom nen: '
                    f'{left_bg}')
left_ap = [k for k, v in after.items()
           if re.search(r'Automation Pass', k, re.I)
           and 'lượt' not in v.lower()]
if left_ap:
    problems.append(f'con giu "Automation Passes": {left_ap}')

# Nhom BWF phai giu nguyen ca hai kieu cau truc (chua quyet)
bwf = [k for k in vi if k.startswith('BWF')]
if len(bwf) != 11:
    problems.append(f'phep thu yeu: nhom BWF co {len(bwf)} chuoi, mong doi 11')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khoa viet tay : {len(real)}')
print(f'can doi      : {len(changed)}')
print(f'[doi chieu] Background: {len(bg)} chuoi, trc {n_vi} nen / {n_en} '
      'tieng Anh -> het tieng Anh')
print(f'[doi chieu] Automation Pass: {len(ap)} chuoi, het so nhieu, het tieng Anh')
print(f'[ghi nhan] BWF: {len(bwf)} chuoi, hai kieu cau truc deu dung - de nguyen')
print()
for k, v in changed.items():
    print(f'  {k[:38]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
