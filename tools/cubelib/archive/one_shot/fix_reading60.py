"""Round 60: four values where the label and the value swapped halves.

    "CC: Attack Time"       ->  "Thời gian CC: Attack"
    "CC: Portamento Control" ->  "Điều khiển CC: Portamento"
    "CC: Portamento Time"    ->  "Thời gian CC: Portamento"
    "CC: Release Time"       ->  "Thời gian CC: Release"

The Vietnamese word went to the FRONT, and the English prefix stayed exactly
where the English had it, so the name of the label ended up after the thing it
labels. The reader is told what time it is before they are told which control.

This is the "reordered English preposition" class that audit_quality has looked
for since early on, and it found nothing here - because that check wants a
preposition, and this is a whole noun phrase. Reordering is reordering; the
check was too narrow about what can be reordered.

The family shows the right shape, because nine siblings have it:

    "CC: Data Decrement"  ->  "CC: Giảm dữ liệu"
    "CC: Gen Purp 1"      ->  "CC: Mục đích chung 1"
    "CC: Portamento Time" ->  "Thời gian CC: Portamento"      <- the other way

Found by a new detector for the shape, and it is worth recording why the first
version of it was useless:

    tools/find_misplaced_prefix.py

Asked "where is a 'Word: ' prefix that is not at the front of a value", it
reported 126, and almost all of them were right:

    "Drum Editor: Bat tat hien do dai not"     a sentence with a colon in it
    "Chuyen tiep EQ/Filter: Quick"              a label inside a sentence
    "Khong the sua VariAudio: khong phat hien"  a SENTENCE colon

The test that is both necessary and sufficient is much narrower: the KEY has to
start with the same prefix, or there is nothing to complain about. Then it
reports 4, and all 4 are the same defect. A first cut that reports 126 teaches
you to ignore the tool; a first cut that reports 4 teaches you the shape.

  python tools/fix_reading60.py
  python tools/fix_reading60.py --write
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
    'CC: Attack Time': 'CC: Thời gian tấn công',
    'CC: Portamento Control': 'CC: Điều khiển Portamento',
    'CC: Portamento Time': 'CC: Thời gian Portamento',
    'CC: Release Time': 'CC: Thời gian Release',
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
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
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
