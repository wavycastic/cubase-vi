#!/usr/bin/env python3
r"""Cong cu Binary Patch truc tiep vao Cubase15.exe de kich hoat Multiband Waveform.

Khong can runtime DLL hook, khong can injector, chay vinh vien va hoan toan doc lap.
Tu dong sao luu Cubase15.exe -> Cubase15.exe.bak va cho phep khoi phuc 1 lenh.

Co che:
  1. Bo sung section `.wave` (4096 bytes) vao file PE Cubase15.exe (tan dung 48 bytes trong PE header).
  2. Nap bo ma may thuan Multiband DSP Renderer vao section `.wave`:
     - Bo loc 5 mot cuc FL Studio (WaveColour_Next) phan tich pho tan so (Bass, Mid, Treble)
     - Tu dong gan mau: Bass = Do/Cam, Mid = Xanh luc, Treble = Xanh lam/Tim
     - Goi truc tiep lenh ve GDI/D2D cua thiet bi Cubase (MoveTo, LineTo, SetPaint)
  3. Tai 0x141E9E649 (Channel 0) va 0x141E9E75A (Channel 1):
     Thay the lenh ve da giac don sac cu bang lenh goi BridgeChannel0 / BridgeChannel1.

Cach dung:
  python tools/patch_multiband.py status       # Kiem tra trang thai
  python tools/patch_multiband.py apply        # Ap dung patch Multiband
  python tools/patch_multiband.py restore      # Khoi phuc ban goc
"""
import argparse
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from cubelib.pe import PE  # noqa: E402

DEFAULT_CUBASE_PATHS = [
    Path(r"E:\Steinberg\Cubase 15\Cubase15.exe"),
    Path(r"C:\Program Files\Steinberg\Cubase 15\Cubase15.exe"),
    Path(r"D:\Steinberg\Cubase 15\Cubase15.exe"),
]

VA_SITE_CH0 = 0x141E9E649
VA_SITE_CH1 = 0x141E9E75A
ORIG_CH0_BYTES = bytes((0xE8, 0xC2, 0xC6, 0xFF, 0xFF))  # call 0x141e9ad10
ORIG_CH1_BYTES = bytes((0xE8, 0xB1, 0xC5, 0xFF, 0xFF))  # call 0x141e9ad10


def find_cubase_exe(custom_path=None):
    if custom_path:
        p = Path(custom_path)
        if p.is_file():
            return p
        sys.exit(f"LOI: Khong tim thay file tai {custom_path}")
    for p in DEFAULT_CUBASE_PATHS:
        if p.is_file():
            return p
    sys.exit("LOI: Khong tim thay Cubase15.exe o cac thu muc mac dinh.")


def assemble_payload():
    """Bien dich hook/multiband_full.asm bang ml64.exe va tra ve ma may hoan chinh."""
    asm_file = ROOT / 'hook' / 'multiband_full.asm'
    obj_file = ROOT / 'multiband_full.obj'

    tools_root = Path(r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC')
    if not tools_root.exists():
        sys.exit("LOI: Khong tim thay MSVC BuildTools.")
    vc = tools_root / sorted(p.name for p in tools_root.iterdir() if p.is_dir())[-1]
    ml64 = vc / 'bin' / 'Hostx64' / 'x64' / 'ml64.exe'

    cmd = [str(ml64), '/nologo', '/c', str(asm_file)]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"LOI ml64: {r.stderr or r.stdout}")

    with open(obj_file, 'rb') as f:
        d = f.read()

    hdr = d[20:60]
    size, ptr = struct.unpack_from('<II', hdr, 16)
    code = bytearray(d[ptr:ptr + size])

    # 5 relocations noi bo trong section .text$mn cua multiband_full.obj
    # vaddr -> sym_offset
    relocs = [
        (0xAD, 0x00),  # c_k
        (0xB5, 0x04),  # c_half
        (0xBE, 0x08),  # c_eps
        (0xC7, 0x0C),  # c_255
        (0xFB, 0x10),  # c_sign
    ]
    for vaddr, target in relocs:
        disp32 = target - (vaddr + 4)
        struct.pack_into('<i', code, vaddr, disp32)

    return bytes(code)


