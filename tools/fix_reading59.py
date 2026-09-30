#!/usr/bin/env python3
"""Round 59: the frame class hides in past participles, and the LABEL: VALUE
menus were never checked at all.

THE FRAME. A plain reading of the notation labels turned up

    "Used in Project: %s"  ->  "Used trong Project: %s"

which is the frame defect in its purest form - an English past participle
standing exactly where the Vietnamese verb belongs, with a Vietnamese
preposition spliced after it. And the function-word detector, which has
reported this class as clean since round 54, walked straight past it, because
"Used" is not a function word by anyone's definition.

That is the real lesson, and it is the third time this project has learned it:

    a frame does not need a function word in it to be a frame. It needs a VERB.

So the detector grew a second list - thirty-odd past participles, used, selected,
activated, disabled, displayed, hidden, opened, created, deleted, added,
removed, imported, exported, saved, loaded, applied, copied, moved, loaded -
and re-running it at the looser threshold of ONE verbish word instead of two
function words put 72 values on the list, because "so", "do", "in" and "a" are
all identical in English and Vietnamese. That noise is worth paying for once:
two of the 72 are real.

    "Global Editing Disabled" -> "Editing Disabled toàn cục"
    "Global Editing Enabled"  -> "Editing Enabled toàn cục"

"Editing" is right - Warp Editing, Group Editing and Note Editing Overlay all
keep it, and so does the third key of this very family, "Global Editing" ->
"Editing toàn cục". Only the participles are English, and they are the two
half-sentences the detector now sees. The fourth key disagrees with the other
three, which is how it turned up:

    "Global Editing (All Tracks)" -> "Chỉnh sửa toàn cục (Tất cả Track)"

And one more frame the same list found, with three separate errors in it:

    "Import dropped File as single Part"
      -> "Import dropped File như single Part"

"as" is NOT "nhu". "Nhu" is LIKE. And "dropped" and "single" are English.

THE LABEL: VALUE MENUS. A shape nobody had looked for, found by asking what
the 1502 values with no Vietnamese in them actually are. Eighty-two of them
are "Something: Something", and most are the official MIDI continuous
controller names - "CC: BankSelect MSB", "CC: Sostenuto", "CC: Portamento" -
which are correctly English, because the specification prints them that way.

But three families in the list are a menu item built as "<section label>: <item>",
and the section label is a label the map has translated:

    "Expand: Cue Sends"  ->  "Expand: Cue Sends"     10 siblings say "Mở rộng:"
    "Expand: Device Panels" -> "Expand: Device Panels"
    "Source: Cue Sends"  ->  "Source: Cue Sends"      5 siblings say "Nguồn:"
    "Source: External Inputs" -> "Source: External Input"
    "Source: Monitor Mix"    -> "Source: Monitor Mix"
    "Bypass: Channel Strip"  -> "Bypass: Channel Strip"  6 of these, and
    "Bypass: EQs"               the label is "Bỏ qua"
    "Bypass: Inserts"           in the same map
    "Bypass: Modulators"
    "Bypass: Sends"
    "Bypass: Channel Strip on Main Mix"
    "Bypass: EQs on Main Mix"
    "Bypass: Inserts on Main Mix"

The user opens a menu and sees "Bypass: Sends" next to a checkbox labelled
"Bỏ qua".

And "Bypassed" -> "Đang bypass", the same word in lower case inside a
Vietnamese phrase, which is the shape of the eleven "read one word as another"
defects this project has had.

The thirty values that keep "Bypass" in PROSE stay English, and that is not an
oversight: "Bypass Insert on/off" names a command, the same exemption that
"Record Enable" and "Monitor" get. A label is translated; a command it names is
not.

  python tools/fix_reading59.py
  python tools/fix_reading59.py --write
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
    # the frame, in its purest form
    # ==================================================================
    'Used in Project: %s': 'Đã dùng trong Project: %s',

    # ==================================================================
    # "as" is not "nhu". And two English words beside it.
    # ==================================================================
    'Import dropped File as single Part':
        'Import File được thả vào làm một Part duy nhất',

    # ==================================================================
    # the family disagrees with itself three to one
    # ==================================================================
    'Global Editing': 'Editing toàn cục',
    'Global Editing (All Tracks)': 'Editing toàn cục (Tất cả Track)',
    'Global Editing Disabled': 'Editing toàn cục bị tắt',
    'Global Editing Enabled': 'Editing toàn cục được bật',

    # ==================================================================
    # a label is translated; a command it names is not
    # ==================================================================
    'Bypassed': 'Đang bỏ qua',
    'Bypass: Channel Strip': 'Bỏ qua: Channel Strip',
    'Bypass: Channel Strip on Main Mix':
        'Bỏ qua: Channel Strip trên Main Mix',
    'Bypass: EQs': 'Bỏ qua: EQs',
    'Bypass: EQs on Main Mix': 'Bỏ qua: EQs trên Main Mix',
    'Bypass: Inserts': 'Bỏ qua: Inserts',
    'Bypass: Inserts on Main Mix': 'Bỏ qua: Inserts trên Main Mix',
    'Bypass: Modulators': 'Bỏ qua: Modulators',
    'Bypass: Sends': 'Bỏ qua: Sends',

    'Expand: Cue Sends': 'Mở rộng: Cue Sends',
    'Expand: Device Panels': 'Mở rộng: Device Panels',

    'Source: Cue Sends': 'Nguồn: Cue Sends',
    'Source: External Inputs': 'Nguồn: External Input',
    'Source: Monitor Mix': 'Nguồn: Monitor Mix',

    # ==================================================================
    # a dropdown value whose own name is the term
    # ==================================================================
    'View Mode: Page View': 'Chế độ xem: Page View',
    'View Mode: Fill View[Score View Option]':
        'Chế độ xem: Fill View[Score View Option]',
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
    print(f'  {k[:60]!r}')
    print(f'      {vi.get(k, "")[:88]!r}')
    print(f'   -> {v[:88]!r}')

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
