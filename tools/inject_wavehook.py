#!/usr/bin/env python3
"""Nap `hook\\wavehook.dll` vao tien trinh Cubase15.exe, va goi ham export.

Khong dung thu vien ngoai. Chi can `ctypes` + `kernel32`.

    python tools\\inject_wavehook.py status
    python tools\\inject_wavehook.py load
    python tools\\inject_wavehook.py unload
    python tools\\inject_wavehook.py calls

Vi sao phai can than
--------------------
1. Cubase 15 64 bit, nen `ctypes` phai dung con tro 64 bit. Khoi tao
   `c_void_p` mac dinh da la 64 bit tren Python 64 bit, nhung de bao dam
   thi kiem tra `struct.calcsize('P') == 8` va tu choi neu khong.
2. LoadLibrary phai chay TRONG tien trinh Cubase. Tren Windows khong co
   "inject" that nghĩa tai lý - phai dung `CreateRemoteThread` chay
   `LoadLibraryW` cua chinh tien trinh do. Do la kỹ thuật chuan cho
   plugin dung cho MOT tieng trinh, khong phai virus: no chi nap mot
   DLL vao mot PID ma nguoi dung vua khai bao.
3. `unload` go `FreeLibrary`. Nhung ma trong bo nho da ghi de van con lai
   nen DLL khong tu goi `WaveHook_Remove` khi bi unload. Do do `unload`
   goi `WaveHook_Remove` TRUOC, roi moi `FreeLibrary`. Bo qua buoc nay
   thi Cubase se crash.
"""
import argparse
import ctypes
import os
import struct
import sys
import time
from ctypes import wintypes
from pathlib import Path

k32 = ctypes.WinDLL('kernel32', use_last_error=True)

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION      = 0x0008
PROCESS_VM_READ           = 0x0010
PROCESS_VM_WRITE          = 0x0020
PROCESS_CREATE_THREAD     = 0x0002

MEM_COMMIT  = 0x1000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000
PAGE_RW     = 0x04

TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE  = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010

RVA_WAVE_DRAW = 0x1E9AD10
# 15 byte dau ham to dải song 0x1E9AD10:
#   mov [rsp+8], rbx    (5 byte: 48 89 5C 24 08)
#   mov [rsp+10h], rsi  (5 byte: 48 89 74 24 10)
#   mov [rsp+18h], rdi  (5 byte: 48 89 7C 24 18)
PROLOGUE_SIZE = 15
EXPECTED_PROLOGUE = bytes((0x48, 0x89, 0x5C, 0x24, 0x08,         # mov [rsp+8], rbx
                           0x48, 0x89, 0x74, 0x24, 0x10,         # mov [rsp+10h], rsi
                           0x48, 0x89, 0x7C, 0x24, 0x18))        # mov [rsp+18h], rdi

DLL = Path(__file__).resolve().parent.parent / 'hook' / 'wavehook.dll'
EXE = Path(r'E:\Steinberg\Cubase 15\Cubase15.exe')
LOG = Path(__file__).resolve().parent.parent / 'hook' / 'wavehook.log'


class MODULEENTRY32(ctypes.Structure):
    # `modBaseAddr` phai la so 64 bit CO CANH CHINH 8 byte. Neu khai bao
    # no la `c_byte * 8` (canh 1 byte) thi struct lech, va Toolhelp tra
    # ERROR_BAD_LENGTH (24) ma khong bao gi ca. Day la loai canh bi can
    # rat de bo qua trong ctypes.
    _fields_ = [
        ('dwSize', wintypes.DWORD), ('th32ModuleID', wintypes.DWORD),
        ('th32ProcessID', wintypes.DWORD), ('GlblcntUsage', wintypes.DWORD),
        ('ProccntUsage', wintypes.DWORD), ('modBaseAddr', ctypes.c_uint64),
        ('modBaseSize', wintypes.DWORD), ('hModule', wintypes.HMODULE),
        ('szModule', ctypes.c_char * 256), ('szExePath', ctypes.c_char * 260),
    ]

    def base(self):
        return int(self.modBaseAddr)


