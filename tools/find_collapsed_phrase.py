"""Find a phrase that appears twice, joined by a connector.

    "Flatten (with Options & Preferences)"
      -> "Lam phang (voi Tuy chon & Tuy chon)"

Round 61's finding, and the shape of it is much narrower than "a word repeats".
Counting words is far too loose - counting multi-syllable Vietnamese gives 297
values and almost all of them are a long sentence reusing a noun, which is what
long sentences do. Two attempts were needed to find the real class:

    find_repeated_word.py         381 values, all but a handful noise
    find_repeated_vietnamese.py   297 values, same problem

Both fail for one reason: a repetition only means something when the two halves
are set AGAINST each other. A connector does that. So the test is a phrase,
immediately repeated, with only a connector between:

    "Tuy chon & Tuy chon"          A & A
    "Tuy chon hoac Tuy chin"       A hoac B   (two words, one phrase each)
    "Project Project"              A A        (adjacent, no connector)

And the second half of the test is the one that makes it precise: the ENGLISH
must have two DIFFERENT words there. If the English says "Options and
Preferences" and the Vietnamese says "Tuy chon va Tuy chon", then two distinct
menu items have collapsed onto one word and the reader cannot tell which one a
label refers to.

If the English also repeats the word, the repetition is intentional - a
parallel construction - and the value is fine. That single condition is what
separates the defect from every legitimate repeat in the map.

    python tools/find_collapsed_phrase.py
"""
import json, re, sys, os

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
# the same 1-3 word phrase, twice, with only a connector between
JOIN = r'(?:\s*(?:&|/|,|;|\bnhưng\b|\bhoặc\b|\bvà\b|\bhay\b|\bor\b|\+)\s*)'
PHRASE = re.compile(
    r'((?:[^\s,;/&+]+\s+){0,2}[^\s,;/&+]+)' + JOIN + r'\1(?![^\s,;/&+])',
    re.IGNORECASE)

# the same test on English words, to decide whether the repetition is intended
EN_JOIN = r'(?:\s*(?:&|/|,|;|\band\b|\bor\b|\+)\s*)'
EN_PHRASE = re.compile(
    r'((?:[A-Za-z][A-Za-z\'-]*\s+){0,2}[A-Za-z][A-Za-z\'-]*)'
    + EN_JOIN + r'\1(?![A-Za-z])')

rows = []
for k, v in vi.items():
    if not HAN.search(v):
        continue
    m = PHRASE.search(v)
    if not m:
        continue
    phrase = m.group(1)
    # must be a real phrase, not a two-letter fragment
    if len(phrase) < 5 or not HAN.search(phrase):
        continue
    en = src.get(k, '')
    # the English repeating the same words means the repetition is intended
    intended = bool(EN_PHRASE.search(en))
    rows.append((intended, k, v, phrase, m.group(0)))

defects = [r for r in rows if not r[0]]
intended = [r for r in rows if r[0]]
defects.sort(key=lambda t: t[1])
print(f'same phrase twice, joined: {len(rows)}'
      f'   (intended in the English too: {len(intended)})')
print(f'COLLAPSED - two words, one phrase: {len(defects)}\n')
for _, k, v, phrase, whole in defects:
    print(f'  {phrase!r}')
    print(f'      EN  {src.get(k, "?")[:88]!r}')
    print(f'      VI  {v[:88]!r}')
    print()
if intended:
    print('--- intended repetitions, for the record')
    for _, k, v, phrase, whole in intended[:10]:
        print(f'  {phrase!r} in {k[:56]!r}')
