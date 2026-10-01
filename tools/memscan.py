#!/usr/bin/env python3
"""Doc RAM cua Cubase15.exe de tim doi tuong AudioImage - CHI DOC, khong ghi gi.

    python tools\\memscan.py find 0x145FFAE30          # tim con tro tro toi vtable
    python tools\\memscan.py obj  0x1A2B3C4D5E6        # dump 0x70 byte quanh con tro do
    python tools\\memscan.py peak 0x1A2B3C4D5E6        # doc ban ghi peak that trong RAM
    python tools\\memscan.py probe                     # quet ca 4 vtable AudioImage
    python tools\\memscan.py read 0x141E9AD10 64        # doc bat ky dia chi nao

Van de an toan
-------------
Tren Windows khong co quyen doc RAM cua tien trinh khac. Cách duy nhat la
`OpenProcess` + `ReadProcessMemory`. O day **`PROCESS_VM_WRITE` va
`PROCESS_CREATE_THREAD` deu KHONG mo** — cong cu nay khong the ghi vao Cubase,
ke ca khi co loi. Dung `tools\\inject_wavehook.py` cho phan ghi.

Mot kien thuc ve con tro: trong Cubase mot vtable nam o dau doi tuong, nen dia
chi con tro tro toi vtable chinh la dia chi doi tuong. Quet duy nhat mot vtable
cung du de tim ra doi tuong, va chi can doc 0x70 byte quanh no.
"""
import argparse
import ctypes
import struct
import sys
import time
from ctypes import wintypes
from pathlib import Path

k32 = ctypes.WinDLL('kernel32', use_last_error=True)

PROCESS_VM_READ           = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

MEM_COMMIT  = 0x1000
MEM_FREE    = 0x10000
MEM_RESERVE = 0x2000
PAGE_GUARD  = 0x100
PAGE_NOACCESS = 0x01

# SIZE / ADDRESS phai la UL_PTR (8 byte).
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BaseAddress', ctypes.c_void_p),
        ('AllocationBase', ctypes.c_void_p),
        ('AllocationProtect', wintypes.DWORD),
        ('RegionSize', ctypes.c_size_t),
        ('State', wintypes.DWORD),
        ('Protect', wintypes.DWORD),
        ('Type', wintypes.DWORD),
    ]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD), ('th32ModuleID', wintypes.DWORD),
        ('th32ProcessID', wintypes.DWORD), ('GlblcntUsage', wintypes.DWORD),
        ('ProccntUsage', wintypes.DWORD), ('modBaseAddr', ctypes.c_uint64),
        ('modBaseSize', wintypes.DWORD), ('hModule', wintypes.HANDLE),
        ('szModule', ctypes.c_char * 256), ('szExePath', ctypes.c_char * 260),
    ]

    def base(self):
        return int(self.modBaseAddr)


class PROCESSENTRY32(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
        ('th32ProcessID', wintypes.DWORD), ('th32DefaultHeapID',
                                            ctypes.c_size_t),
        ('th32ModuleID', wintypes.DWORD), ('cntThreads', wintypes.DWORD),
        ('th32ParentProcessID', wintypes.DWORD), ('pcPriClassBase',
                                                  ctypes.c_longlong),
        ('dwFlags', wintypes.DWORD), ('szExeFile', ctypes.c_char * 260),
    ]


TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010