class PROCESSENTRY32(ctypes.Structure):
    # STRUCT NAY PACKED 4 BYTE, KHONG PHAI 8.
    #
    # `th32DefaultHeapID` la ULONG_PTR (8 byte) nhung nam o offset 12 - tuc
    # la ngay sau `th32ProcessID`, khong co khoang dem cho canh 8. Neu de
    # mac dinh canh 8, ten tien trinh se bi doc o offset 52 thay vi 44, ra
    # chuoi cat ngan ("Process]" thay vi "System Process"), va vong duyet
    # khong tim thay Cubase.
    #
    # Cach kiem chung: doc struct tho, `szExeFile` phai bat dau bang chu
    # cai dau cua ten tien trinh dau tien.
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


def say(msg):
    print(msg, flush=True)


def check_bitness():
    if struct.calcsize('P') != 8:
        sys.exit('LOI: can Python 64 bit de dieu khien Cubase 64 bit.')


def set_prototypes():
    """Khai bao chu ky cua cac ham Win32. KHONG bo qua buoc nay.

    `ctypes` mac dinh coi ham tra ve `int` - 32 bit. Dia chi khu vuc do
    Windows cap tren Windows 64 bit la 64 bit, nen gia tri bi cat ngan,
    `WriteProcessMemory` nhan dia chi sai va tra loi
    "Invalid access to memory location" (WinError 998). Moi ham tra ve con
    tro hoac handle deu phai khai bao `restype` la con tro 64 bit.
    """
    P = ctypes.c_void_p
    H = wintypes.HANDLE
    D = wintypes.DWORD

    k32.OpenProcess.restype = H
    k32.OpenProcess.argtypes = [D, wintypes.BOOL, D]
    k32.CloseHandle.restype = wintypes.BOOL
    k32.CloseHandle.argtypes = [H]
    k32.VirtualAllocEx.restype = P
    k32.VirtualAllocEx.argtypes = [H, P, ctypes.c_size_t, D, D]
    k32.VirtualFreeEx.restype = wintypes.BOOL
    k32.VirtualFreeEx.argtypes = [H, P, ctypes.c_size_t, D]
    k32.ReadProcessMemory.restype = wintypes.BOOL
    k32.ReadProcessMemory.argtypes = [H, P, P, ctypes.c_size_t,
                                      ctypes.POINTER(ctypes.c_size_t)]
    k32.WriteProcessMemory.restype = wintypes.BOOL
    k32.WriteProcessMemory.argtypes = [H, P, P, ctypes.c_size_t,
                                       ctypes.POINTER(ctypes.c_size_t)]
    k32.CreateRemoteThread.restype = H
    k32.CreateRemoteThread.argtypes = [H, P, ctypes.c_size_t, P, P, D, P]
    k32.WaitForSingleObject.restype = D
    k32.WaitForSingleObject.argtypes = [H, D]
    k32.GetExitCodeThread.restype = wintypes.BOOL
    k32.GetExitCodeThread.argtypes = [H, ctypes.POINTER(D)]
    k32.GetModuleHandleW.restype = H
    k32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    k32.GetProcAddress.restype = P
    k32.GetProcAddress.argtypes = [H, ctypes.c_char_p]
    k32.CreateToolhelp32Snapshot.restype = H
    k32.CreateToolhelp32Snapshot.argtypes = [D, D]
    k32.Process32First.restype = wintypes.BOOL
    k32.Process32First.argtypes = [H, ctypes.c_void_p]
    k32.Process32Next.restype = wintypes.BOOL
    k32.Process32Next.argtypes = [H, ctypes.c_void_p]
    k32.Module32First.restype = wintypes.BOOL
    k32.Module32First.argtypes = [H, ctypes.c_void_p]
    k32.Module32Next.restype = wintypes.BOOL
    k32.Module32Next.argtypes = [H, ctypes.c_void_p]


