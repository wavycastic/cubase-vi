#!/usr/bin/env python3
"""§2 la 'giu tieng Anh', khong phai 'cam dich'. Khac nhau o cho nao?

    nhan  'Cycle Mode'          -> 'Chế độ Cycle'        giu, dung
    cau   'Allow machine controlled cycle' -> 'Cycle do may...' giu, dung
    nhan  'Transpose'           -> 'Chuyen am'           DICH, sai
    cau   'Transpose the selected events'  -> 'Chuyen am...' dich, DUNG

Cung mot tu, hai ngu canh, hai ket qua dung. Nen mot bong den 'cam dich
Transpose' se bao dong gia o moi cau - AGENT.md §7: bo do bao dong gia
nhieu lan con te hon khong co bo do.

Thu can kiem la NHAN: chuoi ngan, thuat ngu la danh tu chinh, khong co
menh de. O do Cubase ve chu len nut/danh sach va ban dich phai giu tieng
Anh. Trong cau dai thi dich la dung.

    python tools\audit_labels.py            # nhan nao da dich thuat ngu?
    python tools\audit_labels.py --terms    # chi liet ke ung vien §2
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)

V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# Dong tu/menh de tieng Anh: xuat hien thi chuoi la CAU, dich la dung
CLAUSE = re.compile(r'\b(is|are|was|were|will|would|shall|should|can|could|may|'
                    r'might|must|have|has|had|do|does|did|to|if|when|while|'
                    r'that|which|you|your|we|it|they|this|these|than|because|'
                    r'before|after|not|no|only|with|without|from|into|which)\b',
                    re.I)
# Lenh/dong tu mo dau: 'Delete All', 'Create New Track' - dong tu phai dich
IMPERATIVE = re.compile(r'^[A-Z][a-z]+\b')


def is_label(en):
    """Nhan: ngan, khong menh de, khong phai cau lenh day du."""
    if len(en) > 46:
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", en)
    if len(words) > 5:
        return False
    if CLAUSE.search(en):
        return False
    if en.rstrip().endswith(('.', '?', '!', ':')) and len(words) > 2:
        return False
    return True


def load():
    vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
    src = {}
    for line in open(T('keys', 'all_strings.tsv'),
                     encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return vi, src


def section2():
    """Doc AGENT.md §2 va lay dong 'DAW - giu tieng Anh'."""
    txt = open(T('AGENT.md'), encoding='utf-8').read()
    m = re.search(r'\*\*DAW[^\n]*\*\*(.*?)\n\n', txt, re.S)
    body = m.group(1) if m else ''
    terms = [t.strip() for t in re.split(r'[·|]', body) if t.strip()]
    return [t for t in terms if t and not t.startswith('*')]


def main():
    vi, src = load()
    terms = section2()
    only = '--terms' in sys.argv
    if not terms:
        sys.exit('khong doc duoc §2 - kiem tra dinh dang AGENT.md')

    found = collections.defaultdict(list)
    for k, v in vi.items():
        if k not in src or not V.search(v):
            continue
        en = src[k]
        if not is_label(en):
            continue
        for t in terms:
            pat = r'(?<![A-Za-z])' + re.escape(t).replace(r'\ ', r'\s+') + r'(?![A-Za-z])'
            if re.search(pat, en, re.I) and not re.search(pat, v, re.I):
                found[t].append((k, en, v))

    print(f'{len(vi)} chuoi · §2 co {len(terms)} thuat ngu\n')
    print('NHAN (ngan, khong menh de) ma ban dich DA DICH thuat ngu §2:\n')
    tot = 0
    for t, items in sorted(found.items(), key=lambda x: -len(x[1])):
        tot += len(items)
        print(f'--- {t}  ({len(items)})')
        for k, en, v in items[:8]:
            print(f'    EN {en}')
            print(f'    VI {v}')
        if len(items) > 8:
            print(f'    ... {len(items) - 8} nua')
        print()
    print(f'TONG: {tot} nhan da dich thuat ngu §2')


if __name__ == '__main__':
    main()