def set_prototypes():
    P = ctypes.c_void_p
    D = wintypes.DWORD
    k32.OpenProcess.restype = wintypes.HANDLE
    k32.OpenProcess.argtypes = [D, wintypes.BOOL, D]
    k32.CloseHandle.restype = wintypes.BOOL
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    k32.ReadProcessMemory.restype = wintypes.BOOL
    k32.ReadProcessMemory.argtypes = [wintypes.HANDLE, P, P, ctypes.c_size_t,
                                      ctypes.POINTER(ctypes.c_size_t)]
    k32.VirtualQueryEx.restype = ctypes.c_size_t
    k32.VirtualQueryEx.argtypes = [wintypes.HANDLE, P, P, ctypes.c_size_t]
    k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    k32.CreateToolhelp32Snapshot.argtypes = [D, D]
    k32.Process32First.restype = wintypes.BOOL
    k32.Process32First.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    k32.Process32Next.restype = wintypes.BOOL
    k32.Process32Next.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    k32.Module32First.restype = wintypes.BOOL
    k32.Module32First.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    k32.Module32Next.restype = wintypes.BOOL
    k32.Module32Next.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    # KHONG dung `GetMappedFileNameW`: no nam trong `psapi.dll`, khong phai
    # `kernel32`, va khai bao no o day se lam `set_prototypes()` no ra
    # AttributeError truoc khi quet duoc mot byte nao. Module lay bang Toolhelp.


def find_pid(name='cubase15.exe'):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        e = PROCESSENTRY32()
        e.dwSize = ctypes.sizeof(e)
        ok = k32.Process32First(snap, ctypes.byref(e))
        while ok:
            if e.szExeFile.decode(errors='replace').lower() == name:
                return e.th32ProcessID
            ok = k32.Process32Next(snap, ctypes.byref(e))
    finally:
        k32.CloseHandle(snap)
    return None


def modules(pid):
    """Danh sach (ten, base, size) cua module trong tien trinh."""
    snap = k32.CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    out = []
    try:
        e = MODULEENTRY32()
        e.dwSize = ctypes.sizeof(e)
        ok = k32.Module32First(snap, ctypes.byref(e))
        while ok:
            out.append((e.szModule.decode(errors='replace'), e.base(),
                        e.modBaseSize))
            ok = k32.Module32Next(snap, ctypes.byref(e))
    finally:
        k32.CloseHandle(snap)
    return out


def open_read(pid):
    h = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not h:
        raise ctypes.WinError(ctypes.get_last_error())
    return h


def rdmem(h, addr, n):
    """Doc n byte. Tra (bytes, so_byte_doc_duoc) — khong nem loi."""
    if n <= 0:
        return b'', 0
    buf = (ctypes.c_char * n)()
    got = ctypes.c_size_t()
    if not k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, n,
                                 ctypes.byref(got)):
        return b'', 0
    return bytes(buf[:got.value]), got.value


def regions(h, limit=None):
    """Cac vung nho COMMIT va doc duoc."""
    addr = 0
    mbi = MEMORY_BASIC_INFORMATION()
    total = 1 << 47
    while addr < total:
        if not k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi),
                                  ctypes.sizeof(mbi)):
            break
        base = mbi.BaseAddress or 0
        size = mbi.RegionSize
        ok = (mbi.State == MEM_COMMIT
              and not (mbi.Protect & PAGE_GUARD)
              and not (mbi.Protect & PAGE_NOACCESS))
        if ok and size:
            yield base, size
        nxt = base + size
        if nxt <= addr:                 # chong loi vong
            break
        addr = nxt


def module_of(pid, addr):
    for name, base, size in modules(pid):
        if base <= addr < base + size:
            return name
    return None


def scan(h, pattern, start=None, end=None, max_hits=64, progress=None):
    """Tim `pattern` (bytes) trong cac vung nho. Tra danh sach dia chi."""
    hits = []
    seen = set()
    nregions = 0
    for base, size in regions(h):
        # Doc theo lat 8 MB de khong phai cap phat bo dem qua lon
        step = 8 << 20
        overlap = len(pattern) - 1
        for off in range(0, size, step):
            chunk_len = min(step + overlap, size - off)
            data, got = rdmem(h, base + off, chunk_len)
            if not data:
                continue
            i = data.find(pattern)
            while i >= 0:
                a = base + off + i
                if start is None or start <= a < end:
                    if a not in seen:
                        seen.add(a)
                        hits.append(a)
                        if len(hits) >= max_hits:
                            return hits
                i = data.find(pattern, i + 1)
        nregions += 1
        if progress and nregions % 200 == 0:
            progress(nregions)
    return hits


