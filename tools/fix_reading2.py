#!/usr/bin/env python3
"""The last set found by reading: English word order left in place, and
adjectives that should have been translated.

Note the opposite check first: "T\u00ean Channel", "S\u1ed1 Note", "Ch\u1ebf \u0111\u1ed9 Value"
are correct - Vietnamese puts the noun first. Only the values where the
modifier stayed English are wrong.

  python tools/fix_reading2.py
  python tools/fix_reading2.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

WORDING = {
    # --- modifier still in English -----------------------------------------
    'Fixed Length': 'Độ dài cố định',
    'Full Name': 'Tên đầy đủ',
    'Family Name': 'Tên họ',
    'Initial Number': 'Số ban đầu',
    'Secondary Mode': 'Chế độ phụ',
    'Inside Range': 'Vùng bên trong',
    'Outside Range': 'Vùng bên ngoài',
    'Enter Name': 'Nhập tên',
    'Generate Name': 'Tạo tên',
    'Absolute Position': 'Vị trí tuyệt đối',
    'Relative Position': 'Vị trí tương đối',
    'Frame Count': 'Số Frame',
    'Insert Type': 'Loại chèn',
    'Insert Length': 'Chèn độ dài',
    'Clock Source': 'Nguồn Clock',
    'Close Threshold': 'Ngưỡng đóng',
    'Open Threshold': 'Ngưỡng mở',
    'Bank Assignment': 'Gán Bank',
    'Dissolve Part': 'Hòa tan Part',
    'In Record': 'Ghi In',
    'Default Destination': 'Đích đến mặc định',
    'Secondary Destination': 'Đích đến phụ',
    'Filter Target': 'Lọc Target',
    'Program Dependent': 'Phụ thuộc Program',
    'Time Dependent': 'Phụ thuộc thời gian',
    'Type Dependent': 'Phụ thuộc loại',
    'Include Envelopes': 'Bao gồm Envelope',
    'Exclude Envelopes': 'Loại trừ Envelope',
    'Include Fades': 'Bao gồm Fade',
    'Exclude Fades': 'Loại trừ Fade',
    'Include Volume': 'Bao gồm Volume',
    'Exclude Volume': 'Loại trừ Volume',
    'Include Pan': 'Bao gồm Pan',
    'Exclude Pan': 'Loại trừ Pan',
    'Include Mute': 'Bao gồm Mute',
    'Exclude Mute': 'Loại trừ Mute',
    'Normalize': 'Chuẩn hoá',
    'Reverse': 'Đảo ngược',
    'Random': 'Ngẫu nhiên',
    'Variance': 'Phương sai',
    'Standard Deviation': 'Độ lệch chuẩn',
    'Maximum': 'Lớn nhất',
    'Minimum': 'Nhỏ nhất',
    'Average': 'Trung bình',
    'Sum': 'Tổng',
    'Minimum Distance from Staff': 'Khoảng cách tối thiểu từ khuông nhạc',
    'Add Steps Randomly': 'Thêm Step ngẫu nhiên',
    'Auto Fades': 'Fade tự động',
    'Auto Fades - Project: %s': 'Fade tự động - Project: %s',
    'Auto Fades - Track: %s': 'Fade tự động - Track: %s',
    'CC: Main Volume': 'CC: Main Volume',
    'CC07 : Volume': 'CC07 : Volume',
    'CC07 : Volume LSB': 'CC07 : Volume LSB',
    'CC: Main Volume LSB': 'CC: Main Volume LSB',
    'CR Volume': 'CR Volume',
    'Channel Volume': 'Volume của Channel',
    'Audition Volume': 'Nghe thử Volume',
    'Choose Destination Mode': 'Chọn chế độ đích đến',
    'Apply Ref. Volume': 'Áp dụng Volume tham chiếu',
    'Apply MIDI Velocity Variance': 'Áp dụng phương sai Velocity MIDI',
    'Adjust Fades to Range': 'Căn Fade theo vùng',
    'Add Track To Selected: VCA Fader': 'Thêm Track vào mục đã chọn: VCA Fader',
}

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
from cubelib.placeholders import PLACEHOLDER  # one pattern; see cubelib/placeholders.py

real = {k: v for k, v in WORDING.items() if k in src}
print(f'defined : {len(WORDING)}   real keys : {len(real)}')
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'not in Cubase ({len(missing)}): {missing}')

bad = [(k, v) for k, v in real.items()
       if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v))
       or '\ufffd' in v]
if bad:
    print('PROBLEM:')
    for k, v in bad:
        print(f'  {k!r}: {v!r}')
    sys.exit(1)

changes = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'to change : {len(changes)}')
for k, v in changes.items():
    print(f'  {k!r}\n      {vi.get(k)!r}\n   -> {v!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changes.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s)')
