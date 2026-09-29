#!/usr/bin/env python3
"""Round 10 of reading: windows, panels, pages and menus.

The interface shell. Its own defect class is not scrambles - the sentences are
mostly fine - but a term that changes spelling between a menu item and the
panel it opens:

    "Automation Panel"      -> "Bang Automation"
    "Open Automation Panel"  -> "Mo Automation Panel"
    "Open/Close Automation Panel" -> "Mo/Dong Bang Automation"

    "Device Panel"           -> "Bang thiet bi"
    "Open Device Panel"      -> "Mo Bang Device"
    "Select Device Panel"    -> "Chon Device Panel"

    "Panel" is rendered three ways across nineteen keys: "Panel", "Bang",
    and "Bang thiet bi". One of them, per domain, per decision.

  Pages drift the same way: "Mapping Page" and "Reset Mapping Page" use
  "Trang Mapping" while seven others use "Mapping Page".

  And a few sentences came apart:

    "Please Choose Window to Reset Layout"
      -> "Cu so Please Choose vao Dat lai Layout"
    "Press up to 3 keys to assign remote keys"
      -> "Press up vao 3 keys vao Gan remote keys"
    "View Mode: Page View" -> "Che do xem View Mode: Page"
    "Quick Control Focus (Plug-in Window)"
      -> "Control Focus (Plug-in Window) nhanh"

One regression found here, and it was not in the values but in the tools:
glossary_readthrough.py carried 'Command': 'Command' from an earlier round,
which silently undid fix_reading4's 'Command': 'Lenh' every time it ran. The
bracketed twin "Command[Key]" and the plural "Commands" were both already
"Lenh", so the map had one English label sitting between two Vietnamese ones.
Fixed in the glossary module, because that is the one applied last.

  python tools/fix_reading10.py
  python tools/fix_reading10.py --write
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
    # "Panel": one word, per domain
    # ==================================================================
    'Automation Panel': 'Bảng Automation',
    'Open Automation Panel': 'Mở Bảng Automation',
    'Open/Close Automation Panel': 'Mở/Đóng Bảng Automation',
    'Device Panel': 'Bảng thiết bị',
    'Open Device Panel': 'Mở Bảng thiết bị',
    'Select Device Panel': 'Chọn Bảng thiết bị',
    'Indicates if Device Panel is active':
        'Chỉ báo Bảng thiết bị đang hoạt động',
    'Open/Close Device Panel Section':
        'Mở/Đóng phần Bảng thiết bị',
    'Show ADR Panel': 'Hiện Bảng ADR',
    'Open Sound References Panel': 'Mở Bảng Sound References',
    'Open Studio Panel': 'Mở Bảng Studio',
    'Studio Panel': 'Bảng Studio',
    'Blind Panel': 'Bảng mù',

    # ==================================================================
    # "Mapping Page": one form
    # ==================================================================
    'Mapping Page': 'Mapping Page',
    'Activate Mapping Page': 'Bật Mapping Page',
    'Reset Mapping Page': 'Đặt lại Mapping Page',
    'Page Mapping': 'Mapping Page',
    'Add Mapping Page': 'Thêm Mapping Page',
    'Mapping Page Actions': 'Thao tác Mapping Page',
    'Mapping Page Settings': 'Cài đặt Mapping Page',
    'Mapping Page Type': 'Loại Mapping Page',
    'Next Mapping Page': 'Mapping Page kế tiếp',
    'Previous Mapping Page': 'Mapping Page liền trước',
    'Go to Previous Mapping Page': 'Tới Mapping Page liền trước',

    # ==================================================================
    # Page: one form
    # ==================================================================
    'Page Name': 'Tên Page',
    'Please enter a Page Name': 'Vui lòng nhập tên Page',
    'Please enter a new Page Name': 'Vui lòng nhập tên Page mới',
    'Do you really want to delete the Page?':
        'Bạn có thực sự muốn xóa Page này không?',
    'Remove Current Page': 'Gỡ bỏ Page hiện tại',
    'Untitled Page': 'Page chưa đặt tên',
    'Page Margins': 'Lề Page',
    'Show Next Page': 'Hiện Page kế tiếp',
    'Show Previous Page': 'Hiện Page liền trước',
    'Show Next Meter Page': 'Hiện trang Meter kế tiếp',

    # ==================================================================
    # sentences that came apart
    # ==================================================================
    'Please Choose Window to Reset Layout':
        'Vui lòng chọn cửa sổ để đặt lại Layout',
    'Press up to 3 keys to assign remote keys':
        'Nhấn tối đa 3 phím để gán remote key',
    'View Mode: Page View': 'View Mode: Page View',
    'Quick Control Focus (Plug-in Window)':
        'Quick Control Focus (cửa sổ Plug-in)',
    'Reveal Video Window': 'Mở cửa sổ Video',
    'Setup Window Layout': 'Thiết lập Layout cửa sổ',
    'Preview in Context On/Off': 'Bật/Tắt Preview trong Context',
    'Plug-in Window Focus Only': 'Chỉ tập trung cửa sổ Plug-in',
    'Select Next Plug-in Window': 'Chọn cửa sổ Plug-in kế tiếp',
    'Select Separate Window': 'Chọn cửa sổ riêng',
    'Track and Plug-in Window Focus':
        'Tập trung cửa sổ Track và Plug-in',
    'Window Transparency': 'Độ mờ cửa sổ',
    'Window Width': 'Chiều rộng cửa sổ',
    'Window Zone Controls': 'Điều khiển Window Zone',
    'Window Zones': 'Các Window Zone',
    'Onscreen Window': 'Cửa sổ Onscreen',
    'Onscreen Window is not active.': 'Cửa sổ Onscreen không hoạt động.',
    'Modulators: Assign to Modulator': 'Modulator: Gán vào Modulator',
    'Pattern Editor: Assign to Step Automation':
        'Pattern Editor: Gán vào Step Automation',
    'Increment/Decrement on Left/Right-Click':
        'Tăng/giảm khi nhấp chuột trái/phải',
    'Number of Cells Per Page :': 'Số ô mỗi trang :',
    'Height': 'Chiều cao',
    'Assign to First Unassigned Pad': 'Gán vào Pad chưa gán đầu tiên',
    'Assign Common Version ID': 'Gán ID Version chung',
    'Status bar and shortcut guide': 'Thanh trạng thái và hướng dẫn phím tắt',
    'Mixer Functions Menu': 'Mixer Functions Menu',
    'Set up Toolbar': 'Thiết lập thanh công cụ',
    'Select Panel': 'Chọn Panel',
    'Open Panel': 'Mở Panel',
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
