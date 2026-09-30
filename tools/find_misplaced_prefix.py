"""Find a "LABEL: " prefix that is not at the start of a value.

Found in round 60, on

    "CC: Attack Time"  ->  "Thời gian CC: Attack"
    "CC: Release Time" ->  "Thời gian CC: Release"

Four values. The Vietnamese word went to the FRONT and the English prefix stayed
where it was in the English, so the label and the value swapped halves - which
is the "reordered English preposition" class that audit_quality already looks
for, except that class wants a preposition and this is a whole noun phrase.

The class is mechanical once stated. In a hybrid value, a "Word: " prefix is
one of four things:

    "Bar: %d"                the prefix IS the value           - at position 0
    "CC: Balance"            the prefix is a label             - at position 0
    "Bỏ qua: Sends"          the prefix was translated         - at position 0
    "Project > Convert"      a menu path                       - a different shape

A "Word: " that starts halfway through a value is none of those. It is a
translation that ran backwards, and the reader gets the label's name after the
thing it labels.

Menu paths are excluded explicitly, because "Studio > Convert > Tracks" also
carries a colon and is right to keep.

  python tools/find_misplaced_prefix.py
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# a single capitalised word or an acronym, immediately followed by ": "
PREFIX = re.compile(r'(?<![>\w])([A-Z][A-Za-z0-9]{0,14}): ')

# The key has to START with the same prefix, or there is nothing wrong: a
# sentence that happens to contain "Drum Editor: Bat tat" is a sentence.
# "Cannot edit VariAudio: ..." is the same - its colon is a sentence colon, and
# the prefix it contains is not a label at all.
rows = []
for k, v in vi.items():
    if not HAN.search(v):
        continue
    for m in PREFIX.finditer(v):
        if m.start() == 0:
            continue
        en = src.get(k, '')
        if not en.startswith(m.group(1) + ': '):
            continue
        before = v[:m.start()]
        if before.rstrip('\n').endswith('\n') or before == '':
            continue
        rows.append((k, m.group(1), v))

print(f'"Word: " prefixes moved off the front of their own key: {len(rows)}\n')
for k, p, v in rows:
    print(f'  {p!r} in {k[:58]!r}')
    print(f'      {v[:100]!r}')
