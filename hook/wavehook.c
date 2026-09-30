/* wavehook.c - nap hook vao tien trinh Cubase15.exe.
 *
 * Chay trong chinh tien trinh Cubase (nap qua LoadLibrary). DllMain khong
 * gan hook - viec do do injector goi qua `WaveHook_Install`.
 *
 * KHONG sua gi khi khong khop byte mong doi. Nguyen tac: sua sai byte thi
 * crash, va mot lan da xay ra khi sua `skin.srf` doi do dai nen bo nho.
 * Day la kiem tra duy nhat bao ve.
 */
#include "wavehook.h"

/* 15 byte dau ham ve song trong Cubase15.exe 15.0.30: 4 lenh chi doi
 * thoat so. Neu Cubase update va cac byte doi, ta bao loi va tu choi ghi
 * de - thay vi ghi de vao ham la khac. */
static const BYTE kExpected[HOOK_PATCH_SIZE] = {
    0x48, 0x8B, 0xC4,                         /* mov rax, rsp        */
    0x4C, 0x89, 0x48, 0x20,                    /* mov [rax+0x20], r9  */
    0x4C, 0x89, 0x40, 0x18,                    /* mov [rax+0x18], r8  */
    0x48, 0x89, 0x50, 0x10,                    /* mov [rax+0x10], rdx */
};

static BYTE           g_saved[HOOK_PATCH_SIZE];
static BYTE          *g_hookAddr;        /* ham da bi ghi de trong Cubase  */
static volatile LONG g_hooked = 0;

/* Dia chi cua trampoline trong chinh DLL. Stub nhay ve day de chay lai
 * 15 byte da doi chieu cua ham goc.
 *
 * Dinh nghia o day vi ASM can mot bien rieng: neu gop chung voi
 * `WaveDrawResumeVA` thi stub va trampoline se cung tro toi mot cho va
 * vong lap vo han. */
void *WaveDrawTrampolineVA;

/* Dia chi tiep tuc trong ham goc, sau 15 byte vua ghi de. Trampoline nhay
 * ve day. */
void *WaveDrawResumeVA;

/* Ma may: 13 byte `mov r11, imm64` roi `jmp r11`. */
static const BYTE kJmpAbs[HOOK_JMP_SIZE] = {
    0x49, 0xBB, 0, 0, 0, 0, 0, 0, 0, 0,      /* mov r11, imm64 */
    0x41, 0xFF, 0xE3,                          /* jmp r11        */
};

/* Bien dem de kiem chung hook co that su chay khong. Injector doc qua
 * ReadProcessMemory nen phai export (xem wavehook.def). */
volatile LONG g_callCount = 0;
WaveColourState g_state;

/* Buoc da di xa trong `patch`, de chan doan khi `Install` tra ve ma loi
 * Windows thay vi 0/1. 0 chua lam gi, 1 da gan co, 2 kiem tra byte xong,
 * 3 bao viet xong, 4 luu byte cu xong, 5 ghi dinh dich xong, 6 ghi JMP
 * xong, 7 tra lenh, 8 xong han, 9 khoi phuc byte cu xong. */
LONG g_step = 0;

HMODULE WINAPI DllMain(HINSTANCE hinst, DWORD reason, LPVOID reserved)
{
    (void)reserved;
    if (reason == DLL_PROCESS_ATTACH)
        DisableThreadLibraryCalls(hinst);
    return TRUE;
}

/* Tim ImageBase cua module dang chay trong chinh tien trinh nay. */
static HMODULE find_cubase(void)
{
    HMODULE h = GetModuleHandleW(L"Cubase15.exe");
    if (h == NULL)
        h = GetModuleHandleW(L"Cubase15");       /* phong khi khong co .exe */
    return h;
}

/* Ghi vong nho co the ghi. Phu 15 byte, dung bang kich thuoc that. */
static int make_writable(BYTE *addr, DWORD *oldProtect)
{
    DWORD old;
    if (!VirtualProtect(addr, HOOK_PATCH_SIZE, PAGE_EXECUTE_READWRITE, &old))
        return 0;
    *oldProtect = old;
    return 1;
}

