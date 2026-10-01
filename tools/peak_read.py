#!/usr/bin/env python3
"""Doc file `.peak` cua Cubase (Audio Image File) va ve lai duong song.

    python tools\\peak_read.py <file.peak>
    python tools\\peak_read.py <file.peak> --png out.png --width 1600
    python tools\\peak_read.py <file.peak> --check          # kiem tra nhieu file
    python tools\\peak_read.py <file.peak> --at 0.5          # 1 giay, giua file

Dinh dang (do ra tu 19 file that, xem docs/WAVEFORM.md §15)
---------------------------------------------------------
Tat ca so trong header la **big-endian**; du lieu la **little-endian**. Hai thu do
nguoc nhau, va day la tu doan sai de nhat khi doc file nay:

    +0x00  char[4]   "PIFF"          <- chu ky THAT tren dia
    +0x04  BE u32    hang            (65736 o ca 19 file)
    +0x08  BE u32    kich thuoc header (96)
    +0x0C  BE u32    so kenh         (2)
    +0x10  BE u32    TONG SO FRAME cua audio
    +0x14  BE u32    hang            (256)
    +0x18  BE u32    sentinel -1     (0xFFFFFFFF)
    +0x1C  BE u32    nhan dinh dang  (hang o 18/19 file)
    +0x20  char[]    ten file audio goc, NUL ket thuc
    +0x60  du lieu: 2 x float32 LE moi ban ghi, XEN KE theo kenh

Cong thuc kiem tra du lieu (khop 19/19 file):

    so ban ghi == 2 * ceil(frames / 256)

Tuc moi **cot** gop **256 frame** cua **moi kenh**. Do phan giai cua file `.peak`
la 256 - KHAC voi nguong 8192 ma Cubase dung cho cache trong RAM (docs/WAVEFORM.md
§14.5 va §15.4).

Gia tri trong moi ban ghi la **hai so khong am** (da do 30000/30030 ban ghi), la
`(dinh tren, |dinh duoi|)` chuan hoa 0..1 - KHONG phai `(min, max)` co dau.
"""
import argparse
import math
import struct
import sys
import zlib
from pathlib import Path

HEADER_MIN = 0x20
DATA_OFF = 0x60
REC = 8
FRAMES_PER_COLUMN = 256


class Peak:
    """Mot file `.peak`. Doc header lazily; du lieu tai theo yeu cau."""

    def __init__(self, path):
        self.path = Path(path)
        self.d = self.path.read_bytes()
        if self.d[:4] != b'PIFF':
            raise SystemExit(
                f'{self.path}: khong phai file .peak (4 byte dau = '
                f'{self.d[:4]!r}, mong doi "PIFF")')
        self.sig_peak = self._be32(0x04)
        self.header_size = self._be32(0x08)
        self.channels = self._be32(0x0C)
        self.frames = self._be32(0x10)
        self.h14 = self._be32(0x14)
        self.h18 = self._be32(0x18)
        self.h1c = self._be32(0x1C)
        end = self.d.index(b'\0', HEADER_MIN)
        self.source = self.d[HEADER_MIN:end].decode('utf-8', 'replace')
        self.records = (len(self.d) - DATA_OFF) // REC

    def _be32(self, off):
        return struct.unpack_from('>I', self.d, off)[0]

    def pair(self, i):
        """Ban ghi thu `i`: (dinh tren, |dinh duoi|), ca hai float 0..1."""
        o = DATA_OFF + i * REC
        return struct.unpack_from('<ff', self.d, o)

    @property
    def columns(self):
        return self.records // self.channels

    def consistent(self):
        """Kiem tra cong thuc `records == channels * ceil(frames / 256)`.

        Tra ve (ok, so cot, frame cua cot cuoi).
        """
        cols = math.ceil(self.frames / FRAMES_PER_COLUMN)
        ok = self.records == self.channels * cols
        last = self.frames - (cols - 1) * FRAMES_PER_COLUMN
        return ok, cols, last


def envelope(peak, c0, c1, width):
    """Gom cot `c0..c1` thanh `width` pixel, trai ve (tren, duoi) moi pixel.

    Chieu cao pixel = 0.5 (0.5..1.0) nen no khong bao gio cat het duoi day.
    """
    top = [0.0] * width
    bot = [0.0] * width
    if c1 <= c0:
        return top, bot
    span = c1 - c0
    ch = peak.channels
    for c in range(c0, c1):
        x = (c - c0) * width // span
        if x >= width:
            x = width - 1
        base = c * ch
        for k in range(ch):
            a, b = peak.pair(base + k)
            if a > top[x]:
                top[x] = a
            if b > bot[x]:
                bot[x] = b
    return top, bot


