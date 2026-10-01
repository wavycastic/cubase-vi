#!/usr/bin/env python3
"""Tim noi ma so mot thong diep Win32 xuat hien ngay trong .text.

    python tools/research/msg_scan.py Cubase15.exe 20A

Vao sao can
-----------
RE "con lan chuot tren ruler co zoom khong" = tim cho biet Cubase quyet dinh
"scroll hay zoom" o dau. Do la mot nhanh so sanh voi WM_MOUSEWHEEL (0x20A),
nen thay noi ma so la tim ra tat ca cac ung vien.

Van de: 0x020A la mot so nho, dung chung rat nhieu voi moi thu kieu
(HIWORD cua mot gia tri, mot ID, mot offset...). Script nay CHI loc, khong ket
luan. Moi ket qua deu phai doc assembly de xac nhan - xem `disasm.py --func`.

Vi sao phai gioi han vao `.text`
--------------------------------
Neu quet ca file, se gap hang nghin kem o .data va .rdata. Phan lon la
metadata khong phai ma thuc thi.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _bootstrap  # noqa: F401  (dat them tools/ vao sys.path cho `import cubelib`)
from cubelib.pe import PE
from _bootstrap import die


def imm_encodings(value, size):
    """Cac cach ma hoa mot immediate trong x86-64.

    Tra ve danh sach (nhan, byte) cho tung dang: so 32 bit va (neu dung)
    so 16 bit - `81 F9 imm32` va `66 81 F9 imm16` deu hop le.
    """
    out = [(f'imm{size * 8}', value.to_bytes(size, 'little'))]
    if size == 4:
        # dang 16 bit co tien to 0x66 de khong mo rong len 32
        out.append(('imm16+66', b'\x66' + value.to_bytes(2, 'little')))
    return out


def num(text):
    """'20A', '0x20A', '522' -> 522. `int(x, 0)` tu choi '20A' (khong co 0x)."""
    return int(text, 16) if not text.lower().startswith('0x') else int(text, 0)


def is_jump_displacement(data, h):
    """Co phai 4 byte tai `h` la displacement cua lenh nhay khong?

    Day la hang loai bao dom lon nhat cua cach quet nay. `0F 8C 0A 02 00 00`
    doc lenh la `jl +0x20A` - byte 0x0A 02 00 00 la *khoang cach*, khong phai
    so so sanh voi thong diep. Neu khong loai, 25 dong dau ra deu rac.
    """
    # jcc rel32: 0F 8x <rel32>
    if h >= 2 and data[h - 2] == 0x0F and 0x80 <= data[h - 1] <= 0x8F:
        return True
    # call rel32 (E8) / jmp rel32 (E9)
    if h >= 1 and data[h - 1] in (0xE8, 0xE9):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('exe')
    ap.add_argument('msg', help='message id, xem hoac hex (20A) hay decimal (522)')
    ap.add_argument('-n', '--max', type=int, default=40)
    ap.add_argument('--section', default='.text')
    args = ap.parse_args()

    msg = num(args.msg)

    pe = PE(args.exe)
    sec = None
    for s in pe.sections:
        name = s.name.rstrip('\x00') if isinstance(s.name, str) else \
            s.name.rstrip(b'\x00').decode('latin-1')
        if name == args.section:
            sec = s
            break
    if sec is None:
        names = [(s.name.rstrip('\x00') if isinstance(s.name, str)
                  else s.name.rstrip(b'\x00').decode('latin-1'))
                 for s in pe.sections]
        die(f'khong co section {args.section}; co: {names}')

    base = sec.vaddr
    # `Binary.slice(off, LENGTH)` - tham so thu hai la DO DAI, khong phai moc
    # cuoi. Truoc day truyen `base + vsize` nen quet tu dau `.text` den HET
    # FILE, khong dung `.text`: ket qua "0 hit" khi do van dung (qui la
    # rong hon), nhung so lieu dem lai sai, va moi dia chi RVA in ra lech -
    # da lam mot ket luan sai ve mot ung vien. Phai dung `raw_size`.
    data = bytes(pe.bin.slice(pe.rva_to_off(base), sec.raw_size))
    print(f'# {args.exe}')
    print(f'# {args.section}: RVA 0x{base:X}, {len(data):,} byte')
    print(f'# WM id = 0x{msg:X} ({msg})')

    total = 0
    skipped = 0
    for label, pat in imm_encodings(msg, 4):
        hits = []
        i = data.find(pat)
        while i != -1:
            if is_jump_displacement(data, i):
                skipped += 1
            else:
                hits.append(i)
            i = data.find(pat, i + 1)
        shown = hits[:args.max]
        total += len(hits)
        print(f'\n=== {label} ({len(hits)} hit(s), showing {len(shown)}) ===')
        for h in shown:
            rva = base + h
            # can 5 byte truoc de doc tien to opcode
            lo = max(0, h - 5)
            ctx = data[lo:h + 4].hex(' ')
            fn = pe.function_containing(rva)
            where = (f'func RVA 0x{fn[0]:X}..0x{fn[1]:X}' if fn
                     else 'KHONG co trong .pdata')
            print(f'  RVA 0x{rva:08X}  [{where}]')
            print(f'    bytes[-5..+4]: {ctx}')

    print(f'\n# bo qua {skipped} hop do la displacement cua lenh nhay')

    if total == 0:
        # phai bao loi chu khong coi la "da sach" - xem AGENT.md §8.11
        raise SystemExit(
            'KHONG tim thay so nay. Hay kiem lai gia tri, hoac quet them section '
            'khac bang --section.')


if __name__ == '__main__':
    main()