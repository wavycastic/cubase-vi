"""Round 61: two families in the project domain, read by hand.

TEMPLATE, SPLIT SIX AGAINST ELEVEN. In the network/permissions panel - the part
of Cubase this domain covers - "Template" is a file on the server, and
"mau" is the word. But the family that lives in the media and disk menus keeps
the English:

    "Templates"          -> "Mau"             "All Templates"        -> "Tat ca mau"
    "Templates:"         -> "Mau:"            "Track Templates"      -> "Mau Track"
    "Save as Template"   -> "Luu thanh mau"   "Use a Project as Template" -> "Dung Project lam mau"
    "Test Template"      -> "Mau kiem tra"
    "Install Template"       -> "Cai dat Template"        <- the odd ones
    "Select Template"        -> "Chon Template"           <-
    "Template Category"      -> "Danh muc Template"        <-
    "Load SyncStation Template" -> "Tai SyncStation Template"
    "Project Templates"      -> "Template cua Project"

Five keys saying "Template" and ten saying "mau", with no line between them
except which panel each sits in. So the decision is made and written down -
"mau" is the word, and "Template" is kept only where a proper name contains it,
which is one key, "Load SyncStation Template", because that is Steinberg's
product.

And the same read turned up the same English noun twice in a value, which no
detector here can see because it needs two keys to compare:

    "Version 3 (skin tag + templates tag)"
      -> "Version 3 (the Skin + the Template)"

Both "tag" became "the" in a list of two, and the list is a list of FILE TAGS -
Cubase's own manifest keys, which are printed by other software. So the tags
are names:

    "Version 3 (skin tag + template tag)"

It is the same rule as the button faces: a name another program prints is
printed as it is.

And two small ones from the same read:

    "Flatten (with Options & Preferences)"  ->  "Lam phang (voi Tuy chon & Tuy chon)"

"Options" and "Preferences" are two DIFFERENT menu items - one is the dialog, one
is the dialog tab - and the value says the same word twice. "Tuy chon va Tuy
chon" reads as a stutter, and the user cannot tell which one the parenthesis
points at. The Fix tab is "Options", so:

    "Lam phang (voi Tuy chon & Tuy chinh)"

  python tools/fix_reading61.py
  python tools/fix_reading61.py --write
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
    # ten keys say "mau", five say "Template", nothing separates them
    # but which panel each sits in
    # ==================================================================
    'Install Template': 'Cài đặt mẫu',
    'Select Template': 'Chọn mẫu',
    'Template Category': 'Danh mục mẫu',
    'Project Templates': 'Mẫu của Project',

    # kept English: "Load SyncStation Template" is a Steinberg product name
    'Version 3 (skin tag + templates tag)':
        'Version 3 (skin tag + template tag)',

    # ==================================================================
    # two DIFFERENT menu items, rendered as the same word twice
    # ==================================================================
    'Flatten (with Options & Preferences)':
        'Làm phẳng (với Tùy chọn & Tùy chỉnh)',
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
    print(f'  {k[:60]!r}\n      {vi.get(k, "")[:74]!r}\n   -> {v!r}')

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
