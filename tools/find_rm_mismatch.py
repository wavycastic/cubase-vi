"""Check every "[RM]" key against its base key.

Cubase's extractor makes a second copy of a label for its read-mode display and
names it "X[RM]". Those are two separate <String> entries carrying the SAME
English, and the marker lives in the Key attribute and nowhere else.

What settles that is not an argument, it is the original translation.xml: all
EIGHT vendors translate the pair IDENTICALLY, and not one of them puts the
marker in the value.

    Keep History        de "Verlauf speichern"   fr "Garder historique"
    Keep History[RM]    de "Verlauf speichern"   fr "Garder historique"

    New Parts           de "Neue Parts"          fr "Nouveaux conteneurs"
    New Parts[RM]       de "Neue Parts"          fr "Nouveaux conteneurs"

    Stacked             ru "Nakoplenie dublei"
    Stacked[RM]         ru "S nakopleniem"

So the rule is: the value of X[RM] EQUALS the value of X, with no marker. The
first version of this tool asserted the opposite - that the value should be the
base value PLUS "[RM]" - and eleven values followed that wrong rule, which means
the string "[RM]" was going to be drawn on screen next to eleven labels in read
mode. A tool that encodes a guess is worse than no tool, and this one had a
plausible-looking story behind the guess.

Two of the pairs also disagreed on the wording, which is the part no rule
catches:

    "Keep History[RM]"  ->  "Giu History[RM]"     "History" untranslated
    "New Parts[RM]"     ->  "Tao Parts[RM]"       a different reading of
                                                   the same English

Both are the same defect - the pair must be one string - and both are visible
here because the values are compared for EQUALITY rather than for shape.

  python tools/find_rm_mismatch.py
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

MARK = '[RM]'
rows = []
orphan = []
for k in sorted(vi):
    if not k.endswith(MARK):
        continue
    base = k[:-len(MARK)]
    if base not in vi:
        orphan.append(k)
        continue
    if vi[k] != vi[base]:
        rows.append((k, base, vi[k], vi[base]))

print(f'[RM] keys whose value differs from the base key: {len(rows)}')
print(f'[RM] keys with no base key at all: {len(orphan)}\n')
for k, base, got, want in rows:
    print(f'  {k[:60]!r}')
    print(f'      EN   {src.get(k, "?")[:64]!r}')
    print(f'      got  {got[:70]!r}')
    print(f'      base {want[:70]!r}')
    print()
print('--- [RM] keys with no base key: nothing to compare against, and the')
print('    marker has nothing to copy, so it must not be in the value either')
for k in orphan:
    bad = MARK in vi[k]
    print(f'  {"MARKER IN VALUE" if bad else "ok":16} {k[:44]!r}  VI {vi[k][:44]!r}')
