#!/usr/bin/env python3
"""Round 18 of reading: the L-M block of the general catch-all.

Six slices, 2860..3460, about 600 labels. Two classes dominate, and both are
the reverse of a mistake I have been fixing all along.

REVERSED, in the MIDI family this time. "MIDI" is a prefix, and the strings
that carry it kept it in front while the noun behind it was translated, so the
result reads as a Vietnamese noun with a stray acronym glued to its face:

    "MIDI Channels"        -> "Kenh MIDI"          (fine, actually)
    "MIDI Controller Scripts" -> "Script MIDI Controller"
    "MIDI Device Automation"   -> "Automation MIDI Device"
    "MIDI Files"           -> "File MIDI"
    "MIDI Hex Editor"      -> "Editor MIDI Hex"
    "MIDI In Activity"     -> "MIDI trong Activity"
    "MIDI In port for MIDI Timecode" -> "MIDI trong port cho MIDI Timecode"
    "MIDI Input"           -> "MIDI Dau vao"
    "MIDI Input Port"      -> "MIDI Dau vao Cong"
    "MIDI Input Ports"     -> "MIDI Dau vao Cong"
    "MIDI Inserts"         -> "Inserts MIDI"
    "MIDI Keyboard"        -> "MIDI Ban phim"
    "MIDI Clock Destinations" -> "Dich den MIDI Clock"
    "MIDI Clock Follows Project Position" -> "Vi tri MIDI Clock Follows Project"
    "MIDI Controller Surface Editor" -> "Trinh sua be mat MIDI Controller"
    "MIDI Device"          -> "Thiet bi MIDI"
    "MIDI Devices"         -> "Thiet bi MIDI"
    "MIDI Manager"         -> "Quan ly thiet bi MIDI"

  Note the last pair and the pair above them: "MIDI Controller" is left alone in
  eight keys and rendered "MIDI Controller" everywhere, but "MIDI Device",
  "MIDI Keyboard" and "MIDI Input" flip it. "Thiet bi MIDI" is the awkward
  reading - the acronym belongs in front in Vietglish, the way "MIDI Track"
  already does it correctly in several hundred keys.

COMPOUND SPLIT AGAIN, the round 17 class, one layer deeper:

    "Locked to \"%s\""       -> "Locked vao \"%s\""
    "Load previously saved Project?" -> "Tai previously saved Project?"
    "Limit Number of Attribute Filters" -> "So Limit cua Filter Attribute"
    "Lock multiple Hitpoints" -> "Khoa multiple Hitpoints"

  The last one is a Latin word left alone in a Vietnamese sentence, where
  "Nhieu" was needed. The second leaves an English adjective and verb in place
  of the whole phrase "luu truoc do".

  python tools/fix_reading18.py
  python tools/fix_reading18.py --write
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
    # "MIDI" is a MODIFIER, not a prefix. Vietnamese noun first, then
    # "MIDI" - the shape of "duong so 5", and what most of the map
    # already does. The defect was never where the acronym sits, it was
    # the REVERSAL: acronym at the front with the noun stranded behind it.
    #     "Script MIDI Controller" -> "MIDI Controller Script"
    #     "MIDI trong Activity"   -> "Hoat dong MIDI In"
    #     "MIDI Ban phim"         -> "Ban phim MIDI"
    #     "MIDI Dau vao Cong"     -> "Cong dau vao MIDI"
    # ==================================================================
    'MIDI Controller Scripts': 'MIDI Controller Script',
    'MIDI Controller Surface Editor': 'Trình sửa bề mặt MIDI Controller',
    'MIDI Device Manager': 'Quản lý thiết bị MIDI',
    'MIDI Device Manager...': 'Quản lý thiết bị MIDI...',
    'MIDI Device Automation': 'MIDI Device Automation',
    'MIDI Files': 'File MIDI',
    'MIDI Hex Editor': 'Trình sửa MIDI Hex',
    'MIDI In Activity': 'Hoạt động MIDI In',
    'MIDI In port for MIDI Timecode': 'Cổng MIDI In cho MIDI Timecode',
    'MIDI Inputs': 'Đầu vào MIDI',
    'MIDI Input Port': 'Cổng đầu vào MIDI',
    'MIDI Input Ports': 'Cổng đầu vào MIDI',
    'MIDI Inserts': 'Insert MIDI',
    'MIDI Keyboard': 'Bàn phím MIDI',
    'MIDI Clock Destinations': 'Đích đến MIDI Clock',
    'MIDI Clock Follows Project Position':
        'Vị trí Project mà MIDI Clock bám theo',
    'MIDI Controller No.': 'Số MIDI Controller',
    'MIDI Click': 'Click MIDI',
    'MIDI Click Settings': 'Cài đặt Click MIDI',
    'MIDI Channels': 'Kênh MIDI',
    'MIDI Ports': 'Cổng MIDI',
    'MIDI Sends': 'Send MIDI',
    'MIDI Tracks': 'Track MIDI',

    # ==================================================================
    # the "Listen" family, where Dim and Key were flipped in
    # ==================================================================
    'Listen Dim': 'Listen Dim',
    'Listen Dim Level': 'Mức Listen Dim',
    'Listen Key': 'Listen Key',
    'Listen Key Level': 'Mức Listen Key',
    'Listen Display': 'Hiển thị Listen',
    'Listen Enabled': 'Listen đã bật',
    'Listen Level': 'Mức Listen',
    'Listen Volume': 'Âm lượng Listen',
    'Listen for All Visible Channels On/Off':
        'Bật/Tắt Listen cho mọi Channel đang hiện',

    # ==================================================================
    # the "Link Group:" and "Load" families
    # ==================================================================
    'Link Group: Edit Link Group Settings':
        'Link Group: Sửa cài đặt Link Group',
    'Link Group: Next Link Group': 'Link Group: Link Group kế tiếp',
    'Link Group: Previous Link Group': 'Link Group: Link Group liền trước',
    'Link Channels': 'Link Channel',
    'Linked Channels': 'Linked Channel',
    'Link Selected Channels': 'Link Channel đã chọn',
    'Link Selected Channels...': 'Link Channel đã chọn...',
    'Link Sections to Configurations': 'Link Section vào Configuration',
    'Link MixConsoles': 'Link MixConsole',
    'Link Panners': 'Link Panner',
    'Link Word Clock Outputs': 'Link đầu ra Word Clock',
    'Link Playback to Chordtrack': 'Link Playback vào Chord Track',
    'Link Project and Lower Zone Cursors':
        'Link con trỏ Project và Lower Zone',
    'Linked Panner': 'Linked Panner',
    'Load All Mixer Settings': 'Tải toàn bộ cài đặt Mixer',
    'Load Chords & Players': 'Tải hợp âm & Player',
    'Load Chords Only': 'Chỉ tải hợp âm',
    'Load Chords from Preset': 'Tải hợp âm từ Preset',
    'Load Default': 'Tải mặc định',
    'Load Input Assignment': 'Tải phép gán Input',
    'Load Log Entry to Preview': 'Tải mục Log vào Preview',
    'Load Players Only': 'Chỉ tải Player',
    'Load Players from Preset': 'Tải Player từ Preset',
    'Load Preset': 'Tải Preset',
    'Load Preset Settings': 'Tải cài đặt Preset',
    'Load Preset...': 'Tải Preset...',
    'Load Selected Channels': 'Tải cài đặt Channel đã chọn',
    'Load Selected Channels...': 'Tải cài đặt Channel đã chọn...',
    'Load Strip Preset...': 'Tải Preset Strip...',
    'Load Track Preset': 'Tải Preset Track',
    'Load Track Preset...': 'Tải Preset Track...',
    'Load available update': 'Tải bản cập nhật khả dụng',
    'Load from MediaBay...': 'Tải từ MediaBay...',
    'Load next Program': 'Tải Program kế tiếp',
    'Load previous Program': 'Tải Program liền trước',
    'Load previously saved Project?': 'Tải Project đã lưu trước đó?',
    'Load...': 'Tải...',
    'Loading GUI Resources ...': 'Đang tải tài nguyên GUI...',

    # ==================================================================
    # English left in place of a phrase
    # ==================================================================
    'Locked to "%s"': 'Đã khóa vào "%s"',
    'Lock multiple Hitpoints': 'Khóa nhiều Hitpoint',
    'Limit Number of Attribute Filters': 'Số bộ lọc thuộc tính tối đa',
    'Live Events': 'Event trực tiếp',
    'Live Keys': 'Key trực tiếp',
    'Live Input': 'Input trực tiếp',
    'Lists all tracks with hitpoints': 'Liệt kê mọi Track có Hitpoint',
    'Load previously saved Project?': 'Tải Project đã lưu trước đó?',
    'Local Drives': 'Ổ đĩa cục bộ',
    'Local Harddisks': 'Ổ đĩa cứng cục bộ',
    'Locate Dropout Position in Project': 'Tới vị trí Dropout trong Project',
    'Locate Previous Event': 'Tới Event liền trước',
    'Locate Previous Hitpoint': 'Tới Hitpoint liền trước',
    'Locate Selection End': 'Tới cuối vùng chọn',
    'Locate Selection Start': 'Tới đầu vùng chọn',
    'Locate when Clicked in Empty Space': 'Định vị khi nhấp vào vùng trống',
    'Locators': 'Các Locator',
    'Locators to Selection': 'Đưa Locator về vùng chọn',
    'Lock Event Attributes': 'Khóa thuộc tính Event',
    'Lock Events': 'Khóa các Event',
    'Lock Frames': 'Khóa các Frame',
    'Lock Punch Points to Locators': 'Khóa Punch Point vào Locator',
    'Logical Presets': 'Logical Preset',
    'Logical Editor Presets': 'Preset Logical Editor',
    'Log Messages': 'Ghi nhật ký thông điệp',
    'Loudness: Enable': 'Loudness: Bật',
    'Loudness: Reset': 'Loudness: Đặt lại',
    'Loudness: Switch between LU and LUFS':
        'Loudness: Chuyển giữa LU và LUFS',
    'Loudness Integrated: %.1f LUFS': 'Loudness tích hợp: %.1f LUFS',
    'Lydic diminished': 'Lydic giảm',
    'Lyrics from Clipboard': 'Lời bài hát từ Clipboard',
    'M&E Track only': 'Chỉ Track M&E',
    'Lower Switch': 'Switch dưới',
    'Lower Switch:': 'Switch dưới:',
    'Lowest CC Value': 'Giá trị CC thấp nhất',
    'Lowest Pitch': 'Cao độ thấp nhất',
    'Lowest Velocity': 'Velocity thấp nhất',
    'Highest CC Value': 'Giá trị CC cao nhất',
    'Line 2 Display': 'Hiển thị dòng 2',
    'Line Width': 'Độ dày đường vẽ',
    'Light Magenta': 'Hồng cánh sen nhạt',
    'Loud': 'To',
    'Loops & Samples': 'Loop & Sample',
    'List Editor: Show/Hide Filters': 'List Editor: Hiện/Ẩn bộ lọc',

    # ==================================================================
    # case
    # ==================================================================
    'Lock Recording': 'Khóa Recording',
    'Lock/Unlock Track': 'Khóa/Mở khóa Track',
    'Low-Cut Filter Frequency': 'Tần số Low-Cut Filter',
    'Lower Limit': 'Giới hạn dưới',
    'Location Tree': 'Cây vị trí',
    'Lyricist': 'Người viết lời',
    'Load GM Preset "%s"...': 'Tải GM Preset "%s"...',
    'Load FX Chain Preset...': 'Tải Preset FX Chain...',
    'MIDI Display Resolution: 1/16 = ': 'Độ phân giải hiển thị MIDI: 1/16 = ',
    'MIDI In': 'MIDI In',
    'MIDI Output': 'Đầu ra MIDI',
    'MIDI Outputs': 'Đầu ra MIDI',
    'MIDI Control': 'MIDI Control',
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
