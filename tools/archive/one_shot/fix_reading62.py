"""Round 62: "Next" read as the wrong half of its own phrase.

    "Subfolder Next to Exported File"  ->  "Subfolder Next vào File Exported"

Twenty-five siblings read "Next X" as "X ke tiep" - the NEXT one. This one reads
it as "Next INTO", and the giveaway is that it is the ONLY value in the map that
begins with the English word "Next" and continues in Vietnamese:

    "Subfolder Next vào File Exported"

"Next" is a standalone label here - "Next[Key]" is "Phim Next" - so keeping the
word is not the error. The error is the VERB that follows it. "Next to" is
BESIDE, and in the MediaBay preferences it means the subfolder sits alongside
the exported file:

    "Subfolder bên cạnh File Exported"

This is the eleventh "read one word as another word" defect in this project, and
it is the same mechanism as the previous ten, which is worth stating once:

    an English word standing NEXT TO another English word in the source table
    gets read as the neighbour

The word that was read wrong is always the one whose own label exists elsewhere
in the map. "Next" has twenty-five keys that say "ke tiep", so "Next to" was
read as "Next" plus something, and "to" was rendered as "vao" - INTO - which is
what you get by translating each half of a two-word phrase in isolation.

The fix is to read the phrase, not the word.

The two other finds from the same detector are compounds and are correct:
"Bao gom thu muc va thu muc con" contains "thu muc" inside "thu muc con", and
"Ten Track va ten Track Version" does the same. The detector reports them
because it counts a phrase inside a longer phrase, which is the price of a
mechanical test; both are one line to dismiss, and both are correct Vietnamese.

  python tools/fix_reading62.py
  python tools/fix_reading62.py --write
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
    # "Next to" is BESIDE. "vao" is INTO, which is what you get by translating
    # each half of a two-word phrase on its own.
    'Subfolder Next to Exported File': 'Subfolder bên cạnh File Exported',
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
    print(f'  {k!r}\n      {vi.get(k, "")!r}\n   -> {v!r}')

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
