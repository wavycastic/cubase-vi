#!/usr/bin/env python3
"""Audit every term that rounds 38-51 changed, across the WHOLE map.

Rounds 38 to 51 changed about twenty terms. Every one of those is a chance
that some key nobody revisited still carries the old form, and a chance that a
new key was translated a second way while the change was being made - which is
what happened to Material, audio stream, Retrospective Record, External,
factory, Users and Cycle, one after another.

The audit is mechanical. For each term, list every distinct rendering the map
uses and how many keys use it. A rendering used by one or two keys against
dozens is a leftover, and the list says which.

  python tools/audit_terms.py [term ...]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

# term -> (the rendering the glossary settled on, the old forms to catch)
TERMS = {
    'Duration':        ('thời lượng', ['trường độ']),
    'Chord Symbol':    ('hóa biểu', ['ký hiệu hợp âm']),
    'Key Signature':   ('số chỉ nhịp', ['hóa biểu']),
    'External':        ('External', ['bên ngoài', 'ngoài']),
    'Octave':          ('quãng tám', ['octave']),
    'Retrospective':   ('ghi hồi tố', ['hồi cứu']),
    'Material':        ('chất liệu', ['tư liệu']),
    'Cycle':           ('Cycle', ['chu kỳ']),
    'Factory':         ('Factory', ['xuất xưởng']),
    'User':            ('người dùng', ['các User', 'User đã']),
    'Warp Marker':     ('Warp Tab', ['Warp Marker']),
    'Disk Cache':      ('Disk Cache', ['bộ nhớ đệm đĩa']),
    'audio stream':    ('audio stream', ['luồng Audio']),
    'Word Clock':      ('Word Clock', ['Từ Clock', 'Word Clock ngoài']),
    'mouse wheel':     ('con lăn chuột', ['cuộn chuột']),
    'driver':          ('trình điều khiển', ['driver']),
    'Write Protection': ('bảo vệ ghi', ['chống ghi']),
    'Serial Port':     ('Cổng Serial', ['cổng serial']),
    'Emphasis':        ('làm nổi bật', ['nhấn mạnh']),
    'Zoom':            ('Zoom', ['Phóng to/thu nhỏ']),
    'Deactivate':      ('tắt', ['hủy kích hoạt']),
}

want = sys.argv[1:]
for term, (good, bad) in TERMS.items():
    if want and term.lower() not in [w.lower() for w in want]:
        continue
    # does the map use the term at all? look at the key column
    hit = [k for k in src if term.lower() in k.lower()]
    print(f'=== {term}   (keys: {len(hit)}, settled: {good!r})')
    for b in bad:
        n = [k for k, v in vi.items() if b in v]
        if n:
            print(f'    OLD {b!r} still in {len(n)} value(s):')
            for k in n[:6]:
                print(f'       {k[:60]!r}')
                print(f'         {vi[k][:96]!r}')
    # any other form of the same word, listed by key for a look
    others = [k for k in vi if term.lower() in k.lower()]
    print(f'    {len(others)} value(s) mention it; sample:')
    for k in others[:4]:
        print(f'       {vi[k][:96]!r}')
    print()
