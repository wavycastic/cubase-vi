"""Find two keys that differ ONLY in whitespace or case, but not in their values.

    "Cues (Post-Fader)"   ->  "Cue (Post-Fader)"
    "Cues  (Post-Fader)"  ->  "Cues  (Post-Fader)"     two spaces, plural kept

Two keys, the same label, one space apart in the source - and Cubase shows the
value of whichever key it matched, so the SAME menu entry reads differently
depending on which one the lookup hit. That is worse than a wrong translation,
because there is no correct string to put in the file.

The same shape turns up in several forms, all of them invisible per value:

    "Channel"    ->  "Channel"
    "Channel "   ->  "Channel "        trailing space
    "add"        vs  "Add"             case
    "1 beat"     vs  "1 Beat"          case, mid-string
    "Replace[RM]" vs  "Replace"        the read-mode marker

Every one of those is two keys the extractor made from the same English by
normalising differently, and the map has to give them the same answer. This
detector groups keys by a normalised form - lower-cased, runs of whitespace
collapsed, the [RM] marker removed - and reports the groups whose values are not
identical.

The value is NOT normalised for the comparison, on purpose. "Cues " and
"Cue " genuinely need different strings, and the report shows both so the
reading decides whether the difference is the source's own or a mistake.

  python tools/find_near_duplicate_keys.py [minlen]
"""
import json, re, sys, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 3

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# the [RM] suffix is the extractor marking a read-mode variant of the same
# label; it is not part of the English
RM = re.compile(r'\[RM\]$')


def norm(k):
    return re.sub(r'\s+', ' ', RM.sub('', k)).strip().lower()


g = defaultdict(list)
for k in vi:
    if len(norm(k)) < MINLEN:
        continue
    g[norm(k)].append(k)

rows = []
for n, ks in g.items():
    if len(ks) < 2:
        continue
    vals = {k: vi[k] for k in ks}
    # ignore differences that are only the source's own whitespace
    squashed = {re.sub(r'\s+', ' ', v).strip() for v in vals.values()}
    if len(squashed) == 1:
        continue
    rows.append(ks)

rows.sort(key=lambda t: t[0])
print(f'near-duplicate key groups with differing values: {len(rows)}\n')
for ks in rows:
    print(f'  [{len(ks)}]')
    for k in sorted(ks, key=len):
        print(f'       {k[:70]!r}')
        print(f'         EN {src.get(k, "?")[:70]!r}')
        print(f'         VI {vi[k][:70]!r}')
    print()
