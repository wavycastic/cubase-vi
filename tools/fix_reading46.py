#!/usr/bin/env python3
"""Round 46: the mixer domain, long values 0-55.

`Retrospective Record` is split seven seven.

    "MIDI Retrospective Recording"              -> "Ghi am MIDI hoi cuu"
    "Retrospective Recording"                   -> "Ghi am hoi cuu"
    "MIDI Retrospective Record: Empty All Buffers"
                                                -> "Ghi hoi to MIDI: Xoa tat ca Buffer"
    "Retrospective Record: Chords"              -> "Ghi hoi to MIDI: Hop am"

`Hoi cuu` is RECOVERY - the black box in an aircraft, video playback. `Hoi to` is
RETROACTIVE - retroactive pay, retroactive medicine. "Retrospective Record"
records what you have just played, and the feature's own name in the panel is
Retrospective Record, so the word has to survive in the translation. Fourteen
keys, two renderings, neither half wrong on its own.

Third time this month that a single feature has been rendered two ways -
`Material` in round 43, `audio stream` in round 41 - and the reason is always
the same: nobody compared the new key against the seven that were already
there. That is why the fix is a grep on the WORD.

`Z-Axis Pan` is the reverse problem: a QUOTED FEATURE NAME, translated in two
keys and left English in three.

    "Converting automation data may invalidate existing 'Z-Axis Pan' automation."
      -> "... lam mat hieu luc Automation 'Pan truc Z' hien co."
    "This profile requires '3-Layer 3D Pan Mode'. ... otherwise 'Z-Axis Pan'
     automation will be wrong."
      -> "... 'Z-Axis Pan' se sai."

Round 32 established the rule: a quoted feature name is not untranslated text.
It is a proper noun, and it has to match what the panel says. Both go back to
'Z-Axis Pan', and '3D Pan Mode' with them.

And the "[ALT + nhap" family again - four tooltips of the shape

    "Bypass Insert on/off.\\nInsert on/off with [ALT + click]."
      -> "Bat/tat Bypass Insert.\\nBat/tat Insert bang [ALT + nhap]."

where the map says "con lan chuot" and "nhap chuot" correctly in fifty other
keys. Round 33 fixed six, round 34 six more; these are the rest.

  python tools/fix_reading46.py
  python tools/fix_reading46.py --write
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
    # "Hoi cuu" is recovery, "hoi to" is retroactive. Fourteen keys, one
    # feature, two renderings.
    # ==================================================================
    'MIDI Retrospective Recording': 'Ghi hồi tố MIDI',
    'Retrospective MIDI Recording': 'Ghi hồi tố MIDI',
    'Retrospective Recording': 'Ghi hồi tố',
    'Retrospective Cycle Recording is not supported in MIDI Editors':
        'Không hỗ trợ ghi hồi tố theo Cycle trong MIDI Editor',
    'Insert Retrospective Recording from All MIDI Inputs on Selected Track':
        'Chèn bản ghi hồi tố từ mọi MIDI đầu vào vào Track đã chọn',
    'Insert Retrospective Recording from Track Input in Editor':
        'Chèn bản ghi hồi tố từ đầu vào Track vào Editor',
    'MIDI Retrospective Record: Insert from All MIDI Inputs':
        'Ghi hồi tố MIDI: Chèn từ tất cả MIDI đầu vào',

    # ==================================================================
    # a quoted feature name is a proper noun and stays English
    # ==================================================================
    'Convert Z-Axis Pan Automation of Selected Tracks':
        'Chuyển đổi Automation Z-Axis Pan của các Track đã chọn',
    "Converting automation data may invalidate existing 'Z-Axis Pan' "
    'automation. Do you want to convert it anyway?':
        "Chuyển đổi dữ liệu Automation có thể làm mất hiệu lực Automation "
        "'Z-Axis Pan' hiện có. Bạn vẫn muốn chuyển đổi?",
    "Switching '3D Pan Mode' may invalidate existing 'Z-Axis Pan' automation. "
    "Please check your automation tracks and use the 'Convert Z-Axis Pan "
    "Automation of Selected Tracks' function if needed.":
        "Chuyển '3D Pan Mode' có thể làm mất hiệu lực Automation 'Z-Axis Pan' "
        "hiện có. Vui lòng kiểm tra các Automation Track và dùng chức năng "
        "'Chuyển đổi Automation Z-Axis Pan của các Track đã chọn' nếu cần.",

    # ==================================================================
    # "[ALT + nhap" for click - rounds 33 and 34 fixed twelve of these
    # ==================================================================
    'Bypass Insert on/off.\\nInsert on/off with [ALT + click].':
        'Bật/tắt Bypass Insert.\\nBật/tắt Insert bằng [ALT + nhấp chuột].',
    'Channel Strip Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Channel Strip.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Direct Routing Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Direct Routing.\\nĐặt lại bằng [CTRL + nhấp chuột].',
    'Set Channel Type Filter\\nUse [CTRL + click] to Reset Channel Type '
    'Filter':
        'Đặt Channel Type Filter\\nDùng [CTRL + nhấp chuột] để đặt lại Channel '
        'Type Filter',

    # ==================================================================
    # small
    # ==================================================================
    'A Brickwall limiter will be used to comply to this Max. True Peak Level':
        'Một Brickwall Limiter sẽ được dùng để tuân theo mức True Peak tối đa '
        'này',
    'Include MIDI Channel (for pre-configured multi-timbral external '
    'instruments - such as Samplers)':
        'Bao gồm MIDI Channel (cho nhạc cụ External đa âm sắc cấu hình trước - '
        'như Sampler)',
    'Edit Channel Settings (Hold to edit VST instrument)':
        'Sửa cài đặt Channel (Giữ để sửa VST Instrument)',
    'Move Channel Strip to Post-Inserts Position':
        'Di chuyển Channel Strip vào vị trí Post-Inserts',
    'Move Channel Strip to Pre-Inserts Position':
        'Di chuyển Channel Strip vào vị trí Pre-Inserts',
    'Insert is not possible.\\nOrigin is before project start.':
        'Không thể chèn.\\nĐiểm gốc nằm trước đầu Project.',
    'Cannot load settings of a channel "%s" into a channel "%s": Channel Type '
    'Mismatch.':
        'Không thể tải cài đặt của Channel "%s" vào Channel "%s": loại Channel '
        'không khớp.',
    'More than one channel are selected!\\nAre you sure you want to reset the '
    'selected Channels?':
        'Đã chọn nhiều hơn một Channel!\\nBạn có chắc muốn đặt lại các Channel '
        'đã chọn không?',
}

# the eight "Jump to Marker N" keys, which all said "nhap" for click
WORDING.update({
    f'Jump to Marker {n}\\nUse [ALT + click] to set':
        f'Tới Marker {n}\\nDùng [ALT + nhấp chuột] để đặt'
    for n in range(1, 9)
})

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
