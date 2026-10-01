#!/usr/bin/env python3
"""Score Editor round 1: voices, the band, keyboards and strings.

`instrumentnames_en.xml` holds 624 instrument entities and 1,126 distinct
name strings, none of which had ever been translated.  146 of them are
already settled - `tools/score_instruments.py import` reuses the 88 the main
UI table has translated and records the 58 that are correctly identical -
which leaves 980.

This round takes the four smallest families, 166 strings.  The style is not
invented here: it is the one `import` already established, and every rule
below is a rule the seeded 88 already follow.

  1. The instrument name stays English.

     `import` seeded `Conga` -> `Conga`, `Guitar` -> `Guitar`,
     `Hi-hat` -> `Hi-hat`, `Sampler` -> `Sampler`.  Vietnamese musicians say
     "guitar", "piano", "kora", not "đàn ghi-ta", and the German and Japanese
     catalogues agree: they translate the register qualifier and leave the
     instrument alone.

  2. A qualifier in brackets is translated, capitalised, and keeps its
     bracket.

     `Tenor Drum (High)` -> `Trống Tenor (Cao)`,
     `Tabla baya (larger)` -> `Tabla baya (Lớn hơn)`.  So `(Female)` is
     `(Nữ)` and `(High Tone)` is `(Âm cao)`, never "Cao" bare.

  3. Vietnamese has no plural, so a plural form takes the singular's wording.

     `Pianos`, `Accordions`, `Mezzo-sopranos` all become the singular.  The
     file keeps separate `singularFullName` and `pluralFullName` elements, and
     both are filled - the engine just gets the same word twice, which is
     correct rather than a gap.

  4. Abbreviations are not lengthened.

     `import` seeded `Ch.` -> `Ch.`, `Bar` -> `Bar.`, `Pan` -> `Pan`,
     `Tab.` -> `Tab`, `Synth.` -> `Synth`.  These are the part names in the
     score's instrument panel and in every part header, a column too narrow
     for a longer word.  `T. Dr.`, `M-S.`, `B. Vla da G.`, `P. F.` therefore
     stay exactly as they are.

  5. Section names are translated, because they are not instrument names.

     `Brass` -> `Bộ đồng` and `Keyboard` -> `Bàn phím` are both seeded, so
     `Strings` -> `Bộ dây` follows the same shape.

`Choir` -> `Dàn ca` and `Lead` -> `Dẫn` are the two judgement calls.  `Dàn ca`
is what a Vietnamese choir is called; "hợp thanh" would mean harmony, which is
a different thing.  `Lead` is the top line of a choral score, so `Dẫn`
("leads") rather than a mistranslation like `Chính`.

  python tools/fix_score01.py
  python tools/fix_score01.py --write
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from cubelib import score                                      # noqa: E402
from score_instruments import FAMILIES, family_of, load_batches  # noqa: E402

BATCH_DIR = os.path.join(ROOT, 'translations', 'score', 'instruments')
SOURCE = os.path.join(r'E:\Steinberg\Cubase 15', 'Components', 'ScoringEngine',
                      'l10n', 'instrumentnames_en.xml')
WRITE = '--write' in sys.argv
FAMILY = ('band', 'sing', 'keyb', 'str')

_, entities = score.read(SOURCE)
en = set(score.source_strings(entities))

WORDING = {
    # ---- band: the family vi.json already wrote `Marching Tenor Drum
    # (1 line)` -> `Trống Tenor diễu hành (1 dòng)`, so drop the qualifier
    'Marching Tenor Drum': 'Trống Tenor diễu hành',
    'Marching Tenor Drums': 'Trống Tenor diễu hành',
    'T. Dr.': 'T. Dr.',

    # ---- sing: voice ranges are loanwords in Vietnamese music, and the
    # main table already keeps Alto, Tenor and Soprano as they are
    'A.': 'A.',
    'Altos': 'Alto',
    'B.': 'B.',
    'Bar.': 'Bar.',
    'Baritone': 'Baritone',
    'Baritones': 'Baritone',
    'Bass': 'Bass',
    'Basses': 'Bass',
    'Ca.': 'Ca.',
    'Ch.': 'Ch.',
    'Choir': 'Dàn ca',
    'Choir (reduction)': 'Dàn ca (rút gọn)',
    'Contralto': 'Contralto',
    'Contraltos': 'Contralto',
    'Countertenor': 'Countertenor',
    'Countertenors': 'Countertenor',
    'Ct.': 'Ct.',
    'L.': 'L.',
    'Lead': 'Dẫn',
    'M-S.': 'M-S.',
    'Mezzo-soprano': 'Mezzo-soprano',
    'Mezzo-sopranos': 'Mezzo-soprano',
    'S.': 'S.',
    'Soprano': 'Soprano',
    'Sopranos': 'Soprano',
    'T.': 'T.',
    'Tenor': 'Tenor',
    'Tenors': 'Tenor',
    'Treble': 'Treble',
    'Trebles': 'Treble',
    'V.': 'V.',

    # ---- keyb
    'Accord.': 'Accord.',
    'Accordion': 'Accordion',
    'Accordions': 'Accordion',
    'Band.': 'Band.',
    'Bandoneon': 'Bandoneon',
    'Bandoneons': 'Bandoneon',
    'Cel.': 'Cel.',
    'Celesta': 'Celesta',
    'Celestas': 'Celesta',
    'Celeste': 'Celeste',
    'Celestes': 'Celeste',
    'Clav.': 'Clav.',
    'Clavichord': 'Clavichord',
    'Clavichords': 'Clavichord',
    'E. Org.': 'E. Org.',
    'E. Pno': 'E. Pno',
    'E. Pnos': 'E. Pno',
    'Electric Organ': 'Organ điện',
    'Electric Organs': 'Organ điện',
    'Electric Piano': 'Piano điện',
    'Electric Pianos': 'Piano điện',
    'H-t. Pno': 'H-t. Pno',
    'H-t. Pnos': 'H-t. Pno',
    'Har.': 'Har.',
    'Harmonium': 'Harmonium',
    'Harmoniums': 'Harmonium',
    'Harpsichord': 'Harpsichord',
    'Harpsichords': 'Harpsichord',
    'Honky-tonk Piano': 'Piano honky-tonk',
    'Honky-tonk Pianos': 'Piano honky-tonk',
    'Hpsd': 'Hpsd',
    'Hpsds': 'Hpsd',
    'Kbd': 'Kbd',
    'Kbds': 'Kbd',
    'Keyboards': 'Bàn phím',
    'Mel.': 'Mel.',
    'Melodica': 'Melodica',
    'Melodicas': 'Melodica',
    'Org.': 'Org.',
    'Organ': 'Organ',
    'Organs': 'Organ',
    'P. F.': 'P. F.',
    'Pianoforte': 'Pianoforte',
    'Pianofortes': 'Pianoforte',
    'Pianos': 'Piano',
    'Pno': 'Pno',
    'Pnos': 'Pno',
    'Synth.': 'Synth.',
    'Synthesizer': 'Synthesizer',

    # ---- str: the viol family, the lutes and the baroque strings all
    # keep their names, as the main table keeps Guitar and Djembe
    'B. Viol': 'B. Viol',
    'B. Viols': 'B. Viol',
    'B. Vla da G.': 'B. Vla da G.',
    'B. Vlas da G.': 'B. Vla da G.',
    'Bass Viol': 'Bass Viol',
    'Bass Viola da Gamba': 'Bass Viola da Gamba',
    'Bass Violas da Gamba': 'Bass Viola da Gamba',
    'Bass Viols': 'Bass Viol',
    'Cb.': 'Cb.',
    'Contrabass': 'Contrabass',
    'Contrabasses': 'Contrabass',
    'D. B.': 'D. B.',
    'Double Bass': 'Double Bass',
    'Double Basses': 'Double Bass',
    'Fid.': 'Fid.',
    'Fiddle': 'Fiddle',
    'Fiddles': 'Fiddle',
    'Guitarrón': 'Guitarrón',
    'Guitn': 'Guitn',
    'Guitns': 'Guitn',
    'H-gurdies': 'H-gurdy',
    'H-gurdy': 'H-gurdy',
    'Hurdy-gurdies': 'Hurdy-gurdy',
    'Hurdy-gurdy': 'Hurdy-gurdy',
    'Kora': 'Kora',
    'Koras': 'Kora',
    'Koto': 'Koto',
    'Kotos': 'Koto',
    'Oud': 'Oud',
    'Ouds': 'Oud',
    'Sar.': 'Sar.',
    'Sarangi': 'Sarangi',
    'Sarangis': 'Sarangi',
    'Sha.': 'Sha.',
    'Shamisen': 'Shamisen',
    'Shamisens': 'Shamisen',
    'St.': 'St.',
    'String Bass': 'String Bass',
    'String Basses': 'String Bass',
    'Strings': 'Bộ dây',
    'T. Viol': 'T. Viol',
    'T. Viols': 'T. Viol',
    'T. Vla da G.': 'T. Vla da G.',
    'T. Vlas da G.': 'T. Vla da G.',
    'Tambu.': 'Tambu.',
    'Tambura': 'Tambura',
    'Tambura (Female)': 'Tambura (Nữ)',
    'Tambura (Male)': 'Tambura (Nam)',
    'Tamburas': 'Tambura',
    'Tan.': 'Tan.',
    'Tanpura': 'Tanpura',
    'Tanpura (Female)': 'Tanpura (Nữ)',
    'Tanpura (Male)': 'Tanpura (Nam)',
    'Tanpuras': 'Tanpura',
    'Tenor Viol': 'Tenor Viol',
    'Tenor Viola da Gamba': 'Tenor Viola da Gamba',
    'Tenor Violas da Gamba': 'Tenor Viola da Gamba',
    'Tenor Viols': 'Tenor Viol',
    'Tr. Viol': 'Tr. Viol',
    'Tr. Viols': 'Tr. Viol',
    'Tr. Vla da G.': 'Tr. Vla da G.',
    'Tr. Vlas da G.': 'Tr. Vla da G.',
    'Treble Viol': 'Treble Viol',
    'Treble Viola da Gamba': 'Treble Viola da Gamba',
    'Treble Violas da Gamba': 'Treble Viola da Gamba',
    'Treble Viols': 'Treble Viol',
    'Upright Bass': 'Upright Bass',
    'Upright Basses': 'Upright Bass',
    'Vc.': 'Vc.',
    'Viola': 'Viola',
    'Violas': 'Viola',
    'Violin': 'Violin',
    'Violins': 'Violin',
    'Violoncello': 'Violoncello',
    'Violoncellos': 'Violoncello',
    'Vlas': 'Vlas',
    'Vln': 'Vln',
    'Vlns': 'Vln',
    'Zith.': 'Zith.',
    'Zither': 'Zither',
    'Zithers': 'Zither',
}

# ---------------------------------------------------------------- self-checks
real = {k: v for k, v in WORDING.items() if k in en}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN instrumentnames_en.xml ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

mapping, pending, clashes, _ = load_batches()
if clashes:
    sys.exit('!! conflicting translations; fix them before writing')
after = dict(mapping)
after.update(real)

# The shared checker, the same one rounds 2-5 and `score_instruments.py check`
# use.  Round 1 originally carried its own copy of rules 1-3 and its own
# singular/plural test, and the copy was stricter than the real rule: it flagged
# `Vlas` -> `Vlas` against `Vla` -> `Vla`, which is two identity mappings and not
# a disagreement.  Two copies of one rule is how they drift apart.
problems = score.check_consistency(after, en)

by = {}
for value, users in score.source_strings(entities).items():
    if family_of(users[0]) in FAMILY:
        by.setdefault(family_of(users[0]), []).append(value)
for stem in FAMILY:
    left = [v for v in by.get(stem, []) if not after.get(v)]
    if left:
        problems.append(f'{stem}: {len(left)} string(s) still blank, e.g. '
                        + ', '.join(repr(v) for v in left[:6]))

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if mapping.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'newly written    : {len(changed)}')
print(f'already the same : {len(real) - len(changed)}')
for stem in FAMILY:
    rows = [v for v in by.get(stem, [])]
    done = sum(1 for v in rows if after.get(v))
    print(f'  {stem:6} {done:>3}/{len(rows):<3} strings')
print()

if not WRITE:
    print('(dry run - pass --write)')
    sys.exit(0)

n = 0
for stem in FAMILY:
    path = os.path.join(BATCH_DIR, f'{stem}.json')
    with open(path, encoding='utf-8') as fh:
        rows = json.load(fh)
    for k, v in real.items():
        if k in rows and rows[k] != v:
            rows[k] = v
            n += 1
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write('\n')
print(f'applied {n} value(s) to {BATCH_DIR}')
