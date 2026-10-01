#!/usr/bin/env python3
"""Round 35 of reading: the last of the long values in `general`.

Slice 450, which finishes the catch-all. Twenty-nine labels left in this
domain after this round: every short label and every long sentence has now
been read by hand at least once.

Three fixes, and one of them is a rule the glossary already had:

    "'Return to Start Position on Stop' has been deactivated"
      -> "'Quay ve vi tri bat dau khi dung' da bi huy kich hoat"

`Huy` is CANCEL, and AGENT.md settled in round 24 that Deactivate is not Hủy -
a deactivated switch is off, not a cancelled dialog. It is the only remaining
`huy kich hoat` in the map; the six other `bi huy` are genuine cancels
("Action is canceled", "the function had to be canceled") and stay.

    "You have modified the timecode offset."
      -> "Ban da sua doi Offset Timecode."

Round 32 turned "Negative project start offset" into "do lech bat dau Project".
Here the offset was left in English next to a word that IS a Cubase term
(Timecode), so the sentence read half and half.

    "Warn if real time mixdown is required in order to include external
     plug-in."
      -> "... de gop Plug-in ben ngoai."

External, the round 33 find, once more - this time in the one sentence that
still had it.

  python tools/fix_reading35.py
  python tools/fix_reading35.py --write
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
    "\\'Return to Start Position on Stop\\' has been deactivated":
        "'Quay về vị trí bắt đầu khi dừng' đã bị tắt",
    'You have modified the timecode offset. Do you want keep the project '
    'content at its timecode positions?':
        'Bạn đã sửa đổi độ lệch Timecode. Bạn có muốn giữ nội dung Project tại '
        'vị trí Timecode không?',
    'Warn if real time mixdown is required in order to include external '
    'plug-in.':
        'Cảnh báo nếu cần Mixdown thời gian thực để gộp Plug-in External.',
    'Video service does not respond. Waiting for video service...':
        'Dịch vụ Video không phản hồi. Đang chờ dịch vụ Video...',
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
