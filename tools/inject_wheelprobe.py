#!/usr/bin/env python3
"""Nap `hook\\wheelprobe.dll` vao Cubase: ban CHI QUAN SAT con lan chuot.

    python tools\\inject_wheelprobe.py load      # nap DLL, chua bat
    python tools\\inject_wheelprobe.py install   # nap + bat ghi log
    python tools\\inject_wheelprobe.py log       # doc log
    python tools\\inject_wheelprobe.py remove    # tra WNDPROC ve nguyen bat

Tai sao khong dung `inject_wavehook.py --dll`
---------------------------------------------
`load()` trong do go cung `WaveHook_Install`, ma wheelprobe.dll khong co ham
nay - nen se fail ngay sau khi nap. Sua `inject_wavehook.py` lai de them
tuy chon thi lam hong mot cong cu dang chay. File nay `import` no de dung
lai may (tim PID, `remote_call`, tim export) va tu goi ham cua rieng minh.

`unload` khong co o day - co y dua.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))

import inject_wavehook as I          # noqa: E402  (can `tools/` vao sys.path truoc)

# `find_export` lay base module theo `DLL.name`, nen phai gan TRUOC khi goi.
I.DLL = Path(__file__).resolve().parent.parent / 'hook' / 'wheelprobe.dll'
LOG = I.DLL.with_suffix('.log')


def install():
    """Nap DLL (neu chua nap) roi goi `WheelProbe_Install`."""
    I.check_bitness()
    if not I.DLL.exists():
        sys.exit(f'LOI: khong co {I.DLL}. Chay hook\\build_probe.bat truoc.')

    pid = I.find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay. Hay mo project truoc.')

    # Nap xong kiem module co that su da nap chua, neu co roi di tiep.
    base, _ = I.module_base(pid, I.DLL.name)
    if base is None:
        I.load(install=False)

    h = I.open_proc(pid)
    try:
        fn = I.find_export(pid, 'WheelProbe_Install')
        if fn is None:
            sys.exit('LOI: khong tim thay export WheelProbe_Install.')
        code = I.remote_call(h, fn)
        I.say(f'  WheelProbe_Install -> {code}')
        if code != 1:
            sys.exit('LOI: khong bat duoc.')
    finally:
        I.k32.CloseHandle(h)

    I.say('')
    I.say(f'  Log ghi vao: {LOG}')
    I.say('  Bay gi cuon chuot tren cua so Project (ke ca tren ruler).')
    I.say('  Thu ca hai: co Ctrl va khong Ctrl.')
    I.say('  Xem ket qua bang:  python tools\\inject_wheelprobe.py log')
    I.say('')
    I.say('  Gac lai:           python tools\\inject_wheelprobe.py remove')
    I.say('  Cubase phai dong hoan toan truoc khi nap lai.')


def remove():
    """Tra WNDPROC ve nguyen bat. KHONG FreeLibrary."""
    I.check_bitness()
    pid = I.find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = I.open_proc(pid)
    try:
        fn = I.find_export(pid, 'WheelProbe_Remove')
        if fn is None:
            I.say('  DLL chua duoc nap hoac chua bien dich lai.')
            return
        code = I.remote_call(h, fn)
        I.say(f'  WheelProbe_Remove -> {code}')
    finally:
        I.k32.CloseHandle(h)
    I.say('  Da tra WNDPROC. Cubase tro lai binh thuong ngay.')


def show_log(limit=400):
    if not LOG.exists():
        sys.exit(f'Chua co {LOG}. Nghia la DLL chua chay lan nao.')
    lines = LOG.read_text(errors='replace').splitlines()
    I.say(f'--- {LOG}  ({len(lines)} dong) ---')
    for line in lines[-limit:]:
        I.say('  ' + line)


def main():
    I.set_prototypes()
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'install'
    if cmd == 'load':
        I.load(install=False)
    elif cmd == 'install':
        install()
    elif cmd == 'remove':
        remove()
    elif cmd == 'log':
        show_log()
    else:
        sys.exit(f'lenh khong ro: {cmd}\n'
                 'dung: load | install | log | remove')


if __name__ == '__main__':
    main()