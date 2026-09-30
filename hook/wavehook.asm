; wavehook.asm - stub hook cho ham ve duong song cua Cubase 15.
;
; Muc tieu: ham ve song la RVA 0x1E9E140, chi co MOT noi goi
; (0x1E9B9AB), nen hook bang JMP o dau ham la du.
;
; ------------------------------------------------------------------------
; VET 15 BYTE, KHONG PHAI 5
; ------------------------------------------------------------------------
; Ham ve bat dau bang 4 lenh chi la "doi thoat so" - khong can lam gi
; ve nghiep vu:
;
;   0x141E9E140  48 8B C4        mov rax, rsp          (3 byte)
;   0x141E9E143  4C 89 48 20     mov [rax+0x20], r9   (4 byte)
;   0x141E9E147  4C 89 40 18     mov [rax+0x18], r8   (4 byte)
;   0x141E9E14B  48 89 50 10     mov [rax+0x10], rdx  (4 byte)
;                                                  tong 15 byte
;
; 15 la diem dung lenh, va la MOT KHOANG TRON NHO. Nen ta ghi de ca 15
; byte nay bang lenh nhay 13 byte + 2 NOP, roi copy 15 byte do sang
; trampoline de chay tiep.
;
; ------------------------------------------------------------------------
; VET 13 BYTE: NHAAY TUYET DOI, KHONG PHAI REL32
; ------------------------------------------------------------------------
; Ban dau ghi 5 byte `E9 rel32`. Do chi với duoc tu -2 GB den +2 GB, con
; DLL voi Cubase cach nhau hang tram GB, nen rel32 bi cat con lai 4 byte
; thap va JMP nhay vao vung bo nho chua cap - tien trinh chet ngay. Da gap
; dung loi nay: minidump ghi RIP vao mot ban sao DLL o dia chi khac.
;
; Dung `mov r11, imm64` + `jmp r11` thi 13 byte va khong gioi han khoang
; cach nao. r11 la thanh ghi "volatile" trong ABI Windows x64, nen bay toan
; bo thanh ghi khac giu nguyen; ra khoi ham bang `jmp` chu khong phai
; `ret`, nen r11 co the lam ban tuy y.
;
; ------------------------------------------------------------------------
; CANH 16 BYTE - BAT BUOC PHAI CANH
; ------------------------------------------------------------------------
; Khi vao mot ham, rsp = 8 (mod 16) vi return address da duoc day vao, va
; TRUOC moi `call` rsp phai = 0 (mod 16). Sau 8 lenh push (64 byte) thi
; canh khong doi, nen `sub rsp` phai cong them so le: 8 + 0x40 + 0x48 =
; 0x90, chia het 16. `sub rsp, 40h` se lam moi `call` lech 8 byte va ham C
; ben trong se chet ngay tren lenh MOVAPS.
;
; Vung [rsp+00h..1Fh] la shadow space cua lenh call - ham duoi duoc phep
; xoa, nen KHONG giu tham so o do. Luu tu [rsp+20h] tro len.

include wavehook.inc

_TEXT SEGMENT

; Cac hang so dung chung voi wavehook.c (xem wavehook.inc).

; ---------------------------------------------------------------------
; WaveDrawHook - dieu huong vao ham ve cua Cubase
;
; rcx, rdx, r8, r9 = tham so 1..4
; [rsp+0x20]        = tham so 5
;
; Khong `ret` - nhai thang cho trampoline, de bo nho cua Cubase giu nguyen
; nguyen trang.
; ---------------------------------------------------------------------
PUBLIC WaveDrawHook
WaveDrawHook PROC
    push    rbp
    push    rbx
    push    rsi
    push    rdi
    push    r12
    push    r13
    push    r14
    push    r15
    sub     rsp, 48h

    mov     [rsp+20h], rcx
    mov     [rsp+28h], rdx
    mov     [rsp+30h], r8
    mov     [rsp+38h], r9
    mov     rax, [rsp+88h+20h]        ; tham so 5, tren khung goc da day
    mov     [rsp+40h], rax

    call    WaveDrawHook_C

    mov     rcx, [rsp+20h]
    mov     rdx, [rsp+28h]
    mov     r8,  [rsp+30h]
    mov     r9,  [rsp+38h]
    mov     rax, [rsp+40h]

    add     rsp, 48h
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rdi
    pop     rsi
    pop     rbx
    pop     rbp

    ; Nhay ve TRAMPOLINE - noi chay lai 15 byte da doi chieu cua ham goc.
    ; KHONG nhay thang ve `WaveDrawResumeVA`: 4 lenh "doi thoat so" o giua
    ; phai duoc chay, bo qua chung se lam ham goc thay sai gia tri tham so.
    lea     rax, [WaveDrawTrampolineVA]
    jmp     qword ptr [rax]
