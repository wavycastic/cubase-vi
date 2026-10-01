#!/usr/bin/env python3
"""Round 44: the last of the media domain's long values, 205 in all read.

THREE SENTENCES DROPPED, and this is the worst loss found so far:

    "You have activated the Steinberg Audio Power Scheme.

     The Steinberg Audio Power Scheme optimizes Windows power handling for
     best possible audio performance at low-latency ASIO settings. However,
     this also increases the power consumption of the computer.

     If power consumption is a concern, please disable this option and increase
     the buffer size of your audio hardware.

     Further information on the Steinberg Audio Power Scheme can be found in
     the Steinberg Knowledge Base."
      -> "Ban da kich hoat Steinberg Audio Power Scheme.

         Co che nay toi uu hoa viec quan ly nguon dien cua Windows de co hieu
         nang Audio tot nhat o thiet lap ASIO do tre thap."

One of five sentences survives. What is lost is the ENTIRE cost side: the
scheme INCREASES power consumption, and if that matters to you, turn it off and
raise the buffer size instead. The dialog now reads as pure praise for a
setting that spends your battery.

The dropped half has a shape by now - it is always the clause with a
CONDITION in it. Round 32 lost "but requires you to estimate the pickup value".
Round 38 lost "This has no effect for bar numbers centered on the bar". Round 40
lost "Please note that this conversion might lead to clipping". Round 38 lost
"If this option is set to show a cautionary either with or without
parentheses, then ...". Four for four, the second half went.

Worth recording as a rule: after translating a long string, COUNT THE
SENTENCES. The map is full of correct-looking Vietnamese that is one sentence
short.

And three more of the pairs this domain keeps producing:

    "Link Word Clock Outputs"     -> "Link dau ra Word Clock"
    "Link All Word Clock Outputs" -> "Lien ket tat ca dau ra Word Clock"

"Link" is a DAW term as a noun and a Vietnamese verb as a verb. One key used
the noun sense on a verb.

    "Warning: Sample rate does not match external word clock."
      -> "Canh bao: Sample Rate khong khop voi Word Clock ngoai."

`External`, the round 33 find, in the last place it was hiding. Ten Word Clock
keys, and this is the only one that translated the adjective.

    "You have selected regions for processing"  -> "... cac vung de xu ly"
    28 keys say `Region`.

  python tools/fix_reading44.py
  python tools/fix_reading44.py --write
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
    # five sentences in, one out
    # ==================================================================
    'You have activated the Steinberg Audio Power Scheme.\\n\\nThe Steinberg '
    'Audio Power Scheme optimizes Windows power handling for best possible '
    'audio performance at\\nlow-latency ASIO settings. However, this also '
    'increases the power consumption of the computer.\\n\\nIf power '
    'consumption is a concern, please disable this option and increase the '
    'buffer size of your audio hardware.\\n\\nFurther information on the '
    'Steinberg Audio Power Scheme can be found in the Steinberg Knowledge '
    'Base.':
        'Bạn đã kích hoạt Steinberg Audio Power Scheme.\\n\\nSteinberg Audio '
        'Power Scheme tối ưu hóa việc quản lý nguồn điện của Windows để có '
        'hiệu năng Audio tốt nhất ở\\ncác thiết lập ASIO độ trễ thấp. Tuy nhiên, '
        'điều này cũng làm tăng mức tiêu thụ điện của máy tính.\\n\\nNếu lo lắng '
        'về mức tiêu thụ điện, vui lòng tắt tùy chọn này và tăng kích thước '
        'buffer cho phần cứng Audio của bạn.\\n\\nThông tin thêm về Steinberg '
        'Audio Power Scheme có trong Steinberg Knowledge Base.',

    # ==================================================================
    # "Link" is a noun term and a Vietnamese verb. This key used the
    # noun sense on a verb.
    # ==================================================================
    'Link Word Clock Outputs': 'Liên kết đầu ra Word Clock',

    # ==================================================================
    # External, the round 33 find, last place it was hiding
    # ==================================================================
    'Warning: Sample rate does not match external word clock.':
        'Cảnh báo: Sample Rate không khớp với Word Clock External.',

    # ==================================================================
    # Region, in a family of 28 that already say Region
    # ==================================================================
    'You have selected regions for processing\\nthat refer to overlapping '
    'audio material!':
        'Bạn đã chọn các Region để xử lý\\ntham chiếu tới chất liệu Audio bị '
        'chồng lấn!',

    # ==================================================================
    # driver, again - round 41, 42, now twice more
    # ==================================================================
    'To ensure that you actually hear audio from %s, please select the driver '
    'of your audio interface from the list below. This is required for '
    'correct routing of playback and recording signals to your audio '
    'hardware.':
        'Để đảm bảo bạn thực sự nghe thấy Audio từ %s, vui lòng chọn trình điều '
        'khiển của Audio Interface từ danh sách bên dưới. Điều này cần thiết cho '
        'Routing chính xác tín hiệu phát và ghi tới phần cứng Audio của bạn.',
    'You can change your driver selection and settings at any time in the '
    'Studio Setup dialog (Studio menu > Studio Setup) in the VST Audio System '
    'section.':
        'Bạn có thể thay đổi lựa chọn trình điều khiển và cài đặt bất kỳ lúc nào '
        'trong hộp thoại Thiết lập Studio (menu Studio > Thiết lập Studio) ở '
        'phần VST Audio System.',

    # ==================================================================
    # small
    # ==================================================================
    'it is used in another Pool and it has more than one edit version!':
        'nó đang được dùng trong một Pool khác và có nhiều hơn một phiên bản '
        'chỉnh sửa!',
    'Would you like to import all bitmaps in project folder?':
        'Bạn có muốn import tất cả ảnh bitmap trong thư mục Project không?',
    'This project file contains surround channels which are not supported by '
    'this program version. All surround channels are switched to \'stereo\'.':
        'File Project này chứa các Channel Surround mà phiên bản chương trình '
        'này không hỗ trợ. Tất cả Channel Surround được chuyển thành '
        "'Stereo'.",
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
