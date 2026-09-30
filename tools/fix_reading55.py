#!/usr/bin/env python3
"""Round 55: two menu items with the same text, and the glossary row that
allowed it.

    "Add Key Signature"      -> "Them so chi nhip"
    "Add Time Signature"     -> "Them so chi nhip"

    "Add Displayed Key Signature"  -> "Them so chi nhip hien thi"
    "Add Displayed Time Signature" -> "Them so chi nhip hien thi"

    "Key Signatures"         -> "So chi nhip"
    "Time Signature"         -> "So chi nhip"
    "Time Signatures"        -> "So chi nhip"

    "Cautionary Key Signature at End of System"
                               -> "So chi nhip nhac lai tai cuoi dong nhac"
    "Cautionary Time Signature at End of System"
                               -> "So chi nhip nhac lai tai cuoi dong nhac"

Five pairs. The user cannot tell the two menu items apart, opens the wrong one,
and nothing anywhere says why.

NO CHECK IN THIS PROJECT COULD SEE IT, and the reason is structural: every
check works on one value at a time. Two individually perfect values pass. So
the new tool compares values ACROSS keys:

    tools/find_duplicate_values.py

It reports 172 collisions, most of them legitimate - Cubase really does render
"Bypass", "Discard", "Ignore" and "Skip" identically, and half the list is a
singular and a plural of the same word. The pairs to look at are the ones whose
KEYS are not themselves the same words, and the Key Signature cluster is the
only one where a menu is broken.

THE CAUSE IS IN THE TABLE. AGENT.md section 4 gives both terms the same
Vietnamese, because some Vietnamese sources use "so chi nhip" for both. That is
defensible in a sentence and useless in a menu, and it is the same shape as the
two table errors this project has already had: round 22's "Key Signature | hoa
bieu", and the correct "Chord Symbols | hoa bieu" that seven keys had drifted
away from. This is a third kind - a table row that cannot be right, because the
menu needs the two apart and the table gives them one name.

So:

    Key Signature    ->  hóa âm
    Time Signature   ->  số chỉ nhịp

`Hoa am` is the established Vietnamese music term for a key signature - "hoa am
Sol", "hoa am thu". It is one letter away in shape from `hoa bieu`, which is the
CHORD SYMBOLS, and the two objects do look alike on the page: a row of glyphs at
the start of a staff, one of accidentals and one of chord names. That is a
documentation problem rather than a translation problem, and it is written down
in section 4 so the next person does not have to rediscover it.

The thirteen keys are rewritten by substituting the term rather than by hand,
because every one of them says "so chi nhip" for Key Signature and none of them
mentions a Time Signature - so the substitution cannot touch the wrong one.

And three from reading the notation labels:

    "Notation of Short-Dotted Long Patterns" -> "Notation của Pattern ngan..."
    "Notation of Short-Long-Short Patterns"  -> "Notation của Pattern ngan..."

Round 38 set "Notation of Short-Long-Short Patterns That Cross the Half-Bar" to
"Ky am", on the grounds that here Notation is the ordinary English word. These
two are the same word and had been missed. The FEATURE "Notation" stays
English - "Notation Settings", "Notation only", "For Notation" - and the two
senses of one English word in one panel is the "String" mistake from round 29.

    "Every System" -> "Mỗi dòng"

Truncated. System is "dòng nhạc" in forty-odd keys.

  python tools/fix_reading55.py
  python tools/fix_reading55.py --write
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
    # "Notation" the ordinary English word, against the FEATURE
    # "Notation" which stays English
    # ==================================================================
    'Notation of Short-Dotted Long Patterns':
        'Ký âm các Pattern ngắn-có chấm-dài',
    'Notation of Short-Long-Short Patterns':
        'Ký âm các Pattern ngắn-dài-ngắn',
    'Every System': 'Mỗi dòng nhạc',
    'Below Timecode Staff': 'Phía dưới khuông nhạc Timecode',
}

# Key Signature: thirteen keys, all of which say "so chi nhip" for it and none
# of which mentions a Time Signature, so the term can be substituted rather than
# retyped. This is what un-collides the five menu pairs.
for k, v in vi.items():
    # the phrase appears lower-cased in two of the Accidentals tooltips, which
    # round 39 had set to "so chi nhip" when that was still the right answer
    if 'key signature' not in k.lower() or 'time signature' in k.lower():
        continue
    new = v.replace('Số chỉ nhịp', 'Hóa âm').replace('số chỉ nhịp', 'hóa âm')
    if new != v:
        WORDING[k] = new

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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:76]!r}\n   -> {v[:76]!r}')

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
