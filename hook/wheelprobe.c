/* wheelprobe.c - DLL CHI QUAN SAT, khong can thiep hanh vi Cubase.
 *
 * Muc tieu: tra loi ba cau hoi ma RE tinh tien chua tra loi duoc
 *   1. Cua so nao la Project window? (ten lop cua so khong tim duoc trong
 *      chuoi cua Cubase15.exe - `ProjectWindow` o 0x060EF910 hoa ra la ten
 *      truong metadata, no nam canh `Composer`/`Lyricist`/`Copyright`)
 *   2. Dai ruler nam o clientY nao? (phu thuoc toolbar + Info Line)
 *   3. Ctrl+wheel co zoom khi con tro nam TRONG ruler khong?
 *
 * Cach lam: subclass moi cua so top-level cua chinh tien trinh nay, ghi log
 * moi lan WM_MOUSEWHEEL. KHONG doi thong diep nao, KHONG ghi byte nao, KHONG
 * fake phim gi. Cubase chay y het nhu chua co DLL.
 *
 * Day la buoc DO TRUOC khi viet ban can thiep that. Sua byte sai thi crash -
 * dung nguyen tac cua wavehook.c. Ban nay chi them SetWindowLongPtr, nen
 * neu no crash thi do nhiem loi cua chinh no, khong phai do Cubase.
 *
 * Xuat:
 *   WheelProbe_Install     - bat subclass + mo log
 *   WheelProbe_Remove     - tra WNDPROC ve nguyen bat, dong log
 *   WheelProbe_IsInstalled
 *   WheelProbe_Enable(int)- 1 = ghi log, 0 = im (mac dinh 1)
 *
 * Log: file `wheelprobe.log` canh DLL. Injector doc truc tiep, khong can doi
 * giao thuc cua no (cung cach waveprobe.c lam).
 */
#include <windows.h>
#include <windowsx.h>   /* GET_X_LPARAM / GET_Y_LPARAM / GET_WHEEL_DELTA_WPARAM */
#include <stdio.h>
#include <string.h>

#define PROBE_MAXWIN   512
#define PROBE_MAXTEXT  65536

/* Module handle cua chinh DLL nay.
 *
 * DllMain CHI giu lai handle roi return - khong lam gi khac. Mọi thao tac
 * that (CreateFile, EnumWindows, SetWindowLongPtr) di vao trong
 * WheelProbe_Install, do injector goi. Vay ly do cua wavehook.c: loader
 * lock va tao file hay tao thread trong DllMain deu gay treo hoac deadlock
 * khi process nap DLL. */
static HMODULE g_self = NULL;

BOOL APIENTRY DllMain(HMODULE m, DWORD reason, LPVOID reserved)
{
    (void)reserved;
    if (reason == DLL_PROCESS_ATTACH)
        g_self = m;
    return TRUE;
}

typedef struct {
    HWND    hwnd;
    WNDPROC orig;      /* WNDPROC cu cua so, de goi lai nguyen ban */
    int     used;
} ProbeWin;

static ProbeWin  g_wins[PROBE_MAXWIN];
static CRITICAL_SECTION g_lock;
static int  g_lockReady = 0;
static int  g_installed = 0;
static volatile LONG g_enabled = 1;

static HANDLE   g_log = NULL;
static CRITICAL_SECTION g_fileLock;

/* Ap dung cho MOT thong diep, roi tra ve ma cua wndproc cu. */
static LRESULT CALLBACK ProbeSubclass(HWND h, UINT msg, WPARAM wp, LPARAM lp);

