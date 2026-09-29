#!/usr/bin/env python3
"""Round 9 of reading: audio, media and the Pool.

  1. "Warp Marker" was rendered four different ways in one panel:

        "Warp Markers"              -> "Marker Warp"     reversed
        "Create Warp Tabs"          -> "Tao The Warp"
        "Create Warp Tabs from Hitpoints" -> "Tao Warp Tab tu Hitpoint"
        "Delete Warp Tab"           -> "Xoa The Warp"
        "Free Warp"                 -> "Warp tu do"      reversed

     One key, "Copy Warp Markers from Selected Event", had it right all along,
     which is how the others are now written. AGENT.md section 3 lists Marker
     as a term to keep, so it is "Warp Marker" everywhere.

  2. progress messages never translated, only their surroundings:

        "Converting file..."  -> "Converting file..."
        "Closing file..."     -> "Closing file..."
        "Connecting Media..." -> "Connecting Media..."
        "Copying files ..."   -> "Copying files..."
        "Flattening file..."  -> "Flattening file..."

     and the ones that did get translated kept the English gerund in the
     middle: " Loi exporting media", " Loi while exporting OMF file".

  3. "File X" with the English noun in front of the Vietnamese one, over a
     dozen keys. Vietnamese puts the noun first, so "File Vi tri" should be
     "Vi tri File". Same class as "Ten Channel", which is correct.

  4. two sentences that came apart:

        "Failed to create audio file:" -> "Failed vao Tao audio file:"
        "Ignore this File"             -> "File Ignore this"
        "Fade In to Range Start"       -> "Fade trong to Range Start"

  python tools/fix_reading9.py
  python tools/fix_reading9.py --write
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
    # Warp Tab, one rendering. Most of the family already said "Warp Tab";
    # the strays were "The Warp", "tab Warp" and a fully reversed "Marker Warp".
    # ==================================================================
    'Warp Markers': 'Warp Tabs',
    'Create Warp Tabs': 'Tạo Warp Tab',
    'Create Warp Tabs from Hitpoints': 'Tạo Warp Tab từ Hitpoint',
    'Creates Warp Tabs at Hitpoints': 'Tạo Warp Tab tại Hitpoint',
    'Defines which hitpoint positions are used for creating Warp Tabs':
        'Xác định vị trí Hitpoint nào được dùng để tạo Warp Tab',
    'Delete Warp Tab': 'Xóa Warp Tab',
    'Delete Warp Tabs': 'Xóa Warp Tab',
    'Edit Warp Tab': 'Sửa Warp Tab',
    'Remove all Warp Tabs': 'Gỡ bỏ tất cả Warp Tab',
    'Copy Warp Markers from Selected Event':
        'Sao chép Warp Tab từ Event đã chọn',
    'Paste Warp Markers to Selected Events':
        'Dán Warp Tab vào Event đã chọn',
    'Free Warp': 'Free Warp',
    'Free Warp Tool': 'Công cụ Free Warp',
    'Time Warp': 'Time Warp',
    'Time Warp Tool': 'Công cụ Time Warp',
    'Reset Warp Changes': 'Đặt lại thay đổi Warp',
    'Reset Warp Changes for Selection': 'Đặt lại thay đổi Warp cho vùng chọn',
    'Custom Warp Settings': 'Cài đặt Warp tùy chỉnh',

    # ==================================================================
    # progress messages, translated or not
    # ==================================================================
    'Converting file...': 'Đang chuyển đổi file...',
    'Converting files...': 'Đang chuyển đổi file...',
    'Converting media...': 'Đang chuyển đổi Media...',
    'Copying file...': 'Đang sao chép file...',
    'Copying files ...': 'Đang sao chép file...',
    'Copying files to clipboard': 'Đang sao chép file vào clipboard',
    'Closing file...': 'Đang đóng file...',
    'Connecting Media...': 'Đang kết nối Media...',
    'Flattening file...': 'Đang Flatten file...',
    'Creating new audio stream in video file':
        'Đang tạo audio stream mới trong file video',
    'Creating Render Files Directory...':
        'Đang tạo thư mục Render File...',
    'Creating OMF file...': 'Đang tạo file OMF...',
    'Creating OpenTL file...': 'Đang tạo file OpenTL...',
    'Creating backup file': 'Đang tạo file sao lưu',
    'Could not create OMF file...': 'Không thể tạo file OMF...',

    # ==================================================================
    # the English gerund left in the middle of a Vietnamese sentence
    # ==================================================================
    'Error exporting media': 'Lỗi khi Export Media',
    'Error in importing OMF media': 'Lỗi khi Import Media OMF',
    'Error while exporting OMF file': 'Lỗi khi Export file OMF',
    'Errors on importing media:\\n': 'Lỗi khi Import Media:\\n',
    'Cannot write AES31 media: %s': 'Không thể ghi Media AES31: %s',

    # ==================================================================
    # "File X" with the English noun first
    # ==================================================================
    'File Format': 'Định dạng File',
    'File Format Setup Error': 'Lỗi thiết lập định dạng File',
    'File Location': 'Vị trí File',
    'File Path': 'Đường dẫn File',
    'File System': 'Hệ thống File',
    'File System Error': 'Lỗi hệ thống File',
    'File Sample Rate': 'Sample Rate của File',
    'File Name Conflict Options': 'Tùy chọn xung đột tên File',
    'File Name Options': 'Tùy chọn tên File',
    'File Name Settings': 'Cài đặt tên File',
    'Record File Format': 'Ghi định dạng File',
    'Split File Format': 'Tách định dạng File',
    'Select File Format Presets': 'Chọn Preset định dạng File',
    'Audio Tracks': 'Audio Track',
    'Audio Track Presets': 'Preset Audio Track',
    'Audio Channels': 'Channel Audio',
    'Audio Events to Part': 'Chuyển Audio Event thành Part',
    'Destination Format': 'Định dạng đích',
    'Export %s File': 'Export file %s',

    # ==================================================================
    # sentences that came apart
    # ==================================================================
    'Failed to create audio file:': 'Không thể tạo file Audio:',
    'Ignore this File': 'Bỏ qua file này',
    'Fade In to Range Start': 'Fade In tới đầu vùng',
    'Dissolve Audio Parts': 'Hòa tan Audio Part',
    'Drop Audio Event or MIDI Part': 'Thả Audio Event hoặc MIDI Part',
    'Drop Audio Sample or MIDI Part Here':
        'Thả Audio Sample hoặc MIDI Part vào đây',
    'Freeze/Unfreeze': 'Freeze/Bỏ Freeze',
    'Freeze/Unfreeze Selected Tracks': 'Freeze/Bỏ Freeze Track đã chọn',
    'Freeze MIDI Events': 'Freeze MIDI Event',
    'Freeze MIDI Modifiers': 'Freeze MIDI Modifier',
    'Freeze MIDI Quantize': 'Freeze Quantize MIDI',
    'Export MIDI Loop...': 'Export MIDI Loop...',
    'Export Markers': 'Export Marker',
    'Export Master Track': 'Export Master Track',
    'Export Inspector Patch': 'Export Patch của Inspector',
    'Export Inspector Volume/Pan': 'Export Volume/Pan của Inspector',
    'Export Clip Based Volume (OMF2.0 only)':
        'Export Volume dựa trên Clip (chỉ dành cho OMF2.0)',
    'Export Clip Names (OMF2.0 only)':
        'Export tên Clip (chỉ dành cho OMF2.0)',
    'Export list as text': 'Export danh sách dưới dạng text',
    'Could not export': 'Không thể Export',
    'Delete Unused Audio Files': 'Xóa Audio File không dùng',
    'Custom Warp Settings': 'Cài đặt Warp tùy chỉnh',
    'Audio Hardware Removed': 'Đã tháo phần cứng Audio',
    'Audio Hardware Input': 'Đầu vào phần cứng Audio',
    'Audio Hardware Output': 'Đầu ra phần cứng Audio',
    'Divide Audio Events at Hitpoints': 'Chia Audio Event tại Hitpoint',
    'Enlarge Range to Previous Audio Segment':
        'Mở rộng vùng tới đoạn Audio liền trước',
    'Go to Previous Fade': 'Tới Fade liền trước',
    'Create Unique File Name': 'Tạo tên File duy nhất',
    'Audio Record Modes': 'Các chế độ ghi Audio',
    'Bit Weight': 'Bit trọng số',
    'Bit Rate/Quality': 'Bit Rate/Chất lượng',
    'Browse for File': 'Duyệt tìm file',
    'Browse for File: ': 'Duyệt tìm file: ',
    'Control Change 14 Bit': 'Control Change 14 Bit',
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
       or '\ufffd' in v or not v.strip()]
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
