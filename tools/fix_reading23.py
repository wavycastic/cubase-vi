#!/usr/bin/env python3
"""Round 23 of reading: the S block of the general catch-all.

Four slices, 5260..5660, about 400 labels. The "Show ..." and "Show/Hide ..."
families - about 130 keys between them - were left about half in English, and
the "Set up ..." family of twenty was left entirely so:

    "Set up Attribute Columns"  -> "Thiet lap Attribute Columns"
    "Set up Cell Layout"        -> "Thiet lap Cell Layout"
    "Set up Items"              -> "Thiet lap Items"
    "Set up Status Line"        -> "Thiet lap Status Line"
    "Set up Tabs"               -> "Thiet lap Tabs"

where "Thiet lap" is the prefix and nothing behind it was translated. And in
the Show family the object was left in English next to a translated verb:

    "Show Tracks with Data"          -> "Hien Tracks voi Data"
    "Show Event Volume Curve"        -> "Hien Event Volume Curve"
    "Show Meter View"                -> "Hien Meter View"
    "Show Part Borders"              -> "Hien Part Borders"
    "Show Pitches with Events"       -> "Hien Pitches voi Events"
    "Show live events"               -> "Hien live events"
    "Show log files in Finder"       -> "Hien log files trong Finder"
    "Show playback events"           -> "Hien playback events"

A second instance of the "key signature" error from round 22, and the same
wrong word:

    "Sign." -> "Hoa bieu"

  "Sign." is Signature abbreviated, and the map has it right next door as "So
  chi nhip". "Hoa bieu" is Expression. Two abbreviations of two different words
  both became Expression.

Three more reversals, the shape is by now unmistakable:

    "Shows Input Pad State"        -> "Trang thai Shows Input Pad"
    "Shows Phantom Power State"    -> "Trang thai Shows Phantom Power"
    "Show/Hide Step Lane Inspector"-> "Hien/An Inspector Step Lane"
    "Size Events"                  -> "Event Kich thuoc"
    "Size Part"                    -> "Part Kich thuoc"
    "Slash Noteheads"              -> "Gach cheo Dau noi"
    "Simple Crossfade Editor"      -> "Editor Simple Crossfade"
    "Shift Notes down One Octave"  -> "Octave Shift Notes down One"

  "Octave Shift Notes down One" is the worst: the sentence has been rotated,
  not reversed. Reading it, nothing is a predicate of anything.

And "Skip Doubles" said "bo qua not lap doi" where "Delete Doubles" two
hundred keys away said "Xoa Note trung". Doubles are duplicate notes, not
doubled notes.

  python tools/fix_reading23.py
  python tools/fix_reading23.py --write
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
    # "Set up ..." - the prefix translated, the object left in English
    # ==================================================================
    'Set up ADR Text Overlays': 'Thiết lập lớp phủ văn bản ADR',
    'Set up Attribute Columns': 'Thiết lập cột thuộc tính',
    'Set up Cell Layout': 'Thiết lập Layout ô',
    'Set up Computer Keyboard Input':
        'Thiết lập đầu vào bàn phím máy tính',
    'Set up Info Line': 'Thiết lập dòng thông tin',
    'Set up Items': 'Thiết lập mục',
    'Set up Lane Controls': 'Thiết lật điều khiển Lane',
    'Set up Musical Scales...': 'Thiết lập Scale nhạc...',
    'Set up Naming Scheme...': 'Thiết lập quy tắc đặt tên...',
    'Set up Result Columns': 'Thiết lập cột kết quả',
    'Set up Sections': 'Thiết lật phần',
    'Set up Status Line': 'Thiết lật thanh trạng thái',
    'Set up Tabs': 'Thiết lật thẻ',
    'Set root key for unassigned events':
        'Đặt Root Key cho các Event chưa gán',
    'Set all Tracks to Musical Timebase':
        'Đặt tất cả Track sang Musical Timebase',
    'Set Write Protection': 'Đặt bảo vệ ghi',
    'Sets the focus according to the track selection.':
        'Đặt tiêu điểm theo vùng chọn Track.',
    'Settings: Next Settings': 'Cài đặt: Cài đặt kế tiếp',

    # ==================================================================
    # the "Show ..." family, object left in English
    # ==================================================================
    'Show Event Volume Control': 'Hiện điều khiển âm lượng Event',
    'Show Event Volume Curve': 'Hiện đường cong âm lượng Event',
    'Show Event Volume Curves Always':
        'Luôn hiện đường cong âm lượng Event',
    'Show Events': 'Hiện Event',
    'Show Fades': 'Hiện Fade',
    'Show Folders in Deep Results': 'Hiện thư mục trong kết quả sâu',
    'Show Half Level Axis': 'Hiện trục nửa mức',
    'Show Info': 'Hiện thông tin',
    'Show Info Line': 'Hiện dòng thông tin',
    'Show Inserts as <%s>': 'Hiện Insert dạng <%s>',
    'Show Keyboard Preview': 'Hiện xem trước bàn phím',
    'Show Lanes': 'Hiện Lane',
    'Show Markers': 'Hiện Marker',
    'Show Meter View': 'Hiện chế độ xem Meter',
    'Show Modulators as <%s>': 'Hiện Modulator dạng <%s>',
    'Show No Further Cautionary Accidentals':
        'Không hiện dấu hóa nhắc lại nữa',
    'Show Once per Bracket': 'Hiện một lần cho mỗi dấu ngoặc',
    'Show Overlaps': 'Hiện phần chồng lấn',
    'Show Part Borders': 'Hiện viền Part',
    'Show Picture': 'Hiện hình ảnh',
    'Show Pitches with Events': 'Hiện cao độ có Event',
    'Show Playback Techniques': 'Hiện Playing Techniques',
    'Show Pre as <%s>': 'Hiện Pre dạng <%s>',
    'Show Quick Controls as <%s>': 'Hiện Quick Control dạng <%s>',
    'Show Rhythms in Tablature': 'Hiện nhịp trong Tablature',
    'Show Scales': 'Hiện Scale',
    'Show Sends as <%s>': 'Hiện Send dạng <%s>',
    'Show Strip Modules as <%s>': 'Hiện Module Strip dạng <%s>',
    'Show Surface Element Rectangles':
        'Hiện hình chữ nhật phần tử Surface',
    'Show Track Pictures': 'Hiện hình ảnh Track',
    'Show Track View': 'Hiện chế độ xem Track',
    'Show Tracks': 'Hiện Track',
    'Show Tracks with Data': 'Hiện Track có dữ liệu',
    'Show Tracks with Drum Map': 'Hiện Track có Drum Map',
    'Show Tracks with Selected Events': 'Hiện Track có Event đã chọn',
    'Show Tracks with Selected Parts': 'Hiện Track có Part đã chọn',
    'Show Equalizer Controls': 'Hiện điều khiển Equalizer',
    'Show Event Details': 'Hiện chi tiết Event',
    'Show Controls as Knobs': 'Hiện Control dạng Knob',
    'Show Controls as Sliders': 'Hiện Control dạng Slider',
    'Show Default Smart Controls': 'Hiện Smart Control mặc định',
    'Show Automated QC Assignments': 'Hiện phép gán QC tự động',
    'Show Cautionary Accidentals': 'Hiện dấu hóa nhắc lại',
    'Show Cautionary in Parentheses': 'Hiện dấu hóa nhắc lại trong ngoặc',
    'Show Click Patterns': 'Hiện Click Pattern',
    'Show Clips': 'Hiện Clip',
    'Show Controllers': 'Hiện Controller',
    'Show Drum Sounds in use by Instrument':
        'Hiện âm thanh Drum đang được Instrument dùng',
    'Show Drum Sounds with Events': 'Hiện âm thanh Drum có Event',
    'Show live events': 'Hiện Event trực tiếp',
    'Show log files in Explorer': 'Hiện file log trong Explorer',
    'Show log files in Finder': 'Hiện file log trong Finder',
    'Show playback events': 'Hiện Event phát lại',
    'Show in Scripts Folder': 'Hiện trong thư mục Script',
    'Show Output Chain': 'Hiện Chain đầu ra',
    'Show Interval on Trill': 'Hiện quãng trên dấu Trill',
    'Show Key Signatures': 'Hiện Key Signature',
    'Show Log Messages Only': 'Chỉ hiện thông điệp nhật ký',
    'Show All Messages': 'Hiện tất cả thông điệp',
    'Show All Plug-ins': 'Hiện tất cả Plug-in',
    'Show All Smart Controls': 'Hiện tất cả Smart Control',
    'Show All Volume Automation': 'Hiện tất cả Automation âm lượng',

    # ==================================================================
    # the "Show/Hide ..." family
    # ==================================================================
    'Show/Hide Attribute Filters': 'Hiện/Ẩn bộ lọc thuộc tính',
    'Show/Hide Controller Lanes': 'Hiện/Ẩn Controller Lane',
    'Show/Hide Info': 'Hiện/Ẩn thông tin',
    'Show/Hide Latency': 'Hiện/Ẩn độ trễ',
    'Show/Hide Left Zone': 'Hiện/Ẩn Left Zone',
    'Show/Hide Right Zone': 'Hiện/Ẩn Right Zone',
    'Show/Hide Macros': 'Hiện/Ẩn Macro',
    'Show/Hide Modulators': 'Hiện/Ẩn Modulator',
    'Show/Hide Pictures': 'Hiện/Ẩn hình ảnh',
    'Show/Hide Regions': 'Hiện/Ẩn Region',
    'Show/Hide Status Line': 'Hiện/Ẩn thanh trạng thái',
    'Show/Hide Step Lane Inspector': 'Hiện/Ẩn Step Lane Inspector',
    'Show/Hide Value Display': 'Hiện/Ẩn hiển thị giá trị',
    'Show/Hide Output Chain': 'Hiện/Ẩn Chain đầu ra',
    'Show/Hide Global Tracks': 'Hiện/Ẩn Track toàn cục',
    'Show/Hide Automation Mode': 'Hiện/Ẩn chế độ Automation',
    'Show/Hide Editor Visibility': 'Hiện/Ẩn khả năng hiển thị của Editor',

    # ==================================================================
    # reversed, and one that was rotated rather than reversed
    # ==================================================================
    'Shows Input Pad State': 'Hiển thị trạng thái Input Pad',
    'Shows Phantom Power State': 'Hiển thị trạng thái Phantom Power',
    'Size Event End': 'Kích thước cuối Event',
    'Size Event Start': 'Kích thước đầu Event',
    'Size Events': 'Kích thước Event',
    'Size Objects': 'Kích thước đối tượng',
    'Size Part': 'Kích thước Part',
    'Size Region End': 'Kích thước cuối Region',
    'Size Region Start': 'Kích thước đầu Region',
    'Size in Parts': 'Kích thước tính bằng Part',
    'Sizing Applies Time Stretch': 'Kích thước áp dụng Time Stretch',
    'Sizing Moves Contents': 'Kích thước di chuyển nội dung',
    'Shift Chords': 'Dịch hợp âm',
    'Shift Notes': 'Dịch Note',
    'Shift Notes down One Octave': 'Dịch Note xuống một octave',
    'Shift Notes up One Octave': 'Dịch Note lên một octave',
    'Shift Left': 'Dịch sang trái',
    'Shift Right': 'Dịch sang phải',
    'Shift Selected Steps': 'Dịch các Step đã chọn',
    'Slash Noteheads': 'Đầu nốt gạch chéo',
    'Slash Region': 'Region gạch chéo',
    'Simple Crossfade Editor': 'Trình sửa Crossfade đơn giản',
    'Show Volume Curve Display Mode': 'Hiện chế độ hiển thị đường cong âm lượng',

    # ==================================================================
    # "Sign." is Signature abbreviated, not Expression
    # ==================================================================
    'Sign.': 'Số chỉ nhịp.',
    'Sign at End With Dashed Line': 'Ký hiệu ở cuối bằng đường nét đứt',
    'Sign at end': 'Ký hiệu ở cuối',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Side-Chain Input': 'Side-Chain Input',
    'Side-Chain Inputs:': 'Side-Chain Input:',
    'Side-chain Inputs': 'Side-chain Input',
    'Skip Doubles': 'Bỏ qua Note trùng',
    'Slave to MIDI Machine Control': 'Slave cho MIDI Machine Control',
    'Shuffle Results': 'Xáo trộn kết quả',
    'Slices': 'Các Slice',
    'Skin Files': 'Các file Skin',
    'Skin XML Version': 'Phiên bản XML của Skin',
    'Short Name': 'Tên ngắn',
    'Short-Term Intelligibility': 'Khả năng nghe rõ ngắn hạn',
    'Short-Term Loudness': 'Loudness ngắn hạn',
    'Show Additional Functions': 'Hiện các chức năng bổ sung',

    # ==================================================================
    # case
    # ==================================================================
    'Show Frame Numbers': 'Hiện số Frame',
    'Show Next Tab': 'Hiện thẻ kế tiếp',
    'Show Previous Tab': 'Hiện thẻ liền trước',
    'Show Script Info': 'Hiện thông tin Script',
    'Show Settings': 'Hiện cài đặt',
    'Show Thumbnail Numbers': 'Hiện số Thumbnail',
    'Show Version Name in Track List': 'Hiện tên Version trong danh sách Track',
    'Show Cautionary': 'Hiện dấu hóa nhắc lại',
    'Show All - Used Only': 'Hiện tất cả - Chỉ dùng',
    'Showing and Hiding': 'Hiện và Ẩn',
    'Second Viennese School': 'Trường phái Vienna thứ hai',
    'Setup ID3 Tag': 'Thiết lập ID3 Tag',
    'Single or Multiple Job': 'Tác vụ đơn hoặc nhiều',
    'Settling Time Allowance': 'Dung sai thời gian ổn định',
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
