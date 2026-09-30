#!/usr/bin/env python3
"""Round 53: the glossary table checked mechanically, and a detector bug that
had been hiding half the map from every check I wrote.

THE DETECTOR BUG. Nine tools tested for a Vietnamese letter with

    HAN = re.compile(r'[A-ỿ]')

which is U+0100 to U+1EF9. Vietnamese keeps most of its common letters - a,
a, e, e, o, o, u, u, d and their tone marks - in U+00C0 to U+00FF, which is
BELOW the start of that range. So a value written entirely with those letters

    "Thêm bè"

tested as NOT Vietnamese, and every one of those nine tools was looking at a
subset of the map. It surfaced because a value that should have been reported
was not: "Select which notes are used for 'Randomize', 'Create Variation' and
'Add Voice'" quotes 'Add Voice' in English while the label says "Thêm bè", and
the tool had been reporting zero mismatches for four rounds.

That is the second detector bug in this project and the more embarrassing one,
because the first - the truncated key - at least had an honest comment. Both
were invisible: a detector that under-reports looks exactly like a detector
that has nothing to report, and rounds 36 to 52 all read "0" or "all correct"
as good news.

All nine now spell the class with escapes, and re-running everything against
the corrected class found four more quoted-name mismatches at once.

WHAT THE GLOSSARY AUDIT FOUND. The other new tool parses AGENT.md section 4
and checks every row against the whole map:

  tools/audit_glossary.py

Section 4 is the one artefact here that cannot go stale by accident, and it has
been wrong twice - "Key Signature | hoa bieu" in round 22, which spread into
eight strings, and the correct row "Chord Symbols | hoa bieu" in round 39,
which seven keys had drifted away from. So it is worth checking rather than
re-reading.

Two real rows, both in the same shape as the Chord Symbols one: the table
settled the term, the table was right, and a handful of keys were written
afterwards without looking at it.

    "Add Key Signature"            -> "Them Key Signature"
    "Add Displayed Key Signature"  -> "Them Key Signature hien thi"
    "Key Signatures"               -> "Key Signature"
    "Show Key Signatures"          -> "Hien Key Signature"

Sixteen keys say `so chi nhp`; four kept the English, in the same notation
menu, three of them within two hundred keys of each other. The `Key Signatures`
label also lost its plural, so the menu shows a singular where the English
shows a plural.

    "Maximum Number of Rhythm Dots Allowed in Compound Beats"
      -> "So dau cham nhip toi da duoc phep trong nhip phuc"
    "Maximum Number of Rhythm Dots Allowed in Simple Beats"
      -> "So dau cham nhip toi da duoc phep trong nhip don"

Round 30b set "Rhythm Dot" to "dau cham doi" and caught three of five. The two
that say "dau cham nhip" are the remaining pair - "dot" read as "beat", which is
the notation sense of the same word.

And "externally clocked", which round 33 fixed four External strings and left
this one, the same shape as the round 49 Word Clock find:

    "(externally clocked)" -> "(lay xung ngoai)"

The label is "Externally Clocked" and stays English - a clock mode is named by
what it is called - so the parenthetical has to say the same.

  python tools/fix_reading53.py
  python tools/fix_reading53.py --write
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
    # the table settled it in round 22, the table is right, and four
    # keys were written afterwards without looking at it
    # ==================================================================
    'Add Displayed Key Signature': 'Thêm số chỉ nhịp hiển thị',
    'Add Key Signature': 'Thêm số chỉ nhịp',
    'Key Signatures': 'Số chỉ nhịp',
    'Show Key Signatures': 'Hiện số chỉ nhịp',

    # ==================================================================
    # "dot" read as "beat" - the notation sense of the same word
    # ==================================================================
    'Maximum Number of Rhythm Dots Allowed in Compound Beats':
        'Số dấu chấm dôi tối đa được phép trong nhịp phức',
    'Maximum Number of Rhythm Dots Allowed in Simple Beats':
        'Số dấu chấm dôi tối đa được phép trong nhịp đơn',

    # ==================================================================
    # External, the seventh time, in the same shape as round 49's
    # Word Clock
    # ==================================================================
    '(externally clocked)': '(Externally Clocked)',
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
