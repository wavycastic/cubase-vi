#!/usr/bin/env python3
"""Inject a <vi> language into a Steinberg translation.xml.

usage: inject.py <in.xml> <out.xml> <map.json> [--langname Vietnamese]
map.json: { "<String Key value>": "<Vietnamese>", ... }
Only keys present in the map get a <vi> element; everything else falls back to English.
"""
import json, re, sys, os

src, dst, mapfile = sys.argv[1], sys.argv[2], sys.argv[3]
langname = 'Vietnamese'
if '--langname' in sys.argv:
    langname = sys.argv[sys.argv.index('--langname') + 1]
lang = 'vi'

with open(src, 'r', encoding='utf-8') as f:
    txt = f.read()
with open(mapfile, 'r', encoding='utf-8') as f:
    tmap = json.load(f)

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

# 1) register the language
if f'<language key="{lang}">' not in txt:
    txt = txt.replace(
        '</LanguageTable>',
        f'\t\t<language key="{lang}">{langname}</language>\n\t</LanguageTable>', 1)
    print(f'+ registered language {lang} = {langname}')

# 2) add <vi> to each String that we have a translation for
added = 0
matched = set()
out = []
pos = 0
pat = re.compile(r'<String Key="(.*?)">(.*?)</String>', re.S)
for m in pat.finditer(txt):
    key, body = m.group(1), m.group(2)
    raw_key = (key.replace('&lt;', '<').replace('&gt;', '>')
                  .replace('&quot;', '"').replace('&amp;', '&'))
    if raw_key in tmap:
        matched.add(raw_key)
        vi = esc(tmap[raw_key])
        if re.search(rf'<{lang}>.*?</{lang}>', body, re.S):
            continue
        out.append((m.end() - len('</String>'), f'<{lang}>{vi}</{lang}>\n\t\t'))
        added += 1

for off, ins in reversed(out):
    txt = txt[:off] + ins + txt[off:]

unmatched = [k for k in tmap if k not in matched]
if unmatched:
    print(f'! {len(unmatched)} map entries had no matching <String Key>:')
    for k in unmatched:
        print(f'    - {k!r}')

with open(dst, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)

print(f'+ injected <{lang}> into {added:,} strings')
print(f'  map entries : {len(tmap):,}')
print(f'  output      : {os.path.getsize(dst):,} bytes (was {os.path.getsize(src):,})')
