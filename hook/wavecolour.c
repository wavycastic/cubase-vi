/* wavecolour.c - cong thuc mau FL Studio "Multiband", chuyen sang C.
 *
 * DAY LA BAN CHuyen DOI truc tiep tu RE, khong phai viet lai theo cam nhan.
 * Nguon goc: Shared\ildsp_x64.dll, class WaveformColouring,
 * ham mau RVA 0x1AA0B0..0x1AA28B (475 byte).
 * Ghi lai day du trong docs/FLWAVE.md §8.
 *
 * Chup nhan bi chinh cua FL:
 *   - 5 bo loc mot cuc (one-pole) tren cung mot dau vao
 *   - R = m5, G = m4, B = m3   (dien giai nguoc: R = tan so thap nhat)
 *   - chuan hoa theo tong: v = R / max(sum, 1.19e-07)
 *   - tan so lay mau 1000 Hz o moi bo loc -> k = 0.0615118 @ 48 kHz
 *
 * Ham cua FL duoc goi MOT LAN cho moi cot pixel va trang thai GIU GIUA cac
 * lan goi, nen day la may trang thai, khong phai ham tinh lai tu dau.
 */
#include "wavehook.h"

/* He so cua bo loc mot cuc, tach tu ham tan() cua FL (RVA 0x1C9EF0).
 *
 * FL dung tan(x) voi giam bien do theo pi, roi k = tan(pi*f/SR)/(1+tan(pi*f/SR)).
 * Voi f = 1000 Hz, SR = 48000:  k = 0.0615118...
 *
 * Gia tri lich su trong constructor (0x3D863BA7, 0x3D7BF3C6) khop voi cong
 * thuc nay den 7 chu so, nen day la hanh tu chinh xac chu khong phai xap xi.
 */
#define WAVE_SAMPLE_RATE   48000.0
#define WAVE_CROSSOVER     1000.0

static double wave_coeff(double freq, double sr)
{
    double t = tan(3.14159265358979323846 * freq / sr);
    return t / (1.0 + t);
}

void WaveColour_Reset(WaveColourState *st)
{
    int i;
    for (i = 0; i < 5; i++)
        st->m[i] = 0.0f;
}

void WaveColour_Next(WaveColourState *st, float in_, float freq,
                     unsigned char *r, unsigned char *g, unsigned char *b)
{
    static int initialised = 0;
    static float k = 0.0f;

    double R, G, B, sum, v, norm;
    int i;

    if (!initialised) {
        k = (float)wave_coeff(WAVE_CROSSOVER, WAVE_SAMPLE_RATE);
        initialised = 1;
    }

    /* 5 bo loc mot cuc: y[n] = (1-k)*x[n] + k*y[n-1] */
    for (i = 0; i < 5; i++)
        st->m[i] = (1.0f - k) * in_ + k * st->m[i];

    /* FL dung R = m5, G = m4, B = m3 (mang la muc thu nhat -> 0) */
    R = st->m[4];
    G = st->m[3];
    B = st->m[2];

    sum = R + G + B;
    v = R / (sum > WAVE_EPSILON ? sum : WAVE_EPSILON);

    /* Doi [0,1] thanh byte; giu 0 neu tong <= eps (cot im) */
    norm = (sum > WAVE_EPSILON) ? 255.0 : 0.0;

    *r = (unsigned char)(v * norm + 0.5);
    *g = (unsigned char)((G / (sum > WAVE_EPSILON ? sum : WAVE_EPSILON)) * norm + 0.5);
    *b = (unsigned char)((B / (sum > WAVE_EPSILON ? sum : WAVE_EPSILON)) * norm + 0.5);

    (void)freq;   /* FL cung 1000 Hz cho ca 5 bo loc, xem docs/FLWAVE.md §8.9 */
}