def find_cubase_pid():
    """PID cua Cubase15.exe, hoac None."""
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        e = PROCESSENTRY32()
        e.dwSize = ctypes.sizeof(e)
        found = None
        ok = k32.Process32First(snap, ctypes.byref(e))
        while ok:
            if e.szExeFile.decode(errors='replace').lower() == 'cubase15.exe':
                found = e.th32ProcessID
                break
            ok = k32.Process32Next(snap, ctypes.byref(e))
        return found
    finally:
        k32.CloseHandle(snap)


def module_base(pid, name='Cubase15.exe'):
    """Module base va handle cua `name` trong tien trinh `pid`, hoac (None,None)."""
    snap = k32.CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        e = MODULEENTRY32()
        e.dwSize = ctypes.sizeof(e)
        ok = k32.Module32First(snap, ctypes.byref(e))
        while ok:
            if e.szModule.decode(errors='replace').lower() == name.lower():
                return e.base(), e.hModule
            ok = k32.Module32Next(snap, ctypes.byref(e))
        return None, None
    finally:
        k32.CloseHandle(snap)


def open_proc(pid):
    h = k32.OpenProcess(
        PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION |
        PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE, False, pid)
    if not h:
        raise ctypes.WinError(ctypes.get_last_error())
    return h


def find_export(pid, func):
    """Dia chi cua export trong DLL da nap.

    Base module lay theo TEN FILE cua `DLL` (khong phai ten hard-code):
    `load()` co the nap nhieu ban (wavehook.dll cu, wavehook2.dll moi) vao
    cung mot tien trinh. Neu lay base cua module nao khong thi dia chi
    tinh ra se nam giua hai module - go vao do la chet ngay. Da xay ra
    dung mot lan: minidump ghi RIP = RVA cua ham trong file moi, nhung lai
    nam trong vung cua file cu.
    """
    modname = DLL.name
    base, _h = module_base(pid, modname)
    if base is None:
        return None

    from cubelib.pe import PE
    pe = PE(str(DLL))
    # Ten trong DATA_DIRS la 'Export' (viet hoa chu E), khong phai 'EXPORT'.
    exp_rva, exp_size = pe.data_dir('Export')
    if not exp_rva:
        return None

    d = pe.bin.data

    def u32(rva):
        return struct.unpack_from('<I', d, pe.rva_to_off(rva))[0]

    def u16(rva):
        return struct.unpack_from('<H', d, pe.rva_to_off(rva))[0]

    def cstr(rva):
        o = pe.rva_to_off(rva)
        out = bytearray()
        while d[o + len(out)] != 0:          # `d` la mmap, khong co .index
            out.append(d[o + len(out)])
        return bytes(out).decode(errors='replace')

    # IMAGE_EXPORT_DIRECTORY, 40 byte:
    #  12 Name RVA | 16 OrdinalBase | 20 NumberOfFunctions
    #  24 NumberOfNames | 28 ExportAddressTable | 32 NamePointerTable
    #  36 OrdinalTable
    n_funcs = u32(exp_rva + 20)
    n_names = u32(exp_rva + 24)
    addr_tbl = u32(exp_rva + 28)
    name_tbl = u32(exp_rva + 32)
    ord_tbl = u32(exp_rva + 36)

    for i in range(n_names):
        if cstr(u32(name_tbl + 4 * i)) != func:
            continue
        # OrdinalTable cho chi so vao ExportAddressTable, khong phai
        # ordinal thuc - cai sau moi cong them OrdinalBase.
        fn_rva = u32(addr_tbl + 4 * u16(ord_tbl + 2 * i))
        if fn_rva == 0 or fn_rva & 0x8000_0000:     # 0 hoac forwarder
            return None
        addr = base + fn_rva
        # Kiem tra lan cuoi: dia chi phai nam trong dung module do. Neu
        # inject theo duong dan nao khac nhung module dang tim la ten khac,
        # phep nay chan ngay thay vi gọi vao bo nho rác.
        if not (base <= addr < base + 0x01000000):
            raise SystemExit(
                f'LOI: {func} tinh ra 0x{addr:X} nam ngoai module {modname} '
                f'(base 0x{base:X}). Co the DLL tren dia khac ban file.')
        return addr
    return None