/* --- treo cac luong khac -------------------------------------------
 *
 * Ham ve dang chay tren luong cua Cubase. Neu ghi 15 byte theo loat, se
 * co khoang thoi gian ma luong do doc mot tap byte nua cua lenh cu, va
 * chay sai. Da gap dung loi nay: minidump ghi 7 byte la `e9 8b c4 4c 89
 * 48 20` - JMP moi co byte 0, con rel32 van la cua lenh cu.
 *
 * Cach dung: dung `InterlockedExchange64` de ghi 8 byte trong MOT lenh
 * (x64 dung lenh ghi 8 byte la nguyen tu). Nhung 15 byte khong nhip trong
 * 8, nen 7 byte con lai van phai ghi thuong. Voi 7 byte con lai do, thoi
 * gian cua no rat ngan, va phai dung them thuoc phap.
 *
 * Nen ta treo TAT CA luong khac trong tien trinh, ghi, roi tha. Day la
 * cach chuan cua cac khung hook. Treo qua 30 luong ton tai mot tho, va
 * chi xay ra khi cai hook - khong phai trong vong ve hinh anh.
 */
#define MAX_THREADS 512

typedef struct {
    HANDLE h[MAX_THREADS];
    int    n;
} ThreadSet;

/* `THREADENTRY32` khong nam trong <windows.h> ma o <tlhelp32.h>. */
#include <tlhelp32.h>

static void suspend_others(ThreadSet *ts)
{
    HANDLE       snap;
    THREADENTRY32 te;
    DWORD        self = GetCurrentThreadId();

    ts->n = 0;
    snap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (snap == INVALID_HANDLE_VALUE)
        return;

    te.dwSize = sizeof(te);
    if (Thread32First(snap, &te)) {
        do {
            if (te.th32ThreadID == self || ts->n >= MAX_THREADS)
                continue;
            ts->h[ts->n] = OpenThread(THREAD_SUSPEND_RESUME, FALSE,
                                      te.th32ThreadID);
            if (ts->h[ts->n] && SuspendThread(ts->h[ts->n]) != -1)
                ts->n++;
            else if (ts->h[ts->n]) {
                CloseHandle(ts->h[ts->n]);
                ts->h[ts->n] = NULL;
            }
        } while (Thread32Next(snap, &te));
    }
    CloseHandle(snap);
}

static void resume_others(ThreadSet *ts)
{
    int i;
    for (i = 0; i < ts->n; i++) {
        ResumeThread(ts->h[i]);
        CloseHandle(ts->h[i]);
    }
    ts->n = 0;
}

/* Ghi 13 byte lenh nhay tuyet doi vao `at`, kem 2 NOP cho du 15 byte.
 *
 *   at[0]      49        mov r11, ...
 *   at[1]      BB        ...opcode
 *   at[2..9]   <imm64>   dia chi dich, little-endian
 *   at[10..12] 41 FF E3  jmp r11
 *   at[13..14] 90 90     NOP
 *
 * CANH THAT: 8 byte dia chi phai o `at[2..9]`, khong phai `at[0..7]`. Viet
 * sai cho phep `49 BB` bi ghi de, kenh kich thuoc lai dung 13 byte nen
 * test van bao "hop le" - nhung lenh thuc thi thi la `add [rax], al` va
 * Cubase chet. Da gap dung loi nay.
 */
static void write_abs_jmp(BYTE *at, void *dest)
{
    /* `ULONGLONG_PTR` khong ton tai tren MSVC. Ep con tro ve 64 bit bang
     * kieu so nguyen, roi ep nguoc lai khi ghi ra byte. */
    ULONGLONG v = (ULONGLONG)(ULONG_PTR)dest;
    int i;

    at[0] = kJmpAbs[0];              /* 49 */
    at[1] = kJmpAbs[1];              /* BB */
    for (i = 0; i < 8; i++)
        at[2 + i] = (BYTE)(v >> (8 * i));
    at[10] = kJmpAbs[10];            /* 41 */
    at[11] = kJmpAbs[11];            /* FF */
    at[12] = kJmpAbs[12];            /* E3 */
    at[13] = 0x90;                   /* NOP */
    at[14] = 0x90;                   /* NOP */
}

