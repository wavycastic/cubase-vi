"""Round 66: the "[RM]" marker was in the text, and it would have been drawn on
screen.

    "Keep History"      ->  "Giu Lich su"
    "Keep History[RM]"  ->  "Giu Lich su[RM]"          <- "[RM]" is drawn

Cubase's extractor makes a second copy of a label for its read-mode display and
names it "X[RM]". Those are two separate <String> entries with the SAME English,
and the marker exists only in the Key attribute. What settled it is not an
argument, it is the original file: all EIGHT vendors translate the pair
identically and none of them puts the marker in the value.

    Keep History         de "Verlauf speichern"   fr "Garder historique"
    Keep History[RM]     de "Verlauf speichern"   fr "Garder historique"

    New Parts            de "Neue Parts"          fr "Nouveaux conteneurs"
    New Parts[RM]        de "Neue Parts"          fr "Nouveaux conteneurs"

    Stacked              ru "Nakoplenie dublei"
    Stacked[RM]          ru "S nakopleniem"

Eleven of the fifteen [RM] values carried the marker, which means the string
"[RM]" was going to appear on screen next to eleven labels in read mode. Nothing
in this project could see it: the marker is legal text, and the value it is
sitting in is otherwise a perfectly good translation.

So there is now a fifth hard rule in check_style.py, and it is the only one of
the five that is not a matter of style:

    Rule 5: no value may contain "[RM]"

Two more from the same detector, which groups keys that differ only in case or
in a run of whitespace - "Cues (Post-Fader)" against "Cues  (Post-Fader)" was
its first find in round 65:

    "files"   ->  "File"        "Files"   ->  "Cac File"
    "samples" ->  "Sample"      "Samples" ->  "Cac Sample"

Two keys each, the same word, the plural rendered with the article in one and
without it in the other. "Cac File" is what the family already does - "Cac File
da sao chep", "Cac Sampler Channel", "Cac Sampler Track" - and Vietnamese
category names are not the place to be reading a sentence.

And "New Parts[RM]" was not just carrying the marker, it was a DIFFERENT
reading of the same English: "Tao Parts" where its twin said "Part moi". Once the
marker is gone the two have to agree, and the faithful rendering of the label
"New Parts" is "Part moi".

  python tools/fix_reading66.py
  python tools/fix_reading66.py --write
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
MARK = '[RM]'

# The rule, applied to every key rather than to the four this round found, so
# that the seven that already matched their base stay matched and the four that
# did not get fixed whether or not anyone listed them.
WORDING = {}
for k, v in vi.items():
    if not k.endswith(MARK):
        continue
    base = k[:-len(MARK)]
    if base in vi:
        # every vendor gives the pair the same text, marker or no marker
        WORDING[k] = vi[base]
    else:
        # no base key in the map: the marker has nothing to copy, so it goes
        new = v.replace(MARK, '').rstrip()
        if new:
            WORDING[k] = new

WORDING['files'] = 'Các File'
WORDING['samples'] = 'Các Sample'

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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v[:70]!r}')

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
