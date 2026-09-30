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

# 1) register the language.
#
# The indentation is taken from the sibling <language> lines rather than
# hardcoded.  The old version emitted a literal two-tab indent, which landed one
# tab deeper than its nine siblings because those two tabs of existing
# indentation were still in front of the insertion point.  XML does not care; a
# diff of 10,737 entries does, and the odd line made the injected entry look
# like a sibling of the table rather than a member of it.
if f'<language key="{lang}">' not in txt:
    existing = re.findall(r'\n(\t*)<language key="', txt)
    if not existing:
        sys.exit(f'no <language key=...> lines found in {src}')
    depth = existing[-1]
    # Anchor on the whole closing line, not on the tag text.  Replacing just
    # '</LanguageTable>' leaves that tag's own leading tab in front of the new
    # line, which is how the earlier attempt ended up one tab too deep.
    m_close = re.search(r'\n(\t*)</LanguageTable>', txt)
    if not m_close:
        sys.exit(f'no </LanguageTable> found in {src}')
    close_depth = m_close.group(1)
    txt = (txt[:m_close.start()]
           + f'\n{depth}<language key="{lang}">{langname}</language>'
           + m_close.group(0)
           + txt[m_close.end():])
    print(f'+ registered language {lang} = {langname} at '
          f'{len(depth)} tab(s), matching its nine siblings')

# 2) add <vi> to each String that we have a translation for
added = 0
matched = set()
out = []
pos = 0
pat = re.compile(r'<String Key="(.*?)">(.*?)</String>', re.S)

# The depth the nine shipped language tags sit at inside a <String>.  Taken from
# the file, so the injected <vi> is a child of <String> exactly like its
# siblings.  The old version appended the block at whatever indentation
# </String> already had, which is one tab less - it read as though <vi> closed
# the <String> rather than belonging to it.
_depths = re.findall(r'\n(\t*)<\w\w>', txt)
TAG_DEPTH = (max(set(_depths), key=_depths.count) if _depths else '\t\t\t')
for m in pat.finditer(txt):
    key, body = m.group(1), m.group(2)
    raw_key = (key.replace('&lt;', '<').replace('&gt;', '>')
                  .replace('&quot;', '"').replace('&amp;', '&'))
    if raw_key in tmap:
        matched.add(raw_key)
        vi = esc(tmap[raw_key])
        if re.search(rf'<{lang}>.*?</{lang}>', body, re.S):
            continue
        # Where to insert, and what to insert.
        #
        # The text just before </String> already ends with a newline and that
        # tag's own indentation, so inserting at the position of </String>
        # itself and supplying a leading newline leaves that indentation
        # orphaned on a line of its own.  The offset therefore moves back over
        # it, and the block brings its own newline and depth.  An earlier
        # attempt did not, and tools/check_translation_build.py caught it: the
        # stripped output was 32,211 characters longer than the original, which
        # is three per entry.
        _close = re.search(r'\n(\t*)</String>\s*$', m.group(0))
        close_depth = _close.group(1) if _close else TAG_DEPTH
        insert_at = m.end() - len('</String>') - len(close_depth) - 1
        out.append((insert_at, f'\n{TAG_DEPTH}<{lang}>{vi}</{lang}>'))
        added += 1

print(f'  <{lang}> block at {len(TAG_DEPTH)} tab(s), matching its nine '
      'siblings')

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
