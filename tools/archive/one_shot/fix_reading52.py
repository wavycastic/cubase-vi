#!/usr/bin/env python3
"""Round 52: audit every term rounds 38-51 changed, across the whole map.

Rounds 38 to 51 changed about twenty terms. Every change is two chances: that
some key nobody revisited still carries the old form, and that a new key was
translated a second way while the change was being made. That second one is
what has actually happened - Material, audio stream, Retrospective Record,
External, factory, Users, Cycle - every single time, and always for the same
reason: nobody compared the new key against the ones already there.

So the audit is mechanical rather than another reading pass. For each term,
list every rendering the map still uses and how many keys use it. A rendering
used by one or two keys against dozens is a leftover, and the table says which:

  tools/audit_terms.py            all terms
  python tools/audit_terms.py Zoom one term

The finds, in order of size:

    "Add External Input (%d avail.)"
      -> "Them dau vao ben ngoai (%d kha dung)"

Six keys say `External Input` - the label itself, `Select Ext. Input`,
`Select External Inputs`, two `Select Source External Input`, and `Source:
External Inputs`. One says "ben ngoai", which is the opposite. Round 33 fixed
`ben ngoai` four times and left this one.

    "Start from Cycle Start" -> "Start tu Cycle Start"

Untranslated - "Start" and "Cycle Start" both left in English, in a family where
`Start from Project Cursor Position`, `Start from Selection Start` and
`Start from Selection or Cycle Start` are all translated. And the sentence that
quotes it, "Start Mode has been changed to 'Start from Cycle Start'", quoted a
DIFFERENT form again, "Bat dau tu dau chu ky", which the label does not say.

`Chu ky` is a CALENDAR cycle. Round 49 fixed three keys of the `Cycle follows`
family to `Cycle` and these two labels were not in that batch - and the label
has to be right first, because the quoted name is copied from it.

    "New Audio Drivers Found" -> "Tao Audio Drivers Found"

`Tao` is CREATE, and round 20 settled that `New` is *moi* - twenty-eight of
thirty-two labels had it wrong at the time. Here the word is wrong AND "Found"
is left in English: a frame with the wrong verb.

    "Clefs with Octave Indicators" -> "... chi bao octave"
    "In general, the voice in which notes appear ..."
      -> "... cung cao do va octave o cac be khac"

Round 39 made Octave `quang tam` in fourteen keys; these two were not in it. The
label family - `Ignore Octave Indicator`, `Respect Octave Indicator`,
`Octave Line`, `Octave Symbol` - writes it with a capital, so this one is
lowercase as well as untranslated.

    "Scale Tempo"                    -> "Phong to/thu nho Tempo"
    "Scale Vertically"               -> "Phong to/thu nho theo chieu doc"
    "Scale Number of Systems by Page Height"
                                       -> "Phong to/thu nho so dong nhac theo
                                           chieu cao trang"
    "Zoom while Locating in Time Scale"
                                       -> "Phong to/thu nho khi dinh vi..."

Four keys where `Scale` is a VERB - zoom the view - rendered as "Phong to/thu
nho" against 67 keys that say `Zoom`. Round 39 made the note-length sense
`quang tam`, which left this one: "Scale" as a musical scale and "scale" as a
resize are three words wearing one spelling, and this is the third.

And three sentences still saying `driver` where the glossary says `trinh dieu
khien`. The six LABELS say `Driver` - `ASIO Driver`, `Audio Driver Setup`,
`No Driver`, `Release Driver...` - and that is right, a panel name is kept in
English. The difference between a label and a sentence is the whole of the
round-33 lesson applied to this word.

  python tools/fix_reading52.py
  python tools/fix_reading52.py --write
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
    # six keys say "External Input"; one says its opposite
    # ==================================================================
    'Add External Input (%d avail.)': 'Thêm External Input (%d khả dụng)',

    # ==================================================================
    # untranslated label, and a sentence quoting a form the label does
    # not use
    # ==================================================================
    'Start from Cycle Start': 'Bắt đầu từ đầu Cycle',
    "Start Mode has been changed to \\'Start from Cycle Start\\'":
        "Chế độ Start đã được đổi thành 'Bắt đầu từ đầu Cycle'",
    'Start from Selection or Cycle Start':
        'Bắt đầu từ vùng chọn hoặc đầu Cycle',

    # ==================================================================
    # "Tao" is CREATE; "New" is "moi" - and "Found" left in English
    # ==================================================================
    'New Audio Drivers Found': 'Đã tìm thấy trình điều khiển Audio mới',

    # ==================================================================
    # Octave, the two keys round 39 did not reach
    # ==================================================================
    'Clefs with Octave Indicators': 'Khóa nhạc kèm chỉ báo Octave',
    'In general, the voice in which notes appear does not influence the '
    'appearance of cautionary accidentals. However, for complex music on '
    'instruments with multiple staves, you may prefer to allow cautionary '
    'accidentals to appear for notes at the same pich and octave in other '
    'voices.':
        'Nhìn chung, bè chứa nốt không ảnh hưởng tới sự xuất hiện của dấu hóa '
        'nhắc lại. Tuy nhiên, với nhạc phức tạp trên nhạc cụ nhiều khuông, bạn '
        'có thể cho phép dấu hóa nhắc lại xuất hiện cho các nốt cùng cao độ và '
        'quãng tám ở các bè khác.',

    # ==================================================================
    # Scale as a VERB, against 67 keys that say Zoom
    # ==================================================================
    'Scale Tempo': 'Zoom Tempo',
    'Scale Vertically': 'Zoom theo chiều dọc',
    'Scale Number of Systems by Page Height':
        'Zoom số dòng nhạc theo chiều cao trang',
    'Zoom while Locating in Time Scale': 'Zoom khi định vị trong Time Scale',

    # ==================================================================
    # driver in prose; the six LABELS say Driver and are right
    # ==================================================================
    'Click here to open the driver control panel.':
        'Nhấp vào đây để mở bảng cấu hình của trình điều khiển.',
    'The audio driver could not be loaded.\\nPlease make sure your audio '
    'hardware is connected correctly to your computer.':
        'Không thể nạp trình điều khiển Audio.\\nVui lòng đảm bảo phần cứng '
        'Audio được kết nối chính xác với máy tính.',
    'The audio hardware using the "%s" audio driver was removed from the '
    'computer.':
        'Phần cứng Audio dùng trình điều khiển Audio "%s" đã bị tháo khỏi máy '
        'tính.',
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
