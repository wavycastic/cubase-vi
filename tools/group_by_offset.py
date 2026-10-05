#!/usr/bin/env python3
"""Gom nhóm chuỗi theo VỊ TRÍ của nó trong .rdata — công cụ để đọc.

    python tools/group_by_offset.py                    # tóm tắt
    python tools/group_by_offset.py --list             # mọi cụm
    python tools/group_by_offset.py -c Transport       # đọc một cụm
    python tools/group_by_offset.py -k Stacked         # cụm của một chuỗi
    python tools/group_by_offset.py --ambiguous        # chuỗi quá chung, bị lo
    python tools/group_by_offset.py --uncovered        # chuỗi không có literal
    python tools/group_by_offset.py --gap 200          # cụm mịn hơn

**Vì sao cần. Đây là hướng duy nhất trả lời được câu hỏi mà bốn nguồn
khác không trả lời: chuỗi này thuộc nhóm nào.**

Bản dịch là XML phẳng 10.737 mục, xếp A-Z, không có trường "nhóm", "màn
hình" hay "hộp thoại". Thấy `Spike` thì không có cách biết nó là đỉnh nhọn
trên đường cong automation hay gai trên cây — và đã dịch sai thành "gai".

Bốn nguồn sẵn có chỉ phủ 33,4%:

    Key Commands.xml (74 nhóm)               959    8,9%
    Defaults/UserPreferences group            146    1,4%
    skin.srf thuộc tính title=/label=       2.668   24,8%
    ------------------------------------------------------------
    hợp nhất                                3.590   33,4%

**Còn lại là vị trí trong binary.** Đo được:

    chuỗi CÙNG NHÓM median cách nhau    73.824 byte
    chuỗi KHÁC NHÓM median cách nhau 1.082.648 byte
    tỉ số 0,43 — gần nhau hơn 14 lần

Steinberg cấp phát literal theo module dịch vụ, các module đứng cạnh nhau.
Nên cắt `.rdata` thành cụm là ra nhóm.

**Hai hướng RE đã thử và đã chết — đừng thử lại:**

1. *Gom nhóm theo hàm gọi.* Mỗi hàm lá chỉ dựng **một** nhãn:
   `Transport Panel` -> 2 hàm, mỗi hàm đúng 1 chuỗi. Không có gia đình.
2. *`xref.py` với file offset.* Báo "0 verified xrefs" — **sai cách gọi**.
   Target ở `.rdata` phải dùng `--va`, không phải offset.

**Bốn nguồn nhiễu đã lo, đừng bỏ sóc:**

| Nhiễu | Cách lo |
|---|---|
| regex nuốt **byte mã máy** (`tWt:ttt`, `llHl$ll`) | phải có ≥3 ký tự chữ cái trong phần lõi |
| chuỗi trùng nhiều nơi, offset đầu vô nghĩa | `Transpose` ×85, `Right` ×34 → đánh dấu **ambiguous**, không gán nhóm |
| chuỗi ≤4 ký tự quá chung | bỏ qua `   `, ` %d`, ` & ` |
| ngưỡng gap rộng gộp nhiều module | `--gap` chỉnh được; mặc định 4.000 |

Đo lại sau khi lọc: 5.781 UTF-16 + 1.987 ASCII = 7.768 chuỗi có nhóm.
21 chuỗi ambiguous, 2.948 không có literal ở đâu.

**Giới hạn, nói thẳng.** 2.948 chuỗi không tồn tại trong code — đã tìm ở
mọi section, cả ASCII lẫn UTF-16: `Show Horizontal Line`, `%d User(s)`,
`+18 Scale` chỉ ra `.rsrc` và không có chỗ nào khác. `deobf_scan` chạy rồi:
281 chuỗi, toàn đường dẫn `__FILE__`. Với 27,5% đó **không có cách tĩnh
nào** biết nhóm — `tools/read.py inspect` (9 ngôn ngữ) vẫn là nguồn rẻ nhất.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUBASE = r'E:\Steinberg\Cubase 15\Cubase15.exe'
KEY_COMMANDS = os.path.expandvars(
    r'%APPDATA%\Steinberg\Cubase 15_64\Key Commands.xml')

# Ngưỡng cắt cụm. Median gap toàn cục là 40 byte. Mặc định 4.000 cho cụm
# thô (định vị vùng module); `--gap 200` cho cụm mịn (tách được
# `Stacked` / `Keep Last` / `Mix-Stacked` thành ba nhóm riêng).
GAP = 4000
MIN_CLUSTER = 2

# Một chuỗi chỉ tin được nếu có ít nhất 3 ký tự chữ cái trong "lõi" (lõi =
# bỏ số và ký tự đặc biệt). Chặn byte mã máy `tWt:ttt` và ` %d`, ` & `.
MIN_LETTERS = 3
MIN_LEN = 3

# Trên ngưỡng này thì offset không còn đáng tin: `Transpose` xuất hiện 85 lần.
MAX_OCCURRENCES = 1


def _core_letters(text):
    return re.sub(r'[^A-Za-z]', '', text)


def scan_literals(pe, keys):
    """key -> offset, cho mọi literal tìm thấy đúng MỘT lần.

    Trả về (found, ambiguous): `ambiguous` là những chuỗi xuất hiện quá
    nhiều lần nên offset đầu tiên không nói được chuỗi đó thuộc module nào.
    """
    found, ambiguous = {}, {}
    for sec in pe.sections:
        if sec.raw_size == 0:
            continue
        blob = pe.bin.data[sec.raw_ptr:sec.raw_ptr + sec.raw_size]
        base = sec.raw_ptr

        for enc, pattern in (('utf-16-le', rb'(?:[\x20-\x7e]\x00){3,}'),
                             ('ascii', rb'[\x20-\x7e]{3,}')):
            seen = {}
            for m in re.finditer(pattern, blob):
                try:
                    text = m.group().decode(enc)
                except UnicodeDecodeError:
                    continue
                if text not in keys or text in seen:
                    continue
                if len(text) < MIN_LEN:
                    continue
                if len(_core_letters(text)) < MIN_LETTERS:
                    continue
                seen[text] = base + m.start()
            for text, off in seen.items():
                # đếm lần xuất hiện thật để đánh dấu ambiguous
                n = blob.count(m.group(0)) if enc == 'ascii' else None
                if text in found:
                    continue
                if enc == 'ascii':
                    (ambiguous if n > MAX_OCCURRENCES else found)[text] = off
                else:
                    found[text] = off
    return found, ambiguous


def key_command_categories(us2key):
    """key -> tên category, từ 74 nhóm trong Key Commands.xml."""
    if not os.path.exists(KEY_COMMANDS):
        return {}
    kc = open(KEY_COMMANDS, encoding='utf-8').read()
    out = {}
    for cat, body in re.findall(
            r'<item>\s*<string name="Name" value="([^"]+)"\s*/>\s*'
            r'<list name="Commands" type="list">(.*?)</list>', kc, re.S):
        for name in re.findall(
                r'<string name="Name" value="([^"]+)"\s*/>', body):
            out.setdefault(us2key.get(name, name), cat)
    return out


def manual_names():
    """offset đầu cụm -> tên đặt tay, đọc từ `tools/group_names.json`.

    Key Commands.xml chỉ đặt được tên cho 104/333 cụm. 229 cụm còn lại được
    đặt tay một lần rồi lưu vào đây, nên chạy lại vẫn ra cùng tên — không
    phải đoán lại mỗi vòng (AGENT.md §8.3: bảng sửa cũ là một lệnh ghi đè,
    đừng đo lại).
    """
    path = os.path.join(ROOT, 'tools', 'group_names.json')
    if not os.path.exists(path):
        return {}
    raw = json.load(open(path, encoding='utf-8'))
    return {int(k, 16): v for k, v in raw.items()}


def build(gap=GAP):
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    from cubelib.pe import PE

    src = open(os.path.join(ROOT, 'keys', 'translation_original.xml'),
               encoding='utf-8').read()
    keys = re.findall(r'<String Key="([^"]*)"', src)
    us2key = {}
    for m in re.finditer(r'<String Key="([^"]*)">\s*<us>(.*?)</us>', src, re.S):
        us2key.setdefault(m.group(2), m.group(1))

    pe = PE(CUBASE)
    try:
        found, ambiguous = scan_literals(pe, set(keys))
    finally:
        pe.close()

    ordered = sorted(found.items(), key=lambda kv: kv[1])
    clusters = []
    for key, off in ordered:
        if clusters and off - clusters[-1][-1][1] <= gap:
            clusters[-1].append((key, off))
        else:
            clusters.append([(key, off)])
    clusters = [c for c in clusters if len(c) >= MIN_CLUSTER]

    cat_of = key_command_categories(us2key)
    manual = manual_names()
    named = []
    for c in clusters:
        votes = {}
        for key, _ in c:
            cat = cat_of.get(key)
            if cat:
                votes[cat] = votes.get(cat, 0) + 1
        label, score = '', 0
        if votes:
            label, score = max(votes.items(), key=lambda kv: kv[1])
        # tên tự đặt trong tools/group_names.json thắng: Key Commands chỉ
        # phủ 104/333 cụm, và đặt sai khi cụm lẫn nhiều module.
        # So khớp theo số nguyên: `hex()` ra chữ thường, JSON ghi chữ hoa.
        start = min(o for _, o in c)
        if start in manual:
            label, score = manual[start], -1
        named.append((label, score, len(c), c))

    return keys, found, ambiguous, named


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', metavar='TEXT', help='đọc cụm có tên chứa TEXT')
    ap.add_argument('-k', metavar='KEY', help='cụm chứa chuỗi này')
    ap.add_argument('-g', '--gap', type=int, default=GAP, metavar='N',
                    help='ngưỡng cắt cụm, byte (mặc định %d)' % GAP)
    ap.add_argument('--list', action='store_true', help='mọi cụm')
    ap.add_argument('--ambiguous', action='store_true',
                    help='chuỗi quá chung nên bị lo')
    ap.add_argument('--uncovered', action='store_true',
                    help='chuỗi không có literal trong code')
    a = ap.parse_args()

    keys, found, ambiguous, named = build(a.gap)
    n_all = len(keys)

    if a.ambiguous:
        print('%d chuỗi xuat hien nhieu lan -> offset dau vo nghia, da lo.'
              % len(ambiguous))
        print('Vi du: Transpose x85, Right x34, Full x34, Lower x28.\n')
        for k in sorted(ambiguous)[:40]:
            print('  %r' % k)
        if len(ambiguous) > 40:
            print('  ... +%d more' % (len(ambiguous) - 40))
        return 0

    if a.uncovered:
        rest = [k for k in keys if k not in found and k not in ambiguous]
        print('%d chuoi (%.1f%%) khong co literal o bat ky section nao:'
              % (len(rest), 100.0 * len(rest) / n_all))
        print('Da thu ca ASCII, UTF-16 va deobfuscate. Khong co cach tinh.')
        print('Dung read.py inspect cho nhom nay.\n')
        for k in rest[:40]:
            print('  %r' % k)
        if len(rest) > 40:
            print('  ... +%d more' % (len(rest) - 40))
        return 0

    if a.k:
        t = a.k.lower()
        for label, score, n, c in named:
            if any(t in k.lower() for k, _ in c):
                print('cum %-26s %d chuoi, khop %d voi Key Commands\n'
                      % (label or '(chua ten)', n, score))
                for k, off in c:
                    print('   0x%08X  %r' % (off, k))
                return 0
        print('khong tim thay %r trong cum nao' % a.k)
        if a.k in ambiguous:
            print('  (chuoi nay xuat hien nhieu lan -> da lo, xem --ambiguous)')
        elif a.k not in found:
            print('  (khong co literal) -> xem --uncovered')
        return 1

    if a.c:
        t = a.c.lower()
        for label, score, n, c in named:
            if t in label.lower():
                print('=== %s === %d chuoi, khop %d voi Key Commands\n'
                      % (label, n, score))
                for k, off in c:
                    print('   0x%08X  %r' % (off, k))
                print()
        return 0

    if a.list:
        for label, score, n, c in sorted(named, key=lambda x: -x[2]):
            print('%4d  %-26s %r' % (n, label or '(chua ten)', c[0][0][:44]))
        return 0

    print('literal tin duoc       : %d / %d  (%.1f%%)'
          % (len(found), n_all, 100.0 * len(found) / n_all))
    print('bi lo (qua chung)      : %d' % len(ambiguous))
    print('khong co literal       : %d  (%.1f%%)'
          % (n_all - len(found) - len(ambiguous),
             100.0 * (n_all - len(found) - len(ambiguous)) / n_all))
    print('\ncum (gap %d byte, >= %d chuoi): %d' % (a.gap, MIN_CLUSTER, len(named)))
    print('  ten tu Key Commands   : %d' % sum(1 for _, s, _, _ in named if s > 0))
    print('  ten dat tay (json)    : %d' % sum(1 for _, s, _, _ in named if s == -1))
    print('  chua ten              : %d' % sum(1 for _, s, _, _ in named if not s))
    print('  chuoi nam trong cum  : %d' % sum(n for _, _, n, _ in named))
    print('\ncum lon nhat:')
    for label, score, n, c in sorted(named, key=lambda x: -x[2])[:10]:
        print('  %4d  %-24s %r' % (n, label or '(chua ten)', c[0][0][:40]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
