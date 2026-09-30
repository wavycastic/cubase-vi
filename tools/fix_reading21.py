#!/usr/bin/env python3
"""Round 21 of reading: the P-R block of the general catch-all.

Six slices, 4260..4860, about 600 labels. Four families reversed, and one of
them is the largest single group of reversals I have found.

THE "RANGE ..." FAMILY - twenty-two keys, every one with the tail first:

    "Range"                        -> "Pham vi"   (while "Range 1" said "Vung 1")
    "Range End"                    -> "Vung Ket thuc"
    "Range Start"                  -> "Vung Bat dau"
    "Range Length"                 -> "Do dai Range"
    "Range Selection Tool"         -> "Cong cu Range Selection"
    "Range Selection Tool: Selection B" -> "Vung Selection Tool: Selection B"
    "Range Target"                 -> "Vung Target"
    "Range Tool"                   -> "Cong cu Range"
    "Range Tool Splits Partly Selected Events"
                                    -> "Event Range Tool Splits Partly Selected"
    "Range End in PPQ"             -> "Range End trong PPQ"

  Note that "Range Selection Tool: Selection A" was already correct - "Cong cu
  chon vung: Vung chon A" - one key above the broken twin. That is how it got
  missed: the correct one was the evidence that the family was translatable,
  not a reason to check it.

THE "QUICK ..." FAMILY - the same shape, seven keys:

    "Quick Analysis"         -> "Analysis nhanh"
    "Quick Control Focus"    -> "Nhanh Dieu khien Tap trung"
    "Quick Control Focus (Track)" -> "Control Focus (Track) nhanh"
    "Quick Controls on/off"  -> "Controls on/off nhanh"
    "Quick Loudness Analysis"-> "Loudness Analysis nhanh"
    "Quick Rescan Disk"      -> "Rescan Disk nhanh"

  while "Focus Quick Controls" and "Enable Quick Controls", one screen away,
  were both correct. So the map had "Tap trung Quick Control" and "Nhanh Dieu
  khien Tap trung" for the same feature.

THE "PROJECT ..." FAMILY - fourteen keys:

    "Project Duration"     -> "Duration Project"
    "Project History"      -> "History Project"
    "Project Ownership"    -> "Ownership Project"
    "Project Structure"    -> "Structure Project"
    "Project Templates"    -> "Templates Project"
    "Project Root Key"     -> "Key Project Root"
    "Project Input Transformer" -> "Transformer Project Input"
    "Project & Tracks"     -> "Track Project &"
    "Project Clipboard"    -> "Clipboard Project"
    "Project Time Displays"-> "Project Thoi gian Hien thi"
    "Project Workspaces"   -> "Workspaces Project"

  "Project Time Displays" is the worst form: three of four words displaced, and
  what is left is not a phrase in any language.

"Previous" said "truoc" in eleven keys while "Next" said "ke tiep" in eleven
more, so the two halves of one navigation family did not match. Settled on
"lien truoc" for Previous, which is the counterpart AGENT.md already uses
elsewhere.

And "Punch In" said "Ghi vao" in one key and "Punch In" in four, so the record
start point had two names depending on which menu you opened.

  python tools/fix_reading21.py
  python tools/fix_reading21.py --write
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
    # the "Range ..." family
    # ==================================================================
    'Range': 'Vùng',
    'Range End': 'Cuối vùng',
    'Range Start': 'Đầu vùng',
    'Range End in PPQ': 'Cuối vùng tính bằng PPQ',
    'Range Start in PPQ': 'Đầu vùng tính bằng PPQ',
    'Range Length': 'Độ dài vùng',
    'Range Selection Follows Track Selection':
        'Vùng chọn bám theo vùng chọn Track',
    'Range Selection Tool': 'Công cụ chọn vùng',
    'Range Selection Tool: Selection B': 'Công cụ chọn vùng: Vùng chọn B',
    'Range Target': 'Đích vùng',
    'Range Tool': 'Công cụ vùng',
    'Range Tool Splits Partly Selected Events':
        'Công cụ vùng tách các Event được chọn một phần',

    # ==================================================================
    # the "Quick ..." family
    # ==================================================================
    'Quick Analysis': 'Phân tích nhanh',
    'Quick Control Focus': 'Tập trung Quick Control',
    'Quick Control Focus (Track)': 'Tập trung Quick Control (Track)',
    'Quick Control %d': 'Quick Control %d',
    'Quick Controls on/off': 'Bật/Tắt Quick Controls',
    'Quick Loudness Analysis': 'Phân tích Loudness nhanh',
    'Quick Rescan Disk': 'Quét lại đĩa nhanh',

    # ==================================================================
    # the "Project ..." family
    # ==================================================================
    'Project & Tracks': 'Project & Track',
    'Project Clipboard': 'Clipboard của Project',
    'Project Duration': 'Thời lượng Project',
    'Project Frame Rate': 'Frame Rate của Project',
    'Project History': 'Lịch sử Project',
    'Project Input Transformer': 'Input Transformer của Project',
    'Project Input Transformer...': 'Input Transformer của Project...',
    'Project Ownership': 'Quyền sở hữu Project',
    'Project Preview': 'Project Preview',
    'Project Preview created': 'Đã tạo Project Preview',
    'Project Preview removed': 'Đã gỡ bỏ Project Preview',
    'Project Root Key': 'Key gốc của Project',
    'Project Structure': 'Cấu trúc Project',
    'Project Templates': 'Template của Project',
    'Project Time Displays': 'Hiển thị thời gian Project',
    'Project Workspace': 'Workspace của Project',
    'Project Workspaces': 'Các Workspace của Project',
    'Project Logical Editor': 'Logical Editor của Project',
    'Project Logical Editor...': 'Logical Editor của Project...',
    'Project Logical Editor Presets': 'Preset Logical Editor của Project',
    'Project Colors Setup': 'Thiết lập màu Project',
    'Project Colors Setup...': 'Thiết lật màu Project...',
    'Project Synchronisation Setup': 'Thiết lật đồng bộ Project',
    'Project Synchronization Setup...': 'Thiết lật đồng bộ Project...',

    # ==================================================================
    # "Previous" said "truoc" where "Next" said "ke tiep"
    # ==================================================================
    'Previous': 'Liền trước',
    'Previous Chain Step': 'Chain Step liền trước',
    'Previous Dropout': 'Dropout liền trước',
    'Previous Mixer Bank': 'Mixer Bank liền trước',
    'Previous Pattern': 'Pattern liền trước',
    'Previous Plug-in Parameter Bank': 'Plug-in Parameter Bank liền trước',
    'Previous Preset': 'Preset liền trước',
    'Previous Subpage': 'Subpage liền trước',
    'Previous Tool': 'Công cụ liền trước',
    'Previous Version': 'Version liền trước',
    'Prev[Key]': 'Phím liền trước',

    # ==================================================================
    # the "Preview ..." family, where three of them had the tail first
    # ==================================================================
    'Preview Pause': 'Dừng tạm Preview',
    'Preview Start': 'Bắt đầu Preview',
    'Preview Stop': 'Dừng Preview',
    'Preview:': 'Preview:',
    'Preview Active On/Off': 'Bật/Tắt Preview đang hoạt động',
    'Previewer Sequence Mode': 'Chế độ chuỗi Previewer',
    'Primary Time Display': 'Hiển thị thời gian chính',
    'Primary Parameter: Decrease': 'Tham số chính: Giảm',
    'Primary Parameter: Fine Decrease': 'Tham số chính: Giảm tinh vi',
    'Primary Parameter: Fine Increase': 'Tham số chính: Tăng tinh vi',
    'Primary Parameter: Increase': 'Tham số chính: Tăng',

    # ==================================================================
    # "Punch In" had two names depending on the menu
    # ==================================================================
    'Punch In': 'Punch In',
    'Punch Out': 'Punch Out',
    'Punch in previewing parameters now':
        'Punch In và xem trước tham số ngay',
    'Program': 'Program',
    'Programs': 'Các Program',
    'Program Plug-ins': 'Plug-in trong Program',
    'Program Version': 'Phiên bản Program',
    'Prop Type': 'Loại Property',
    'Ramp': 'Ramp',
    'Randomize Parameter': 'Ngẫu nhiên hóa tham số',
    'Randomize Settings': 'Ngẫu nhiên hóa cài đặt',
    'Random1Max': 'Random 1 Max.',
    'Random1Min': 'Random 1 Min.',
    'Random2Max': 'Random 2 Max.',
    'Random2Min': 'Random 2 Min.',
    'RMS Resolution in ms': 'Độ phân giải RMS tính bằng ms',
    'Random 1': 'Ngẫu nhiên 1',
    'Random 2': 'Ngẫu nhiên 2',
    'RTF Text': 'Văn bản RTF',
    'Random Target': 'Đích ngẫu nhiên',
    'Random1Target': 'Random 1 Target',
    'Random2Target': 'Random 2 Target',
    'Rack Instruments': 'Rack Instrument',

    # ==================================================================
    # English left in place of a word
    # ==================================================================
    'Project download failed.': 'Không thể tải Project về.',
    'Project size of %s exceeded!': 'Kích thước Project %s đã vượt quá!',
    'Press two keys to define range': 'Nhấn hai phím để xác định vùng',
    'Processes': 'Các Process',
    'Projects': 'Các Project',
    'Overwrite existing script at %s': 'Ghi đè Script đã có tại %s',
    'Print': 'In',
    'Print...': 'In...',
    'Proceed and Keep': 'Tiếp tục và giữ lại',
    'Program-gated loudness measurement according to EBU R 128':
        'Đo Loudness theo chương trình, tuân theo EBU R 128',
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
