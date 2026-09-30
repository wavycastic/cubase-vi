#!/usr/bin/env python3
"""Cung mot thuat ngu, tai sao MOT chuoi bi dich con phan lon duoc giu?

Day la mau that cua tan giong. `Cycle` giu o 81 chuoi. Neu con 1 chuoi goi
no bang tu Viet, do khong phai 'dich sai theo cam tinh' - do la **keo nhom**:
mot chuoi lot ra khoi 81 chuoi, va no se keo theo cac chuoi lot sau.

Khong can biet 'dich dung la gi'. Chi can thay mot chuoi khac 81 chuoi.

Cach do: voi moi thuat ngu, tach cac chuoi 'giu' (con chu) va 'dich' (mat
chu). In chuoi 'dich' khi con it nhat 3 chuoi 'giu' - va lam ro phan nao
cua chuoi do thuc su khac.

    python tools\audit_outlier.py            # bang tom tat
    python tools\audit_outlier.py --show 25  # xem chi tiet 25 dong dau
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)
V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r'[A-Za-zÀ-ỹ\u0100-\u024f]+')

vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(T('keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

# Tu Viet thuong / lien quan - loai de kiem tra nguoi doc
AMBIGUOUS = set("""lặp lại lặp bỏ qua cân bằng hiệu ứng hiệu năng đa kênh
bố cục phẳng làm phẳng phiên bản chương trình chương ứng dụng vùng khu vực
tổng quan quan sát theo dõi trì trộn lẫn tổng hợp trình bày kết xuất
tạo mới tốc độ độ trễ ngưỡng dải học hàng dải phần đoạn nốt nhịp""".split())


def survey(term):
    rx = re.compile(r'(?<![A-Za-z])' + re.escape(term).replace(r'\ ', r'\s+')
                    + r'(?![A-Za-z])', re.I)
    kept, trans = [], []
    for k, v in vi.items():
        if k not in src or not V.search(v):
            continue
        if not rx.search(src[k]):
            continue
        (kept if rx.search(v) else trans).append(k)
    return kept, trans


def distinctive(val, en):
    """Tu trong ban dich ma khong co trong ban goc - thuoc ve ban dich rieng."""
    en_w = {w.lower() for w in WORD.findall(en)}
    out = []
    for w in WORD.findall(val):
        lw = w.lower()
        if len(w) > 2 and lw not in en_w:
            out.append(w)
    return out


def main():
    show = 25
    if '--show' in sys.argv:
        show = int(sys.argv[sys.argv.index('--show') + 1])

    # moi tu viet hoa trong nguon, dem nhanh bang Counter
    counts = collections.Counter()
    for k in vi:
        if k not in src:
            continue
        for w in set(re.findall(r'[A-Za-z][A-Za-z-]+', src[k])):
            counts[w] += 1

    rows = []
    for term, _ in counts.most_common():
        if len(term) < 3 or not term[0].isupper():
            continue
        kept, trans = survey(term)
        if len(kept) < 3 or not trans:
            continue
        # 1 chuoi lech giua hang tram -> nghi keo nhom
        if len(trans) > max(2, len(kept) // 6):
            continue
        rows.append((len(trans), len(kept), term, kept, trans))

    rows.sort()
    print(f'{"n_dich":>6} {"n_giu":>6}  thuat ngu')
    print('-' * 64)
    for n_t, n_k, term, kept, trans in rows[:show]:
        flag = '  <<<' if n_t == 1 else ''
        print(f'{n_t:6} {n_k:6}  {term}{flag}')
    print(f'\n{len(rows)} thuat ngu co 1-2 chuoi lech giữ >=3 chuoi giu')

    if '--show' not in sys.argv:
        print('Chi tiet: python tools\\audit_outlier.py --show 0')
        return

    print('\n' + '=' * 70)
    for n_t, n_k, term, kept, trans in rows:
        print(f'\n### {term} — giu {n_k}, lich {n_t}')
        print(f'  (chu mau giu: {vi[kept[0]][:60]!r})')
        for k in trans[:4]:
            ds = distinctive(vi[k], src[k])
            print(f'  EN {src[k][:74]}')
            print(f'  VI {vi[k][:74]}')
            print(f'     rieng cua ban dich: {ds}')
            print(f'     con "giu" deu dung: {n_k} chuoi')


if __name__ == '__main__':
    main()