def read_mem(h, addr, n):
    buf = (ctypes.c_char * n)()
    got = ctypes.c_size_t()
    if not k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, n,
                                ctypes.byref(got)):
        raise ctypes.WinError(ctypes.get_last_error())
    return bytes(buf[:got.value])


def write_mem(h, addr, data):
    buf = ctypes.create_string_buffer(data, len(data))
    got = ctypes.c_size_t()
    if not k32.WriteProcessMemory(h, ctypes.c_void_p(addr), buf, len(data),
                                   ctypes.byref(got)):
        raise ctypes.WinError(ctypes.get_last_error())


def remote_call(h, addr, arg=0):
    t = k32.CreateRemoteThread(h, None, 0, ctypes.c_void_p(addr),
                               ctypes.c_void_p(arg), 0, None)
    if not t:
        raise ctypes.WinError(ctypes.get_last_error())
    k32.WaitForSingleObject(t, 10000)
    code = wintypes.DWORD()
    k32.GetExitCodeThread(t, ctypes.byref(code))
    k32.CloseHandle(t)
    return code.value


def load(install=True):
    """Nap DLL vao Cubase. `install=False` chi nap, khong gan hook.

    Dung `install=False` khi chay bo dem: gan ca hook don le o 0x1E9E140 lan
    hook 29 diem cung luc se tang rui ro ma khong them gi cho phep do.
    """
    if not DLL.exists():
        sys.exit(f'LOI: khong co {DLL}. Chay hook\\build.bat truoc.')
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    say(f'Cubase15.exe pid={pid}')

    h = open_proc(pid)
    try:
        base, _ = module_base(pid)
        say(f'  ImageBase = 0x{base:X}')

        # Kiem tra prologue DUNG chua truoc khi nap: dung ban Cubase khac
        # thi DLL tu choi ghi de, va ta bao ro ngay.
        pro = read_mem(h, base + RVA_WAVE_DRAW, PROLOGUE_SIZE)
        if pro != EXPECTED_PROLOGUE:
            say(f'  CANH BAO: {PROLOGUE_SIZE} byte dau ham ve khong dung ban biet.')
            say(f'    doi mon: {pro.hex(" ")}')
            say(f'    mong doi: {EXPECTED_PROLOGUE.hex(" ")}')
            say('  Van nap - DLL se tu kiem tra lai truoc khi ghi de.')
        else:
            say(f'  prologue 0x{RVA_WAVE_DRAW:X} dung nhu da RE '
                f'({PROLOGUE_SIZE} byte)')

        # LoadLibraryW trong tien trinh dich
        rva = k32.GetProcAddress(
            k32.GetModuleHandleW('kernel32.dll'), b'LoadLibraryW')
        if not rva:
            raise ctypes.WinError(ctypes.get_last_error())

        path = str(DLL)
        nbytes = (len(path) + 1) * 2
        remote = k32.VirtualAllocEx(h, None, nbytes, MEM_COMMIT | MEM_RESERVE,
                                    PAGE_RW)
        if not remote:
            raise ctypes.WinError(ctypes.get_last_error())
        write_mem(h, remote, path.encode('utf-16-le'))
        remote_call(h, rva, remote)
        k32.VirtualFreeEx(h, ctypes.c_void_p(remote), ctypes.c_size_t(0),
                          MEM_RELEASE)

        time.sleep(0.3)
        dbase, _ = module_base(pid, DLL.name)
        if dbase is None:
            sys.exit(f'LOI: {DLL.name} khong nap duoc.')
        say(f'  {DLL.name} da nap, base = 0x{dbase:X}')

        if not install:
            return

        # LoadLibrary CHI nap DLL, chua gan hook - `DllMain` khong lam viec
        # nay (va cung khong nen). Phai goi `WaveHook_Install` rieng.
        k32.CloseHandle(h)
        h = open_proc(pid)
        code = remote_call(h, find_export(pid, 'WaveHook_Install'))
        say(f'  WaveHook_Install -> {code}  (1 = thanh cong)')
        if code != 1:
            say('  DLL khong gan duoc (byte prologue khong khop, hoac RVA '
                'nam ngoai module).')
            step = find_export(pid, 'g_step')
            if step:
                g = struct.unpack('<i', read_mem(h, step, 4))[0]
                say(f'  g_step = {g}  '
                    f'(2 = het kiem tra byte, -1 = ham khong canh 8 byte)')
            sys.exit(1)
    finally:
        k32.CloseHandle(h)


