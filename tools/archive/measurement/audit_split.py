#!/usr/bin/env python3
"""Thuat ngu nao AGENT.md §2 bat giu tieng Anh, ma ban dich lai dich?

    nguon 'Delete Track'      -> 'Xoa Track'    -> giu, dung
    nguon 'Remove the track'  -> 'Xoa rãnh'     -> dich, sai

Khong doan dang dich sai. Lay tu chinh nguon tieng Anh (cot 2 cua
all_strings.tsv), roi hoi: ban dich con chu do khong? Lech o day moi la
su that can xem - mot nguoi doc lai vi.json khong the thay "Latency xuat
hien 25 lan, 23 lan dich thanh 'do tre'", vi khong ai dem 10.737 chuoi.

Cach tim dang dich THAY THE: trong nhung chuoi khong con giu thuat ngu,
tim cum tieng Viet xuat hien nhieu nhat ma KHONG co trong ban goc. Do la
dang dich, do bang du lieu chu khong phai bang suy dien.

    python tools\audit_terms.py             # bang tom tat
    python tools\audit_terms.py Latency     # chi tiet mot thuat ngu
    python tools\audit_terms.py --all       # moi chuoi bi dich
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)

# AGENT.md §2, dong "DAW - giu tieng Anh"
DAW_TERMS = """Track Channel Bus FX Group VCA Insert Send Slot Fader Pan Solo
Mute Meter Metronome Click Marker Locator Automation Clip Event Part Pool
Quantize Snap Grid Bounce Render Freeze Warp Velocity Pitch Note Chord Tempo
Timecode Bar Beat Fade Punch Buffer Latency Sample Rate ASIO VST Plug-in
Preset MixConsole Inspector Zone Export Import Arranger Chain Step Lane
Pattern Expression Voicing Tension Articulation Layout Map Mapping Script
Talkback Cue""".split()

V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
WORD = re.compile(r"[A-Za-zÀ-ỹ\u0100-\u024f]+")

# Tu tieng Viet khong bao gio la "ban dich cua thuat ngu"
STOP = set("""cua và là của cho với một các một trong ngoài trên dưới khi nếu thì
để vào ra từ tới tại đã sẽ đang được bị có không thể này đó kia những cái
bạn hãy hộp nhấn giữ chọn mở đóng thêm xóa sửa đặt bật tắt hiển thị
audio midi track the to of a in on for with and or not all new""".split())


def load():
    vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
    src = {}
    for line in open(T('keys', 'all_strings.tsv'),
                     encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return vi, src


def survey(term, vi, src):
    """(giu, dich[], vi_tu_dien_the) cho mot thuat ngu."""
    pat = r'(?<![A-Za-z])' + re.escape(term).replace(r'\ ', r'\s+') + r'(?![A-Za-z])'
    rx = re.compile(pat, re.I)
    keep, trans = 0, []
    for k, v in vi.items():
        if k not in src or not V.search(v):
            continue
        en = src[k]
        if not rx.search(en):
            continue
        if rx.search(v):
            keep += 1
        else:
            trans.append((k, en, v))

    # cum tieng Viet xuat hien trong ban dich ma khong co trong ban goc
    cand = collections.Counter()
    for _k, en, v in trans:
        en_words = {w.lower() for w in WORD.findall(en)}
        for w in WORD.findall(v.lower()):
            if w in STOP or len(w) < 3 or w in en_words:
                continue
            cand[w] += 1
    return keep, trans, cand


def main():
    vi, src = load()
    detailed = [a for a in sys.argv[1:] if not a.startswith('-')]
    show_all = '--all' in sys.argv

    if detailed:
        terms = detailed
    else:
        terms = DAW_TERMS

    rows = []
    for term in terms:
        keep, trans, cand = survey(term, vi, src)
        if keep + len(trans) < 3:
            continue
        rows.append((len(trans), keep, term, trans, cand))

    if detailed:
        for n, keep, term, trans, cand in rows:
            print(f'=== {term}: giu {keep}, dich {n} ===')
            if cand:
                print('    dang dich thay bang: ' +
                      ', '.join(f'{w} x{c}' for w, c in cand.most_common(4)))
            shown = trans if show_all else trans[:12]
            for k, en, v in shown:
                print(f'    EN {en[:88]}')
                print(f'    VI {v[:88]}')
                print()
            if not show_all and len(trans) > 12:
                print(f'    ... {len(trans) - 12} chuoi nua (--all)\n')
        return

    print(f'{len(vi)} chuoi · AGENT.md §2 bat giu tieng Anh\n')
    print(f'{"thuat ngu":16} {"giu":>6} {"dich":>6}   {"dang dich thay bang":38}')
    print('-' * 92)
    for n, keep, term, trans, cand in sorted(rows, reverse=True):
        rep = ', '.join(f'{w} x{c}' for w, c in cand.most_common(3)) if cand else ''
        flag = '  <<<' if n >= 10 and keep < n else ''
        print(f'{term:16} {keep:6} {n:6}   {rep[:36]:38}{flag}')
    # NOTE: do not write `n, _, _, _, _` here - the last `_` wins and becomes
    # the Counter, so `_ < n` compares a Counter to an int.
    pending = [r for r in rows if r[0] >= 10 and r[1] < r[0]]
    print()
    print(f'{len(pending)} thuat ngu co >=10 chuoi bi dich VA it hon so chuoi '
          f'giu - dang phan van')
    print('Chi tiet: python tools\\audit_terms.py Latency')


if __name__ == '__main__':
    main()