static void log_init(void)
{
    char path[MAX_PATH];
    DWORD n;

    if (g_log != NULL)
        return;

    /* file canh DLL dang chay - dung GetModuleFileName cua chinh module nay
     * vi ham nay chay trong Cubase, khong phai trong process ta goi. */
    n = GetModuleFileNameA(g_self, path, MAX_PATH);
    if (n == 0 || n >= MAX_PATH)
        return;

    /* cat '.dll' roi them '.log' */
    {
        char *dot = strrchr(path, '.');
        if (dot != NULL)
            *dot = '\0';
    }
    lstrcatA(path, ".log");

    g_log = CreateFileA(path, FILE_APPEND_DATA,
                        FILE_SHARE_READ | FILE_SHARE_WRITE, NULL,
                        OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
}

static void log_write(const char *s)
{
    DWORD written = 0;

    if (g_log == NULL || g_enabled == 0)
        return;

    EnterCriticalSection(&g_fileLock);
    WriteFile(g_log, s, (DWORD)lstrlenA(s), &written, NULL);
    LeaveCriticalSection(&g_fileLock);
}

/* ---------------------- ghi lai mot lan cuon ---------------------- */
static void log_wheel(HWND h, WPARAM wp, LPARAM lp)
{
    char  cls[128], title[256], line[900];
    POINT pt;
    int   clientX = 0, clientY = 0;
    int   cx = 0, cy = 0, delta;
    int   ctrl, shift, alt;
    RECT  rc;

    cls[0] = title[0] = '\0';
    GetClassNameA(h, cls, (int)sizeof(cls));
    GetWindowTextA(h, title, (int)sizeof(title));

    /* lParam cua WM_MOUSEWHEEL la toa do MAN HINH cua con tro. */
    pt.x = GET_X_LPARAM(lp);
    pt.y = GET_Y_LPARAM(lp);
    ScreenToClient(h, &pt);
    clientX = pt.x;
    clientY = pt.y;

    GetClientRect(h, &rc);
    cx = rc.right - rc.left;
    cy = rc.bottom - rc.top;

    delta = GET_WHEEL_DELTA_WPARAM(wp);

    /* Doc THAT trang thai phim tai thoi diem cuon. Day la thu Cubase cung
     * doc, nen neu nguoi dung bam Ctrl roi cuon, ta se thay gia tri day. */
    ctrl  = (GetKeyState(VK_CONTROL)  & 0x8000) ? 1 : 0;
    shift = (GetKeyState(VK_SHIFT)    & 0x8000) ? 1 : 0;
    alt   = (GetKeyState(VK_MENU)     & 0x8000) ? 1 : 0;

    _snprintf_s(line, sizeof(line), _TRUNCATE,
                "hwnd=0x%llx class=%s title=\"%s\" client=(%d,%d) "
                "size=(%dx%d) screen=(%d,%d) delta=%+d ctrl=%d shift=%d alt=%d\r\n",
                (unsigned long long)h, cls, title, clientX, clientY,
                cx, cy, pt.x, pt.y, delta, ctrl, shift, alt);
    log_write(line);
}

/* ---------------------- wndproc con ---------------------- */
static LRESULT CALLBACK ProbeSubclass(HWND h, UINT msg, WPARAM wp, LPARAM lp)
{
    WNDPROC orig = NULL;
    LRESULT r;

    EnterCriticalSection(&g_lock);
    {
        int i;
        for (i = 0; i < PROBE_MAXWIN; i++) {
            if (g_wins[i].used && g_wins[i].hwnd == h) {
                orig = g_wins[i].orig;
                break;
            }
        }
    }
    LeaveCriticalSection(&g_lock);

    if (orig == NULL)
        return DefWindowProcA(h, msg, wp, lp);

    if (msg == WM_MOUSEWHEEL)
        log_wheel(h, wp, lp);        /* chi ghi, KHONG doi gi */

    r = CallWindowProcA(orig, h, msg, wp, lp);
    return r;
}

/* ---------------------- them / bot mot cua so ---------------------- */
static void add_window(HWND h)
{
    int i;

    EnterCriticalSection(&g_lock);
    for (i = 0; i < PROBE_MAXWIN; i++) {
        if (!g_wins[i].used) {
            g_wins[i].used = 1;
            g_wins[i].hwnd = h;
            g_wins[i].orig = (WNDPROC)SetWindowLongPtrA(h, GWLP_WNDPROC,
                                                      (LONG_PTR)ProbeSubclass);
            break;
        }
    }
    LeaveCriticalSection(&g_lock);
}

static void remove_all(void)
{
    int i;

    EnterCriticalSection(&g_lock);
    for (i = 0; i < PROBE_MAXWIN; i++) {
        if (g_wins[i].used) {
            if (IsWindow(g_wins[i].hwnd))
                SetWindowLongPtrA(g_wins[i].hwnd, GWLP_WNDPROC,
                                  (LONG_PTR)g_wins[i].orig);
            g_wins[i].used = 0;
            g_wins[i].hwnd = NULL;
            g_wins[i].orig = NULL;
        }
    }
    LeaveCriticalSection(&g_lock);
}

static BOOL CALLBACK enum_cb(HWND h, LPARAM lp)
{
    DWORD pid = 0;

    (void)lp;
    GetWindowThreadProcessId(h, &pid);
    if (pid == GetCurrentProcessId())
        add_window(h);
    return TRUE;      /* tiep tuc, de thu ca cua so an/ke, xem het bo lai */
}

/* ---------------------- API xuat ---------------------- */
__declspec(dllexport) int WheelProbe_Install(void)
{
    if (g_installed)
        return 1;
    if (!g_lockReady) {
        InitializeCriticalSection(&g_lock);
        InitializeCriticalSection(&g_fileLock);
        g_lockReady = 1;
    }

    log_init();
    EnumWindows(enum_cb, 0);
    g_installed = 1;
    return 1;
}

__declspec(dllexport) int WheelProbe_Remove(void)
{
    if (!g_installed)
        return 1;
    remove_all();               /* tra WNDPROC TRUOC khi dong file */
    if (g_log != NULL) {
        CloseHandle(g_log);
        g_log = NULL;
    }
    g_installed = 0;
    return 1;
}

__declspec(dllexport) int WheelProbe_IsInstalled(void)
{
    return g_installed;
}

__declspec(dllexport) void WheelProbe_Enable(int on)
{
    InterlockedExchange(&g_enabled, on ? 1 : 0);
}