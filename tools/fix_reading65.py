"""Round 65: the mixer domain, read by hand.

INSERT, THE NOUN AND THE VERB - the same shape as "String" in round 29 and
"Notation" in round 55:

    "Insert"   ->  "Chen"      the VERB, as a menu item
    "Inserts"  ->  "Inserts"   the noun
    "Insert Effect" -> "Hieu ung Insert"

Ninety-odd values use "Insert" as a noun - "Bat Insert", "Xoa Insert", "Sao chep
Insert", "Bypass Insert", "Enable Insert Slot by Number" - and a bare "Insert" in
the MixConsole is the section header, not a verb. So:

    "Insert"  ->  "Insert"

The verb keeps "Chen" where the English is a verb, which is most of them:
"Chen Bar", "Chen Velocity", "Chen MIDI Event", "Chen Note", "Chen Text", "Chen
Layer", "Chen Silence". Those are right, and "Insert Length" -> "Do dai chen" and
"Insert Type" -> "Loai chen" are the noun phrase, also right.

THREE SMALL ONES:

    "Frozen Channel"  ->  "Frozen Channel"

"Freeze" is a term here and thirty keys keep it, including three that render the
STATE with it - "Cac Track da Freeze", not "da Frozen". So the state should be
"da Freeze" too. And it cannot be "Freeze Channel", because that is a different
key with a different English - the command - and it already reads "Freeze
Channel".

    "Including Channel Settings"  ->  "Cai dat Channel lien quan"

"Including" is INCLUDING. "Lien quan" is RELATED. It is a checkbox in the
Channel Settings, and the reader cannot tell what including what.

    "Hide: All Channel Types"  ->  "An: moi loai Channel"

"mọi" lower-case after a colon, where "Tat ca" is what every other value in the
family says, and the sentence starts after the colon.

And a pair of adjacent keys that differ only in a space, and disagreed:

    "Cues  (Post-Fader)"  ->  "Cues  (Post-Fader)"
    "Cues (Post-Fader)"   ->  "Cue (Post-Fader)"

Two spaces in the first, one in the second, and the first also kept the plural
while its twin dropped it. The two spaces are the source's own and are kept.

  python tools/fix_reading65.py
  python tools/fix_reading65.py --write
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
    # the noun, not the verb: a section header in the MixConsole
    'Insert': 'Insert',

    # three keys render the STATE with "Freeze", so this one does too - and it
    # cannot be "Freeze Channel", which is a different key and a command
    'Frozen Channel': 'Channel đã Freeze',

    'Including Channel Settings': 'Bao gồm cài đặt Channel',

    'Hide: All Channel Types': 'Ẩn: Tất cả loại Channel',

    # two keys differing only in a space, which disagreed on the plural
    'Cues  (Post-Fader)': 'Cue  (Post-Fader)',
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
