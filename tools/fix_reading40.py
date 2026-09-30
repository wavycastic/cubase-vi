#!/usr/bin/env python3
"""Round 40: the rest of the music-theory long values, 45 sentences.

Two missing sentences, and the same one twice.

    "The project contains files or crossfades in 32-bit float format. Since OMF
     does not support this format, the files will be converted and exported as
     embedded data. Please note that this conversion might lead to clipping!"
      -> "Project chua cac file hoac Crossfade o dinh dang 32-bit float. Vi OMF
         khong ho tro dinh dang nay, cac file se duoc chuyen doi va Export
         dang du lieu nhung."

"Please note that this conversion might lead to clipping" - the warning that
the export can DESTROY the audio - is gone. The user gets a silent truncation.

    "... Please contact the manufacturer of the plug-in for an updated
     version."
      -> "Vui long lien he nha san xuat de co phien ban moi hon."

"of the plug-in" dropped: the message now tells you to contact the manufacturer
of something, without saying what.

And the consistency pair, both of which the map had already settled and then
not used:

    "Snap Pitches to Scale Assistant Settings while editing"
      -> "Snap Pitch theo cai dat Scale Assistant khi dang sua"

Nine keys say `Tro ly Scale` - the feature name rendered the same way as
`Tro ly Proximity` - and this one alone kept the English.

    "... select your Note Expression Input Device"
      -> "... va chon thiet bi dau vao Note Expression cua ban"

"Note Expression Input Device" is a compound: the DEVICE is Note Expression,
"input" qualifies it. Round 39 set two keys to "thiet bi Note Expression dau
vao"; these two were not in that batch.

And "Chord Pads" in a sentence. Nineteen keys use "Chord Pad" with no plural -
correct, Vietnamese has no plural - but five sentences say "tai ca Chord Pad",
where the plural IS needed because "tat ca" already supplies it.

  python tools/fix_reading40.py
  python tools/fix_reading40.py --write
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
    # the warning about clipping, dropped
    # ==================================================================
    'The project contains files or crossfades in 32-bit float format. Since '
    'OMF does not support this format, the files will be converted and '
    'exported as embedded data. Please note that this conversion might lead '
    'to clipping!':
        'Project chứa các file hoặc Crossfade ở định dạng 32-bit float. Vì OMF '
        'không hỗ trợ định dạng này, các file sẽ được chuyển đổi và export dạng '
        'dữ liệu nhúng. Xin lưu ý rằng việc chuyển đổi này có thể làm âm '
        'thanh bị cắt!',
    'The plug-in could not be validated and has been moved to the blocklist. '
    'You can reactivate the plug-in, but please note that the operating '
    "system's protection may prevent the plug-in from loading. Please contact "
    'the manufacturer of the plug-in for an updated version.':
        'Plug-in không thể xác thực và đã được chuyển vào Blocklist. Bạn có thể '
        'kích hoạt lại, nhưng lưu ý cơ chế bảo vệ của hệ điều hành có thể ngăn '
        'Plug-in nạp. Vui lòng liên hệ nhà sản xuất Plug-in để có phiên bản '
        'mới hơn.',

    # ==================================================================
    # nine keys say "Tro ly Scale"; this one kept the English
    # ==================================================================
    'Snap Pitches to Scale Assistant Settings while editing':
        'Bắt Pitch theo cài đặt Trợ lý Scale khi đang sửa',

    # ==================================================================
    # "Note Expression Input Device" - the compound, twice. Round 39 set
    # two keys this way and these two were not in that batch.
    # ==================================================================
    'To have initial states sent, open the Input Routing menu and select your '
    'Note Expression Input Device':
        'Để gửi trạng thái ban đầu, hãy mở menu Input Routing và chọn thiết bị '
        'Note Expression đầu vào của bạn',
    'To play Note Expressions, open the Input Routing menu and select your '
    'Note Expression Input Device':
        'Để phát Note Expression, hãy mở menu Input Routing và chọn thiết bị '
        'Note Expression đầu vào của bạn',

    # ==================================================================
    # Vietnamese has no plural, but "tat ca" needs the particle
    # ==================================================================
    'Select controller to set tensions for all chord pads':
        'Chọn Controller để đặt Tension cho tất cả các Chord Pad',
    'Select controller to set voicings for all chord pads':
        'Chọn Controller để đặt Voicing cho tất cả các Chord Pad',
    'Select controller to transpose all chord pads':
        'Chọn Controller để Transpose tất cả các Chord Pad',
    'To use Chord Pads activate "Monitor" of tracks where Input Routing is '
    'set to Chord Pads':
        'Để dùng các Chord Pad, hãy bật "Monitor" của các Track có Input '
        'Routing đặt thành Chord Pads',
    'To use Chord Pads activate "Record Enable" or "Monitor" of tracks where '
    'Input Routing is set to Chord Pads':
        'Để dùng các Chord Pad, hãy bật "Record Enable" hoặc "Monitor" của các '
        'Track có Input Routing đặt thành Chord Pads',

    # ==================================================================
    # a button label is a proper noun and stays English
    # ==================================================================
    'To save the project as is, click \'Save\'. Note that the project will no '
    'longer be compatible with program versions older than 13.0.30.':
        "Để lưu Project như hiện tại, nhấp 'Save'. Lưu ý rằng Project sẽ không "
        'còn tương thích với các phiên bản chương trình cũ hơn 13.0.30.',
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
