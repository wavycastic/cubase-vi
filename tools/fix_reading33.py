#!/usr/bin/env python3
"""Round 33 of reading: slices 90-270 of the long values.

The short labels are done. Sentences have a defect the short ones do not, and
it is the same defect every round since round 2: the English is inside a
Vietnamese sentence but not yet translated.

    "Click 'Start' to scan for unreferenced files"
      -> "Click 'Start' vao scan cho unreferenced files"
    "Found participants without master: %s. Try to reconnect?"
      -> "Found participants without master: %s. Try vao reconnect?"
    "IP Conflict with client: %s - set client state to logged off."
      -> "IP Conflict voi client: %s - set client state vao logged off"

Three sentences where the only Vietnamese is the word "vao" - a preposition
that has no business being the only word in the line. Two of them are almost
entirely English.

    "Picks up on the value of the %s function as soon as the control reaches
     that value. This results in smooth value changes, but requires you to
     estimate the pickup value."
      -> "... Dieu nay giup thay doi gia tri muot ma hon."

The second half of that sentence was dropped. It is the half that says what
the feature COSTS you - "but requires you to estimate the pickup value" - and
a Cubase user reading the tooltip is not told the price.

    "Please select a project.\\nIn case no projects are online,\\nyou cannot join."
      -> "... ban khong the tham gia."

Also dropped its object. Round 22 fixed "Cannot join project." and round 31
fixed "You can join" - both with the word "Project" in them. This third copy
lost it.

    "Complete Signal Path + Master Effects" -> "... + Effect Master"

Reversed, in a family where "Complete Signal Path" alone was already right.

And the sixth "read a word as a different word", this one a neighbour again:

    "External plug-in is used"     -> "Plug-in ben ngoai dang duoc dung"
    "External files will be..."    -> "Cac file ben ngoai se duoc sao chep"
    "External sync cannot be..."   -> "Dong bo ben ngoai khong the kich hoat"
    "Do Not Connect ... When Loading External Projects"
                                   -> "... Khi tai Project ben ngoai"

"Ben ngoai" is "outside". External is a Cubase term and is kept, in forty-odd
other keys. Four sentences in one panel read it as the opposite.

    "Medium type not supported or invalid medium" -> "Loai Medium khong duoc ho tro"

Medium here is storage media, not "medium" as in average. Sibling "MediaType"
is "Loai Media" - so the map already had it.

    "In Single Voice mode, the notes are mapped to the selected voice
     (monophonic material only)"
      -> "... (chi danh cho am thanh don am)"

"Am thanh don am" is "monophonic SOUND". "Material" is the content being
played - a MIDI file, a Part. Two different nouns, one of them wrong.

  python tools/fix_reading33.py
  python tools/fix_reading33.py --write
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
    # a Vietnamese sentence with one Vietnamese word in it
    # ==================================================================
    "Click 'Start' to scan for unreferenced files":
        "Nhấp 'Start' để quét các file không được tham chiếu",
    'Found participants without master: %s. Try to reconnect?':
        'Tìm thấy các bên tham gia không có master: %s. Thử kết nối lại?',
    'IP Conflict with client: %s - set client state to logged off.':
        'Xung đột IP với client: %s - đặt trạng thái client thành logged off.',

    # ==================================================================
    # a dropped clause - usually the second half of the sentence
    # ==================================================================
    'Picks up on the value of the %s function as soon as the control reaches '
    'that value. This results in smooth value changes, but requires you to '
    'estimate the pickup value.':
        'Bắt giá trị của chức năng %s ngay khi điều khiển đạt tới giá trị đó. '
        'Điều này giúp thay đổi giá trị mượt mà hơn, nhưng đòi hỏi bạn phải '
        'ước lượng giá trị bắt đầu.',
    'Please select a project.\\nIn case no projects are online,\\n'
    'you cannot join.':
        'Vui lòng chọn một Project.\\nTrong trường hợp không có Project nào '
        'trực tuyếp,\\nbạn không thể tham gia Project.',

    # ==================================================================
    # External is a term, "ben ngoai" is its opposite
    # ==================================================================
    'External files will be copied into the working directory!':
        'Các file External sẽ được sao chép vào thư mục làm việc!',
    'External plug-in is used. Freezing will be done in real time.':
        'Plug-in External đang được dùng. Việc Freeze sẽ diễn ra theo thời gian '
        'thực.',
    'External sync cannot be activated because Nuendo is the timecode master.':
        'Không thể kích hoạt External Sync vì Nuendo là Timecode Master.',
    'Do Not Connect Input/Output Busses When Loading External Projects':
        'Không nối Input/Output Bus khi tải Project External',

    # ==================================================================
    # a third noun read as a second noun
    # ==================================================================
    'In Single Voice mode, the notes are mapped to the selected voice '
    '(monophonic material only)':
        'Ở chế độ Single Voice, các nốt được ánh xạ tới bè đã chọn '
        '(chỉ dành cho chất liệu đơn âm)',
    'Error: Medium type not supported or invalid medium!':
        'Lỗi: Loại Media không được hỗ trợ hoặc Media không hợp lệ!',
    'Destination Path is invalid for copying or consolidation':
        'Đường dẫn đích không hợp lệ để sao chép hoặc hợp nhất',
    'Drag to change order of modulators in signal chain':
        'Kéo để đổi thứ tự các Modulator trong chuỗi tín hiệu',
    'Drag to change order of modules in signal path':
        'Kéo để đổi thứ tự các Module trong đường truyền tín hiệu',

    # ==================================================================
    # reversed, and capitals in the middle
    # ==================================================================
    'Complete Signal Path + Master Effects':
        'Toàn bộ đường truyền tín hiệu + Master Effect',
    'Do you really want to remove the mixer bank zone (%s)?':
        'Bạn có thực sự muốn gỡ bỏ Mixer Bank Zone (%s) không?',
    'Do you really want to remove all Quick Control assignments?':
        'Bạn có thực sự muốn gỡ bỏ tất cả phép gán Quick Control không?',
    'Close MIDI Controller Surface Editor and Open Mapping Assistant':
        'Đóng MIDI Controller Surface Editor và mở trợ lý Mapping',
    'Link All Word Clock Outputs (Where matching rate is possible)':
        'Liên kết tất cả đầu ra Word Clock (khi tần số có thể khớp)',
    'Other assigned pads will be transposed when changing the Root Key.':
        'Các Pad khác được gán sẽ được Transpose khi đổi Root Key.',
    'Part/Clip Editing Mode: All Parts/Clips on Active Track':
        'Chế độ sửa Part/Clip: Tất cả Part/Clip trên Track đang hoạt động',
    'Select Active Arranger Chain + Functions':
        'Chọn Arranger Chain đang hoạt động + chức năng',
    'Event cannot be moved.\\nOrigin is before project start.':
        'Event không thể di chuyển.\\nĐiểm gốc nằm trước đầu Project.',
    'No Mappable Controller found, please connect a supported MIDI Controller':
        'Không tìm thấy Controller nào có thể gán, vui lòng kết nối một '
        'MIDI Controller được hỗ trợ',
    'Indicates if Track Quick Controls are active':
        'Chỉ báo nếu Quick Control của Track đang hoạt động',
    'Modulators are not displayed in inactive projects':
        'Modulator không được hiện trong Project không hoạt động',
    'Number of true peak values exceeding reference level':
        'Số giá trị True Peak vượt mức tham chiếu',
    'Reduce Automation Events of Selected Tracks':
        'Giảm số Event Automation của các Track đã chọn',
    'Notes Inside this Range will not be Quantized':
        'Các nốt bên trong Vùng này sẽ không bị Quantize',
    'Extend Playback Range of Notes that start before the Part':
        'Mở rộng vùng phát lại của các nốt bắt đầu trước Part',
    'Fill Gaps with Current Value (Selected Tracks)':
        'Lấp chỗ trống bằng giá trị hiện tại (Track đã chọn)',
    'Get Default Factory Layout/Copy Layout from Other Tab':
        'Lấy Layout Factory mặc định/Sao chép Layout từ thẻ khác',
    'Hide Plug-ins That Are in Active Collection':
        'Ẩn các Plug-in trong Collection đang hoạt động',
    'Remove Unavailable Plug-ins from All Collections':
        'Gỡ bỏ các Plug-in không khả dụng khỏi tất cả Collection',
    'Paste Click Pattern to Selected Signatures':
        'Dán Mẫu Click vào các số chỉ nhịp đã chọn',
    'No MIDI Remote Controller available. Controllers can be imported or '
    'created in the MIDI Remote Manager.':
        'Không có MIDI Remote Controller khả dụng. Controller có thể được '
        'import hoặc tạo trong MIDI Remote Manager.',
    'Script could not be imported. A Script for %s - %s already exists. Use '
    "the 'Delete Script' button first.":
        'Không thể import Script. Một Script cho %s - %s đã tồn tại. Vui lòng '
        "dùng nút 'Xóa Script' trước.",
    'Please update your graphics card driver or switch to a more effective '
    'graphics card.':
        'Vui lòng cập nhật trình điều khiển card đồ họa hoặc chuyển sang card '
        'đồ họa mạnh hơn.',
    'Could not create the Clip Packages folder inside the project folder.':
        'Không thể tạo thư mục Clip Packages bên trong thư mục Project.',
    'Deleted %i inactive versions (of %i tracks)':
        'Đã xóa %i Version không hoạt động (của %i Track)',

    # ==================================================================
    # "X ... on/off. Reset with [CTRL + click]." - eleven near-identical
    # tooltips, all of which said "nhap" for "click"
    # ==================================================================
    'Creating ContentPack (unprotected, no compression)...':
        'Đang tạo ContentPack (không bảo vệ, không nén)...',
    'Database creation failed because the target is write protected.\\n':
        'Tạo cơ sở dữ liệu thất bại vì đích bị bảo vệ ghi.\\n',
    'Dialogue-gated loudness measurement according to ITU-R BS.1770':
        'Đo Loudness theo hội thoại, tuân theo ITU-R BS.1770',
    'Defines what happens AFTER a linear or cycled recording...':
        'Xác định điều gì xảy ra sau khi ghi tuyến tính hoặc ghi theo Cycle...',
    'Disk Cache Overload\\nClick to Reset Display':
        'Quá tải Disk Cache\\nNhấp để đặt lại hiển thị',
    'Processing Overload\\nClick to Reset Display':
        'Quá tải xử lý\\nNhấp để đặt lại hiển thị',
    'Next Chain Step\\nUse [ALT]-Click to jump to last chain step':
        'Chain Step kế tiếp\\nDùng [ALT] + Click để nhảy tới Chain Step cuối '
        'cùng',
    'Previous Chain Step\\nUse [ALT]-Click to jump to first chain step':
        'Chain Step trước\\nDùng [ALT] + Click để nhảy tới Chain Step đầu tiên',
}

# the "Reset with [CTRL + click]." tooltips, all six of which said "nhap"
# for "click" - a word the map uses correctly forty times elsewhere
WORDING.update({
    'Cue Sends Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Cue Send.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Equalizers Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Equalizer.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Inserts Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Insert.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'MIDI Inserts Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass MIDI Insert.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'MIDI Sends Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass MIDI Send.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Pre Filter Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Pre Filter.\\nĐặt lại bằng [CTRL + nhấp chuột].',
})

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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v!r}')

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