/* Logic ghi de dung, dung chung cho Cubase that va process thu nghiem. */
static int patch(BYTE *target)
{
    BYTE      *hookFn;
    ThreadSet  ts;
    DWORD      oldProtect = 0;
    int        i;

    g_step = 1;
    if (InterlockedCompareExchange(&g_hooked, 1, 0) != 0)
        return 1;                       /* da hook roi */

    /* Kiem tra byte: KHONG khop thi tu choi, khong ghi gi ca */
    for (i = 0; i < HOOK_PATCH_SIZE; i++) {
        if (target[i] != kExpected[i])
            return 0;
    }
    g_step = 2;

    if (!make_writable(target, &oldProtect))
        return 0;
    g_step = 3;

    /* Luu byte cu de ghi lai. 15 byte, va byte 15 la byte dau cua lenh
     * ke tiep trong ham goc. */
    for (i = 0; i < HOOK_PATCH_SIZE; i++)
        g_saved[i] = target[i];
    g_step = 4;

    /* Trampoline chay lai 15 byte da doi chieu, roi nhay ve phan con lai
     * cua ham goc. Hai dia chi nay phai tach nhau: gop lai thi stub va
     * trampoline tro cung mot cho. */
    WaveDrawTrampolineVA = (void *)&WaveDrawTrampoline;
    WaveDrawResumeVA = target + HOOK_PATCH_SIZE;

    /* Chuyen dia chi ham sang con tro byte. `WaveDrawHook` la ky hieu do
     * MASM dua ra, nen phai lay dia chi ma khong goi. */
    hookFn = (BYTE *)(void *)&WaveDrawHook;
    g_step = 5;

    suspend_others(&ts);
    write_abs_jmp(target, hookFn);
    g_step = 6;
    VirtualProtect(target, HOOK_PATCH_SIZE, oldProtect, &oldProtect);
    FlushInstructionCache(GetCurrentProcess(), target, HOOK_PATCH_SIZE);
    resume_others(&ts);
    g_step = 7;

    g_hookAddr = target;
    g_step = 8;
    return 1;
}

/* Hook ham ve cua Cubase: RVA co dinh trong tieu de. */
int WaveHook_Install(void)
{
    HMODULE cub;
    BYTE   *target;

    cub = find_cubase();
    if (cub == NULL)
        return 0;

    /* Kiem tra RVA nam trong anh cua module TRUOC khi doc.
     *
     * Neu nap nham vao mot module nho hon, byte dau ham nam ngoai vung da
     * cap: doc se sinh ACCESS_VIOLATION ngay trong ham nay. */
    {
        IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)cub;
        IMAGE_NT_HEADERS64 *nt;

        if (dos->e_magic != IMAGE_DOS_SIGNATURE)
            return 0;
        nt = (IMAGE_NT_HEADERS64 *)((BYTE *)cub + dos->e_lfanew);
        if (nt->Signature != IMAGE_NT_SIGNATURE)
            return 0;
        if (CUBASE_WAVE_DRAW_RVA + HOOK_PATCH_SIZE > nt->OptionalHeader.SizeOfImage)
            return 0;
    }

    target = (BYTE *)cub + CUBASE_WAVE_DRAW_RVA;
    return patch(target);
}

/* Hook ham bat ky - dung cho process thu nghiem. */
int WaveHook_InstallAt(void *fn, void *cont)
{
    (void)cont;
    if (fn == NULL)
        return 0;
    return patch((BYTE *)fn);
}

int WaveHook_Remove(void)
{
    ThreadSet ts;
    DWORD      oldProtect = 0;
    int        i;

    if (g_hooked == 0 || g_hookAddr == NULL)
        return 1;

    if (!make_writable(g_hookAddr, &oldProtect))
        return 0;

    suspend_others(&ts);
    for (i = 0; i < HOOK_PATCH_SIZE; i++)
        g_hookAddr[i] = g_saved[i];
    VirtualProtect(g_hookAddr, HOOK_PATCH_SIZE, oldProtect, &oldProtect);
    FlushInstructionCache(GetCurrentProcess(), g_hookAddr, HOOK_PATCH_SIZE);
    resume_others(&ts);

    g_step = 9;
    g_hooked = 0;
    g_hookAddr = NULL;
    return 1;
}

int WaveHook_IsInstalled(void)
{
    return g_hooked != 0;
}

/* Ham nay chay MOT LAN cho moi cot pixel. Hien tai chi dem de chung minh
 * hook dung cho, va khoi dong lai trang thai mau theo tung chuoi ve.
 *
 * Tham so truyen tu wavehook.asm, giu nguyen toan bo thanh ghi phia truoc.
 */
void __cdecl WaveDrawHook_C(void)
{
    InterlockedIncrement(&g_callCount);

    /* Moi mot lan ve la mot chuoi moi: khoi dong lai bo loc mot cuc.
     * FL giu trang thai giua cac cot trong MOT chuoi, nen phan bien ranh
     * giua cac chuoi la canh. Xem docs/FLWAVE.md §9.11. */
    WaveColour_Reset(&g_state);
}
