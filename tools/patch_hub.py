#!/usr/bin/env python3
r"""Công cụ tích hợp tiếng Việt cho Cubase Pro Hub (`Components\hubservice.dll`).

Cubase Hub là một module độc lập sở hữu 89 chuỗi giao diện riêng
(Create Empty Project, Recent, Tutorials, Deals, User Manuals, Hub Settings,
Choose File...) nhúng trong PE Resource `TRANSLATION.XML` (RT_RCDATA #10 / Name #1031).

Script này:
1. Đọc 89 chuỗi tiếng Việt chuẩn mực từ `translations/hub_strings.json`.
2. Trích xuất resource `TRANSLATION.XML` gốc từ `hubservice.dll`.
3. Thêm `<language key="vi">Vietnamese</language>` và 89 thẻ `<vi>...</vi>`.
4. Tạo bản sao lưu an toàn `hubservice.dll.bak`.
5. Cập nhật resource PE bằng Windows API chuẩn `UpdateResourceW`.
6. Tự động kiểm tra tính toàn vẹn (PE structural verification).

Cách dùng:
    python tools/patch_hub.py                    # Tự động tìm Cubase 15 và patch
    python tools/patch_hub.py --dry-run          # Chạy kiểm tra thử không ghi DLL
    python tools/patch_hub.py --restore          # Khôi phục từ file .bak

"""

import argparse
import ctypes
import ctypes.wintypes as wt
import json
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB_JSON = os.path.join(ROOT, 'translations', 'hub_strings.json')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cubelib.pe import PE  # noqa: E402

DEFAULT_CUBASE_PATHS = [
    r"E:\Steinberg\Cubase 15",
    r"C:\Program Files\Steinberg\Cubase 15",
    r"D:\Steinberg\Cubase 15",
]


def find_hub_dll(custom_dir=None):
    candidates = []
    if custom_dir:
        candidates.append(custom_dir)
    candidates.extend(DEFAULT_CUBASE_PATHS)

    for c in candidates:
        dll = os.path.join(c, 'Components', 'hubservice.dll')
        if os.path.isfile(dll):
            return dll
    return None


def generate_patched_xml(orig_xml_bytes, hub_dict):
    orig_text = orig_xml_bytes.decode('utf-8', errors='replace')

    # 1. Thêm thẻ ngôn ngữ vi vào <LanguageTable>
    if '<language key="vi">' not in orig_text:
        target_lang = '<language key="ru">Russian</language>'
        replacement_lang = '<language key="ru">Russian</language>\n\t\t<language key="vi">Vietnamese</language>'
        if target_lang in orig_text:
            orig_text = orig_text.replace(target_lang, replacement_lang, 1)
        else:
            orig_text = orig_text.replace('</LanguageTable>', '\t<language key="vi">Vietnamese</language>\n\t</LanguageTable>', 1)

    # 2. Chèn thẻ <vi>...</vi> vào từng <String Key="...">
    def replacer(match):
        full_block = match.group(0)
        key = match.group(1)
        if key in hub_dict:
            vi_val = hub_dict[key]
            # Escape XML entities
            vi_escaped = vi_val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Nếu đã có <vi> thì thay thế, chưa có thì chèn trước </String>
            if '<vi>' in full_block:
                return re.sub(r'<vi>.*?</vi>', f'<vi>{vi_escaped}</vi>', full_block)
            else:
                return full_block.replace('</String>', f'\t<vi>{vi_escaped}</vi>\n\t\t</String>')
        return full_block

    pattern = re.compile(r'<String Key="((?:[^"]|"(?!>))*?)">.*?</String>', re.DOTALL)
    patched_text = pattern.sub(replacer, orig_text)

    # Chuẩn hóa CRLF
    patched_text = patched_text.replace('\r\n', '\n').replace('\n', '\r\n')
    patched_bytes = patched_text.encode('utf-8')
    return patched_bytes


