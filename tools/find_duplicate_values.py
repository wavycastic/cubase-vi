#!/usr/bin/env python3
"""Find two DIFFERENT keys that have the IDENTICAL value.

Found in round 55, in the notation menus, and it is the defect no check in this
project could see:

    "Add Key Signature"      -> "Them so chi nhip"
    "Add Time Signature"     -> "Them so chi nhip"

    "Add Displayed Key Signature"  -> "Them so chi nhip hien thi"
    "Add Displayed Time Signature" -> "Them so chi nhip hien thi"

    "Key Signatures"         -> "So chi nhip"
    "Time Signatures"        -> "So chi nhip"
    "Time Signature"         -> "So chi nhip"

    "Cautionary Key Signature at End of System"
                               -> "So chi nhip nhac lai tai cuoi dong nhac"
    "Cautionary Time Signature at End of System"
                               -> "So chi nhip nhac lai tai cuoi dong nhac"

Two menu items with the same text. The user cannot tell them apart, opens the
wrong one, and nothing in the log says why. Every existing check is per-value,
so two individually perfect values pass.

The cause is in AGENT.md section 4, which gives BOTH Key Signature and Time
Signature the same Vietnamese, because some Vietnamese sources use "so chi
nhip" for both. That is defensible in a sentence and useless in a menu.

Most collisions in the output are legitimate - two keys that really are the
same label, or a label and a heading - so this is a lead list. But a menu where
two items collide is broken, and the pairs to look at are the ones where the
two English labels are NOT the same words.

  python tools/find_duplicate_values.py
"""
import json, re, sys, os
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

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r"[a-z]+")
STOP = set("a an the of in on at to for with and or is are no".split())


def content(s):
    return {w for w in WORD.findall(s.lower()) if w not in STOP}


g = defaultdict(list)
for k, v in vi.items():
    if not HAN.search(v):
        continue           # an untranslated label is a label, not a bug
    g[v].append(k)

rows = []
for v, ks in g.items():
    if len(ks) < 2:
        continue
    # only interesting when the KEYS are not themselves the same words
    sets = [content(k) for k in ks]
    same = all(s == sets[0] for s in sets)
    if same:
        continue
    rows.append((len(ks), ks, v))

rows.sort(key=lambda t: (-t[0], t[1][0]))
print(f'collisions: {len(rows)} values shared by different keys\n')
for n, ks, v in rows:
    print(f'  [{n}] {v[:76]!r}')
    for k in ks:
        print(f'       {k[:70]!r}')
    print()
