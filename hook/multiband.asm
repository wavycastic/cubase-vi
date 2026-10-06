; multiband.asm - Pure flat standalone Multiband Waveform Renderer for Cubase 15
; Assembled with ml64.exe /c
; Fits entirely in .wave section of Cubase15.exe with ZERO external relocations.

_TEXT SEGMENT

ALIGN 16
c_k       DD 0.0615118
c_half    DD 0.5
c_eps     DD 1.1920929e-7
c_255     DD 255.0
c_sign    DD 7FFFFFFFh

PUBLIC MultibandRender
MultibandRender PROC
    ; Parameters:
    ;   rcx = device
    ;   rdx = col_data (float* y_top, y_bot)
    ;   r8d = num_cols
    ;   r9d = start_x

    test    rcx, rcx
    jz      _done
    test    rdx, rdx
    jz      _done
    test    r8d, r8d
    jle     _done

    push    rbx
    push    rsi
    push    rdi
    push    r12
    push    r13
    push    r14
    push    r15
    push    rbp
    sub     rsp, 88h

    mov     r14, rcx                  ; r14 = device
    mov     rsi, rdx                  ; rsi = col_data
    mov     ebp, r8d                  ; ebp = num_cols
    mov     edi, r9d                  ; edi = current_x

    mov     rax, qword ptr [r14]      ; device vtable
    mov     r12, qword ptr [rax + 8]  ; MoveTo
    mov     r15, qword ptr [rax + 0]  ; LineTo
    mov     r13, qword ptr [rax + 80h]; SetPaint

    ; Filter states (s0, s1, s2, s3, s4) = 0
    xorps   xmm10, xmm10              ; s0
    xorps   xmm11, xmm11              ; s1
    xorps   xmm12, xmm12              ; s2
    xorps   xmm13, xmm13              ; s3
    xorps   xmm14, xmm14              ; s4

    movss   xmm6, c_k
    movss   xmm7, c_half
    movss   xmm8, c_eps
    movss   xmm9, c_255

    xor     ebx, ebx                  ; i = 0

_loop:
    cmp     ebx, ebp
    jge     _cleanup

    ; Read y_top, y_bot
    movss   xmm0, dword ptr [rsi + rbx*8]     ; y_top
    movss   xmm1, dword ptr [rsi + rbx*8 + 4] ; y_bot

    ; Check if empty column (both 0.0)
    xorps   xmm2, xmm2
    ucomiss xmm0, xmm2
    jnz     _not_empty
    ucomiss xmm1, xmm2
    jz      _next_col

_not_empty:
    ; h = fabsf(y_bot - y_top)
    movaps  xmm2, xmm1
    subss   xmm2, xmm0
    andps   xmm2, c_sign                      ; xmm2 = h

    ; d0 = (h - s0) * k; s0 += d0; e = h - s0
    movaps  xmm3, xmm2
    subss   xmm3, xmm10
    mulss   xmm3, xmm6
    addss   xmm10, xmm3
    movaps  xmm4, xmm2
    subss   xmm4, xmm10               ; xmm4 = e

    ; d1 = (e - s1) * k; s1 += d1; e2 = e - s1
    movaps  xmm3, xmm4
    subss   xmm3, xmm11
    mulss   xmm3, xmm6
    addss   xmm11, xmm3
    movaps  xmm5, xmm4
    subss   xmm5, xmm11               ; xmm5 = e2

    ; s2 = s2 + (s0*s0 - s2) * k
    movaps  xmm3, xmm10
    mulss   xmm3, xmm10
    subss   xmm3, xmm12
    mulss   xmm3, xmm6
    addss   xmm12, xmm3               ; m5_sq

    ; s3 = s3 + (s1*s1 - s3) * k
    movaps  xmm3, xmm11
    mulss   xmm3, xmm11
    subss   xmm3, xmm13
    mulss   xmm3, xmm6
    addss   xmm13, xmm3               ; m4_sq

    ; s4 = s4 + (e2*e2 - s4) * k
    movaps  xmm3, xmm5
    mulss   xmm3, xmm5
    subss   xmm3, xmm14
    mulss   xmm3, xmm6
    addss   xmm14, xmm3               ; m3_sq

    ; m5 = sqrt(max(0, m5_sq)) -> Low (Red)
    xorps   xmm3, xmm3
    maxss   xmm12, xmm3
    sqrtss  xmm3, xmm12

    ; m4 = sqrt(max(0, m4_sq)) -> Mid (Green)
    xorps   xmm4, xmm4
    maxss   xmm13, xmm4
    sqrtss  xmm4, xmm13

    ; m3 = sqrt(max(0, m3_sq)) -> High (Blue)
    xorps   xmm5, xmm5
    maxss   xmm14, xmm5
    sqrtss  xmm5, xmm14

    ; sum = m3 + m4 + m5
    movaps  xmm2, xmm3
    addss   xmm2, xmm4
    addss   xmm2, xmm5

    ; inv = (sum > eps) ? 255.0 / sum : 0.0
    ucomiss xmm2, xmm8
    jbe     _zero_col
    movaps  xmm15, xmm9
    divss   xmm15, xmm2
    jmp     _calc_rgb

