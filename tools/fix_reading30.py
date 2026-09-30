#!/usr/bin/env python3
"""Round 30: Key Signature was wrong in the rule table, not in the map.

Round 29 finished the R block. Before moving on, one thing in it needed
checking, and it turned out to be the worst find of the project.

AGENT.md section 4 has a table of score-editor terms. One row read:

    | Key Signature | hoa bieu |
    | Time Signature | so chi nhip |

That row is wrong. Key Signature - the key signature, the sharps and flats -
is "so chi nhip" in Vietnamese music notation, the same word as Time Signature.
"Hoa bieu" is Chord Symbols: the chord name written beside a note, Cm7 and
friends.

The translation had followed the table faithfully, so the error had propagated
into EIGHT strings, several of them long sentences that had passed through six
reading rounds without being questioned:

    "Notes Following a Change of Key Signature That Shows Cancellation Naturals"
      -> "Cac not sau khi doi hoa bieu co hien dau binh huy bo"
    "Key Signatures at Start of System Following First System"
      -> "Hoa bieu o dau cac dong nhac sau dong nhac dau tien"
    "Position Bar Numbers at Start of System After Clef and Key Signature"
      -> "Dat so Bar o dau dong nhac sau khoa nhac va hoa bieu"
    "In some hand-copied lead sheets, the key signature is shown only at ..."
      -> "... hoi bang to hop chep tay, hoa bieu chi hien o dau Bar dau tien ..."

The part that should sting: rounds 22 and 23 DID find this same error, in
"SMF: Key signature" and "Sign.", fixed both, and wrote the finding into
AGENT.md - without reopening the table to see where it came from. The map was
right; the rule was wrong. Every fix applied from that table was correct
*according to the table*.

A wrong term table produces no error of its own. It produces correct work, and
the error is invisible until somebody checks the table against the outside
world rather than against the translation it produced.

So: when a terminology error turns up, fix the map AND the table row, then grep
the whole map for the wrong word. Here that was "hoa bieu" - nine hits, one of
them "Dau hoa" (Accidental), which is correct and had to be left alone. Which
is the other half of the lesson: the grep finds the places to look, and someone
still has to decide which of them are wrong.

  python tools/fix_reading30.py
  python tools/fix_reading30.py --write
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
    # Key Signature is the key signature. Every one of these said "hoa bieu",
    # which is Chord Symbols, because the AGENT.md table said so.
    'Cautionary Key Signature at End of System':
        'Số chỉ nhịp nhắc lại tại cuối dòng nhạc',
    'Key Signatures at Start of System Following First System':
        'Số chỉ nhịp ở đầu các dòng nhạc sau dòng nhạc đầu tiên',
    'Notes Following a Change of Key Signature That Shows Cancellation Naturals':
        'Các nốt sau khi đổi số chỉ nhịp có hiện dấu bình hủy bỏ',
    'Notes Following a Change of Key Signature in the Middle of a Bar':
        'Các nốt sau khi đổi số chỉ nhịp ở giữa Bar',
    'Notes in the Bar Following a Change of Key Signature':
        'Các nốt trong Bar sau khi đổi số chỉ nhịp',
    'Position Bar Numbers at Start of System After Clef and Key Signature':
        'Đặt số Bar ở đầu dòng nhạc sau khóa nhạc và số chỉ nhịp',
    "In some hand-copied lead sheets, the key signature is shown only at the "
    "beginning of the first bar, and it is hidden on subsequent systems. To "
    "follow this convention, choose 'Hide Key Signatures'.":
        'Trong một số bản tổng phổ chép tay, số chỉ nhịp chỉ hiện ở đầu Bar '
        'đầu tiên và ẩn ở các dòng nhạc tiếp theo. Để theo quy ước này, hãy '
        "chọn 'Ẩn số chỉ nhịp'.",
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
