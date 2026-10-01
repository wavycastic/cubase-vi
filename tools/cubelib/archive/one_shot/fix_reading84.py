#!/usr/bin/env python3
"""Round 84: add 27 forbidden translations, and fix the 3 strings they found.

The list of terms that must not be translated was 22 patterns. It is now 49.
Nothing was invented to get there: every new pattern is a mistranslation
already recorded in AGENT.md or in AGENT.md.bak, the 2,442-line original that
the 199-line compression reduced to rules and thereby dropped the evidence
for.

What the new patterns found on the live map:

  1. `Display Quantization` -> "Hiển thị Quantize"  (hard rule violation)

     Word order. Three keys up, `Display Note` is `Note hiển thị`; the whole
     map puts the noun first. Round 72 fixed this exact defect - "Display
     Quantize bị dịch là 'Hiển thị Quantize' -> Quantize hiển thị" - and one
     key came back.

  2. `Factory Library` -> "Thư viện mặc định"

     AGENT.md §3: "`Factory` -> giữ `Factory`, đã có 4 kiểu". Eleven other
     Factory keys keep the English. This one alone translated it, and in a
     way that drops Library entirely.

  3. `Learn` -> "Học"

     §72 standardised `MIDI Learn` and `Bypass chế độ Learn` across the map;
     a bare `Learn` rendered as "Học" is the only string that treats it as a
     verb.

Two things are NOT fixed here, deliberately:

  `Band %d` -> "Dải %d" is left alone. `Band` means an EQ band as often as a
  frequency band, and "Dải" is right for the first. One string is not enough
  to tell which; a human picks.

  `Time Signature` -> "số chỉ nhịp" is left alone although it is 49 strings
  and AGENT.md §2 lists Time Signature under "giữ tiếng Anh". §2 and the map
  have disagreed about this term since before the compression, in favour of
  the Vietnamese. Recording it in terms_do_not_translate.json where it can be
  decided once, rather than making a 49-string change inside a round whose
  job was to add detectors.

  python tools/fix_reading84.py
  python tools/fix_reading84.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cubelib.placeholders import PLACEHOLDER

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

WORDING = {
    'Display Quantization': 'Quantize hiển thị',
    'Factory Library': 'Factory Library',
    'Learn': 'Learn',
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}): {missing}')
    sys.exit(1)

bad = [(k, v) for k, v in real.items()
       if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'total to change : {len(changed)}')
for k, v in changed.items():
    old = vi.get(k, '')
    print(f'  {k!r}  {len(old)}c -> {len(v)}c')
    print(f'      {old!r}')
    print(f'   -> {v!r}')

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
print(f'\napplied {n} change(s) to batches')