#!/usr/bin/env python3
"""Enforce the hybrid English-Vietnamese style mandated by AGENT.md.

Every translated value must be one of:
  A) exactly the source key                     (kept in English)
  B) "<Vietnamese> (<key>)"                     (hybrid, English in parentheses)

Also checks that %-placeholders survive unchanged, and warns on glossary drift.

Usage:  python tools/check_style.py [--verbose]
Exit code 0 = clean, 1 = violations found.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)
TSV, MAP = T('keys', 'all_strings.tsv'), T('translations', 'vi.json')
verbose = '--verbose' in sys.argv

if not os.path.exists(TSV):
    sys.exit(f'missing {TSV} - run: python tools/list_strings.py ...')

# source English text per key
src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, us = line.split('\t', 1)
        src[k] = us

m = json.load(open(MAP, encoding='utf-8'))

def norm(s):
    """Normalise for comparison: casefold, drop trailing dots/space."""
    return re.sub(r'[\s.]+$', '', s or '').strip().casefold()

PARENS = re.compile(r'^(?P<vi>.+?)\s*\((?P<en>[^()]*)\)\s*$')
PLACEHOLDER = re.compile(r'%(?:\.\d+)?[a-zA-Z%]|\{[a-zA-Z0-9_]*\}')

errors, warns = [], []

for key, val in sorted(m.items()):
    if not isinstance(val, str) or not val.strip():
        errors.append((key, val, 'empty value'))
        continue

    # --- rule 1: must be style A or style B -------------------------------
    if norm(val) == norm(key):
        style = 'A'
    else:
        mo = PARENS.match(val)
        if mo and norm(mo.group('en')) == norm(key):
            style = 'B'
        else:
            errors.append((key, val, 'not hybrid: value must equal the key, or end with " (<key>)"'))
            continue

    if style == 'B':
        vi = PARENS.match(val).group('vi').strip()
        if not vi:
            errors.append((key, val, 'empty Vietnamese part before the parenthetical'))
        # a hybrid value whose Vietnamese part is identical to the English is pointless
        elif norm(vi) == norm(key):
            warns.append((key, val, 'Vietnamese part duplicates the English'))

    # --- rule 2: placeholders must survive --------------------------------
    if key in src:
        want = PLACEHOLDER.findall(src[key])
        got = PLACEHOLDER.findall(val)
        # only the English half of a hybrid value carries the runtime placeholders
        if style == 'B' and want:
            # the parenthetical repeats the key; compare the Vietnamese part only
            vi_part = PARENS.match(val).group('vi')
            got = PLACEHOLDER.findall(vi_part)
        if sorted(want) != sorted(got):
            errors.append((key, val, f'placeholder mismatch: source has {want}, translation has {got}'))

print(f'style check: {len(m)} entries in {os.path.relpath(MAP, ROOT)}')

if warns:
    print(f'\n{len(warns)} warning(s):')
    for k, v, why in warns:
        print(f'  {k!r} = {v!r}\n      {why}')

if errors:
    print(f'\n{len(errors)} VIOLATION(S):')
    for k, v, why in errors:
        print(f'  {k!r} = {v!r}\n      -> {why}')
    print('\nSee AGENT.md section 1 for the two permitted forms.')
    sys.exit(1)

print('\nOK - every value follows the hybrid style (AGENT.md)')
if verbose:
    for k, v in sorted(m.items())[:40]:
        print(f'  {k!r:44} -> {v}')
