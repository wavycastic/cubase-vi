"""Find two keys with the SAME English but DIFFERENT Vietnamese.

The mirror image of find_duplicate_values.py, and the more dangerous of the two.

find_duplicate_values asks "do two different labels read the same on screen",
which is a usability problem. This asks the opposite: "do two labels that
Cubase stores under the same English read DIFFERENTLY on screen". That is a
correctness problem, and whether it matters depends on one thing - whether
Cubase looks the translation up by the Key or by the English.

The two are not always the same string. Round 66 is the proof:

    Key="Keep History"     <us>Keep History</us>
    Key="Keep History[RM]" <us>Keep History</us>

Two keys, one English, so a lookup by English cannot tell them apart. Every
vendor translates them identically, which is what a lookup by English forces -
and it is why the "[RM]" marker belongs in the Key and nowhere else.

So this tool is a safety net rather than a diagnosis: where the map gives one
English two different Vietnamese, one of the two is unreachable IF Cubase
resolves by English, and a needless difference if it does not. Either way it
should be a decision, and right now it is not - it is an accident of which key
was written first.

  python tools/find_same_english.py
"""
import json, re, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

g = defaultdict(list)
for k, u in src.items():
    if k in vi:
        g[u].append(k)

# Most of the 44 groups the first cut found are the extractor's own
# DISAMBIGUATION markers, and those are exactly what is SUPPOSED to separate
# two labels that share an English:
#
#     "Clear"        <us>Clear</us>       "Clear[Key]"    <us>Clear</us>
#     "Click"        <us>Click</us>       "Click[Mouse]"  <us>Click</us>
#     "Copy"         <us>Copy</us>        "Copy{{Noun}}"  <us>Copy</us>
#
# A marker in the KEY is the mechanism, so those groups are correct and there is
# nothing to report. What is left - and what cannot be resolved by a marker,
# because there is no marker - is two keys that are the SAME string with no
# distinguishing suffix at all, differing only in case or in a space. Those are
# the ones a lookup cannot tell apart.
MARK = re.compile(r'\[(?:[^\]]*)\]|\{\{[^{}]*\}\}')


def bare(k):
    return re.sub(r'\s+', ' ', MARK.sub('', k)).strip().lower()


rows = []
for u, ks in g.items():
    if len(ks) < 2:
        continue
    vals = {vi[k] for k in ks}
    if len(vals) < 2:
        continue
    # EVERY key in the group must be the same bare string. One stray key whose
    # column 2 was truncated into a neighbour - "VST Connections" and "Audio
    # Connections" both have column 2 "Audio Connections" - otherwise drags a
    # group in that has nothing to do with the defect.
    if len({bare(k) for k in ks}) != 1:
        continue
    rows.append((u, ks))

rows.sort(key=lambda t: t[0])
print(f'English strings given more than one Vietnamese: {len(rows)}\n')
for u, ks in rows:
    print(f'  EN {u[:74]!r}')
    for k in sorted(ks, key=len):
        print(f'       {k[:66]!r}')
        print(f'         -> {vi[k][:66]!r}')
    print()