def call_export(func, expect=None):
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_proc(pid)
    try:
        addr = find_export(pid, func)
        if addr is None:
            sys.exit(f'LOI: khong tim thay export {func} trong tien trinh.')
        say(f'  {func} @ 0x{addr:X}')
        code = remote_call(h, addr)
        say(f'  tra ve {code}')
        if expect is not None and code != expect:
            sys.exit(f'LOI: {func} tra ve {code}, mong doi {expect}. '
                     f'Xem {LOG} neu co.')
        return code
    finally:
        k32.CloseHandle(h)


def probe():
    """In ket qua probe device ma DLL da ghi ra file.

    DLL tu ghi `%TEMP%\\waveprobe.txt` ngay trong lan ve dau tien, nen lenh
    nay chi doc lai - khong can goi ham nao co hai tham so, va khong can
    sua byte nao trong tien trinh Cubase dang chay.
    """
    path = Path(os.environ.get('TEMP', '.')) / 'waveprobe.txt'
    if not path.exists():
        say(f'Chua co {path}.')
        say('Nghia la hook chua chay lan nao - Cubase chua ve duong song.')
        say('Hay mo mot project co audio trong Project Window roi chay lai.')
        return
    say(f'--- {path} ---')
    say(path.read_text(errors='replace'))


def status():
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        say('Cubase15.exe khong chay.')
        return
    base, _ = module_base(pid)
    say(f'Cubase15.exe pid={pid}  ImageBase 0x{base:X}')
    dbase, _ = module_base(pid, DLL.name)
    if dbase is None:
        say(f'  {DLL.name}: CHUA nap')
    else:
        say(f'  {DLL.name}: da nap, base 0x{dbase:X}')
    h = open_proc(pid)
    try:
        pro = read_mem(h, base + RVA_WAVE_DRAW, PROLOGUE_SIZE)
        if pro[:2] == b'\x49\xBB' and pro[10:13] == b'\x41\xFF\xE3':
            dest = struct.unpack_from('<Q', pro, 2)[0]
            say(f'  0x{RVA_WAVE_DRAW:X}: DA HOOK (JMP tuyet doi -> 0x{dest:X})')
        elif pro == EXPECTED_PROLOGUE:
            say(f'  0x{RVA_WAVE_DRAW:X}: chua hook ({PROLOGUE_SIZE} byte prologue goc)')
        else:
            say(f'  0x{RVA_WAVE_DRAW:X}: KHONG HOP - {pro.hex(" ")}')
            say(f'  {"mong doi":<20} {EXPECTED_PROLOGUE.hex(" ")}')
    finally:
        k32.CloseHandle(h)


def calls():
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_proc(pid)
    try:
        addr = find_export(pid, 'g_callCount')
        if addr is None:
            addr = find_export(pid, 'WaveColour_Reset')
        if addr is None:
            say('khong doc duoc bien dem (co the DLL chua duoc bien dich '
                'voi -Zi). Bo qua.')
            return
        raw = read_mem(h, addr, 4)
        say(f'g_callCount = {struct.unpack("<i", raw)[0]}')
    finally:
        k32.CloseHandle(h)


