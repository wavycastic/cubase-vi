#!/usr/bin/env python3
"""Analyse the embedded Steinberg string-XML inside Cubase15.exe (or any binary)."""
import sys, mmap, re, collections

path = sys.argv[1]
with open(path, 'rb') as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    data = mm

def find_all(pat, limit=None):
    out, pos = [], 0
    while True:
        i = data.find(pat, pos)
        if i < 0: break
        out.append(i)
        pos = i + 1
        if limit and len(out) >= limit: break
    return out

print(f'file size = {len(data):,} bytes (0x{len(data):X})')
print()

print('--- "<?xml" occurrences ---')
for i in find_all(b'<?xml'):
    ctx = data[i:i+300]
    end = ctx.find(b'?>')
    print(f'  @0x{i:08X} : {ctx[:end+2][:300].decode("utf-8","replace")}')

print()
print('--- "<String Key=" count / first / last ---')
sk = find_all(b'<String Key=')
if sk:
    print(f'  count = {len(sk):,}')
    print(f'  first @0x{sk[0]:08X}   last @0x{sk[-1]:08X}')

print()
print('--- language child tags (counts) ---')
tags = collections.Counter()
# sample the whole string-table region for <xx>...</xx>
if sk:
    lo, hi = max(0, sk[0] - 4096), min(len(data), sk[-1] + 4096)
    for m in re.finditer(rb'<([a-z]{2,3})>', data[lo:hi]):
        tags[m.group(1).decode()] += 1
for t, c in tags.most_common(40):
    print(f'  <{t}> : {c:,}')

print()
print('--- "</String>" count ---')
es = find_all(b'</String>')
print(f'  count = {len(es):,}')

print()
print('--- region around first <String Key= (structural context) ---')
if sk:
    s = sk[0]
    seg = data[max(0,s-1500): s+200]
    txt = seg.decode('utf-8', 'replace')
    txt = re.sub(r'<[^>]*>', lambda m: m.group(0), txt)
    print(repr(txt[-1200:]))
mm.close()
