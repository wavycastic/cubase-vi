#!/usr/bin/env python3
"""Sinh bo skin moi cho Cubase, mac dinh ghi ra file rieng, khong dong vao `skin.srf`.

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

    python tools/make_fl_skin.py [--level vua] [--out <duong dan>] [--install]

`--install` se sao luu `skin.srf` thanh `skin.srf.bak-<gio>` roi ghi de. Cubase 15
khong hien skin tach rieng trong danh sach, nen thuong phai ghi de truc tiep.
"""
import argparse
import colorsys
import os
import shutil
import subprocess
import sys
import time
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
    ap.add_argument('--install', action='store_true',
                    help='sao luu skin.srf roi GHI DE no bang ban moi '
                         '(Cubase 15 khong hien skin tach rieng trong danh sach)')
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

    if a.install:
        install(a.out, changes)
    else:
        print(f'\nkiem tra lai bang goc de doc:')
        for name in changes:
            got = read_back(a.out, name)
            flag = 'OK ' if got == changes[name] else 'SAI'
            print(f'  {flag} {name:<22} {got}')
        print(f'\nmuon ghi de skin.srf: them --install')


def read_back(path, name):
    return subprocess.run(
        [sys.executable, str(Path(__file__).with_name('skin_edit.py')),
         'get', str(path), name],
        check=True, capture_output=True, text=True).stdout.strip()


def install(built, changes):
    """Back up skin.srf, put the built file in its place, then verify in place."""
    if cubase_running():
        raise SystemExit('Cubase dang chay — no se ghi de skin.srf khi thoat.\n'
                         'Hay thoat Cubase truoc roi chay lai lenh nay.')

    was = SOURCE.stat()
    before = {n: read_back(SOURCE, n) for n in changes}
    backup = SOURCE.with_name(f'skin.srf.bak-{time.strftime("%Y%m%d-%H%M%S")}')
    shutil.copy2(SOURCE, backup)
    print(f'\nsao luu: {backup.name}  ({was.st_size:,} byte)')

    # ban sao luu phai chua nguyen gia tri cua ban goc
    copied = {n: read_back(backup, n) for n in changes}
    if copied != before:
        raise SystemExit(f'FAIL: ban sao luu doc ra {copied}, '
                         f'khac voi ban goc {before}; da dung truoc khi sua')
    print(f'  ban sao luu doc dung gia tri goc, ví dụ {before["eventBackDefault"]}')

    shutil.copyfile(built, SOURCE)
    print(f'ghi de: {SOURCE}  ({SOURCE.stat().st_size:,} byte)')

    now = {n: read_back(SOURCE, n) for n in changes}
    bad = {n: (v, changes[n]) for n, v in now.items() if v != changes[n]}
    if bad:
        shutil.copy2(backup, SOURCE)
        raise SystemExit(f'FAIL: doc lai skin.srf ra {bad}; da khoi phuc tu ban sao luu')
    print('  doc lai trong chinh skin.srf:')
    for n, v in now.items():
        print(f'  OK  {n:<22} {v}')


def cubase_running():
    if os.name != 'nt':
        return False
    import subprocess as sp
    out = sp.run(['tasklist', '/FI', 'IMAGENAME eq Cubase15.exe'],
                 capture_output=True, text=True).stdout
    return 'Cubase15.exe' in out


if __name__ == '__main__':
    main()