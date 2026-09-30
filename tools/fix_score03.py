#!/usr/bin/env python3
"""Score Editor round 3: the fretted strings, 173 strings.

The frets family is where the naming rule has to be sharpest, because the
names are a mix of loanwords and English descriptors and the two have to be
told apart.  The rule was not guessed.  `instrumentnames_ja.xml` and
`instrumentnames_de.xml` both had to answer exactly this question, and they
agree on every string in this family:

    English                       Japanese                     German
    Acoustic Guitar                アコースティックギター        Akustische Gitarre
    Electric Guitar                エレキギター                  Elektrische Gitarre
    Fretless Bass                  フレットレスベース            Fretless-Bass
    Banjo                          バンジョー                    Banjo
    Charango                       チャランゴ                    Charango
    Cuatro                         クアトロ                      Cuatro
    Ac. B. Gtr                     Ac. B. Gtr                  Ak. B.-Git.
    A. Bal.                        A. Bal.                     Alt-Bal.
    Dul.                           Dul.                        Dul.

Three rules, and every one of them is visible in that table.

  1. A descriptor is the language's; a name is a loanword.

     `Acoustic`, `Electric`, `Fretless`, `Classical`, `Jazz`,
     `Steel-string`, `Semi-acoustic`, `Resonator` and the country names are
     all translated by Japanese and by German, so they are translated here:
     `Electric Guitar` -> `Guitar điện`, `Classical Guitar` ->
     `Guitar cổ điển`, `Resonator Guitar` -> `Guitar cộng hưởng`.
     `Banjo`, `Charango`, `Cuatro`, `Bandurria`, `Cavaquinho`, `Theorbo`
     stay as themselves in all three languages, so they stay here too.

  2. A descriptor that is already a music loanword stays in place.

     `Alto Balalaika`, `Bass Balalaika`, `Contrabass Balalaika`,
     `Prima Balalaika`, `Secunda Balalaika`, `Piccolo Domra`, `Tenor Lute`,
     `Tenor Banjo` - German writes `Alt-Balalaika` and `Kontrabass-Balalaika`
     with the register still in front, Japanese writes アルト + バラライカ
     the same way.  Neither moves it, so neither does this: those strings are
     identity, and saying so is the decision.

  3. Abbreviations are never touched, but their plurals collapse.

     Japanese leaves `Ac. B. Gtr` and `Ban.` byte-identical, and so does
     German for `Ban.`, `Bando.`, `Dul.`.  Round 1's rule 4 applies.  The
     plural abbreviation is the one exception: `Ac. B. Gtrs` -> `Ac. B. Gtr`,
     because Vietnamese has no plural to mark and a short part label that
     still ended in a lowercase `s` would be English leaking through.  This
     is the same collapse round 1 and round 2 applied to `Pianos` and
     `Doumbeks`; the Japanese catalogue does not collapse `Ac. B. Gtrs`, but
     Japanese had no reason to and Vietnamese does.

`Fretless` is the one word with no settled Vietnamese: `Bass không phím bấm`
("bass with no fretting keys").  `Semi-acoustic` is left as
`Guitar semi-acoustic` rather than invented into Vietnamese, and `Lap Steel`
is treated as a name (`Guitar Lap Steel Hawaii 10 dây`) because that is what
it is - the name of the instrument, not a description of it.

  python tools/fix_score03.py
  python tools/fix_score03.py --write
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from cubelib import score                                      # noqa: E402
from score_instruments import family_of, load_batches          # noqa: E402

BATCH_DIR = os.path.join(ROOT, 'translations', 'score', 'instruments')
SOURCE = os.path.join(r'E:\Steinberg\Cubase 15', 'Components', 'ScoringEngine',
                      'l10n', 'instrumentnames_en.xml')
WRITE = '--write' in sys.argv
FAMILY = ('frets',)

_, entities = score.read(SOURCE)
en = set(score.source_strings(entities))

WORDING = {
    # ---- rule 1: descriptors translated
    '10-course Renaissance Lute (Tenor)': 'Lute Renaissance 10 dây (Tenor)',
    '10-string Hawaiian Lap Steel Guitar': 'Guitar Lap Steel Hawaii 10 dây',
    '11-course Baroque Lute': 'Lute Baroque 11 dây',
    '12-course Baroque Lute': 'Lute Baroque 12 dây',
    '12-string Acoustic Guitar': 'Guitar acoustic 12 dây',
    '12-string Electric Guitar': 'Guitar điện 12 dây',
    '13-course Baroque Lute': 'Lute Baroque 13 dây',
    '14-course Baroque Theorbo': 'Theorbo Baroque 14 dây',
    '4-string Acoustic Bass': 'Bass acoustic 4 dây',
    '4-string Acoustic Bass Guitar': 'Guitar bass acoustic 4 dây',
    '4-string Bass': 'Bass 4 dây',
    '4-string Bass Guitar': 'Guitar bass 4 dây',
    '5-string Acoustic Bass': 'Bass acoustic 5 dây',
    '5-string Acoustic Bass Guitar': 'Guitar bass acoustic 5 dây',
    '5-string Bass': 'Bass 5 dây',
    '5-string Bass Guitar': 'Guitar bass 5 dây',
    '6-course Renaissance Lute (Tenor)': 'Lute Renaissance 6 dây (Tenor)',
    '6-string Bass': 'Bass 6 dây',
    '6-string Bass Guitar': 'Guitar bass 6 dây',
    '6-string Hawaiian Lap Steel Guitar': 'Guitar Lap Steel Hawaii 6 dây',
    '7-course Renaissance Lute (Tenor)': 'Lute Renaissance 7 dây (Tenor)',
    '7-string Electric Guitar': 'Guitar điện 7 dây',
    '8-course Renaissance Lute (Tenor)': 'Lute Renaissance 8 dây (Tenor)',
    '8-string Hawaiian Lap Steel Guitar': 'Guitar Lap Steel Hawaii 8 dây',
    'Acoustic Bass': 'Bass acoustic',
    'Acoustic Bass Guitar': 'Guitar bass acoustic',
    'Acoustic Bass Guitars': 'Guitar bass acoustic',
    'Acoustic Basses': 'Bass acoustic',
    'Acoustic Guitar': 'Guitar acoustic',
    'Acoustic Guitars': 'Guitar acoustic',
    'Classical Guitar': 'Guitar cổ điển',
    'Colombian Tiple': 'Tiple Colombia',
    'Electric Guitar': 'Guitar điện',
    'Electric Guitars': 'Guitar điện',
    'Fretless 4-string Bass': 'Bass không phím bấm 4 dây',
    'Fretless 4-string Bass Guitar': 'Guitar bass không phím bấm 4 dây',
    'Fretless 5-string Bass': 'Bass không phím bấm 5 dây',
    'Fretless 5-string Bass Guitar': 'Guitar bass không phím bấm 5 dây',
    'Fretless 6-string Bass': 'Bass không phím bấm 6 dây',
    'Fretless 6-string Bass Guitar': 'Guitar bass không phím bấm 6 dây',
    'Fretless Bass': 'Bass không phím bấm',
    'Fretless Bass Guitar': 'Guitar bass không phím bấm',
    'Fretless Bass Guitars': 'Guitar bass không phím bấm',
    'Fretless Basses': 'Bass không phím bấm',
    'Hawaiian Steel Guitar': 'Guitar thép Hawaii',
    'Hawaiian Steel Guitars': 'Guitar thép Hawaii',
    'Jazz Guitar': 'Guitar jazz',
    'Jazz Guitars': 'Guitar jazz',
    'Mexican Vihuela': 'Vihuela Mexico',
    'Pedal Steel Guitar': 'Guitar pedal',
    'Pedal Steel Guitar (Two Necks)': 'Guitar pedal (hai cần)',
    'Pedal Steel Guitars': 'Guitar pedal',
    'Portuguese Guitar': 'Guitar Bồ Đào Nha',
    'Portuguese Guitarra': 'Guitarra Bồ Đào Nha',
    'Portuguese Guitars': 'Guitar Bồ Đào Nha',
    'Resonator Guitar': 'Guitar cộng hưởng',
    'Semi-acoustic 4-string Bass': 'Bass semi-acoustic 4 dây',
    'Semi-acoustic 4-string Bass Guitar': 'Guitar bass semi-acoustic 4 dây',
    'Semi-acoustic Bass': 'Bass semi-acoustic',
    'Semi-acoustic Bass Guitar': 'Guitar bass semi-acoustic',
    'Semi-acoustic Bass Guitars': 'Guitar bass semi-acoustic',
    'Semi-acoustic Basses': 'Bass semi-acoustic',
    'Semi-acoustic Guitar': 'Guitar semi-acoustic',
    'Semi-acoustic Guitars': 'Guitar semi-acoustic',
    'Steel-string Acoustic Guitar': 'Guitar acoustic dây thép',

    # ---- rule 2: a loanword register stays where it is
    'Alto Balalaika': 'Alto Balalaika',
    'Alto Balalaikas': 'Alto Balalaika',
    'Alto Domra': 'Alto Domra',
    'Basso Domra': 'Basso Domra',
    'Bass Balalaika': 'Bass Balalaika',
    'Bass Balalaikas': 'Bass Balalaika',
    'Bass Guitar': 'Guitar bass',
    'Bass Guitars': 'Guitar bass',
    'Contrabass Balalaika': 'Contrabass Balalaika',
    'Contrabass Balalaikas': 'Contrabass Balalaika',
    'Minor Domra': 'Minor Domra',
    'Piccolo Domra': 'Piccolo Domra',
    'Prima Balalaika': 'Prima Balalaika',
    'Prima Balalaikas': 'Prima Balalaika',
    'Secunda Balalaika': 'Secunda Balalaika',
    'Secunda Balalaikas': 'Secunda Balalaika',
    'Tenor Banjo': 'Tenor Banjo',
    'Tenor Banjos': 'Tenor Banjo',
    'Tenor Lute': 'Tenor Lute',
    'Tenor Lutes': 'Tenor Lute',

    # ---- names, unchanged, plurals collapsed
    'Bandola': 'Bandola',
    'Bandolas': 'Bandola',
    'Bandurria': 'Bandurria',
    'Bandurrias': 'Bandurria',
    'Banjo': 'Banjo',
    'Banjos': 'Banjo',
    'Bordonúa': 'Bordonúa',
    'Bordonúas': 'Bordonúa',
    'Cavaquinho': 'Cavaquinho',
    'Cavaquinhos': 'Cavaquinho',
    'Charango': 'Charango',
    'Charangos': 'Charango',
    'Cuatro': 'Cuatro',
    'Cuatros': 'Cuatro',
    'Cuatro, Puerto Rico': 'Cuatro, Puerto Rico',
    'Cuatro, Venezuela': 'Cuatro, Venezuela',
    'Dulcimer': 'Dulcimer',
    'Dulcimers': 'Dulcimer',
    'Guitarra': 'Guitarra',
    'Guitarras': 'Guitarra',
    'Guitars': 'Guitar',
    'Lute': 'Lute',
    'Lutes': 'Lute',
    'Mandolin': 'Mandolin',
    'Mandolins': 'Mandolin',
    'Requinto': 'Requinto',
    'Requintos': 'Requinto',
    'Theorbo': 'Theorbo',
    'Tiple': 'Tiple',
    'Tiples': 'Tiple',
    'Ukulele': 'Ukulele',
    'Ukuleles': 'Ukulele',
    'Vihuela': 'Vihuela',
    'Vihuelas': 'Vihuela',

    # ---- rule 3: abbreviations verbatim, their plurals collapsed
    'A. Bal.': 'A. Bal.',
    'A. Dom.': 'A. Dom.',
    'Ac. B. Gtr': 'Ac. B. Gtr',
    'Ac. B. Gtrs': 'Ac. B. Gtr',
    'Ac. Bass': 'Ac. Bass',
    'Ac. Basses': 'Ac. Bass',
    'Ac. Gtr': 'Ac. Gtr',
    'Ac. Gtrs': 'Ac. Gtr',
    'B. Bal.': 'B. Bal.',
    'B. Dom.': 'B. Dom.',
    'B. Gtr': 'B. Gtr',
    'B. Gtrs': 'B. Gtr',
    'Ban.': 'Ban.',
    'Bando.': 'Bando.',
    'Bandu.': 'Bandu.',
    'Bordo.': 'Bordo.',
    'Cav.': 'Cav.',
    'Cb. Bal.': 'Cb. Bal.',
    'Char.': 'Char.',
    'Cuat.': 'Cuat.',
    'Dul.': 'Dul.',
    'E. Gtr': 'E. Gtr',
    'E. Gtrs': 'E. Gtr',
    'Gtr': 'Gtr',
    'Gtrs': 'Gtr',
    'Guit.': 'Guit.',
    'H. St. Gtr': 'H. St. Gtr',
    'H. St. Gtrs': 'H. St. Gtr',
    'M. Dom.': 'M. Dom.',
    'Mand.': 'Mand.',
    'P. Dom.': 'P. Dom.',
    'P. Gtr': 'P. Gtr',
    'P. Gtrs': 'P. Gtr',
    'P. St. Gtr': 'P. St. Gtr',
    'P. St. Gtrs': 'P. St. Gtr',
    'Pr. Bal.': 'Pr. Bal.',
    'Req.': 'Req.',
    'S-ac. B. Gtr': 'S-ac. B. Gtr',
    'S-ac. B. Gtrs': 'S-ac. B. Gtr',
    'S-ac. Bass': 'S-ac. Bass',
    'S-ac. Basses': 'S-ac. Bass',
    'S-ac. Gtr': 'S-ac. Gtr',
    'S-ac. Gtrs': 'S-ac. Gtr',
    'Se. Bal.': 'Se. Bal.',
    'T. Ban.': 'T. Ban.',
    'T. Lute': 'T. Lute',
    'T. Lutes': 'T. Lute',
    'Theo.': 'Theo.',
    'Tip.': 'Tip.',
    'Tres': 'Tres',
    'Uku.': 'Uku.',
    'Vih.': 'Vih.',
    'Vla': 'Vla',
}

# ---------------------------------------------------------------- self-checks
real = {k: v for k, v in WORDING.items() if k in en}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN instrumentnames_en.xml ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

problems = []
for k, v in real.items():
    if v == k:
        continue
    try:
        score.check_text(v, k)
    except score.ScoreError as exc:
        problems.append(str(exc))

mapping, pending, clashes, _ = load_batches()
after = dict(mapping)
after.update(real)
by = {}
for value, users in score.source_strings(entities).items():
    if family_of(users[0]) in FAMILY:
        by.setdefault(family_of(users[0]), []).append(value)
for stem in FAMILY:
    left = [v for v in by.get(stem, []) if not after.get(v)]
    if left:
        problems.append(f'{stem}: {len(left)} string(s) still blank, e.g. '
                        + ', '.join(repr(v) for v in left[:6]))

# A plural takes its singular's wording, unless the singular key is absent.
for k, v in real.items():
    sing = k[:-1] if k.endswith('s') else None
    if sing and sing in after and after[sing] != v:
        problems.append(f'plural differs from its singular: {k!r} -> {v!r} '
                        f'but {sing!r} -> {after[sing]!r}')

# A collapsed plural must land on a string the file actually contains.
# `Ac. Basses` -> `Ac. Bass` is legal because `Ac. Bass` is a key in its own
# right; a value that is merely the key with a letter lopped off, landing on
# nothing, is a mangling.  This catches abbreviations and names alike without
# having to guess which keys are abbreviations: `Acoustic Guitars` ->
# `Guitar acoustic` and `Jazz Guitar` -> `Guitar jazz` are not prefixes of
# their keys, so they are never examined.
for k, v in real.items():
    if v == k or not k.startswith(v):
        continue
    tail = k[len(v):]
    if tail in ('s', 'es', 'n') and v not in after:
        problems.append(f'plural collapsed onto a string that is not in the '
                        f'file: {k!r} -> {v!r}')

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
    rows = by.get(stem, [])
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
