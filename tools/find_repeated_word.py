"""Find an English content word that appears TWO OR MORE times in one value.

Found in round 61, twice, and the two findings have nothing to do with each
other except that they share the shape:

    "Version 3 (skin tag + templates tag)"
      -> "Version 3 (the Skin + the Template)"

One English noun, "tag", appears twice in the English and is translated twice in
the value. That is a defect whenever the word is being TRANSLATED, because two
occurrences of a translated word usually means the two occurrences needed
different words - here they are file manifest keys, and other software prints
them.

    "Flatten (with Options & Preferences)"
      -> "Lam phang (voi Tuy chon & Tuy chon)"

The reverse: the English half is two DIFFERENT words, "Options" and
"Preferences", and the Vietnamese half is the same word twice, because both
rendered as "Tuy chon". A Vietnamese noun repeated in one value is always
either a stutter or a mistranslation, and neither is ever intentional.

Neither class is visible to any check here, because a repetition only means
something when you read the words - a detector can count occurrences but cannot
tell a deliberate repetition ("Bar: %d", "Lặp lại lặp lại") from a wrong one.

So this is a lead list, ordered by how often the word repeats. The noise is
small: terms that are genuinely repeated, and the two-element Vietnamese phrase
that legitimately repeats a noun for emphasis. Both are recognisable on sight.

    python tools/find_repeated_word.py [mincount] [top]
"""
import json, re, sys, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 2
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 70

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# a word is a whitespace token that is purely ASCII letters
TOKEN = re.compile(r"[^\s]+")
STOP = set("a an the of in on at to for and or is are no not be mm dd hh ss".split())


def words(text, minlen=3):
    """ASCII-letter tokens only.

    A character-class scan cuts Vietnamese words in half - "cua" contains an
    ASCII a between two non-ASCII letters - and every fragment then looks like
    an English word. Round 53, and again in round 54.
    """
    for tok in TOKEN.findall(text):
        tok = tok.strip('.,:;!?()[]"\'`')
        if len(tok) >= minlen and tok.isascii() and tok.isalpha():
            if tok.lower() not in STOP:
                yield tok


rows = []
for k, v in vi.items():
    if len(v) < 6:
        continue
    c = Counter(w.lower() for w in words(v))
    rep = [w for w, n in c.items() if n >= MIN]
    if not rep:
        continue
    # only interesting when the value also has Vietnamese, or the repetition is
    # in a value that is supposed to be translated at all
    if not HAN.search(v) and len(v) < 30:
        continue
    rows.append((len(rep), max(c.values()), k, v, rep))

rows.sort(key=lambda t: (-t[0], -t[1], t[2]))
print(f'values with a word repeated {MIN}+ times: {len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for n, mx, k, v, rep in rows[:TOP]:
    print(f'  [{n}w x{mx}] {k[:60]!r}')
    print(f'          {v[:104]!r}')
    print(f'          {rep}')
