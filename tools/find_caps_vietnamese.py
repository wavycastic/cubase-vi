#!/usr/bin/env python3
"""Find a capital Latin word whose lower-case form is a Vietnamese word.

That is exactly the round 31-34 defect:

    "Set Controller Type"  -> "Dat Loai Controller"
    "Set Color"            -> "Dat Mau"
    "Set Crossfade Length" -> "Dat Do dai Crossfade"
    "Set Automation Value" -> "Dat Gia tri Automation"

"Dat Loai Controller" is wrong three times over - Loai should be lower-case
`loai`, Controller is a term, and `Dat` is a Vietnamese verb - and the capital
letter is what hides it. check_style cannot see it, because a capital letter is
a perfectly legal character, and audit_leak cannot see it either, because the
word has no English in it.

The test is mechanical and precise. Take every capital Latin word in a value,
lower-case it, strip the diacritics, and ask whether the result is a word the
Vietnamian half of the map already uses. If it is, the word is Vietnamese that
somebody capitalised. Four characters minimum, because `Do` and `La` and `Co`
strip down to Vietnamese by accident.

The vocabulary is not a word list - it is every word appearing in the Vietnamese
half of the map itself, so it can only ever report a word that is demonstrably
in use. That also means the check is self-limiting: it needs no dictionary, and
it cannot invent a false positive out of a word nothing else uses.

  python tools/find_caps_vietnamese.py [minlen]
"""
import json, re, sys, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 4

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# A VIETNAMESE LETTER, spelled with escapes on purpose. The obvious
# [A-ỿ] is U+0100 to U+1EF9, and it is WRONG: Vietnamese keeps its most
# common letters - a, a, e, e, o, o, u, u, d and their tone marks - in
# U+00C0 to U+00FF, which is BELOW the start of that range. So a value
# written entirely with those letters, like "Thêm bè", tested as NOT
# Vietnamese, and eight detectors built on this test were quietly looking
# at a subset of the map. Found in round 53, by a value that should have
# been reported and was not.
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'\-]*")
# a run of capitals is a term or an acronym, not a capitalised Vietnamese word
TERMISH = re.compile(r'^[A-Z0-9][A-Z0-9\-/+.]*$')


def fold(s):
    """lower-case and strip diacritics, so `Loai` meets `loại`."""
    s = s.lower()
    out = []
    for ch in unicodedata.normalize('NFD', s):
        if unicodedata.combining(ch):
            continue
        out.append(ch)
    return ''.join(out)


# the Vietnamese vocabulary, built from the map itself
vocab = set()
for v in vi.values():
    if not HAN.search(v):
        continue
    for w in re.findall(r'[a-zà-ỹĐđ]{3,}', v):
        vocab.add(fold(w))

rows = []
for k, v in vi.items():
    if len(v) < MIN or not HAN.search(v):
        continue
    stray = []
    for i, m in enumerate(WORD.finditer(v)):
        w = m.group(0)
        if i == 0 or not w[0].isupper():
            continue
        if TERMISH.match(w) or len(w) < 4:
            continue
        f = fold(w)
        if len(f) < 4 or f not in vocab:
            continue
        pre = v[:m.start()].rstrip()
        if pre.endswith(('.', ':', ';', '"', "'")):
            continue          # a capital is fine after a sentence break
        stray.append(w)
    if stray:
        rows.append((len(stray), k, v, stray))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'values with a capitalised Vietnamese word: {len(rows)}\n')
for n, k, v, stray in rows:
    print(f'  [{n}] {k[:64]!r}')
    print(f'      {v[:112]!r}')
    print(f'      {stray}')
