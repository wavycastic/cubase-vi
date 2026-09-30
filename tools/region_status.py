#!/usr/bin/env python3
"""Trong phan con lai (nhan ngan, khong thuoc vung nao), con thuc su BI CON
KHONG - hay da xong?

Neu da xong thi vung nay khong can "dich", chi can de xem. Do la khac biet
giua "chua xep vung" va "chua dich": mot nhan ngan nhu "Low" -> "Thap" da
xong, khong con viec gi.

    python tools\region_status.py [ten-vung]
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from by_region import region_of, COMPILED, VERB, shape_of

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')

# Nhom can xem: gia tri con nguyen tieng Anh (chua co Viet) hoac co Viet
# nhung rat ngan (co the la con sót).
def status(k, v):
    en = src[k]
    if not V.search(v):
        return 'chua-co-tieng-Viet'
    # co tieng Viet nhung it - kiem so phan la tieng Anh con lai
    viet = len(re.findall(r'[\u00c0-\u024f]', v))
    if viet <= 2 and len(v) > 6:
        return 'it-tieng-Viet'
    return 'co-tieng-Viet'


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    groups = collections.defaultdict(list)
    for k, v in vi.items():
        if k not in src:
            continue
        r = region_of(k, src[k]) or ('con-lai/' + shape_of(src[k]))
        groups[(r, status(k, v))].append((k, v))

    regions = sorted({r for r, _ in groups})
    print(f'{"vung / nhom":22} {"co Viet":>9} {"it Viet":>9} {"chua Viet":>10}')
    print('-' * 54)
    for r in regions:
        if only and r != only:
            continue
        a = len(groups.get((r, 'co-tieng-Viet'), []))
        b = len(groups.get((r, 'it-tieng-Viet'), []))
        c = len(groups.get((r, 'chua-co-tieng-Viet'), []))
        tot = a + b + c
        print(f'{r:22} {a:9} {b:9} {c:10}   (tong {tot})')

    # Chi tiet phan con lai
    if only:
        for st in ('chua-co-tieng-Viet', 'it-tieng-Viet'):
            items = groups.get((only, st), [])
            if not items:
                continue
            print(f'\n--- {only} / {st} ({len(items)}) ---')
            for k, v in items[:30]:
                print(f'  EN {src[k][:80]}')
                print(f'  VI {v[:80]}')


if __name__ == '__main__':
    main()