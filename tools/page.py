#!/usr/bin/env python3
"""Đọc TUẦN TỰ theo thứ tự key trong bảng, không lọc, không chấm điểm.

    python tools/page.py 0 60          # 60 chuỗi đầu, đúng thứ tự
    python tools/page.py 60 60         # 60 chuỗi tiếp theo
    python tools/page.py 5000 60 -q    # chỉ key + VI, không in EN

Cách làm này **không bỏ sót**. Công cụ cũ (`read.py`,
`sample_domain.py`) lấy mẫu theo miền hoặc ngẫu nhiên, nên chỉ đọc được
một phần. Ở đây mỗi chuỗi được đọc đúng một lần, theo thứ tự của
`keys/all_strings.tsv` - cùng thứ tự đó dùng để chia khối cho nhiều người
đọc song song mà không giẫm lên nhau.

Vì sao không lọc: hai vòng trước lọc bằng tỉ lệ số từ rồi ra danh sách
chuỗi dài, và đó là sai - dài không phải lỗi. Đọc hết thì không cần lọc, và
không có chỗ nào bị bỏ sót.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                        encoding='utf-8'))
    src = {}
    order = []
    for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                     encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
            order.append(k)
    return vi, src, order


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('start', type=int, help='vị trí bắt đầu (0-based)')
    ap.add_argument('count', type=int, nargs='?', default=60,
                    help='số chuỗi')
    ap.add_argument('-q', '--quiet', action='store_true',
                    help='chỉ in key và VI')
    ap.add_argument('-w', '--width', type=int, default=0,
                    help='in n chuỗi mỗi dòng dạng bảng (0 = mặc định 78)')
    args = ap.parse_args()

    vi, src, order = load()
    if args.start >= len(order):
        sys.exit(f'start {args.start} vượt quá {len(order)} chuỗi')
    block = order[args.start:args.start + args.count]

    print(f'#{args.start}..{args.start + len(block) - 1} '
          f'của {len(order)}  (còn {len(order) - args.start - len(block)})')
    if not args.quiet:
        print(f'{"#":>5}  {"EN":<{args.width or 40}}  VI')
        print('-' * (8 + (args.width or 40) + 2))
    for i, k in enumerate(block, args.start):
        if args.quiet:
            print(f'{i:>5}  {k}')
            print(f'        {vi[k]}')
        else:
            w = args.width or 40
            e = src.get(k, '?')
            print(f'{i:>5}  {e[:w]:<{w}}  {vi[k]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
