#!/usr/bin/env python3
"""Round 25 of reading: the T-U block of the general catch-all.

Five slices, 6060..6560, about 500 labels. The "Time ..." family is the round
22 compound-split defect one level deeper - the head noun was translated and
the modifier left behind, so the value is a Vietnamese word followed by a
stranded English one:

    "Time Code"         -> "Thoi gian Code"
    "Time Correction"   -> "Thoi gian Correction"
    "Time Domain"       -> "Thoi gian Domain"
    "Time Linear"       -> "Thoi gian Tuyen tinh"
    "Time Base Device ID" -> "Thoi gian Base Device ID"
    "Time Signature Design" -> "Thoi gian Signature Design"
    "Time Signature:"   -> "Thoi gian Signature:"
    "Time Signatures"   -> "Thoi gian So chi nhip"   both halves wrong
    "Time Stretch Tool Algorithm" -> "Thoi gian Stretch Tool Algorithm"
    "Time Type mismatch!" -> "Thoi gian Loai mismatch!"
    "Time code input"   -> "Thoi gian code input"

  "Time Type mismatch!" is the extreme: three of the four words moved, and
  "mismatch" is still English. "Thoi gian Loai mismatch!" is not a sentence.

And the reverse inside the same family, which is why the class is worth the
care:

    "Timecode Source"   -> "Timecode Nguon"
    "Timecode Input Scheme" -> "Timecode Dau vao So do"
    "Timecode Relative Position" -> "Vi tri Timecode Relative"

The "Toggle ..." family had drifted the same way - a dozen said "Chuyen doi"
where six said "Bat/tat", and a third set said "Chuyen doi" with the object
left in English:

    "Toggle Logging"        -> "Chuyen doi Logging"
    "Toggle Range Selection"-> "Chuyen doi Range Selection"
    "Toggle Selection"      -> "Chuyen doi Selection"
    "Toggle Step Input"     -> "Chuyen doi Step Input"
    "Toggle Switch"         -> "Chuyen doi Switch"

And "Toggle Read Enable All Tracks" - whose English is "Read Automation for
All Tracks On/Off" - kept the whole English phrase "Read Enable", while
round 13 had already settled the same idea as "Bat/Tat doc cho tat ca Track"
under a different key.

Two strings taken apart:

    "To New Tracks"                      -> "Track To New"
    "Unfreeze Drum Track for editing"    -> "Track Unfreeze Drum cho editing"
    "Unfreeze Sampler Track for editing" -> "Track Unfreeze Sampler cho editing"

And "Trying to match image files..." -> "Trying vao match image files...", the
frame class from round 15, in its purest form yet: an English gerund, a
Vietnamese preposition, and two more English words.

  python tools/fix_reading25.py
  python tools/fix_reading25.py --write
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
    # the "Time ..." family - head translated, modifier stranded
    # ==================================================================
    'Time Base 9-Pin Device ID': 'ID thiết bị Time Base 9 chân',
    'Time Base Device ID': 'ID thiết bị Time Base',
    'Time Code': 'Timecode',
    'Time Correction': 'Time Correction',
    'Time Domain': 'Time Domain',
    'Time Linear': 'Time Linear',
    'Time Offset': 'Lệch thời gian',
    'Time Offset (Bars + Beats)': 'Lệch thời gian (Bar + Nhịp)',
    'Time Offset (Bars+Beats)': 'Lệch thời gian (Bar+Nhịp)',
    'Time Offset On/Off': 'Bật/Tắt lệch thời gian',
    'Time Signature Design': 'Thiết kế số chỉ nhịp',
    'Time Signature:': 'Số chỉ nhịp:',
    'Time Signatures': 'Số chỉ nhịp',
    'Time Stretch Tool Algorithm': 'Thuật toán công cụ Time Stretch',
    'Time Type mismatch!': 'Loại thời gian không khớp!',
    'Time code input': 'Nhập time code',
    'Time Displays': 'Hiển thị thời gian',
    'Timecode In': 'Timecode In',
    'Timecode Input': 'Timecode đầu vào',
    'Timecode Input Scheme': 'Sơ đồ Timecode đầu vào',
    'Timecode Relative Position': 'Vị trí Timecode tương đối',
    'Timecode Source': 'Nguồn Timecode',

    # ==================================================================
    # the "To ..." family
    # ==================================================================
    'To Back': 'Về phía sau',
    'To Background': 'Về nền',
    'To Front': 'Về phía trước',
    'To New Tracks': 'Tới Track mới',
    'To Origin': 'Tới điểm gốc',
    'To Polyphonic Voices': 'Tới các bè đa thanh',
    'To Previous Available Position': 'Tới vị trí khả dụng liền trước',

    # ==================================================================
    # the "Toggle ..." family
    # ==================================================================
    'Toggle Auto Apply': 'Bật/tắt áp dụng tự động',
    'Toggle Clip Musical Mode': 'Chuyển đổi chế độ Musical của Clip',
    'Toggle Computer Keyboard Input':
        'Chuyển đổi đầu vào bàn phím máy tính',
    'Toggle Inspector Footer Tabs': 'Chuyển đổi thẻ Footer của Inspector',
    'Toggle Inspector Tabs': 'Chuyển đổi thẻ Inspector',
    'Toggle Logging': 'Chuyển đổi ghi nhật ký',
    'Toggle Musical Mode': 'Chuyển đổi chế độ Musical',
    'Toggle Range Selection': 'Chuyển đổi chọn vùng',
    'Toggle Selected Track': 'Chuyển đổi Track đã chọn',
    'Toggle Selection': 'Chuyển đổi vùng chọn',
    'Toggle Round Brackets': 'Chuyển đổi dấu ngoặc tròn',
    'Toggle Square Brackets': 'Chuyển đổi dấu ngoặc vuông',
    'Toggle Step Input': 'Chuyển đổi đầu vào Step',
    'Toggle Switch': 'Bật/tắt công tắc',
    'Toggle Track List': 'Chuyển đổi danh sách Track',
    'Toggle Enharmonic Spelling': 'Chuyển đổi chính tả cảm điệu',
    'Toggle between Track View and Meter View':
        'Chuyển đổi giữa chế độ xem Track và chế độ xem Meter',
    'Toggle Edit Group on Selected Tracks':
        'Chuyển đổi Group sửa trên Track đã chọn',
    'Toggle Read Enable All Tracks': 'Bật/tắt đọc cho tất cả Track',
    'Toggle Read Enable Selected Tracks': 'Bật/tắt đọc cho Track đã chọn',
    'Toggle Write Enable All Tracks': 'Bật/tắt ghi cho tất cả Track',
    'Toggle Write Enable Selected Tracks': 'Bật/tắt ghi cho Track đã chọn',

    # ==================================================================
    # the "Track ..." family
    # ==================================================================
    'Track Name Font Weight': 'Độ đậm font của tên Track',
    'Track Name Width': 'Chiều rộng tên Track',
    'Track Operation': 'Thao tác Track',
    'Track Pictures': 'Hình ảnh Track',
    'Track Pictures Browser': 'Trình duyệt hình ảnh Track',
    'Track Preset: Open Browser': 'Track Preset: Mở trình duyệt',
    'Track Preset: Previous': 'Track Preset liền trước',
    'Track Quick Controls': 'Quick Control của Track',
    'Track Selection': 'Chọn Track',
    'Track Templates': 'Mẫu Track',
    'Track Title': 'Tiêu đề Track',
    'Track Type Default Colors': 'Màu mặc định theo loại Track',
    'Track Versions': 'Các phiên bản Track',
    'TrackVersions': 'Các phiên bản Track',
    'Track Instruments': 'Instrument của Track',
    'Track Display Settings: Toggle Modes':
        'Cài đặt hiển thị Track: đảo chế độ',
    'Track Data to be Imported': 'Dữ liệu Track cần import',
    'Tracks': 'Các Track',
    'Tracks from Project...': 'Track từ Project...',
    'Tracks are recording!': 'Các Track đang ghi!',
    'Tool Buttons': 'Nút công cụ',
    'Tool Modifiers': 'Modifier của công cụ',
    'Trim Events': 'Trim Event',
    'Trim Start': 'Đầu Trim',
    'Trill Line': 'Vạch Trill',
    'Transpose Notes': 'Transpose các Note',
    'Transpose notes': 'Transpose các Note',
    'Transpose to Root Key': 'Transpose tới Root Key',
    'Transpose Pads': 'Transpose các Pad',
    'Transpose Palette': 'Transpose bảng màu',
    'Transpose by Semitones': 'Transpose theo nửa cung',
    'Transposed Pitch': 'Cao độ đã Transpose',
    'Transpose Modifiers': 'Modifier của Transpose',
    'Transpose Lock': 'Khóa Transpose',
    'Transpose All': 'Transpose tất cả',
    'Transpose All Maps in Project': 'Transpose tất cả Map trong Project',
    'Transpose All Pads': 'Transpose tất cả Pad',
    'Transpose All Remote Triggers': 'Transpose tất cả Trigger Remote',
    'Transpose Up': 'Transpose lên',
    'Transpose Down': 'Transpose xuống',
    'Triads': 'Hợp âm ba nốt',
    'Triads with maj9': 'Hợp âm ba nốt với maj9',
    'Triads with maj9 and min9': 'Hợp âm ba nốt với maj9 và min9',
    'Tremolos': 'Các Tremolo',
    'Tune Down Half-Step': 'Cân chỉnh xuống nửa cung',
    'Tune Up Half-Step': 'Cân chỉnh lên nửa cung',
    'Type of New Controller Events': 'Loại Event của Controller mới',
    'Unassigned Key': 'Key chưa gán',
    'Undefined Value': 'Giá trị chưa xác định',
    'Unexpected Error': 'Lỗi ngoài dự kiến',
    'Unfold Tracks': 'Mở Track',
    'Unfreeze Drum Track for editing': 'Bỏ Freeze Drum Track để sửa',
    'Unfreeze Sampler Track for editing': 'Bỏ Freeze Sampler Track để sửa',
    'Unchanged (defaults)': 'Không đổi (mặc định)',
    'Touch (Control)': 'Touch (Control)',

    # ==================================================================
    # an English gerund with a Vietnamese preposition wedged into it
    # ==================================================================
    'Trying to match image files...': 'Đang đối chiếu các file hình ảnh...',
    'Total': 'Tổng',
    'Total Recorded': 'Tổng đã ghi',
    'Total Size: %s': 'Tổng kích thước: %s',
    'Transmit to Hardware': 'Truyền sang phần cứng',
    'Timecode positions': 'Các vị trí Timecode',
    'Tremolo': 'Tremolo',
    'Trim': 'Trim',
    'Top Track': 'Track trên',
    'Touch': 'Touch',
    'Touch Collect Assistant': 'Trợ lý Touch Collect',
    'Touch Collect Assistant Disabled': 'Trợ lý Touch Collect đã bị tắt',
    'Touch Collect Assistant Enabled': 'Trợ lý Touch Collect đã bật',
    'Tuning': 'Tuning',
    'Try again': 'Thử lại',
    'Try to Recognize Device': 'Thử nhận diện thiết bị',
    'True Peak Level': 'Mức True Peak',
    'Type Is': 'Loại là',
    'Two Rows': 'Hai hàng',
    'Tuned Percussion': 'Bộ gõ có cao độ',
    'Unchanged (defaults)': 'Không đổi (mặc định)',
    'Undo': 'Hoàn tác',
    'Unique ID': 'ID duy nhất',
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
