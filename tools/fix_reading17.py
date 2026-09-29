#!/usr/bin/env python3
"""Round 17 of reading: the G-L block of the general catch-all.

Six slices, 2460..2860, about 600 labels. Two new defect classes, plus the
worst pair of split compounds I have found.

NEW CLASS 1 - a compound term cut in half, only the tail translated:

    "Key Signatures" -> "Key So chi nhip"
    "Key Switch"     -> "Key Chuyen"

  Both read as the word "key" followed by a stray verb. The first noun was
  dropped and the second translated, which produces something that is neither
  "Key Signatures" nor "Key Signature". "Add Displayed Key Signature" two
  hundred keys earlier was left correct, so the compound was never checked
  against itself.

NEW CLASS 2 - the prefix moved into the middle:

    "Layout: Concert Pitch"      -> "Pitch Layout: Concert"
    "Layout: Transposed Pitch"   -> "Pitch Layout: Transposed"
    "Layout: Add Layout"         -> "Layout Them Layout"
    "Layout: Remove Layout"      -> "Layout Go bo Layout"
    "Lane Controls"              -> "Lane Dieu khien"
    "Length Attribute Source"    -> "Do dai Thuoc tinh Source"
    "Length Factor"              -> "Do dai He so"

  "Pitch Layout: Concert" is the sharpest: the parenthesised option name has
  been split in two and the halves exchanged, so the label now claims to be a
  property of Concert Pitch rather than a layout option called Concert Pitch.

And two more words read as a different word:

    "Holds and Pauses"  -> "Ngat va Nghi"
  Holds is "giu". "Ngat" is break.

    "Interpret Sustain Pedal" -> "Dien giai Sustain Pedal"
  AGENT.md settled this years ago: interpret is "phan tich". It had been
  decided for CSV files and never applied here.

  python tools/fix_reading17.py
  python tools/fix_reading17.py --write
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
    # a compound cut in half, only the tail translated
    # ==================================================================
    'Key Signatures': 'Key Signature',
    'Key Switch': 'Key Switch',

    # ==================================================================
    # the "Layout:" / "Lane" / "Length" prefixes moved into the middle
    # ==================================================================
    'Layout: Concert Pitch': 'Layout: Concert Pitch',
    'Layout: Transposed Pitch': 'Layout: Transposed Pitch',
    'Layout: Add Layout': 'Layout: Thêm Layout',
    'Layout: Remove Layout': 'Layout: Gỡ bỏ Layout',
    'Layout: Switch to Layout %d': 'Layout: Chuyển sang Layout %d',
    'Layout: Lock/Unlock Layout': 'Layout: Khóa/Mở khóa',
    'Lane Controls': 'Điều khiển Lane',
    'Lane Display Type': 'Loại hiển thị Lane',
    'Lane Comping': 'Comping trong Lane',
    'Lanes Active': 'Các Lane đang hoạt động',
    'Lanes from Versions': 'Lane từ Version',
    'Length Adjustment': 'Điều chỉnh độ dài',
    'Length Attribute Source': 'Nguồn thuộc tính độ dài',
    'Length Decay': 'Suy giảm độ dài',
    'Length Factor': 'Hệ số độ dài',
    'Length in Bars': 'Độ dài tính bằng Bar',
    'Length in Samples': 'Độ dài tính bằng Sample',
    'Length in Seconds': 'Độ dài tính bằng giây',
    'Length of current recording': 'Độ dài của bản ghi hiện tại',
    'Lengths': 'Các độ dài',
    'Legato Overlap': 'Chồng lấn Legato',
    'Last Repeat of Current Chain Step':
        'Repeat cuối cùng của Chain Step hiện tại',

    # ==================================================================
    # two words read as a different word
    # ==================================================================
    # Holds is "giu"; "Ngat" is break
    'Holds and Pauses': 'Giữ và tạm dừng',
    # AGENT.md: interpret is "phan tich", decided for CSV, never applied here
    'Interpret Sustain Pedal': 'Phân tích Sustain Pedal',
    'Interval in seconds': 'Interval tính bằng giây',

    # ==================================================================
    # reversed
    # ==================================================================
    'Hitpoint Edit': 'Sửa Hitpoint',
    'Hitpoint Tracks': 'Các Track Hitpoint',
    'Ignore Master Track Events on Merge':
        'Bỏ qua Event của Master Track khi Merge',
    'Ignore all Files': 'Bỏ qua tất cả File',
    'Include Bass Notes': 'Bao gồm Note bass',
    'Include Sends': 'Bao gồm Send',
    'Incoming MIDI Data from Other Controller':
        'Dữ liệu MIDI đến từ Controller khác',
    'Increment Event Volume': 'Tăng âm lượng của Event',
    'Increment Volume in dB': 'Tăng âm lượng tính bằng dB',
    'Info Line': 'Dòng thông tin',
    'Initialize Dynamic Range': 'Khởi tạo Dynamic Range',
    'Input Port': 'Cổng đầu vào',
    'Input Port %d': 'Cổng đầu vào %d',
    'Input Ports': 'Các cổng đầu vào',
    'Input MIDI Signal': 'Tín hiệu MIDI đầu vào',
    'Inserted Notes Velocity': 'Velocity của Note đã chèn',
    'Install Device': 'Cài đặt Device',
    'Installed Devices': 'Các Device đã cài',
    'Instrument Output Track': 'Instrument Output Track',
    'Instrument Sounds': 'Âm thanh Instrument',
    'Instrument Return': 'Instrument Return',
    'Instrument Tracks': 'Các Instrument Track',
    'Instrument Pitch or Transposition':
        'Cao độ hoặc chuyển âm của Instrument',
    'Invert Control Value': 'Đảo giá trị Control',
    'Integrated Loudness': 'Loudness tích hợp',
    'Integrated Loudness in LUFS': 'Loudness tích hợp tính bằng LUFS',
    'Jazz Articulations': 'Articulation kiểu Jazz',
    'Left to Stereo': 'Trái thành Stereo',
    'Left Switch:': 'Switch trái:',
    'Left Arrow[Key]': 'Phím mũi tên trái',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Hide When Inactive': 'Ẩn khi không hoạt động',
    'Hide muted Notes in Editors': 'Ẩn Note bị Mute trong Editor',
    'Hide Truncated Event Names': 'Ẩn tên Event bị cắt',
    'Highlight Borders of Selected Events': 'Tô sáng viền Event đã chọn',
    'Highlight Suggestions from List Tab': 'Đánh dấu gợi ý từ thẻ danh sách',
    'Hold on Stop': 'Giữ khi dừng',
    'Keep Editor Contents On/Off': 'Bật/Tắt giữ nội dung Editor',
    'Keep Existing Notes': 'Giữ các Note hiện có',
    'Keep History': 'Giữ Lịch sử',
    'Keep Notes in Range': 'Giữ Note trong vùng',
    'Keep Silent Segments': 'Giữ Segment im lặng',
    'Keep Source Events Unchanged': 'Giữ nguyên Source Event',
    'Keep Source Tracks': 'Giữ Source Track',
    'Keep Source Tracks Unchanged': 'Giữ nguyên Source Track',
    'Keeps Silent Segments as Separate Events':
        'Giữ các Segment im lặng thành Event riêng biệt',
    'Last Hovered Control': 'Control đã hover gần nhất',
    'Last Touched Control': 'Control đã điều chỉnh gần nhất',
    'Last Touched Parameter': 'Tham số đã điều chỉnh gần nhất',
    'Last Month': 'Tháng trước',
    'Last Week': 'Tuần trước',
    'Image under construction...': 'Hình ảnh đang được dựng...',
    'Individual Controller Settings': 'Cài đặt Controller riêng',
    'Input Filter': 'Bộ lọc đầu vào',
    'Intput Port Names': 'Tên cổng đầu vào',
    'Invalid working directory!': 'Thư mục làm việc không hợp lệ!',
    'Installed Fonts': 'Font đã cài đặt',
    'Inserts Reset': 'Đặt lại Insert',
    'Inserts Bypass': 'Bypass Insert',
    'Inserts and Strip': 'Inserts và Strip',
    'Inserts/EQs/Sends': 'Inserts/EQs/Sends',
    'Inserts/Sends': 'Inserts/Sends',
    'Label Field': 'Trường Label',
    'Inhibit warning when applying Offline Processes':
        'Chặn cảnh báo khi áp dụng Offline Process',
    'Inhibit Restart ms': 'Thời gian chặn khởi động lại, tính bằng ms',
    "In 'All MIDI Inputs'": "Trong 'Tất cả đầu vào MIDI'",
    'Importing video track: %d': 'Đang Import Track video: %d',
    'Just Notes and No Pitchbend Data':
        'Chỉ có Note và không có dữ liệu Pitchbend',
    'Jump to Previous Range with Low Intelligibility':
        'Tới Vùng liền trước có khả năng nghe rõ thấp',

    # ==================================================================
    # "Indicates if" - "neu" (if) instead of "lieu" (whether)
    # ==================================================================
    'Indicates if Hitpoints are calculated': 'Chỉ báo liệu Hitpoint đã được tính',
    'Indicates if annotations exist': 'Chỉ báo liệu có chú thích hay không',
    'Indicates if more than one Version exists':
        'Chỉ báo liệu có nhiều hơn một Version',
    'Included in Link Group: <%s>': 'Có trong Link Group: <%s>',

    # ==================================================================
    # the Intelligibility family, which was three different things
    # ==================================================================
    'Intelligibility': 'Khả năng nghe rõ',
    'Average Intelligibility': 'Khả năng nghe rõ trung bình',
    'Enable Intelligibility Measurement':
        'Bật phép đo khả năng nghe rõ',

    # ==================================================================
    # case, plural, and a missing full stop
    # ==================================================================
    'Invalid': 'Không hợp lệ',
    'Invalid event': 'Event không hợp lệ',
    'Invalid signature': 'Số chỉ nhịp không hợp lệ',
    'Invalid Path': 'Đường dẫn không hợp lệ',
    'Is Muted': 'Đang bị Mute',
    'Hold First': 'Giữ đầu tiên',
    'Highest CC Value': 'Giá trị CC cao nhất',
    'Highest Pitch': 'Cao độ cao nhất',
    'Highest Velocity': 'Velocity cao nhất',
    'High Quality Mode': 'Chế độ High-Quality',
    'High-Quality Mode': 'Chế độ High-Quality',
    'High Resolution Display Range': 'Vùng hiển thị độ phân giải cao',
    'Hitpoints': 'Các Hitpoint',
    'Hide Source Tracks': 'Ẩn Source Track',
    'Image Height': 'Chiều cao hình ảnh',
    'Image Width': 'Chiều rộng hình ảnh',
    'Include Inserts': 'Bao gồm Insert',
    'Input Channels': 'Các Input Channel',
    'Input Transformer Presets': 'Preset Input Transformer',
    'Instrument Channels': 'Các Instrument Channel',
    'Instrument (Disable with ALT + click)':
        'Instrument (Tắt bằng ALT + click)',
    'Increasing Stepwise': 'Tăng dần từng bậc',
    'Instances': 'Các Instance',
    'Instances:': 'Các Instance:',
    'Knobs': 'Các núm vặn',
    'L/R Channels from Surround': 'Các Channel L/R từ Surround',
    'LSB Control No.': 'Số Control LSB',
    'Labels': 'Các nhãn',
    'Libraries': 'Các thư viện',
    'Levels': 'Các mức',
    'Less or Equal': 'Ít hơn hoặc bằng',
    'Left-Aligned on Barline': 'Căn trái theo vạch nhịp',
    'Left/Right movement (Glide)': 'Di chuyển trái/phải (Glide)',
    'Length Quant.': 'Độ dài Quant.',
    'Move Down': 'Di chuyển xuống',
    'Move Up': 'Di chuyển lên',
    'Move Left': 'Di chuyển trái',
    'Move Right': 'Di chuyển phải',
    'Inversions: Move Down': 'Thể đảo: Di chuyển xuống',
    'Inversions: Move Up': 'Thể đảo: Di chuyển lên',
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
