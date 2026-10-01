#!/usr/bin/env python3
"""Round 8 of reading: chords, scales and note expressions.

The worst-behaving domain in the map. Almost every finding is the same defect
- the head noun moved to the front - but applied to three-word keys where the
middle word had been translated, so the value is no longer an anagram of the
key and every earlier rule missed it.

  Chord Track - Create Chord Events  ->  Event Chord Track - Create Chord
  Chord Track - Set up Musical Scales  ->  Scale Chord Track - Set up Musical
  Extend Note Lengths to Next Selected Note
                                    ->  Do dai Extend Note vao Note Next Selected
  Transpose Notes within the Defined Scale
                                    ->  Transpose Scale Notes within the Defined

  1. "Chord Track" itself reversed, seven keys:
        "Follow Chord Track"    -> "Track Follow Chord"
        "From Chord Track"      -> "Track From Chord"
        "Follows Chord Track"   -> "Track Follows Chord"
        "Match with Chord Track" -> "Match voi Track Chord"

  2. bare English where the sibling translated, or the reverse:
        "Highest Note" / "Lowest Note" / "Whole Note" / "Double Whole Note"
        stayed English while "Whole Note (Semibreve)" became "Not tron".
        "Tension" became "Not cang", which is wrong - that was the same bad
        guess as the earlier "It not cang hon", which this round replaced.

  3. "Chords with 1 Common Note" -> "Chords voi Note 1 Common".

  4. one sentence left entirely in English:
        "Handling of Chord Pads played with overlap"
        -> "Handling cua Chord Pads played voi overlap"

  python tools/fix_reading8.py
  python tools/fix_reading8.py --write
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
    # "Chord Track" reversed
    # ==================================================================
    'Follow Chord Track': 'Bám theo Chord Track',
    'Follows Chord Track': 'Bám theo Chord Track',
    'From Chord Track': 'Từ Chord Track',
    'Assign from Chord Track': 'Gán từ Chord Track',
    'Match with Chord Track': 'Đối chiếu với Chord Track',
    # enharmonic = the same pitch spelled differently, not a crescendo
    'Enharmonics from Chord Track': 'Bộ cảm điệu từ Chord Track',
    'Chord Editing - Match with Chord Track':
        'Chỉnh sửa hợp âm - Đối chiếu với Chord Track',
    'Destination track already contains chord events.':
        'Track đích đã chứa Chord Event.',

    # ==================================================================
    # "Chord Track X" with the head in the middle
    # ==================================================================
    'Chord Track - Create Chord Events':
        'Chord Track - Tạo Chord Event',
    'Chord Track - Chords to MIDI': 'Chord Track - Hợp âm sang MIDI',
    'Chord Track - Map to Chord Track': 'Chord Track - Gán sang Chord Track',
    'Chord Track - Set up Musical Scales...':
        'Chord Track - Thiết lập Scale nhạc...',
    'Chord Track - Assign Voices to Notes':
        'Chord Track - Gán bè cho các nốt',
    'Map to Chord Track': 'Gán sang Chord Track',
    'Is Part of Chord': 'Là một phần của hợp âm',
    'Is Part of Scale': 'Là một phần của Scale',

    # ==================================================================
    # "Chord X" reversed or scrambled
    # ==================================================================
    'Chord Symbol': 'Ký hiệu hợp âm',
    'Chord Symbols Preset': 'Preset ký hiệu hợp âm',
    'Chord Pads Presets': 'Preset Chord Pad',
    'Chord Pads Display Settings': 'Cài đặt hiển thị Chord Pad',
    'Chord Pads Remote Settings': 'Cài đặt Remote của Chord Pad',
    'Chord Pads Step Input': 'Nhập Step bằng Chord Pad',
    'Chord Pads Step Input - Move Events':
        'Nhập Step bằng Chord Pad - Di chuyển Event',
    'Chord Pads  - Open Remote Settings': 'Chord Pad - Mở cài đặt Remote',
    'Chord Pads': 'Chord Pad',
    'Chord Pads - Fewer Tensions': 'Chord Pad - Ít Tension hơn',
    'Chord Pads - More Tensions': 'Chord Pad - Nhiều Tension hơn',
    'Chord Pads - Previous Voicing': 'Chord Pad - Voicing liền trước',
    'Chord Pads - Next Voicing': 'Chord Pad - Voicing kế tiếp',
    'Chord Pads - Show/Hide Chord Pads': 'Chord Pad - Hiện/Ẩn Chord Pad',
    'Chord Pads - Show/Hide Editor/Assistant':
        'Chord Pad - Hiện/Ẩn Editor/Assistant',
    'Chord Pads - Latch Chords On/Off':
        'Chord Pad - Bật/Tắt Latch hợp âm',
    'Chord Pads - Transpose Down': 'Chord Pad - Transpose xuống',
    'Chord Pads - Transpose Up': 'Chord Pad - Transpose lên',
    'Latch Chord Pads': 'Latch Chord Pad',
    'Load Chord Pads Preset': 'Tải Preset Chord Pad',
    'Save Chord Pads Preset': 'Lưu Preset Chord Pad',
    'Open Chord Pads Preset Browser': 'Mở trình duyệt Preset Chord Pad',
    'Set Chords for Chord Lane': 'Đặt hợp âm cho Chord Lane',
    'Chords with 1 Common Note': 'Hợp âm có 1 nốt chung',
    'Chord Font': 'Font hợp âm',
    'Chord Input': 'Chord Input',
    'Chord Modifiers': 'Bộ thay đổi hợp âm',
    'Chord Note Distribution': 'Phân bố nốt của hợp âm',
    'Chord Voicing Style': 'Phong cách Voicing của hợp âm',
    'Chord type of selected notes': 'Loại hợp âm của các nốt đã chọn',
    'Chord Editing - Add to Chord Track':
        'Chỉnh sửa hợp âm - Thêm vào Chord Track',
    'Chord Editing - Drop 2 + 4': 'Chỉnh sửa hợp âm - Drop 2 + 4',
    'Chord Editing - Inversions: Move Down':
        'Chỉnh sửa hợp âm - Đảo: Xuống',
    'Chord Editing - Inversions: Move Up':
        'Chỉnh sửa hợp âm - Đảo: Lên',
    'Chord Assistant - Circle of Fifths':
        'Chord Assistant - Vòng tròn quãng năm',
    'Chord Assistant - List': 'Chord Assistant - Danh sách',
    'Chord Assistant - Proximity': 'Chord Assistant - Độ gần',
    'Current Chord Display': 'Hiển thị hợp âm hiện tại',
    'Configure voicing parameters': 'Cấu hình tham số Voicing',
    'Custom Chord Symbols': 'Ký hiệu hợp âm tùy chỉnh',

    # ==================================================================
    # "Note X" reversed
    # ==================================================================
    'Note Insert Velocity': 'Chèn Velocity của Note',
    'Note Input Toolbar': 'Thanh công cụ nhập Note',
    'Note On': 'Bật Note',
    'Note Off': 'Tắt Note',
    'Note To CC': 'Chuyển Note sang CC',
    'Note is Equal To': 'Note bằng với',
    'MIDI + MIDI Note Number': 'MIDI + số Note MIDI',
    'Lowest Root Note': 'Root Note thấp nhất',
    'Highest Note': 'Nốt cao nhất',
    'Lowest Note': 'Nốt thấp nhất',
    'Move highest note to bottom': 'Chuyển nốt cao nhất xuống dưới',
    'Move lowest note to top': 'Chuyển nốt thấp nhất lên trên',
    'Notate as Single Note': 'Ký âm thành một nốt đơn',
    'Note Number in Chord (lowest = 0)': 'Số thứ tự nốt trong hợp âm (thấp nhất = 0)',
    'Start Note': 'Nốt bắt đầu',
    'Step to next Note': 'Chuyển tới Note kế tiếp',
    'Slashed Grace Note': 'Nốt lạc có gạch chéo',
    'Unslashed Grace Note': 'Nốt lạc không gạch chéo',
    'Stretch Note Expression Data': 'Kéo giãn dữ liệu Note Expression',
    'Show Note Ons': 'Hiện các Note On',
    'Show Note Length On/Off': 'Bật/Tắt hiển thị độ dài Note',
    'Show Pitches from Scale Assistant': 'Hiện cao độ từ Trợ lý Scale',
    'Extend Note Lengths to Next Selected Note':
        'Kéo dài nốt tới Note đã chọn kế tiếp',
    'Mute/Unmute note segments': 'Mute/Bỏ Mute đoạn Note',
    'Limit note pitches to this value':
        'Giới hạn cao độ của nốt theo giá trị này',
    'Limit note velocities to this value':
        'Giới hạn Velocity của nốt theo giá trị này',

    # ==================================================================
    # "Scale X" reversed
    # ==================================================================
    'Scale Legato': 'Legato của Scale',
    'Scale Controller Data': 'Dữ liệu Scale Controller',
    'Scale Tempo Data': 'Dữ liệu Scale Tempo',
    'Scale Volume Curve': 'Đường cong Volume của Scale',
    'Scale Number of Systems by Page Height':
        'Phóng to/thu nhỏ số dòng nhạc theo chiều cao trang',
    'Scale Tempo': 'Phóng to/thu nhỏ Tempo',
    'Scale Vertically': 'Phóng to/thu nhỏ theo chiều dọc',
    'Scales - All Shown with a C-Root Note':
        'Scale - Tất cả đều hiện với nốt gốc C',
    'Set Highest Available Scale Note':
        'Đặt Note Scale khả dụng cao nhất',
    'Set Lowest Available Scale Note':
        'Đặt Note Scale khả dụng thấp nhất',
    'New Scale': 'Scale mới',
    'New Custom Chord': 'Hợp âm tùy chỉnh mới',
    'Transpose to Scale': 'Transpose sang Scale',
    'Quantize Pitches to Scale': 'Quantize cao độ theo Scale',
    'Synchronize with Root Note': 'Đồng bộ với Root Note',
    'Synchronize with Scale': 'Đồng bộ với Scale',
    'Use this Scale for Suggestions': 'Dùng Scale này để gợi ý',
    'Select scale for editing': 'Chọn Scale để sửa',
    'Voicings (From Chord Track)': 'Voicing (Từ Chord Track)',
    'Chord Notes': 'Nốt của hợp âm',
    'Transpose Notes within the Defined Scale':
        'Transpose các nốt trong Scale đã định nghĩa',

    # ==================================================================
    # wrong word choices
    # ==================================================================
    # "not cang" is not tension. Tension is the chord tension, left English.
    'Tension': 'Tension',
    'Tension Modifiers': 'Bộ thay đổi Tension',
    # "Rã" means to come apart; dissolve is a fade-out
    'Dissolve Note Expression': 'Hòa tan Note Expression',
    'Dissolve Part': 'Hòa tan Part',
    # "Khoa" is a different word from "Khoá"
    'Lock Chord Assignment on Pad': 'Khóa phép gán hợp âm trên Pad',
    # "duan" is a segment; an overlap is a region
    'Consolidate Note Expression Overlaps':
        'Gộp vùng chồng lấn của Note Expression',
    # "Tỉ lệ" is a ratio, not a musical scale
    'Editor Scale:': 'Scale của Editor:',
    # "Duplicates" are copies, not repetitions
    'Duplicates: Name & Scale': 'Bản trùng: Tên & Scale',
    'Highest in Chord from at Least n Notes':
        'Cao nhất trong hợp âm từ ít nhất n nốt',
    'Lowest in Chord from at Least n Notes':
        'Thấp nhất trong hợp âm từ ít nhất n nốt',
    'Set Note Length': 'Đặt độ dài Note',
    'Generate Harmony Voices': 'Tạo bè hòa âm',
    'Generate Harmony Voices...': 'Tạo bè hòa âm...',
    'Previous Chord': 'Hợp âm liền trước',
    'Previous Voicing': 'Voicing liền trước',
    'Previous Voicing (mouse wheel on pad)':
        'Voicing liền trước (cuộn chuột trên pad)',
    'Go to Previous Chord (Left Arrow)':
        'Tới hợp âm liền trước (Mũi tên trái)',
    'Go to Next Chord (Right Arrow)':
        'Tới hợp âm kế tiếp (Mũi tên phải)',
    'Record MIDI as Note Exp.': 'Ghi MIDI dưới dạng Note Exp.',
    'Mouse Note Position': 'Vị trí Note so với con chuột',
    'Handling of Chord Pads played with overlap':
        'Cách xử lý các Chord Pad bị chồng tiếng',
    'Zoom while Locating in Time Scale':
        'Phóng to/thu nhỏ khi định vị trong Time Scale',
    'Insert a suspended fourth chord with a 7':
        'Chèn hợp âm treo cấp 4 với nốt 7',
    'Insert a suspended second chord with a 7':
        'Chèn hợp âm treo cấp 2 với nốt 7',
    'Selected Articulation Combinations':
        'Tổ hợp Articulation đã chọn',
    'Yamaha Guitar Voicing': 'Voicing Guitar Yamaha',
    'Whole Note': 'Nốt tròn',
    'Double Whole Note': 'Nốt tròn đôi',
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
