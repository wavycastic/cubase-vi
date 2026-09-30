#!/usr/bin/env python3
"""Find a lowercase Vietnamese word followed by a capitalised Latin word.

That is the round 31-34 defect, seen from the left:

    "Set Controller Type"  -> "Dat Loai Controller"
    "Set Color"            -> "Dat Mau"
    "Set Crossfade Length" -> "Dat Do dai Crossfade"
    "Set Automation Value" -> "Dat Gia tri Automation"

"Dat Loai Controller" is wrong three times over and the capital letter is what
hides it: check_style cannot see a capital letter because a capital letter is a
perfectly legal character, and audit_leak cannot see it either because the word
has no English in it. Nobody reading 6,834 short labels reads every word.

The signal needs no vocabulary and so cannot invent anything: a value that has
Vietnamese, where a lowercase word that contains a Vietnamese-only letter is
immediately followed by a capitalised word, and that capital word is not an
acronym, not a bracketed key, and not a term the glossary keeps in English.

    DAT + LOAI          hit
    "Dat LOAI"          no - quoted
    [ALT + LOAI]        no - inside brackets
    DO I (English)      no - no Vietnamese-only letter in "DO"

  python tools/find_caps_after_vietnamese.py [top]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 60

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
# a lowercase word carrying at least one letter that only Vietnamese uses:
# ă â đ ê ô ơ ư and the accented forms. That is what makes it a Vietnamese word
# rather than an English one, without a dictionary.
VWORD = re.compile(r"[a-zà-ỹĂăÂâĐđÊêÔôƠơƯư]*[ĂăÂâĐđÊêÔôƠơƯưàáảãạằắẳẵặầấẩẫậ"
                   r"èéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụ"
                   r"ừứửữựỳýỷỹỵà-ỹ][a-zà-ỹĂăÂâĐđÊêÔôƠơƯưà-ỹ]*")
CAPWORD = re.compile(r"[A-Z][A-Za-z0-9'\-]*")
ACRONYM = re.compile(r'^[A-Z0-9][A-Z0-9\-/+.]*$')

rows = []
for k, v in vi.items():
    if not HAN.search(v):
        continue
    hit = []
    for m in VWORD.finditer(v):
        end = m.end()
        if end >= len(v) or v[end] != ' ':
            continue
        pre = v[:m.start()].rstrip()
        if pre.endswith(('[', '(', '"', "'", '\\')):
            continue
        nxt = CAPWORD.match(v, end + 1)
        if not nxt:
            continue
        w = nxt.group(0)
        if ACRONYM.match(w):
            continue
        if any(b in w for b in "'\"[]"):
            continue
        hit.append((m.group(0), w))
    if hit:
        rows.append((len(hit), k, v, hit))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'values with a capital word right after a Vietnamese word: {len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for n, k, v, hit in rows[:TOP]:
    print(f'  [{n}] {k[:64]!r}')
    print(f'      {v[:112]!r}')
    print(f'      {" ".join(f"{a} {b}" for a, b in hit)}')