def add_wave_section(data, sec_size=0x1000):
    """Them section .wave vao bytearray PE neu chua co."""
    e_lfanew = struct.unpack_from('<I', data, 0x3C)[0]
    num_sections = struct.unpack_from('<H', data, e_lfanew + 6)[0]
    opt_hdr_size = struct.unpack_from('<H', data, e_lfanew + 0x14)[0]
    sec_align = struct.unpack_from('<I', data, e_lfanew + 0x18 + 0x20)[0]
    file_align = struct.unpack_from('<I', data, e_lfanew + 0x18 + 0x24)[0]
    size_of_headers = struct.unpack_from('<I', data, e_lfanew + 0x18 + 0x3C)[0]

    sec_tbl_start = e_lfanew + 0x18 + opt_hdr_size
    sec_tbl_end = sec_tbl_start + num_sections * 40

    # Kiem tra neu section .wave da ton tai
    for i in range(num_sections):
        s_hdr = data[sec_tbl_start + i * 40 : sec_tbl_start + (i + 1) * 40]
        s_name = s_hdr[:8].rstrip(b'\x00').decode('ascii', errors='replace')
        if s_name == '.wave':
            s_vsize, s_vaddr, s_raw_size, s_raw_ptr = struct.unpack_from('<IIII', s_hdr, 8)
            return s_vaddr, s_raw_ptr

    if sec_tbl_end + 40 > size_of_headers:
        raise ValueError("Khong du khoang trong PE header de them section moi.")

    last_hdr = data[sec_tbl_start + (num_sections - 1) * 40 : sec_tbl_start + num_sections * 40]
    last_vsize, last_vaddr, last_raw_size, last_raw_ptr = struct.unpack_from('<IIII', last_hdr, 8)

    next_vaddr = (last_vaddr + last_vsize + sec_align - 1) & ~(sec_align - 1)
    next_raw_ptr = (last_raw_ptr + last_raw_size + file_align - 1) & ~(file_align - 1)

    if len(data) < next_raw_ptr:
        data.extend(b'\x00' * (next_raw_ptr - len(data)))

    raw_size = (sec_size + file_align - 1) & ~(file_align - 1)
    virt_size = sec_size

    name_bytes = b'.wave\x00\x00\x00'
    characteristics = 0x60000020  # CODE | EXECUTE | READ
    new_hdr = struct.pack(
        '<8sIIIIIIHHI',
        name_bytes,
        virt_size,
        next_vaddr,
        raw_size,
        next_raw_ptr,
        0, 0, 0, 0,
        characteristics
    )

    data[sec_tbl_end : sec_tbl_end + 40] = new_hdr
    struct.pack_into('<H', data, e_lfanew + 6, num_sections + 1)

    new_image_size = (next_vaddr + virt_size + sec_align - 1) & ~(sec_align - 1)
    struct.pack_into('<I', data, e_lfanew + 0x18 + 0x38, new_image_size)

    data.extend(b'\x00' * raw_size)
    return next_vaddr, next_raw_ptr


def inspect_status(exe_path):
    pe = PE(str(exe_path))
    has_wave_sec = any(s.name == '.wave' for s in pe.sections)

    rva0 = VA_SITE_CH0 - pe.imagebase
    off0 = pe.rva_to_off(rva0)
    bytes0 = pe.bin.data[off0:off0 + 5]

    rva1 = VA_SITE_CH1 - pe.imagebase
    off1 = pe.rva_to_off(rva1)
    bytes1 = pe.bin.data[off1:off1 + 5]

    print(f"File: {exe_path}")
    print(f"Section .wave: {'Co' if has_wave_sec else 'Chua co'}")
    print(f"Call site CH0 (0x{VA_SITE_CH0:X}): {bytes0.hex(' ')}")
    print(f"Call site CH1 (0x{VA_SITE_CH1:X}): {bytes1.hex(' ')}")

    if bytes0 == ORIG_CH0_BYTES and bytes1 == ORIG_CH1_BYTES:
        print("  -> Trang thai: NGUYEN BAN (Chua patch Multiband)")
    elif has_wave_sec and bytes0[0] == 0xE8 and bytes1[0] == 0xE8:
        print("  -> Trang thai: DA PATCH MULTIBAND THANH CONG!")
    else:
        print("  -> Trang thai: KHAC (Custom)")

    bak_path = exe_path.with_suffix('.exe.bak')
    print(f"File sao luu .bak: {'Co' if bak_path.exists() else 'Chua co'}")


