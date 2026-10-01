"""Round 68: the "[Key]" pairs, seven of ten against three.

Ten labels in the map have a "[Key]" twin - the same English, marked as the
keyboard shortcut. Ten pairs, and the map does three different things with them:

    Clear[Key]     -> "Clear"          the same word, English
    End[Key]       -> "End"
    Help[Key]      -> "Help"
    Print[Key]     -> "Print"
    Select[Key]    -> "Select"
    Pause[Key]     -> "Pause"          the same word, English
    Separator[Key] -> "Separator"

    Next[Key]      -> "Phim Next"      the same word, with "Phim" in front
    Play[Key]      -> "Phim Play"
    Stop[Key]      -> "Phim Stop"

Seven one way, three the other, and the split is not by any rule - it is by which
round touched the key. The three that add "Phim" are the only ones where a reader
would learn anything from the addition, because a Key Commands list already says
"Key" in its own title, and "Phim Next" is what you get by reading the marker as
a word instead of reading it as a marker.

The vendors settle it, and they settle it 7 out of 10 in the other direction -
the [Key] twin gets the SAME translation as the base:

    Clear      de "Entf."        Clear[Key]  de "Entf."
    End        de "Ende"         End[Key]    de "Ende"
    Help       de "Hilfe"        Help[Key]   de "Hilfe"
    Next       de "Naechstes"    Next[Key]   de "Naechste"   (a variant spelling)
    Play       de "Wiedergabe"   Play[Key]   de "Wiedergabe"
    Print      de "Drucken"      Print[Key]  de "Drucken"
    Select     de "Auswahl"      Select[Key] de "Auswahl"
    Stop       de "Stop"         Stop[Key]   de "Stop"

And the three exceptions are the three where a KEY NAME has to stay English,
because a keyboard key is named by what is printed on it - the same exemption
that Record Enable and Monitor get:

    Pause       de "Pause"   jp "Kyuushi Kigo"     Pause[Key]  jp "Pause"
    Separator   de "Trennzeichen"                   Separator[Key]  de "Separator"

So Pause[Key] and Separator[Key] keep what they have, and the other three lose
the "Phim".

And one more of the same family, which is a two-way split of its own:

    "Key"                        ->  "Key"
    "Key[keycomms]"              ->  "Phim"
    "Key[Key Commands dialog]"   ->  "Phim tat"

Two markers for the same dialog, and three renderings of one word. The dialog is
the Key Commands one, so both are "Phim tat".

One thing checked and left alone, because the split turned out to be a rule
rather than an accident: "Cue Sends" appears ten times and "Cue Send" seventeen,
and the ten are exactly the ones that act on the WHOLE set - "Reset All Cue
Sends", "Activate Cue Sends", "Views: Cue Sends" - while the seventeen act on one
send. That is right, and it is the same distinction as a plural noun for a
section and a singular for a command on one item.

  python tools/fix_reading68.py
  python tools/fix_reading68.py --write
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

WORDING = {
    # the vendors give the [Key] twin the SAME text as the base, 7 times out
    # of 10. The three exceptions are Pause and Separator below, plus the ones
    # that already matched.
    'Clear[Key]': 'Xóa',
    'End[Key]': 'Kết thúc',
    'Help[Key]': 'Trợ giúp',
    'Next[Key]': 'Tiếp',
    'Play[Key]': 'Phát',
    'Print[Key]': 'In',
    'Select[Key]': 'Chọn',
    'Stop[Key]': 'Dừng',

    # a key name stays English, as the vendors do for these two
    'Pause[Key]': 'Pause',
    'Separator[Key]': 'Separator',

    # two markers for the same dialog, three renderings of one word
    'Key[keycomms]': 'Phím tắt',
    'Key[Key Commands dialog]': 'Phím tắt',
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
       or '\ufffd' in v or not v.strip() or MARK in v]
if bad:
    print('PROBLEM (placeholder, U+FFFD, empty, or [RM] in the value):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
for k, v in changed.items():
    print(f'  {k[:50]!r}\n      {vi.get(k, "")[:64]!r}\n   -> {v[:64]!r}')

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
