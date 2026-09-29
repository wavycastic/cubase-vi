#!/usr/bin/env python3
"""Read the short values: menu labels and button names.

read_long.py covers sentences. This covers the other half of the map - roughly
9,000 labels of one to six words. That is where the term drift lives, because
a label has no sentence to carry the meaning and is the first thing the
automated passes got wrong.

  python tools/read_short.py mixer 0 90
  python tools/read_short.py all 0 90
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


def domain(k):
    s = k.lower()
    if re.search(r'\b(chord|voicing|tension|scale|articulation|harmony|note)\b', s):
        return 'music-theory'
    if re.search(r'\b(export|render|bounce|warp|audio|file|pool|import|media|'
                 r'format|bit|sample rate|fade|freeze|process)\b', s):
        return 'media'
    if re.search(r'\b(insert|send|eq|plugin|vst|bus|channel|fader|pan|routing|'
                 r'compressor|gate|limiter)\b', s):
        return 'mixer'
    if re.search(r'\b(locator|marker|cycle|transport|cursor|record|play|loop|'
                 r'tempo|quantize|grid|snap|scroll|zoom)\b', s):
        return 'transport'
    if re.search(r'\b(shortcut|key command|assign|menu|command|context|'
                 r'right.click|window|toolbar|panel|dialog|page)\b', s):
        return 'ui'
    if re.search(r'\b(score|stave|staff|system|bar|beat|clef|rest|notation|'
                 r'beam|ledger|signatur)\b', s):
        return 'notation'
    if re.search(r'\b(network|server|user|permission|shared|profile|'
                 r'project setup|template|preferences)\b', s):
        return 'project'
    return 'general'


def islong(v):
    return len(v) >= 45 and (len(re.findall(r'[A-Za-z\u00c0-\u1ef9]+', v)) >= 6
                             or '\\n' in v)


want = sys.argv[1] if len(sys.argv) > 1 else 'all'
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
count = int(sys.argv[3]) if len(sys.argv) > 3 else 90
maxlen = int(sys.argv[4]) if len(sys.argv) > 4 else 44

items = [(k, v) for k, v in vi.items()
         if not islong(v) and len(v) <= maxlen
         and (want == 'all' or domain(k) == want)]
items.sort()
print(f'## {want}  {len(items)} short values  (showing {start}..{start+count})\n')
for k, v in items[start:start + count]:
    print(f'{src.get(k, "?")}\n    {v}\n')
