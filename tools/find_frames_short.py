#!/usr/bin/env python3
"""The English-frame detector, restricted to SHORT values and a 3-word run.

find_english_frame.py uses a four-word run over every value, because in a long
sentence four consecutive English words can be a run of DAW terms. In a short
label that is not true: "Cycle Length", "Time Format", "Track Number" are two or
three words, and three consecutive English words that all appear in the source
of a value that also contains Vietnamese means the label was ANNOTATED, not
translated.

This is where the round 36 class is most likely to survive, because the short
labels of the seven non-general domains were read early and the long values
were read last - so whatever the long-value rounds found, the short-label
rounds found first and may have missed.

  python tools/find_frames_short.py [run] [top]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = int(sys.argv[1]) if len(sys.argv) > 1 else 3
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 80
MAXLEN = int(sys.argv[3]) if len(sys.argv) > 3 else 39

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
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
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

rows = []
for k, v in vi.items():
    if len(v) > MAXLEN or not HAN.search(v):
        continue
    en = src.get(k, '')
    if not en:
        continue
    low = set(w.lower() for w in WORD.findall(en))
    w = WORD.findall(v)
    best = cur = at = st = 0
    for i, x in enumerate(w):
        if x.lower() in low:
            if cur == 0:
                st = i
            cur += 1
            if cur > best:
                best, at = cur, st
        else:
            cur = 0
    if best >= RUN:
        rows.append((best, k, v, ' '.join(w[at:at + best])))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'short values ({MAXLEN} chars or fewer) with a {RUN}+ word English run: '
      f'{len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for b, k, v, r in rows[:TOP]:
    print(f'  [{b}] {k[:64]!r}')
    print(f'      {v[:100]!r}')
    print(f'      > {r!r}')
