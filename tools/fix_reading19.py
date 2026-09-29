#!/usr/bin/env python3
"""Round 19 of reading: the M-N block of the general catch-all.

Four slices, 3460..3860, about 400 labels. Two large families, and the second
one is the single biggest pocket of untranslated text still in the map.

THE "No ..." FAMILY. About sixty keys open with "No", and roughly forty of them
had the noun left in English:

    "No Cautionary"          -> "Khong co Cautionary"
    "No Checksum"            -> "Khong co Checksum"
    "No Data"                -> "Khong co Data"
    "No Detected Chords"     -> "Khong co Detected Chords"
    "No Files Found..."      -> "Khong co Files Found..."
    "No Global Tracks"       -> "Khong co Global Tracks"
    "No Modulator"           -> "Khong co Modulator"
    "No Preset"              -> "No Preset"          (nothing translated at all)
    "No Status Info"         -> "Thong tin No Status"
    "No Parameter"           -> "Tham so No"
    "No Section"             -> "Phan No"
    "No error occurred."     -> "Khong co error occurred"   (and lost the full stop)
    "No events selected!"    -> "Khong co events selected!"
    "No global tracks in project" -> "No global tracks trong project"
    "No Track found with Monitoring enabled."
                              -> "No Track found voi Monitoring enabled"
    "No. of Frets"           -> "No. cua Frets"

  Four of them had "No" treated as if it were a noun and pushed to the end,
  which is the same reversal as "Group" in round 16: "Tham so No" reads as
  "parameter no", "Phan No" as "section no", "Thong tin No Status" as
  "info no status". "No." here is the abbreviation of Number, not the negative.

THE "New ..." FAMILY. Thirty-two keys, and twenty-eight of them turned "New"
into "Tao" - create - instead of "moi":

    "New Attribute"  -> "Tao Attribute"
    "New Bank"       -> "Tao Bank"
    "New Folder"     -> "Tao Folder"
    "New Library"    -> "Tao Library"
    "New Preset"     -> "Tao Preset"
    "New Track"      -> "Tao Track"
    ... and so on

  Two siblings were right - "New Project" -> "Project moi", "New Version" ->
  "Phien ban moi" - which is exactly why the other twenty-eight were never
  compared against anything. A user reading "Tao Track" in a menu is being
  told to create a track, not that this is the new-track command; in a project
  with existing tracks the difference matters.

Also two spellings of a scale name, in the map's own output:

    "Myxolydian"  -> "Mixolydian"
    "Myxolydic9/11" -> "Mixolydic 9/11"

  Cubase spells it with a y. The translation had silently corrected it, which
  makes the Vietnamese text disagree with the English the user selected.

And "Natural Minor" -> "Thu tu nhien", which is "natural order". The same
error AGENT.md already records for Aeolian: this is the sixth degree, so
"thu sau tu nhien".

  python tools/fix_reading19.py
  python tools/fix_reading19.py --write
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
    # "New" read as "Tao" (create) instead of "moi"
    # ==================================================================
    'New Attribute': 'Attribute mới',
    'New Bank': 'Bank mới',
    'New Clip Package': 'Clip Package mới',
    'New Collection': 'Collection mới',
    'New Color': 'Màu mới',
    'New Color Set': 'Bảng màu mới',
    'New Color Set Settings': 'Cài đặt bảng màu mới',
    'New Empty Project': 'Project trống mới',
    'New Favorite': 'Mục yêu thích mới',
    'New Files': 'File mới',
    'New Folder': 'Thư mục mới',
    'New Length': 'Độ dài mới',
    'New Library': 'Thư viện mới',
    'New Library...': 'Thư viện mới...',
    'New Link Group Name': 'Tên Link Group mới',
    'New Macro': 'Macro mới',
    'New Map': 'Map mới',
    'New Mixer Bank Zone': 'Mixer Bank Zone mới',
    'New MIDI Track': 'MIDI Track mới',
    'New Parts': 'Part mới',
    'New Pattern': 'Pattern mới',
    'New Preset': 'Preset mới',
    'New Range': 'Vùng mới',
    'New Scheme': 'Scheme mới',
    'New Subbank': 'Subbank mới',
    'New Track': 'Track mới',
    'New Workspace': 'Workspace mới',
    'New Aspect...': 'Aspect mới...',
    'New Copy': 'Bản sao mới',
    'New from Selection': 'Mới từ vùng chọn',
    'New End Position': 'Vị trí kết thúc mới',
    'New Pattern Created ( %d/%d )': 'Đã tạo Pattern mới ( %d/%d )',
    'New Project': 'Project mới',
    'New Version': 'Version mới',

    # ==================================================================
    # the "No ..." family
    # ==================================================================
    'No Cautionary': 'Không dùng',
    'No Cautionary Accidentals': 'Không có dấu hóa nhắc lại',
    'No Checksum': 'Không có mã kiểm tra',
    'No Clip Detected': 'Không phát hiện thấy Clip',
    'No Color Space': 'Không có không gian màu',
    'No Condition set': 'Chưa đặt điều kiện',
    'No Configuration available': 'Không có Configuration khả dụng',
    'No Data': 'Không có dữ liệu',
    'No Detected Chords': 'Không phát hiện thấy hợp âm',
    'No DSP Resource': 'Không có tài nguyên DSP',
    'No Editor Open': 'Không có Editor nào đang mở',
    'No Favorite Defined': 'Chưa định nghĩa mục yêu thích',
    'No Files Found...': 'Không tìm thấy File nào...',
    'No Global Tracks': 'Không có Track toàn cục',
    'No Input Assignment': 'Chưa gán Input',
    'No Mapping selected': 'Chưa chọn Mapping',
    'No Modulator': 'Không có Modulator',
    'No Object Selected': 'Chưa chọn đối tượng',
    'No Parameter': 'Không có tham số',
    'No Picture': 'Không có hình ảnh',
    'No Port available': 'Không có Port khả dụng',
    'No Preset': 'Không có Preset',
    'No Section': 'Không có phần nào',
    'No Sections Detected': 'Không phát hiện thấy phần nào',
    'No Source': 'Không có Source',
    'No Status Info': 'Không có thông tin trạng thái',
    'No Text': 'Không có văn bản',
    'No Track found with Monitoring enabled.':
        'Không tìm thấy Track nào đang bật Monitoring.',
    'No Workspace': 'Không có Workspace',
    'No error occurred.': 'Không có lỗi nào xảy ra.',
    'No events selected!': 'Chưa chọn Event nào!',
    'No global tracks in project': 'Không có Track toàn cục trong Project',
    'No slot available': 'Không có Slot khả dụng',
    'No. of Frets': 'Số Frets',
    'No Link': 'Không có Link',
    'No Machine Control': 'Không có Machine Control',
    'No MIDI Reference': 'Không có MIDI Reference',
    'No MIDI Reference Track': 'Không có MIDI Reference Track',
    'No Map': 'Không có Map',
    'No Mapping': 'Không có Mapping',
    'No Modifier': 'Không có phím bổ trợ',
    'No Output Port': 'Không có cổng đầu ra',
    'No Panner': 'Không có Panner',
    'No Target': 'Không có đích đến',

    # ==================================================================
    # reversed, with "No" treated as a noun and pushed to the end
    # ==================================================================
    'Never Reset Chased Controllers':
        'Không đặt lại Controller đã Chase',
    'Never Show Data': 'Không bao giờ hiện dữ liệu',
    'Next Automation Mode': 'Chế độ Automation kế tiếp',
    'Next Plug-in Parameter Bank': 'Plug-in Parameter Bank kế tiếp',
    'Next Mixer': 'MixConsole kế tiếp',
    'Mute Source Events': 'Tắt tiếng Source Event',
    'Mute Source Tracks': 'Tắt tiếng Source Track',
    'Mute section': 'Tắt tiếng phần',
    'Mute/Unmute Events': 'Tắt tiếng/Bỏ tắt tiếng Event',
    'Mute/Unmute Objects': 'Tắt tiếng/Bỏ tắt tiếng đối tượng',

    # ==================================================================
    # Mute said "Tat tieng" in four keys and "Mute" in the other dozen
    # ==================================================================
    'Mute Events': 'Tắt tiếng Event',
    'Mute Sections': 'Tắt tiếng các phần',
    'Mute Input': 'Tắt tiếng đầu vào',
    'Mute Gaps': 'Tắt tiếng khoảng trống',
    'Mute Silent Segments': 'Tắt tiếng các đoạn im lặng',
    'Mute all Inputs': 'Tắt tiếng tất cả đầu vào',
    'Mute all video tracks': 'Tắt tiếng tất cả Track video',
    'Muted Slash Noteheads': 'Đầu nối gạch chéo bị tắt tiếng',
    'Muted': 'Đã tắt tiếng',

    # ==================================================================
    # a scale name the translation had silently respelled, and "thu tu
    # nhien" - the same error as Aeolian
    # ==================================================================
    'Myxolydian': 'Myxolydian',
    'Myxolydic9/11': 'Myxolydic 9/11',
    'Natural Minor': 'Thứ sáu tự nhiên',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Name contains': 'Tên chứa',
    'Names': 'Các tên',
    'Musical Information': 'Thông tin nhạc lý',
    'Normal Sizing': 'Kích thước chuẩn',
    'Normalize to Integrated Loudness': 'Chuẩn hoá theo Integrated Loudness',
    'NTSC to PAL Pull-Down': 'NTSC sang PAL Pull-Down',

    # ==================================================================
    # "Muted" said "Bi Mute" while its five siblings said "Dang ..."
    # ==================================================================
    'Is Muted': 'Đang bị tắt tiếng',
    'No Parameters Used': 'Không có tham số nào được dùng',
    'No Options Available.': 'Không có tùy chọn khả dụng.',
    'No Automation Object': 'Không có đối tượng Automation',
    'No Editor Available': 'Không có Editor khả dụng',
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
