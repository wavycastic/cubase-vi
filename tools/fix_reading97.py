#!/usr/bin/env python3
r"""Vòng 97: 78 chuỗi, #601-678. Đọc tuần tự, không lọc.

Ba lỗi.

1. `Add to Project 'Group' Folder` -> `Thêm vào thư mục '**Nhóm**' của Project`

   Có ba chuỗi anh em, cách nhau vài dòng:

       Add to Project 'FX' Folder    -> thư mục '**FX**'
       Add to Project 'Group' Folder -> thư mục '**Nhóm**'     <- lạc
       Add to Project 'VCA' Folder   -> thư mục '**VCA**'

   Tên trong dấu nháy kép là **tên thư mục hiện trên màn hình**, không phải
   mô tả. Người dùng phải nhìn thấy đúng chữ trong Project window thì mới tìm
   được. Dịch nó thành "Nhóm" là chặn người dùng vào đúng chỗ.

2. `Add-on Sound Slot` -> `Sound Slot **mở rộng**`

   "mở rộng" là "extension", không phải "Add-on". Cả nhóm giữ "Add-on":
   `Add (Add-on)` -> `Thêm (Add-on)`,
   `Add Sound Slot (Add-on)` -> `Thêm Sound Slot (Add-on)`,
   `MIDI Modifiers (Not for Add-ons)` -> `... (không dùng cho Add-on)`.
   Riêng chuỗi này dịch, và dịch sang nghĩa khác.

3. `Selects Algorithm Preset` -> `Chọn Preset **thuật toán**`

   Nhóm `Algorithm` tách theo nghĩa, và cái tách đó **đúng**:

   * đứng một mình là khái niệm -> dịch
     `Algorithm` -> `Thuật toán`, `Warping Algorithm` -> `Thuật toán Warping`,
     `Algorithm Settings` -> `Cài đặt thuật toán`

   * nằm trong tên một tính năng Cubase -> giữ tiếng Anh
     `Set Algorithm` -> `Đặt Algorithm`,
     `Set Algorithm Preset` -> `Đặt Preset Algorithm`,
     `Change Stretch Algorithm` -> `Đổi Stretch Algorithm`,
     `Real Time Algorithm...` -> giữ,
     `Algorithm Preset` -> `Algorithm Preset`

   Nhưng **ba chuỗi cùng nói "Algorithm Preset" thì hai giữ, một dịch**:
   `Algorithm Preset` -> giữ, `Set Algorithm Preset` -> giữ,
   `Selects Algorithm Preset` -> dịch. Cái thứ ba lạc. Sửa theo đa số của
   chính nó: hai anh em giữ, nó giữ.

**Không sửa, đã kiểm:** `After stopping, how many milliseconds before system
can be restarted` không có dấu hỏi ở **cả tiếng Anh lẫn tiếng Việt**, nên
không phải dấu hỏi bị rơi. `Aeolian (nat. minor)` -> `Aeolian (thứ sáu tự
nhiên)` đúng - thứ sáu tự nhiên là tên tiếng Việt của natural minor.

  python tools/fix_reading97.py
  python tools/fix_reading97.py --write
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
    "Add to Project 'Group' Folder": "Thêm vào thư mục 'Group' của Project",
    'Add-on Sound Slot': 'Add-on Sound Slot',
    'Selects Algorithm Preset': 'Chọn Algorithm Preset',
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
    # trích dẫn trong nguồn phải giữ nguyên trong giá trị
    for q in re.findall(r"'([^']*)'", src[k]):
        if q not in v:
            problems.append(f'mất trích dẫn {q!r} trong {k[:44]!r}')

SIBLINGS = [
    ("Add to Project 'FX' Folder", "'FX'"),          # 1
    ("Add to Project 'VCA' Folder", "'VCA'"),
    ('Add (Add-on)', 'Add-on'),                      # 2
    ('Add Sound Slot (Add-on)', 'Add-on'),
    ('MIDI Modifiers (Not for Add-ons)', 'Add-on'),
    ('Algorithm Preset', 'Algorithm Preset'),         # 3
    ('Set Algorithm Preset', 'Preset Algorithm'),
    # nhóm Algorithm tách theo nghĩa - phần "giữ tiếng Anh" phải giữ nguyên
    ('Set Algorithm', 'Đặt Algorithm'),
    ('Change Stretch Algorithm', 'Stretch Algorithm'),
    # phần "dịch" cũng phải giữ nguyên
    ('Algorithm', 'Thuật toán'),
    ('Algorithm Settings', 'thuật toán'),
    ('Warping Algorithm', 'Thuật toán Warping'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k[:40]!r} không chứa {must!r}')

# Sau khi sửa, mọi giá trị vừa có "Algorithm" vừa có "Preset" phải giữ
# "Algorithm" bằng tiếng Anh. Không so theo chuỗi "Algorithm Preset" nguyên
# văn, vì "Set Algorithm Preset" dịch ra "Đặt Preset Algorithm" - cùng thuật
# ngữ, chỉ đảo trật tự theo tiếng Việt.
after = dict(vi)
after.update(real)
ap = {k: v for k, v in after.items()
      if 'Algorithm' in v and 'Preset' in v}
odd = {k: v for k, v in ap.items() if 'thuật toán' in v}
if odd:
    problems.append(f'"Algorithm" trong cụm "...Preset" vẫn bị dịch: {odd}')
if len(ap) < 3:
    problems.append(f'phép thử yếu: chỉ thấy {len(ap)} chuỗi, mong đợi 3')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] {len(ap)} giá trị có cả "Algorithm" và "Preset", '
      'tất cả giữ "Algorithm" bằng tiếng Anh')
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
