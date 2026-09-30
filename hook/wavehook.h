/* wavehook.h - khai bao chung cho DLL hook va injector.
 *
 * Muc tieu: ve lai duong song trong Project Window cua Cubase 15 theo kieu
 * FL Studio "Colourful Waves -> Multiband", tuc la mau hoa theo tam so.
 *
 * Xem docs/FLWAVE.md §8 (cong thuc cua FL, lay tu ildsp_x64.dll) va
 * docs/WAVEFORM.md §3, §8 (ham ve cua Cubase).
 */
#ifndef WAVEHOOK_H
#define WAVEHOOK_H

#include <windows.h>

/* Dia chi ham ve song trong Cubase15.exe.
 *
 * RVA 0x1E9E140, ham 0x1E9E140..0x1E9E825 (1765 byte), chi co MOT noi goi:
 * 0x1E9B9AB trong ham 0x1E9B6F0..0x1E9BA17. Do do hook o dau ham la du -
 * khong phai tim nhieu diem vao.
 *
 * Ve 15 byte, khong phai 5: ham bat dau bang 4 lenh chi doi thoat so
 * (3 + 4 + 4 + 4 byte) va 15 la diem dung lenh. 15 byte do duoc copy sang
 * trampoline. Chi tiet va ly do trong `wavehook.asm`.
 */
#define CUBASE_WAVE_DRAW_RVA   0x1E9E140
#define HOOK_PATCH_SIZE        15

/* Do dai lenh nhay 13 byte: `mov r11, imm64` (10) + `jmp r11` (3).
 * Nhay tuyet doi, khong dung rel32 - xem giai thich trong wavehook.asm. */
#define HOOK_JMP_SIZE          13

/* Ky hieu do MASM dua ra ngoai DLL (xem wavehook.def).
 *
 * Khai bao `extern` - KHONG dung dllimport: may ky tu do cung mot DLL,
 * dllimport se sinh mot lop gọi qua IAT cho chinh ham cua no. Chi can
 * khai bao de C va MASM tro toi cung mot dia chi. Neu asm tu khai bao
 * rieng, con do ghi dinh dich trong C se tro toi cho khac. */
extern void  WaveDrawHook(void);
extern void  WaveDrawTrampoline(void);
extern void *WaveDrawTrampolineVA;   /* stub nhay ve day           */
extern void *WaveDrawResumeVA;       /* trampoline nhay ve day    */

/* Giao dien cho injector goi qua GetProcAddress. */
__declspec(dllexport) int  WaveHook_Install(void);
__declspec(dllexport) int  WaveHook_Remove(void);
__declspec(dllexport) int  WaveHook_IsInstalled(void);
__declspec(dllexport) void WaveDrawHook_C(void);

/* Danh sach RVA cho `WaveProbe_InstallAll`. So phan tu va danh sach phai
 * cung mot khoi: `CreateRemoteThread` chi truyen duoc MOT tham so, nen
 * tham so thu hai (`rdx`) luon bang 0. Bo cuc phai dung 4 byte cho ca
 * `count` va tung RVA, va giong het phia Python trong `inject_wavehook.py`.
 */
#pragma pack(push, 4)
#define MAX_PROBES 64
typedef struct {
    unsigned int count;
    unsigned int rva[MAX_PROBES];
} ProbeTargets;
#pragma pack(pop)

/* --- bo dem nhieu diem (xem waveprobe.c) -----------------------------
 *
 * Dung de TIM ham ve duong song that bang cach do, khong doan: gan hook vao
 * moi ham co prologue 15 byte an toan roi xem cho nao chay khi Cubase ve
 * duong song. Toan bo exe chi co 29 ham dang do.
 */
extern LONG       g_probeCount[];
extern ULONGLONG  g_probeArg0[];
extern LONG       g_probeInstalled;

__declspec(dllexport) int WaveProbe_InstallAll(const ProbeTargets *t);
__declspec(dllexport) int WaveProbe_RemoveAll(void);
__declspec(dllexport) int WaveProbe_Count(void);
__declspec(dllexport) void WaveProbe_C(void *site, void *arg0);

/* Handler dung chung, viet bang MASM. Khai bao `extern` de C lay duoc dia
 * chi ma khong goi. */
extern void WaveProbeCommon(void);

/* Giong `WaveHook_Install` nhung cho phep chi dinh dia chi ham can hook.
 *
 * Ly do co ham nay: de kiem chung hook tren process thu nghiem, ta can
 * hook mot ham bat ky trong file do, chu khong phai ham o RVA cua Cubase.
 * `/SECTION` cua link.exe khong chuyen duoc section sang RVA bat buoc (chi
 * can it nhat mot dac tinh moi nhan dia chi), nen khong lam duoc the nao.
 * Cho phep truyen dia chi thi dung logic ghi de 7 byte + trampoline duoc
 * kiem chung nguyen ve, con `WaveHook_Install` van la duong dung voi
 * Cubase that.
 *
 *   fn   - dia chi ham se bi ghi de 7 byte dau
 *   cont - dia chi tiep tuc sau 7 byte do (noi trampoline nhay ve)
 */
__declspec(dllexport) int  WaveHook_InstallAt(void *fn, void *cont);

/* So cot pixel toi da cho phep. Doc ra tu ham ve: no bo qua cot nao co
 * gia tri -0.0f (0x145FA4E40) o ca min va max. */
#define WAVE_MAX_COLUMNS       8192

/* Gia tri nho gap nhat cho mau, tuong duong hang cua FL trong
 * docs/FLWAVE.md §8.8 (1.19e-07). */
#define WAVE_EPSILON           1.19e-07f

/* Cong thuc FL: 5 bo loc mot cuc, tan so 1000 Hz, R:G:B = m5:m4:m3.
 *
 * Input la chuoi theo thu tu thoi gian (moi lai goi ham ve mot cot pixel
 * roi), nen trang thai cac bo loc phai giu giua cac lan goi. Doc FLWAVE.md
 * §8.8 va §8.9.
 */
typedef struct {
    float m[5];               /* trang thai 5 bo loc mot cuc           */
} WaveColourState;

/* Khoi tao trang thai cho 1 chuoi moi. */
void WaveColour_Reset(WaveColourState *st);

/* Tinh mau cho gia tri vao `in` (bien do tho), ghi R, G, B (0..255).
 * `freq` la tan so lay mau (Hz). */
void WaveColour_Next(WaveColourState *st, float in_, float freq,
                     unsigned char *r, unsigned char *g, unsigned char *b);

#endif /* WAVEHOOK_H */
