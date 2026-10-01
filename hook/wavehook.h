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
#include <stdint.h>

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

/* Bố cục struct WaveStyle (184 byte = 0xB8) nạp vào hàm vẽ */
#pragma pack(push, 8)
typedef struct {
    void     *vtable;          /* +0x00 */
    uint32_t  field_8;         /* +0x08 */
    uint8_t   field_C;         /* +0x0C */
    uint8_t   pad_D[3];
    void     *field_10;        /* +0x10 */
    void     *field_18;        /* +0x18 */
    void     *field_20;        /* +0x20 */
    uint32_t  field_28;        /* +0x28 */
    uint8_t   field_2C;        /* +0x2C */
    uint8_t   pad_2D[3];
    void     *field_30;        /* +0x30 */
    void     *field_38;        /* +0x38 */
    /* +0x40: Primary fill brush/color */
    void     *fill_vtable;     /* +0x40 */
    uint32_t  fill_refcount;   /* +0x48 */
    uint32_t  fill_pad;        /* +0x4C */
    uint64_t  fill_color;      /* +0x50: 4x uint16_t (R, G, B, A) */
    /* +0x58: Secondary brush/color */
    void     *sec_vtable;      /* +0x58 */
    uint32_t  sec_refcount;    /* +0x60 */
    uint32_t  sec_pad;         /* +0x64 */
    uint64_t  sec_color;       /* +0x68 */
    /* +0x70 */
    uint32_t  field_70;        /* +0x70 */
    uint32_t  field_74;        /* +0x74 */
    /* +0x78: Outline brush/color */
    void     *outline_vtable;  /* +0x78 */
    uint32_t  outline_refcount;/* +0x80 */
    uint32_t  outline_pad;     /* +0x84 */
    uint64_t  outline_color;   /* +0x88: 4x uint16_t (R, G, B, A) */
    /* Scales & Flags */
    double    scale_x;         /* +0x90 */
    double    scale_y;         /* +0x98 */
    uint32_t  field_A0;        /* +0xA0 */
    uint32_t  field_A4;        /* +0xA4 */
    void     *field_A8;        /* +0xA8 */
    uint32_t  flags;           /* +0xB0: bitfield (bit 0=fill, bit 3=dot, bit 7=layer) */
    uint32_t  pad_B4;          /* +0xB4 */
} WaveStyle;
#pragma pack(pop)

/* Chế độ màu dải sóng */
enum WaveColorMode {
    WAVE_COLOR_PASSTHROUGH  = 0,  /* Giữ màu gốc của Cubase */
    WAVE_COLOR_FL_MULTIBAND = 1,  /* Màu động FL Studio Multiband (theo phổ) */
    WAVE_COLOR_FL_NEON_BLUE = 2,  /* Màu xanh lam neon đặc trưng FL Playlist */
    WAVE_COLOR_FL_ORANGE    = 3,  /* Màu cam ấm rực rỡ FL Studio Beat */
    WAVE_COLOR_FL_CYAN      = 4,  /* Màu xanh ngọc (cyan) viền sáng */
    WAVE_COLOR_CUSTOM       = 5,  /* Màu tuỳ chỉnh do người dùng đặt */
};

/* Tiện ích đóng/mở gói màu 64-bit của Cubase */
static inline uint64_t MakeWaveColor(uint8_t r, uint8_t g, uint8_t b, uint8_t a)
{
    uint16_t r16 = (uint16_t)r << 8;
    uint16_t g16 = (uint16_t)g << 8;
    uint16_t b16 = (uint16_t)b << 8;
    uint16_t a16 = (uint16_t)a << 8;
    return ((uint64_t)a16 << 48) |
           ((uint64_t)b16 << 32) |
           ((uint64_t)g16 << 16) |
           ((uint64_t)r16 <<  0);
}

static inline void DecodeWaveColor(uint64_t c, uint8_t *r, uint8_t *g, uint8_t *b, uint8_t *a)
{
    if (r) *r = (uint8_t)((c >>  0) >> 8);
    if (g) *g = (uint8_t)((c >> 16) >> 8);
    if (b) *b = (uint8_t)((c >> 32) >> 8);
    if (a) *a = (uint8_t)((c >> 48) >> 8);
}

/* Ky hieu do MASM dua ra ngoai DLL (xem wavehook.def). */
extern void  WaveDrawHook(void);
extern void  WaveDrawTrampoline(void);
extern void *WaveDrawTrampolineVA;   /* stub nhay ve day           */
extern void *WaveDrawResumeVA;       /* trampoline nhay ve day    */

/* Giao dien cho injector goi qua GetProcAddress. */
__declspec(dllexport) int  WaveHook_Install(void);
__declspec(dllexport) int  WaveHook_Remove(void);
__declspec(dllexport) int  WaveHook_IsInstalled(void);

/* Điều khiển chế độ màu */
__declspec(dllexport) void WaveHook_SetColorMode(int mode);
__declspec(dllexport) int  WaveHook_GetColorMode(void);
__declspec(dllexport) void WaveHook_SetCustomColor(int r, int g, int b, int or_, int og, int ob);

/* Ham C hook nhan toan bo tham so ve tu ASM */
__declspec(dllexport) void WaveDrawHook_C(void *dev, void *ctx, void *pen, WaveStyle *style,
                                         void *dst_coords, const float *src_minmax, int64_t num_cols);

/* Do dai vtable can xuat cho probe. 0xC0 = 24 slot: vua dat hon
 * slot +0x80 ma `0x141E9D010` goi, vua vua het cac slot danh tieng
 * (QueryInterface / AddRef / Release) o dau bang. */
#define WAVE_PROBE_SLOTS      24
#define WAVE_PROBE_MAXTEXT    32768

/* Ket qua probe, do chinh DLL ghi ra file de khong phai doi giao thuc
 * cua injector. Doc bang `WaveProbe_ReadFile`. */
__declspec(dllexport) int  WaveProbe_DumpCount(void);
__declspec(dllexport) int  WaveProbe_ReadFile(char *buf, int len);

/* Bat/tat viec ghi dump. Mac dinh bat. */
__declspec(dllexport) void WaveProbe_Enable(int on);

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
