#!/usr/bin/env python3
"""Round 14 of reading: the C-D block of the general catch-all.

Seven slices, 860..1560, about 700 labels. The same four families as round 13,
plus three that only show up in this stretch.

Punctuation moved:

  "CC: Modulation"            -> "CC Modulation"      (the colon was dropped)
  "Checked Chains ...."       -> "Checked Chains..."  (one dot of four gone)
  "Database creation failed." -> "Tao co so du lieu that bai."  (no full stop)
  "Create new Project ?"      -> "Tao ? Project"      (the ? jumped into
                                                       the middle of the clause)
  "Ch."                       -> "Ch"                 (the dot was dropped)

Words lost that carry the sense:

  "Create New Chain"           -> "Tao Chain"
  "Create New Project"         -> "Tao Project"
  "Create New Drum Track"      -> "Tao Drum Track"
  "Create New Sampler Track"   -> "Tao Sampler Track"
  "Date + Time"                -> "Thoi gian Date +"
  "Date / Time"                -> "Thoi gian Date /"

  The first four dropped "New" while their siblings - "Create New Folder",
  "Create New MIDI Device", "Create New Version", "Create New Arranger Chain" -
  kept it. The last two are worse: the value no longer says what is being
  created, it says "time" and then a dangling sign.

Reversed, again the AGENT.md section 2 shape:

  "Chase Events"       -> "Event Chase"
  "Capture Events"     -> "Event Capture"
  "Capture Event Types"-> "Loai Capture Event"
  "Copied Files"       -> "File Copied"
  "Date Created"       -> "Created Ngay"
  "Date Modified"      -> "Modified Ngay"
  "Clip Detected"      -> "Phat hien Clip"
  "Color Indicator"    -> "Mau Chi bao"
  "Creating Tracks..." -> "Track Creating..."
  "Currently Selected Parameter" -> "Tham so Currently Selected"
  "Controller and Event Types"   -> "Loai Controller va Event"
  "Controller Brightness"        -> "Controller Do sang"
  "Control No."                  -> "Dieu khien Khong"   ("No." read as
                                                           the word "no")

And the Control Link family, where "Control Link" had been turned into
"Dieu khien Link" - which reads as a Link being controlled, the opposite of
what it is:

  "Control Link: Edit Control Link Settings"   -> "Cai dat Control Link: Edit..."
  "Control Link: Next Control Link Group"      -> "Dieu khien Link: Next..."

Two of those are untranslated English sitting in the middle of a Vietnamese
sentence ("Next Control Link Group", "Reset All Controllers" under a "CCMode:"
prefix, "Currently assigned parameter"), which is the shape the audit calls
untranslated-word leakage.

Also: the "Controller Lane Setup" family spelled its base label "Cai dat" and
its sixteen numbered children "Thiet lap"; "Deactivate All X States" spelled
three of the four "Huy" (cancel) and one "Tat"; "Delete Automation Spikes"
said "dinh nhon" in one key and "gai" in the other; and three of the six
"Dark <colour>" labels kept the English colour while the other three were
translated.

  python tools/fix_reading14.py
  python tools/fix_reading14.py --write
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
    'CC: Modulation': 'CC: Modulation',
    'Checked Chains ....': 'Checked Chains ....',
    'Database creation failed.': 'Không thể tạo cơ sở dữ liệu.',
    'Create new Project ?': 'Tạo Project mới ?',
    'Ch.': 'Ch.',
    'Create New Chain': 'Tạo Chain mới',
    'Create New Project': 'Tạo Project mới',
    'Create New Drum Track': 'Tạo Drum Track mới',
    'Create New Sampler Track': 'Tạo Sampler Track mới',
    'Create new Project for "%s"?': 'Tạo Project mới cho "%s"?',
    'Date + Time': 'Ngày + giờ',
    'Date / Time': 'Ngày / giờ',
    'Date Created': 'Ngày tạo',
    'Date Modified': 'Ngày sửa',
    'Chase Events': 'Chase Event',
    'Capture Events': 'Capture Event',
    'Capture Event Types': 'Các loại Event được Capture',
    'Copied Files': 'Các File đã sao chép',
    'Clip Detected': 'Đã phát hiện Clip',
    'Color Indicator': 'Chỉ báo màu',
    'Creating Tracks...': 'Đang tạo Track...',
    'Currently Selected Parameter': 'Tham số đang chọn',
    'Currently assigned parameter': 'Tham số đang gán',
    'Controller and Event Types': 'Các loại Controller và Event',
    'Controller Brightness': 'Độ sáng Controller',
    'Controller Catch Range': 'Vùng Catch của Controller',
    'Control No.': 'Số Control',
    'Control Parameter Assignment': 'Gán tham số Control',
    'Center L/R channels': 'Căn giữa Channel Trái/Phải',
    'Center Width': 'Độ rộng trung tâm',
    'Centered on Barline': 'Căn theo vạch nhịp',
    'Chain Step Repeat Change': 'Thay đổi lặp của Chain Step',
    'Correct Segment End': 'Sửa cuối Segment',
    'Correct Segment Start': 'Sửa đầu Segment',
    'Cell Info': 'Thông tin ô',
    'Count Change': 'Thay đổi số đếm',
    'Create Unique Name': 'Tạo tên duy nhất',
    'Decrement Event Volume': 'Giảm âm lượng của Event',
    'Decrement Volume in dB': 'Giảm âm lượng tính bằng dB',
    'Control Link: Edit Control Link Settings': 'Control Link: Sửa cài đặt Control Link',
    'Control Link: Next Control Link Group': 'Control Link: Control Link Group kế tiếp',
    'Control Link: Previous Control Link Group': 'Control Link: Control Link Group liền trước',
    'CCMode: Reset All Controllers': 'CCMode: Reset All Controller',
    'Deactivate All Listen States': 'Tắt tất cả trạng thái Listen',
    'Deactivate All Mute States': 'Tắt tất cả trạng thái Mute',
    'Deactivate All Solo': 'Tắt tất cả Solo',
    'Deactivate All Solo States': 'Tắt tất cả trạng thái Solo',
    'Controller Lane Setup': 'Thiết lập Controller Lane',
    'Controller Lanes': 'Các Controller Lane',
    'Controllers': 'Các Controller',
    'Delete Automation Spikes': 'Xóa gai Automation',
    'Delete Automation Spikes of Selected Tracks': 'Xóa gai Automation của các Track đã chọn',
    'Delete Collection': 'Xóa Collection',
    'Dark Green': 'Tối Xanh lá',
    'Dark Magenta': 'Tối Đỏ tươi',
    'Dark Orange': 'Tối Cam',
    'Customized': 'Tùy chỉnh',
    'Count-In': 'Count-In',
    'Click & Count-in': 'Click & Count-In',
    'Click & Count-in & Click Pattern': 'Click & Count-In & Click Pattern',
    'Count-In Click Count': 'Số lần Click của Count-In',
    'Create Lanes from Versions': 'Tạo Lane từ Version',
    'Create Tracks from Lanes': 'Tạo Track từ Lane',
    'Create Versions from Lanes': 'Tạo Version từ Lane',
    'Create MIDI Notes from Hitpoints': 'Tạo Note MIDI từ Hitpoint',
    'Create Markers from Hitpoints': 'Tạo Marker từ các Hitpoint',
    'Create Regions': 'Tạo Region',
    'Create Regions from Hitpoints': 'Tạo Region từ các Hitpoint',
    'Copy Arranger Events': 'Sao chép Arranger Event',
    'Copy Steps to Lane': 'Sao chép Step vào Lane',
    'Copy Files': 'Sao chép file',
    'Convert Channels': 'Chuyển đổi Channel',
    'Convert Channels...': 'Chuyển đổi Channel...',
    'Convert Tracks': 'Chuyển đổi Track',
    'Delete Source Tracks': 'Xóa Source Track',
    'Delete Segments': 'Xóa Segment',
    'Define Bars': 'Định nghĩa các Bar',
    'Crossfades': 'Các Crossfade',
    'Channels': 'Các Channel',
    'Convert Hitpoints to MIDI Notes': 'Chuyển đổi Hitpoint sang Note MIDI',
    'Convert MIDI to Articulations': 'Chuyển đổi MIDI sang Articulation',
    'Convert Pattern Event to MIDI Part': 'Chuyển đổi Pattern Event sang MIDI Part',
    'Convert RPN/NRPN to single Events': 'Chuyển đổi RPN/NRPN thành các Event riêng',
    'Copy Click Pattern to Clipboard': 'Sao chép Click Pattern vào Clipboard',
    'Copy To Clipboard': 'Sao chép vào Clipboard',
    'Copy to Clipboard': 'Sao chép vào Clipboard',
    'Copy to Active Project Folder': 'Sao chép vào thư mục Project đang hoạt động',
    'Change Type...': 'Đổi loại...',
    'Change Font Styles': 'Đổi kiểu phông chữ',
    'Change Paragraph Styles': 'Đổi kiểu đoạn văn',
    'Change Velocities': 'Đổi Velocity',
    'Cannot convert effect:': 'Không thể chuyển đổi Effect:',
    'Cannot convert effect: %s': 'Không thể chuyển đổi Effect: %s',
    'Cannot convert scopes references!': 'Không thể chuyển đổi tham chiếu scopes!',
    'Canceled': 'Đã hủy',
    'Checked': 'Đã kiểm tra',
    'Checking Licenses...': 'Đang kiểm tra License...',
    'Checksum': 'Mã kiểm tra',
    'Conflicts': 'Xung đột',
    'Consolidate': 'Gộp',
    'Constrain Direction': 'Giới hạn hướng',
    'Constraint Direction': 'Hướng ràng buộc',
    'Content Summary': 'Tóm tắt Content',
    'Conversion failed!': 'Chuyển đổi thất bại!',
    'Compression Factor': 'Hệ số Compression',
    'Compute Scales': 'Tính Scale',
    'Define New...': 'Định nghĩa mới...',
    'Define Stereo as Dual Mono': 'Định nghĩa Stereo thành Dual Mono',
    'Defined': 'Đã định nghĩa',
    'Definition': 'Định nghĩa',
    'Definitions': 'Các định nghĩa',
    'Decreasing Stepwise': 'Giảm dần từng bậc',
    'Deactivate Additional Outputs': 'Tắt đầu ra bổ sung',
    'Delete Log Entry from List': 'Xóa mục Log khỏi danh sách',
    'Delete Path': 'Xóa đường dẫn',
    'Delete Step Backward': 'Xóa Step lùi',
    'Create Initial Parameter Events': 'Tạo Event tham số ban đầu',
    'Create Label Field': 'Tạo trường Label',
    'Create Multiple': 'Tạo nhiều mục',
    'Create New': 'Tạo mới',
    'Create Custom MIDI Controller Surface': 'Tạo MIDI Controller Surface tùy chỉnh',
    'Create Subfolder for Artist': 'Tạo thư mục con cho Nghệ sĩ',
    'Create part using regions?': 'Tạo Part bằng các region?',
    'Could not join project.': 'Không thể tham gia Project.',
    'Could not share project.': 'Không thể chia sẻ Project.',
    'Could not read keycommands': 'Không thể đọc key command',
    'Could not mount database.': 'Không thể mount database.',
    'Could not unmount database.': 'Không thể unmount database.',
    'Color Name': 'Tên màu',
    'Color Setup': 'Thiết lập màu',
    'Computer Keyboard Input On/Off': 'Bật/Tắt đầu vào bàn phím máy tính',
    'Choose Metronome Sound': 'Chọn âm thanh Metronome',
    'Choose from existing Playback Techniques': 'Chọn từ các Playback Technique hiện có',
    'Choose Location': 'Chọn vị trí',
    'Choose location': 'Chọn vị trí',
    'Delay in ms': 'Trễ tính bằng ms',
    'Default Author Name': 'Tên tác giả mặc định',
    'Default Company Name': 'Tên công ty mặc định',
    'Default Noteheads': 'Đầu nốt mặc định',
    'Default Paper Size Type': 'Loại khổ giấy mặc định',
    'Default Track Time Type': 'Loại thời gian Track mặc định',
    'Default Text Font': 'Font văn bản mặc định',
    'Default Color Schemes': 'Các bảng màu mặc định',
    'Delete Version': 'Xóa Version',
    'Delete Tool': 'Xóa công cụ',
    'Click Sound Presets': 'Preset âm thanh của Click',
    'Click Sounds': 'Âm thanh của Click',
    'Currently used in the following sound slots:\\n%s': 'Đang được dùng trong các Sound Slot sau:\\n%s',
    'Check Files': 'Tìm File thiếu',
    'Check Mark': 'Dấu Check',
    'Copy %s Setting': 'Sao chép cài đặt %s',
    'Copy All Files to Project Folder': 'Sao chép tất cả file vào thư mục Project',
    'Copy End': 'Sao chép kết thúc',
    'Copy Start': 'Sao chép bắt đầu',
    'Copying files to clipboard': 'Đang sao chép file vào clipboard',
    'Create Empty': 'Tạo trống',
    'Controller Script Disabled': 'Controller Script đã tắt',
    'Convert Options': 'Chuyển đổi tùy chọn',
    'Change Cue Sends Levels': 'Đổi mức Cue Send',
    'Change Cue Sends Levels...': 'Đổi mức Cue Send...',
    'Change Engraving Settings': 'Đổi cài đặt Engraving',
    'Change Editor Size': 'Đổi kích thước Editor',
    'Change Event Color': 'Đổi màu Event',
    'Change Instrument Type': 'Đổi loại Instrument',
    'Change Project Colors': 'Đổi màu Project',
    'Change Release Length': 'Đổi độ dài Release',
    'Change Swing Settings': 'Đổi cài đặt Swing',
    'Change Track Color': 'Đổi màu Track',
    'Choose Event Color': 'Chọn màu Event',
    'Choose Function': 'Chọn chức năng',
    'Choose Track Color': 'Chọn màu Track',
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
