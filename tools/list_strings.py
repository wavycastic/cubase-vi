#!/usr/bin/env python3
"""Dump all String Key / <us> pairs from translation.xml into a TSV."""
import re, sys, json

src = sys.argv[1]
out = sys.argv[2]
txt = open(src, encoding='utf-8').read()

def unesc(s):
    return (s.replace('&lt;', '<').replace('&gt;', '>')
             .replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&'))

rows = []
for m in re.finditer(r'<String Key="(.*?)">(.*?)</String>', txt, re.S):
    key = unesc(m.group(1))
    body = m.group(2)
    u = re.search(r'<us>(.*?)</us>', body, re.S)
    us = unesc(u.group(1)) if u else ''
    rows.append((key, us))

with open(out, 'w', encoding='utf-8', newline='') as f:
    f.write('key\tus\n')
    for k, u in rows:
        f.write(f'{k}\t{u}\n')

print(f'wrote {out}: {len(rows):,} rows')

short = [(k, u) for k, u in rows if 0 < len(u) <= 40 and '\\' not in u and '{' not in u]
print(f'short (<=40 chars, no placeholders): {len(short):,}')

# a quick view of the most "menu-like" ones
menus = [(k, u) for k, u in rows if re.fullmatch(r'[A-Za-z][A-Za-z \-&/]{0,28}', u) and len(u) <= 30]
print(f'menu-like candidates: {len(menus):,}')
print('\n--- first 120 menu-like ---')
for k, u in menus[:120]:
    print(f'  {u!r:34} key={k!r}')
