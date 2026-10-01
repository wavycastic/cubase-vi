#!/usr/bin/env python3
"""Round 57: reading the notation labels by hand, and three words that are not
one word.

THE DECISIVE ONE. One value translates the same English word two ways in the
same sentence:

    "Notes That Subdivide Compound Beats, and Fill the Beat"
      -> "Cac not phan chia NHIP phuc va lap day PHACH"

So the map has three renderings of "beat": `phach` in twenty-one keys, `Beat`
in ten more, and `nhip` in eight. `Beats` is "Nhip" and `Beat` alone is "Phach",
and those two are four keys apart in the ruler family.

`nhip` is the standard Vietnamese term and `phach` is not - "phach" is the
ACCENTED PART of a beat, which is a real thing and not what Cubase's beat is.
Eight keys were already right, and the family that Cubase itself prints - the
time scale, the Beat Calculator, the Beat Track, the position fields - keeps
"Beat" as a term, which is a different decision and a correct one.

So `phach` becomes `nhip` in the twenty-one keys, and the two decisions stay
apart: prose and notation say "nhip", Cubase's own position and feature labels
say "Beat". That also removes the contradiction inside the one value.

    "Notes That Subdivide Compound Beats, and Fill the Beat"
      -> "Cac not phan chia nhip phuc va lap day nhip"

SECOND. Round 52 settled `Cycle` over `chu ky` and the metronome click is
another one of those, and it is holding: `Activate Metronome Click` -> "Bat
Click Metronome", `Audio Click Level` -> "Muc Click Audio", `Click Sounds` ->
"Am thanh cua Click", and thirty more. "Click" there is the SOUND, and
"Click[Mouse]" is the one that means a mouse - "Click chuot" - beside
"Click[Speaker]". Both right, and they are different words.

But six values have a mouse instruction outside the brackets, because the
source writes the modifier in brackets and the verb outside:

    "Assign Downmix Preset 1 (Reset All Presets with [Alt] + Click)"
      -> "... bang [Alt] + Click"
    "Next Chain Step\\nUse [ALT]-Click to jump to last chain step"
      -> "... dung [ALT]-Click de nhay toi..."

Round 54 replaced inside brackets only, so it could not reach these - which is
the right way round to have got it wrong, and the reason the class was only
nearly closed. The substitution is repeated here for the shape `[X]-Click` and
`[X] + Click`, and a key chord is still left in English so only the verb moves.

THIRD, and it is a joke:

    "Pick-up"      -> "Lay da"
    "Pick-up Bar of:" -> "Bar lay da cua:"

`Lay da` is TAKE THE CHEEK. The word is right - the English "pick up" means to
take over the current value, and that is the sense in "Pick-up Mode", which
the map has rendered correctly as "Che do Pick-up". So the two keys that
reached for a Vietnamese word reached for the wrong one, and the fix is to
leave the term alone, as its own third sibling already does.

And "Score Direction" and "Score Dynamic" were the only two values in the whole
map to say "Huong trong Score" and "Dong luc trong Score", where eight
siblings say `Dynamic` and the glossary has "Direction [musical performance
direction]" as "Chi dan dien tacu". A performance direction in a score is a
mark on the page, not a heading; "huong" is the sense of a stem.

  python tools/fix_reading57.py
  python tools/fix_reading57.py --write
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
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')

WORDING = {
    # ==================================================================
    # "lay da" is TAKE THE CHEEK. Its own third sibling keeps the term.
    # ==================================================================
    'Pick-up': 'Pick-up',
    'Pick-up Bar of:': 'Bar Pick-up của:',

    # ==================================================================
    # the two odd ones out in a family of eight
    # ==================================================================
    'Score Direction': 'Chỉ dẫn trong Score',
    'Score Dynamic': 'Dynamic trong Score',
    'Dynamic': 'Dynamic',
}

# --- "phach" is the accented PART of a beat, not the beat
for k, v in vi.items():
    if 'phách' not in v:
        continue
    new = v.replace('phách', 'nhịp').replace('Phách', 'Nhịp')
    if new != v:
        WORDING[k] = new

# --- a mouse verb outside the brackets: "[ALT]-Click", "[Alt] + Click".
# The key chord stays English, so only the verb moves, and the metronome click
# is untouched because it is never preceded by a chord.
OUTSIDE = re.compile(r'(\[[^\]]+\][\s]*[-+]?[\s]*)([Cc]lick)\b')
for k, v in vi.items():
    if not HAN.search(v):
        continue
    new = OUTSIDE.sub(r'\1nhấp chuột', v)
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
