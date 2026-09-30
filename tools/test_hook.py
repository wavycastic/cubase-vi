#!/usr/bin/env python3
"""Kiem chung hook tren MOT tien trinh thu nghiem, khong phai Cubase that.

Ky thuat: ta bien dich mot file .exe nho co ham ve song gia lap, co dung 7
byte prologue cua Cubase, roi nap `hook\\wavehook.dll` vao va goi
`WaveHook_InstallAt`. Cach nay kiem duoc toan bo duong ghi de byte,
trampoline va khop lai ma KHONG de vao tinh trang cua Cubase - neu hook
sai byte, chi co process thu nghiem chet.

Chay:
    python tools\\test_hook.py run
"""
import ctypes
import struct
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = ROOT / 'build' / 'hooktest'
DLL = ROOT / 'hook' / 'wavehook.dll'

# 15 byte dau ma Cubase that co - 4 lenh chi doi thoat so. DLL kiem tra
# dung 15 byte nay, nen ham thu nghiem phai co y het (xem ASM_SOURCE).
PATCH_SIZE = 15
FAKE_PROLOGUE = bytes((0x48, 0x8B, 0xC4,          # mov rax, rsp
                       0x4C, 0x89, 0x48, 0x20,     # mov [rax+20h], r9
                       0x4C, 0x89, 0x40, 0x18,     # mov [rax+18h], r8
                       0x48, 0x89, 0x50, 0x10))    # mov [rax+10h], rdx

C_SOURCE = r'''
/* Process thu nghiem: vong lap goi ham ve song gia lap trong mot luong.
 *
 * File nay KHONG dung `__asm`: MSVC x64 khong ho tro inline asm (chi co o
 * x86), nen 7 byte prologue do MASM sinh ra xem ASM_SOURCE ben canh.
 */
#include <windows.h>
#include <stdio.h>

__declspec(dllexport) void target_draw(void);
__declspec(dllexport) void go_target(void);

__declspec(dllexport) void go_target(void)
{
    target_draw();
}

/* Bat loi va ghi ra dia chi. Khong co buoc nay thi process chet im lang
 * va chi con lai ma loi 0xC0000005 - khong biet hook loi cho. */
static void ghi_loi(EXCEPTION_POINTERS *ep)
{
    char buf[512];
    DWORD n;
    HANDLE f;
    CONTEXT *c = ep->ContextRecord;

    n = (DWORD)snprintf(buf, sizeof buf,
        "code=0x%08lX\n"
        "exception_address=0x%llX\n"
        "access=%s  fault_address=0x%llX\n"
        "RIP=0x%llX  RSP=0x%llX  RBP=0x%llX\n"
        "RAX=0x%llX  RBX=0x%llX  RCX=0x%llX  RDX=0x%llX\n"
        "RSI=0x%llX  RDI=0x%llX  R8 =0x%llX  R9 =0x%llX\n"
        "R10=0x%llX  R11=0x%llX  R12=0x%llX  R13=0x%llX\n"
        "R14=0x%llX  R15=0x%llX\n",
        (unsigned long)ep->ExceptionRecord->ExceptionCode,
        (unsigned long long)ep->ExceptionRecord->ExceptionAddress,
        ep->ExceptionRecord->NumberParameters >= 2
            ? (ep->ExceptionRecord->ExceptionInformation[0] == 0 ? "DOC"
             : ep->ExceptionRecord->ExceptionInformation[0] == 1 ? "GHI"
             : "THUC THI") : "?",
        (unsigned long long)(ep->ExceptionRecord->NumberParameters >= 2
                             ? ep->ExceptionRecord->ExceptionInformation[1] : 0),
        (unsigned long long)c->Rip, (unsigned long long)c->Rsp,
        (unsigned long long)c->Rbp,
        (unsigned long long)c->Rax, (unsigned long long)c->Rbx,
        (unsigned long long)c->Rcx, (unsigned long long)c->Rdx,
        (unsigned long long)c->Rsi, (unsigned long long)c->Rdi,
        (unsigned long long)c->R8,  (unsigned long long)c->R9,
        (unsigned long long)c->R10, (unsigned long long)c->R11,
        (unsigned long long)c->R12, (unsigned long long)c->R13,
        (unsigned long long)c->R14, (unsigned long long)c->R15);

    f = CreateFileA("hooktest-crash.txt", GENERIC_WRITE, 0, NULL,
                   CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (f != INVALID_HANDLE_VALUE) {
        DWORD w;
        WriteFile(f, buf, n, &w, NULL);
        CloseHandle(f);
    }
    ExitProcess(0xEE);
}

static DWORD WINAPI spin_thread(LPVOID p)
{
    (void)p;
    for (;;) {
        __try {
            go_target();
        } __except (ghi_loi(GetExceptionInformation()),
                     EXCEPTION_EXECUTE_HANDLER) {
            return 1;
        }
        Sleep(1);
    }
    return 0;
}

int main(void)
{
    CreateThread(NULL, 0, spin_thread, NULL, 0, NULL);
    for (;;)
        Sleep(1000);
    return 0;
}
'''

