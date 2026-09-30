#!/usr/bin/env python3
"""Thuat ngu nao BAN DICH dang coi la khong dich duoc, du AGENT.md chua ghi?

Nguon tot nhat cua danh sach "tu cam dich" khong phai suy dien, ma la
chinh ban dich: neu 100 chuoi giu 'Cycle' nguyen tieng Anh va 0 chuoi dich
no, thi 'Cycle' da la tu cam dich tren thuc te - chi la chua duoc viet vao
luat, nen dot sau co the pha no ma khong ai bao.

    giu  = so chuoi nguon co thuat ngu nay, va ban dich CON giu no
    mat  = so chuoi nguon co thuat ngu nay, va ban dich DICH no

    giu cao, mat thap   -> dang duoc bao ve, thieu trong luat
    giu thap, mat cao   -> luat ghi mot dang, ban dich lam mot dang
    ca hai deu cao      -> dang phan van, phai doc tay

    python tools\audit_protected.py              # ung vien nen them vao luat
    python tools\audit_protected.py --conflict   # luat va ban dich lech nhau
    python tools\audit_protected.py --detail Cycle
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)

V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# tu tieng Anh thong thuong - khong bao gio la thuat ngu chuyen nganh
COMMON = set("""the a an and or of to in on for with is are be been was were not no
all any new old this that these those you your it its as at by from if then
than so can may must will would should could use used using only when where
which what who how why do does did done make made makes take takes set sets
get gets got give gives move moves open opens close closes add adds remove
removes delete deletes show shows hide hides select selects send sends
import imports export exports read reads write writes start starts stop stops
first last next previous other others more less most least one two three
file files name names value values type types size sizes time times left
right up down over under out off top bottom zero not""".split())
# Cac gioi tu/trang tu tieng Anh xuat hien trong nhan Cubase
STOPWORD = COMMON


# Thuong hieu / ten rieng / dinh dang - giu la hien nhien, khong can luat
BRAND = set("""Steinberg Yamaha Nuendo Cubase MIDI ASIO VST VCA OMF AAF SMF BWF CSV
NRPN LSB CTRL SysEx MixConsole VariAudio SyncStation MediaBay MPEX EBU AES
Windows Mac Apple Focusrite Mackie Pre Pre-Fader Post-Fader Post-roll Pre-roll
Surround Mono Stereo XY MS API UAD""".split())


def is_acronym(w):
    """OMF, AAF, SMF, NRPN, LSB, CTRL - giu la hien nhien."""
    return w.upper() == w and len(w) <= 6


def load():
    vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
    src = {}
    for line in open(T('keys', 'all_strings.tsv'),
                     encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return vi, src


# Nhung tu BAT BUOC viet hoa dau (danh tu rieng Cubase) - mot chu thuong
# nhu "note/bar/part" co the la tu tieng Anh binh thuong.
def candidates(vi, src):
    keep = collections.Counter()
    gone = collections.Counter()
    for k, v in vi.items():
        if k not in src:
            continue
        en = src[k]
        en_words = set(re.findall(r'[A-Za-z][A-Za-z-]+', en))
        for w in en_words:
            if w.lower() in STOPWORD or len(w) < 3:
                continue
            if not w[0].isupper():
                continue          # 'note', 'part' thuong: bo qua
            if re.search(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])', v):
                keep[w] += 1
            elif V.search(v):
                gone[w] += 1
    return keep, gone


def main():
    vi, src = load()
    keep, gone = candidates(vi, src)

    if '--detail' in sys.argv:
        w = sys.argv[sys.argv.index('--detail') + 1]
        pat = re.compile(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])')
        n = 0
        for k, v in vi.items():
            if k in src and pat.search(src[k]) and not pat.search(v) and V.search(v):
                print(f'EN {src[k][:90]}\nVI {v[:90]}\n')
                n += 1
        print(f'{n} chuoi da dich mat {w!r}')
        return

    conflict = '--conflict' in sys.argv
    rows = []
    for w in set(keep) | set(gone):
        kp, gn = keep[w], gone[w]
        tot = kp + gn
        if tot < 3:
            continue
        rows.append((kp, gn, w, tot))

    if conflict:
        print('=== LUAT/THUC TE LECH: ban dich DICH thu luat bat giu ===')
        print(f'{"thuat ngu":18} {"giu":>5} {"dich":>5} {"tong":>5}')
        print('-' * 40)
        for kp, gn, w, tot in sorted(rows, key=lambda r: -r[1]):
            if gn >= 3 and gn > kp:
                print(f'{w:18} {kp:5} {gn:5} {tot:5}')
        return

    print('=== ung vien NEN them vao luat: dang duoc giu nguyen ===')
    print(f'{"thuat ngu":18} {"giu":>5} {"dich":>5} {"tong":>5}  giu%')
    print('-' * 48)
    new = []
    for kp, gn, w, tot in sorted(rows, key=lambda r: -r[0]):
        if kp < 5 or gn > 1:
            continue
        if w.upper() == w or is_acronym(w) or w in BRAND:
            continue          # thuat ngu/viet tat: giu khong phai la mot luat
        pct = 100 * kp / tot
        print(f'{w:18} {kp:5} {gn:5} {tot:5}  {pct:.0f}%')
        new.append(w)
    print(f'\n{len(new)} ung vien giu >=5, dich <=1 (da loai viet tat/thuong hieu)')
    print('(nhung tu nay ban dich da coi la khong dich - chua co trong AGENT.md §2)')
    print(f'\nthanh mot dong de dan vao AGENT.md §2:')
    print('  ' + ' · '.join(new))


if __name__ == '__main__':
    main()