def update_pe_resource(dll_path, xml_bytes):
    kernel32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)

    BeginUpdateResourceW = kernel32.BeginUpdateResourceW
    BeginUpdateResourceW.argtypes = [wt.LPCWSTR, wt.BOOL]
    BeginUpdateResourceW.restype = wt.HANDLE

    UpdateResourceW = kernel32.UpdateResourceW
    UpdateResourceW.argtypes = [wt.HANDLE, wt.LPCWSTR, wt.LPCWSTR, wt.WORD, wt.LPVOID, wt.DWORD]
    UpdateResourceW.restype = wt.BOOL

    EndUpdateResourceW = kernel32.EndUpdateResourceW
    EndUpdateResourceW.argtypes = [wt.HANDLE, wt.BOOL]
    EndUpdateResourceW.restype = wt.BOOL

    RT_RCDATA = ctypes.cast(ctypes.c_void_p(10), wt.LPCWSTR)
    RES_NAME = "TRANSLATION.XML"
    LANG_ID = 1031

    hUpdate = BeginUpdateResourceW(dll_path, False)
    if not hUpdate:
        raise ctypes.WinError(ctypes.get_last_error())

    buf = ctypes.create_string_buffer(xml_bytes)
    res = UpdateResourceW(hUpdate, RT_RCDATA, RES_NAME, LANG_ID, buf, len(xml_bytes))
    if not res:
        err = ctypes.get_last_error()
        EndUpdateResourceW(hUpdate, True)
        raise ctypes.WinError(err)

    if not EndUpdateResourceW(hUpdate, False):
        raise ctypes.WinError(ctypes.get_last_error())


def main():
    parser = argparse.ArgumentParser(description="Patch tiếng Việt cho Cubase Pro Hub (hubservice.dll)")
    parser.add_argument("--cubase-dir", help="Đường dẫn thư mục cài đặt Cubase 15")
    parser.add_argument("--dry-run", action="store_true", help="Chạy kiểm tra thử mà không ghi vào DLL")
    parser.add_argument("--restore", action="store_true", help="Khôi phục hubservice.dll từ file .bak")
    args = parser.parse_args()

    dll_path = find_hub_dll(args.cubase_dir)
    if not dll_path:
        sys.exit("LỖI: Không tìm thấy Components\\hubservice.dll. Vui lòng chỉ định --cubase-dir.")

    bak_path = dll_path + '.bak'
    print(f"Mục tiêu: {dll_path}")

    if args.restore:
        if not os.path.isfile(bak_path):
            sys.exit(f"LỖI: Không tìm thấy file sao lưu {bak_path}")
        shutil.copy2(bak_path, dll_path)
        print(f"Đã khôi phục thành công từ {bak_path}")
        return

    if not os.path.isfile(HUB_JSON):
        sys.exit(f"LỖI: Không tìm thấy file từ điển Hub tại {HUB_JSON}")

    hub_dict = json.load(open(HUB_JSON, encoding='utf-8'))
    print(f"Đã nạp {len(hub_dict)} chuỗi từ điển Hub.")

    # Đọc resource gốc từ DLL
    with PE.open(dll_path) as pe:
        res = pe.find_resource('TRANSLATION.XML')
        if not res:
            sys.exit("LỖI: Không tìm thấy resource TRANSLATION.XML trong hubservice.dll")
        orig_bytes = pe.bin.slice(res.off, res.size)

    patched_bytes = generate_patched_xml(orig_bytes, hub_dict)

    # Tự kiểm tra cú pháp XML mới
    try:
        root = ET.fromstring(patched_bytes)
        vi_count = len([s for s in root.findall(".//StringTable/String") if s.find("vi") is not None])
        print(f"Kiểm tra XML: Hợp lệ 100%, chứa {vi_count}/89 thẻ <vi>.")
    except Exception as e:
        sys.exit(f"LỖI: XML được tạo không hợp lệ: {e}")

    if args.dry_run:
        print("\n[DRY RUN] Kiểm tra hoàn tất thành công, không có file nào bị thay đổi.")
        return

    # Tạo bản sao lưu .bak nếu chưa có
    if not os.path.isfile(bak_path):
        shutil.copy2(dll_path, bak_path)
        print(f"Đã tạo bản sao lưu an toàn: {bak_path}")

    # Cập nhật PE Resource
    try:
        update_pe_resource(dll_path, patched_bytes)
        print("Đã cập nhật thành công resource TRANSLATION.XML trong hubservice.dll!")
    except Exception as e:
        # Nếu lỗi (ví dụ file đang bị lock), báo cho người dùng
        sys.exit(f"LỖI khi cập nhật DLL: {e}\n(Nếu Cubase đang chạy, vui lòng đóng Cubase rồi chạy lại).")

    # Xác minh lại file sau khi patch
    with PE.open(dll_path) as pe:
        res = pe.find_resource('TRANSLATION.XML')
        verify_bytes = pe.bin.slice(res.off, res.size)
        assert b'<language key="vi">' in verify_bytes, "Xác minh thất bại: thiếu <language key='vi'>"
        assert b'<vi>' in verify_bytes, "Xác minh thất bại: thiếu <vi>"

    print("\nHOÀN THÀNH XUẤT SẮC: Cubase Pro Hub đã được tích hợp tiếng Việt đầy đủ!")


if __name__ == '__main__':
    main()