ASM_SOURCE = r'''
; target_draw - 15 byte dau GION HET ham ve song cua Cubase.
;
; DLL kiem tra 15 byte nay truoc khi ghi de, nen file thu nghiem phai co
; DUNG 15 byte do, va 15 la diem dung lenh:
;
;   mov rax, rsp          (3)
;   mov [rax+20h], r9     (4)
;   mov [rax+18h], r8     (4)
;   mov [rax+10h], rdx    (4)
;                      = 15
;
; Cac lenh sau do chi de ham khong rong va khong bi toi uu hoa mat.
;
; Ham nay nam o section binh thuong, khong can RVA co dinh: injector goi
; `WaveHook_InstallAt(dia_chi_ham)` de chi dinh ham can hook, dia chi lay
; tu export table cua chinh file .exe.
;
; Da thu chuyen section sang RVA 0x1E9E140 bang `/SECTION` cua link.exe -
; khong duoc: `/SECTION:name=<dia-chi>` chi nhan khi kem it nhat mot dac
; tinh, va con phai them dac tinh thi lien khong. Do do cach dung la truyen
; dia chi ham vao DLL, khong chien dau voi linker.
_TEXT SEGMENT

PUBLIC target_draw
target_draw PROC
    mov     rax, rsp                 ; 48 8B C4
    mov     [rax+20h], r9            ; 4C 89 48 20
    mov     [rax+18h], r8            ; 4C 89 40 18
    mov     [rax+10h], rdx           ; 48 89 50 10
    ; Chi con nop roi. KHONG ghi bo nho o day: `inc qword ptr [rsp+28h]`
    ; se lam dung phan tren shadow space cua chinh no, tuc la khung cua ham
    ; goi no - lam hong bien cua do. Da gap loi nay: tien trinh chet voi
    ; ma 0x80000003 (INT3) o dia chi truoc ham.
    nop
    nop
    nop
    nop
    nop
    nop
    ret
target_draw ENDP

_TEXT ENDS

END
'''


def export_rva(path, name):
    """RVA cua mot export, doc tu export table cua file PE."""
    from cubelib.pe import PE
    pe = PE(str(path))
    er, _ = pe.data_dir('Export')
    if not er:
        return None
    d = pe.bin.data
    u32 = lambda r: struct.unpack_from('<I', d, pe.rva_to_off(r))[0]
    u16 = lambda r: struct.unpack_from('<H', d, pe.rva_to_off(r))[0]

    def cs(r):
        o = pe.rva_to_off(r)
        b = bytearray()
        while d[o + len(b)]:
            b.append(d[o + len(b)])
        return bytes(b).decode()

    nn = u32(er + 24)
    at, nt, ot = u32(er + 28), u32(er + 32), u32(er + 36)
    for i in range(nn):
        if cs(u32(nt + 4 * i)) == name:
            return u32(at + 4 * u16(ot + 2 * i))
    return None


