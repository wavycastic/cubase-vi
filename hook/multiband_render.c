/* multiband_render.c - Pure standalone Multiband waveform renderer for Cubase 15
 * Completely position-independent: no CRT calls, no external math dependencies.
 */
#include <stdint.h>
#include <xmmintrin.h>

#pragma pack(push, 8)
typedef struct {
    int32_t x;
    int32_t y;
} GdiPoint;

typedef struct {
    uint64_t color;
    uint32_t mode;
    uint32_t pad;
    uint64_t pad2[2];
} GdiPaint;

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
    void     *fill_vtable;     /* +0x40 */
    uint32_t  fill_refcount;   /* +0x48 */
    uint32_t  fill_pad;        /* +0x4C */
    uint64_t  fill_color;      /* +0x50 */
    void     *sec_vtable;      /* +0x58 */
    uint32_t  sec_refcount;    /* +0x60 */
    uint32_t  sec_pad;         /* +0x64 */
    uint64_t  sec_color;       /* +0x68 */
    uint32_t  field_70;        /* +0x70 */
    uint32_t  field_74;        /* +0x74 */
    void     *outline_vtable;  /* +0x78 */
    uint32_t  outline_refcount;/* +0x80 */
    uint32_t  outline_pad;     /* +0x84 */
    uint64_t  outline_color;   /* +0x88 */
    double    scale_x;         /* +0x90 */
    double    scale_y;         /* +0x98 */
    uint32_t  field_A0;        /* +0xA0 */
    uint32_t  field_A4;        /* +0xA4 */
    void     *field_A8;        /* +0xA8 */
    uint32_t  flags;           /* +0xB0 */
} WaveStyle;
#pragma pack(pop)

typedef void (*FnConstructPaint)(GdiPaint *paint, const uint64_t *color, uint32_t mode, uint32_t flags);
typedef void (*FnDestructPaint)(GdiPaint *paint);

static inline float fast_sqrt(float x)
{
    if (x <= 0.0f) return 0.0f;
    __m128 v = _mm_set_ss(x);
    v = _mm_sqrt_ss(v);
    return _mm_cvtss_f32(v);
}

static inline uint64_t PackColor64(uint8_t r, uint8_t g, uint8_t b, uint8_t a)
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

void RenderMultiband(void *device, const float *col_data, int num_cols, int start_x, WaveStyle *style)
{
    if (!device || !col_data || num_cols <= 0)
        return;

    void **vtable = *(void***)device;
    typedef void (*FnLine)(void *dev, const GdiPoint *pt);
    typedef void (*FnPaint)(void *dev, const GdiPaint *paint);

    FnLine LineTo = (FnLine)vtable[0x00 / 8];
    FnLine MoveTo = (FnLine)vtable[0x08 / 8];
    FnPaint SetPaint = (FnPaint)vtable[0x80 / 8];

    FnConstructPaint ConstructPaint = (FnConstructPaint)(0x144A958D0);
    FnDestructPaint  DestructPaint  = (FnDestructPaint)(0x144A95580);

    /* FL Studio one-pole filter coefficients @ 1000 Hz, 48 kHz */
    const float k = 0.0615118f;
    float s0 = 0.0f, s1 = 0.0f, s2 = 0.0f, s3 = 0.0f, s4 = 0.0f;

    for (int i = 0; i < num_cols; i++) {
        float y_top = col_data[i * 2 + 0];
        float y_bot = col_data[i * 2 + 1];

        /* Skip empty column */
        if (y_top == 0.0f && y_bot == 0.0f)
            continue;

        float h = y_bot - y_top;
        if (h < 0.0f) h = -h;

        /* FL Studio 5 one-pole filter bank */
        float d0 = (h - s0) * k; s0 += d0; float e  = h - s0;
        float d1 = (e - s1) * k; s1 += d1; float e2 = e - s1;

        float m5_sq = s2 + (s0 * s0 - s2) * k; s2 = m5_sq;
        float m4_sq = s3 + (s1 * s1 - s3) * k; s3 = m4_sq;
        float m3_sq = s4 + (e2 * e2 - s4) * k; s4 = m3_sq;

        float m5 = fast_sqrt(m5_sq);
        float m4 = fast_sqrt(m4_sq);
        float m3 = fast_sqrt(m3_sq);

        float sum = m3 + m4 + m5;
        float inv = (sum > 1.19e-7f) ? 255.0f / sum : 0.0f;

        uint8_t r = (uint8_t)(m5 * inv + 0.5f);
        uint8_t g = (uint8_t)(m4 * inv + 0.5f);
        uint8_t b = (uint8_t)(m3 * inv + 0.5f);

        /* Set color */
        uint64_t col64 = PackColor64(r, g, b, 0xFF);
        GdiPaint paint;
        ConstructPaint(&paint, &col64, 1, 0);
        SetPaint(device, &paint);

        /* Draw column vertical slice */
        int cur_x = start_x + i;
        GdiPoint pt1 = { cur_x, (int32_t)(y_top + 0.5f) };
        GdiPoint pt2 = { cur_x, (int32_t)(y_bot + 0.5f) };

        MoveTo(device, &pt1);
        LineTo(device, &pt2);

        DestructPaint(&paint);
    }
}
