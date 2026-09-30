#!/usr/bin/env python3
"""Check every quoted name against the translation of the LABEL it names.

The rule is not "quoted names stay English" - that was the first, wrong version
of this tool. The rule is:

    a quoted name must match what the LABEL it names is translated to.

because in a localised Cubase the menu shows the localised name, so a tooltip
that quotes the English is as wrong as one that quotes a Vietnamese string the
menu does not contain.

    'Part Editing Mode'   -> label "Part Editing Mode" is "Che do sua Part"
                            so 'Che do sua Part' in a sentence is CORRECT

    'Z-Axis Pan'         -> there is no label "Z-Axis Pan"; the parameter is
                            called Z-Axis Pan in the automation lane in every
                            language, so quoting it in English is CORRECT

Both readings are right, and only looking at the label decides between them.
Rounds 45, 46 and 47 each fixed a few of these by hand and each time the rule
turned out to be subtler than "keep it English", which is what a first pass at
this tool assumed.

So for every quoted name in every value: find the label whose English is exactly
that name, read its translation, and compare. That is mechanical, and it
catches both directions - a name translated where the label is English, and a
name left English where the label is Vietnamese.

  python tools/find_quoted_names.py
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
longest = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
        # Cubase truncates the long keys, and column 2 is truncated with them -
        # which CUTS A QUOTE IN HALF and makes the two sides disagree. The
        # untruncated text is another row's key, so prefer it when there is
        # exactly one candidate.
        longest.setdefault(k[:60], []).append(k)


def full(k):
    cand = longest.get(k[:60], [])
    if len(cand) == 1 and len(cand[0]) > len(k):
        return cand[0]
    return src.get(k, '')


vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# A VIETNAMESE LETTER, spelled with escapes on purpose. The obvious
# [A-ỿ] is U+0100 to U+1EF9, and it is WRONG: Vietnamese keeps its most
# common letters - a, a, e, e, o, o, u, u, d and their tone marks - in
# U+00C0 to U+00FF, which is BELOW the start of that range. So a value
# written entirely with those letters, like "Thêm bè", tested as NOT
# Vietnamese, and eight detectors built on this test were quietly looking
# at a subset of the map. Found in round 53, by a value that should have
# been reported and was not.
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# names that are button faces or dropdown values rather than menu commands, and
# are therefore named by what is printed on them in every language. Round 48
# found that matching the label blindly gives "Bat \"Bat ghi\" hoac \"Monitor\""
# - enable, enable-record, or monitor.
BUTTONS = {'Record Enable', 'Monitor', 'Solo', 'Read', 'Write', 'Any', 'or'}
# Cubase truncates the long keys, so a key of 60+ characters is a prefix of its
# own English; the quote regex sees the prefix's quotes as if they were the
# whole string.
Q = re.compile(r"'([^'\\]{3,60})'|\"([^\"\\]{3,60})\"")
TRIM = str.maketrans('', '', '\\')


def clean(s):
    return s.replace('\\', '').strip()


rows = []
for k, v in vi.items():
    en = full(k)
    if not en:
        continue
    a = {clean(m.group(1) or m.group(2)) for m in Q.finditer(en)}
    if not a:
        continue
    b = {clean(m.group(1) or m.group(2)) for m in Q.finditer(v)}
    for name in a:
        if name in BUTTONS:
            continue
        # the label this name refers to, if the map has one
        label = vi.get(name, src.get(name, None))
        if label is None:
            continue                      # no such label: nothing to match
        want = clean(label)
        if name in b:
            # quoted the English name. Right only if the label is English too.
            if want != name and HAN.search(want):
                rows.append((name, want, k, v, sorted(b), 'ENGLISH QUOTE'))
            continue
        if want in b:
            continue                      # quoted as the label translates
        rows.append((name, want, k, v, sorted(b), 'WRONG FORM'))

rows.sort()
print(f'quoted names that do not match their own label: {len(rows)}\n')
for name, want, k, v, b, why in rows:
    viet = HAN.search(want) is not None
    print(f'  {why:<13} label {name!r} is {want!r} ({"VI" if viet else "EN"})')
    print(f'    in {k[:66]!r}')
    print(f'    VI quotes {b}')
    print()
