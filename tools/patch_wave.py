#!/usr/bin/env python3
r"""Cong cu Binary Patch truc tiep vao Cubase15.exe de to mau dải song kieu FL Studio.

Khong can runtime DLL hook, khong can injector, chay vinh vien va hoan toan doc lap.
Tu dong sao luu Cubase15.exe -> Cubase15.exe.bak va cho phep khoi phuc 1 lenh.

Co che:
  1. Tai 0x141E9AD93 (trong ham to dai song 0x141E9AD10), thay the `call 0x141ea8150` (5 byte)
     bang `call <code_cave>` nhay vao vung dem 77 byte o cuoi section .text.
  2. Trong code cave:
     - Ghi ma mau 64-bit vao style->fill_color (+0x50)
     - Ghi ma mau 64-bit vao style->outline_color (+0x88)
     - Bat bitfield co fill + outline (+0xB0)
     - Nhay tiep toi ham goc 0x141ea8150 (jmp rel32).
  3. Hoan toan giu nguyen kich thuoc file PE, khong lech offset bat ky section nao.

Cach dung:
  python tools/patch_wave.py status                          # Kiem tra trang thai
  python tools/patch_wave.py apply                           # Patch mau Neon Blue (mac dinh)
  python tools/patch_wave.py apply --preset orange           # Patch mau Orange Beat
  python tools/patch_wave.py apply --preset cyan             # Patch mau Cyan Glow
  python tools/patch_wave.py apply --fill 2378EB --outline 6EDCFF # Mau tu chon
  python tools/patch_wave.py restore                         # Khoi phuc tu file .bak
"""
import argparse
import os
import shutil
import struct
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

VA_CALL_SITE = 0x141E9AD93
VA_TARGET_FUNC = 0x141EA8150
ORIG_CALL_BYTES = bytes((0xE8, 0xB8, 0xD3, 0x00, 0x00))  # call 0x141ea8150

PRESETS = {
    'neon_blue': {
        'name': 'FL Studio Playlist Neon Blue',
        'fill': (35, 120, 235),
        'outline': (110, 220, 255),
    },
    'orange': {
        'name': 'FL Studio Beat Warm Orange',
        'fill': (245, 110, 30),
        'outline': (255, 195, 80),
    },
    'cyan': {
        'name': 'FL Studio Cyan Glow',
        'fill': (20, 190, 160),
        'outline': (100, 255, 230),
    },
}


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


def encode_wave_color(r, g, b, a=255):
    """Mã hoá màu Cubase 64-bit: 4x uint16_t (R, G, B, A) little-endian."""
    r16 = (r & 0xFF) << 8
    g16 = (g & 0xFF) << 8
    b16 = (b & 0xFF) << 8
    a16 = (a & 0xFF) << 8
    return (a16 << 48) | (b16 << 32) | (g16 << 16) | r16


def build_code_cave(va_cave, fill_col64, outline_col64):
    cave = bytearray()
    # mov rax, fill_col64 (48 B8 <8 bytes>)
    cave += b'\x48\xb8' + struct.pack('<Q', fill_col64)
    # mov [rdi + 0x50], rax (48 89 47 50)
    cave += b'\x48\x89\x47\x50'
    # mov rax, outline_col64 (48 B8 <8 bytes>)
    cave += b'\x48\xb8' + struct.pack('<Q', outline_col64)
    # mov [rdi + 0x88], rax (48 89 87 88 00 00 00)
    cave += b'\x48\x89\x87\x88\x00\x00\x00'
    # or dword ptr [rdi + 0xB0], 3 (83 8F B0 00 00 00 03)
    cave += b'\x83\x8f\xb0\x00\x00\x00\x03'
    # jmp va_target_func (E9 <rel32>)
    va_after_jmp = va_cave + len(cave) + 5
    rel32_jmp = VA_TARGET_FUNC - va_after_jmp
    cave += b'\xe9' + struct.pack('<i', rel32_jmp)
    return bytes(cave)


