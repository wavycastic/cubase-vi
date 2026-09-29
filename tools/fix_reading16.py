#!/usr/bin/env python3
"""Round 16 of reading: the E-G block of the general catch-all.

Six slices, 1960..2460, about 600 labels. Three whole families came apart here,
and one of them is the worst systematic error I have found in the map.

  1. "Event <noun>" was reversed across the board:

        "Event Display"  -> "Event Hien thi"
        "Event End"       -> "Event Ket thuc"
        "Event Start"     -> "Event Bat dau"
        "Event Target Filters" -> "Filter Event Target"
        "Estimated Pitch" -> "Pitch Estimated"

      "Event Ket thuc" is not a Vietnamese phrase in any reading - the head noun
      has been pushed behind its own modifier and the result is a fragment.

  2. "Group" was translated as the VERB "gop" instead of the NOUN "nhom":

        "Group"        -> "Gop nhom"
        "Group 1"      -> "Gop nhom 1"
        "Group 1..4"   -> "Gop nhom 1..4"
        "Group Track"  -> "Gop nhom Track"
        "Group Tracks" -> "Gop nhom Tracks"
        "Group Channels" / "Group Editing" / "Group Track to Selected Tracks..."

      Nine keys. Every one of them is a noun - a label for an object, or a menu
      path. "Gop nhom Track" tells the user to merge, which is a different
      action entirely. The one place the verb really is a verb, "Add Group
      Track" -> "Them Group Track", had been left alone - so the noun form was
      never checked against it.

  3. "Expand:" had been scattered:

        "Expand: Cue Sends"    -> "Sends Expand: Cue"
        "Expand: Device Panels" -> "Bang Expand: Device"
        "Expand: VCA"          -> "Mo rong VCA"        (colon gone)
        "Expand: EQs"          -> "Mo rong EQs"        (colon gone)
        "Expand: Inserts"      -> "Mo rong: Insert"    (s gone)
        "Expand: Modulators"   -> "Mo rong: Modulator" (s gone)

      Two of the six have the tail before the head, as if the string had been
      cut in half and the halves put back in the other order.

  And two words that were read as the wrong word entirely:

        "Half (I-V-I)" -> "Giam (I-V-I)"
      Half is "nua". "Giam" is flat - it is the value this map already uses for
      "Flat", and the two were never compared.

        "Ext. %d" -> "Mo rong %d"
      Ext. is External. "Mo rong" is Extend. Two different things that share
      three letters.

  Also the External family, split three ways: "External Effect" and "External
  Instrument" keep English, "External Input" says "Input ben ngoai", "External
  Sync" says "Sync ben ngoai", and "External Source: 1/2/3" said "Nguon ngoai"
  while 4/5/6 said "ben ngoai Source" - two shapes inside one family of six.

  python tools/fix_reading16.py
  python tools/fix_reading16.py --write
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
    # "Event <noun>" reversed
    # ==================================================================
    'Event Display': 'Hiển thị Event',
    'Event Display in Editor': 'Hiển thị Event trong Editor',
    'Event End': 'Kết thúc Event',
    'Event Start': 'Bắt đầu Event',
    'Event Target Filters': 'Bộ lọc đích của Event',
    'Event Types': 'Các loại Event',
    'Event Types and Subtype': 'Các loại và loại phụ của Event',
    'Event Channels': 'Event Channel',
    'Events': 'Các Event',
    'Events and Parts': 'Event và Part',
    'Events from Regions': 'Event từ Region',
    'Events to Front': 'Chuyển Event về phía trước',
    'Events to Origin': 'Chuyển Event tới điểm gốc',
    'Estimated Pitch': 'Pitch ước tính',
    'Every Other Event': 'Mọi Event xen kẽ',
    'Event/Range to Selected Track': 'Event/vùng tới Track đã chọn',
    'Event Transform Actions': 'Các thao tác Event Transform',

    # ==================================================================
    # "Group" read as the verb "gop" instead of the noun "nhom"
    # ==================================================================
    'Group %d': 'Nhóm %d',
    'Group 1': 'Nhóm 1',
    'Group 2': 'Nhóm 2',
    'Group 3': 'Nhóm 3',
    'Group 4': 'Nhóm 4',
    'Group Track': 'Group Track',
    'Group Tracks': 'Các Group Track',
    'Group Track to Selected Tracks...': 'Group Track vào Track đã chọn...',
    'Group Channels': 'Group Channel',
    'Group Channels: Mute Sources as well': 'Group Channel: Mute cả Sources',
    'Group Editing': 'Group Editing',
    'Groups': 'Các Group',

    # ==================================================================
    # the Expand: family - tail before head on two, colon gone on two
    # ==================================================================
    'Expand: Cue Sends': 'Expand: Cue Sends',
    'Expand: Device Panels': 'Expand: Device Panels',
    'Expand: VCA': 'Mở rộng: VCA',
    'Expand: EQs': 'Mở rộng: EQs',
    'Expand: Inserts': 'Mở rộng: Inserts',
    'Expand: Modulators': 'Mở rộng: Modulators',
    'Expand: Sends': 'Mở rộng: Sends',
    'Expand/Reduce': 'Mở rộng/Thu nhỏ',
    'Expand Sections Exclusively': 'Mở rộng phần theo kiểu loại trừ',
    'Expand Tree': 'Mở rộng cây',
    'Expand All Groups': 'Mở rộng tất cả Group',
    'Exit Fullscreen Mode': 'Thoát chế độ Fullscreen',

    # ==================================================================
    # two words read as a different word
    # ==================================================================
    # Half is "nua"; "giam" is flat, which is what "Flat" already maps to
    'Half (I-V-I)': 'Nửa (I-V-I)',
    'Half Size': 'Kích thước nửa',
    'Half Speed Playback': 'Phát nửa tốc độ',
    # Ext. is External; "Mo rong" is Extend
    'Ext. %d': 'External %d',
    'Extend to Next Selected': 'Mở rộng tới mục chọn kế tiếp',

    # ==================================================================
    # the External family, split three ways
    # ==================================================================
    'External': 'External',
    'External Input': 'External Input',
    'External Sync': 'External Sync',
    'External Sync State': 'External Sync State',
    'External Source: 1': 'External Source: 1',
    'External Source: 2': 'External Source: 2',
    'External Source: 3': 'External Source: 3',
    'External Source: 4': 'External Source: 4',
    'External Source: 5': 'External Source: 5',
    'External Source: 6': 'External Source: 6',
    'External Files: %d': 'External Files: %d',
    'External Plug-ins': 'External Plug-ins',
    'Externally Clocked': 'Externally Clocked',

    # ==================================================================
    # reversed
    # ==================================================================
    'Grace Notes': 'Nốt Grace',
    'Grace Notes and Ties': 'Nốt Grace và dấu nối',
    'Guitar Symbol': 'Ký hiệu Guitar',
    'Glue All Following Events': 'Dán nối tất cả Event phía sau',
    'Glue Segments': 'Dán nối Segment',
    'Global Snapshot: Store': 'Snapshot toàn cục: Lưu',
    'Global Tracks': 'Track toàn cục',
    'Go to Next Controller': 'Tới Controller kế tiếp',
    'Go to Previous Controller': 'Tới Controller liền trước',
    'Folding: Tracks To Folder': 'Folding: Track vào Folder',
    'Follow Track List': 'Bám theo danh sách Track',
    'Filter Notes': 'Lọc Note',
    'Fill Range from Clipboard': 'Lấp dải từ Clipboard',
    'Error Messages': 'Thông báo lỗi',
    'Equalizer Curve': 'Đường cong Equalizer',
    'Erase Destination': 'Xóa đích đến',

    # ==================================================================
    # "Fill" left in English next to a translated sibling
    # ==================================================================
    'Fill Gaps on Selected Tracks': 'Lấp chỗ trống trên Track đã chọn',
    'Fill To End': 'Lấp tới cuối',
    'Fill To Punch': 'Lấp tới điểm Punch',
    'Fill To Start': 'Lấp tới đầu',
    'Fill to Project End': 'Lấp tới cuối Project',
    'Fill to Punch-in Point': 'Lấp tới điểm Punch-in',
    'Fill to Start Point': 'Lấp tới điểm đầu',
    'Filter Hitpoints by Intensity': 'Lọc Hitpoint theo cường độ',
    'Filter Hitpoints by Peak Level': 'Lọc Hitpoint theo mức đỉnh',
    'Filter markers': 'Lọc Marker',
    'Filters': 'Các Filter',

    # ==================================================================
    # Erase read as "xo tay" - and the Delete Tool key already had it right
    # ==================================================================
    'Erase': 'Xóa',
    'Erase After': 'Xóa sau',
    'Erase Before': 'Xóa trước',
    'Erase Destination': 'Xóa đích đến',
    'Erase End Character': 'Xóa ký tự cuối',
    'Erase Front Character': 'Xóa ký tự đầu',
    'Erase Tool': 'Xóa công cụ',
    'Find Loaded Instruments': 'Tìm Instrument đã nạp',
    'Find Tracks': 'Tìm Track',
    'Find Missing Files...': 'Tìm File thiếu...',
    'Finding maximum...': 'Đang tìm giá trị lớn nhất...',
    'Finishing Recording...': 'Đang hoàn tất ghi...',
    'Failed to create archive!': 'Không thể tạo archive!',
    'Fewer Tensions': 'Ít Tension hơn',
    'Fetch Device State': 'Lấy trạng thái Device',
    'Feet\'n\'Frames Count from Project Start':
        'Đếm Feet\'n\'Frames từ đầu Project',
    'Generate Custom Timecode': 'Tạo Timecode tùy chỉnh',
    'Generate Steps': 'Tạo các Step',
    'Expression Maps': 'Expression Maps',
    'Expression Map: Articulations': 'Expression Map: Articulations',
    'Exports the video with main overlay': 'Export Video với Main Overlay',
    'Exports the video with top overlay': 'Export Video với Top Overlay',
    'Extracted Channels': 'Các Channel đã trích xuất',
    'Extract to Lanes': 'Trích xuất sang Lane',
    'Extract to Track': 'Trích xuất sang Track',
    'Extensions': 'Extensions',
    'Exclude Row': 'Loại trừ hàng',
    'Exchange?': 'Hoán đổi?',
    'Equal Power': 'Bằng công suất',
    'Equalizers': 'Các Equalizer',
    'Error creating Project Preview': 'Lỗi khi tạo Project Preview',
    'Error exporting track': 'Lỗi khi export Track',
    'Fades Brightness': 'Độ sáng Fade',
    'Files': 'Các File',
    'Frames': 'Các Frame',
    'Folders': 'Các thư mục',
    'Focus Quick Controls': 'Tập trung Quick Controls',
    'Focus Quick Controls Indicator': 'Chỉ báo Focus Quick Controls',
    'Focus Quick Controls Lock State: %s':
        'Trạng thái khóa Focus Quick Controls: %s',
    'Focus Modes': 'Các chế độ Focus',
    'Flatten Arranger Track': 'Làm phẳng Arranger Track',
    'First Repeat of Current Chain Step':
        'Repeat đầu tiên của Chain Step hiện tại',
    'Follow Time Signature Denominator':
        'Bám theo mẫu số của số chỉ nhịp',
    'Full (I-IV-V-I)': 'Đầy (I-IV-V-I)',
    'Full Randomization': 'Ngẫu nhiên hóa hoàn toàn',
    'Full Vertical': 'Toàn bộ theo chiều dọc',
    'Hermode Tuning': 'Hermode Tuning',
    'Hardware Unit': 'Hardware Unit',
    'Hidden Controllers': 'Các Controller đang ẩn',
    'Hidden Controls': 'Các Control đang ẩn',
    'Hidden Noteheads': 'Các đầu nốt đang ẩn',
    'Hide Data When Expanded': 'Ẩn dữ liệu khi mở rộng',
    'Hide Keyboard Preview': 'Ẩn xem trước bàn phím',
    'Hi-hat (pedal)': 'Hi-hat (pedal)',
    'Hardware Version': 'Phiên bản phần cứng',
    'Global Workspaces': 'Các Workspace toàn cục',
    'From Value1': 'Từ giá trị 1',
    'From Value2': 'Từ giá trị 2',
    'From Value3': 'Từ giá trị 3',
    'Equal Pitch - all Octaves': 'Cùng Pitch - tất cả octave',
    'Equal Pitch - same Octave': 'Cùng Pitch - cùng octave',
    'Enter Script Creator Name': 'Nhập tên Script Creator',
    'Enter Text': 'Nhập văn bản',
    'Enter Title': 'Nhập tiêu đề',
    'Enter Vendor Name': 'Nhập tên nhà cung cấp',
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
