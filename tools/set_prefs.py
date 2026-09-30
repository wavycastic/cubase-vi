#!/usr/bin/env python3
r"""Đọc/sửa `UserPreferences.xml` của Cubase, có sao lưu và tự kiểm.

    python tools\set_prefs.py --list PAudioImage
    python tools\set_prefs.py --group PAudioImage --set "Show Volume Curves Always=0"

Vì sao phải cẩn thận
-------------------
1. File XML nằm ở `%APPDATA%\Steinberg\<bản>_64\UserPreferences.xml`, và **Cubase
   ghi đè toàn bộ file khi thoát**. Sửa lúc Cubase đang chạy là vô nghĩa — thay đổi
   sẽ bị mất. Script kiểm tra tiến trình trước khi ghi.
2. Tên pref trong file **không nhất quán**: cùng nhóm vừa có khoá tiếng Anh
   (`Wave Brightness`) vừa có khoá đã dịch tiếng Việt (`Hiển Fade`). Tức tên khoá
   phụ thuộc bản dịch đang nạp, và đổi bản dịch có thể làm một pref rơi về mặc
   định. Script in đúng tên nó tìm thấy để đối chiếu.
3. Sửa bằng `xml.etree` sẽ **bỏ hết chú thích và định dạng** của file, tạo diff
   khổng lồ với file 174 KB mà Cubase vẫn đọc được. Nên script sửa *trên chuỗi*
   bằng regex, chỉ thay đúng đoạn `<int name="..." value="..."/>`, rồi parse lại
   bằng `ElementTree` để xác nhận file vẫn hợp lệ và các giá trị đúng ý.
"""
import argparse
import os
import re
import shutil
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

APPDATA = Path(os.environ.get('APPDATA', ''))


def candidates():
    root = APPDATA / 'Steinberg'
    if not root.is_dir():
        return []
    return sorted(p for p in root.glob('*/UserPreferences.xml'))


def group_block(text, group):
    """Return (start, end) span of the <item> whose <string name="Group"> is `group`."""
    key = f'<string name="Group" value="{group}"/>'
    i = text.find(key)
    if i < 0:
        return None
    start = text.rfind('<item>', 0, i)
    depth, pos = 0, start
    while pos >= 0 and pos < len(text):
        nxt = text.find('<item>', pos + 1)
        end = text.find('</item>', pos + 1)
        if end < 0:
            break
        if 0 <= nxt < end:
            depth += 1
            pos = nxt
        else:
            if depth == 0:
                return start, end + len('</item>')
            depth -= 1
            pos = end
    return None


def read_group(path, group):
    text = path.read_text(encoding='utf-8', errors='replace')
    span = group_block(text, group)
    if not span:
        return {}
    out = {}
    for m in re.finditer(r'<(int|float|string|bool)\s+name="([^"]+)"\s+value="([^"]*)"',
                         text[span[0]:span[1]]):
        out[m.group(2)] = m.group(3)
    return out


def cubase_running():
    if os.name != 'nt':
        return False
    try:
        out = subprocess_run(['tasklist', '/FI', 'IMAGENAME eq Cubase15.exe'])
    except Exception:
        return False
    return 'Cubase15.exe' in out


def subprocess_run(args):
    import subprocess
    return subprocess.run(args, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--file', type=Path, help='duong dan UserPreferences.xml')
    ap.add_argument('--list', metavar='GROUP', help='in pref cua nhom nay')
    ap.add_argument('--group', help='nhom pref can sua')
    ap.add_argument('--set', action='append', default=[], metavar='NAME=VALUE',
                    help='gan gia tri moi (lap lai neu nhieu)')
    a = ap.parse_args()

    path = a.file
    if path is None:
        found = candidates()
        if not found:
            raise SystemExit('khong tim thay UserPreferences.xml nao')
        for p in found:
            print(f'  tim thay: {p}', file=sys.stderr)
        path = found[0]
    if not path.exists():
        raise SystemExit(f'khong ton tai: {path}')

    if a.list:
        vals = read_group(path, a.list)
        if not vals:
            raise SystemExit(f'khong tim thay nhom {a.list!r}')
        print(f'# {path}\n# nhom "{a.list}" — {len(vals)} gia tri\n')
        for k, v in vals.items():
            print(f'  {k:<44} = {v}')
        return 0

    if not a.set:
        ap.error('can --list hoac --set')

    if cubase_running():
        raise SystemExit('Cubase dang chay — no se ghi de file khi thoat.\n'
                         'Hay thoat Cubase truoc roi chay lai lenh nay.')

    text = path.read_text(encoding='utf-8', errors='surrogateescape')
    span = group_block(text, a.group)
    if not span:
        raise SystemExit(f'khong tim thay nhom {a.group!r}')

    body = text[span[0]:span[1]]
    applied, missed = [], []
    for item in a.set:
        if '=' not in item:
            raise SystemExit(f'can NAME=VALUE, nhan duoc {item!r}')
        name, val = item.split('=', 1)
        pat = re.compile(r'(<int\s+name="' + re.escape(name) + r'"\s+value=")([^"]*)(")')
        m = pat.search(body)
        if not m:
            missed.append(name)
            continue
        body = body[:m.start()] + m.group(1) + val + m.group(3) + body[m.end():]
        applied.append((name, m.group(2), val))
    if missed:
        raise SystemExit('khong co pref nay trong nhom: ' + ', '.join(missed))

    backup = path.with_suffix(f'.xml.bak-{time.strftime("%Y%m%d-%H%M%S")}')
    shutil.copy2(path, backup)

    out = text[:span[0]] + body + text[span[1]:]
    path.write_text(out, encoding='utf-8', errors='surrogateescape')

    # -- verify ------------------------------------------------------------
    # KHONG dung ElementTree: file nay khong co DOCTYPE nhung van dung entity
    # HTML (`&aacute;`), nen bo phan giai XML tieu chuan se bao loi `undefined
    # entity` tren chinh file goc. Thay bang so sanh theo dong, va dich chung cho
    # rang chi nhung dong `<int .../>` da dinh sua bi doi.
    old_lines = text.splitlines()
    new_lines = out.splitlines()
    if len(old_lines) != len(new_lines):
        shutil.copy2(backup, path)
        raise SystemExit(f'FAIL: so dong doi {len(old_lines)} -> {len(new_lines)}; '
                         'da khoi phuc file goc')
    touched = {n for n, _o, _v in applied}
    int_re = re.compile(r'<int\s+name="([^"]+)"\s+value="([^"]*)"\s*/>')
    for i, (o, n) in enumerate(zip(old_lines, new_lines)):
        if o == n:
            continue
        om, nm_ = int_re.search(o), int_re.search(n)
        if not om or not nm_ or om.group(1) not in touched \
                or om.group(1) != nm_.group(1) or om.group(2) != nm_.group(2):
            shutil.copy2(backup, path)
            raise SystemExit(f'FAIL: dong {i + 1} doi khong mong doi:\n'
                             f'  - {o.strip()}\n  + {n.strip()}\n'
                             'da khoi phuc file goc')
    again = read_group(path, a.group)
    bad = [n for n, _o, v in applied if again.get(n) != v]
    if bad:
        shutil.copy2(backup, path)
        raise SystemExit(f'FAIL: doc lai ra {bad}; da khoi phuc file goc')

    print(f'sua {path}')
    print(f'sao luu {backup.name}')
    for name, old, new in applied:
        print(f'  {name:<44} {old} -> {new}')
    print('  chi nhung dong <int .../> da dinh sua bi doi; doc lai khop')
    return 0


if __name__ == '__main__':
    sys.exit(main())