def hexdump(base, data, width=16):
    out = []
    for i in range(0, len(data), width):
        ch = data[i:i + width]
        hexs = ' '.join('%02X' % c for c in ch)
        txt = ''.join(chr(c) if 32 <= c < 127 else '.' for c in ch)
        out.append('  %012X  %-*s |%s|' % (base + i, width * 3 - 1, hexs, txt))
    return '\n'.join(out)


def u64(data, off=0):
    return struct.unpack_from('<Q', data, off)[0]


def u32(data, off=0):
    return struct.unpack_from('<I', data, off)[0]


def f32(data, off=0):
    return struct.unpack_from('<f', data, off)[0]


# Vtable interface 6 slot, xac ninh o docs/WAVEFORM.md §3.6
VTABLES = {
    0x145FFAE30: 'AudioImageFile.interface',
    0x145FFACA0: 'AudioImageCache.interface',
    0x145FFACE0: 'AudioImageCacheAccessor.interface',
    0x145FFAE70: 'AudioImageAccessor.interface',
    0x145FFADC0: 'AudioImageFile.primary',
    0x145FFAC20: 'AudioImageCache.primary',
}

# 0x1421F4C20 doc mot ban ghi: [rcx+0x20] >> 3 = so ban ghi,
# [rcx+0x30] -> [ +0x30] = tong so ban ghi, [ +0x38] = ...
OFF_RECORD_COUNT_PTR = 0x30
OFF_RECORD_COUNT = 0x30


def cmd_find(a):
    pid = find_pid()
    if not pid:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_read(pid)
    try:
        pat = struct.pack('<Q', a.addr)
        print(f'quet 0x{a.addr:X} trong pid {pid} ...')
        t0 = time.time()
        hits = scan(h, pat, max_hits=a.limit,
                    progress=lambda n: print('  ...%d vung' % n, flush=True))
        print('  tim thay %d dia chi trong %.1fs' % (len(hits),
                                                      time.time() - t0))
        for x in hits:
            mod = module_of(pid, x) or '?'
            print('  0x%X   (%s)' % (x, mod))
    finally:
        k32.CloseHandle(h)


def dump_object(h, pid, addr, size=0x70):
    data, got = rdmem(h, addr, size)
    if not data:
        print('  doc that bai tai 0x%X' % addr)
        return None
    print('  doc duoc %d byte' % got)
    print(hexdump(addr, data))
    if got >= 8:
        vt = u64(data, 0)
        name = VTABLES.get(vt)
        print('\n  vtable = 0x%X  %s' % (vt, name or '(khong trong bang)'))
    return data


def cmd_obj(a):
    pid = find_pid()
    if not pid:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_read(pid)
    try:
        print('doi tuong tai 0x%X:' % a.addr)
        dump_object(h, pid, a.addr, a.size)
    finally:
        k32.CloseHandle(h)


def cmd_peak(a):
    """Doc ban ghi peak that trong RAM.

    Theo docs/WAVEFORM.md §3.6: `vfunc+0x18` doc `[this+0x30]->+0x38`, va
    `vfunc+0x20` chan tren `[this+0x30]->+0x30`. Hai truong nay phai bang nhau
    voi so ban ghi trong file `.peak`. Doc ca hai de kiem tra.
    """
    pid = find_pid()
    if not pid:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_read(pid)
    try:
        head, _ = rdmem(h, a.addr, 0x70)
        if len(head) < 0x40:
            sys.exit('  doc that bai')
        print('this = 0x%X   vtable = 0x%X %s'
              % (a.addr, u64(head),
                 VTABLES.get(u64(head), '?')))
        inner = u64(head, OFF_RECORD_COUNT_PTR)
        print('[this+0x30] -> 0x%X' % inner)
        if not inner:
            print('  null -> chua nap du lieu (se tra 256 theo nhanh null)')
            return
        ib, got = rdmem(h, inner, 0x60)
        if len(ib) < 0x40:
            sys.exit('  doc [this+0x30] that bai')
        print('\n--- struct long trong (0x60 byte) ---')
        print(hexdump(inner, ib, 0x40))
        print('\n  [+0x30] = %d   (so ban ghi theo vfunc+0x20)' % u32(ib, 0x30))
        print('  [+0x38] = %d   (gia tri ma vfunc+0x18 tra ve)' % u32(ib, 0x38))
        print('  [+0x28] = 0x%X' % u32(ib, 0x28))
        print('\n--- 6 truong con tro dau ---')
        for off in range(0, 0x30, 8):
            print('  [+0x%02X] = 0x%X' % (off, u64(ib, off)))
    finally:
        k32.CloseHandle(h)


