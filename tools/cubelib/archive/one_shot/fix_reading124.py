#!/usr/bin/env python3
r"""Vòng 124: 85 chuỗi, #2831-2915 (kèm các anh em họ Root Note, Hitpoint và Score Editor Arpeggio). Đọc tuần tự, không lọc.

Mười bảy sửa đổi chia thành 5 nhóm lớn:

1. Đồng bộ bộ ba thông số điều khiển Dry/Wet:
   - `Dry mix` -> `Trộn Dry` (tr��ớc: `Dry mix` - sót tiếng Anh)
   Đối xứng 100% với hai anh em ruột:
       `Wet mix`     -> `Trộn Wet`
       `Dry/Wet mix` -> `Trộn Dry/Wet`

2. Sửa lỗi đảo ngược và sót từ cốt lõi trong `Edit Chord Event`:
   - `Edit Chord Event` -> `Sửa Chord Event` (trước: `Sửa Event hợp âm`)
   Khớp với toàn bộ 10 chuỗi khác trong phần mềm:
       `Chord Event`         -> `Chord Event`
       `Create Chord Events` -> `Tạo Chord Event`
       `Insert Chord Event`  -> `Chèn Chord Event`
       `Insert Chord Events` -> `Chèn Chord Event`

3. Chuẩn hóa gia đình `Root Note` (Note là 70 từ cốt lõi, AGENT.md §1):
   - `Duplicate the root note (one octave higher)`
       -> `Nhân bản Root Note (cao hơn 1 quãng tám)` (trước: `... nốt gốc...`)
   - `Add the root note (bass) to the voicing`
       -> `Thêm Root Note (bass) vào Voicing` (trước: `... nốt gốc...`)
   - `Root Note/Pitch` -> `Root Note/Pitch` (trước: `Nốt gốc/Pitch`)
   - `Root Notes` -> `Root Note` (trước: `Nốt gốc`, đồng thời bỏ số nhiều)
   - `Scales - All Shown with a C-Root Note`
       -> `Scale - Tất cả đều hiện với Root Note C` (trước: `... nốt gốc C`)
   Đồng bộ với: `Lowest Root Note` -> `Root Note thấp nhất`, `Select Root Note for Scale` -> `Chọn Root Note cho Scale`.

4. Bỏ số nhiều 's' và từ "các" thừa trong thao tác Hitpoint và Patch Bank:
   - `Edit Hitpoints`    -> `Sửa Hitpoint` (trước: `Sửa các Hitpoint`)
   - `Disable Hitpoints` -> `Tắt Hitpoint` (trước: `Tắt các Hitpoint`)
   - `Remove Hitpoints`  -> `Gỡ bỏ Hitpoint` (trước: `Gỡ bỏ các Hitpoint`)
   - `Hitpoints`         -> `Hitpoint` (trước: `Các Hitpoint`)
   - `Hitpoint Tracks`   -> `Track Hitpoint` (trước: `Các Track Hitpoint`)
   - `Edit Patch Banks`  -> `Sửa Patch Bank` (trước: `Sửa các Patch Bank`)

5. Cập nhật nhóm Score Editor: giữ nguyên thuật ngữ chuyên ngành ký âm (chỉ thị AGENT.md):
   - `Down Arpeggios` -> `Down Arpeggio`
   - `Up Arpeggios`   -> `Up Arpeggio`
   - `Appearance of Down Arpeggios` -> `Hình dạng của Down Arpeggio`
   - `Appearance of Up Arpeggios`   -> `Hình dạng của Up Arpeggio`

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
    # 1. Dry mix
    'Dry mix': 'Trộn Dry',

    # 2. Chord Event
    'Edit Chord Event': 'Sửa Chord Event',

    # 3. Root Note
    'Duplicate the root note (one octave higher)':
        'Nhân bản Root Note (cao hơn 1 quãng tám)',
    'Add the root note (bass) to the voicing':
        'Thêm Root Note (bass) vào Voicing',
    'Root Note/Pitch': 'Root Note/Pitch',
    'Root Notes': 'Root Note',
    'Scales - All Shown with a C-Root Note':
        'Scale - Tất cả đều hiện với Root Note C',

    # 4. Hitpoint & Patch Bank
    'Edit Hitpoints': 'Sửa Hitpoint',
    'Disable Hitpoints': 'Tắt Hitpoint',
    'Remove Hitpoints': 'Gỡ bỏ Hitpoint',
    'Hitpoints': 'Hitpoint',
    'Hitpoint Tracks': 'Track Hitpoint',
    'Edit Patch Banks': 'Sửa Patch Bank',

    # 5. Score Editor: chuyên ngành giữ nguyên
    'Down Arpeggios': 'Down Arpeggio',
    'Up Arpeggios': 'Up Arpeggio',
    'Appearance of Down Arpeggios': 'Hình dạng của Down Arpeggio',
    'Appearance of Up Arpeggios': 'Hình dạng của Up Arpeggio',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r}')
    if '%s' in src[k] and '%s' not in v:
        problems.append(f'missing %s in {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

SIBLINGS = [
    # 1. Dry/Wet
    ('Wet mix', 'Trộn Wet'),
    ('Dry/Wet mix', 'Trộn Dry/Wet'),
    # 2. Chord Event
    ('Chord Event', 'Chord Event'),
    ('Create Chord Events', 'Tạo Chord Event'),
    ('Insert Chord Event', 'Chèn Chord Event'),
    # 3. Root Note
    ('Lowest Root Note', 'Root Note thấp nhất'),
    ('Select Root Note for Scale', 'Chọn Root Note cho Scale'),
    # 4. Hitpoint
    ('Hitpoint', 'Hitpoint'),
    ('Hitpoint Edit', 'Sửa Hitpoint'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Dry mix khớp Trộn Dry
if after['Dry mix'] != 'Trộn Dry':
    problems.append(f'Dry mix sai: {after["Dry mix"]!r}')

# 2. Edit Chord Event không còn Event hợp âm
if 'Event hợp âm' in after['Edit Chord Event']:
    problems.append('Edit Chord Event van con Event hop am')
if after['Edit Chord Event'] != 'Sửa Chord Event':
    problems.append(f'Edit Chord Event sai: {after["Edit Chord Event"]!r}')

# 3. Toàn bộ họ Root Note không còn \"nốt gốc\"
for k in ('Duplicate the root note (one octave higher)',
          'Add the root note (bass) to the voicing',
          'Root Note/Pitch', 'Root Notes',
          'Scales - All Shown with a C-Root Note'):
    if 'nốt gốc' in after[k].lower():
        problems.append(f'{k!r} van con chu not goc: {after[k]!r}')

# 4. Hitpoint không còn \"các Hitpoint\"
for k in ('Edit Hitpoints', 'Disable Hitpoints', 'Remove Hitpoints', 'Hitpoints'):
    if 'các hitpoint' in after[k].lower():
        problems.append(f'{k!r} van con chu cac Hitpoint: {after[k]!r}')

# 5. Score Editor Arpeggio
if 'đi xuống' in after['Down Arpeggios'] or 'đi lên' in after['Up Arpeggios']:
    problems.append('Down/Up Arpeggios chua ve tieng Anh chuyen nganh')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Dry mix: \"Trộn Dry\", đồng bộ bộ ba Trộn Dry / Wet / Dry/Wet')
print(f'[đối chiếu] Chord Event: sửa lỗi trật tự ngược và từ cốt lõi')
print(f'[đối chiếu] Root Note: chuẩn hóa 100% họ từ, loại bỏ hoàn toàn \"nốt gốc\"')
print(f'[đối chiếu] Hitpoint & Patch Banks: bỏ số nhiều \"s\" và từ \"các\"')
print(f'[đối chiếu] Score Editor: giữ nguyên Down/Up Arpeggio theo chỉ đạo chuyên ngành')
print()
for k, v in changed.items():
    print(f'  {k[:42]!r}')
    cur = vi.get(k, '')
    print(f'      {cur!r}')
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
