#!/usr/bin/env python3
"""Round 4 of reading: the Key Command family, plus what ui/project/media
still had.

The largest find here is a term that has two renderings in the same map.
"Key Commands" is established as "phím tắt" and a dozen keys use that. A
second dozen put the head noun in front instead, which reads as neither:

    "Assigned Key Commands"      -> "Lệnh Assigned Key"
    "Customized Key Commands"    -> "Lệnh Customized Key"
    "Unassigned Key Commands"    -> "Lệnh Unassigned Key"
    "Remove Key Command"         -> "Gỡ bỏ Lệnh Key"
    "Toggle Alternate Key Commands" -> "Chuyển đổi Lệnh Alternate Key"

"Key Command" is a keyboard shortcut, so every member becomes "phím tắt".
"Command" on its own is "lệnh" - but the bare key was left in English while
its plural was translated, which is why this looked like two systems.

Also here:
  - two keys where the sentence lost its subject or its last sentence
  - "diễn giải" for "interpret" of a CSV file, which reads as "explain"
  - "44,1 kHz" where the English said "44.1 kHz" - a decimal separator the
    translation must not touch
  - "warp markers" -> "marker Warp", the reversed head noun once more

  python tools/fix_reading4.py
  python tools/fix_reading4.py --write
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
    # "Key Command" = phim tat. One rendering for the whole family.
    # ==================================================================
    'Assigned Key Commands': 'Phím tắt đã gán',
    'Customized Key Commands': 'Phím tắt tùy chỉnh',
    'Unassigned Key Commands': 'Phím tắt chưa gán',
    'Remove Key Command': 'Gỡ bỏ phím tắt',
    'Reset Key Command': 'Đặt lại phím tắt',
    'Toggle Alternate Key Commands': 'Chuyển đổi phím tắt thay thế',
    'Key Command Mapping': 'Gán phím tắt',
    'Key[Key Commands dialog]': 'Phím tắt',
    'Reset User Command Assignments': 'Đặt lại các phép gán lệnh của người dùng',

    # ==================================================================
    # "Command" on its own = lenh. The bare key was left English while
    # its plural was translated.
    # ==================================================================
    'Command': 'Lệnh',
    'Command[Key]': 'Lệnh',
    'Command Categories': 'Danh mục Lệnh',
    'Add Command to Macro': 'Thêm Lệnh vào Macro',
    'Remove Command from Macro': 'Gỡ bỏ Lệnh khỏi Macro',
    'Open Command Destination': 'Mở nơi nhận của Lệnh',
    'Multiple Command Messages': 'Nhiều thông điệp lệnh',
    'Enable Record Command': 'Bật lệnh ghi',
    'Basic Commands': 'Lệnh cơ bản',
    'Other Commands': 'Lệnh khác',
    'Transport Commands': 'Lệnh Transport',
    'Post-Process Commands': 'Lệnh Post-Process',
    'Pre & Post Commands': 'Lệnh Pre & Post',
    'Pre-Process Commands': 'Lệnh Pre-Process',
    'Press Key/Search Command': 'Nhấn phím/Tìm kiếm lệnh',
    'Use Standard Zoom Commands': 'Dùng lệnh Zoom tiêu chuẩn',
    'Send Shuttle Command instead of Fast Forward/Rewind':
        'Gửi lệnh Shuttle thay cho Fast Forward/Rewind',
    'Send Still Command instead of Stop': 'Gửi lệnh Still thay cho Stop',

    # ==================================================================
    # Mapping Page, two keys scrambled into "Trang Go to Next Mapping"
    # ==================================================================
    'Go to Next Mapping Page': 'Tới Mapping Page kế tiếp',
    'Go to Previous Mapping Page': 'Tới Mapping Page trước',

    # ==================================================================
    # plural dropped, and "in focus" is not "được chọn"
    # ==================================================================
    'Follow Plug-in Window in Focus':
        'Theo cửa sổ Plug-in đang được tập trung',
    'Modulators State (Bypass Modulators with click/Context-menu shows usage)':
        'Trạng thái Modulator (Nhấp để Bypass Modulator/Menu ngữ cảnh hiện '
        'mức dùng)',
    'Sends State (Bypass Sends with click)':
        'Trạng thái Send (Nhấp để Bypass Send)',
    'Sends State (Bypass Sends with click/Context-menu shows usage)':
        'Trạng thái Send (Nhấp để Bypass Send/Menu ngữ cảnh hiện mức dùng)',
    'Inserts State (Bypass Inserts with click)':
        'Trạng thái Insert (Nhấp để Bypass Insert)',
    'Inserts State (Bypass Inserts with click/Context-menu shows usage)':
        'Trạng thái Insert (Nhấp để Bypass Insert/Menu ngữ cảnh hiện mức '
        'dùng)',
    'EQs State (Bypass EQs with click)':
        'Trạng thái EQ (Nhấp để Bypass EQ)',

    # ==================================================================
    # "chữ" means "letter". The page is not less full of letters.
    # ==================================================================
    'When the page is less full than the threshold for justifying staves, no '
    'vertical justification occurs.':
        'Khi trang ít nội dung hơn ngưỡng căn đều khuông nhạc, sẽ không có '
        'căn theo chiều dọc.',

    # ==================================================================
    # lost content
    # ==================================================================
    'Click and drag this page to move or copy it, or to swap it with another '
    'page.':
        'Nhấp và kéo trang này để di chuyển hoặc sao chép, hoặc để hoán đổi '
        'với một trang khác.',
    'Could not open the file for reading.\\nIs the file already opened by '
    'another program?':
        'Không thể mở file để đọc.\\nFile đã được chương trình khác mở chưa?',
    'This option deletes the preferences of current and older program '
    'installations and initializes the program with factory settings. Please '
    'be aware that all your custom settings will be removed. This operation '
    'cannot be undone.':
        'Tùy chọn này xóa các tùy chọn của bản cài đặt hiện tại và các bản cũ '
        'hơn, rồi khởi tạo lại chương trình với cài đặt xuất xưởng. Lưu ý rằng '
        'toàn bộ cài đặt tùy chỉnh của bạn sẽ bị gỡ bỏ. Thao tác này không thể '
        'hoàn tác.',
    'This option uses the preferences currently stored in the program.':
        'Tùy chọn này dùng các tùy chọn hiện đang được lưu trong chương trình.',

    # ==================================================================
    # "interpret" of a CSV file is "phân tích", not "diễn giải"
    # ==================================================================
    'Could not interpret the CSV file.':
        'Không thể phân tích file CSV.',
    'Could not interpret the CSV file. Maybe the file is in the wrong CSV '
    'format?\\nPlease check the separator setting.\\nAn error was found near '
    'this position:\\n\\n':
        'Không thể phân tích file CSV. Có thể file sai định dạng CSV?\\nVui lòng '
        'kiểm tra cài đặt dấu phân cách.\\nPhát hiện lỗi gần vị trí này:\\n\\n',
    'Could not interpret the CSV file. Please check your separator settings.'
    '\\nAn error was found near this position:\\n\\n':
        'Không thể phân tích file CSV. Vui lòng kiểm tra cài đặt dấu phân cách.'
        '\\nPhát hiện lỗi gần vị trí này:\\n\\n',
    'Reinterpret Bars': 'Phân tích lại các Bar',

    # ==================================================================
    # reversed head noun, and "metering" is a noun not a noun phrase
    # ==================================================================
    'Map Input Bus Metering to Audio Track (in Direct Monitoring)':
        'Map Metering của Input Bus sang Audio Track (khi Direct Monitoring)',
    'Phase-coherent AudioWarp operations require equal event lengths, '
    'positions, and warp markers. Click "Bounce" to create such events.':
        'Các thao tác AudioWarp đồng pha cần các Event có độ dài, vị trí và '
        'Warp Marker bằng nhau. Nhấp "Bounce" để tạo các Event như vậy.',

    # ==================================================================
    # a verb with no subject
    # ==================================================================
    'Reaching the 2GB limit of the OMF file format, some media will be '
    'missing...':
        'Đã đạt giới hạn 2GB của định dạng file OMF, một số Media sẽ bị thiếu...',
    'Reaching the 2GB limit of the OMF file format, the followig media will '
    'not be embedded.':
        'Đã đạt giới hạn 2GB của định dạng file OMF, các Media sau sẽ không '
        'được nhúng.',

    # ==================================================================
    # "swap" left English in the middle
    # ==================================================================
    'Select Primary Time Format\\nUse [ALT + click] swap Primary & Secondary '
    'Time Formats':
        'Chọn Primary Time Format\\nDùng [ALT + nhấp] để hoán đổi Primary & '
        'Secondary Time Format',
    'Select Secondary Time Format\\nUse [ALT + click] swap Primary & '
    'Secondary Time Formats':
        'Chọn Secondary Time Format\\nDùng [ALT + nhấp] để hoán đổi Primary & '
        'Secondary Time Format',

    # ==================================================================
    # term drift: the sibling keys keep "Primary Time Format" in English
    # ==================================================================
    'Tempo and signature tracks can only be imported if \'Bars+Beats\' is '
    'selected as \'Primary Time Format\'.':
        'Chỉ có thể Import Tempo Track và Signature Track nếu \'Bars+Beats\' '
        'được chọn làm \'Primary Time Format\'.',
    'Link to Primary Time Format': 'Liên kết với Primary Time Format',
}

# ---------------------------------------------------------------------- #
# families
# ---------------------------------------------------------------------- #

# the network-interfaces dialog lost everything after the second sentence:
# the subnet mask explanation and how to reopen the box.
NETWORK_LONG = (
    'This computer has multiple network interfaces. Please determine which \\n'
    'interface is connected to the Nuendo workgroup and select the \\n'
    'corresponding IP address. \\n\\nThe subnet mask specifies in which range '
    'broadcast messages \\nare sent to identify other Nuendo workstations. The '
    'default subnet mask \\nis a common choice, please adopt it for your '
    'specific network adapter.\\n\\nTo reopen this dialog, deactivate the '
    'network and activate it again.')
NETWORK_VI = (
    'Máy tính có nhiều giao diện mạng. Vui lòng xác định giao diện nào \\n'
    'được kết nối tới nhóm làm việc Nuendo và chọn địa chỉ IP \\n'
    'tương ứng. \\n\\nSubnet mask xác định phạm vi mà thông điệp broadcast \\n'
    'được gửi để nhận diện các máy trạm Nuendo khác. Subnet mask mặc định \\n'
    'là một lựa chọn phổ biến, vui lòng dùng nó cho adapter mạng của bạn.'
    '\\n\\nĐể mở lại hộp thoại này, hãy tắt mạng rồi bật lại.')

# Note on "44,1 kHz": the English key itself uses a comma decimal separator,
# so the translation matching it is correct, not a defect. No rule here.

# ---------------------------------------------------------------------- #

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()
if NETWORK_LONG in src:
    real[NETWORK_LONG] = NETWORK_VI

fixes = dict(real)

bad = [(k, v) for k, v in fixes.items()
       if sorted(PH.findall(src.get(k, ''))) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src.get(k, "?")!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in fixes.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:56]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v!r}')

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