def cmd_probe(a):
    pid = find_pid()
    if not pid:
        sys.exit('LOI: Cubase15.exe khong chay.')
    print(f'pid {pid}, ImageBase cua Cubase15.exe:')
    for name, base, size in modules(pid):
        if name.lower() == 'cubase15.exe':
            print('  base 0x%X  size 0x%X' % (base, size))
    exe_base = 0x140000000
    h = open_read(pid)
    try:
        for vt, label in sorted(VTABLES.items(), key=lambda kv: kv[1]):
            if not (exe_base <= vt < exe_base + 0x8000000):
                print('\n%s  0x%X  -- ngoai image, BO QUA' % (label, vt))
                continue
            print('\n=== %s  0x%X ===' % (label, vt))
            pat = struct.pack('<Q', vt)
            t0 = time.time()
            # KHONG truyen `progress`: so vung nho la >4000, in tien do lam
            # output thanh 20 dong rac cho moi vtable ma khong them gi thong tin.
            hits = scan(h, pat, max_hits=16)
            print('  %d dia chi (%.1fs)' % (len(hits), time.time() - t0))
            for x in hits[:8]:
                d, _ = rdmem(h, x, 0x40)
                extra = ''
                if len(d) >= 0x38:
                    inner = u64(d, 0x30)
                    if inner:
                        ib, _ = rdmem(h, inner, 0x40)
                        if len(ib) >= 0x3C:
                            extra = ('  ->[+0x30]=%d [+0x38]=%d'
                                     % (u32(ib, 0x30), u32(ib, 0x38)))
                    extra += '  [+0x20]=%d' % u32(d, 0x20)
                print('    0x%X%s' % (x, extra))
    finally:
        k32.CloseHandle(h)


def cmd_read(a):
    pid = find_pid()
    if not pid:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_read(pid)
    try:
        mod = module_of(pid, a.addr)
        print('0x%X  %s' % (a.addr, mod or '(khong ro module)'))
        data, got = rdmem(h, a.addr, a.size)
        print('doc %d byte' % got)
        print(hexdump(a.addr, data))
    finally:
        k32.CloseHandle(h)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('find', help='quet mot dia chi vtable')
    p.add_argument('addr', type=lambda s: int(s, 0))
    p.add_argument('--limit', type=int, default=32)
    p.set_defaults(fn=cmd_find)

    p = sub.add_parser('obj', help='dump byte quanh mot con tro')
    p.add_argument('addr', type=lambda s: int(s, 0))
    p.add_argument('--size', type=lambda s: int(s, 0), default=0x70)
    p.set_defaults(fn=cmd_obj)

    p = sub.add_parser('peak', help='doc so ban ghi peak tu RAM')
    p.add_argument('addr', type=lambda s: int(s, 0))
    p.set_defaults(fn=cmd_peak)

    p = sub.add_parser('probe', help='quet ca 4 vtable AudioImage')
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser('read', help='doc dia chi bat ky')
    p.add_argument('addr', type=lambda s: int(s, 0))
    p.add_argument('size', type=lambda s: int(s, 0), default=64)
    p.set_defaults(fn=cmd_read)

    a = ap.parse_args()
    if struct.calcsize('P') != 8:
        sys.exit('LOI: can Python 64 bit.')
    set_prototypes()
    a.fn(a)


if __name__ == '__main__':
    main()
