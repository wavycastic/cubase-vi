"""Round 63: a family split three ways, one member of it not translated at all.

    "Insert MIDI Retrospective Recording in Editor"
      ->  "Chen MIDI Retrospective Recording trong Editor"

Round 52 settled this term as "ghi hoi to" and rewrote sixteen keys, and that
was right - "retrospective" in Cubase is a RECORDING you retrieve afterwards, not
a survey, so "hoi cuu" is wrong and the glossary says so. But the family came
out of that round in three shapes:

    "Retrospective Record"        ->  "Ghi hoi to"
    "Retrospective Recording"     ->  "Ghi hoi to"
    "MIDI Retrospective Recording"->  "Ghi hoi to MIDI"
    "Insert Retrospective Recording"
                                   ->  "Chen ban ghi hoi to"      <- literal
    "Insert Retrospective Recording from Track Input in Editor"
                                   ->  "Chen ban ghi hoi to tu dau vao Track vao Editor"
    "Insert MIDI Retrospective Recording in Editor"
                                   ->  "Chen MIDI Retrospective Recording trong Editor"  <- not translated

Three renderings of one term, and the third of them is the English. That last
one is also the only value in the map where an English noun phrase sits in the
middle of a Vietnamese sentence with nothing around it - "trong Editor" is the
giveaway, because the sentence has a Vietnamese preposition on one side of the
phrase and an English one on the other.

"Retrospective Record: Chords" has the mirror problem: the key says no MIDI and
the value says MIDI, because round 52's substitution went through the bare term
inside it. The two siblings that DO say MIDI keep it, so this one loses it.

The word to unify on is "ghi hoi to" - the shorter one, and the one sixteen keys
already use. "Ban ghi hoi to" is a defensible literal rendering of "retrospective
recording", but it is a second name for the same feature, and the reader has no
way to know the sixteen keys and the three are the same thing.

  python tools/fix_reading63.py
  python tools/fix_reading63.py --write
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
    # the only value in the map with a Vietnamese preposition on one side of an
    # English noun phrase and nothing on the other
    'Insert MIDI Retrospective Recording in Editor':
        'Chèn ghi hồi tố MIDI vào Editor',

    # three keys naming a second thing by a second name
    'Insert Retrospective Recording': 'Chèn ghi hồi tố',
    'Insert Retrospective Recording from Track Input in Editor':
        'Chèn ghi hồi tố từ đầu vào Track vào Editor',
    'Insert Retrospective Recording from All MIDI Inputs on Selected Track':
        'Chèn ghi hồi tố từ mọi MIDI đầu vào vào Track đã chọn',

    # the key says no MIDI and the value said MIDI
    'Retrospective Record: Chords': 'Ghi hồi tố: Hợp âm',
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
    print(f'  {k[:62]!r}\n      {vi.get(k, "")[:82]!r}\n   -> {v[:82]!r}')

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
