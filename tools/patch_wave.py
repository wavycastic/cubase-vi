#!/usr/bin/env python3
r"""Cong cu Binary Patch truc tiep vao Cubase15.exe de to mau dai song kieu FL Studio.

Khong can runtime DLL hook, khong can injector, chay vinh vien va hoan toan doc lap.
Tu dong sao luu Cubase15.exe -> Cubase15.exe.bak va cho phep khoi phuc 1 lenh.

Co che:
  Can thiep tai diem khoi tao bang mau PSeqEventImageScheme::buildScheme (0x14393BCC0).
  Day la noi Cubase 15 sinh bang mau cho dai song va vien song tu mau track:
  1. Tai 0x14393C4B4: thay the `mov [rbx + 0x98], rax` (7 byte)
     bang `call <code_cave>; nop; nop` nhay vao code cave trong vung dem .text slack.
  2. Trong code cave:
     - Nap rax = fill_color (mau dai song chinh)
     - Nap r11 = outline_color (mau vien sang kieu FL)
     - Ghi [rbx + 0x98] = rax
     - ret
  3. Tai 0x14393C4D7, 0x14393CBD5, 0x14393CE7F:
     Thay the `mov [rbx + 0x170], rax` bang `mov [rbx + 0x170], r11` (1 byte prefix 48 -> 4C)
     de vien song luon mang mau outline viền sang kieu FL Studio.

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

VA_SITE_FILL = 0x14393C4B4
ORIG_FILL_BYTES = bytes((0x48, 0x89, 0x83, 0x98, 0x00, 0x00, 0x00))  # mov [rbx+0x98], rax

VA_OUTLINE_SITES = [
    0x14393C4D7,
    0x14393CBD5,
    0x14393CE7F,
]
ORIG_OUTLINE_BYTES = bytes((0x48, 0x89, 0x83, 0x70, 0x01, 0x00, 0x00))  # mov [rbx+0x170], rax
PATCH_OUTLINE_BYTES = bytes((0x4C, 0x89, 0x9B, 0x70, 0x01, 0x00, 0x00)) # mov [rbx+0x170], r11

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


def build_code_cave(fill_col64, outline_col64):
    cave = bytearray()
    # movabs rax, fill_col64 (48 B8 <8 bytes>)
    cave += b'\x48\xb8' + struct.pack('<Q', fill_col64)
    # movabs r11, outline_col64 (49 BB <8 bytes>)
    cave += b'\x49\xbb' + struct.pack('<Q', outline_col64)
    # mov qword ptr [rbx + 0x98], rax (48 89 83 98 00 00 00)
    cave += b'\x48\x89\x83\x98\x00\x00\x00'
    # ret (C3)
    cave += b'\xc3'
    return bytes(cave)


def parse_hex_color(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError(f"Ma mau phai gom 6 ky tu hex (vi du: 2378EB), nhan: {hex_str}")
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def inspect_status(exe_path):
    pe = PE(str(exe_path))
    rva_fill = VA_SITE_FILL - pe.imagebase
    off_fill = pe.rva_to_off(rva_fill)
    cur_fill = pe.bin.data[off_fill:off_fill + 7]

    sec_text = [s for s in pe.sections if s.name == '.text'][0]
    rva_cave = sec_text.vaddr + sec_text.vsize
    off_cave = sec_text.raw_ptr + sec_text.vsize
    va_cave = pe.imagebase + rva_cave

    print(f"File: {exe_path}")
    print(f"Fill site (0x{VA_SITE_FILL:X}, off 0x{off_fill:X}): {cur_fill.hex(' ')}")

    if cur_fill == ORIG_FILL_BYTES:
        print("  -> Trang thai: NGUYEN BAN (Goc, chua patch)")
    elif cur_fill[0] == 0xE8:
        rel = struct.unpack('<i', cur_fill[1:5])[0]
        dest = VA_SITE_FILL + 5 + rel
        if dest == va_cave:
            print(f"  -> Trang thai: DA PATCH (tro toi cave 0x{va_cave:X})")
            cave_bytes = pe.bin.data[off_cave:off_cave + 28]
            if len(cave_bytes) >= 10 and cave_bytes[:2] == b'\x48\xb8':
                fill_val = struct.unpack('<Q', cave_bytes[2:10])[0]
                rf = (fill_val >> 8) & 0xFF
                gf = (fill_val >> 24) & 0xFF
                bf = (fill_val >> 40) & 0xFF
                print(f"     Fill color: RGB({rf}, {gf}, {bf})")
            if len(cave_bytes) >= 20 and cave_bytes[10:12] == b'\x49\xbb':
                out_val = struct.unpack('<Q', cave_bytes[12:20])[0]
                ro = (out_val >> 8) & 0xFF
                go = (out_val >> 24) & 0xFF
                bo = (out_val >> 40) & 0xFF
                print(f"     Outline color: RGB({ro}, {go}, {bo})")
        else:
            print(f"  -> Trang thai: TUY BIEN (dest = 0x{dest:X})")
    else:
        print("  -> Trang thai: KHONG XAC DINH")

    bak_path = exe_path.with_suffix('.exe.bak')
    print(f"File sao luu .bak: {'Co' if bak_path.exists() else 'Chua co'}")


def apply_patch(exe_path, fill_rgb, outline_rgb, dry_run=False):
    pe = PE(str(exe_path))
    rva_fill = VA_SITE_FILL - pe.imagebase
    off_fill = pe.rva_to_off(rva_fill)
    cur_fill = pe.bin.data[off_fill:off_fill + 7]

    sec_text = [s for s in pe.sections if s.name == '.text'][0]
    rva_cave = sec_text.vaddr + sec_text.vsize
    off_cave = sec_text.raw_ptr + sec_text.vsize
    va_cave = pe.imagebase + rva_cave
    slack_len = sec_text.raw_size - sec_text.vsize

    if cur_fill != ORIG_FILL_BYTES and cur_fill[0] != 0xE8:
        sys.exit(f"LOI: Byte tai fill site khong khop mau an toan: {cur_fill.hex(' ')}")

    fill_val = encode_wave_color(*fill_rgb)
    outl_val = encode_wave_color(*outline_rgb)
    cave_code = build_code_cave(fill_val, outl_val)

    if len(cave_code) > slack_len:
        sys.exit(f"LOI: Code cave ({len(cave_code)} bytes) vuot qua slack ({slack_len} bytes)")

    rel32_call = va_cave - (VA_SITE_FILL + 5)
    patch_call = b'\xe8' + struct.pack('<i', rel32_call) + b'\x90\x90'

    print(f"=== Thong so patch ===")
    print(f"  Fill color   : RGB{fill_rgb} -> 0x{fill_val:016X}")
    print(f"  Outline color: RGB{outline_rgb} -> 0x{outl_val:016X}")
    print(f"  Code cave    : off 0x{off_cave:X} (VA 0x{va_cave:X}, {len(cave_code)} bytes)")
    print(f"  Patch call   : off 0x{off_fill:X} -> {patch_call.hex(' ')}")

    outline_offsets = []
    for va in VA_OUTLINE_SITES:
        rva = va - pe.imagebase
        off = pe.rva_to_off(rva)
        cur = pe.bin.data[off:off + 7]
        if cur != ORIG_OUTLINE_BYTES and cur != PATCH_OUTLINE_BYTES:
            sys.exit(f"LOI: Byte tai outline site 0x{va:X} khong hop le: {cur.hex(' ')}")
        outline_offsets.append((off, va))
        print(f"  Patch outline: off 0x{off:X} (VA 0x{va:X}) -> {PATCH_OUTLINE_BYTES.hex(' ')}")

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
        # 2. Ghi lenh call vao fill site
        f.seek(off_fill)
        f.write(patch_call)
        # 3. Ghi lenh mov r11 vao cac outline sites
        for off, _ in outline_offsets:
            f.seek(off)
            f.write(PATCH_OUTLINE_BYTES)

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