_zero_col:
    xorps   xmm15, xmm15

_calc_rgb:
    ; r = (uint8)(m5 * inv + 0.5)
    mulss   xmm3, xmm15
    addss   xmm3, xmm7
    cvttss2si eax, xmm3
    movzx   ecx, al                   ; ecx = R

    ; g = (uint8)(m4 * inv + 0.5)
    mulss   xmm4, xmm15
    addss   xmm4, xmm7
    cvttss2si eax, xmm4
    movzx   edx, al                   ; edx = G

    ; b = (uint8)(m3 * inv + 0.5)
    mulss   xmm5, xmm15
    addss   xmm5, xmm7
    cvttss2si eax, xmm5
    movzx   eax, al                   ; eax = B

    ; Pack Cubase 64-bit color:
    ; col64 = (0xFF00 << 48) | (B << 40) | (G << 24) | (R << 8)
    shl     rax, 40
    shl     rdx, 24
    shl     rcx, 8
    or      rax, rdx
    or      rax, rcx
    mov     rdx, 0FF00000000000000h
    or      rax, rdx                  ; rax = col64

    ; Stack layout for calls:
    ; [rsp + 20h] = pt1 / paint
    ; [rsp + 28h] = pt2
    ; [rsp + 30h] = color storage
    ; [rsp + 40h] = GdiPaint buffer (32 bytes)

    mov     qword ptr [rsp + 30h], rax
    lea     rdx, [rsp + 30h]          ; &col64
    lea     rcx, [rsp + 40h]          ; &paint
    mov     r8d, 1                    ; mode = 1
    xor     r9d, r9d                  ; flags = 0
    mov     rax, 144A958D0h           ; ConstructPaint
    call    rax

    lea     rdx, [rsp + 40h]          ; &paint
    mov     rcx, r14                  ; device
    call    r13                       ; SetPaint(device, &paint)

    ; Calculate Y points
    addss   xmm0, xmm7                ; y_top + 0.5
    addss   xmm1, xmm7                ; y_bot + 0.5
    cvttss2si eax, xmm0
    cvttss2si edx, xmm1

    ; pt1 = { cur_x, y_top }
    mov     dword ptr [rsp + 20h], edi
    mov     dword ptr [rsp + 24h], eax
    ; pt2 = { cur_x, y_bot }
    mov     dword ptr [rsp + 28h], edi
    mov     dword ptr [rsp + 2Ch], edx

    lea     rdx, [rsp + 20h]
    mov     rcx, r14
    call    r12                       ; MoveTo(device, &pt1)

    lea     rdx, [rsp + 28h]
    mov     rcx, r14
    call    r15                       ; LineTo(device, &pt2)

    lea     rcx, [rsp + 40h]
    mov     rax, 144A95580h           ; DestructPaint
    call    rax

_next_col:
    inc     edi                       ; cur_x++
    inc     ebx                       ; i++
    jmp     _loop

_cleanup:
    add     rsp, 88h
    pop     rbp
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rdi
    pop     rsi
    pop     rbx

_done:
    ret
MultibandRender ENDP

_TEXT ENDS

END
