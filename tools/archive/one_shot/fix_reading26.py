#!/usr/bin/env python3
"""Round 26 of reading: the V-W block, and the last of the general catch-all.

Five slices, 6560..7060. One consistency decision and the rest is the usual
families.

VERSION HAD TWO NAMES. Forty of the forty-three Version labels already said
"Version"; eleven said "Phien ban":

    "Version"          -> "Phien ban"
    "Version:"         -> "Phien ban:"
    "Track Versions"   -> "Cac phien ban Track"
    "Add new Track Version" -> "Them phien ban Track moi"
    "Core Version"     -> "Phien ban Core"
    "Hardware Version" -> "Phien ban phan cung"
    "Program Version"  -> "Phien ban Program"
    "Skin XML Version" -> "Phien ban XML cua Skin"
    "VST Version"      -> "VST Phien ban"      also in the wrong order
    "Software Version" -> "Phan mem Version"   half and half

  Unified on "Version", which is both the majority and the AGENT.md rule that
  DAW terms stay in English. Note the boundary: the thirty-one SENTENCES that
  contain "phien ban" are describing a program's or a file's version -
  "muc phien ban chuong trinh da ho tro", "du lieu khong duoc phien ban
  chuong trinh ho tro" - and there the ordinary Vietnamese word is right. Only
  the LABELS were wrong. A grep for the word would have flagged all forty-two
  and most of them are fine, which is why the fix is eleven hand-written
  entries and not a substitution.

The "Views: ..." family, all ten keys, and three of them taken apart:

    "Views: Cue Sends"     -> "Sends Views: Cue"
    "Views: Device Panels" -> "Bang Views: Device"
    "Views: Quick Controls"-> "Dieu khien Views: Quick"
    "Views: EQs"           -> "Che do xem EQs"        colon dropped
    "Views: VCA"           -> "Che do xem VCA"        colon dropped
    "View/Attributes"      -> "Thuoc tinh View/"      trailing slash orphaned

And two more of the frame class, both of them pure English with a Vietnamese
preposition in the middle:

    "Wait for plug-in to respond"       -> "Wait cho plug-in vao respond"
    "Waiting for participants responses"-> "Waiting cho participants responses"

  The second one has three English words in a row after the preposition. It is
  the purest instance of the class: not a partially translated sentence but a
  Vietnamese preposition with English on both sides of it.

  python tools/fix_reading26.py
  python tools/fix_reading26.py --write
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
    # Version: eleven labels to bring in line with the other thirty-two
    # ==================================================================
    'Version': 'Version',
    'Version:': 'Version:',
    'Track Versions': 'Các Track Version',
    'TrackVersions': 'Các Track Version',
    'Add new Track Version': 'Thêm Track Version mới',
    'Core Version': 'Core Version',
    'Hardware Version': 'Version phần cứng',
    'Program Version': 'Version Program',
    'Skin XML Version': 'Version XML của Skin',
    'Software Version': 'Version phần mềm',
    'VST Version': 'Version VST',

    # ==================================================================
    # the "Views: ..." family - three taken apart, two missing the colon
    # ==================================================================
    'Views: Cue Sends': 'Chế độ xem: Cue Sends',
    'Views: Device Panels': 'Chế độ xem: Device Panels',
    'Views: Quick Controls': 'Chế độ xem: Quick Controls',
    'Views: EQs': 'Chế độ xem: EQs',
    'Views: VCA': 'Chế độ xem: VCA',
    'Views: Filters/Gain': 'Chế độ xem: Filters/Gain',
    'Views: Inserts': 'Chế độ xem: Inserts',
    'Views: Modulators': 'Chế độ xem: Modulators',
    'Views: Sends': 'Chế độ xem: Sends',
    'View/Attributes': 'Chế độ xem/Thuộc tính',
    'View Modes': 'Các chế độ xem',

    # ==================================================================
    # English with a Vietnamese preposition wedged into it
    # ==================================================================
    'Wait for plug-in to respond': 'Chờ Plug-in phản hồi',
    'Waiting for participants responses': 'Đang chờ phản hồi của các bên tham gia',
    'Warn on Processing Overloads': 'Cảnh báo khi xử lý bị quá tải',
    'Verify failed for this node!': 'Xác minh thất bại cho node này!',
    'Vel. Filter': 'Vel. Filter',
    'Velocity Factor': 'Hệ số Velocity',
    'Velocity Shift': 'Dịch Velocity',
    'Velocity on Mouse Click': 'Velocity khi nhấp chuột',
    'Volume Automation Precision': 'Độ chính xác Automation âm lượng',
    'Volume Controller Curve': 'Đường cong Controller âm lượng',
    'Volume Max.': 'Âm lượng tối đa',

    # ==================================================================
    # "Vertical X" where the noun had been pushed behind its modifier
    # ==================================================================
    'Vertical Justification': 'Căn dọc',
    'Vertical Pitch Spread': 'Phân bố cao độ dọc',
    'Vertical Spacing': 'Khoảng cách dọc',
    'Video Files': 'Các file Video',
    'Video Files Color Space': 'Không gian màu của file Video',
    'Video Follows Editing On/Off': 'Bật/Tắt Video bám theo chỉnh sửa',
    'Video Output Devices': 'Thiết bị đầu ra Video',
    'Video Playback': 'Phát lại Video',
    'Video Player': 'Trình phát Video',
    'Visible Loudness Lower Limit': 'Giới hạn dưới Loudness đang hiện',
    'Visible Loudness Upper Limit': 'Giới hạn trên Loudness đang hiện',
    'Visible Controllers': 'Các Controller đang hiện',
    'Visible Controls': 'Các Control đang hiện',
    'Voices': 'Các bè',
    'Voicings': 'Voicings',
    'Waveform Brightness': 'Độ sáng dạng sóng',
    'Warped/Pitched': 'Đã Warp/đổi Pitch',
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
