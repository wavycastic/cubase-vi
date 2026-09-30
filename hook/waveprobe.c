/* waveprobe.c - bo dem nhieu diem, dung de TIM ra ham ve duong song that.
 *
 * Voi sao can cai nay
 * ------------------
 * Ham `0x1E9E140` da gan hook duoc (15 byte prologue khop mau an toan) nhung
 * `g_callCount` van = 0 sau khi da mo project co audio. Hoac la nhan dinh
 * "day la ham ve duong song" sai, hoac ham do khong nam tren duong ve dang
 * dung. Giai quyet bang cach DO, khong doan: gan hook vao tat ca ham co
 * prologue 15 byte an toan, roi xem cho nao thuc su chay.
 *
 * Toan bo exe 135 MB chi co 29 ham co dung 15 byte do, nen 29 diem la
 * du de biet duong ve song di qua ham nao.
 *
 * Ky thuat
 * --------
 * Moi diem co MOT khu vuc bo nho rieng (VirtualAlloc) chua:
 *   stub[0..31]   `mov r11, <dia chi diem>` + `mov r10, <common>`
 *                 + `jmp r10`
 *   tramp[32..63] 15 byte prologue goc + `mov r11, <diem + 15>` + `jmp r11`
 * va 15 byte tai `diem` duoc ghi bang `mov r11, <stub>` + `jmp r11` + 2 NOP.
 *
 * `WaveProbeCommon` (MASM) day `r11` vao vung, goi `WaveProbe_C` de tang
 * dem theo dia chi, roi nhay ve trampoline cua diem do.
 *
 * KHONG sua gi khi 15 byte khong khop mau an toan - ham do bo qua, khong
 * phai ep.
 */
#include "wavehook.h"
#include <tlhelp32.h>

#define MAX_PROBES 64

/* 15 byte prologue duoc coi la AN TOAN de hook: 4 lenh chi doi thoat so
 * (mov rax, rsp; mov [rax+20h], r9; mov [rax+18h], r8; mov [rax+10h], rdx).
 * Chúng khong dung dia chi tương doi RIP nen copy sang dia chi khac van
 * chay dung, va 15 la diem dung lenh. */
static const BYTE kSafePrologue[HOOK_PATCH_SIZE] = {
    0x48, 0x8B, 0xC4,
    0x4C, 0x89, 0x48, 0x20,
    0x4C, 0x89, 0x40, 0x18,
    0x48, 0x89, 0x50, 0x10,
};

typedef struct {
    BYTE *site;          /* ham bi gan hook trong Cubase   */
    BYTE *stub;          /* vao WaveProbeCommon            */
    BYTE *tramp;         /* chay lai 15 byte goc roi noi tiep */
} Probe;

static Probe g_probes[MAX_PROBES];
static int   g_nProbes = 0;

/* Dem moi diem. Injector doc qua ReadProcessMemory; export khai bao trong
 * wavehook.def. KHONG them `__declspec(dllexport)` o day - se trung ten voi
 * .def va linker canh bao LNK4197. */
LONG g_probeCount[MAX_PROBES];
/* Tham so 1 (rcx) cua lan goi dau tien - nhieu khi la con tro doi tuong
 * ve, giup do la ham nao. */
ULONGLONG g_probeArg0[MAX_PROBES];

/* Trampoline dang chay, gan boi `WaveProbe_C`. */
void *WaveProbeTrampVA;

LONG g_probeInstalled = 0;

/* --- treo luong, dung chung kieu voi wavehook.c ---------------------- */
#define MAX_THREADS 512

typedef struct {
    HANDLE h[MAX_THREADS];
    int    n;
} ThreadSet;

