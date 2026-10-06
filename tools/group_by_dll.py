#!/usr/bin/env python3
"""Nhóm chuỗi theo vị trí trong TỪNG DLL của Cubase.

    python tools/group_by_dll.py                    # tóm tắt
    python tools/group_by_dll.py --list             # mọi cụm
    python tools/group_by_dll.py -c ScoringEngine   # đọc một module

**Vì sao cần.** `group_by_offset.py` chỉ quét `Cubase15.exe`. Đo được:
trong 3.973 chuỗi không có nhóm, **297** nằm trong DLL khác —

    ScoringEngine.dll      61        OMFFilter.dll         50
    Sampler Track.dll      54        aaffilter.dll         36
    Drum Machine.dll       19        admeditor.dll         13

Mỗi DLL là một module UI riêng, nên offset của nó tự nó đã là một nhóm
chức năng: cắt `.rdata` của `OMFFilter.dll` ra là ra nhóm của bộ lọc AAF.
Không cần gán chúng vào cụm của exe — chúng không thuộc cụm đó.

Kết quả: exe 6.642 chuỗi / 333 cụm, DLL thêm 297 chuỗi.
"""
import argparse
import bisect
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
CUBASE = r'E:\Steinberg\Cubase 15'

GAP = 4000
MIN_CLUSTER = 2
MIN_LETTERS = 3

ASCII = re.compile(rb'[\x20-\x7e]{3,}')
U16 = re.compile(rb'(?:[\x20-\x7e]\x00){3,}')


def core_letters(t):
    return re.sub(r'[^A-Za-z]', '', t)


def us_map():
    src = open(os.path.join(ROOT, 'keys', 'translation_original.xml'),
               encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<String Key="([^"]*)">(.*?)</String>', src, re.S):
        L = dict(re.findall(r'<(\w+)>(.*?)</\1>', m.group(2), re.S))
        out[m.group(1)] = L.get('us', '')
    return out


def dlls():
    pats = ('*.dll', '*.plg')
    found = []
    for p in pats:
        found += glob.glob(os.path.join(CUBASE, '**', p), recursive=True)
    return sorted(found)


def scan(path, want):
    """Mọi literal của `want` trong một file -> [(text, offset)]."""
    data = open(path, 'rb').read()
    hits = []
    seen = set()
    for rx, dec in ((ASCII, 'ascii'), (U16, 'utf-16-le')):
        for m in rx.finditer(data):
            try:
                t = m.group().decode(dec)
            except UnicodeDecodeError:
                continue
            if t not in want or t in seen:
                continue
            if len(core_letters(t)) < MIN_LETTERS:
                continue
            seen.add(t)
            hits.append((t, m.start()))
    return hits


def build(gap=GAP, modules=None, exclude=None):
    """`exclude` = set key đã có nhóm trong exe. Bỏ chúng ra, vì DLL của
    Cubase dùng CHUNG một bể chuỗi UI với exe — quét cả 10.737 key vào mọi
    DLL ra 6.087 chuỗi, nhưng phần lớn đã có nhóm sẵn ở exe. Chỉ phần chưa
    có nhóm mới là thông tin mới: 297 chuỗi."""
    us = us_map()
    want = {}
    for k, u in us.items():
        if u and len(core_letters(u)) >= MIN_LETTERS:
            want.setdefault(u, []).append(k)
    if exclude:
        want = {t: ks for t, ks in want.items()
                if not all(k in exclude for k in ks)}
    named = []
    for path in dlls():
        base = os.path.basename(path)
        mod = os.path.splitext(base)[0]
        if modules and not any(m.lower() in mod.lower() for m in modules):
            continue
        hits = scan(path, want)
        if len(hits) < MIN_CLUSTER:
            continue
        hits.sort(key=lambda kv: kv[1])
        groups = []
        for t, off in hits:
            if groups and off - groups[-1][-1][1] <= gap:
                groups[-1].append((t, off))
            else:
                groups.append([(t, off)])
        groups = [g for g in groups if len(g) >= MIN_CLUSTER]
        if groups:
            named.append((mod, len(groups), groups))
    return named


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', metavar='TEXT',
                    help='đọc module có tên chứa TEXT')
    ap.add_argument('-l', '--list', action='store_true', help='mọi module')
    ap.add_argument('-m', '--module', action='append', metavar='NAME',
                    help='chỉ quét module này')
    ap.add_argument('--gap', type=int, default=GAP)
    ap.add_argument('--all', action='store_true',
                    help='không loại chuỗi đã có nhóm trong exe')
    a = ap.parse_args()

    exclude = None
    if not a.all:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'gbo', os.path.join(ROOT, 'tools', 'group_by_offset.py'))
        gbo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gbo)
        keys, found, amb, named_exe = gbo.build(a.gap)
        exclude = set(k for _, _, _, c in named_exe for k, _ in c)
        print('exe: %d chuoi da co nhom (bi lo khoi DLL)\n' % len(exclude))

    named = build(a.gap, a.module, exclude)
    total = sum(len(k) for _, _, g in named for k in g)

    if a.c:
        for mod, _, groups in named:
            for g in groups:
                for t, _ in g:
                    if a.c.lower() in t.lower():
                        us = us_map()
                        want = {}
                        for k, u in us.items():
                            want.setdefault(u, []).append(k)
                        print('#### %s (%d chuoi)' % (mod, len(g)))
                        for t2, _ in g:
                            k = want.get(t2, ['?'])[0]
                            print('  %-40r %s' % (t2[:38], k))
                        print()
        return

    if a.list:
        for mod, ng, groups in named:
            print('### %s (%d cum, %d chuoi)'
                  % (mod, ng, sum(len(g) for g in groups)))
            for g in groups:
                us = us_map()
                print('   %d chuoi' % len(g))
        return

    print('nhom theo DLL: %d module, %d chuoi co nhom'
          % (len(named), total))
    for mod, ng, groups in sorted(named, key=lambda t: -sum(len(g)
                                                            for g in t[2])):
        print('  %-30s %3d cum  %4d chuoi'
              % (mod[:30], ng, sum(len(g) for g in groups)))


if __name__ == '__main__':
    main()