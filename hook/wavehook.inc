; wavehook.inc - ky hieu dung chung giua wavehook.asm va wavehook.c.
;
; MASM khong "thay" ky hieu C. Neu asm tu khai bao bien rieng, cong doan
; ghi dinh dich trong C se khong bao gio tro toi cung mot dia chi - hook
; se nhay ve cho trong. Nen phai khai bao o MOT noi va dua chung vao
; wavehook.def de linker dua no ra ngoai DLL.
;
; Do la nguyen nhan pho bien nhat khi viet hook cho binary la.

EXTRN WaveDrawHook_C:NEAR
EXTRN WaveProbe_C:NEAR
EXTRN WaveDrawTrampolineVA:DWORD
EXTRN WaveDrawResumeVA:DWORD
EXTRN WaveProbeTrampVA:DWORD

; Ham ve cua Cubase, RVA 0x1E9E140. Sau 7 byte vua ghi de la 0x1E9E147.
; Chi dung o nhung cho can gia tri gan, va luon tinh lai tu RVA de khi
; doi ban Cubase chi sua MOT cho.
CUBASE_WAVE_DRAW_RVA     EQU 01E9E140h
CUBASE_WAVE_DRAW_CONT    EQU 01E9E147h
