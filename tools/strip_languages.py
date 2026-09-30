#!/usr/bin/env python3
"""Strip translation.xml down to English and Vietnamese only.

    usage: strip_languages.py <in.xml> <out.xml> [--keep us,vi]

Cubase's file carries nine languages for every one of its 10,737 strings, and the
eight this project does not use account for about 82% of the text:

    ru 544,420   jp 534,556   fr 471,434   it 470,224
    es 447,688   pt 443,998   de 433,529   zh 361,083     bytes
    us 379,104   vi 443,091                                 bytes

    full build      5,328,470 bytes
    two languages   ~1,621,538 bytes

WHY IT IS A SEPARATE FILE AND NOT A REPLACEMENT. The original has exactly nine
language elements in all 10,737 entries - not one entry anywhere is missing one,
so the file is perfectly uniform and a reduced one is a shape Cubase has never
been handed. Two things make that recoverable rather than risky:

  - keys/translation_original.xml is the source build_translation.py reads, it
    is in git, and install.ps1 writes a .bak beside every file it overwrites
    and has an -Action uninstall that puts it back;
  - this is a build TARGET, not a step. build.py still produces the full file,
    and this one is opt-in.

WHAT IS TOUCHED. Only the language ELEMENTS inside each <String> are removed, and
only those whose key is not in --keep. Nothing else is rewritten: not the
<LanguageTable>, not the <String Key>, not the order, not the whitespace between
elements. The output is therefore still the original document with some children
of each <String> taken out, which is the smallest possible edit.

  python tools/strip_languages.py keys/translation_original.xml build/x.xml
"""
import re, sys, os

src, dst = sys.argv[1], sys.argv[2]
keep = {'us', 'vi'}
if '--keep' in sys.argv:
    keep = {s.strip() for s in sys.argv[sys.argv.index('--keep') + 1].split(',')}

with open(src, 'r', encoding='utf-8') as f:
    txt = f.read()

# Every language element. The indentation is three tabs inside a <String> and
# the elements sit on their own lines:
#
#   \t\t<String Key="...">
#   \t\t\t<us>...</us>
#   \t\t\t<de>...</de>
#
# Only elements at THREE tabs are inside a <String>. The <LanguageTable> entries
# are at two tabs and must survive - they are what makes "Vietnamese" appear in
# the language list at all.
ELEM = re.compile(r'\n\t\t\t<(\w+)>(.*?)</\1>', re.S)
seen = set()
removed = [0]


def prune(m):
    lang = m.group(1)
    seen.add(lang)
    if lang in keep:
        return m.group(0)
    removed[0] += 1
    return ''


out = ELEM.sub(prune, txt)

# self-closing <de/> style, if the file ever uses one
EMPTY = re.compile(r'\n\t\t\t<(\w+)\s*/>')


def prune_empty(m):
    lang = m.group(1)
    seen.add(lang)
    if lang in keep:
        return m.group(0)
    removed[0] += 1
    return ''


out = EMPTY.sub(prune_empty, out)

# The <LanguageTable> lists the languages Cubase will OFFER in
# Edit > Preferences > General > Language. If it keeps rows for languages whose
# strings are gone, the dropdown offers German and French and then has nothing
# for them, which is untidy at best and unexplained at worst. Dropping the rows
# makes the file consistently two-language, which is what was asked for.
#
# This is the one edit that is NOT a pure deletion of a <String> child, and it
# is why the file is a separate target rather than a change to the build: the
# language list is what puts Vietnamese in the menu.
if '--keep-langtable' not in sys.argv:
    ROW = re.compile(r'\n\t\t<language key="(\w+)">([^<]*)</language>')
    dropped = []

    def prune_row(m):
        if m.group(1) in keep:
            return m.group(0)
        dropped.append((m.group(1), m.group(2)))
        return ''

    out = ROW.sub(prune_row, out)
    print(f'language rows dropped from the table: '
          f'{len(dropped)}  ({", ".join(k for k, _ in dropped)})')

with open(dst, 'w', encoding='utf-8', newline='') as f:
    f.write(out)

a, b = os.path.getsize(src), os.path.getsize(dst)
print(f'kept      : {sorted(keep)}')
print(f'languages found: {sorted(seen)}')
print(f'elements removed: {removed[0]:,}')
print(f'{a:,} bytes  ->  {b:,} bytes   ({100 * b / a:.0f}%)')

# a String that lost its <us> is broken, so check none did
lost = len(re.findall(r'<String Key="[^"]*">(?:(?!</String>).)*?</String>', out, re.S))
n_str = out.count('<String Key=')
bad = 0
for m in re.finditer(r'<String Key="[^"]*">(.*?)</String>', out, re.S):
    if '<us>' not in m.group(1):
        bad += 1
print(f'String entries: {n_str:,}   without <us>: {bad}')
sys.exit(1 if bad else 0)