def build_target():
    import os
    BUILD.mkdir(parents=True, exist_ok=True)
    src = BUILD / 'hooktest.c'
    asm = BUILD / 'target.asm'
    # Giu nguyen tieng Viet trong chu thich
    src.write_text(C_SOURCE, encoding='utf-8')
    asm.write_text(ASM_SOURCE, encoding='utf-8')

    tools_root = Path(r'C:\Program Files (x86)\Microsoft Visual Studio'
                      r'\2022\BuildTools\VC\Tools\MSVC')
    vc = tools_root / sorted(p.name for p in tools_root.iterdir()
                             if p.is_dir())[-1]
    sdk_root = Path(r'C:\Program Files (x86)\Windows Kits\10')
    sv = sorted(p.name for p in (sdk_root / 'Include').iterdir()
                if p.is_dir())[-1]

    env = dict(os.environ)
    env['PATH'] = f'{vc / "bin" / "Hostx64" / "x64"};{env["PATH"]}'

    r = subprocess.run(['ml64.exe', '/nologo', '/c', '/I', str(vc / 'include'),
                        asm.name],
                       cwd=BUILD, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit('LOI: ml64 that bai')

    # `cl.exe` va `link.exe` la CU so 16: tach tham so bang dau nhay kinh,
    # nen truyen list co dau nhay se bi giu nguyen va thanh loi. Chay trong
    # thu muc BUILD nen chi can duong dan tuong doi.
    out = BUILD / 'hooktest.exe'
    cmd = ['cl.exe', '/nologo', '/O1', '/MT',
           f'/I{vc / "include"}',
           f'/I{sdk_root / "Include" / sv / "um"}',
           f'/I{sdk_root / "Include" / sv / "shared"}',
           src.name, 'target.obj', '/Fe:hooktest.exe',
           '/link', '/EXPORT:target_draw', '/EXPORT:go_target',
           f'/LIBPATH:{vc / "lib" / "x64"}',
           f'/LIBPATH:{sdk_root / "Lib" / sv / "ucrt" / "x64"}',
           f'/LIBPATH:{sdk_root / "Lib" / sv / "um" / "x64"}']
    r = subprocess.run(cmd, cwd=BUILD, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit('LOI: bien dich file thu nghiem that bai')
    print(f'  xong: {out.name}')

    if export_rva(out, 'target_draw') is None:
        sys.exit('LOI: file thu nghiem khong co export target_draw')
    return out


def main():
    if len(sys.argv) < 2 or sys.argv[1] != 'run':
        sys.exit(__doc__)

    sys.path.insert(0, str(HERE))
    import inject_wavehook as iw
    iw.check_bitness()
    iw.set_prototypes()

    exe = build_target()
    proc = subprocess.Popen([str(exe)])
    print(f'  process thu nghiem pid={proc.pid}')
    time.sleep(1.0)

    k32 = iw.k32
    h = None
    try:
        # -- nap DLL ------------------------------------------------
        print('\n-- nap DLL --')
        h = iw.open_proc(proc.pid)
        rva = k32.GetProcAddress(
            k32.GetModuleHandleW('kernel32.dll'), b'LoadLibraryW')
        path = str(DLL)
        n = (len(path) + 1) * 2
        rem = k32.VirtualAllocEx(h, None, n, iw.MEM_COMMIT | iw.MEM_RESERVE,
                                 iw.PAGE_RW)
        iw.write_mem(h, rem, path.encode('utf-16-le'))
        iw.remote_call(h, rva, rem)
        k32.VirtualFreeEx(h, ctypes.c_void_p(rem), ctypes.c_size_t(0),
                          iw.MEM_RELEASE)
        time.sleep(0.4)
        dbase, _ = iw.module_base(proc.pid, 'wavehook.dll')
        if not dbase:
            sys.exit('LOI: DLL khong nap duoc')
        print(f'  wavehook.dll base = 0x{dbase:X}')

        # -- tim ham can hook --------------------------------------
        tbase, _ = iw.module_base(proc.pid, 'hooktest.exe')
        if not tbase:
            sys.exit('LOI: khong thay module cua process thu nghiem')
        taddr = tbase + export_rva(exe, 'target_draw')
        print(f'  target_draw @ 0x{taddr:X}')

        # -- kiem tra prologue -------------------------------------
        pro = iw.read_mem(h, taddr, PATCH_SIZE)
        print('\n-- prologue --')
        print(f'  doc duoc : {pro.hex(" ")}')
        print(f'  mong doi : {FAKE_PROLOGUE.hex(" ")}')
        if pro != FAKE_PROLOGUE:
            sys.exit('LOI: prologue khong dung - dung ngay de sua file .asm')
        print('  khop')

        # -- dem truoc khi hook ------------------------------------
        cc = iw.find_export(proc.pid, 'g_callCount')
        before = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        time.sleep(0.5)
        during = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        print('\n-- truoc khi hook --')
        print(f'  g_callCount = {during} (luc moi nap: {before})')
        print(f'  neu bang 0 thi hook CHUA chay - dung lam moi bac')

        # -- gan hook -----------------------------------------------
        print('\n-- gan hook --')
        fn = iw.find_export(proc.pid, 'WaveHook_InstallAt')
        if fn is None:
            sys.exit('LOI: DLL thieu export WaveHook_InstallAt. '
                     'Bien dich lai hook/build.bat.')
        print(f'  WaveHook_InstallAt @ 0x{fn:X}')
        code = iw.remote_call(h, fn, taddr)
        print(f'  tra ve {code}  (1 = thanh cong)')
        step_addr = iw.find_export(proc.pid, 'g_step')
        if step_addr:
            step = struct.unpack('<i', iw.read_mem(h, step_addr, 4))[0]
            names = {0: 'chua lam gi', 1: 'da kiem tra co',
                     2: 'kiem tra byte xong', 3: 'VirtualProtect xong',
                     4: 'luu 7 byte cu xong', 5: 'lay dia chi hook xong',
                     6: 'da ghi JMP + 2 NOP', 7: 'FlushInstructionCache xong',
                     8: 'HOAN TAT'}
            print(f'  g_step = {step} ({names.get(step, "?")})')

        # Chan doan: 0xC0000005 (3221225477) nghia la ACCESS_VIOLATION.
        # Phai biet 7 byte da duoc ghi hay chua va process con song khong,
        # thi moi phan biet duoc "Install that bai" voi "hook ghi xong roi
        # stub lam chet process".
        try:
            bytes_now = iw.read_mem(h, taddr, PATCH_SIZE)
            print(f'  {PATCH_SIZE} byte ngay sau lenh go: {bytes_now.hex(" ")}')
        except OSError as e:
            print(f'  doc bo nho that bai: {e}')
            bytes_now = None
        print(f'  process con song: {proc.poll() is None}')

        # Doc dia chi trampoline ma DLL dich san. Neu con NULL thi stub se
        # nhay ve dia chi 0 va chet ngay lan dau tien co ai goi ham ve.
        cont_addr = iw.find_export(proc.pid, 'WaveDrawResumeVA')
        if cont_addr:
            cont = struct.unpack('<Q', iw.read_mem(h, cont_addr, 8))[0]
            print(f'  WaveDrawResumeVA = 0x{cont:X}  '
                  f'(mong doi 0x{taddr + PATCH_SIZE:X})')
            if cont != taddr + PATCH_SIZE:
                sys.exit('LOI: trampoline tro sai cho - stub se nhay rac')
        tr_addr = iw.find_export(proc.pid, 'WaveDrawTrampolineVA')
        if tr_addr:
            tr = struct.unpack('<Q', iw.read_mem(h, tr_addr, 8))[0]
            print(f'  WaveDrawTrampolineVA = 0x{tr:X}  '
                  f'(trong DLL: {dbase <= tr < dbase + 0x100000})')
            if not (dbase <= tr < dbase + 0x100000):
                sys.exit('LOI: stub se nhay ra ngoai DLL')

        if code != 1:
            sys.exit('LOI: hook that bai')
        if proc.poll() is not None:
            sys.exit('LOI: process chet ngay sau khi hook - stub co van de')

        time.sleep(0.5)
        if proc.poll() is not None:
            rc = proc.returncode
            print(f'  process da tho, ma loi 0x{rc & 0xFFFFFFFF:08X}')
            crash = BUILD / 'hooktest-crash.txt'
            if crash.exists():
                print('  --- chi tiet loi (do file thu nghiem ghi ra) ---')
                for ln in crash.read_text(encoding='utf-8',
                                          errors='replace').splitlines():
                    print(f'    {ln}')
                db = iw.module_base(proc.pid, 'wavehook.dll')[0]
                sys.exit(f'LOI: stub lam loi. '
                         f'(wavehook.dll base 0x{db:X})')
            sys.exit('LOI: process chet - stub lam loi luc chay')
        print('  process con song')

        after_patch = bytes_now or iw.read_mem(h, taddr, PATCH_SIZE)
        print(f'  {PATCH_SIZE} byte sau hook: {after_patch.hex(" ")}')
        # `49 BB <imm64> 41 FF E3` = mov r11, imm64 ; jmp r11
        if after_patch[:2] != b'\x49\xBB' or after_patch[10:13] != b'\x41\xFF\xE3':
            sys.exit('LOI: khong thay lenh nhay 13 byte o dau ham')
        dest = struct.unpack_from('<Q', after_patch, 2)[0]
        print(f'  JMP tuyet doi -> 0x{dest:X}')
        print(f'  nam trong wavehook.dll: '
              f'{dbase <= dest < dbase + 0x100000}')
        if not (dbase <= dest < dbase + 0x100000):
            sys.exit('LOI: JMP khong chi vao DLL')

        # -- dem sau khi hook ---------------------------------------
        n1 = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        time.sleep(0.5)
        n2 = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        print('\n-- sau khi hook --')
        print(f'  g_callCount: {n1} -> {n2} (tang {n2 - n1})')
        if n2 <= n1:
            sys.exit('LOI: hook khong chay')
        print('  hook co that su chay')

        ins = iw.remote_call(h, iw.find_export(proc.pid,
                                               'WaveHook_IsInstalled'))
        print(f'  WaveHook_IsInstalled -> {ins}  (mong doi 1)')
        if ins != 1:
            sys.exit('LOI: IsInstalled tra ve sai')

        # -- khop lai -------------------------------------------------
        print('\n-- khop lai --')
        code = iw.remote_call(h, iw.find_export(proc.pid, 'WaveHook_Remove'))
        print(f'  WaveHook_Remove -> {code}')
        restored = iw.read_mem(h, taddr, PATCH_SIZE)
        print(f'  {PATCH_SIZE} byte sau khi go: {restored.hex(" ")}')
        if restored != FAKE_PROLOGUE:
            sys.exit('LOI: khong khoi phuc duoc byte goc')
        print('  khop lai dung byte')

        time.sleep(0.8)
        if proc.poll() is not None:
            sys.exit('LOI: process chet sau khi go hook')
        n3 = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        time.sleep(0.5)
        n4 = struct.unpack('<i', iw.read_mem(h, cc, 4))[0]
        print(f'  g_callCount sau khi go: {n3} -> {n4} '
              f'(tang {n4 - n3}; 0 = da dung hook)')
        if n4 != n3:
            sys.exit('LOI: hook van chay sau khi Remove')
        print('  hook da dung')
    finally:
        try:
            if h is not None:
                k32.CloseHandle(h)
        except Exception:
            pass
        if proc.poll() is None:
            proc.kill()
            proc.wait()

    print('\nTAT CA BUOC KIEM TRA DA QUA.')


if __name__ == '__main__':
    main()
