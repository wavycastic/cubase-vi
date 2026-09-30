#!/usr/bin/env python3
"""Sinh bo skin moi cho Cubase: `Skins/fl-wave.srf`, khong dong vao `skin.srf`.

Ba muc do, chon bang `--level`:

  nhe   chi sang len, giu sat mau xanh xam cua Cubase
  vua   sang + co mau (mac dinh)
  manh  sang + mau dam, gan voi look cua FL Studio

Thay doi ba muc, theo thu tu:
  1. `eventBackDefault`   - mau nen event, cung la mau to song
  2. `eventBackMuted` / `eventWaveMuted` - giu nguyen chenh lech L ma skin goc
     dung (backMuted = backDefault + 25, waveMuted = backDefault + 20)
  3. `eventWaveAutomFill` / `eventWaveAutomLine` - dat BANG `eventBackDefault`,
     de lop phu duong volume bi giao voi mau nen o bat ke pref nao

KHONG doi `hue`: giu nguyen 210 cua Cubase nen khong phai doan cach quy doi
0-360 hay 0-255.

    python tools/make_fl_skin.py [--level vua] [--out <duong dan>]
"""
import argparse
import colorsys
import subprocess
import sys
from pathlib import Path

CUBASE_SKINS = Path(r'E:\Steinberg\Cubase 15\Skins')
SOURCE = CUBASE_SKINS / 'skin.srf'
DEFAULT_OUT = CUBASE_SKINS / 'fl-wave.srf'

# (ten, sat cua mau nen, lightness cua mau nen)
LEVELS = {
    'nhe':  (25, 88),
    'vua':  (80, 100),
    'manh': (150, 105),
}
HUE = 210


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 255.0, s / 255.0)
    return tuple(round(x * 255) for x in (r, g, b))


def edits(level):
    s, l = LEVELS[level]
    return {
        'eventBackDefault':   f'${HUE},{s:03d},{l:03d}',
        'eventBackMuted':     f'${HUE},{max(6, s // 5):03d},{l + 25:03d}',
        'eventWaveMuted':     f'${HUE},{max(4, s // 8):03d},{l + 20:03d}',
        # bang mau nen -> lop phu duong volume bi giao
        'eventWaveAutomFill': f'${HUE},{s:03d},{l:03d}',
        'eventWaveAutomLine': f'${HUE},{s:03d},{l:03d}',
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--level', choices=sorted(LEVELS), default='vua')
    ap.add_argument('--out', type=Path, default=DEFAULT_OUT)
    a = ap.parse_args()

    if not SOURCE.exists():
        raise SystemExit(f'khong thay skin goc: {SOURCE}')

    changes = edits(a.level)
    print(f'muc "{a.level}"   nguon {SOURCE}')
    print(f'{"id":<22}{"gia tri moi":<18}{"rgb":<18}doi voi goc')
    orig = {'eventBackDefault': (20, 70), 'eventBackMuted': (10, 95),
            'eventWaveMuted': (5, 90), 'eventWaveAutomFill': (15, 90),
            'eventWaveAutomLine': (15, 75)}
    for name, val in changes.items():
        h, s, l = (int(x) for x in val.strip('$').split(','))
        os_, ol = orig[name]
        d = l - ol
        print(f'{name:<22}{val:<18}{str(hsl(h, s, l)):<18}'
              f'L {ol:>3} -> {l:<3} ({d:+d})')
    print()

    args = [sys.executable, str(Path(__file__).with_name('skin_edit.py')),
            'set', str(SOURCE), '-o', str(a.out), '--check-index']
    for name, val in changes.items():
        args.append(f'{name}={val}')
    subprocess.run(args, check=True)

    print(f'\nkiem tra lai bang goc de doc:')
    for name in changes:
        got = subprocess.run(
            [sys.executable, str(Path(__file__).with_name('skin_edit.py')),
             'get', str(a.out), name],
            check=True, capture_output=True, text=True).stdout.strip()
        flag = 'OK ' if got == changes[name] else 'SAI'
        print(f'  {flag} {name:<22} {got}')


if __name__ == '__main__':
    main()