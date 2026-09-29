#!/usr/bin/env python3
"""Sample translations by domain so quality can be judged by reading, not by
counting.  python tools/sample_domain.py <start> <count>
"""
import json, os, sys, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

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


want = sys.argv[1] if len(sys.argv) > 1 else None
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
count = int(sys.argv[3]) if len(sys.argv) > 3 else 60

buckets = {}
for k, v in vi.items():
    buckets.setdefault(domain(k), []).append((k, v))

if want and want != 'all':
    buckets = {want: buckets.get(want, [])}

random.seed(7)
for name, items in sorted(buckets.items()):
    if want and want != 'all' and name != want:
        continue
    print(f'\n######## {name}  ({len(items)} strings) ########')
    for k, v in items[start:start + count]:
        print(f'  EN: {src.get(k, "?")[:110]}')
        print(f'  VI: {v[:110]}')
