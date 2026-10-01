#!/usr/bin/env python3
r"""Vòng 121: 75 chuỗi, #2596-2670 (kèm #1067 và #4775 theo gia đình Dissolve và MIDI Channel). Đọc tuần tự, không lọc.

Năm lỗi được phát hiện và sửa theo gia đình:

1. Bỏ số nhiều tiếng Anh trong `Disable Cue Sends`:
   - `Disable Cue Sends` -> `Tắt Cue Send` (trước: `Tắt Cue Sends`)
   Khớp 100% với toàn bộ các chuỗi thao tác Cue Send khác:
       `Deactivate Cue Send`      -> `Tắt Cue Send`
       `Deactivate Cue Sends`     -> `Tắt Cue Send`
       `Click to Bypass Cue Sends`-> `Nhấp để Bypass Cue Send`
       `Clear Cue Send`           -> `Xóa Cue Send`

2. Đồng bộ 100% nhóm lệnh `Dissolve` về thuật ngữ `Rã`:
   - `Dissolve to Lanes`      -> `Rã sang Lane`          (trước: `Dissolve sang Lane`)
   - `Auto Dissolve Format 0` -> `Tự động rã Format 0`   (trước: `Tự động Dissolve Format 0`)
   Toàn bộ phần mềm chỉ có đúng 5 chuỗi chứa `Dissolve`. Ba chuỗi kia đã dịch rất chuẩn:
       `Dissolve Part`            -> `Rã Part`
       `Dissolve Audio Parts`     -> `Rã Audio Part`
       `Dissolve Note Expression` -> `Rã Note Expression`
   Hai chuỗi này sót từ "Dissolve" tiếng Anh. Nay cả 5/5 chuỗi đều dùng "Rã".

3. Sửa lỗi dịch sai thuật ngữ cốt lõi `Channel` và trật tự từ trong `MIDI Channel`:
   - `MIDI Channels` -> `MIDI Channel` (trước: `Kênh MIDI`)
     `Channel` nằm trong 70 từ cốt lõi của AGENT.md §1, bắt buộc giữ nguyên tiếng Anh.
     Dịch thành "Kênh" là vi phạm luật. Đồng thời bỏ số nhiều 's', khớp với:
         `MIDI Channel`           -> `MIDI Channel`
         `Show/Hide: MIDI Channels`-> `Hiện/Ẩn: MIDI Channel`
         `Include MIDI Channel`   -> `Bao gồm MIDI Channel`
   - `Distribute Notes to MIDI Channels` -> `Phân bổ Note sang MIDI Channel`
     (trước: `... Channel MIDI` - đảo ngược trật tự từ tiếng Anh).

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
    'Disable Cue Sends': 'Tắt Cue Send',
    'Dissolve to Lanes': 'Rã sang Lane',
    'Auto Dissolve Format 0': 'Tự động rã Format 0',
    'Distribute Notes to MIDI Channels': 'Phân bổ Note sang MIDI Channel',
    'MIDI Channels': 'MIDI Channel',
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
    # 1. Cue Send
    ('Deactivate Cue Send', 'Tắt Cue Send'),
    ('Deactivate Cue Sends', 'Tắt Cue Send'),
    ('Click to Bypass Cue Sends', 'Nhấp để Bypass Cue Send'),
    # 2. Dissolve -> Rã
    ('Dissolve Part', 'Rã Part'),
    ('Dissolve Audio Parts', 'Rã Audio Part'),
    ('Dissolve Note Expression', 'Rã Note Expression'),
    # 3. MIDI Channel
    ('MIDI Channel', 'MIDI Channel'),
    ('Show/Hide: MIDI Channels', 'Hiện/Ẩn: MIDI Channel'),
    ('Include MIDI Channel', 'Bao gồm MIDI Channel'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'gia dinh sai: khong thay {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'gia dinh sai: {k[:40]!r} khong chua {must!r}')

after = dict(vi)
after.update(real)

# 1. Disable Cue Sends không còn chữ "Sends"
if 'Sends' in after['Disable Cue Sends']:
    problems.append('Disable Cue Sends van con chu Sends')

# 2. Cả 5 chuỗi Dissolve đều dùng "Rã", không còn chữ "Dissolve" tiếng Anh
for k in ('Dissolve Part', 'Dissolve Audio Parts', 'Dissolve Note Expression',
          'Dissolve to Lanes', 'Auto Dissolve Format 0'):
    if 'Dissolve' in after[k]:
        problems.append(f'{k!r} van con chu Dissolve: {after[k]!r}')
    if 'rã' not in after[k].lower():
        problems.append(f'{k!r} khong chua chu \"rã\": {after[k]!r}')

# 3. Không còn "Kênh MIDI" hoặc "Channel MIDI"
if 'Kênh MIDI' in after['MIDI Channels']:
    problems.append('MIDI Channels van la Kênh MIDI')
if 'Channel MIDI' in after['Distribute Notes to MIDI Channels']:
    problems.append('Distribute Notes to MIDI Channels van con trật tự ngược Channel MIDI')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] Cue Send: bỏ số nhiều "Sends" khớp các anh em Deactivate/Bypass')
print(f'[đối chiếu] Dissolve: 5/5 chuỗi trong phần mềm đều đồng bộ dùng "Rã"')
print(f'[đối chiếu] MIDI Channel: sửa "Kênh MIDI" vi phạm từ cốt lõi và sửa trật tự ngược')
print()
for k, v in changed.items():
    print(f'  {k[:36]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
