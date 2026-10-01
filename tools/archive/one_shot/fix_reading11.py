#!/usr/bin/env python3
"""Round 11 of reading: profiles, permissions and the network layer.

Small domain, and its defects are the leftovers of the automated pass:

  - "User X" with the English word first, which reads as nothing:
        "User Defined"  -> "Defined nguoi dung"
        "User abort"     -> "abort nguoi dung"

  - "User MIDI Strings" -> "Nguoi dung MIDI Day dan". Two errors: the word order,
    and "Strings" here is Cubase's MIDI Strings data, not guitar strings. "Day
    dan" would send an engineer looking for a violin.

  - "User Interface Scaling" -> "Ti le giao dien". "Ti le" is a ratio; scaling
    the interface is zooming it.

  - English left in place next to its translated twin:
        "network name"    -> "Ten network"
        "Users in Local Network" -> "Users trong Network cuc bo"
        "Save marked preferences only" -> "Chi Store marked preferences"
        "Progress of active network transfers:" -> "Progress cua active..."
        "Show User Presets Location..."  -> "Hien User Presets Location..."
        "Not Shared"      -> "Khong Shared"
        "On Processing Shared Clips" -> "Clip On Processing Shared"

  python tools/fix_reading11.py
  python tools/fix_reading11.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
PH = re.compile(r'%(?:(?:\.\d+)?[a-zA-Z%]|l)')

WORDING = {
    # ==================================================================
    # "User X" with the English word first
    # ==================================================================
    'User Defined': 'Do người dùng định nghĩa',
    'User abort': 'Người dùng hủy',
    'User Content': 'Nội dung người dùng',
    'User Library': 'Thư viện người dùng',
    'User Mapping': 'Mapping người dùng',
    'User Pattern': 'Pattern người dùng',
    'User Presets': 'Preset người dùng',
    'User Attributes': 'Thuộc tính người dùng',
    'User Commands': 'Lệnh người dùng',
    'User Description': 'Mô tả người dùng',
    'User Manager': 'Trình quản lý người dùng',
    'User Manager...': 'Trình quản lý người dùng...',
    'User Mode': 'Chế độ người dùng',
    'User Name': 'Tên người dùng',
    'User': 'Người dùng',

    # ==================================================================
    # wrong senses
    # ==================================================================
    # MIDI Strings is Cubase's string table, not guitar strings
    'User MIDI Strings': 'MIDI String của người dùng',
    'User-definable Frame Rate': 'Frame Rate do người dùng định nghĩa',
    'User Interface Scaling: Decrease': 'Thu phóng giao diện: Giảm',
    'User Interface Scaling: Increase': 'Thu phóng giao diện: Tăng',
    'Edit History Preferences': 'Tùy chọn Edit History',

    # ==================================================================
    # English left next to its translated twin
    # ==================================================================
    'network name': 'tên network',
    'Users in Local Network': 'Người dùng trong Network cục bộ',
    'Store marked preferences only': 'Chỉ lưu các tùy chọn đã đánh dấu',
    'Progress of active network transfers:':
        'Tiến trình các lần truyền qua mạng đang chạy:',
    'Show User Presets Location...':
        'Hiện vị trí lưu Preset người dùng...',
    'Not Shared': 'Chưa chia sẻ',
    'On Processing Shared Clips': 'Khi xử lý Clip đã chia sẻ',
    'Rename selected profile': 'Đổi tên Profile đã chọn',

    # ==================================================================
    # capitalisation and drift against a sibling
    # ==================================================================
    'Remove User Attribute': 'Gỡ bỏ thuộc tính người dùng',
    'Set up User Attributes': 'Thiết lập thuộc tính người dùng',
    'Set up Editor Preferences': 'Thiết lập tùy chọn Editor',
    'Open/Close Network Section': 'Mở/Đóng phần Network',
    'Network Drives': 'Các ổ đĩa mạng',
    'Permission Presets': 'Các Preset Permission',
    'Flatten (with Options & Preferences)':
        'Làm phẳng (với Tùy chọn & Tùy chọn)',
    '%d fps (User)': '%d fps (người dùng)',
    'Test Template': 'Mẫu kiểm tra',
    'Download the Network Project?': 'Tải Project mạng về?',
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:62]!r}\n   -> {v!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
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
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s)')
