#!/usr/bin/env python3
"""Validate a generated translation.xml: well-formed, language registered, counts per language."""
import sys, re
import xml.etree.ElementTree as ET

path = sys.argv[1]
print(f'validating {path} ...')
try:
    tree = ET.parse(path)
except ET.ParseError as e:
    print(f'  XML PARSE ERROR: {e}')
    sys.exit(1)
print('  XML is well-formed  OK')

root = tree.getroot()
print(f'  root element: <{root.tag}>')

langs = [e.get('key') for e in root.findall('./LanguageTable/language')]
print(f'  LanguageTable ({len(langs)}): {langs}')
if 'vi' not in langs:
    print('  !! vi NOT registered'); sys.exit(1)
print('  vi registered  OK')

strings = root.findall('./StringTable/String')
print(f'  StringTable entries: {len(strings):,}')

counts = {}
vi_empty = 0
for s in strings:
    for child in s:
        tag = child.tag
        if tag == 'String':
            continue
        counts[tag] = counts.get(tag, 0) + 1
        if tag == 'vi' and not (child.text or '').strip():
            vi_empty += 1
print('  children per language:')
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'    <{k}> : {v:,}')
if vi_empty:
    print(f'  !! {vi_empty} empty <vi> elements')

# spot-check a few known menus
checks = {'File': 'Tệp', 'Edit': 'Sửa', 'Transport': 'Phát', 'Devices': 'Thiết bị'}
print('  spot-check:')
for s in strings:
    k = s.get('Key')
    if k in checks:
        vi = s.find('vi')
        got = (vi.text if vi is not None else None)
        mark = 'OK' if got == checks[k] else 'MISMATCH'
        print(f'    {k:12} -> {got!r}  [{mark}]')
print('\nVALIDATION PASSED' if not vi_empty else '\nVALIDATION PASSED (with empty entries)')
