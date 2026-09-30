#!/usr/bin/env python3
"""Round 29 of reading: the R block, the third gap.

Slices 4460 to 4860, 400 labels - and it is almost entirely three families,
"Remove ...", "Rename ..." and "Reset ...", about 150 keys between them. The
"Remove" family had "Selected" left in English in six keys and the noun left in
English in another dozen:

    "Remove Selected Tracks"      -> "Gos bo Selected Tracks"
    "Remove Selected Effects"     -> "Gos bo Selected Effects"
    "Remove Selected Instruments" -> "Gos bo Selected Instruments"
    "Remove Selected Mappings"    -> "Gos bo Selected Mappings"
    "Remove Parameters"           -> "Gos bo Parameters"
    "Remove Value"                -> "Gos bo Value"
    "Remove Variable"             -> "Gos bo Variable"
    "Remove Property"             -> "Gos bo Property"
    "Remove Write Protection"     -> "Gos bo Write Protection"

"Reset" was the same, and worse, because the sibling three keys along had been
done properly:

    "Reset Pitch Changes"                     -> "Dat lai thay doi Pitch"  ok
    "Reset Pitch Changes for Selection"       -> "Dat lai Pitch Changes cho Selection"
    "Reset Pitch Curve Changes"               -> "Dat lai Pitch Curve Changes"
    "Reset Volume Changes"                    -> "Dat lai Volume Changes"
    "Reset Volume Changes for Selection"      -> "Dat lai Changes am luong cho Selection"

The last one is a scramble: "Changes" and "am luong" have exchanged places, so
it reads "reset changes-volume for selection".

Two more taken apart whole:

    "Replace All Events and Parts"     -> "Part Replace All Events and"
    "Replace Recording in Editors"     -> "Editor Replace Recording in"
    "Restore Default Setup"             -> "Thiet lap Restore Default"
    "Restore Factory Presets"          -> "Preset Restore Factory"
    "Reload Track Preset"              -> "Preset Reload Track"
    "Resolve Missing Files"            -> "File Resolve Missing"
    "Reveal Parameter on Write"        -> "Tham so Reveal tren Write"
    "Resulting Video Files"            -> "File Resulting Video"

And one word read as a different word, for the third time in this project:

    "Replace Search String" -> "Thay the Tim kiem Day dan"

  Search String is the text you are searching for. "Day dan" is a guitar string.
  The same word has now been read three ways in three rounds: "dây đàn" for a
  MIDI String, "String" for a MIDI String, and now "dây đàn" for a text string.

"Factory" had four renderings: "xuất xưởng", "từ nhà sản xuất", "Factory", and
a sentence that mixed two of them. Unified on "Factory", which is what round 26
settled and what the AGENT.md rule about DAW terms says.

  python tools/fix_reading29.py
  python tools/fix_reading29.py --write
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
    # the "Remove ..." family
    # ==================================================================
    'Remove "%s" as Monitor Source': 'Gỡ bỏ "%s" làm Monitor Source',
    'Remove Group "%s" as Monitor Source':
        'Gỡ bỏ Group "%s" làm Monitor Source',
    'Remove Input "%s" as Monitor Source':
        'Gỡ bỏ Input "%s" làm Monitor Source',
    'Remove Output "%s" as Monitor Source':
        'Gỡ bỏ Output "%s" làm Monitor Source',
    'Remove All Assignments': 'Gỡ bỏ tất cả phép gán',
    'Remove Assignment': 'Gỡ bỏ phép gán',
    'Remove Alternative Key Set': 'Gỡ bỏ bộ Key Set thay thế',
    'Remove Aspect': 'Gỡ bỏ MediaBay Aspect',
    'Remove Current Tab': 'Gỡ bỏ thẻ hiện tại',
    'Remove Default Preset': 'Gỡ bỏ Preset mặc định',
    'Remove Event Volume Curve': 'Gỡ bỏ đường cong âm lượng Event',
    'Remove Extension from Selected Events':
        'Gỡ bỏ Extension khỏi các Event đã chọn',
    'Remove Extension from Selected Track':
        'Gỡ bỏ Extension khỏi Track đã chọn',
    'Remove Favorite': 'Gỡ bỏ mục yêu thích',
    'Remove Filter': 'Gỡ bỏ bộ lọc',
    'Remove filter': 'Gỡ bỏ bộ lọc',
    'Remove Group Track "%s"': 'Gỡ bỏ Group Track "%s"',
    'Remove Hitpoints': 'Gỡ bỏ các Hitpoint',
    'Remove Inactive': 'Gỡ bỏ mục không hoạt động',
    'Remove Individual Settings': 'Gỡ bỏ cài đặt riêng',
    'Remove Legato from Steps': 'Gỡ bỏ Legato khỏi các Step',
    'Remove Link Group "%s"': 'Gỡ bỏ Link Group "%s"',
    'Remove Overlaps': 'Gỡ bỏ các phần chồng lấn',
    'Remove Parameter': 'Gỡ bỏ tham số',
    'Remove Parameters': 'Gỡ bỏ tham số',
    'Remove Property': 'Gỡ bỏ thuộc tính',
    'Remove Regions/Hitpoints on all Offline Processes':
        'Gỡ bỏ Region/Hitpoint trên mọi Offline Process',
    'Remove Selected Busses': 'Gỡ bỏ các Bus đã chọn',
    'Remove Selected Effects': 'Gỡ bỏ các Effect đã chọn',
    'Remove Selected Instruments': 'Gỡ bỏ các Instrument đã chọn',
    'Remove Selected Mappings': 'Gỡ bỏ các Mapping đã chọn',
    'Remove Selected Sound Reference': 'Gỡ bỏ Sound Reference đã chọn',
    'Remove Selected Tracks': 'Gỡ bỏ các Track đã chọn',
    'Remove Signature': 'Gỡ bỏ số chỉ nhịp',
    'Remove Source Events': 'Gỡ bỏ Source Event',
    'Remove Source Tracks': 'Gỡ bỏ Source Track',
    'Remove Steps': 'Gỡ bỏ các Step',
    'Remove Takes': 'Gỡ bỏ các Take',
    'Remove Touched': 'Gỡ bỏ mục đã điều chỉnh',
    'Remove Unused Files': 'Gỡ bỏ các file không dùng',
    'Remove Unused Parameters': 'Gỡ bỏ tham số không dùng',
    'Remove Value': 'Gỡ bỏ giá trị',
    'Remove Variable': 'Gỡ bỏ biến',
    'Remove Write Protection': 'Gỡ bỏ bảo vệ ghi',
    'Remove all Steps from Pattern': 'Gỡ bỏ tất cả Step khỏi Pattern',
    'Remove all Steps from Step Lane': 'Gỡ bỏ tất cả Step khỏi Step Lane',
    'Remove all control assignments?': 'Gỡ bỏ tất cả phép gán Control?',
    'Removes Silent Segments': 'Gỡ bỏ các Segment im lặng',
    'Remove Fades': 'Xóa các Fade',

    # ==================================================================
    # the "Rename ..." family
    # ==================================================================
    'Rename Configuration': 'Đổi tên cấu hình',
    'Rename Events': 'Đổi tên Event',
    'Rename Favorite': 'Đổi tên mục yêu thích',
    'Rename Range Events': 'Đổi tên Event trong vùng',
    'Rename Selected Events': 'Đổi tên Event đã chọn',
    'Rename Selected Events...': 'Đổi tên Event đã chọn...',
    'Remote key for 1st section': 'Phím Remote cho phần thứ nhất',
    'Remote key for 2nd section': 'Phím Remote cho phần thứ hai',
    'Remote key for 3rd section': 'Phím Remote cho phần thứ ba',
    'Remote key for 4th section': 'Phím Remote cho phần thứ tư',
    'Remote key for 5th section': 'Phím Remote cho phần thứ năm',
    'Remote key for 1st subsection': 'Phím Remote cho Subsection thứ nhất',
    'Remote key for 2nd subsection': 'Phím Remote cho Subsection thứ hai',
    'Remote key for 3rd subsection': 'Phím Remote cho Subsection thứ ba',
    'Remote key for 4th subsection': 'Phím Remote cho Subsection thứ tư',
    'Remote key for 5th subsection': 'Phím Remote cho Subsection thứ năm',
    'Recent Paths': 'Đường dẫn gần đây',
    'Recent Projects': 'Các Project gần đây',
    'Read for All Tracks': 'Đọc cho tất cả Track',
    'Read Automation On/Off': 'Bật/Tắt đọc Automation',
    'Read machine position from selected source':
        'Đọc vị trí máy từ nguồn đã chọn',
    'Reading MIDI Devices': 'Đang đọc MIDI Device',
    'Reading OpenTL Track Files...': 'Đang đọc các file OpenTL Track...',
    'Reading projects...': 'Đang đọc các Project...',
    'Rating Filter': 'Bộ lọc đánh giá',
    'Ranges': 'Các vùng',
    'Recall Device State': 'Gọi lại trạng thái Device',
    'Refresh Views': 'Làm mới chế độ xem',
    'Reference Files': 'File tham chiếu',
    'Reference Level': 'Mức tham chiếu',
    'Reference Value': 'Giá trị tham chiếu',
    'References': 'Các tham chiếu',
    'Relative Binary Offset': 'Offset nhị phân tương đối',
    'Relative Circular': 'Circular tương đối',
    'Relay Click': 'Click Relay',
    'Release Date': 'Ngày phát hành',
    'Release Lock': 'Bỏ khóa',
    'Release Driver when Application is in Background':
        'Giải phóng Driver khi ứng dụng chạy nền',
    'Reload Scripts': 'Tải lại Script',
    'Reload Track Preset': 'Tải lại Preset Track',
    'Remote Trigger': 'Trigger Remote',
    'Remote Trigger behaviour on release': 'Hành vi Trigger Remote khi thả',
    'Range1Min': 'Range 1 Min.',
    'Range2Max': 'Range 2 Max.',
    'Range2Min': 'Range 2 Min.',
    'Rectangular Noteheads': 'Đầu nốt hình chữ nhật',
    'Reconstruct': 'Dựng lại',
    'Reduce Automation Events': 'Giảm số Event Automation',
    'Reduce Section Height': 'Giảm chiều cao phần',

    # ==================================================================
    # Region and Range had both become "Vung"; Region stays English,
    # which is what the majority of its keys already did
    # ==================================================================
    'Region': 'Region',
    'Region End': 'Cuối Region',
    'Region Start': 'Đầu Region',
    'Region Names': 'Các tên Region',
    'Regions': 'Các Region',

    # ==================================================================
    # the "Reset ..." family
    # ==================================================================
    'Reset %s Setting': 'Đặt lại cài đặt %s',
    'Reset Input Configuration': 'Đặt lại cấu hình Input',
    'Reset MIDI Velocity Variance': 'Đặt lại phân tán Velocity MIDI',
    'Reset Meters': 'Đặt lại các Meter',
    'Reset MixConsole Channels...': 'Đặt lại các MixConsole Channel...',
    'Reset Pitch Changes for Selection': 'Đặt lại thay đổi Pitch cho vùng chọn',
    'Reset Pitch Curve Changes': 'Đặt lại thay đổi đường cong Pitch',
    'Reset Pitch Curve Changes for Selection':
        'Đặt lại thay đổi đường cong Pitch cho vùng chọn',
    'Reset Ports': 'Đặt lại các cổng',
    'Reset Processing Overload Indicator': 'Đặt lại chỉ báo quá tải Processing',
    'Reset Properties': 'Đặt lại thuộc tính',
    'Reset Result Filters': 'Đặt lại bộ lọc kết quả',
    'Reset Search': 'Đặt lại tìm kiếm',
    'Reset Section': 'Đặt lại phần',
    'Reset Section with Warning': 'Đặt lại phần kèm cảnh báo',
    'Reset Selected': 'Đặt lại mục đã chọn',
    'Reset Tilt/Rotate Anchor': 'Đặt lại điểm tựa Tilt/Rotate',
    'Reset Volume Changes': 'Đặt lại thay đổi âm lượng',
    'Reset Volume Changes for Selection':
        'Đặt lại thay đổi âm lượng cho vùng chọn',
    'Reset Current Picture': 'Đặt lại hình ảnh hiện tại',
    'Reset Curve': 'Đặt lại đường cong',
    'Reset Destination Tracks': 'Đặt lại Track đích',
    'Reset Filter': 'Đặt lại bộ lọc',
    'Reset Formant Shift Changes': 'Đặt lại thay đổi Formant Shift',
    'Reset Formant Shift Changes for Selection':
        'Đặt lại thay đổi Formant Shift cho vùng chọn',
    'Reset Click Pattern to Default': 'Đặt lại Click Pattern về mặc định',
    'Reset Color': 'Đặt lại màu',
    'Reset Counter Start Value': 'Đặt lại giá trị bắt đầu của Counter',

    # ==================================================================
    # "Factory" had four renderings
    # ==================================================================
    'Reset to Factory': 'Đặt lại về Factory',
    'Reset to Factory Patterns': 'Đặt lại về Factory Pattern',
    'Reset Color Set to Default': 'Đặt lại bảng màu về mặc định',
    'Reset Color Set to Factory Settings': 'Đặt lại bảng màu về cài đặt Factory',
    'Restore Factory Presets': 'Factory Preset',
    'Restore Default Setup': 'Khôi phục thiết lập mặc định',
    'Restore Defaults': 'Khôi phục mặc định',
    'Restore Default Column Widths': 'Khôi phục độ rộng cột mặc định',
    'Add new profile with factory settings': 'Thêm Profile mới với cài đặt Factory',
    'Get Default Factory Layout': 'Lấy Layout Factory mặc định',
    'Resolve Missing Files': 'Tìm File thiếu',

    # ==================================================================
    # replaced / result / reveal
    # ==================================================================
    'Replace All Events and Parts': 'Thay thế tất cả Event và Part',
    'Replace Recording in Editors': 'Thay thế bản ghi trong Editor',
    'Replace Files': 'Thay thế file',
    'Replace Search String': 'Thay thế chuỗi tìm kiếm',
    'Replace events?': 'Thay thế các Event?',
    'Replace existing Favorite "%s"?': 'Thay thế mục yêu thích "%s" đã có?',
    'Resulting Length': 'Độ dài kết quả',
    'Resulting Length in Samples': 'Độ dài kết quả tính bằng Sample',
    'Resulting Length in Seconds': 'Độ dài kết quả tính bằng giây',
    'Resulting Video Files': 'Các file Video kết quả',
    'Results': 'Các kết quả',
    'Reveal Parameter on Write': 'Hiện tham số khi ghi',
    'Reveal in Finder': 'Hiện trong Finder',
    'Reverse Drum Sound List': 'Đảo danh sách âm thanh Drum',
    'Revert to the previously saved version?':
        'Trở về Version đã lưu trước đó?',
    'Repeat Events': 'Repeat Event',
    'Repeat Line': 'Vạch lặp lại',
    'Repeat Range': 'Vùng lặp lại',
    'Repeat Rate': 'Tỉ lệ lặp lại',
    'Rhythm Dots': 'Các dấu chấm dôi',
    'Rhythmic Slashes': 'Dấu gạch chéo nhịp',
    'Rescan Disk': 'Quét lại đĩa',
    'Rendered files include all source settings.':
        'Các file đã Render bao gồm mọi cài đặt nguồn.',
    'Rendering Range %i of %i': 'Đang Render vùng %i trong %i',
    'Return to Start Position on Stop': 'Return tới vị trí Start khi dừng',
    'Right Divider': 'Divider phải',
    'Reset to Default Notehead': 'Đặt lại về đầu nốt mặc định',
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
