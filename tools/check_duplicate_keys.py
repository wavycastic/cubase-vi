#!/usr/bin/env python3
"""Find near-duplicate source keys that were translated inconsistently.

Cubase reuses the same label in several keys that differ only by case,
trailing dot, or an ellipsis. Those must all get the same Vietnamese.
Also flags 'X' vs 'X...' pairs whose Vietnamese dropped/added the dots.
"""
import json, re, os, collections

ROOT = r"E:\01_Projects\cubase-vi"
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))


def canon(k):
    """Collapse the cosmetic differences between equivalent keys."""
    s = k.strip()
    s = re.sub(r'\s*\.\.\.$', '', s)          # trailing ellipsis
    s = re.sub(r'\s*\[RM\]$', '', s)           # right-click marker
    s = re.sub(r'\s*\[QP\]$', '', s)           # quantize-picker marker
    s = re.sub(r'\.\s*$', '', s)               # trailing dot
    return s.strip().lower()


groups = collections.defaultdict(list)
for k, v in vi.items():
    groups[canon(k)].append((k, v))

drift = []
for c, items in groups.items():
    if len(items) < 2:
        continue
    vals = {v for _, v in items}
    if len(vals) > 1:
        drift.append((c, sorted(items)))

drift.sort(key=lambda x: -len(x[1]))
print(f'near-duplicate key groups with differing Vietnamese: {len(drift)}\n')

# only report groups where the difference is more than just an ellipsis
real = []
for c, items in drift:
    vs = sorted({v for _, v in items})
    stripped = {v.rstrip('.… ') for v in vs}
    if len(stripped) > 1:
        real.append((c, items))

print(f'... of which genuinely different wording: {len(real)}\n')
for c, items in real[:30]:
    print(f'  canonical: {c!r}')
    for k, v in items:
        print(f'      {k!r:56} -> {v!r}')
    print()
