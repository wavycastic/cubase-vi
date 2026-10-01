#!/usr/bin/env python3
"""Chia nho 10.737 chuoi thanh vung de biet con bao nhieu cho, va con gi.

Vung hien tai (sample_domain.py) la 8 nhom, phan loai bang `if` **tuyen tu**:
chuoi khop `music-theory` truoc se khong bao gio den `notation`. Do la dung
y muon - mot chuoi chi thuoc ve mot vung - nhung phai kiem chung.

Cong cu nay in:
  1. so chuoi moi vung
  2. do dai trung binh (vung nao dai, vung nao ngan)
  3. so chuoi CHUA duoc dich (con nguyen tieng Anh) - vung nao con no
  4. nhom lon nhat theo tien to key, de thay co vung nao chua duoc tach ra

    python tools\audit_domains.py
    python tools\audit_domains.py --keys notation    # xem chi tiet mot vung
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)

vi = json.load(open(T('translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(T('keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

# Thu tu nay la thu tu UUU TIEN trong sample_domain.py. Giu nguyen de so lieu
# so voi cong cu dang co; comment o moi nhan ghi ro vi sao thu tu do la dung.
RULES = [
    ('music-theory', r'\b(chord|voicing|tension|scale|articulation|harmony|note)\b'),
    ('media', r'\b(export|render|bounce|warp|audio|file|pool|import|media|'
              r'format|bit|sample rate|fade|freeze|process)\b'),
    ('mixer', r'\b(insert|send|eq|plugin|vst|bus|channel|fader|pan|routing|'
              r'compressor|gate|limiter)\b'),
    ('transport', r'\b(locator|marker|cycle|transport|cursor|record|play|loop|'
                  r'tempo|quantize|grid|snap|scroll|zoom)\b'),
    ('ui', r'\b(shortcut|key command|assign|menu|command|context|'
          r'right.click|window|toolbar|panel|dialog|page)\b'),
    ('notation', r'\b(score|stave|staff|system|bar|beat|clef|rest|notation|'
                 r'beam|ledger|signatur)\b'),
    ('project', r'\b(network|server|user|permission|shared|profile|'
                r'project setup|template|preferences)\b'),
]
COMPILED = [(n, re.compile(p)) for n, p in RULES]
V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')


def domain(k):
    s = k.lower()
    for name, rx in COMPILED:
        if rx.search(s):
            return name
    return 'general'


def main():
    want = None
    if '--keys' in sys_args():
        want = sys_args()[sys_args().index('--keys') + 1]

    buckets = collections.defaultdict(list)
    for k, v in vi.items():
        buckets[domain(k)].append((k, v))

    if want:
        items = buckets.get(want, [])
        print(f'######## {want}: {len(items)} chuoi')
        for k, v in items[:80]:
            print(f'  EN {src.get(k, "?")[:96]}')
            print(f'  VI {v[:96]}')
        return

    total = len(vi)
    print(f'{"vung":14} {"so chuoi":>9} {"%":>5} {"TB dai":>7} '
          f'{"chua dich":>10} {"%":>5}')
    print('-' * 62)
    for name, items in sorted(buckets.items(), key=lambda x: -len(x[1])):
        avg = sum(len(v) for _k, v in items) / len(items)
        un = sum(1 for _k, v in items if not V.search(v))
        print(f'{name:14} {len(items):9} {100*len(items)/total:5.1f} '
              f'{avg:7.1f} {un:10} {100*un/len(items):5.1f}')

    # Nhom lon nhat theo tien to key - cho thay vung nao chua duoc tach ra
    pre = collections.Counter()
    for k in vi:
        if domain(k) == 'general':
            m = re.match(r'([A-Za-z][A-Za-z ]{2,22})[:\[]', k)
            pre[m.group(1).strip() if m else k[:18]] += 1
    print(f'\n"general" = {len(buckets["general"])} chuoi khong khop vung nao.')
    print('Nhom lon nhat theo tien to key (ung vien de tach them vung):')
    for p, c in pre.most_common(18):
        if c >= 12:
            print(f'  {c:5}  {p}')


def sys_args():
    import sys
    return sys.argv


if __name__ == '__main__':
    main()