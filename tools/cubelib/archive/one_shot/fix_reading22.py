#!/usr/bin/env python3
"""Round 22 of reading: the R-S block of the general catch-all.

Four slices, 4860..5260, about 400 labels.

A lost bracket, which is the same class as the lost colon in round 13:

    "Select Preset (rename using [Alt + click])"
      -> "Chon Preset (doi ten bang [Alt + click]"

  The closing bracket of the outer parenthesis is gone. The key carries a
  nested bracket pair and the value carries one of the two.

A lost verb:

    "Select Tool (Press [ALT] to draw events)"
      -> "Cong cu chon (Nhan [ALT] de ve Event)"

  There is no "Select" anywhere in the Vietnamese - the label begins with the
  noun, so it reads as "tool to select", which is the other menu.

And the same reversal, once more, in a family I have already fixed twice
elsewhere - "No." read as the negative instead of Number:

    "Scene No." -> "Canh Khong"      reads as "scene none"

  Two hundred keys earlier "No. of Voices (Part)" had been given "So be (Part)"
  correctly. The abbreviation had been decided once and not applied.

The "Scripting Tools:" family had three of six with "Scripting" shortened to
"Script" and one fully scrambled:

    "Scripting Tools: Open Script Folder"
      -> "Thu muc Scripting Tools: Open Script"

  which is the sentence taken apart: the object moved to the front and the verb
  left in English, in the wrong order, in a string that already contained
  "Scripting Tools".

Also "Select Effect" said "Chon hieu ung" and "Select Effect Type" said "Chon
loai hieu ung", while round 14 had set "Add Effect" and "Bypass Effect" to keep
Effect in English on the grounds that the whole family does. Two of the family
had been left behind.

  python tools/fix_reading22.py
  python tools/fix_reading22.py --write
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
    # a lost bracket and a lost verb
    # ==================================================================
    'Select Preset (rename using [Alt + click])':
        'Chọn Preset (đổi tên bằng [Alt + click])',
    'Select Tool (Press [ALT] to draw events)':
        'Chọn công cụ (Nhấn [ALT] để vẽ Event)',
    'Select Tool: Show Extra Info': 'Chọn công cụ: Hiện thông tin thêm',
    'Select Tool': 'Chọn công cụ',

    # ==================================================================
    # "No." as Number, not the negative - decided once, applied once
    # ==================================================================
    'Scene No.': 'Số Scene',

    # ==================================================================
    # the "Scripting Tools:" family
    # ==================================================================
    'Scripting Tools': 'Công cụ Scripting',
    'Scripting Tools: Highlight Bounding Rects':
        'Công cụ Scripting: Đánh dấu khung bao',
    'Scripting Tools: Open Console': 'Công cụ Scripting: Mở Console',
    'Scripting Tools: Open ReadMe': 'Công cụ Scripting: Mở ReadMe',
    'Scripting Tools: Open Script Folder':
        'Công cụ Scripting: Mở thư mục Script',
    'Scripting Tools: Reload Scripts': 'Công cụ Scripting: Tải lại Script',

    # ==================================================================
    # the "Select ..." family
    # ==================================================================
    'Select Effect': 'Chọn Effect',
    'Select Effect Type': 'Chọn loại Effect',
    'Select Scheme Preset': 'Chọn Scheme Preset',
    'Select Search Path...': 'Chọn đường dẫn tìm kiếm...',
    'Select Filter Attributes': 'Chọn thuộc tính Filter',
    'Select Filter Slope': 'Chọn độ dốc Filter',
    'Select Full Vertical': 'Chọn toàn bộ chiều dọc',
    'Select Input Configuration': 'Chọn cấu hình Input',
    'Select Output Configuration': 'Chọn cấu hình Output',
    'Select Matching': 'Chọn kết quả khớp',
    'Select Matching Destination Tracks': 'Chọn Track đích khớp',
    'Select Mode': 'Chọn chế độ',
    'Select Model': 'Chọn model',
    'Select New': 'Chọn mục mới',
    'Select Next': 'Chọn kế tiếp',
    'Select Previous': 'Chọn liền trước',
    'Select Next Downmix Preset': 'Chọn Preset Downmix kế tiếp',
    'Select Next Player': 'Chọn Player kế tiếp',
    'Select Previous Player': 'Chọn Player liền trước',
    'Select Previous Track': 'Chọn Track liền trước',
    'Select Next Track': 'Chọn Track kế tiếp',
    'Select Pattern to Preview': 'Chọn Pattern để Preview',
    'Select Pitch Visibility Options': 'Chọn tùy chọn hiển thị Pitch',
    'Select Silent Segments': 'Chọn Segment im lặng',
    'Select Track: Add Next': 'Chọn Track: Thêm kế tiếp',
    'Select Track: Add Prev': 'Chọn Track: Thêm liền trước',
    'Select Track: Next': 'Chọn Track kế tiếp',
    'Select Track: Prev': 'Chọn Track liền trước',
    'Select Tracks with Same Version ID': 'Chọn Track có cùng Version ID',
    'Select all Inputs [%d]': 'Chọn tất cả Input [%d]',
    'Select destination parameter': 'Chọn tham số đích',
    'Select extraction target folder': 'Chọn thư mục đích trích xuất',
    'Select folder with missing files': 'Chọn thư mục chứa file bị thiếu',
    'Select smart control mode': 'Chọn chế độ Smart Control',
    'Select Track for Auditioning': 'Chọn Track để nghe thử',
    'Select Defined Favorite': 'Chọn mục yêu thích đã định nghĩa',
    'Select Events matching Filter Condition': 'Chọn Event khớp điều kiện lọc',
    'Select External Inputs': 'Chọn External Input',
    'Select Ext. Input': 'Chọn External Input',
    'Select Alternative Key Sets': 'Chọn bộ Key Set thay thế',
    'Select All Source Tracks': 'Chọn tất cả Source Track',
    'Search Channels': 'Tìm kiếm Channel',
    'Search Folder': 'Thư mục tìm kiếm',
    'Search Options': 'Tùy chọn tìm kiếm',
    "Search for [%s] = '%s'": "Tìm [%s] = '%s'",
    'Scanning MIDI Inputs': 'Đang quét MIDI Input',
    'Scanning MIDI-Ports': 'Đang quét MIDI Port',
    'Scrub Tool Volume': 'Âm lượng Công cụ Scrub',
    'Script Messages': 'Thông điệp Script',
    'Script Path': 'Đường dẫn Script',
    'Script Deletion from disk was not sucessful':
        'Việc xóa Script khỏi đĩa không thành công',
    'Script Archive could not be imported.':
        'Không thể import kho lưu trữ Script.',
    'Script could not be exported.': 'Không thể export Script.',
    'Saved Results': 'Đã lưu kết quả',
    'Ruler Colors': 'Màu thước đo',
    'Ruler Mode: Bars+Beats Linear': 'Chế độ thước đo: Bar+Nhịp tuyến tính',
    'Ruler Mode: Time Linear': 'Chế độ thước đo: thời gian tuyến tính',
    'Right Switch:': 'Switch phải:',
    'Right Side': 'Bên phải',
    'Right to Stereo': 'Phải thành Stereo',
    'Root Notes': 'Nốt gốc',
    'Root Position': 'Vị trí gốc',
    'Round White with Dot Noteheads': 'Đầu nốt tròn trắng có chấm',
    'Rise - Fall': 'Tăng - Rơi',
    'Run Setup on Create New Project': 'Chạy Setup khi tạo Project mới',
    'SMF: Key signature': 'SMF: Số chỉ nhịp',
    'SMF: Instrument': 'SMF: Instrument',
    'SMF: Seq.Number': 'SMF: Số Seq.',
    'Same as Project': 'Giống Project',
    'Sampler Control': 'Sampler Control',
    'Sampler Tracks': 'Các Sampler Track',
    'Sampler Channels': 'Các Sampler Channel',
    'Samples': 'Các Sample',
    'Scales': 'Các Scale',
    'Scores': 'Các Score',
    'Scripts': 'Các Script',
    'Sections': 'Các phần',
    'Secondary Parameter: Decrease': 'Tham số phụ: Giảm',
    'Secondary Parameter: Fine Decrease': 'Tham số phụ: Giảm tinh vi',
    'Secondary Parameter: Fine Increase': 'Tham số phụ: Tăng tinh vi',
    'Secondary Parameter: Increase': 'Tham số phụ: Tăng',
    'Secondary Time Display': 'Hiển thị thời gian phụ',
    'Secondary Type': 'Loại phụ',
    'Secondary Value': 'Giá trị phụ',
    'Primary Type': 'Loại chính',
    'Rows': 'Các hàng',
    'Save Changes as Preset...': 'Lưu thay đổi dưới dạng Preset...',
    'Save Configuration': 'Lưu cấu hình',
    'Save Now': 'Lưu ngay',
    'Save Library...': 'Lưu thư viện...',
    'Save SyncStation configuration': 'Lưu cấu hình SyncStation',
    'Save Input Assignment': 'Lưu phép gán Input',
    'Save Definition in Project Only': 'Chỉ lưu Definition trong Project',
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