def parse_hex_color(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError(f"Ma mau phai gom 6 ky tu hex (vi du: 2378EB), nhan: {hex_str}")
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def inspect_status(exe_path):
    pe = PE(str(exe_path))
    rva_call = VA_CALL_SITE - pe.imagebase
    off_call = pe.rva_to_off(rva_call)
    cur_call = pe.bin.data[off_call:off_call + 5]

    sec_text = [s for s in pe.sections if s.name == '.text'][0]
    rva_cave = sec_text.vaddr + sec_text.vsize
    off_cave = sec_text.raw_ptr + sec_text.vsize
    va_cave = pe.imagebase + rva_cave

    print(f"File: {exe_path}")
    print(f"Call site (0x{VA_CALL_SITE:X}, off 0x{off_call:X}): {cur_call.hex()}")

    if cur_call == ORIG_CALL_BYTES:
        print("  -> Trang thai: NGUYEN BAN (Goc, chua patch)")
    elif cur_call[0] == 0xE8:
        rel = struct.unpack('<i', cur_call[1:5])[0]
        dest = VA_CALL_SITE + 5 + rel
        if dest == va_cave:
            print(f"  -> Trang thai: DA PATCH (tro toi cave 0x{va_cave:X})")
            cave_bytes = pe.bin.data[off_cave:off_cave + 43]
            if len(cave_bytes) >= 12 and cave_bytes[:2] == b'\x48\xb8':
                fill_val = struct.unpack('<Q', cave_bytes[2:10])[0]
                rf = (fill_val >> 8) & 0xFF
                gf = (fill_val >> 24) & 0xFF
                bf = (fill_val >> 40) & 0xFF
                print(f"     Fill color: RGB({rf}, {gf}, {bf})")
        else:
            print(f"  -> Trang thai: TUY BIEN (dest = 0x{dest:X})")
    else:
        print("  -> Trang thai: KHONG XAC DINH")

    bak_path = exe_path.with_suffix('.exe.bak')
    print(f"File sao luu .bak: {'Co' if bak_path.exists() else 'Chua co'}")


def apply_patch(exe_path, fill_rgb, outline_rgb, dry_run=False):
    pe = PE(str(exe_path))
    rva_call = VA_CALL_SITE - pe.imagebase
    off_call = pe.rva_to_off(rva_call)
    cur_call = pe.bin.data[off_call:off_call + 5]

    sec_text = [s for s in pe.sections if s.name == '.text'][0]
    rva_cave = sec_text.vaddr + sec_text.vsize
    off_cave = sec_text.raw_ptr + sec_text.vsize
    va_cave = pe.imagebase + rva_cave
    slack_len = sec_text.raw_size - sec_text.vsize

    if cur_call != ORIG_CALL_BYTES and cur_call[0] != 0xE8:
        sys.exit(f"LOI: Byte tai call site khong khop mau an toan: {cur_call.hex()}")

    fill_val = encode_wave_color(*fill_rgb)
    outl_val = encode_wave_color(*outline_rgb)
    cave_code = build_code_cave(va_cave, fill_val, outl_val)

    if len(cave_code) > slack_len:
        sys.exit(f"LOI: Code cave ({len(cave_code)} bytes) vuot qua slack ({slack_len} bytes)")

    rel32_call = va_cave - (VA_CALL_SITE + 5)
    patch_call = b'\xe8' + struct.pack('<i', rel32_call)

    print(f"=== Thong so patch ===")
    print(f"  Fill color   : RGB{fill_rgb} -> 0x{fill_val:016X}")
    print(f"  Outline color: RGB{outline_rgb} -> 0x{outl_val:016X}")
    print(f"  Code cave    : off 0x{off_cave:X} (VA 0x{va_cave:X}, {len(cave_code)} bytes)")
    print(f"  Patch call   : off 0x{off_call:X} -> {patch_call.hex()}")

    if dry_run:
        print("[DRY-RUN] Kiem tra hoan tat, khong ghi file.")
        return

    # Tao ban sao luu neu chua co
    bak_path = exe_path.with_suffix('.exe.bak')
    if not bak_path.exists():
        print(f"Dang tao ban sao luu an toan -> {bak_path.name}...")
        shutil.copy2(exe_path, bak_path)
        print("  Da tao ban sao luu.")

    pe.close()

    # Ghi truc tiep vao file
    with open(exe_path, 'r+b') as f:
        # 1. Ghi code cave vao slack
        f.seek(off_cave)
        f.write(cave_code)
        # 2. Ghi lenh call vao call site
        f.seek(off_call)
        f.write(patch_call)

    print(f"THANH CONG: Da patch Cubase15.exe!")
    print(f"Mo Cubase 15 de trai nghiem dai song moi.")


def restore_backup(exe_path):
    bak_path = exe_path.with_suffix('.exe.bak')
    if not bak_path.exists():
        sys.exit(f"LOI: Khong tim thay file sao luu {bak_path}")

    print(f"Dang khoi phuc {exe_path.name} tu {bak_path.name}...")
    shutil.copy2(bak_path, exe_path)
    print("THANH CONG: Da khoi phuc file Cubase15.exe ve trang thai ban dau.")


def main():
    parser = argparse.ArgumentParser(description="Direct Waveform Binary Patcher for Cubase 15")
    parser.add_argument('action', choices=['status', 'apply', 'restore'],
                        help="Thao tac can thuc hien")
    parser.add_argument('--exe', help="Duong dan Cubase15.exe tuy chon")
    parser.add_argument('--preset', choices=list(PRESETS.keys()), default='neon_blue',
                        help="Preset mau: neon_blue (mac dinh), orange, cyan")
    parser.add_argument('--fill', help="Ma mau fill tuy chon (hex, vi du: 2378EB)")
    parser.add_argument('--outline', help="Ma mau outline tuy chon (hex, vi du: 6EDCFF)")
    parser.add_argument('--dry-run', action='store_true', help="Chay thu nghiem khong ghi file")

    args = parser.parse_args()
    exe_path = find_cubase_exe(args.exe)

    if args.action == 'status':
        inspect_status(exe_path)
    elif args.action == 'restore':
        restore_backup(exe_path)
    elif args.action == 'apply':
        preset = PRESETS[args.preset]
        fill_rgb = parse_hex_color(args.fill) if args.fill else preset['fill']
        outl_rgb = parse_hex_color(args.outline) if args.outline else preset['outline']
        print(f"Chon preset: {preset['name']}")
        apply_patch(exe_path, fill_rgb, outl_rgb, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
