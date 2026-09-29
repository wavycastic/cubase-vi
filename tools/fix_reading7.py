#!/usr/bin/env python3
"""Round 7 of reading: the transport, label by label.

The transport panel is the most translated-looking part of Cubase and the one
where "looks translated" and "is translated" come apart most often.

  1. a single word that got the wrong direction:

        "Select Prev Snap Type" -> "Chon Loai Next Snap"

     That one is a real bug, not a style problem: the menu item offers the
     wrong one of the two choices.

  2. "Retrospective Record" has three renderings in the same map:
        "Ghi bu", "Ghi hoi cuu", "Ghi hoi to"
     "Retrospective Record" is Cubase's own feature name, so all three become
     "Ghi hoi to MIDI".

  3. the noun moved in front of a translated noun, so the result is not an
     anagram of the key and the earlier word-order rule could not see it:

        "Locator Range Duration" -> "Locator Vung Thoi luong"
        "Loop Range Left"        -> "Loop Vung Trai"
        "Record Date"            -> "Ghi Ngay"          (also backwards)
        "Record Folder"          -> "Ghi Folder"
        "Record Panel"           -> "Ghi Panel"
        "Project Window Grid"    -> "Project Cuo so Grid"
        "Select Next Grid Type"  -> "Chon Loai Next Grid"

  4. "Shuttle Play Reverse" translated on four of eight keys:

        "Shuttle Play Reverse 1x" -> "Shuttle Play nguoc 1x"
        "Shuttle Play Reverse 2x" -> "Shuttle Play Reverse 2x"

     and "Nudge Cursor +10 Seconds" kept Seconds on four of six while the +5
     and -5 siblings say "giay".

  5. "Record: Punch In & Out/Re-Record" -> "Record: Punch trong & Out". "Punch
     In" turned into "Punch trong", and the rest of the panel says "Punch In".

  6. Snap: five spellings in one panel - "Snap", "bắt dính", "Snap Live",
     "Loại bắt dính". Snap is a Cubase term, so the whole panel keeps it.

  One error of my own, found while reading: an earlier round produced
  "do ro nhan thap thap" for "Low Intelligibility" - the word repeated. Fixed
  here, and "Intelligibility" is "kha nang nghe ro" rather than "do ro rang",
  which is a calque of a word that does not mean "intelligible" in Vietnamese.

  python tools/fix_reading7.py
  python tools/fix_reading7.py --write
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
    # a menu item pointing at the wrong choice
    # ==================================================================
    'Select Prev Snap Type': 'Chọn loại Snap trước',
    'Select Next Snap Type': 'Chọn loại Snap kế tiếp',
    'Select Prev Grid Type': 'Chọn loại Grid trước',
    'Select Next Grid Type': 'Chọn loại Grid kế tiếp',
    'Select Prev Grid Type Value': 'Chọn giá trị loại Grid trước',
    'Select Next Grid Type Value': 'Chọn giá trị loại Grid kế tiếp',
    'Select Previous Quantize Value': 'Chọn giá trị Quantize trước',
    'Select Next Quantize Value': 'Chọn giá trị Quantize kế tiếp',

    # ==================================================================
    # Retrospective Record had three renderings
    # ==================================================================
    'Retrospective Record': 'Ghi hồi tố MIDI',
    'Retrospective Record: Chords': 'Ghi hồi tố MIDI: Hợp âm',
    'MIDI Retrospective Record: Empty All Buffers':
        'Ghi hồi tố MIDI: Xóa tất cả Buffer',
    'Insert Retrospective Recording': 'Chèn bản ghi hồi tố',
    'Empty Retrospective Record Buffer': 'Làm rỗng Buffer ghi hồi tố',
    'MIDI Retrospective Record: Insert from Track Input as Cycle Recording':
        'Ghi hồi tố MIDI: Chèn từ đầu vào Track dưới dạng ghi theo Cycle',
    'MIDI Retrospective Record: Insert from Track Input as Linear Recording':
        'Ghi hồi tố MIDI: Chèn từ đầu vào Track dưới dạng ghi tuyến tính',
    'Jump to Next Range with Low Intelligibility':
        'Tới Vùng kế tiếp có khả năng nghe rõ thấp',
    'Short-term intelligibility at cursor position':
        'Khả năng nghe rõ ngắn hạn tại vị trí con trỏ',

    # ==================================================================
    # "Punch In" turned into "Punch trong"
    # ==================================================================
    'Record: Punch In & Out/Re-Record': 'Ghi: Punch In & Out/Ghi lại',

    # ==================================================================
    # noun moved in front of a translated noun
    # ==================================================================
    'Locator Range Duration': 'Thời lượng dải Locator',
    'Loop Range Left': 'Biên trái của Loop',
    'Loop Range Right': 'Biên phải của Loop',
    'Loop End Time': 'Thời điểm kết thúc Loop',
    'Loop Start Time': 'Thời điểm bắt đầu Loop',
    'Record Date': 'Ngày ghi',
    'Record Folder': 'Thư mục ghi',
    'Record Panel': 'Bảng ghi',
    'Record Pitch': 'Pitch ghi',
    'Record Shift': 'Lệch ghi',
    'Record Tracks': 'Ghi các Track',
    'Record Enable All Tracks': 'Bật ghi cho tất cả Track',
    'Record Enable On/Off': 'Bật/Tắt ghi',
    'Record Enable/Monitor': 'Bật ghi/Monitor',
    'Project Window Grid': 'Grid của cửa sổ Project',
    'Left Locator Position': 'Vị trí Locator trái',
    'Right Locator Position': 'Vị trí Locator phải',
    'Original Tempo': 'Tempo gốc',
    'Quick Zoom': 'Zoom nhanh',
    'Maximum Quantize Movement': 'Dịch chuyển tối đa khi Quantize',
    'Quantize Presets': 'Preset Quantize',
    'Quantize Link': 'Liên kết Quantize',
    'Quantize as Notated': 'Quantize theo ký âm',
    'Page Scroll': 'Cuộn trang',
    'Pattern Play Direction': 'Hướng phát Pattern',
    'Picture Zoom': 'Zoom hình ảnh',
    'Range Selection Cursor': 'Con trỏ chọn dải',
    'Organize Zoom Presets': 'Sắp xếp Zoom Preset',
    'Set Definition From Tempo': 'Đặt định nghĩa từ Tempo',
    'Set Definition From Tempo...': 'Đặt định nghĩa từ Tempo...',
    'Grid Lines': 'Đường Grid',
    'Grid Match': 'Khớp Grid',
    'Grid Relative': 'Grid tương đối',
    'Grid Resolution': 'Độ phân giải Grid',
    'Grid Type: Bar': 'Loại Grid: Bar',
    'Grid Type: Beat': 'Loại Grid: Beat',
    'Grid Type: Adapt to Zoom': 'Loại Grid: Thích ứng với Zoom',
    'Display Quantize': 'Hiển thị Quantize',
    'Global Quantize': 'Quantize toàn cục',
    'Horizontal Zoom Presets': 'Zoom Preset ngang',
    'Independent Track Loop': 'Track Loop độc lập',
    'From Active Marker Track': 'Từ Marker Track đang hoạt động',
    'From All Marker Tracks': 'Từ tất cả Marker Track',
    'Generate Multiple Marker Tracks': 'Tạo nhiều Marker Track',
    'Inside Selected Marker': 'Bên trong Marker đã chọn',
    'Exchange Left & Right Locator Positions':
        'Hoán đổi vị trí hai Locator',
    'Fill inside Loop': 'Lấp đầy bên trong Loop',
    'Fill Loop with Pattern': 'Lấp đầy Loop bằng Pattern',
    'Events under Cursor': 'Event dưới con trỏ',
    'Move Markers to Cursor': 'Di chuyển Marker tới con trỏ',
    'Snap Live Input': 'Snap đầu vào trực tiếp',
    'Snap MIDI Parts to Bars': 'Snap MIDI Part theo Bar',
    'Snap Pitchbend Events': 'Snap Event Pitchbend',
    'Snap Type: Grid': 'Loại Snap: Grid',
    'Snap Off': 'Tắt Snap',
    'Snap On': 'Bật Snap',

    # ==================================================================
    # half the family translated, half did not
    # ==================================================================
    'Shuttle Play Reverse 1x': 'Shuttle Play ngược 1x',
    'Shuttle Play Reverse 2x': 'Shuttle Play ngược 2x',
    'Shuttle Play Reverse 4x': 'Shuttle Play ngược 4x',
    'Shuttle Play Reverse 8x': 'Shuttle Play ngược 8x',
    'Shuttle Play Reverse 1/2x': 'Shuttle Play ngược 1/2x',
    'Shuttle Play Reverse 1/4x': 'Shuttle Play ngược 1/4x',
    'Shuttle Play Reverse 1/8x': 'Shuttle Play ngược 1/8x',
    'Nudge Cursor +10 Seconds': 'Nhích con trỏ +10 giây',
    'Nudge Cursor +20 Seconds': 'Nhích con trỏ +20 giây',
    'Nudge Cursor -10 Seconds': 'Nhích con trỏ -10 giây',
    'Nudge Cursor -20 Seconds': 'Nhích con trỏ -20 giây',
    'Nudge Cursor +5 Seconds': 'Nhích con trỏ +5 giây',
    'Nudge Cursor -5 Seconds': 'Nhích con trỏ -5 giây',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Play Direction': 'Hướng phát',
    'Set Play Direction': 'Đặt hướng phát',
    'Play Probability': 'Xác suất phát',
    'Set Play Probability': 'Đặt xác suất phát',
    'Reset MIDI Play Probability': 'Đặt lại xác suất phát MIDI',
    'Apply MIDI Play Probability': 'Áp dụng xác suất phát MIDI',
    'Play until Next Marker': 'Phát tới Marker kế tiếp',
    'Play until Selection End': 'Phát tới cuối vùng chọn',
    'Play until Selection Start': 'Phát tới đầu vùng chọn',
    'Play Selection Solo': 'Phát vùng chọn ở chế độ Solo',
    'Play Tracks': 'Phát các Track',
    'Play back Slice': 'Phát lại Slice',
    'Play Project Range': 'Phát dải Project',
    'Select Marker Tracks': 'Chọn Marker Track',
    'Select Next Marker in Markers Window':
        'Chọn Marker kế tiếp trong cửa sổ Marker',
    'Select Previous Marker in Markers Window':
        'Chọn Marker liền trước trong cửa sổ Marker',
    'Set Range to current Locator Range':
        'Đặt dải theo dải Locator hiện tại',
    'Set global project tempo?': 'Đặt Tempo chung của Project?',
    'Set project tempo': 'Đặt Tempo của Project',
    'Set tempo from first event?': 'Đặt Tempo từ Event đầu tiên?',
    'New project tempo : %.3f BPM': 'Tempo mới của Project: %.3f BPM',
    'New tempo at %s : %.3f BPM': 'Tempo mới tại %s: %.3f BPM',
    'Multiply the detected tempo by 3/4': 'Nhân Tempo đã nhận diện với 3/4',
    'Multiply the detected tempo by 4/3': 'Nhân Tempo đã nhận diện với 4/3',
    'New Tempo Points Type': 'Loại Tempo Points mới',
    'New Tempo Type': 'Loại Tempo mới',
    'Restore Marker Attribute Defaults':
        'Khôi phục giá trị mặc định của Marker Attribute',
    'Notes play when triggering chords': 'Nốt phát khi kích hoạt hợp âm',
    'Notes play when triggering chords or sections':
        'Nốt phát khi kích hoạt hợp âm hoặc phân đoạn',
    'Notes play when triggering sections': 'Nốt phát khi kích hoạt phân đoạn',
    'Please set cycle length.': 'Vui lòng đặt độ dài Cycle.',
    'Show Pattern Play Progress': 'Hiện tiến trình phát Pattern',
    'Paste Relative to Cursor': 'Dán tương đối với con trỏ',
    'Go to Previous Marker/Zero': 'Tới Marker/Zero liền trước',
    'Record only Specific Controller No.':
        'Chỉ ghi Controller có số cụ thể.',
    'Decreasing Stepwise (cycle)': 'Giảm dần từng bước (Cycle)',
    'Increasing Stepwise (cycle)': 'Tăng dần từng bước (Cycle)',
    'Jump to Marker 1\\nUse [ALT + click] to set':
        'Tới Marker 1\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 2\\nUse [ALT + click] to set':
        'Tới Marker 2\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 3\\nUse [ALT + click] to set':
        'Tới Marker 3\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 4\\nUse [ALT + click] to set':
        'Tới Marker 4\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 5\\nUse [ALT + click] to set':
        'Tới Marker 5\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 6\\nUse [ALT + click] to set':
        'Tới Marker 6\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 7\\nUse [ALT + click] to set':
        'Tới Marker 7\\nDùng [ALT + nhấp] để đặt',
    'Jump to Marker 8\\nUse [ALT + click] to set':
        'Tới Marker 8\\nDùng [ALT + nhấp] để đặt',

    # ==================================================================
    # capitalisation and drift against a sibling
    # ==================================================================
    'Scroll[Key]': 'Scroll',
    'Open Record Panel': 'Mở bảng ghi',
    'Open Tempo Recording Panel': 'Mở bảng ghi Tempo',
    'Open/Close Transport Panel': 'Mở/Đóng bảng Transport',
    'Set up Common Record Modes': 'Thiết lập chế độ ghi chung',
    'Edit Marker Attribute': 'Sửa thuộc tính Marker',
    'Remove Marker Attribute': 'Gỡ bỏ thuộc tính Marker',
    'Remove Marker Attributes': 'Gỡ bỏ các thuộc tính Marker',
    'Enter Left Locator Position': 'Nhập vị trí Locator trái',
    'Enter Right Locator Position': 'Nhập vị trí Locator phải',
    'Enter Project Cursor Position': 'Nhập vị trí con trỏ Project',
    'Set Cursor Position': 'Đặt vị trí con trỏ',
    'Set Project Cursor Position': 'Đặt vị trí con trỏ Project',
    'Set Left Locator to Project Cursor Position':
        'Đặt Locator trái tới vị trí con trỏ Project',
    'Set Right Locator to Project Cursor Position':
        'Đặt Locator phải tới vị trí con trỏ Project',
    'Set Punch In to Project Cursor Position':
        'Đặt Punch In tới vị trí con trỏ Project',
    'Set Punch Out to Project Cursor Position':
        'Đặt Punch Out tới vị trí con trỏ Project',
    'Set Marker Length': 'Đặt độ dài Marker',
    'Set Focus to Marker Track': 'Đặt Focus tới Marker Track',
    'Link to Grid On/Off': 'Liên kết với Grid: Bật/Tắt',
    'Link to Project Tempo': 'Liên kết với Tempo của Project',
    'MIDI Record Mode': 'Chế độ ghi MIDI',
    'MIDI Record Modes': 'Các chế độ ghi MIDI',
    'MIDI Auto Quantize': 'Quantize tự động MIDI',
    'Select Auto-Scroll Settings': 'Chọn cài đặt Auto-Scroll',
    'In Loop': 'Trong Loop',
    'In Record': 'Khi đang ghi',
    'Snap Track Heights': 'Snap chiều cao Track',
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
