#!/usr/bin/env python3
"""Find the "English frame" defect: the English sentence left standing, with
a Vietnamese preposition dropped into it.

Rounds 33 and 34 hit it by eye three times in `general`:

    "Click 'Start' to scan for unreferenced files"
      -> "Click 'Start' vao scan cho unreferenced files"
    "Press up to 5 keys to assign remote keys to subsections"
      -> "Press up vao 5 keys vao Gan remote keys vao subsections"

Then a Latin/Han ratio sweep turned up a dozen more, all of them notation
strings nobody had read:

    "Notes for Which Accidentals Have Already Been Stated Within the Bar"
      -> "Notes cho Which Accidentals Have Already Been Stated Within the Bar"
    "Primary type is used for the main chord symbol"
      -> "Primary type is used cho the main chord symbol"
    "First channel that is used for channel rotation"
      -> "First channel that is used cho channel rotation"

In every one of these the English is intact. A Vietnamese preposition was put
where the English preposition was, and the sentence was declared done.

This is trivially detectable and no check was detecting it: audit_leak counts
English words but the sentence HAS Vietnamese, so the ratio test fails;
audit_quality's "fully untranslated prose" test also needs a sentence with no
Vietnamese at all.

The signal is a verbatim run. If four or more English words in the value
appear, in the same order, in the source - then the sentence was not
translated, it was annotated. Four is the threshold because DAW terms make
runs of two and three common and harmless.

  python tools/find_english_frame.py [runlen]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = int(sys.argv[1]) if len(sys.argv) > 1 else 4

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
HAN = re.compile(r'[Ā-ỿ]')

rows = []
for k, v in vi.items():
    en = src.get(k, '')
    if not en:
        continue
    words = WORD.findall(v)
    low_en = set(w.lower() for w in WORD.findall(en))
    # sliding window over the value's words
    best = 0
    at = -1
    for i in range(len(words) - RUN + 1):
        run = [w.lower() for w in words[i:i + RUN]]
        if all(w in low_en for w in run):
            if best == 0:
                at = i
            best += 1
    if best:
        # longest contiguous stretch of words all present in the source
        run_words = words[at:at + best]
        rows.append((best, at, k, v, ' '.join(run_words)))

rows.sort(key=lambda t: (-t[0], t[2]))
print(f'values carrying a verbatim {RUN}+ word English run from the source: '
      f'{len(rows)}')
print()
for best, at, k, v, run in rows:
    mark = ' ' * 0
    print(f'  [{best:2d}] {k[:70]!r}')
    print(f'        {v[:132]!r}')
    print(f'        run: {run[:70]!r}')
