#!/usr/bin/env python3
"""Round 30b: cross-check the rest of the AGENT.md section 4 table.

Having found one wrong row in that table, the other rows needed checking
against the map rather than against my memory. Two more were wrong, both in
the same way - the table said one thing, the map had been doing another, and
nobody had noticed which of the two was right:

    | Rhythm Dot | dac cham nhip |   the map says "dac cham doi"
    | Slash      | gach nhip     |   the map says "gach cheo"

Rhythm dot is the dot after a note that makes it dotted - "dấu chấm dôi", the
same word as Dotted. "Nhịp" is wrong.

And the cross-check turned up real defects in the map, in two notation
families that had been assumed fine because the AGENT.md table mentioned them:

  SLASH, which had three Vietnamese forms for one English word:

    "Slashes"                            -> "Gach cheo"
    "Rhythmic Slashes"                   -> "Dau gach cheo nhip"
    "Rhythmic Slash Grouping in ..."     -> "Nhom gach nhip trong ..."
    "Slashed Grace Note"                 -> "Not lac co gach cheo"

  The last one is the round 20/23/28 error arriving in a new key: "Grace Note"
  rendered as "not lac", a word that does not exist in music, in a map where
  the other four Grace keys say "Not Grace". And "Small Slash Noteheads" had
  been reversed to "Nho Gach cheo Dau noi".

  BEAM, where "Beam over Rests" had come out as "Not duoi qua dau lang" -
  "not-tail across rest", a phrase with no meaning. And the Beaming submenu
  spelled "Split Beam" two ways in two keys.

  python tools/fix_reading30b.py
  python tools/fix_reading30b.py --write
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
    # Slash, one word: "gach cheo"
    'Rhythmic Slash Grouping in Compound Time Signatures':
        'Nhóm dấu gạch chéo nhịp trong số chỉ nhịp phức',
    'Rhythmic Slash Grouping in Irregular Time Signatures':
        'Nhóm dấu gạch chéo nhịp trong số chỉ nhịp bất thường',
    'Slash Type': 'Loại gạch chéo',
    'Slashed Grace Note': 'Nốt Grace có gạch chéo',
    'Small Slash Noteheads': 'Đầu nốt gạch chéo nhỏ',
    'Without Slashes': 'Không có gạch chéo',

    # Beam, where one label had come out as a phrase with no meaning
    'Beam over Rests': 'Đuôi nốt qua dấu lặng',
    'Beam Grouping': 'Nhóm đuôi nốt',
    'Beaming: Beam Together': 'Nối đuôi nốt: Nối chung',
    'Beaming: Split Beam': 'Nối đuôi nốt: Tách đuôi nốt',
    'Beam Together': 'Nối chung đuôi nốt',

    # Out of range, spelled two ways
    'Note and Rest Colors: Out of Range': 'Màu Note và Dấu lặng: Ngoài phạm vi',
    'Restore Marker Attribute Defaults':
        'Khôi phục giá trị mặc định của thuộc tính Marker',
    'Restate Cautionary Accidentals': 'Nhắc lại dấu hóa',
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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:62]!r}\n   -> {v!r}')

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
