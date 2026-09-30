#!/usr/bin/env python3
"""Round 42: the media domain, long values 60-120.

Four small classes, all of them the ones this project keeps finding.

    "If you are using the built-in audio connections of your computer, please
     select the corresponding audio driver."
      -> "... vui long chon driver Audio tuong ung."
    "If you want to use another audio hardware, please select the
     corresponding ASIO driver from the list below and click "OK"."
      -> "... vui long chon driver ASIO tuong ung tu danh sach ben duoi ..."

"driver" is "trinh dieu khien" - round 33 settled that for "graphics card
driver", and round 41 fixed one "audio driver". Two more in the same dialog.

    'Bars+Beats' -> 'Bar+Nhiep'    (4 keys)
    "Tempo and signature tracks can only be imported if 'Bars+Beats' is
     selected as 'Primary Time Format'."
      -> "... 'Bars+Beats' duoc chon lam 'Primary Time Format'."

Two keys kept the English. It is a menu value, so it should be one string, and
four keys already decided which.

    "Warp Markers"  -> 'Warp Tabs'   (9 other keys say Warp Tab)
    "... and warp markers. Click "Bounce" to create such events."
      -> "... va Warp Marker bang nhau."

One sentence in the family uses the other name. Nine keys say "Warp Tab",
three say "Warp Tabs" for the English "Warp Markers", and this one says
"Warp Marker". Cubase's own name for the object in the Warp Grid is Warp Tab,
so that is the term; the three are fine and this one is the outlier. Which is
the opposite of round 41, where I was about to "fix" a correct value - the
tool reporting NOT IN CUBASE is what stopped it.

    "Not enough space on disk available for export!"
      -> "Khong du dung luong trong tren dia de Export!"

"dung luong trong" - free space AND quantity, one word. Round 34 removed the
same redundancy from "There is not enough space on the selected drive!" and
from the rendering and copying variants. These two are the export and import
members of that family.

And "Size Event End", where Size is a VERB and the label is "Size Event Start" /
"Size Event End":

    "Size Event End (Audio Event Size Locked)"
      -> "Doi kich thuoc duoi Event (Khoa kich thuoc Audio Event)"

  python tools/fix_reading42.py
  python tools/fix_reading42.py --write
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
    # driver is "trinh dieu khien" - round 33, then round 41, now twice
    # more in the same dialog
    # ==================================================================
    'If you are using the built-in audio connections of your computer, please '
    'select the corresponding audio driver.':
        'Nếu bạn đang dùng kết nối Audio tích hợp của máy tính, vui lòng chọn '
        'trình điều khiển Audio tương ứng.',
    'If you want to use another audio hardware, please select the '
    'corresponding ASIO driver from the list below and click "OK".':
        'Nếu bạn muốn dùng phần cứng Audio khác, vui lòng chọn trình điều khiển '
        'ASIO tương ứng từ danh sách bên dưới và nhấp "OK".',

    # ==================================================================
    # a menu value is one string; four keys decided which
    # ==================================================================
    "Tempo and signature tracks can only be imported if 'Bars+Beats' is "
    "selected as 'Primary Time Format'.":
        "Chỉ có thể import Tempo Track và Signature Track nếu 'Bar+Nhịp' được "
        "chọn làm 'Primary Time Format'.",
    'The time format was changed to Bars+Beats!':
        'Định dạng thời gian đã được chuyển thành Bar+Nhịp!',

    # ==================================================================
    # Warp Tab is the Cubase name; one sentence used the other one
    # ==================================================================
    'Phase-coherent AudioWarp operations require equal event lengths, '
    'positions, and warp markers. Click "Bounce" to create such events.':
        'Các thao tác AudioWarp đồng pha cần các Event có độ dài, vị trí và '
        'Warp Tab bằng nhau. Nhấp "Bounce" để tạo các Event như vậy.',
    'Warp Tab Creation Rules': 'Quy tắc tạo Warp Tab',

    # ==================================================================
    # "dung luong trong" - free space AND quantity, one word
    # ==================================================================
    'Not enough space on disk available for export!':
        'Không đủ dung lượng trên đĩa để export!',
    'Not enough space on disk available for import!':
        'Không đủ dung lượng trên đĩa để import!',
    'No active project for import!\\nPlease create and set up a new project.':
        'Không có Project nào đang hoạt động để import!\\nVui lòng tạo và thiết '
        'lập một Project mới.',

    # ==================================================================
    # Size is a verb in "Size Event Start" / "Size Event End"
    # ==================================================================
    'Size Event End (Audio Event Size Locked)':
        'Đổi kích thước cuối Event (Khóa kích thước Audio Event)',
    'Size Event Start (Audio Event Size Locked)':
        'Đổi kích thước đầu Event (Khóa kích thước Audio Event)',

    # ==================================================================
    # small
    # ==================================================================
    'MPEX algorithms are not supported by this program version. If you want to '
    'modify the process, you can use an Elastique algorithm. To keep the '
    'processed audio, you can make all processes permanent.':
        'Thuật toán MPEX không được hỗ trợ bởi phiên bản chương trình này. Nếu '
        'muốn sửa đổi xử lý, bạn có thể dùng thuật toán Elastique. Để giữ Audio '
        'đã xử lý, bạn có thể chuyển tất cả xử lý thành vĩnh viễn.',
    'MPEX algorithms are not supported by this program version. To modify the '
    'process, you can reprocess using a ZTX algorithm. To keep the processed '
    'audio, you can make all processes permanent.':
        'Thuật toán MPEX không được hỗ trợ bởi phiên bản chương trình này. Để '
        'sửa đổi xử lý, bạn có thể xử lý lại bằng thuật toán ZTX. Để giữ Audio '
        'đã xử lý, bạn có thể chuyển tất cả xử lý thành vĩnh viễn.',
    'Remove selected Users from the User Pool':
        'Gỡ bỏ các User đã chọn khỏi User Pool',
    'The audio device port or midi device assignments of this Favorite are '
    'already in use. Reuse them and add to External Effects?':
        'Cổng thiết bị Audio hoặc phép gán thiết bị MIDI của mục yêu thích này '
        'đã được sử dụng. Tái sử dụng chúng và thêm vào External Effect?',
    'Press [Esc] to cancel the process and terminate the video service.':
        'Nhấn [Esc] để hủy tiến trình và kết thúc dịch vụ Video.',
    'Event fade times on the selected tracks are not aligned.':
        'Thời gian Fade của Event trên các Track đã chọn không căn nhau.',
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