def safe_prologue_rvas(exe):
    """Moi ham co 15 byte prologue AN TOAN de hook.

    15 byte do la 4 lenh chi doi thoat so:
        mov rax, rsp / mov [rax+20h], r9 / mov [rax+18h], r8 / mov [rax+10h], rdx
    Chung khong dung dia chi RIP-relative nen copy sang dia chi khac van
    chay dung, va 15 la diem dung lenh nen co the ghi de ca 15 byte.

    Toan bo Cubase15.exe chi co 29 ham dang do, nen day la tap ung vien
    nho de do xem duong ve duong song di qua ham nao.
    """
    from cubelib.pe import PE
    pe = PE(exe)
    safe = EXPECTED_PROLOGUE
    d = pe.bin.data
    out = []
    for beg, _end in pe.functions():
        off = pe.rva_to_off(beg)
        if off is None:
            continue
        if bytes(d[off:off + len(safe)]) == safe:
            out.append(beg)
    return out


def probe_install():
    """Gan bo dem vao moi ham co prologue an toan, roi in ket qua dem."""
    check_bitness()
    if not DLL.exists():
        sys.exit(f'LOI: khong co {DLL}. Chay hook\\build.bat truoc.')
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    say(f'Cubase15.exe pid={pid}')

    rvas = safe_prologue_rvas(EXE)
    say(f'  {len(rvas)} ham co prologue 15 byte an toan')

    load(install=False)         # chi nap DLL, KHONG gan hook don le

    h = open_proc(pid)
    try:
        # Khoi `ProbeTargets`: 4 byte so phan tu, roi cac RVA. So phan tu va
        # danh sach phai cung mot khoi vi `CreateRemoteThread` chi truyen
        # duoc MOT tham so.
        blob = struct.pack('<I', len(rvas))
        blob += b''.join(struct.pack('<I', r) for r in rvas)
        remote = k32.VirtualAllocEx(h, None, len(blob), MEM_COMMIT | MEM_RESERVE,
                                    PAGE_RW)
        if not remote:
            raise ctypes.WinError(ctypes.get_last_error())
        write_mem(h, remote, blob)

        fn = find_export(pid, 'WaveProbe_InstallAll')
        if fn is None:
            sys.exit('LOI: DLL thieu export WaveProbe_InstallAll. '
                     'Bien dich lai hook/build.bat.')
        code = remote_call(h, fn, remote)
        say(f'  WaveProbe_InstallAll -> {code}  (so diem da gan)')
        if code <= 0:
            sys.exit('LOI: khong gan duoc diem nao. '
                     'Neu van la 0, kiem tra so phan tu co dung khong.')

        cc = find_export(pid, 'g_probeCount')
        time.sleep(0.5)
        say('\n  dem ngay luc moi gan:')
        for i, rva in enumerate(rvas):
            c = struct.unpack('<i', read_mem(h, cc + 4 * i, 4))[0]
            if c:
                say(f'    [{i:>2}] RVA 0x{rva:X}  = {c}')
    finally:
        k32.CloseHandle(h)


def probe_counts(label='dem'):
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    rvas = safe_prologue_rvas(EXE)
    h = open_proc(pid)
    try:
        cc = find_export(pid, 'g_probeCount')
        a0 = find_export(pid, 'g_probeArg0')
        say(f'  {label}:')
        rows = []
        for i, rva in enumerate(rvas):
            c = struct.unpack('<i', read_mem(h, cc + 4 * i, 4))[0]
            if c:
                arg = struct.unpack('<Q', read_mem(h, a0 + 8 * i, 8))[0]
                rows.append((c, rva, arg))
        if not rows:
            say('    (chua diem nao chay)')
        for c, rva, arg in sorted(rows, reverse=True):
            say(f'    RVA 0x{rva:X}  dem={c:<10} arg0=0x{arg:X}')
    finally:
        k32.CloseHandle(h)


