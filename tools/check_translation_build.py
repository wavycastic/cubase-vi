"""Prove build/translation_vi.xml is the original plus <vi>, and nothing else.

This is the invariant the whole project rests on, and install.ps1 asserts a
version of it in prose ("no <us> and no <vi> lost").  Asserting it mechanically
catches what prose does not: a mis-indented injection, a dropped entry, a
changed English string.

Checks, in order:
  1. the file parses;
  2. it has 10,737 <String> entries, each with exactly 10 language blocks;
  3. the nine original languages are byte-identical to the original file;
  4. the <vi> values are exactly translations/vi.json;
  5. removing the injected lines reproduces the original byte for byte;
  6. the injected lines are indented like their siblings.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = r'E:\01_Projects\cubase-vi'
ORIG = os.path.join(ROOT, 'keys', 'translation_original.xml')
BUILT = os.path.join(ROOT, 'build', 'translation_vi.xml')
VI = os.path.join(ROOT, 'translations', 'vi.json')
CODES = ('us', 'de', 'fr', 'es', 'it', 'pt', 'jp', 'zh', 'ru')

if not os.path.exists(BUILT):
    sys.exit(f'{BUILT} not built - run: python tools\\build.py')

orig = open(ORIG, encoding='utf-8').read()
built = open(BUILT, encoding='utf-8').read()
vi = json.load(open(VI, encoding='utf-8'))

fail = []


def check(ok, label, detail=''):
    print(f'  {"PASS" if ok else "FAIL"}  {label}' + (f'  {detail}' if detail
                                                      else ''))
    if not ok:
        fail.append(label)


print('=== 1. it parses ===')
try:
    root = ET.parse(BUILT).getroot()
    check(True, 'well-formed XML', f'root <{root.tag}>')
except ET.ParseError as exc:
    check(False, 'well-formed XML', str(exc))
    sys.exit(1)

print('=== 2. shape ===')
entries = list(root.iter('String'))
check(len(entries) == 10737, '10,737 String entries', f'{len(entries):,}')
shapes = {}
for e in entries:
    kids = tuple(c.tag for c in e)
    shapes[kids] = shapes.get(kids, 0) + 1
check(len(shapes) == 1, 'one block shape across all entries',
      f'{len(shapes)} distinct')
for shape, n in shapes.items():
    check(list(shape) == list(CODES) + ['vi'],
          'blocks are the nine originals then vi', f'{n:,} entries: {shape}')
langs = [l.get('key') for l in root.iter('language')]
check(langs == list(CODES) + ['vi'], 'LanguageTable is the nine then vi',
      f'{langs}')

print('=== 3. the nine original languages are untouched ===')
ENTRY = re.compile(r'<String Key="((?:[^"]|"(?!>))*)">(.*?)</String>', re.S)
o_entries = list(ENTRY.finditer(orig))
b_entries = list(ENTRY.finditer(built))
check(len(o_entries) == len(b_entries) == 10737,
      'same entry count', f'{len(o_entries):,} / {len(b_entries):,}')
diff = 0
for om, bm in zip(o_entries, b_entries):
    if om.group(1) != bm.group(1):
        diff += 1
        continue
    for code in CODES:
        a = re.search(rf'<{code}>(.*?)</{code}>', om.group(2), re.S)
        b = re.search(rf'<{code}>(.*?)</{code}>', bm.group(2), re.S)
        if (a and b and a.group(1) != b.group(1)) or bool(a) != bool(b):
            diff += 1
check(diff == 0, 'no <us>..<ru> value changed', f'{diff} differing')

print('=== 4. the <vi> values are exactly vi.json ===')


def unescape(s):
    return (s.replace('&lt;', '<').replace('&gt;', '>')
             .replace('&quot;', '"').replace('&apos;', "'")
             .replace('&amp;', '&'))


missing = wrong = 0
for m in b_entries:
    key = unescape(m.group(1))
    v = re.search(r'<vi>(.*?)</vi>', m.group(2), re.S)
    if not v:
        missing += 1
        continue
    if vi.get(key) != unescape(v.group(1)):
        wrong += 1
check(missing == 0, 'every entry has a <vi>', f'{missing} without')
check(wrong == 0, 'every <vi> equals vi.json', f'{wrong} differing')
check(len(vi) == 10737, 'vi.json holds 10,737', f'{len(vi):,}')

print('=== 5. removing the injected lines reproduces the original ===')
stripped = re.sub(r'\n\t*<vi>.*?</vi>', '', built, flags=re.DOTALL)
stripped = re.sub(r'\n\t*<language key="vi">[^<]*</language>', '', stripped)
check(stripped == orig, 'byte-for-byte identical to the original',
      f'{len(stripped):,} vs {len(orig):,} chars')

print('=== 6. the injected lines are indented like their siblings ===')
depths = {}
for m in re.finditer(r'\n(\t+)<(\w\w)>', built):
    depths.setdefault(m.group(2), set()).add(len(m.group(1)))
nine = set()
for c in CODES:
    nine |= depths.get(c, set())
check(depths.get('vi') == nine, '<vi> block matches its nine siblings',
      f'vi={sorted(depths.get("vi", []))} siblings={sorted(nine)}')
tbl = [len(l) - len(l.lstrip('\t'))
       for l in built[built.index('<LanguageTable>'):
                      built.index('</LanguageTable>')].splitlines()
       if '<language ' in l]
check(len(set(tbl)) == 1, '<language> lines all at one depth', f'{tbl}')

print()
print('FAILURES:', len(fail))
for f in fail:
    print('  ', f)
sys.exit(1 if fail else 0)
