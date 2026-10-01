#!/usr/bin/env python3
"""Round 20 of reading: the P block of the general catch-all.

Five slices, 3860..4260, about 500 labels. Two things, and the second one is a
mistake I made myself four rounds ago.

THE "Pre/Post" AND "Plug-in" FAMILIES had the tail before the head:

    "Open/Close Attribute Inspector" -> "Mo/Dong Inspector Attribute"
    "Patch Bank Editor"              -> "Editor Patch Bank"
    "Pedal Line"                     -> "Pedal Dong"
    "Pedal Symbol"                   -> "Pedal Ky hieu"
    "Peak Load"                      -> "Peak Tai"
    "Pitch Name Noteheads"           -> "Pitch Ten Dau noi"
    "Play-back Events"               -> "Event Playback"
    "Position & Related Tracks"      -> "Track Position & Related"
    "Preference Presets"             -> "Preset Preference"
    "Pre Filters"                    -> "Filter Pre"
    "Preparing Data..."              -> "Du lieu Preparing..."
    "Preserve Original Track"        -> "Track Preserve Original"
    "Preset Reference"               -> "Preset Tham chieu"
    "Overview Line"                  -> "Tong quan Dong"
    "Optimize Width"                 -> "Chieu rong Optimize"
    "Paint Events"                   -> "Event Paint"

  and one that had simply been taken apart:

    "Pattern Event / Track" -> "Track Pattern Event /"
    "Pre/Post MIDI Modifiers and Inserts" -> "Inserts Pre/Post MIDI Modifiers and"

  In both, the original has become a second string that happens to contain the
  same words.

"Out of memory" -> "Out cua memory" is the frame class from round 15 again, and
"Please fill in all mandatory entries" -> "Please fill trong all mandatory
entries" is worse - a Vietnamese preposition wedged into an English verb.

MY OWN MISTAKE, FOUR ROUNDS OLD. In round 14 I changed "Default Noteheads" to
"Dau noi mac dinh" and in round 15 "Hidden Noteheads" to "Cac dau noi dang an".
The map said "dau not" everywhere - some forty keys - and "dau noi" means a
joint or a terminal, not the head of a note. So I had introduced a second
spelling of Notehead while fixing something else. Caught here by noticing that
"Plus Noteheads" and "Muted Slash Noteheads" still said "dau not" and that
neither of my two was in the family. Reverted all four to "dau not".

  python tools/fix_reading20.py
  python tools/fix_reading20.py --write
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
    # "dau noi" was mine, from round 14 - the map says "dau not"
    # ==================================================================
    'Default Noteheads': 'Đầu nốt mặc định',
    'Hidden Noteheads': 'Các đầu nốt đang ẩn',
    'Muted Slash Noteheads': 'Đầu nốt gạch chéo bị tắt tiếng',
    'Oversized Slash Noteheads': 'Đầu nốt gạch chéo cỡ lớn',

    # ==================================================================
    # tail before head
    # ==================================================================
    'Open/Close Attribute Inspector': 'Mở/Đóng Attribute Inspector',
    'Open/Close Basics Section': 'Mở/Đóng phần Basics',
    'Open/Close Chords Section': 'Mở/Đóng phần Chords',
    'Open/Close Expression Map Section': 'Mở/Đóng phần Expression Map',
    'Open/Close MIDI Inserts Section': 'Mở/Đóng phần MIDI Inserts',
    'Open/Close MIDI Modifiers Section': 'Mở/Đóng phần MIDI Modifiers',
    'Open/Close MIDI Sends Section': 'Mở/Đóng phần MIDI Sends',
    'Open/Close Modulators Section': 'Mở/Đóng phần Modulators',
    'Open/Close Notepad Section': 'Mở/Đóng phần Notepad',
    'Open/Close Pre Section': 'Mở/Đóng phần Pre',
    'Open/Close Quick Controls Section': 'Mở/Đóng phần Quick Controls',
    'Open/Close Strip Section': 'Mở/Đóng phần Strip',
    'Open/Close Track Versions Section': 'Mở/Đóng phần Track Versions',
    'Open/Close VCA Section': 'Mở/Đóng phần VCA',
    'Open Sample Editor in Lower Zone': 'Mở Sample Editor trong Lower Zone',
    'Open in Lower Zone': 'Mở trong Lower Zone',
    'Open Setup Information': 'Mở thông tin thiết lập',
    'Open Synchronization Setup': 'Mở thiết lập Synchronization',
    'Organize Presets': 'Sắp xếp Preset',
    'Organize Presets...': 'Sắp xếp Preset...',
    'Optimize Width': 'Tối ưu chiều rộng',
    'Optimized Display': 'Hiển thị tối ưu',
    'Original Length': 'Độ dài gốc',
    'Original Length in Samples': 'Độ dài gốc tính bằng Sample',
    'Original Length in Seconds': 'Độ dài gốc tính bằng giây',
    'Original Pitch': 'Cao độ gốc',
    'Original Segment Pitch': 'Cao độ gốc của Segment',
    'Orig. Position': 'Vị trí gốc',
    'Origin Time': 'Thời gian gốc',
    'Other Tracks': 'Track khác',
    'Output Chain': 'Chain đầu ra',
    'Output Latency': 'Độ trễ đầu ra',
    'Output Port': 'Cổng đầu ra',
    'Output Port %d': 'Cổng đầu ra %d',
    'Output Ports': 'Các cổng đầu ra',
    'Output Mapping Event Mode': 'Chế độ Event cho Output Mapping',
    'Outside Prefetch Range': 'Ngoài vùng Prefetch',
    'Outside Range': 'Ngoài vùng',
    'Overview Line': 'Dòng tổng quan',
    'Part Display': 'Hiển thị Part',
    'Part Editing Mode': 'Chế độ sửa Part',
    'Parts Get Track Names': 'Part lấy tên Track',
    'Patch Bank Editor': 'Trình sửa Patch Bank',
    'Patch Banks': 'Các Patch Bank',
    'Pattern Event / Track': 'Pattern Event / Track',
    'Pattern Banks': 'Các Pattern Bank',
    'Patterns': 'Các Pattern',
    'Paint Events': 'Tô màu Event',
    'Parameter Details': 'Chi tiết tham số',
    'Parameter Input Assignment': 'Gán Input tham số',
    'Parameter Lane': 'Lane tham số',
    'Parameter Selection': 'Chọn tham số',
    'Parameter Value Count': 'Số giá trị tham số',
    'Passes: Select Previous Branch': 'Lượt xử lý: Chọn nhánh liền trước',
    'Paste %s Setting': 'Dán cài đặt %s',
    'Paste Color': 'Dán màu',
    'Paste Click Pattern to Selected Signatures':
        'Dán Click Pattern vào các Time Signature đã chọn',
    'Paste Settings to Selected Channels':
        'Dán cài đặt vào Channel đã chọn',
    'Path Options': 'Tùy chọn đường dẫn',
    'Peak Load': 'Tải đỉnh',
    'Peak Max.': 'Đỉnh tối đa',
    'Pedal Line': 'Vạch Pedal',
    'Pedal Lines': 'Các vạch Pedal',
    'Pedal Symbol': 'Ký hiệu Pedal',
    'Pitch Name Noteheads': 'Đầu nốt tên Pitch',
    'Pitch Shift Base': 'Gốc của Pitch Shift',
    'Pitch offset from section': 'Lệch Pitch so với phần',
    'Pitch Visibility On/Off': 'Bật/Tắt hiển thị Pitch',
    'Pitch Visibility: On/Off': 'Bật/Tắt hiển thị Pitch',
    'Pitch Visibility: Select Next Option':
        'Hiển thị Pitch: Chọn tùy chọn kế tiếp',
    'Playback Events': 'Playback Event',
    'Playback Technique': 'Playing Technique',
    'Playing Technique': 'Playing Technique',
    'Playing Techniques': 'Playing Techniques',
    'Placement Relative to Dynamics': 'Vị trí so với Dynamics',
    'Plain Chords': 'Hợp âm thuần',
    'Plain Font': 'Font thường',
    'Position & Related Tracks': 'Vị trí & Track liên quan',
    'Position Factor': 'Hệ số vị trí',
    'Position source': 'Nguồn vị trí',
    'Post-roll from Selection End': 'Post-roll từ cuối vùng chọn',
    'Post-roll from Selection Start': 'Post-roll từ đầu vùng chọn',
    'Pre-roll to Selection End': 'Pre-roll tới cuối vùng chọn',
    'Pre-roll to Selection Start': 'Pre-roll tới đầu vùng chọn',
    'Pre (Filters/Gain/Phase)': 'Pre (Filters/Gain/Phase)',
    'Pre Filters': 'Bộ lọc Pre',
    'Pre/Post MIDI Modifiers and Inserts': 'MIDI Modifier và Insert Pre/Post',
    'Preference Presets': 'Preset tùy chọn',
    'Preferred Unit of Measurement': 'Đơn vị đo ưu tiên',
    'Prepare for Archive': 'Chuẩn bị lưu trữ',
    'Preparing Data...': 'Đang chuẩn bị dữ liệu...',
    'Preserve Original Track': 'Giữ nguyên Track gốc',
    'Preset Reference': 'Tham chiếu Preset',
    'Press Key': 'Nhấn phím',
    'Press [ESC] to quit Inspection mode':
        'Nhấn [ESC] để thoát chế độ Inspection',
    'Place-holder': 'Chỗ điền',
    'Place-holder text.': 'Văn bản điền vào.',
    'Piano Keys': 'Các phím piano',
    'Pending Tags': 'Thẻ đang chờ',
    'Pad Layout': 'Pad Layout',

    # ==================================================================
    # a Vietnamese frame around an English clause
    # ==================================================================
    'Please fill in all mandatory entries':
        'Vui lòng điền vào tất cả mục bắt buộc',
    'Out of memory': 'Hết bộ nhớ',
    'Ornament': 'Hoa tiết',
    'Ornaments': 'Hoa tiết',
    'Overwrite existing script at %s': 'Ghi đè Script đã có tại %s',
    'Plug-in Editors "Always on Top"':
        'Trình sửa Plug-in "Luôn ở trên cùng"',
    'Popup Tools': 'Hộp công cụ Pop-up',

    # ==================================================================
    # Phase said "Pha" in one key and "Phase" in six
    # ==================================================================
    'Phase': 'Phase',
    'Phase 0°': 'Phase 0°',
    'Phase 180°': 'Phase 180°',
    'Player Preset:': 'Preset Player:',

    # ==================================================================
    # case, plural, family drift
    # ==================================================================
    'Plug-Ins': 'Plug-ins',
    'Plug-in Parameter Bank Shift Left':
        'Chuyển Bank tham số Plug-in sang trái',
    'Plug-in Parameter Bank Shift Right':
        'Chuyển Bank tham số Plug-in sang phải',
    'Operations': 'Các thao tác',
    'Out of range': 'Ngoài phạm vi',
    'Output Channels': 'Các Output Channel',
    'Overlapping Pitches': 'Các Pitch chồng lấn',
    'Output Port Names': 'Tên Output Port',
    'Output Port Names from Script': 'Tên Output Port từ Script',
    'Output Monitor: ': 'Monitor đầu ra: ',
    'Ports': 'Các cổng',
    'Port Number': 'Số Port',
    'Position & Related Tracks': 'Vị trí & Track liên quan',
    'Pads Remote Range End': 'Cuối vùng Pads Remote',
    'Pads Remote Range Start': 'Đầu vùng Pads Remote',
    'Pictures': 'Các hình ảnh',
    'Pattern Event / Track': 'Pattern Event / Track',
    'PAL to NTSC Pull-Up': 'PAL sang NTSC Pull-Up',
    'NTSC to PAL Pull-Down': 'NTSC sang PAL Pull-Down',
    'Please select a single map': 'Vui lòng chỉ chọn một Map',
    'Panels': 'Các Panel',
    'Parameter Color': 'Màu Parameter',
    'Parameter Mapping': 'Tham số Mapping',
    'Part Data Mode': 'Chế độ dữ liệu Part',
    'Part Merge Mode': 'Chế độ gộp Part',
    'Peak Level': 'Mức đỉnh',
    'Peak Normalization': 'Chuẩn hoá đỉnh tín hiệu',
    'Phrase Player': 'Phrase Player',
    'Pitch Extraction Mode': 'Chế độ trích xuất Pitch',
    'Pitch Spread': 'Độ phân bố Pitch',
    'Pitchbend Range': 'Dải Pitchbend',
    'Pitchbend Range: Down': 'Dải Pitchbend: Xuống',
    'Pitchbend Range: Up': 'Dải Pitchbend: Lên',
    'Phones Level': 'Mức Phones',
    'Percent': 'Phần trăm',
    'Permissions for: ': 'Quyền cho: ',
    'Pause After Repeats': 'Tạm dừng sau mỗi lần lặp',
    'Precision Time Alignment': 'Căn chỉnh thời gian độ chính xác cao',
    'Pre & Post Commands': 'Lệnh Pre & Post',
    'Pre/Post Divider moved': 'Đã di chuyển vạch phân cách Pre/Post',
    'Performance Validation Settings': 'Cài đặt kiểm tra hiệu năng',
    'Pattern Management': 'Quản lý Pattern',
    'Pattern Swing': 'Swing của Pattern',
    'Player Mode Settings': 'Cài đặt chế độ Player',
    'Player Remote Control': 'Player Remote Control',
    'Player Settings': 'Cài đặt Player',
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