def probe_remove():
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_proc(pid)
    try:
        fn = find_export(pid, 'WaveProbe_RemoveAll')
        if fn is None:
            say('  (bo dem chua duoc gan)')
            return
        code = remote_call(h, fn)
        say(f'  WaveProbe_RemoveAll -> {code}  (so diem da go)')
    finally:
        k32.CloseHandle(h)


def set_colormode(mode):
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_proc(pid)
    try:
        addr = find_export(pid, 'WaveHook_SetColorMode')
        if addr is None:
            sys.exit('LOI: khong tim thay export WaveHook_SetColorMode. DLL chua duoc nap?')
        say(f'  Dat ColorMode = {mode}...')
        remote_call(h, addr, mode)
        say('  Thanh cong!')
    finally:
        k32.CloseHandle(h)


def get_color_info():
    check_bitness()
    pid = find_cubase_pid()
    if pid is None:
        sys.exit('LOI: Cubase15.exe khong chay.')
    h = open_proc(pid)
    try:
        addr_mode = find_export(pid, 'g_colorMode')
        addr_color = find_export(pid, 'g_lastColorRGB')
        mode_names = {
            0: "0 (PASSTHROUGH - Mau goc Cubase)",
            1: "1 (FL_MULTIBAND - Mau dong FL Studio theo pho)",
            2: "2 (FL_NEON_BLUE - Xanh lam neon FL Playlist)",
            3: "3 (FL_ORANGE - Cam ruc ro FL Beat)",
            4: "4 (FL_CYAN - Xanh ngoc glow)",
            5: "5 (CUSTOM - Mau tuy chinh)"
        }
        if addr_mode:
            m = struct.unpack('<i', read_mem(h, addr_mode, 4))[0]
            say(f'  Color Mode: {mode_names.get(m, str(m))}')
        if addr_color:
            rgb = struct.unpack('<I', read_mem(h, addr_color, 4))[0]
            r = (rgb >> 16) & 0xFF
            g = (rgb >> 8) & 0xFF
            b = rgb & 0xFF
            say(f'  Mau FL ve gan nhat (RGB): ({r}, {g}, {b})')
    finally:
        k32.CloseHandle(h)


def main():
    global DLL
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['load', 'unload', 'status', 'calls',
                                    'probe', 'probecount', 'proberemove',
                                    'devdump', 'colormode', 'color'])
    ap.add_argument('val', nargs='?', type=int, help='Gia tri cho colormode (0..5)')
    ap.add_argument('--dll', help='duong dan DLL thay the (mac dinh '
                                  'hook/wavehook.dll). Dung khi ban cu dang '
                                  'nap trong Cubase nen khong ghi de duoc.')
    a = ap.parse_args()
    check_bitness()
    set_prototypes()
    if a.dll:
        # Phai la duong dan TUYET DOI. `LoadLibraryW` chay trong tien trinh
        # Cubase nen duong dan tuong doi duoc giai theo thu muc lam viec CUA
        # CUA NO, khong phai thu muc hien tai cua ta - nap that bai va im
        # lang khong bao loi gi.
        DLL = Path(a.dll).resolve()

    if a.cmd == 'load':
        load()
    elif a.cmd == 'unload':
        # Phai goi Remove TRUOC FreeLibrary, xem doan doc dau file.
        call_export('WaveHook_Remove', expect=1)
        call_export('FreeLibrary', expect=0)
    elif a.cmd == 'status':
        status()
    elif a.cmd == 'calls':
        calls()
    elif a.cmd == 'devdump':
        probe()
    elif a.cmd == 'probe':
        probe_install()
    elif a.cmd == 'probecount':
        probe_counts('so lan goi')
    elif a.cmd == 'proberemove':
        probe_remove()
    elif a.cmd == 'colormode':
        if a.val is None:
            sys.exit('Can truyen gia tri mode: 0 (Pass), 1 (FL Multiband), 2 (Neon Blue), 3 (Orange), 4 (Cyan)')
        set_colormode(a.val)
    elif a.cmd == 'color':
        get_color_info()


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
