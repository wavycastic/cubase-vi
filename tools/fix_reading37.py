#!/usr/bin/env python3
"""Round 37: the rest of the "English frame" list, 142 hits down to 110.

Round 36 built the detector and fixed 48. This round reads the remaining 110
and finds four more kinds, all of them small and all of them the same
underlying failure - a string marked done without being read.

PURE ENGLISH, "The" DROPPED. Two keys lost the definite article and stopped
being Vietnamese at all:

    "The application was terminated unexpectedly"
      -> "application was terminated unexpectedly"
    "The search returned no results"
      -> "search returned no results"

audit_quality's "fully untranslated prose" test reported zero, because both
values still count as translated in the coverage sense - the key is present,
the value is filled. The test asks "is there Vietnamese", and "a" and "the"
are the entire difference.

REVERSED, in a family of "verb + noun" labels that all came out backwards:

    "Locate Clip Package File"        -> "File Locate Clip Package"
    "Reading OpenTL Project File..."  -> "File Reading OpenTL Project"
    "Removing old audio stream from video file"
                                      -> "Removing old audio stream tu video file"
    "Send Data via System Link"       -> "Gui Data via System Link"
    "Tempo Track Editor - %s"         -> "Editor Tempo Track - %s"

Six of them. The detector found them because "File", "Locate", "Clip",
"Package" all appear in the source, in that order somewhere - and a label
whose words are the right words in the wrong order still trips the frame
test. Which is a feature: the frame test is not a "did you translate it" test,
it is a "did you look at it" test.

    "Event End/Range End to Cursor"   -> "Event End/Range End toi Cursor"
    "Input Group and Channel"         -> "Input Group and Channel"

One word missing: "to" in the first, and no Vietnamese at all in the second,
where "and" is still English while its four siblings in the same panel say
"Và".

  python tools/fix_reading37.py
  python tools/fix_reading37.py --write
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
    # pure English - "The" dropped
    # ==================================================================
    'The application was terminated unexpectedly':
        'Ứng dụng đã kết thúc đột ngột',
    'The search returned no results': 'Tìm kiếm không trả về kết quả nào',
    'There are no events in the buffer': 'Không có Event nào trong buffer',
    'Use Selected ASIO Ports for Data only':
        'Chỉ dùng ASIO Port đã chọn cho Data',

    # ==================================================================
    # reversed "verb + noun" labels
    # ==================================================================
    'Locate Clip Package File': 'Định vị File Clip Package',
    'Reading OpenTL Project File...': 'Đang đọc File Project OpenTL...',
    'Removing old audio stream from video file':
        'Đang xóa audio stream cũ khỏi file Video',
    'Render New Video File': 'Render File Video mới',
    'Tempo Track Editor - %s': 'Editor Track tempo - %s',
    'MIDI Remote Script Console': 'Script Console MIDI Remote',
    'Process Project Logical Editor': 'Logical Editor của Project',
    'RF64 Broadcast Wave File': 'File Broadcast Wave RF64',

    # ==================================================================
    # English "and" left in a family that says "Và"
    # ==================================================================
    'Input Group and Channel': 'Input Group và Channel',
    'Output Group and Channel': 'Output Group và Channel',

    # ==================================================================
    # one word missing, or an English preposition left
    # ==================================================================
    'Event End/Range End to Cursor': 'Đưa Event End/Range End tới Cursor',
    'Event Start/Range Start to Cursor':
        'Đưa Event Start/Range Start tới Cursor',
    'Send Data via System Link': 'Gửi Data qua System Link',
    "Use project's Clip Packages folder":
        "Dùng thư mục Clip Packages của project",
    'Yamaha XF Version ID': 'ID phiên bản Yamaha XF',

    # ==================================================================
    # "Toggle X Mode" left as "Toggle X"
    # ==================================================================
    'VariAudio - Toggle Pitch Snap Mode':
        'VariAudio - Bật/tắt chế độ Pitch Snap',
    'VariAudio - Toggle Smart Control Mode':
        'VariAudio - Bật/tắt chế độ Smart Control',

    # ==================================================================
    # "[ALT + nhap" - the word the map gets right forty times elsewhere
    # ==================================================================
    'Select Primary Time Format\\nUse [ALT + click] swap Primary & Secondary '
    'Time Formats':
        'Chọn Primary Time Format\\nDùng [ALT + nhấp chuột] để hoán đổi '
        'Primary & Secondary Time Format',
    'Select Secondary Time Format\\nUse [ALT + click] swap Primary & '
    'Secondary Time Formats':
        'Chọn Secondary Time Format\\nDùng [ALT + nhấp chuột] để hoán đổi '
        'Primary & Secondary Time Format',
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
