#!/usr/bin/env python3
"""Round 54: close the bracketed-click class, and the last of the term audit.

Twenty-six values still say `[CTRL + click]` where twenty-six others say
`[CTRL + nhấp chuột]`, and the split is not by any rule - it is by which round
touched the key. Rounds 33, 34, 46 and 49 each converted a handful and stopped,
and each time the batch was the set of keys that happened to be on screen.

So this one is generated rather than hand-written: inside square brackets only,
`click` and `Click` become `nhấp chuột`, and `Hold` in the same bracket becomes
`giữ`. Nothing outside brackets moves, so the five keys that legitimately keep
`Click` in prose - "[Click] an event" - are not touched, and neither is any
quoted feature name.

And the last find from the round 52 term audit:

    "Project and video frame rate do not match."
      -> "Frame rate của Project và Video không khớp."

`frame rate` lowercase, in a family that writes `Frame Rate` in thirty-odd keys
and where round 39 went through the AAF tooltips and fixed two of the three.

  python tools/fix_reading54.py
  python tools/fix_reading54.py --write
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
    'Project and video frame rate do not match.':
        'Frame Rate của Project và Video không khớp.',
}

# the bracketed click, generated. [ ... ] only, and only in a value that has
# Vietnamese - a value with no Vietnamese is a label, and a label keeps its
# key chord in English.
BRACKET = re.compile(r'\[[^\]]*\]')


def fix_brackets(v):
    def one(m):
        s = m.group(0)
        s = re.sub(r'\b[Cc]lick\b', 'nhấp chuột', s)
        s = re.sub(r'\bHold\b', 'giữ', s)
        return s
    return BRACKET.sub(one, v)


for k, v in vi.items():
    if not HAN.search(v) or k in WORDING:
        continue
    new = fix_brackets(v)
    if new != v:
        WORDING[k] = new

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
print(f'keys considered    : {len(real)}')
print(f'total to change    : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:60]!r}')
    print(f'      {vi.get(k, "")[:96]!r}')
    print(f'   -> {v[:96]!r}')

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
