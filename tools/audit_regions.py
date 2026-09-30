#!/usr/bin/env python3
"""Tong hop: 10.737 chuoi chia theo vung NAO DUNG, va vung nao con no.

Hai cach phan bo, tach biet:

  A. THEO MIEN (7 nhom cu + general) - dung de hoi "linh vuc nao con yieu"
  B. THEO DANG (nhan / cau lenh / van xuoi) - dung de hoi "doc cai gi truoc"

Va chi ra: general khong phai mot vung, no la **6.933 chuoi chua duoc gan
vao mieng nao**, trong do 5.009 chi la nhan <=30 ky tu.
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

V = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
BASE = [
    ('mixer', r'\b(insert|send|eq|plugin|vst|bus|channel|fader|pan|routing|'
              r'compressor|gate|limiter)\b'),
    ('transport', r'\b(locator|marker|cycle|transport|cursor|record|play|loop|'
                  r'tempo|quantize|grid|snap|scroll|zoom)\b'),
    ('notation', r'\b(score|stave|staff|system|bar|beat|clef|rest|notation|'
                 r'beam|ledger|signatur)\b'),
    ('music-theory', r'\b(chord|voicing|tension|scale|articulation|harmony|note)\b'),
    ('media', r'\b(export|render|bounce|warp|audio|file|pool|import|media|'
              r'format|bit|sample rate|fade|freeze|process)\b'),
    ('ui', r'\b(shortcut|key command|assign|menu|command|context|'
          r'right.click|window|toolbar|panel|dialog|page)\b'),
    ('project', r'\b(network|server|user|permission|shared|profile|'
                r'project setup|template|preferences)\b'),
]
BASE_RX = [(n, re.compile(p)) for n, p in BASE]
VERB = re.compile(r'^(Add|Delete|Set|Get|Select|Choose|Enable|Disable|Show|Hide|'
                  r'Open|Close|Save|Load|Create|Remove|Insert|Apply|Reset|Copy|Move|'
                  r'Adjust|Change|Define|Activate|Deactivate|Toggle|Import|Export|'
                  r'Bounce|Render|Freeze|Quantize|Warp|Mute|Solo|Record|Play|'
                  r'Stop|Start|Next|Previous|Cancel|Confirm)\b')


def domain(k):
    for name, rx in BASE_RX:
        if rx.search(k.lower()):
            return name
    return 'general'


def shape(en):
    e = en.strip()
    n = len(e)
    if n > 140:
        return 'van xuoi >140c'
    if e.endswith('?'):
        return 'cau hoi (?)'
    if VERB.match(e):
        return 'cau lenh'
    if n > 60:
        return 'van vua 60-140c'
    if n <= 30:
        return 'nhan ngan <=30c'
    return 'ngan 31-60c'


def main():
    by_dom = collections.defaultdict(list)
    by_shape = collections.defaultdict(list)
    for k, v in vi.items():
        if k not in src:
            continue
        by_dom[domain(k)].append(k)
        by_shape[shape(src[k])].append(k)

    total = len(vi)
    print(f'{total} chuoi\n')
    print('A. THEO MIEN (7 cum tu khop key + general)')
    print(f'   {"vung":14} {"so chuoi":>8} {"%":>5} {"chua dich":>10}')
    print('   ' + '-' * 50)
    for name, keys in sorted(by_dom.items(), key=lambda x: -len(x[1])):
        un = sum(1 for k in keys if not V.search(vi[k]))
        print(f'   {name:14} {len(keys):8} {100*len(keys)/total:5.1f} {un:10}')

    print('\nB. THEO DANG (dung de quyet dinh doc cai gi truoc)')
    print(f'   {"dang":18} {"so chuoi":>8} {"%":>5} {"TB VI":>6}')
    print('   ' + '-' * 50)
    for name, keys in sorted(by_shape.items(), key=lambda x: -len(x[1])):
        avg = sum(len(vi[k]) for k in keys) / len(keys)
        print(f'   {name:18} {len(keys):8} {100*len(keys)/total:5.1f} {avg:6.0f}')

    # Cross: general co bao nhieu % o moi dang?
    print('\nC. GENERAL tach theo dang (de biet "chua gan vung" gom gi)')
    g = by_dom['general']
    gb = collections.Counter(shape(src[k]) for k in g)
    for name, c in sorted(gb.items(), key=lambda x: -x[1]):
        print(f'   {name:18} {c:8} {100*c/len(g):5.1f}% cua general')

    print(f'\nD. HANH DONG: doc theo dang, khong theo linh vuc.')
    print('   1. van xuoi 178+20 = 198 chuoi  -> doc tay, may khong kiem duoc')
    print('   2. cau hoi 102 chuoi             -> doc: dau ? va dau cham con')
    print('   3. cau lenh 1449 chuoi           -> kiem: co con "duoc" (bi dong)?')
    print('   4. nhan ngan 5009 chuoi          -> kiem: co cat nhan >78c khong')


if __name__ == '__main__':
    main()