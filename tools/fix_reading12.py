#!/usr/bin/env python3
"""Round 12 of reading: the general catch-all, sampled across the whole map.

"general" is 3,300 labels and most are fine - the domain classification falls
back to it, so it collects everything the other seven domains do not claim.
Sampled in slices rather than read end to end, and the defects came in the same
families as the domains that were read fully, plus a few that only exist here.

The ones that only exist here:

  - "Color Space" -> "Mau Khoang trong", which reads as "empty space". Its own
    child key "Color Space Management" was right: "khong gian mau".
  - "Color Set" -> "Mau Dat".
  - "Combined Destination & Value" -> "Gia tri Combined Destination &" -
    the value lost, the ampersand ended up at the end.
  - "Flip Stems" -> "Lap Ddoi not". Stem is "than not" and Beam is "duoi not"
    (AGENT.md 4); this had the two swapped.
  - "Forced Accidentals" -> "Dau nhan bat buoc". Accidentals is "dau hoa" -
    "dau nhan" is a stress mark in a word.
  - "Flat" -> "Phang", which is level/smooth. A flat is "giam".
  - "Multi" -> "Da kenh". Multi-timbral is "boi", not multichannel.

  - a dozen "Clear ..." labels where the object stayed English next to
    "Clear All" which was translated, and ten "Move ..." labels the same way.

  - "Chords with 2/3 Common Notes" left scrambled after the 1-note key was
    fixed in an earlier round: "Chords voi Note 2 Common".

  python tools/fix_reading12.py
  python tools/fix_reading12.py --write
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
    # scrambled in a way nothing else produced
    # ==================================================================
    'Color Set': 'Bảng màu',
    'Color Set Options': 'Tùy chọn bảng màu',
    'Color Space': 'Không gian màu',
    'Combined Destination & Value': 'Đích & Giá trị kết hợp',
    'Combined Label & Setting': 'Nhãn & Cài đặt kết hợp',
    'Common Notes': 'Nốt chung',
    'Consolidate Events': 'Gộp Event',
    'Click Panning': 'Pan của Click',
    'Click Pattern Editor': 'Editor Click Pattern',
    'Click Sound Presets': 'Preset âm thanh Click',
    'Click Sounds': 'Âm thanh Click',
    'Click Destinations': 'Đích của Click',
    'Click Patterns': 'Click Pattern',
    'Click to Bypass Equalizers': 'Nhấp để Bypass Equalizer',
    'Click & Count-in & Click Pattern': 'Click & đếm nhịp & Click Pattern',
    'Chords with 2 Common Notes': 'Hợp âm có 2 nốt chung',
    'Chords with 3 Common Notes': 'Hợp âm có 3 nốt chung',
    'Chords & Pitches': 'Hợp âm & cao độ',
    'Chords To MIDI': 'Chuyển hợp âm sang MIDI',
    'Chords to MIDI': 'Chuyển hợp âm sang MIDI',
    'Circle of Fifths': 'Vòng tròn quãng năm',
    'Cleanup %s Project Folders': 'Dọn dẹp các thư mục Project %s',
    'Clean Up Lanes': 'Dọn dẹp Lane',
    'Clock Reference': 'Tham chiếu Clock',
    'Collecting Events': 'Đang thu thập Event',
    'Collecting Tags...': 'Đang thu thập Tag...',
    'Collapse All Groups': 'Thu gọn tất cả Group',
    'Collapse Tree': 'Thu gọn cây',
    'Colorize Events': 'Tô màu Event',
    'Colorize Selected Tracks...': 'Tô màu Track đã chọn...',
    'Clip Display Mode': 'Chế độ hiển thị Clip',
    'Clip Editing Mode': 'Chế độ sửa Clip',
    'Combine VCA Automation of Selected Tracks':
        'Gộp VCA Automation của Track đã chọn',
    'Configuration data request failed.': 'Yêu cầu dữ liệu cấu hình thất bại.',
    'Configure Defined Attributes': 'Cấu hình thuộc tính đã định nghĩa',
    'Configure Loudness Settings': 'Cấu hình cài đặt Loudness',
    'Configure Meter Settings': 'Cấu hình cài đặt Meter',
    'Computer Keyboard Input': 'Đầu vào bàn phím máy tính',
    'Constrain Delay Compensation': 'Giới hạn bù trễ Delay',
    'Flatten Arranger Track': 'Flatten Arranger Track',
    'Fixed Lengths': 'Độ dài cố định',
    'Fixed Project Parameters': 'Tham số cố định của Project',
    'Fixed To': 'Cố định tại',
    'Focus Quick Controls': 'Tập trung Quick Control',
    'Fold Tracks': 'Gấp Track',
    'Folder Path': 'Đường dẫn thư mục',
    'Folder Tracks': 'Các Folder Track',
    'Folding: Fold Tracks': 'Folding: Gấp Track',
    'Folding: Toggle Selected Track': 'Folding: Đảo Track đã chọn',
    'Folding: Toggle Tracks': 'Folding: Đảo Track',
    'Folding: Unfold Tracks': 'Folding: Mở Track',
    'Folding: Move Tracks To New Folder with Group Channel':
        'Folding: Chuyển Track vào thư mục mới kèm Group Channel',
    'Font': 'Font',
    'Fonts': 'Font',
    'Font Styles': 'Kiểu phông chữ',
    'Font Styles...': 'Kiểu phông chữ...',
    'Music Font': 'Font nhạc',
    'Multiple Files': 'Nhiều file',
    'Multiple Monitor Sources': 'Nhiều nguồn Monitor',
    'Multiple Part Controls': 'Nhiều điều khiển Part',
    'Mute Sections': 'Tắt tiếng các phần',
    'Move "%s" Down': 'Di chuyển "%s" xuống',
    'Move "%s" Up': 'Di chuyển "%s" lên',
    'Move Down More': 'Di chuyển xuống thêm',
    'Move Up More': 'Di chuyển lên thêm',
    'Move Vertically': 'Di chuyển theo chiều dọc',
    'Move Events to Back': 'Di chuyển Event về phía sau',
    'Move Events to Front': 'Di chuyển Event về phía trước',
    'Move Selected Channels': 'Di chuyển Channel đã chọn',
    'Move Controller Data': 'Di chuyển dữ liệu Controller',
    'Move Configuration to Position': 'Di chuyển cấu hình tới vị trí',
    'Forward/Backward movement (Slide)': 'Di chuyển tiến/lùi (Slide)',

    # ==================================================================
    # wrong senses
    # ==================================================================
    # Stem is "than not"; Beam is "duoi not" (AGENT.md 4). These were swapped.
    'Flip Stems': 'Lật thân nốt',
    # Accidentals are "dau hoa"; "dau nhan" is a stress mark inside a word
    'Forced Accidentals': 'Dấu hóa bắt buộc',
    'Accidentals': 'Các dấu hóa',
    # A flat lowers by a semitone; "phang" means level or smooth
    'Flat': 'Giảm',
    # MIDI String is Cubase's string table, not a guitar string
    'From String': 'Từ String',
    # Multi here is multi-timbral, "boi" - not multichannel
    'Multi': 'Bội',
    'Multi Shift': 'Dịch bội',

    # ==================================================================
    # "Clear X" left in English next to a translated "Clear All"
    # ==================================================================
    'Clear All Assignments': 'Xóa tất cả phép gán',
    'Clear All Measurements': 'Xóa tất cả phép đo',
    'Clear All Messages': 'Xóa tất cả thông điệp',
    'Clear all Messages': 'Xóa tất cả thông điệp',
    'Clear List': 'Xóa danh sách',
    'Clear Messages': 'Xóa thông điệp',
    'Clear Recent Paths': 'Xóa đường dẫn gần đây',
    'Clear Search': 'Xóa tìm kiếm',
    'Clear Search Text': 'Xóa nội dung tìm kiếm',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Multiply by 2': 'Nhân với 2',
    'Multiply by 3/4': 'Nhân với 3/4',
    'Multiply by 4/3': 'Nhân với 4/3',
    'Commit Failed.': 'Không thể Commit.',
    'Compatibility with Other Program Versions':
        'Tương thích với các phiên bản chương trình khác',
    'First Selected Track': 'Track đã chọn đầu tiên',
    'Follow Track List': 'Danh sách Track bám theo',
    'Close Windows': 'Đóng cửa sổ',
    'Clicks': 'Clicks',
    'Flags': 'Flags',
    'Mouse Time Position': 'Vị trí thời gian theo chuột',
    'Mouse Value': 'Giá trị theo chuột',

    # ==================================================================
    # plural dropped
    # ==================================================================
    'Frames': 'Frame',
    'Cues  (Post-Fader)': 'Cues  (Post-Fader)',
    '%s (Selected Channels)': '%s (Channel đã chọn)',
    '%s %d  %s %d (Frames)': '%s %d  %s %d (Frame)',
    '2 Bars': '2 Bar',
    '4 Bars': '4 Bar',
    '+ Groups/Sends (CSP)': '+ Groups/Sends (CSP)',
    '+ Master/Groups/Sends (CSPM)': '+ Master/Groups/Sends (CSPM)',
    'Mute Events': 'Tắt tiếng Event',
    "Activate 'Link Panners' for New Tracks":
        "Bật 'Link Panner' cho Track mới",
    'Click to Bypass Cue Sends': 'Nhấp để Bypass Cue Send',

    # ==================================================================
    # "%s" placed after the noun
    # ==================================================================
    '%s Control': 'Điều khiển %s',
    '%s End': 'Kết thúc %s',
    '%s Start': 'Bắt đầu %s',
    '%d Targets': '%d Đích',

    # ==================================================================
    # sentence fragments
    # ==================================================================
    '(externally clocked)': '(lấy xung ngoài)',
    '(First event cannot be moved)': '(Event đầu tiên không thể được di chuyển)',
    '%1.0fms; Segments Edited: %d': '%1.0fms; Segment đã sửa: %d',
    '%s Open Document Options': 'Tùy chọn mở tài liệu %s',
    '%s Project by %s - %s': '%s Project của %s - %s',
    'Above Specific Instruments\' Staves':
        'Khuông nhạc phía trên của các nhạc cụ cụ thể',
    'Accumulated recording time': 'Thời gian ghi lũy kế',
    'Click Pattern to Default': 'Đặt Click Pattern làm mặc định',
    'Move Event/Range to Selected Track': 'Di chuyển Event/dải tới Track đã chọn',
    'Mute Input': 'Tắt tiếng đầu vào',
    'Music Margins': 'Lề bản nhạc',
    'Compute Quick Loudness Analysis': 'Tính phân tích Loudness nhanh',
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
