#!/usr/bin/env python3
"""Round 56: what the duplicate-value tool turned up beyond the key signature.

    "Drum"    -> "Trong"      the drum kit
    "Empty"   -> "Trong"      empty
    "Zoom In" -> "Phong vao"  zoom in
    "Zoom to Fade" -> "Zoom vao Fade"     zoom to
    "Zoom to Event" -> "Zoom theo Event"  zoom to

`Trong` is BOTH a drum and EMPTY. That is the most consequential collision the
tool has found since the key signature pair, and it is invisible per value:
each one is a defensible translation, and the damage only exists when the user
sees "Empty" in a menu and reads it as "Drum".

The family decides it. Thirty-odd keys keep "Drum" as a term - "Drum Track",
"Drum Editor", "Drum Machine", "Drum Map", "Drum Channels" - and the drum
instruments are "Trong Snare", "Trong phu", "Trong tay", "Trong Bass", which is
the correct Vietnamese. So the bare "Drum" and "Drums" are the Cubase CHANNEL
TYPE and belong with the family, and it is "Empty" that has to move - to
`rong`, which is what round 46's "Lam rong Buffer ghi hoi to" already used.

`Vao` is INTO. "Zoom in" is `Phong to` and "Zoom to X" is `Zoom toi X`, and the
map has three renderings of the second: `vao` in two keys, `theo` in four, and
`the` would be a third if anyone wrote it. `Zoom Out` is `Thu nho` and its
partner has to be `Phong to`, which is what the family already implies - so this
is one wrong word, in three keys, not a term to decide.

And "Retrospective Record" -> "Ghi hoi to MIDI", where the English is bare
"Retrospective Record" and says nothing about MIDI. Its two siblings that do say
MIDI are right.

  python tools/fix_reading56.py
  python tools/fix_reading56.py --write
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
    # "Trong" is a drum AND empty - so the bare labels move, not the
    # instruments. Thirty-odd keys keep "Drum" as the Cubase channel type.
    # ==================================================================
    'Drum': 'Drum',
    'Drums': 'Drums',
    'Empty': 'Rỗng',
    'Empty Bank': 'Bank rỗng',
    'Empty Map': 'Map rỗng',

    # ==================================================================
    # "vao" is INTO. Zoom in is "Phong to"; zoom to X is "Zoom toi X".
    # Zoom Out is "Thu nho", so the pair is decided.
    # ==================================================================
    'Zoom In': 'Phóng to',
    'Zoom In Tracks': 'Phóng to Track',
    'Zoom In Vertically': 'Phóng to theo chiều dọc',
    'Zoom In On Waveform Vertically': 'Phóng to dạng sóng theo chiều dọc',
    'Zoom to Fade': 'Zoom tới Fade',
    'Zoom to Project': 'Zoom tới Project',
    'Zoom Mode': 'Chế độ Zoom',
    'Zoom Palette': 'Bảng màu Zoom',
    'Custom Zoom Level': 'Mức Zoom tùy chỉnh',

    # ==================================================================
    # the bare label says nothing about MIDI
    # ==================================================================
    'Retrospective Record': 'Ghi hồi tố',
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
