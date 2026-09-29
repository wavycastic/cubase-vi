#!/usr/bin/env python3
"""Launch Cubase, then read the live value of the global path string that
translator.cpp uses to build '<path>/translation.xml'. Prints the directory."""
import ctypes, ctypes.wintypes as wt, struct, subprocess, sys, time, os

EXE = r'E:\Steinberg\Cubase 15\Cubase15.exe'
GLOBAL_FILEOFF = 0x77AE990
STR_OFF = 0x40

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

# ---- compute RVA of the global from the file layout ----
raw = open(EXE, 'rb').read()
e_lfanew = struct.unpack_from('<I', raw, 0x3C)[0]
coff = e_lfanew + 4
_, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', raw, coff)
opt = coff + 20
secoff = opt + optsz
def off2rva(off):
    for i in range(nsec):
        o = secoff + i*40
        vsz, va, rsz, ptr = struct.unpack_from('<IIII', raw, o+8)
        if ptr <= off < ptr + rsz:
            return va + (off - ptr)
    return None

RVA_GLOBAL = off2rva(GLOBAL_FILEOFF)
RVA_STR = RVA_GLOBAL + STR_OFF
print(f'global  fileoff 0x{GLOBAL_FILEOFF:X} -> RVA 0x{RVA_GLOBAL:X}')
print(f'string  RVA 0x{RVA_STR:X}')

TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
class MODULEENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', wt.DWORD), ('th32ModuleID', wt.DWORD),
                ('th32ProcessID', wt.DWORD), ('GlblcntUsage', wt.DWORD),
                ('ProccntUsage', wt.DWORD), ('modBaseAddr', ctypes.POINTER(ctypes.c_byte)),
                ('modBaseSize', wt.DWORD), ('hModule', wt.HMODULE),
                ('szModule', wt.WCHAR*256), ('szExePath', wt.WCHAR*260)]
k32.CreateToolhelp32Snapshot.restype = wt.HANDLE
k32.Module32FirstW.restype = wt.BOOL
k32.Module32NextW.restype = wt.BOOL

def module_base(pid, exe):
    h = k32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    me = MODULEENTRY32(); me.dwSize = ctypes.sizeof(MODULEENTRY32)
    base = None
    if k32.Module32FirstW(h, ctypes.byref(me)):
        while True:
            if me.szExePath.lower() == exe.lower():
                base = ctypes.cast(me.modBaseAddr, ctypes.c_void_p).value
                break
            if not k32.Module32NextW(h, ctypes.byref(me)):
                break
    k32.CloseHandle(h)
    return base

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

def readmem(h, addr, size):
    buf = ctypes.create_string_buffer(size)
    n = ctypes.c_size_t()
    if not k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, size, ctypes.byref(n)):
        raise ctypes.WinError(ctypes.get_last_error())
    return buf.raw[:n.value]

def try_read(h, addr, size):
    """Read, tolerating a partially-mapped range by falling back to 8-byte chunks."""
    try:
        d = readmem(h, addr, size)
        if len(d) == size:
            return d
    except Exception:
        pass
    out = b''
    for i in range(0, size, 8):
        try:
            out += readmem(h, addr + i, 8)
        except Exception:
            out += b'\0' * 8
    return out

print('\nlaunching Cubase ...')
p = subprocess.Popen([EXE])
pid = p.pid
print(f'  pid={pid}')

base = None
for _ in range(60):
    time.sleep(1)
    if p.poll() is not None:
        print(f'  process exited early with code {p.returncode}')
        sys.exit(1)
    try:
        base = module_base(pid, EXE)
    except Exception:
        base = None
    if base:
        break
print(f'  module base = 0x{base:X}')

# give it time to finish early initialisation
for wait in (5, 10, 20, 30):
    time.sleep(wait if wait == 5 else wait - prev) if False else None
    break
time.sleep(8)

h = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
if not h:
    print('OpenProcess failed:', ctypes.get_last_error())
    sys.exit(1)

addr = base + RVA_STR
print(f'\nreading std::wstring struct at 0x{addr:X}')
data = try_read(h, addr, 32)
print(f'  raw: {data.hex()}')
ptr, size, cap = struct.unpack('<QQQ', data)
print(f'  ptr=0x{ptr:X}  size={size}  cap={cap}')

if cap == 0xF:
    print(f'  SSO -> inline data: {data[16:32].decode("utf-16-le","replace").split(chr(0))[0]!r}')
else:
    try:
        s = readmem(h, ptr, min(size, 1024))
        txt = s.decode('utf-16-le', 'replace').split('\x00')[0]
        print(f'  PATH = {txt!r}')
        print(f'  -> candidate: {txt}\\{os.path.basename("translation.xml")}')
    except Exception as e:
        print('  failed to deref:', e)

k32.CloseHandle(h)
try:
    p.terminate(); p.wait(timeout=15)
except Exception:
    p.kill()
print('\nterminated Cubase')