def render(peak, width, c0=None, c1=None, height=160):
    """Ve mot doan duong song, tra ve danh sach dong pixel RGB."""
    if c0 is None:
        c0 = 0
    if c1 is None:
        c1 = peak.columns
    c1 = min(c1, peak.columns)
    top, bot = envelope(peak, c0, c1, width)
    mid = height // 2
    scale = (height // 2 - 1) / 0.5          # 1.0 -> het bien
    rows = [[(0, 0, 0)] * width for _ in range(height)]
    for x in range(width):
        y1 = int(round(mid - (top[x] - 0.5) * scale))
        y2 = int(round(mid + (bot[x] - 0.5) * scale))
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(max(0, y1), min(height - 1, y2 + 1)):
            rows[y][x] = (150, 220, 255)
    return rows


def ascii_art(peak, width, c0=None, c1=None, height=18):
    rows = render(peak, width, c0, c1, height)
    out = []
    for r in rows:
        out.append('  |' + ''.join('#' if p != (0, 0, 0) else ' ' for p in r) + '|')
    return out


def write_png(path, rows):
    """Ghi PNG den 24 bit. zlib la thu vien chuan, nen khong can canh cai gi."""
    h = len(rows)
    w = len(rows[0])
    raw = bytearray()
    for r in rows:
        raw.append(0)                          # filter type 0
        for px in r:
            raw += bytes(px)

    def chunk(tag, payload):
        c = struct.pack('>I', len(payload)) + tag + payload
        return c + struct.pack('>I', zlib.crc32(tag + payload) & 0xFFFFFFFF)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    Path(path).write_bytes(png)


def dump_header(peak):
    ok, cols, last = peak.consistent()
    lines = [
        f'{peak.path.name}   ({len(peak.d):,} byte)',
        f'  chu ky         {peak.d[:4].decode()}  (khong phai "PEAK")',
        f'  +0x04          {peak.sig_peak}   (hang o 19/19 file)',
        f'  +0x08          {peak.header_size}      kich thuoc header',
        f'  +0x0C          {peak.channels}          so kenh',
        f'  +0x10          {peak.frames:>10,}      tong so frame',
        f'  +0x14          {peak.h14}      (hang)',
        f'  +0x18          0x{peak.h18:08X}      sentinel -1',
        f'  +0x1C          0x{peak.h1c:08X}      nhan dinh dang',
        f'  +0x20          {peak.source!r}      ten file audio goc',
        f'  ban ghi        {peak.records:,}  = {cols:,} cot x {peak.channels} kenh'
        f'   ({FRAMES_PER_COLUMN} frame/cot)',
        f'  kiem tra       {"KHOP" if ok else "KHONG KHOP"}'
        f'   cot cuoi gom {last} frame',
    ]
    return lines


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('path', help='file .peak, hoac thu muc chua .peak')
    ap.add_argument('--png', metavar='OUT', help='ghi ra file PNG')
    ap.add_argument('--width', type=int, default=100, help='so cot pixel')
    ap.add_argument('--height', type=int, default=160,
                    help='so dong pixel (chi dung voi --png)')
    ap.add_argument('--at', type=float, metavar='SEC',
                    help='ve khoang giua file, don vi giay')
    ap.add_argument('--check', action='store_true',
                    help='quet moi file .peak trong thu muc va kiem tra cong thuc')
    a = ap.parse_args()

    if a.check:
        p = Path(a.path)
        files = sorted(p.glob('*.peak')) if p.is_dir() else [p]
        if not files:
            raise SystemExit(f'khong tim thay file .peak nao trong {p}')
        bad = 0
        for f in files:
            pk = Peak(f)
            ok, cols, _ = pk.consistent()
            bad += not ok
            print(f'  {"OK " if ok else "!! "} {f.name[:44]:<44} '
                  f'frames={pk.frames:>10,}  n={pk.records:>7,}')
        print(f'\n  {len(files) - bad}/{len(files)} khop '
              f'cong thuc records == channels * ceil(frames / {FRAMES_PER_COLUMN})')
        return 0 if bad == 0 else 1

    peak = Peak(a.path)
    for line in dump_header(peak):
        print(line)

    c0 = c1 = None
    if a.at is not None:
        rate = 44100.0
        col = int(a.at * rate / FRAMES_PER_COLUMN)
        span = max(1, a.width * FRAMES_PER_COLUMN)
        c0, c1 = col, col + span

    print()
    for line in ascii_art(peak, a.width, c0, c1):
        print(line)
    if a.png:
        write_png(a.png, render(peak, a.width, c0, c1, a.height))
        print(f'\n  da ghi {a.png}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
