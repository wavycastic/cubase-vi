#!/usr/bin/env python3
"""Round 15 of reading: the D-E block of the general catch-all.

Six slices, 1560..1960, about 600 labels. This stretch turned out to be where
the automated passes left the most behind, and almost all of it is one thing:
a label that was translated word by word, in order, and never read.

    "Do you want to continue recording?" -> "Ban co muon continue recording khong?"
    "Do you want to copy video files too?" -> "... Sao chep video files too ...?"
    "Device failed to open!"               -> "Device failed vao open!"
    "Divide by 2"                          -> "Divide theo 2"
    "Delete later events"                  -> "Xoa later events"
    "Displays follow locating device"      -> "Thiet bi Displays follow locating"

Four of those read as pure English with a Vietnamese frame bolted on. None of
the auditors can see that, because each word it complains about is a word it
expects to find in English.

The reversed short label is the same family as round 13, and it is thick here:

    "Drop Chords"          -> "Hop am Drop"
    "Drop MIDI Part"       -> "Part Drop MIDI"
    "Drop Notes"           -> "Note Drop"
    "Don't Split Events"   -> "Event Don't Split"
    "Deselect All Source Tracks" -> "Track Deselect All Source"
    "Distribute Notes to MIDI Channels" -> "Note Distribute vao Channel MIDI"
    "Deleting Files..."    -> "File Deleting..."
    "Effect Tracks"        -> "Track Effect"
    "Enlarge Active Track" -> "Track Enlarge Active"
    "Enter Custom Name"    -> "Ten Enter Custom"

"Thiet bi Displays follow locating" is the worst of the set: the sentence has
been taken apart, and the part that is left is a Device being followed by two
English verbs, which says nothing.

Then the "Display" family, which had the adjective at the end in four keys
("Chiieu cao Display") while "Display Color" and "Display Name" said "hien thi"
- two different word orders for the same idea.

And a set of noun phrases that lost their head noun:

    "Date + Time" style cases aside, here:
    "Create New Chain"          -> "Tao Chain"        (round 14)
    "Enter Custom Name"         -> "Ten Enter Custom" (here)
    "Double-click opens Editor in Lower Zone"
                                 -> "Editor Double-click opens trong Lower Zone"
    "Enter Punch In Position"   -> "Nhap Punch trong Position"

"Ten Enter Custom" is worth stopping on: it is a field label, and reading it
gives "name enter custom" - the word the user has to type sits in the middle of
the phrase telling them what to type.

Three vocabularies split down the middle and were left split:

    Effect  -> "Hieu ung"   but  Effect Track / Effect Type / Effect Automation
                                / Add Effect / Bypass Effect all keep English
    Edit History -> "Lich su sua" but Edit History Preferences keeps English
    Drum Map / Drum Map Setup keep English, but Drum Map and Drum Maps
                                said "Trong Map"

  python tools/fix_reading15.py
  python tools/fix_reading15.py --write
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
    # a Vietnamese frame around an untranslated English clause
    # ==================================================================
    'Do you want to continue recording?': 'Bạn có muốn tiếp tục ghi không?',
    'Do you want to continue?': 'Bạn có muốn tiếp tục không?',
    'Do you want to copy video files too?':
        'Bạn có muốn sao chép cả file video không?',
    'Do you want to clear all key commands?':
        'Bạn có muốn xóa tất cả phím tắt không?',
    'Do you want to reset all key commands?':
        'Bạn có muốn đặt lại tất cả phím tắt không?',
    'Device failed to open!': 'Không thể mở Device!',
    'Divide by': 'Chia cho',
    'Divide by 2': 'Chia cho 2',
    'Divide Track List': 'Chia danh sách Track',
    'Delete later events': 'Xóa các Event phía sau',
    'Different tracks': 'Các Track khác nhau',
    'Displays follow locating device':
        'Hiển thị bám theo thiết bị định vị',
    'Displays Messages from Host Application':
        'Hiển thị thông điệp từ Host Application',
    'Displays Messages from SyncStation Device':
        'Hiện thông điệp từ thiết bị SyncStation',
    'Display only': 'Chỉ hiển thị',
    "Display 'B' as 'H'": "Hiển thị 'B' thành 'H'",
    "Display 'Bb' as 'B'": "Hiển thị 'Bb' thành 'B'",
    'Delete from Disk': 'Xóa khỏi đĩa',
    'Do Nothing': 'Không làm gì',
    'Drawing': 'Đang vẽ',
    'Editing': 'Đang sửa',
    'Detected': 'Đã phát hiện',
    'Detection': 'Phát hiện',
    'Detect Arpeggios': 'Phát hiện Arpeggio',
    'Detail search': 'Tìm kiếm chi tiết',
    'Denoise Required': 'Cần Denoise',
    'Drag Pattern to Project': 'Kéo Pattern vào Project',
    'Drop into project': 'Thả vào Project',
    'Drop processes here!': 'Thả Process vào đây!',
    'Encoding Scheme': 'Sơ đồ mã hóa',
    'Enter Company': 'Nhập công ty',
    'Enter Copyright': 'Nhập bản quyền',
    'Enter Lyricist': 'Nhập tác giả lời',
    'Domain': 'Miền',
    'Denominator': 'Mẫu số',
    'Diff.': 'Diff.',

    # ==================================================================
    # reversed
    # ==================================================================
    'Drop Chords': 'Thả hợp âm',
    'Drop MIDI Part': 'Thả MIDI Part',
    'Drop Notes': 'Thả Note',
    "Don't Split Events": 'Không tách Event',
    'Deselect All Source Tracks': 'Bỏ chọn tất cả Source Track',
    'Distribute Notes to MIDI Channels': 'Phân bổ Note sang Channel MIDI',
    'Deleting Files...': 'Đang xóa file...',
    'Effect Tracks': 'Các Effect Track',
    'Enlarge Active Track': 'Mở rộng Track đang hoạt động',
    'Enlarge Part': 'Mở rộng Part',
    'Enter Custom Name': 'Nhập tên tùy chỉnh',
    'Enter Model Name': 'Nhập tên model',
    'Enter Preset Name': 'Nhập tên Preset',
    'Editor History': 'Lịch sử chỉnh sửa',
    'Edit History': 'Lịch sử chỉnh sửa',
    'Edit History Preferences': 'Tùy chọn lịch sử chỉnh sửa',
    'Enter Punch In Position': 'Nhập vị trí Punch In',
    'Enter Punch Out Position': 'Nhập vị trí Punch Out',

    # ==================================================================
    # the Double/Display families: adjective at one end, noun at the other
    # ==================================================================
    'Double Length of Pattern': 'Gấp đôi độ dài của Pattern',
    'Double Size': 'Kích thước gấp đôi',
    'Double Speed Playback': 'Phát gấp đôi tốc độ',
    'Double Step Resolution of Pattern':
        'Gấp đôi độ phân giải Step của Pattern',
    'Double Step Resolution of Step Lane':
        'Gấp đôi độ phân giải Step của Step Lane',
    'Display Height': 'Chiều cao hiển thị',
    'Display Width': 'Chiều rộng hiển thị',
    'Display Mode': 'Chế độ hiển thị',
    'Display Options': 'Tùy chọn hiển thị',
    'Display Quantization': 'Hiển thị Quantize',
    'Editor Display Mode': 'Chế độ hiển thị của Editor',
    'Depth Focus': 'Tập trung độ sâu',
    'Distance of Notes': 'Khoảng cách của Note',
    'Disable/Enable Track': 'Tắt/Bật Track',
    "Disable 'Acoustic Feedback' during Playback":
        "Tắt 'Acoustic Feedback' khi phát",
    'Discard all changes to "%s"?': 'Bỏ tất cả thay đổi đối với "%s"?',

    # ==================================================================
    # three vocabularies that had split down the middle
    # ==================================================================
    'Effect': 'Effect',
    'Effects': 'Effects',
    'Effect Channels': 'Các Effect Channel',
    'Edit In-Place': 'Edit In-Place',
    'Edit Inplace': 'Edit In-Place',
    'Drum Map': 'Drum Map',
    'Drum Maps': 'Các Drum Map',
    'Drum Sound': 'Âm thanh Drum',
    'Drum Tracks': 'Các Drum Track',
    'Drum Channels': 'Các Drum Channel',
    'Edit Setting': 'Sửa cài đặt',
    'Edit Signature': 'Sửa số chỉ nhịp',
    'Edit Values': 'Sửa giá trị',
    'Edit Inserts': 'Sửa Insert',
    'Edit Link Group Settings': 'Sửa cài đặt Link Group',
    'Edit Link Group Settings...': 'Sửa cài đặt Link Group...',
    'Edit MIDI Preset': 'Sửa MIDI Preset',
    'Edit Patch Banks': 'Sửa các Patch Bank',
    'Edit Previous Parameter': 'Sửa tham số liền trước',
    'Edit Plug-in': 'Sửa Plug-in',
    'Dynamic Frame Offset': 'Dynamic Frame Offset',
    'Duplicate Version': 'Nhân bản Version',
    'Duplicate Notes to Multiple Voices': 'Nhân bản Note sang nhiều bè',
    'Duplicate Tracks': 'Nhân bản Track',
    'Dialogue-Gated Measurement': 'Đo theo đối thoại',
    'Direct Offline Processing': 'Direct Offline Processing',
    'Direct Offline Processing:': 'Direct Offline Processing:',
    'Download Selected Tracks': 'Tải các Track đã chọn',
    'Drop Frames': 'Thả các Frame',
    'Drop Out Frames': 'Frame bị rớt',
    'Dissolve to Lanes': 'Dissolve sang Lane',
    'Device Bank': 'Bank của thiết bị',
    'Device ID': 'ID thiết bị',
    'Device Node': 'Node thiết bị',
    'Device Online': 'Thiết bị trực tuyến',
    'Disable Source Tracks': 'Tắt Source Track',
    'Editors': 'Các Editor',
    'Encoder Preset': 'Encoder Preset',
    'Empty Map': 'Map trống',
    'Empty Bank': 'Bank trống',

    # ==================================================================
    # "Double-click ..." where the verb had been left in English
    # ==================================================================
    'Double-click opens Editor in Lower Zone':
        'Nhấp đúp để mở Editor trong Lower Zone',
    'Double-click to apply mapping': 'Nhấp đúp để áp dụng mapping',
    'Double-click to open Ambisonics Decoder':
        'Nhấp đúp để mở Ambisonics Decoder',
    'Double-click to open MixConvert': 'Nhấp đúp để mở MixConvert',
    'Double-click to rename Link Group': 'Nhấp đúp để đổi tên Link Group',

    # ==================================================================
    # case
    # ==================================================================
    'Enter Artist': 'Nhập nghệ sĩ',
    'Enter Composer': 'Nhập nhạc sĩ',
    'Enter Description': 'Nhập mô tả',
    'Enter Preset-Bank Name': 'Nhập tên Preset-Bank',
    'End Left': 'Kết thúc bên trái',
    'End Right': 'Kết thúc bên phải',
    'Do you want to save %s!?': 'Bạn có muốn lưu %s!?',
    'Do you want to delete this collection?':
        'Bạn có muốn xóa Collection này không?',
    'Drop Out Frames': 'Frame bị rớt',
    'Disable all Talkbacks': 'Tắt tất cả Talkback',
    'Disable Hitpoints': 'Tắt các Hitpoint',
    'Edit Hitpoints': 'Sửa các Hitpoint',
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
