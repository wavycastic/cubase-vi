"""Compact one-line-per-hit listing of the short-label frame candidates."""
import json, re, os

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
W = re.compile(r"[A-Za-z][A-Za-z'\-]*")

out = []
for k, v in vi.items():
    if len(v) >= 40 or not HAN.search(v):
        continue
    low = set(w.lower() for w in W.findall(src.get(k, '')))
    w = W.findall(v)
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
    if best >= 4:
        out.append((k, v, ' '.join(w[at:at + best])))

out.sort()
print('TOTAL', len(out))
for k, v, r in out:
    print(f'{r[:32]:<34} | {v[:56]}')
