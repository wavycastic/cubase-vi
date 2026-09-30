#!/usr/bin/env python3
"""Round 47: the rest of the mixer domain, long values 55-105.

`Remote-Control Focus` is the feature name and six keys agree on that:

    "Set Remote-Control Focus for VST Quick Controls"
      -> "Dat Remote-Control Focus cho VST Quick Control"
    "Remote-Control Focus for VST Quick Controls follows track selection"
      -> "Remote-Control Focus cho VST Quick Control bam theo lua chon Track"

and four translated it, in two of the same family:

    "Set Remote-Control Focus for VST Quick Controls to Next Instrument"
      -> "Dat tieu dem dieu khien tu xa cho VST Quick Control toi Instrument
         ke tiep"
    "Set Remote-Control Focus on Next Plug-in"
      -> "Dat tieu dem dieu khien tu xa o Plug-in ke tiep"

"Tieu dem dieu khien tu xa" is a translation of the name, and a name is what the
user reads in the menu. Same shape as "Pan truc Z" for 'Z-Axis Pan' last round.

`Post-Fader` lowercase, in the one key of the pair where it should be capitalised
- its eleven siblings all write it with a capital P, and the sibling that
describes the same move the other way says "vi tri Pre-Fader".

And a pair of sentences that repeat a noun three times:

    "The connection could not be created, as the destination is not part of the
     channel. Make sure to assign a destination that is part of the channel."
      -> "Khong the tao ket noi vi dich khong phai la mot phan cua Channel. Hay
         dam bao gan dich la mot phan cua Channel."

"mot phan cua" three times in two sentences. Vietnamese says "thuoc" for
belonging to: "vi dich khong thuoc Channel nay".

And "Your project may sound differently", which round 32 rendered as "Am thanh
cua Project co the se khac" in one key and "Project cua ban co the nghe khac
di" in this one - the same sentence, a hundred keys apart, two answers. The
first is right: it is the sound that changes, not the project.

And the "[ALT] + nhap" family, one more, in a key whose truncated form hid the
sibling that round 46 had already fixed.

  python tools/fix_reading47.py
  python tools/fix_reading47.py --write
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
    # a feature name, not a description of it
    # ==================================================================
    'Set Remote-Control Focus for VST Quick Controls to Next Instrument':
        'Đặt Remote-Control Focus cho VST Quick Control tới Instrument kế tiếp',
    'Set Remote-Control Focus for VST Quick Controls to Previous Instrument':
        'Đặt Remote-Control Focus cho VST Quick Control tới Instrument liền '
        'trước',
    'Set Remote-Control Focus on Next Plug-in':
        'Đặt Remote-Control Focus cho Plug-in kế tiếp',
    'Set Remote-Control Focus on Previous Plug-in':
        'Đặt Remote-Control Focus cho Plug-in trước đó',

    # ==================================================================
    # Post-Fader with a capital, as its eleven siblings write it
    # ==================================================================
    'Pre-Fader Send.\\nClick to move to post-fader position.':
        'Send Pre-Fader.\\nNhấp để chuyển tới vị trí Post-Fader.',

    # ==================================================================
    # "mot phan cua" three times in two sentences
    # ==================================================================
    'The connection could not be created, as the destination is not part of the '
    'channel. Make sure to assign a destination that is part of the channel.':
        'Không thể tạo kết nối vì đích không thuộc Channel này. Hãy đảm bảo gán '
        'một đích thuộc Channel này.',
    'The destination parameter could not be selected, as the destination is '
    'not part of the channel. Make sure to assign a destination that is part '
    'of the channel.':
        'Không thể chọn tham số đích vì đích không thuộc Channel này. Hãy đảm '
        'bảo gán một đích thuộc Channel này.',

    # ==================================================================
    # one sentence, two answers, a hundred keys apart - round 32 had it
    # ==================================================================
    'The channel panner MixConvert has automatically been replaced by '
    'MixConvert V6 for Channel "%s". Your project may sound differently.':
        'Channel panner MixConvert đã được tự động thay bằng MixConvert V6 cho '
        'Channel "%s". Âm thanh của Project có thể sẽ khác.',

    # ==================================================================
    # small
    # ==================================================================
    'Set Channel Visibility Agents\\nUse [ALT]-Click to Reset Channel '
    'Visibility Agents':
        'Đặt Channel Visibility Agent\\nDùng [ALT] + nhấp chuột để đặt lại '
        'Channel Visibility Agent',
    'VST System Link has been deactivated because of too many receive errors!':
        'VST System Link đã bị tắt vì có quá nhiều lỗi nhận!',
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
