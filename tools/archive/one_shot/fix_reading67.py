"""Round 67: the extractor's private note was being printed on screen.

    "Link [short, verb]"                ->  "Lien ket [ngan, dong tu]"
    "Direction [direction of a stem]"   ->  "Direction [huong cua than not]"
    "Panner [Channel Latency Overview]" ->  "Panner [Tong quan do tre Channel]"
    "Relative [VariAudio Pitch Snap Mode]"
                                         ->  "Tuong doi [VariAudio Pitch Snap Mode]"
    "View Mode: Fill View"              ->  "Che do xem: Fill View[Score View Option]"

Round 66 established the mechanism. When two labels share an English, the
extractor puts a marker in the KEY, and Cubase looks the translation up by that
Key rather than by the English - which is not an assumption, it is what the
vendors do, several of them giving the two keys DIFFERENT translations for the
same English to prove it:

    Direction [direction of a stem]           de "Richtung"
    Direction [musical performance direction] de "Spielanweisung"

    Copy            de "Kopieren"     (the verb)
    Copy{{Noun}}    de "Kopie"        (the noun)

    Height          de "Height"
    Height[Page Height] de "Höhe"

So the marker is addressed to the extractor and to nobody else. It is not part of
the label, and a translation that echoes it back has printed a note to the
translator on the user's screen: "Lien ket [ngan, dong tu]".

This is AGENT.md rule 1 - no dictionary-style parenthetical at the end of a value
- and rule 1 does not catch it, because the rule skips any value whose KEY has a
bracket. That guard is right for a bracket the SOURCE had and wrong for one the
extractor invented: "Chord Pad Output Mode\nOn: Output is sent to..." has no
invented bracket, while "Link [short, verb]" has one whose English is a note.

    tools/find_gloss_in_value.py

Getting the detector to seven took three attempts, and the two failures are the
useful part:

    [A-Za-zÀ-ỹ] for a letter    ->  59 hits, every one of them a correct value.
                                   That range is U+00C0 to U+01FF, so it misses
                                   every Vietnamese tone mark. THE SAME TRAP AS
                                   [Ā-ỿ] IN ROUND 53, in a brand new file.

    "at most four tokens"        ->  3 hits, because "[huong cua than not]" and
                                   "[VariAudio Pitch Snap Mode]" are four words
                                   and read as a chord.

    a joiner, or a single token  ->  7 hits, all real.

A key chord after round 54 is a +-joined list or a single token, and that is the
whole test. "Nhan chuot" needs naming because it is two words with no joiner:
round 54 put a two-word Vietnamese phrase inside the bracket.

Two of the seven are already correct by accident and stay as they are - a marker
at the FRONT of a value is the marker being TRANSLATED, which is what it is for:

    "[Mixer Track Number]" -> "[So Track MixConsole]"
    "[Track Type: Group]"  -> "[Loai Track: Group]"

  python tools/fix_reading67.py
  python tools/fix_reading67.py --write
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
    # the marker said WHICH Direction; the value says it instead of repeating it
    'Direction [direction of a stem]': 'Hướng của thân nốt',

    # the marker named the panel; the value does not need to
    'Insert [Channel Latency Overview]': 'Chèn',
    'Panner [Channel Latency Overview]': 'Panner',
    'Strip [Channel Latency Overview]': 'Strip',

    'Link [short, verb]': 'Liên kết',
    'Relative [VariAudio Pitch Snap Mode]': 'Tương đối',
    'View Mode: Fill View[Score View Option]': 'Chế độ xem: Fill View',
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
       or '\ufffd' in v or not v.strip() or '[RM]' in v]
if bad:
    print('PROBLEM (placeholder, U+FFFD, empty, or [RM] in the value):')
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