static void suspend_others(ThreadSet *ts)
{
    HANDLE        snap;
    THREADENTRY32 te;
    DWORD         self = GetCurrentThreadId();

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

/* Ghi 10 byte `mov r11/r10, imm64` roi 3 byte `jmp r11/r10`. */
static void write_mov_r(BYTE *at, int reg, ULONGLONG v)
{
    int i;
    at[0] = (BYTE)(0x49 | (reg << 3));       /* REX.W + REX.B */
    at[1] = (BYTE)(0xBB + reg * 2);          /* mov r11/r15, imm64 */
    for (i = 0; i < 8; i++)
        at[2 + i] = (BYTE)(v >> (8 * i));
}

static void write_jmp_r(BYTE *at, int reg)
{
    at[0] = 0x41;
    at[1] = 0xFF;
    at[2] = (BYTE)(0xE0 + reg);              /* jmp r11/r10 */
}

/* Gan hook dem cho mot ham. Tra 1 neu thanh cong. */
static int probe_one(BYTE *site)
{
    BYTE     *block;
    BYTE     *stub, *tramp;
    ThreadSet ts;
    DWORD     oldProtect = 0, restore = 0;
    int       idx;

    if (g_nProbes >= MAX_PROBES)
        return 0;

    /* Chi nhan ham co 15 byte prologue AN TOAN. Khong ep. */
    if (memcmp(site, kSafePrologue, HOOK_PATCH_SIZE) != 0)
        return 0;

    block = (BYTE *)VirtualAlloc(NULL, 64, MEM_COMMIT | MEM_RESERVE,
                                 PAGE_EXECUTE_READWRITE);
    if (block == NULL)
        return 0;
    stub = block;
    tramp = block + 32;

    idx = g_nProbes;

    /* stub: r11 = dia chi diem, r10 = common, jmp r10 */
    write_mov_r(stub + 0, 1, (ULONGLONG)(ULONG_PTR)site);      /* r11 */
    write_mov_r(stub + 10, 0, (ULONGLONG)(ULONG_PTR)&WaveProbeCommon); /* r10 */
    write_jmp_r(stub + 20, 0);                                  /* jmp r10 */

    /* trampoline: 15 byte prologue goc, roi nhay ve site + 15 */
    memcpy(tramp, site, HOOK_PATCH_SIZE);
    write_mov_r(tramp + HOOK_PATCH_SIZE, 1,
                (ULONGLONG)(ULONG_PTR)(site + HOOK_PATCH_SIZE));
    write_jmp_r(tramp + HOOK_PATCH_SIZE + 10, 1);
    FlushInstructionCache(GetCurrentProcess(), block, 64);

    g_probes[idx].site = site;
    g_probes[idx].stub = stub;
    g_probes[idx].tramp = tramp;
    g_nProbes = idx + 1;

    /* Ghi vao ham dich, co treo cac luong khac de khong dua chay voi
     * luong dang ve. */
    if (!VirtualProtect(site, HOOK_PATCH_SIZE, PAGE_EXECUTE_READWRITE,
                        &oldProtect)) {
        g_nProbes--;
        VirtualFree(block, 0, MEM_RELEASE);
        return 0;
    }
    suspend_others(&ts);
    write_mov_r(site, 1, (ULONGLONG)(ULONG_PTR)stub);
    write_jmp_r(site + 10, 1);
    site[13] = 0x90;
    site[14] = 0x90;
    resume_others(&ts);
    VirtualProtect(site, HOOK_PATCH_SIZE, oldProtect, &restore);
    FlushInstructionCache(GetCurrentProcess(), site, HOOK_PATCH_SIZE);
    return 1;
}

/* Kieu `ProbeTargets` da khai bao trong wavehook.h - phai dung CHUNG mot
 * khai bao, vi injector ghi khoi do vao bo nho cua tien trinh theo chung
 * mot bo cuc 4 byte. Khai bao lai o day se lech kich thuoc. */

/* Gan hook dem cho tat ca ham co prologue an toan trong `t`.
 *
 * Con tro phai tro vao bo nho cua TIEN TRINH DICH - dung con tro cua DLL
 * se khong phai danh sach RVA cua Cubase.
 *
 * Tra ve so diem da gan; nho hon `count` nghia la co ham bi bo qua vi
 * prologue khong khop mau an toan.
 */
int WaveProbe_InstallAll(const ProbeTargets *t)
{
    HMODULE cub;
    int     i, n = 0;

    if (t == NULL || t->count == 0 || t->count > MAX_PROBES)
        return 0;
    cub = GetModuleHandleW(L"Cubase15.exe");
    if (cub == NULL)
        return 0;
    if (g_probeInstalled)
        return g_nProbes;
    g_probeInstalled = 1;

    for (i = 0; i < (int)t->count; i++) {
        BYTE *site = (BYTE *)cub + t->rva[i];
        if (probe_one(site))
            n++;
    }
    return n;
}

/* Go dem: khoi phuc 15 byte goc cua moi diem. */
int WaveProbe_RemoveAll(void)
{
    ThreadSet ts;
    DWORD     oldProtect = 0, restore = 0;
    int       i, n = 0;

    for (i = 0; i < g_nProbes; i++) {
        BYTE *site = g_probes[i].site;
        if (site == NULL)
            continue;
        if (!VirtualProtect(site, HOOK_PATCH_SIZE, PAGE_EXECUTE_READWRITE,
                            &oldProtect))
            continue;
        suspend_others(&ts);
        memcpy(site, kSafePrologue, HOOK_PATCH_SIZE);
        resume_others(&ts);
        VirtualProtect(site, HOOK_PATCH_SIZE, oldProtect, &restore);
        FlushInstructionCache(GetCurrentProcess(), site, HOOK_PATCH_SIZE);
        VirtualFree(g_probes[i].stub, 0, MEM_RELEASE);
        g_probes[i].site = NULL;
        n++;
    }
    g_nProbes = 0;
    g_probeInstalled = 0;
    return n;
}

int WaveProbe_Count(void)
{
    return g_nProbes;
}

/* Handler C, goi tu WaveProbeCommon voi `site` va `arg0`. */
void __cdecl WaveProbe_C(void *site, void *arg0)
{
    int i;

    for (i = 0; i < g_nProbes; i++) {
        if (g_probes[i].site == (BYTE *)site)
            break;
    }
    if (i >= g_nProbes)
        return;
    g_probeCount[i]++;
    if (g_probeArg0[i] == 0)
        g_probeArg0[i] = (ULONGLONG)(ULONG_PTR)arg0;
    WaveProbeTrampVA = g_probes[i].tramp;
}
