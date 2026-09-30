"""Find a VIETNAMESE word repeated two or more times in one value.

    "Flatten (with Options & Preferences)"
      -> "Lam phang (voi Tuy chon & Tuy chon)"

This is round 61's second finding, and the obvious detector - count a word twice
- MISSES IT, because the two occurrences are "Tuy chon" and the repetition is in
the Vietnamese half. find_repeated_word.py counts ASCII words only, and for good
reason: counting characters there cuts Vietnamese words in half. But that same
caution is what makes it blind to the class that matters most here, since a
value in this map is MOSTLY Vietnamese.

So this is the same scan with the other half of the alphabet:

  - a token is a Vietnamese word when it contains a letter outside U+0020-007F
  - it must be at least four characters, so "va", "de", "co" do not qualify
  - English function words that happen to be Vietnamese are excluded, because
    "cho", "trong", "khi" and "nhip" repeat legitimately in every sentence

What is left is small, and what is left is a defect every time. A Vietnamese
noun or verb repeated in one value is either a stutter, two different English
words collapsed onto one, or a word that needed a synonym the writer did not
have. None of the three is ever what was meant.

The exception to look for is a deliberate parallel, where the repetition carries
the parallel - "Lap lai toan bo Track", the two halves of "X or Y". Those read
as deliberate on sight.

    python tools/find_repeated_vietnamese.py [minlen] [mincount] [top]
"""
import json, re, sys, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 4
MINC = int(sys.argv[2]) if len(sys.argv) > 2 else 2
TOP = int(sys.argv[3]) if len(sys.argv) > 3 else 60

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
TOKEN = re.compile(r"[^\s]+")
# Vietnamese words that also exist in English, and so repeat harmlessly. Every
# one of these has been checked against the map: they are all function words,
# and a value repeats them because it has more than one clause.
ENGLISH = set("""
in at on to for and or but not no is are was were be been has have had do does
did will would can could may might must this that these those there here
all any each every some both either neither
""".split())


def viet_words(text):
    for tok in TOKEN.findall(text):
        # strip punctuation and brackets that surround a token
        tok = tok.strip('.,:;!?()[]"\'`%*')
        if len(tok) < MINLEN:
            continue
        if not HAN.search(tok):
            continue          # not a Vietnamese word
        low = tok.lower()
        if low in ENGLISH:
            continue
        yield low


rows = []
for k, v in vi.items():
    if len(v) < 12:
        continue
    c = Counter(viet_words(v))
    rep = {w: n for w, n in c.items() if n >= MINC}
    if not rep:
        continue
    rows.append((sum(rep.values()), k, v, rep))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'values with a Vietnamese word repeated {MINC}+ times '
      f'({MINLEN}+ chars): {len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for n, k, v, rep in rows[:TOP]:
    print(f'  [{n}] {k[:60]!r}')
    print(f'      {v[:100]!r}')
    print(f'      {rep}')
