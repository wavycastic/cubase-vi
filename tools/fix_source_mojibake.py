#!/usr/bin/env python3
"""Repair U+FFFD corruption inside the leak_fixes_*.py source files.

fix_mojibake.py cleans the batches, but apply_retouch.py then writes the fix
maps back over them - so a corrupt value in a fix map silently undoes the
repair. This rewrites the map entries from the verified REPAIRS table so the
source of truth is clean too.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fix_mojibake import REPAIRS

FILES = sorted(glob.glob(os.path.join(ROOT, 'tools', 'leak_fixes_*.py')))
# '...' with no quotes, so a one-line entry is rewritten as a whole
ASSIGN = re.compile(r'^(?P<indent>\s*)(?P<key>".*?"|\'.*?\'):\s*(?P<val>".*?"|\'.*?\'),\s*$')

total = 0
for path in FILES:
    lines = open(path, encoding='utf-8').read().split('\n')
    changed = False
    for i, line in enumerate(lines):
        if '\ufffd' not in line:
            continue
        m = ASSIGN.match(line)
        if not m:
            print(f'  !! cannot parse {os.path.basename(path)}:{i + 1}')
            continue
        key = m.group('key')[1:-1]
        # the file stores the key with escapes; the repairs table is literal
        probe = key.replace('\\\\', '\\').replace('\\"', '"').replace("\\'", "'")
        new = REPAIRS.get(probe)
        if new is None:
            print(f'  !! no repair for {probe!r}')
            continue
        rendered = new.replace('\\', '\\\\').replace("'", "\\'")
        lines[i] = (f'{m.group("indent")}{m.group("key")}: '
                    f"'{rendered}',")
        print(f'  fixed {os.path.basename(path)}:{i + 1}')
        changed = True
        total += 1
    if changed:
        open(path, 'w', encoding='utf-8').write('\n'.join(lines))

print(f'\nrepaired {total} source entry/entries')

# verify nothing is left anywhere in the fix maps
left = []
for path in FILES:
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        if '\ufffd' in line:
            left.append(f'{os.path.basename(path)}:{n}')
print('remaining U+FFFD in fix maps:', left or 'none')
sys.exit(1 if left else 0)
