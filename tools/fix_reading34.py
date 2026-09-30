#!/usr/bin/env python3
"""Round 34 of reading: slices 315-405 of the long values.

Three things this round, and the first is the one worth keeping.

MOUSE WHEEL READ AS "SCROLL". Six keys, all of them pad commands:

    "Fewer Tensions ([ALT] - mouse wheel on pad)"
      -> "It Tension hon ([ALT] - cuon chuot tren pad)"
    "Next Voicing (mouse wheel on pad)"
      -> "Voicing ke tiep (cuon chuot tren pad)"
    "Transpose Up ([SHIFT] - mouse wheel on pad)"
      -> "Transpose len ([SHIFT] - cuon chuot tren pad)"

"Cuon" is to SCROLL. A mouse wheel is "con lan chuot", and the map already says
so - round 31's "Use Mouse Wheel for Event Volume and Fades" came out as "Dung
con lan chuot". So the two spellings of the same word coexist, and the
six-command family picked the wrong one.

Same shape as "External" -> "ben ngoai" in round 33, and a different shape
from it: here the map has the RIGHT word in a sibling key. "Scroll to Selected
Channel" -> "Cuon toi Channel da chon" is correct - that key really is about
scrolling. Both words are in the map; only the pads are wrong.

"CHO GHI" vs "BAO VE GHI". Round 31 settled Write Protection = "bao ve ghi",
because two sibling sentences already said it. Four keys kept the older
"chong ghi":

    "The selected folder was write protected!\nDo you want to disable write
     protection and continue?"
      -> "Thu muc da chon bi chong ghi!\nBan co muon tat chong ghi va tiep tuc khong?"

and this one, which is the label the others are derived from:

    "Write protection (a checkmark in this column prevents an ent..."
      -> "Chong ghi (dau tich o cot nay ngan muc khong bi ghi de)"

The label is the parent of the two sentences. Fixing the sentences and not the
label is how the split happened in the first place.

"SO LUONG" WHERE A COUNT IS MEANT. Twenty-one keys, and the class is real:
"Số" is a number, "số lượng" is a QUANTITY. Round 32 fixed seven
"Cannot add more tracks" sentences and missed four of the nine - the audio,
chord, marker and generic ones all still said "Số lượng X Track đã đạt giới hạn".
"N" is a number of items; a message box telling you the limit was reached does
not need a quantity.

  python tools/fix_reading34.py
  python tools/fix_reading34.py --write
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
    # a mouse wheel is a wheel, not a scroll
    # ==================================================================
    'Fewer Tensions ([ALT] - mouse wheel on pad)':
        'Ít Tension hơn ([ALT] - lăn chuột trên Pad)',
    'More Tensions ([ALT] - mouse wheel on pad)':
        'Thêm Tension ([ALT] - lăn chuột trên Pad)',
    'Next Voicing (mouse wheel on pad)': 'Voicing kế tiếp (lăn chuột trên Pad)',
    'Previous Voicing (mouse wheel on pad)':
        'Voicing liền trước (lăn chuột trên Pad)',
    'Transpose Up ([SHIFT] - mouse wheel on pad)':
        'Transpose lên ([SHIFT] - lăn chuột trên Pad)',
    'Transpose Down ([SHIFT] - mouse wheel on pad)':
        'Transpose xuống ([SHIFT] - lăn chuột trên Pad)',

    # ==================================================================
    # Write Protection, and the label the sentences come from
    # ==================================================================
    'The selected folder was write protected!\\nDo you want to disable write '
    'protection and continue?':
        'Thư mục đã chọn bị bảo vệ ghi!\\nBạn có muốn tắt bảo vệ ghi và tiếp tục '
        'không?',
    'The file is write protected! Do you want to replace it anyway?':
        'File bị bảo vệ ghi! Bạn vẫn muốn thay thế nó?',
    'Database removal failed because the database file is write protected.\\n':
        'Xóa cơ sở dữ liệu thất bại vì file cơ sở dữ liệu bị bảo vệ ghi.\\n',
    'Write protection (a checkmark in this column prevents an entry from '
    'being overwritten)':
        'Bảo vệ ghi (dấu tích ở cột này ngăn mục không bị ghi đè)',

    # ==================================================================
    # Serial Port, capitalised - the label already was
    # ==================================================================
    'The serial port %s could not be opened, because it was already opened by '
    'another application.':
        'Không thể mở Cổng Serial %s, vì nó đã được một ứng dụng khác mở.',
    'The serial port %s could not be opened.': 'Không thể mở Cổng Serial %s.',
    'The serial port %s could not be opened. Error code %d':
        'Không thể mở Cổng Serial %s. Mã lỗi %d',

    # ==================================================================
    # "so luong" where a count is meant - the four "Cannot add more
    # tracks" sentences round 32 missed
    # ==================================================================
    'Cannot add more tracks. The audio track count is at the limit.':
        'Không thể thêm Track. Số Audio Track đã đạt giới hạn.',
    'Cannot add more tracks. The chord track count is at the limit.':
        'Không thể thêm Track. Số Chord Track đã đạt giới hạn.',
    'Cannot add more tracks. The marker track count is at the limit.':
        'Không thể thêm Track. Số Marker Track đã đạt giới hạn.',
    'Cannot add more tracks. The track count for this track type is at the '
    'limit.':
        'Không thể thêm Track. Số Track của loại Track này đã đạt giới hạn.',
    'How many frames of timecode are read before starting system':
        'Số Frame Timecode được đọc trước khi khởi động hệ thống',
    'How many frames of timecode must be missing before system is stopped':
        'Số Frame Timecode phải bị thiếu trước khi hệ thống dừng lại',
    'Merge channels: Number of channels within selection must match channel '
    'configuration of selected track!\\nSplit channels: Number of channels '
    'within selection must match channel configuration of selected and '
    'following tracks!':
        'Gộp Channel: Số Channel trong vùng chọn phải khớp với cấu hình '
        'Channel của Track đã chọn!\\nTách Channel: Số Channel trong vùng chọn '
        'phải khớp với cấu hình Channel của Track đã chọn và các Track '
        'sau đó!',
    'Select Number of Mixer Bank Channels': 'Chọn số Channel của Mixer Bank',
    'Select Number of Parameter Values': 'Chọn số giá trị tham số',
    'Set number of audio tracks to number of input ports':
        'Đặt số Audio Track theo số cổng đầu vào',
    'The number of tracks does not match the selected destination format.':
        'Số Track không khớp với định dạng đích đã chọn.',
    'Toggle between Fixed Number of Steps and Density':
        'Chuyển đổi giữa số Step cố định và mật độ',
    'Track %s exceeds the number of tracks supported by the application. The '
    'track is kept, but cannot be modified.':
        'Track %s vượt quá số Track mà ứng dụng hỗ trợ. Track được giữ lại '
        'nhưng không thể chỉnh sửa.',
    'When Number of Staves Differs': 'Khi số khuông nhạc khác nhau',
    'With multiple events selected, this option is only available if they '
    'have the same number of channels':
        'Khi chọn nhiều Event, tùy chọn này chỉ khả dụng nếu chúng có cùng số '
        'Channel',

    # ==================================================================
    # slices 315-405
    # ==================================================================
    'Sends Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Send.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Set Tilt/Rotate Anchor ([ALT]-Click to Reset)':
        'Đặt điểm tựa Tilt/Rotate ([ALT]-Click để đặt lại)',
    'Set Track Type Filter\\nUse [CTRL + click] to Reset Track Type Filter':
        'Đặt Track Type Filter\\nDùng [CTRL + nhấp chuột] để đặt lại Track '
        'Type Filter',
    'Set Track Visibility Agents\\nUse [ALT]-Click to Reset Track Visibility '
    'Agents':
        'Đặt Track Visibility Agent\\nDùng [ALT] + nhấp chuột để đặt lại Track '
        'Visibility Agent',
    'Show only Expression Maps used in this Project':
        'Chỉ hiện các Expression Map dùng trong Project này',
    'Show only Sound Slots with Remote Trigger assignments':
        'Chỉ hiện các Sound Slot có phép gán Remote Trigger',
    'Text or Symbol Appearance at Start of Subsequent Systems':
        'Vẻ ngoài văn bản hoặc ký hiệu ở đầu các dòng nhạc tiếp theo',
    'The folder that you selected in the Path field does not exist.':
        'Thư mục bạn chọn trong trường Đường dẫn không tồn tại.',
    'The project contains no video. A black screen is exported.':
        'Project không có Video. Màn hình đen sẽ được export.',
    'There is not enough space on the selected drive!':
        'Không đủ dung lượng trên ổ đĩa đã chọn!',
    'Stereo Dual Panner (Remote Control Devices only)':
        'Stereo Dual Panner (Chỉ dành cho Remote Control Device)',
    'Track Display Settings: Active Track Only':
        'Cài đặt hiển thị Track: Chỉ Track đang hoạt động',
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
