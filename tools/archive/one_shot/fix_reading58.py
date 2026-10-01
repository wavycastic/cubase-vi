#!/usr/bin/env python3
"""Round 58: the one word that was a hybrid inside a single label.

    "Bars+Beats"   ->  "Bar+Nhịp"

Read that as a Cubase time-scale position and there is nothing wrong with
either half. Read it as a LABEL and it is a hybrid of two languages in four
characters, in a value whose own two components are not treated alike:

    "Bars"   ->  "Bar"        English
    "Beats"  ->  "Nhịp"       Vietnamese
    "Ticks"  ->  "Tick"       English

`Bar`, `Beat` and `Tick` are the three units Cubase's position field prints,
and two of the three are already English. The third was left over from when
the notation prose said "phách", and round 57 removed that - which left this
exposed rather than causing it. So "Beats" becomes "Beat" and the nine
compounds follow.

This is a different decision from round 57's, and both are right:

    prose and notation, a beat dividing a bar   ->  nhịp
    the unit Cubase prints in a position field  ->  Beat

`Tick` is already `Tick` and `Bar` is already `Bar`, so this also removes the
last English term in the position family that had been translated.

And the Count-In family, which is the same shape one level up. Four values say
`Count-In` - it is what the Transport panel calls it, and it is a feature
name - and three say `đếm nhịp`:

    "Click during Count-In"        ->  "Nhấp trong lúc đếm nhịp"
    "Number of Bars in Count-In"   ->  "Số Bar trong phần đếm nhịp"
    "Use Bars & Beats Count-In"    ->  "Dùng đếm nhịp theo Bar & Nhịp"

`đếm nhịp` is not wrong, it is just a second name for a thing Cubase already
names, and the reader then has to work out which of the two is the panel
button. The majority is the term, so the majority is what the three get.

One from the same read, which round 55 made right without noticing:

    "Choose Time Signature for Count-In :" -> "Chọn số chỉ nhịp cho Count-In :"

`số chỉ nhịp` there is the TIME SIGNATURE, not the key signature, and the
space in front of the colon is the source's own.

  python tools/fix_reading58.py
  python tools/fix_reading58.py --write
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
    # the position units Cubase prints: Bar, Beat, Tick - all English
    # ==================================================================
    'Beat': 'Beat',
    'Beats': 'Beat',

    # ==================================================================
    # the Count-In family: the term four times, a second name three times
    # ==================================================================
    'Click during Count-In': 'Nhấp trong lúc Count-In',
    'Number of Bars in Count-In': 'Số Bar trong Count-In',
    'Use Bars & Beats Count-In': 'Dùng Count-In theo Bar & Beat',
}

# the compounds that mixed the two languages in one label. A hand-written
# entry above wins, because "Use Bars & Beats Count-In" needs BOTH halves
# changed and the substitution only knows about one of them.
for k, v in vi.items():
    if k in WORDING or 'Nhịp' not in v or 'Bar' not in v:
        continue
    WORDING[k] = v.replace('Nhịp', 'Beat')

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
    print(f'  {k[:60]!r}')
    print(f'      {vi.get(k, "")[:92]!r}')
    print(f'   -> {v[:92]!r}')

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