WaveDrawHook ENDP

; ---------------------------------------------------------------------
; WaveDrawTrampoline
;
; 15 byte dau cua ham goc (xem giai thich o dau file), roi nhay ve
; `WaveDrawResumeVA` - ma DLL gan bang `hook + 15` khi cai dat.
; ---------------------------------------------------------------------
PUBLIC WaveDrawTrampoline
WaveDrawTrampoline PROC
    mov     rax, rsp                 ; 48 8B C4
    mov     [rax+20h], r9            ; 4C 89 48 20
    mov     [rax+18h], r8            ; 4C 89 40 18
    mov     [rax+10h], rdx           ; 48 89 50 10
    lea     rax, [WaveDrawResumeVA]
    jmp     qword ptr [rax]
WaveDrawTrampoline ENDP

; ---------------------------------------------------------------------
; WaveProbeCommon - phan dung chung cho bo dem nhieu diem
;
; Moi diem can do co MOT stub rieng sinh ra luc chay, stub do nap r11 =
; dia chi diem do roi nhay vao day. Nho vay handler biet dang so dem cho
; diem nao, ma van phai giu nguyen toan bo thanh ghi cho ham dich.
;
; r11 phai duoc day xuong DAU TIEN truoc khi lam gi khac, vi no mang thong
; tin diem can dem.
;
; Cac lenh nhay giua cac khu vuc deu dung dang tuyet doi (mov r11/r10 +
; jmp), vi khu vuc sinh ra bang VirtualAlloc co the nam xa hon 2 GB so
; voi DLL nen rel32 khong duoc tin.
; ---------------------------------------------------------------------
PUBLIC WaveProbeCommon
WaveProbeCommon PROC
    push    r11                      ; dia chi diem can dem
    push    rbp
    push    rbx
    push    rsi
    push    rdi
    push    r12
    push    r13
    push    r14
    push    r15
    ; CANH: 9 lenh push = 0x48 byte. rsp luc vao ham = 8 (mod 16). Sau 0x48
    ; byte, rsp = 0 (mod 16) - da canh dung cho `call`. `sub` tiep phai
    ; cong mot so CHAN (0x40) de giu nguyen canh do. Dung `sub rsp, 48h` se
    ; lam lech 8 byte va moi `call` vao ham C se chet.
    sub     rsp, 40h

    mov     [rsp+20h], r11
    mov     [rsp+28h], rcx
    mov     [rsp+30h], rdx
    mov     [rsp+38h], r8

    ; Chuoi vao C theo quy uoc Win64: rcx = tham so 1, rdx = tham so 2.
    ; `WaveProbe_C` can `r11` nen phai day no xuong tham so.
    mov     rdx, rcx                  ; tham so 2 = tham so 1 cua ham dich
    mov     rcx, r11                  ; tham so 1 = dia chi diem can dem
    call    WaveProbe_C

    mov     r11, [rsp+20h]
    mov     rcx, [rsp+28h]
    mov     rdx, [rsp+30h]
    mov     r8,  [rsp+38h]

    add     rsp, 48h
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rdi
    pop     rsi
    pop     rbx
    pop     rbp
    pop     r11

    lea     rax, [WaveProbeTrampVA]
    jmp     qword ptr [rax]
WaveProbeCommon ENDP

_TEXT ENDS

END
