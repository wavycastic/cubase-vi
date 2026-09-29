#!/usr/bin/env python3
"""Enforce the natural hybrid English-Vietnamese style mandated by AGENT.md.

Rules:
  1. NO trailing parenthetical glosses like "(<key>)" or "(English)" at the end.
     Translations must be natural Vietglish without dictionary-style parentheses!
  2. DAW technical loanwords (Track, Channel, Bus, Fader, Pan, Insert, Send,
     Metronome, Click, Marker, Locator, Automation, Clip, Event, Quantize,
     Snap, Grid, Bounce, Render, Freeze, Warp, ASIO, VST, MIDI...) must stay in English.
  3. %-placeholders (%s, %d, %.3f, etc.) must survive intact.
  4. No empty values.

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

src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, us = line.split('\t', 1)
        src[k] = us

m = json.load(open(MAP, encoding='utf-8'))

FORBIDDEN_PARENS = re.compile(r'\s*\([^()]+\)\s*$')
FORBIDDEN_TRANSLATIONS = {
    r'\btự động hóa\b': 'Automation',
    r'\brãnh\b': 'Track',
    r'\bđoạn cắt\b': 'Clip',
    r'\bnảy\b': 'Bounce',
    r'\bđóng băng\b': 'Freeze',
    r'\blượng tử hóa\b': 'Quantize',
}
PLACEHOLDER = re.compile(r'%(?:\.\d+)?[a-zA-Z%]|\{[a-zA-Z0-9_]*\}')

errors, warns = [], []

for key, val in sorted(m.items()):
    if not isinstance(val, str) or not val.strip():
        errors.append((key, val, 'empty value'))
        continue

    # Rule 1: No trailing dictionary parentheses like "... (Key)" unless the key itself has them!
    if not FORBIDDEN_PARENS.search(key):
        mo = FORBIDDEN_PARENS.search(val)
        if mo:
            # Check if the text inside parens is an English word or matches key
            inside = mo.group(0).strip()[1:-1].strip()
            if inside.lower() in key.lower() or len(inside) >= 3 and inside.isascii():
                errors.append((key, val, f'dictionary-style parenthesis {mo.group(0)!r} forbidden by AGENT.md'))
                continue

    # Rule 2: No awkward literal Vietnamese translations of standard DAW terms
    val_lower = val.lower()
    for pattern, term in FORBIDDEN_TRANSLATIONS.items():
        if re.search(pattern, val_lower, re.IGNORECASE):
            errors.append((key, val, f'awkward translation of DAW term: keep {term!r} in English'))

    # Rule 3: Placeholders must match
    if key in src:
        want = sorted(PLACEHOLDER.findall(src[key]))
        got = sorted(PLACEHOLDER.findall(val))
        if want != got:
            errors.append((key, val, f'placeholder mismatch: source has {want}, translation has {got}'))

print(f'style check: {len(m)} entries in {os.path.relpath(MAP, ROOT)}')

if warns:
    print(f'\n{len(warns)} warning(s):')
    for k, v, why in warns:
        print(f'  {k!r} = {v!r}\n      {why}')

if errors:
    print(f'\n{len(errors)} VIOLATION(S):')
    for k, v, why in errors[:25]:
        print(f'  {k!r} = {v!r}\n      -> {why}')
    if len(errors) > 25:
        print(f'  ... and {len(errors)-25} more')
    print('\nSee AGENT.md for natural hybrid English-Vietnamese guidelines.')
    sys.exit(1)

print('\nOK - every value follows the natural hybrid style (AGENT.md)')
if verbose:
    for k, v in sorted(m.items())[:40]:
        print(f'  {k!r:44} -> {v}')
