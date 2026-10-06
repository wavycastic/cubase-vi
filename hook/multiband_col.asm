; multiband_col.asm - Per-column Multiband Color Generator for Cubase 15 Rasterizer
; Called directly inside the column loop at 0x141EA7BCC

_TEXT SEGMENT

ALIGN 16
c_k       DD 0.0615118
c_half    DD 0.5
c_eps     DD 1.1920929e-7
c_255     DD 255.0
c_scale   DD 4.0

; Static filter state across columns of the current event
s0        DD 0.0
s1        DD 0.0
s2        DD 0.0
s3        DD 0.0
s4        DD 0.0

PUBLIC MultibandColColor
MultibandColColor PROC
    ; Context on entry:
    ;   rbp = frame pointer of 0x141EA7840
    ;   r12d = column index (0 for first column)
    ;   rdi = [r14 + 8]
    ;   r13 = offset (r12d * 4)
    ;   [rsp + 74h] = y_top (int32)
    ;   [rsp + 7Ch] = y_bot (int32)

    ; Preserve scratch registers that 0x141EA7840 needs
    push    rbx
    push    rdx
    push    rsi

    ; If first column (r12d == 0), reset filter states
    test    r12d, r12d
    jnz     _filter
    xorps   xmm0, xmm0
    movss   s0, xmm0
    movss   s1, xmm0
    movss   s2, xmm0
    movss   s3, xmm0
    movss   s4, xmm0

_filter:
    ; Height h = (y_bot - y_top) in pixels
    ; Note: due to 'push rbx, rdx, rsi' (24 bytes = 18h),
    ; stack offset changes from [rsp + 74h] to [rsp + 74h + 18h] = [rsp + 8Ch]
    ; and [rsp + 7Ch] to [rsp + 7Ch + 18h] = [rsp + 94h]
    mov     eax, dword ptr [rsp + 94h]  ; y_bot
    sub     eax, dword ptr [rsp + 8Ch]  ; y_bot - y_top
    jns     _h_pos
    neg     eax
_h_pos:
    cvtsi2ss xmm0, eax                  ; xmm0 = h (float)

    ; Scale h slightly to increase frequency contrast
    mulss   xmm0, c_scale

    ; Load filter states
    movss   xmm1, s0
    movss   xmm2, s1
    movss   xmm3, s2
    movss   xmm4, s3
    movss   xmm5, s4
    movss   xmm6, c_k

    ; d0 = (h - s0) * k; s0 += d0; e = h - s0
    movaps  xmm7, xmm0
    subss   xmm7, xmm1
    mulss   xmm7, xmm6
    addss   xmm1, xmm7                  ; new s0
    movss   s0, xmm1
    movaps  xmm8, xmm0
    subss   xmm8, xmm1                  ; xmm8 = e

    ; d1 = (e - s1) * k; s1 += d1; e2 = e - s1
    movaps  xmm7, xmm8
    subss   xmm7, xmm2
    mulss   xmm7, xmm6
    addss   xmm2, xmm7                  ; new s1
    movss   s1, xmm2
    movaps  xmm9, xmm8
    subss   xmm9, xmm2                  ; xmm9 = e2

    ; s2 = s2 + (s0*s0 - s2) * k
    movaps  xmm7, xmm1
    mulss   xmm7, xmm1
    subss   xmm7, xmm3
    mulss   xmm7, xmm6
    addss   xmm3, xmm7                  ; new s2 (m5_sq)
    movss   s2, xmm3

    ; s3 = s3 + (s1*s1 - s3) * k
    movaps  xmm7, xmm2
    mulss   xmm7, xmm2
    subss   xmm7, xmm4
    mulss   xmm7, xmm6
    addss   xmm4, xmm7                  ; new s3 (m4_sq)
    movss   s3, xmm4

    ; s4 = s4 + (e2*e2 - s4) * k
    movaps  xmm7, xmm9
    mulss   xmm7, xmm9
    subss   xmm7, xmm5
    mulss   xmm7, xmm6
    addss   xmm5, xmm7                  ; new s4 (m3_sq)
    movss   s4, xmm5

    ; m5 = sqrt(max(0, s2)) -> Low (Red)
    xorps   xmm7, xmm7
    maxss   xmm3, xmm7
    sqrtss  xmm3, xmm3                  ; xmm3 = m5 (Red)

    ; m4 = sqrt(max(0, s3)) -> Mid (Green)
    maxss   xmm4, xmm7
    sqrtss  xmm4, xmm4                  ; xmm4 = m4 (Green)

    ; m3 = sqrt(max(0, s4)) -> High (Blue)
    maxss   xmm5, xmm7
    sqrtss  xmm5, xmm5                  ; xmm5 = m3 (Blue)

    ; sum = m3 + m4 + m5
    movaps  xmm0, xmm3
    addss   xmm0, xmm4
    addss   xmm0, xmm5

    ; inv = (sum > eps) ? 255.0 / sum : 0.0
    ucomiss xmm0, c_eps
    jbe     _fallback_col
    movss   xmm1, c_255
    divss   xmm1, xmm0                  ; xmm1 = inv

    ; Compute R, G, B
    movss   xmm2, c_half
    mulss   xmm3, xmm1
    addss   xmm3, xmm2
    cvttss2si ecx, xmm3                 ; ecx = R (0..255)

    mulss   xmm4, xmm1
    addss   xmm4, xmm2
    cvttss2si edx, xmm4                 ; edx = G (0..255)

    mulss   xmm5, xmm1
    addss   xmm5, xmm2
    cvttss2si eax, xmm5                 ; eax = B (0..255)

    ; Clamp to 255
    cmp     ecx, 255
    jle     _cl_r
    mov     ecx, 255
_cl_r:
    cmp     edx, 255
    jle     _cl_g
    mov     edx, 255
_cl_g:
    cmp     eax, 255
    jle     _cl_b
    mov     eax, 255
_cl_b:
    ; Pack into 32-bit ARGB:
    ; [31..24] = 0xFF (Alpha)
    ; [23..16] = R
    ; [15..8]  = G
    ; [7..0]   = B
    movzx   ecx, cl
    movzx   edx, dl
    movzx   eax, al
    shl     ecx, 16
    shl     edx, 8
    or      eax, ecx
    or      eax, edx
    or      eax, 0FF000000h             ; eax = 0xFF_RR_GG_BB
    jmp     _store_col

_fallback_col:
    ; Fallback: cyan/blue default
    mov     eax, 0FF2378EBh

_store_col:
    ; Store color into [rbp - 6Ch] (the column color in 0x141EA7840)
    mov     dword ptr [rbp - 6Ch], eax

    ; Restore preserved registers
    pop     rsi
    pop     rdx
    pop     rbx

    ; Perform original required instructions:
    ;   0x141EA7BF0: mov rax, qword ptr [rdi]
    ;   0x141EA7BF3: mov ecx, dword ptr [rax + r13]
    ;   0x141EA7BF7: mov dword ptr [rbp - 70h], ecx
    mov     rax, qword ptr [rdi]
    mov     ecx, dword ptr [rax + r13]
    mov     dword ptr [rbp - 70h], ecx

    ret
MultibandColColor ENDP

_TEXT ENDS

END
