#!/usr/bin/env python3
"""Round 28 of reading: the N-P block, the second gap.

Slices 3660 and 3760, 200 labels. Two whole families left in English.

THE "Not ..." FAMILY, which is the mirror image of the "No ..." family from
round 19 and just as large:

    "Not Automated"  -> "Khong Automated"
    "Not Connected"  -> "Khong Da ket noi"
    "Not Empty"      -> "Khong Trong"
    "Not Loaded"     -> "Khong Loaded"
    "Not Valid"      -> "Khong Valid"
    "Not available"  -> "Khong available"
    "Not found"      -> "Khong found"

Seven labels, seven of them saying "Khong" and then leaving the whole word in
English. "Khong Valid" is not Vietnamese in any reading.

THE "Number of ..." FAMILY - seventeen keys, all of them "So cua <English>":

    "Number of Channels" -> "So cua Channels"
    "Number of Clicks"   -> "So cua Clicks"
    "Number of Columns"  -> "So cua Columns"
    "Number of Rows"     -> "So cua Rows"
    "Number of Steps"    -> "So cua Steps"
    "Number of Voices"   -> "So cua Voices"
    "Number of Pads"     -> "So cua Pads"
    "Number of New Tracks" -> "So cua Track New"
    "Number of steps follows Step Resolution"
                          -> "So cua steps follows Step Resolution"

  "So cua" is a word-for-word rendering of "number of". Vietnamese says "So
  Channel", "So Click", "So cot" - the noun goes straight after the number with
  no genitive. And two of the seventeen had also translated the noun while
  keeping the English, so they read "So luong buoc" where the sense is "So
  buoc".

And "Notepad" said "Ghi chu" in one key and "Notepad" in the two next to it;
"Notate as Single Notes" said "Notate nhu Note Single", which is both
untranslated and reversed.

  python tools/fix_reading28.py
  python tools/fix_reading28.py --write
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
    # the "Not ..." family
    # ==================================================================
    'Not Automated': 'Không Automation',
    'Not Connected': 'Chưa kết nối',
    'Not Empty': 'Không trống',
    'Not Loaded': 'Chưa nạp',
    'Not Valid': 'Không hợp lệ',
    'Not available': 'Không khả dụng',
    'Not found': 'Không tìm thấy',
    'Not set': 'Chưa đặt',
    'Not Set': 'Chưa đặt',
    'Not supported by hardware': 'Phần cứng không hỗ trợ',
    'Not a valid plug-in': 'Không phải là một Plug-in hợp lệ',
    'Not all files could be deleted!': 'Không thể xóa tất cả file!',
    'Not enough permissions to unlock this track':
        'Không đủ quyền để mở khóa Track này',
    'Not enough space for additional controller lane':
        'Không đủ chỗ cho thêm một Controller Lane',
    'Not enough space for all used controllers':
        'Không đủ chỗ cho tất cả Controller đang dùng',
    'Not enough space for velocity lane': 'Không đủ chỗ cho Velocity Lane',
    'Not enough space on disk': 'Không đủ dung lượng trống trên đĩa',
    'Not stable (plug-in crashed)': 'Không ổn định (Plug-in bị sự cố)',

    # ==================================================================
    # the "Number of ..." family - "So cua X" is not Vietnamese
    # ==================================================================
    'Number Of Bits': 'Số bit',
    'Number of Bars in Count-In': 'Số Bar trong phần đếm nhịp',
    'Number of Basic Colors': 'Số màu cơ bản',
    'Number of Channels': 'Số Channel',
    'Number of Clicks': 'Số Click',
    'Number of Color Tints': 'Số tông màu',
    'Number of Columns': 'Số cột',
    'Number of Lines Equal to the Duration of the Secondary Group':
        'Số dòng bằng thời lượng của nhóm phụ',
    'Number of New Tracks': 'Số Track mới',
    'Number of Pads': 'Số Pad',
    'Number of Rows': 'Số hàng',
    'Number of Sections': 'Số phần',
    'Number of Steps': 'Số Step',
    'Number of Suggestions': 'Số gợi ý',
    'Number of Visible Tracks': 'Số Track đang hiện',
    'Number of Voices': 'Số bè',
    'Number of controlled Channels': 'Số Channel được điều khiển',
    'Number of steps follows Step Resolution': 'Số Step theo Step Resolution',
    'Number of steps used for shape': 'Số Step dùng cho hình dạng',
    'Number of used MIDI Channels': 'Số MIDI Channel đã dùng',

    # ==================================================================
    # "Notate"/"Notepad" untranslated, and reversed
    # ==================================================================
    'Notate as Single Notes': 'Ký âm thành Note đơn',
    'Notehead: Reset to Default Notehead':
        'Đầu nốt: Đặt lại về Đầu nốt mặc định',
    'Noteheads': 'Các đầu nốt',
    'Notepad': 'Notepad',
    'Notepad Data...': 'Dữ liệu Notepad...',
    'Notes': 'Các Note',
    'Notes Length': 'Độ dài Note',
    'Notes Out of Range': 'Các Note ngoài phạm vi',
    'Notes and Continuous Pitchbend Data':
        'Note và dữ liệu Pitchbend liên tục',
    'Notes and NoteExp Pitchbend Curve':
        'Đường cong Pitchbend của Note và NoteExp',
    'Notes and Static Pitchbend Data': 'Note và dữ liệu Pitchbend tĩnh',
    'Notes Following Grace Notes That Introduce an Accidental':
        'Nốt sau Nốt Grace có dấu hóa',
    'Notes Following Trills That Introduce an Accidental':
        'Nốt sau Trill có dấu hóa',
    'Notes Following a Cue That Introduces an Accidental':
        'Nốt sau Cue có dấu hóa',
    'Nothing to commit.': 'Không có gì để commit.',

    # ==================================================================
    # "On Events" / "Off Events" reversed
    # ==================================================================
    'Off Events': 'Tắt Event',
    'On Events': 'Bật Event',
    'OMF Result': 'Kết quả OMF',
    'Octave Line': 'Vạch Octave',
    'Octave Symbol': 'Ký hiệu Octave',
    'Octaves': 'Các Octave',
    'Octave Offset from C3': 'Lệch Octave tính từ C3',
    'Object Selection Tool': 'Công cụ chọn đối tượng',
    'Objects': 'Các đối tượng',
    'Nuendo Output Offset': 'Độ lệch đầu ra Nuendo',
    'Nuendo ASIO Output': 'Đầu ra ASIO của Nuendo',
    'Nudge Selected Steps': 'Nhích các Step đã chọn',
    'Nudge Steps Left': 'Nhích các Step sang trái',
    'Nudge Steps Right': 'Nhích các Step sang phải',
    'Nudge Notes': 'Nhích các Note',
    'Nudge Settings': 'Cài đặt Nudge',
    'Nudge Step Lane': 'Nhích Step Lane',
    'Offset Samples': 'Offset các Sample',
    'Old-Style Diamond Noteheads': 'Đầu nốt hình thoi kiểu cũ',
    'Only External Projects': 'Chỉ Project External',
    'One Row': 'Một hàng',
    'One track': 'Một Track',
    'One-Shot Mode': 'Chế độ One-Shot',
    'One of': 'Một trong số',
    'On Leaving Trim Mode': 'Khi rời khỏi chế độ Trim',
    'On Mouse Over': 'Khi di chuột qua',
    'On Pass End': 'Khi kết thúc lượt xử lý',
    'On Position Change': 'Khi đổi vị trí',

    # ==================================================================
    # the "Open ..." family - twenty-odd keys, half reversed, half with
    # the object left in English
    # ==================================================================
    'Open About Box...': 'Mở hộp Giới thiệu...',
    'Open Editor Commands open Editors in Lower Zone':
        'Lệnh Open Editor mở các Editor trong Lower Zone',
    'Open Editor for Common Reverb Settings':
        'Mở Editor cho cài đặt Common Reverb',
    'Open Effect Editor after Loading it': 'Mở Effect Editor sau khi tải',
    'Open Engraving Settings': 'Mở cài đặt Engraving',
    'Open Font Styles': 'Mở kiểu phông chữ',
    'Open Help...': 'Mở trợ giúp...',
    'Open Library': 'Mở thư viện',
    'Open Library...': 'Mở thư viện...',
    'Open Markers': 'Mở các Marker',
    'Open Metronome Setup': 'Mở thiết lập Metronome',
    'Open Modulators in Lower Zone': 'Mở các Modulator trong Lower Zone',
    'Open Other...': 'Mở mục khác...',
    'Open Paragraph Styles': 'Mở kiểu đoạn văn',
    'Open Pattern Editor in Lower Zone': 'Mở Pattern Editor trong Lower Zone',
    'Open Plug-in Editor': 'Mở Plug-in Editor',
    'Open Plug-in Editors': 'Mở các Plug-in Editor',
    'Open Plug-in Manager': 'Mở trình quản lý Plug-in',
    'Open Project Logical Editor': 'Mở Logical Editor của Project',
    'Open Project Logical Editor...': 'Mở Logical Editor của Project...',
    'Open Projects in Last Used View':
        'Mở các Project theo chế độ xem dùng gần nhất',
    'Offline Edits': 'Chỉnh sửa Offline',
    'Offbeat Correction': 'Hiệu chỉnh nghịch phách',
    'On-Screen Keyboard': 'Bàn phím ảo trên màn hình',
    'On-Screen Keyboard...': 'Bàn phím ảo trên màn hình...',
    'On/Off': 'Bật/Tắt',
    'Offset (Ticks)': 'Offset (Tick)',
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
       or '�' in v or not v.strip()]
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