def apply_patch(exe_path, dry_run=False):
    payload_code = assemble_payload()
    print(f"Ma may Multiband payload: {len(payload_code)} bytes (San sang).")

    with open(exe_path, 'rb') as f:
        file_bytes = bytearray(f.read())

    # 1. Kiem tra/Them section .wave
    sec_vaddr, sec_raw_ptr = add_wave_section(file_bytes, sec_size=0x1000)
    va_wave = 0x140000000 + sec_vaddr
    print(f"Section .wave: VA 0x{va_wave:X}, file offset 0x{sec_raw_ptr:X}")

    # Bridge offsets
    va_bridge_ch0 = va_wave + 0x14
    va_bridge_ch1 = va_wave + 0x2F

    # Rel32 calls
    rel32_ch0 = va_bridge_ch0 - (VA_SITE_CH0 + 5)
    rel32_ch1 = va_bridge_ch1 - (VA_SITE_CH1 + 5)
    patch_ch0 = b'\xe8' + struct.pack('<i', rel32_ch0)
    patch_ch1 = b'\xe8' + struct.pack('<i', rel32_ch1)

    pe_tmp = PE(str(exe_path))
    off0 = pe_tmp.rva_to_off(VA_SITE_CH0 - pe_tmp.imagebase)
    off1 = pe_tmp.rva_to_off(VA_SITE_CH1 - pe_tmp.imagebase)
    pe_tmp.close()

    print(f"  Patch call CH0: off 0x{off0:X} -> {patch_ch0.hex(' ')} (call 0x{va_bridge_ch0:X})")
    print(f"  Patch call CH1: off 0x{off1:X} -> {patch_ch1.hex(' ')} (call 0x{va_bridge_ch1:X})")

    if dry_run:
        print("[DRY-RUN] Kiem tra hoan tat, khong ghi file.")
        return

    # Tao ban sao luu neu chua co
    bak_path = exe_path.with_suffix('.exe.bak')
    if not bak_path.exists():
        print(f"Dang tao ban sao luu an toan -> {bak_path.name}...")
        shutil.copy2(exe_path, bak_path)
        print("  Da tao ban sao luu.")

    # Ghi payload vao section .wave
    file_bytes[sec_raw_ptr : sec_raw_ptr + len(payload_code)] = payload_code

    # Ghi patch calls
    file_bytes[off0 : off0 + 5] = patch_ch0
    file_bytes[off1 : off1 + 5] = patch_ch1

    # Ghi file
    with open(exe_path, 'wb') as f:
        f.write(file_bytes)

    print("THANH CONG: Da patch Multiband Waveform truc tiep vao Cubase15.exe!")
    print("Mo Cubase 15 de trai nghiem dai song phan tach tan so da mau (FL Studio Multiband).")


def restore_backup(exe_path):
    bak_path = exe_path.with_suffix('.exe.bak')
    if not bak_path.exists():
        sys.exit(f"LOI: Khong tim thay file sao luu {bak_path}")

    print(f"Dang khoi phuc {exe_path.name} tu {bak_path.name}...")
    shutil.copy2(bak_path, exe_path)
    print("THANH CONG: Da khoi phuc file Cubase15.exe ve trang thai ban dau.")


def main():
    parser = argparse.ArgumentParser(description="Multiband Waveform Binary Patcher for Cubase 15")
    parser.add_argument('action', choices=['status', 'apply', 'restore'],
                        help="Thao tac can thuc hien")
    parser.add_argument('--exe', help="Duong dan Cubase15.exe tuy chon")
    parser.add_argument('--dry-run', action='store_true', help="Chay thu nghiem khong ghi file")

    args = parser.parse_args()
    exe_path = find_cubase_exe(args.exe)

    if args.action == 'status':
        inspect_status(exe_path)
    elif args.action == 'restore':
        restore_backup(exe_path)
    elif args.action == 'apply':
        apply_patch(exe_path, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
