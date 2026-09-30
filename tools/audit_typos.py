#!/usr/bin/env python3
"""Loi chinh ta cua Cubase trong cot tieng Anh - ban dich co the sua duoc.

Tim trong NGUON (cot 2 cua all_strings.tsv), khong phai trong ban dich: neu
nguon sai thi ban dich sai theo la dung, va day la thu Cubase khong cho
sua duoc (chi sua o bang dich de doc).

"pich" vs "pitch" la vi du: nguon ghi "same pich and octave", ban dich dich
"cung cao do" - dung nghia, nhung kho doc thay nguon sai ngay tu dau.
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# Cac cap chu hay go nham: (dung, sai)
TYPOS = [
    (r'\bpich\b', 'pitch'),
    (r'\bthe the\b', 'the'),
    (r'\btransfered\b', 'transferred'),
    (r'\boccured\b', 'occurred'),
    (r'\brecieve[sd]?\b', 'received'),
    (r'\bseperate[sd]?\b', 'separated'),
    (r'\bexistance\b', 'existence'),
    (r'\bcompatability\b', 'compatibility'),
    (r'\bavailabe\b', 'available'),
    (r'\bavaliable\b', 'available'),
    (r'\bparamter\b', 'parameter'),
    (r'\bparamater\b', 'parameter'),
    (r'\battribut\b', 'attribute'),
    (r'\binformations\b', 'information'),
    (r'\bprefered\b', 'preferred'),
    (r'\bwich\b', 'which'),
    (r'\bwithing\b', 'within'),
    (r'\bbecuase\b', 'because'),
    (r'\bthier\b', 'their'),
    (r'\bteh\b', 'the'),
    (r'\badn\b', 'and'),
    (r'\btaht\b', 'that'),
]

found = collections.defaultdict(list)
for k, u in src.items():
    for rx, right in TYPOS:
        if re.search(rx, u, re.I):
            found[right].append((k, u, vi.get(k, '')))

total = sum(len(x) for x in found.values())
print(f'NGUON tieng Anh co {total} loi chinh ta trong {len(found)} cap\n')
if not total:
    print('=> sach')
    raise SystemExit(0)
for right, items in sorted(found.items(), key=lambda x: -len(x[1])):
    print(f'--- nen la "{right}"  ({len(items)})')
    for k, u, v in items[:4]:
        bad = re.search(r'\w*' + right.replace('ch', 'c').replace('h', 'h')
                        + r'\w*\b', u, re.I)
        m = re.search(r'\b[a-z]*' + right[:4] + r'[a-z]*\b', u, re.I)
        print(f'    EN {u[:88]}')
        print(f'    VI {v[:88]}')
    print()