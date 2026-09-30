#!/usr/bin/env python3
"""Round 49: the rest of the transport domain, long values 50-96.

`Cycle` is three keys and `Chu ky` is three, in a family of five:

    "Activated: Cycle follows when locating to Markers"
      -> "Da bat: Cycle bam theo khi dinh vi toi Marker"
    "Deactivated: Cycle follows when locating to Markers"
      -> "Da tat: Chu ky bam theo khi dinh vi toi Marker"
    "Toggle: Cycle follows when locating to Markers"
      -> "Chuyen doi: Chu ky bam theo khi dinh vi toi Marker"
    "Cycle Follows When Locating to Markers"
      -> "Chu ky bam theo khi dinh vi toi Marker"

`Chu ky` is a CALENDAR cycle, and Cubase's Cycle is the loop between two
locators. Two and two, decided by which key was translated first, and a
round-34 fix went the wrong way without noticing: this round reads the family
together.

`Jump Mode` the same, one key each way:

    "Jump Mode (determines when the next live section will play)"
      -> "Che do nhay (xac dinh thoi diem phat doan live ke tiep)"
    "Stop Jump Mode" -> "Dung che do Jump"

`Che do nhay` is a proper Vietnamese phrase and `Jump Mode` is Cubase's name for
a MIDI Remote setting, so the two siblings that keep it are right.

`Timecode ngoai`, External a sixth time since round 33.

And one dropped phrase, in the tempo tooltips:

    "Tempo events are generated up to the point, where an irregular tempo
     change is detected. Apply the Smooth Tempo function if the tempo OF THE
     MATERIAL is assumed to be constant."
      -> "... Ap dung chung nang Smooth Tempo neu Tempo duoc gia dinh la
         hang so."

"neu Tempo duoc gia dinh la hang so" - assumed to be constant WHAT? The
tempo of the material. The sentence says the tempo is constant, which is a
tautology, and drops the only thing it could be constant relative to. The
sibling sentence, in the same menu, still has it.

`Retrospective Record Buffer` kept its English where fourteen sibling keys now
say "ghi hoi to", and `Emphasis` is "lam noi bat" in one key and "nhan manh"
in the other - round 20 settled "emphasis" as "lam noi bat", because to
emphasise is to make something stand out, not to press harder.

  python tools/fix_reading49.py
  python tools/fix_reading49.py --write
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
    # Cycle is the loop between two locators, not a calendar cycle
    # ==================================================================
    'Deactivated: Cycle follows when locating to Markers':
        'Đã tắt: Cycle bám theo khi định vị tới Marker',
    'Toggle: Cycle follows when locating to Markers':
        'Chuyển đổi: Cycle bám theo khi định vị tới Marker',
    'Cycle Follows When Locating to Markers':
        'Cycle bám theo khi định vị tới Marker',

    # ==================================================================
    # a dropped phrase: "the tempo OF THE MATERIAL"
    # ==================================================================
    'Tempo events are generated up to the point, where an irregular tempo '
    'change is detected.\\nApply the Smooth Tempo function if the tempo of the '
    'material is assumed to be constant.':
        'Các Tempo Event được tạo tới điểm phát hiện thay đổi Tempo bất '
        'thường.\\nÁp dụng chức năng Smooth Tempo nếu Tempo của chất liệu được '
        'giả định là hằng số.',

    # ==================================================================
    # Jump Mode is Cubase's name for the setting, as its two siblings say
    # ==================================================================
    'Jump Mode (determines when the next live section will play)':
        'Jump Mode (xác định thời điểm phát đoạn live kế tiếp)',

    # ==================================================================
    # External, a sixth time since round 33
    # ==================================================================
    'Transport stays in Play Mode even if External Timecode Stops':
        'Transport vẫn ở chế độ phát dù Timecode External có dừng',

    # ==================================================================
    # Retrospective Record, where fourteen siblings say "ghi hoi to"
    # ==================================================================
    'Retrospective Record Buffer Size in Events':
        'Kích thước Buffer ghi hồi tố trong Events',

    # ==================================================================
    # emphasis is "lam noi bat" - round 20, on the grounds that to
    # emphasise is to make something stand out, not to press harder
    # ==================================================================
    'Use Metronome Click Pattern Level for Grid Line Emphasis':
        'Dùng mức Pattern Click Metronome để làm nổi bật đường Grid',

    # ==================================================================
    # the "[ALT] + nhap" family, two more
    # ==================================================================
    'Punch In (use [ALT + click] to set to Project Cursor Position)':
        'Punch In (dùng [ALT + nhấp chuột] để đặt theo vị trí con trỏ Project)',
    'Punch Out (use [ALT + click] to set to Project Cursor Position)':
        'Punch Out (dùng [ALT + nhấp chuột] để đặt theo vị trí con trỏ Project)',

    # ==================================================================
    # small
    # ==================================================================
    'Defines what happens DURING cycle recording...':
        'Xác định điều gì xảy ra trong khi ghi theo Cycle...',
    'Adds/subtracts the selected amount of frames to the position sent via '
    'RS422 Out (record mode)':
        'Cộng/trừ số lượng Frame đã chọn vào vị trí gửi qua RS422 Out '
        '(chế độ ghi)',
    'Tempo (changes the current tempo at the project cursor position)':
        'Tempo (thay đổi Tempo hiện tại tại vị trí con trỏ Project)',
    'Record Destination when track is enabled for both part record and '
    'automation write':
        'Đích ghi khi Track được bật cho cả ghi Part và ghi Automation',
    'The Locator Range is empty, inverted or its length has been changed. '
    "Please use 'Insert as Linear Recording.'":
        "Dải Locator đang trống, bị đảo ngược hoặc độ dài đã thay đổi. Vui lòng "
        "dùng 'Chèn dạng bản ghi tuyến tính'.",
    'Clicking Locator Range in Upper Part of the Ruler Activates Cycle':
        'Nhấp vào Dải Locator ở phần trên của thước đo sẽ bật Cycle',
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
