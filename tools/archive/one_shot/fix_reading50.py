#!/usr/bin/env python3
"""Round 50: the ui domain, long values 0-49.

A key that is not its own English, and a value that is right because of it:

    key    "Popup Toolbar (static one with modifier click)"
    column "Press modifier key + click to open as static toolbar"
    value  "Thanh cong cu Pop-up (Co dinh khi nhap phim bo tro)"

The value translates the KEY and is exactly right. The second column is a
tooltip that describes the control, and reading the second column instead of the
key is how this round nearly "fixed" a correct value - the batch reported NOT IN
CUBASE and the entry was dropped. Second time the tool has caught that, after
round 41's "creating Warp Tabs".

Worth its own note, because the trap is general: for a key whose text differs
from its English, the value follows the KEY. The summary of this project has
said it since round 2 - cot 1 khac cot o nhieu key - and it is still the easiest
thing to get wrong, because every reading tool prints the English.

The other find is the eleventh of its kind, a word read as a different word:

    "When the page is less full than the threshold for justifying staves, no
     vertical justification occurs."
      -> "Khi trang it chu hon nguong de can deu khuong nhac, se khong co viec
         can theo chieu doc."

"It chu" is FEWER WORDS. "Less full" is "it day hon" - how full the page is,
which is the whole subject of "justify".

Then the standing classes:

    "Press up to 5 keys to assign remote keys to sections"
      -> "Nhan toi da 5 phim de gan phim Remote cho cac phan doan"
    "Press up to 5 keys to assign remote keys to subsections"
      -> "Nhan toi da 5 phim de gan phim tu xa cho cac phan con"   (round 36)

"phim Remote" and "phim tu xa" in a pair of sentences that are identical for
six words.

    "Create new empty Track Version and assign common version ID"
      -> "... gan ID chung cho cac version"

"version" lowercase, in a family where every other key writes Version with a
capital.

    "Inserts State (Bypass Inserts with click/Context-menu shows usage)"
      -> "Trang thai Insert (... Menu ngu canh hien muc dung)"

"muc dung" is a usage LEVEL. "Context-menu shows usage" means the context menu
lists where that button is used. Two siblings had it.

And "xuất xưởng" in three keys against "Factory" in twelve. The glossary settled
Factory as English in round 22, four earlier spellings were unified then, and
these three were written afterwards by hand. "Add new profile with factory
settings" says "cai dat Factory" and is right.

  python tools/fix_reading50.py
  python tools/fix_reading50.py --write
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
    # "less full" read as "fewer words"
    # ==================================================================
    'When the page is less full than the threshold for justifying staves, no '
    'vertical justification occurs.':
        'Khi trang ít đầy hơn ngưỡng căn đều khuông nhạc, sẽ không căn theo chiều '
        'dọc.',

    # ==================================================================
    # one English noun, two renderings, in a pair of sentences that are
    # identical for six words
    # ==================================================================
    'Press up to 5 keys to assign remote keys to sections':
        'Nhấn tối đa 5 phím để gán phím từ xa cho các phân đoạn',

    # ==================================================================
    # "muc dung" is a usage LEVEL; the context menu lists where the
    # button is used
    # ==================================================================
    'Inserts State (Bypass Inserts with click/Context-menu shows usage)':
        'Trạng thái Insert (Nhấp để Bypass Insert/Menu ngữ cảnh hiện cách dùng)',
    'Modulators State (Bypass Modulators with click/Context-menu shows usage)':
        'Trạng thái Modulator (Nhấp để Bypass Modulator/Menu ngữ cảnh hiện cách '
        'dùng)',
    'Sends State (Bypass Sends with click/Context-menu shows usage)':
        'Trạng thái Send (Nhấp để Bypass Send/Menu ngữ cảnh hiện cách dùng)',

    # ==================================================================
    # Factory, as the glossary settled it in round 22
    # ==================================================================
    'This option deletes the preferences of current and older program '
    'installations and initializes the program with factory settings. Please '
    'be aware that all your custom settings will be removed. This operation '
    'cannot be undone.':
        'Tùy chọn này xóa các tùy chọn của bản cài đặt hiện tại và các bản cũ '
        'hơn, rồi khởi tạo lại chương trình với cài đặt Factory. Lưu ý rằng toàn '
        'bộ cài đặt tùy chỉnh của bạn sẽ bị gỡ bỏ. Thao tác này không thể hoàn '
        'tác.',
    'This option disables your custom preferences and initializes the program '
    'with factory settings. Your preferences are available after restarting '
    'the program.':
        'Tùy chọn này tạm tắt các tùy chọn tùy chỉnh của bạn và khởi tạo chương '
        'trình với cài đặt Factory. Các tùy chọn của bạn sẽ khả dụng lại sau khi '
        'khởi động lại chương trình.',
    'This will reset the command assignment to the factory default.':
        'Thao tác này sẽ đặt lại phép gán lệnh về mặc định Factory.',

    # ==================================================================
    # small
    # ==================================================================
    'Create new empty Track Version and assign common version ID':
        'Tạo Track Version rỗng mới và gán ID chung cho các Version',
    'Duplicate current Track Version and assign common version ID':
        'Nhân bản Track Version hiện tại và gán ID chung cho các Version',
    'The connection could not be created, as the destination does not belong '
    'to this effect. Make sure to assign a destination that belongs to this '
    'effect.':
        'Không thể tạo kết nối vì đích không thuộc Effect này. Hãy đảm bảo gán một '
        'đích thuộc Effect này.',
    'The destination parameter could not be selected, as the destination does '
    'not belong to this effect. Make sure to assign a destination that '
    'belongs to this effect.':
        'Không thể chọn tham số đích vì đích không thuộc Effect này. Hãy đảm bảo '
        'gán một đích thuộc Effect này.',
    'If you reconnect the hardware and the dialog does not close '
    'automatically, select the corresponding ASIO driver from the list and '
    'click "OK".':
        'Nếu bạn kết nối lại phần cứng và hộp thoại không tự đóng, hãy chọn trình '
        'điều khiển ASIO tương ứng từ danh sách và nhấp "OK".',
    'Double-click to rename Link Group (Shift + Double-click to open Link '
    'Group Settings dialog)':
        'Nhấp đúp để đổi tên Link Group (Nhấn [SHIFT] + nhấp đúp để mở hộp thoại '
        'cài đặt Link Group)',
    'Do you really want to leave the page and discard your input?':
        'Bạn có thực sự muốn rời khỏi trang và hủy bỏ những gì bạn đã nhập?',
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
