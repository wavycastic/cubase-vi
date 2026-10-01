#!/usr/bin/env python3
"""Length analysis: which Vietnamese values are long *because of the translation*.

A 300-character tooltip is fine if the English is 300 characters too. What
hurts is when the Vietnamese is long and the English is short, or when the
Vietnamese is much longer than the English for the same sentence. Both mean
padding that can be cut.

  python tools/audit_bloat.py            # ranked list
  python tools/audit_bloat.py --ratio 2.0 --minlen 40
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u


def opts(flag, dflt):
    return float(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else dflt


minlen = opts('--minlen', 55)
ratio_max = opts('--ratio', 1.5)
rows = []
for k, v in vi.items():
    en = src.get(k, '')
    if len(en) < 6 or not en.strip():
        continue
    # count words, not characters: a Vietnamese syllable is shorter than an
    # English word, so a fair length ratio is VI words / EN words
    we = len(re.findall(r"[A-Za-z\u00c0-\u1ef9]+", en))
    wv = len(re.findall(r"[A-Za-z\u00c0-\u1ef9]+", v))
    if we < 3:
        continue
    r = wv / we
    if len(v) >= minlen and r > ratio_max:
        rows.append((r, len(v) - len(en), k, en, v, we, wv))

rows.sort(reverse=True)
print(f'bloat audit: {len(vi)} strings, threshold VI/EN > {ratio_max}, len >= {minlen}\n')
print(f'{len(rows)} candidates\n')
for r, d, k, en, v, we, wv in rows[:40]:
    print(f'x{r:.2f}  EN {we}w -> VI {wv}w   (+{d}c)')
    print(f'  EN: {en[:130]}')
    print(f'  VI: {v[:130]}')
    print()
