#!/usr/bin/env python3
"""Đọc một GIA ĐÌNH chuỗi cùng lúc - công cụ để đọc, không phải để chấm.

    python tools/family.py Import
    python tools/family.py "Side-Chain"
    python tools/family.py -p "Set Note"          # chỉ chuỗi BẮT ĐẦU bằng cụm này
    python tools/family.py -l 40 Full             # chuỗi chứa "Full", dài nhất 40
    python tools/family.py -a                     # xem mọi gia đình bị lệch

**Vì sao cần, sau hai vòng đi sai.**

Vòng 88 lọc bằng tỉ lệ số từ. Ra một danh sách chuỗi dài. Nhưng dài không
phải lỗi: 3.234 chuỗi so sánh được thì trung vị là **ngắn hơn** 2 ký tự, và
không chuỗi nào dài hơn 30 ký tự. Công cụ chấm điểm sai chỗ.

Vòng 89 sửa được những lỗi thật, và tất cả đều lộ ra **khi đặt hai chuỗi cạnh
nhau**:

    Import Audio File  -> 'Import file Audio'
    Import Audio Files -> 'Import File Audio'      lệch hoa/thường

    Side-Chain Input  -> 'Side-Chain Input'
    Side-chain Inputs -> 'Side-chain Input'       lệch hoa/thường

Rời ra, mỗi chuỗi trông đều ổn. Đó là lý do phải đọc cả nhóm.

Cơ: key của bảng dịch **chính là chuỗi tiếng Anh**. Không có id, không có
đường dẫn, không có vai trò. Nên gia đình = các chuỗi cùng nói một thứ, và
cách tìm gia đình gần nhất là **từ đầu tiên**: `Import ...`, `Side-Chain ...`.

Lưu ý khi đọc: hai chuỗi khác nhau chỉ ở khoảng trắng cuối
(`Channel` và `Channel `) là **hai key khác nhau** và giữ khoảng trắng là đúng.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                        encoding='utf-8'))
    src = {}
    for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                     encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return vi, src


def show(k, v, src, mark=''):
    print(f'{mark}{k}')
    print(f'     EN  {src.get(k, "?")!r}')
    print(f'     VI  {v!r}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('word', nargs='?', help='từ hoặc cụm cần tìm')
    ap.add_argument('-p', '--prefix', action='store_true',
                    help='chỉ chuỗi BẮT ĐẦU bằng cụm, thay vì chứa')
    ap.add_argument('-l', '--limit', type=int, default=0,
                    help='giới hạn số dòng (0 = không giới hạn)')
    ap.add_argument('-a', '--all', action='store_true',
                    help='liệt kê các gia đình đang dùng hai kiểu ghi')
    ap.add_argument('-c', '--count', type=int, default=200,
                    help='--all: số gia đình in ra')
    args = ap.parse_args()

    vi, src = load()

    if args.all:
        # Những giá trị khác nhau chỉ vì khoảng trắng thừa là HAI key khác nhau
        # (`Channel` và `Channel `), nên phải loại trước - nếu không sẽ báo
        # động giả hàng loạt và công cụ mất tác dụng.
        def norm(s):
            return re.sub(r'\s+', ' ', s).strip().lower()

        g = {}
        for k, v in vi.items():
            g.setdefault(norm(v), set()).add(v)
        split = {}
        for n, vs in g.items():
            if len(vs) < 2:
                continue
            # khác nhau chỉ ở khoảng trắng đầu/cuối -> cùng một thứ
            if {s.strip() for s in vs} == {next(iter({s.strip() for s in vs}))}:
                continue
            split[n] = vs
        print(f'{len(split)} nhóm dùng hai kiểu ghi cho cùng một thứ:\n')
        for n, vs in list(sorted(split.items()))[:args.count]:
            keys = [k for k, v in vi.items() if norm(v) == n]
            print(f'  {sorted(vs)}')
            for k in sorted(keys)[:6]:
                show(k, vi[k], src, '    ')
            print()
        return 0

    if not args.word:
        ap.print_help()
        return 1

    w = args.word
    if args.prefix:
        keys = [k for k in vi if k.lower().startswith(w.lower())]
    else:
        keys = [k for k in vi if w.lower() in k.lower()]
    keys.sort(key=lambda k: (len(k), k))
    if args.limit:
        keys = keys[:args.limit]

    print(f'{len(keys)} chuỗi chứa "{w}"'
          + (' và BẮT ĐẦU bằng nó' if args.prefix else '') + '\n')
    for k in keys:
        show(k, vi[k], src)
    return 0


if __name__ == '__main__':
    sys.exit(main())
