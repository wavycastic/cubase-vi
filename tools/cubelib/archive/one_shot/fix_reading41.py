#!/usr/bin/env python3
"""Round 41: the media domain, first sixty long values.

    "Importing audio stream from video file..."
      -> "Importing audio stream tu video file..."
    "Replacing audio stream in video file..."
      -> "Replacing audio stream trong video file..."

The frame class once more, and the shortest examples in the project. A
Vietnamese sentence does not begin with a bare English -ing form. The value
has "tu" and "trong" in it, so audit_quality counts it as translated - which
is exactly the loophole round 36 measured and round 37 found a word dropped for.

That gives a third, and cheapest, detector of the same defect:

  tools/find_english_opening.py - the FIRST WORD is an English verb form and
      the value runs past thirty characters. Labels like "Export Clip Names" and
      "Mapping of Project" are caught by the test and are correct; the reading
      pass is still a reading pass.

And four consistency pairs, all of which the map had already settled:

    Disk Cache Load        ->  Tai bo nho dem dia
    Disk Cache Overload    ->  Qua tai Disk Cache

`Disk Cache` is a Cubase feature. One of the two was translated, the other
kept - in the same panel.

    audio stream           ->  audio stream        (5 keys)
    Could not extract audio stream %d of file
                           ->  Khong the trich xuat luong Audio %d cua file

    "the same audio material"
                           ->  cung du lieu Audio
    "monophonic material only" (round 39)
                           ->  chi danh cho chat lieu don am

`Material` is `chat lieu`; "du lieu" is data, and the word right next to it is
"audio". Round 39 chose "chat lieu" and this one was not in that batch.

And two small ones worth recording because they are the same defect as
`Word Clock` -> `Tu`: a compound read as its parts.

    "audio drivers" ->  driver Audio (not "trinh dieu khien", as round 33
                                     established for "graphics card driver")

  python tools/fix_reading41.py
  python tools/fix_reading41.py --write
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
    # the frame, at its shortest: a bare English -ing form standing alone
    # ==================================================================
    'Importing audio stream from video file...':
        'Đang nhập audio stream từ file Video...',
    'Replacing audio stream in video file...':
        'Đang thay thế audio stream trong file Video...',
    'Cannot remove existing audio stream from video file!':
        'Không thể gỡ bỏ audio stream hiện có khỏi file Video!',

    # ==================================================================
    # Disk Cache - one key translated it, the other kept it, same panel
    # ==================================================================
    'Disk Cache Load': 'Tải Disk Cache',
    'Disk Cache Load\\nClick to Show Audio Performance Panel':
        'Tải Disk Cache\\nNhấp để hiện Bảng Hiệu năng Audio',

    # ==================================================================
    # "material" is "chat lieu"; round 39 settled it for "monophonic
    # material" and this one was not in that batch
    # ==================================================================
    'Do you want to modify all events that refer to the same audio material?':
        'Bạn có muốn sửa đổi tất cả Event tham chiếu tới cùng chất liệu Audio '
        'không?',

    # ==================================================================
    # a compound read as its parts - "driver" is "trinh dieu khien",
    # as round 33 established for "graphics card driver"
    # ==================================================================
    '%s has detected that new audio drivers are available on your computer. '
    'Please select the audio driver for the audio hardware that you want to '
    'use with %s.':
        '%s phát hiện có trình điều khiển Audio mới trên máy tính của bạn. Vui '
        'lòng chọn trình điều khiển Audio cho phần cứng Audio mà bạn muốn dùng '
        'với %s.',

    # ==================================================================
    # small
    # ==================================================================
    'Could not extract audio stream %d of file ':
        'Không thể trích xuất audio stream %d của file ',
    'Could not import all tracks! The data is corrupted.':
        'Không thể import tất cả Track! Dữ liệu bị hỏng.',
    'Error: Invalid or unsupported file!':
        'Lỗi: file không hợp lệ hoặc không được hỗ trợ!',
    'A file cannot be replaced if it has multiple edit versions!\\nInstead, '
    'new files can be created and replaced in the Pool!':
        'Không thể thay thế file nếu nó có nhiều phiên bản chỉnh sửa!\\nThay vào '
        'đó, bạn có thể tạo file mới rồi thay thế trong Pool!',
    'Determines how far before the actual hitpoint position the audio event '
    'is sliced':
        'Xác định khoảng cách trước vị trí Hitpoint thực tế mà Audio Event '
        'được cắt lát',
    'Defines which hitpoint positions are used for slicing':
        'Xác định vị trí Hitpoint nào được dùng để cắt lát',
    'Audio in musical mode cannot be sliced.\\nDo you want to disable musical '
    'mode?':
        'Audio ở chế độ Musical không thể cắt lát.\\nBạn có muốn tắt chế độ '
        'Musical không?',
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
