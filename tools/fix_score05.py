#!/usr/bin/env python3
"""Score Editor round 5: unpitched percussion, the last 137 strings.

This finishes the catalogue.  It is the family the seeds covered best - 98 of
its 235 strings were already settled by the main UI table - so the work here is
almost entirely the 137 the seeds could not reach, and the seeds are the brief.

  1. A bracketed register is translated, capitalised, and keeps its bracket.

     That is the pattern the seeds wrote 40 times over: `Bongo (High)` ->
     `Bongo (Cao)`, `Tenor Drum (Medium-high)` -> `Trống Tenor (Trung bình
     cao)`, `Temple Block (Low)` -> `Mõ gỗ (Trầm)`, `Conga (Super Tumba)` ->
     `Conga (Super Tumba)`.  So `Agogô (High)` -> `Agogô (Cao)` and
     `Cuíca (Low)` -> `Cuíca (Trầm)`, while `(Quinto)`, `(Requinto)`,
     `(Super Tumba)` and `(pedal)` keep their words, because those are the
     name of the variant rather than a register.

  2. The same register written out in front of the name moves to the end,
     as every seeded adjective already did: `Large Gong` -> `Cồng lớn`,
     `Small Gong` -> `Cồng nhỏ`, `Wind Gong` -> `Cồng gió`, `Opera Gong` ->
     `Cồng Opera`.  So `High Agogô` -> `Agogô cao` and `Low Agogôs` ->
     `Agogô thấp`.

  3. A name the seeds already gave a Vietnamese head noun takes it again.

     `Bell Tree` and `Sleigh Bells` became `Bell Tree` and `Chuông xe trượt
     tuyết`; `Side Drum` became `Trống phụ`; `Triangle` became `Tam giác`;
     `Whip` became `Roi da Whip`.  So `Bell Trees` -> `Bell Tree`,
     `Sleigh Bell` -> `Chuông xe trượt tuyết`, `Side Drums` -> `Trống phụ`,
     `Triangles` -> `Tam giác`, `Whips` -> `Roi da Whip`, `Whistles` -> `Còi`.

  4. 74 of these 137 are abbreviations and short labels, and every one keeps
     its spelling: `B. Dr.`, `Si. Dr.`, `Sl. Bells`, `Sz. Cym.`, `Vibs.`,
     `R-tom`.  Same as rounds 1, 3 and 4.

Two of the 137 carry a comma inside the name and it is kept:
`Marching Snare Drum, rim only (1 line)` -> `Trống Snare diễu hành, chỉ vành
(1 dòng)`.

One inherited value is deliberately left alone.  `Clash Cymbals` is already
`Clash Cymbals` because that is what the main UI table says, and a seed is not
overruled here.  `check_consistency` exempts an identity plural for the same
reason: an inherited English plural is not this round's disagreement to fix.

  python tools/fix_score05.py
  python tools/fix_score05.py --write
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
FAMILY = ('percun',)

_, entities = score.read(SOURCE)
en = set(score.source_strings(entities))

WORDING = {
    # ---- rule 1: bracketed register, brackets kept
    'Agogô (High)': 'Agogô (Cao)',
    'Agogô (Low)': 'Agogô (Trầm)',
    'Cuíca (High)': 'Cuíca (Cao)',
    'Cuíca (Low)': 'Cuíca (Trầm)',

    # ---- rule 2: register in front of the name moves to the end
    'High Agogô': 'Agogô cao',
    'High Agogôs': 'Agogô cao',
    'Low Agogô': 'Agogô thấp',
    'Low Agogôs': 'Agogô thấp',

    # ---- rule 3: the head noun the seeds already chose, plus its plural
    'Bass Drums': 'Trống Bass',
    'Bell Trees': 'Bell Tree',
    'Bongo Bell': 'Chuông Bongo',
    'Bongo Bells': 'Chuông Bongo',
    'Cha-cha': 'Cha-cha',
    'Cha-cha Bells': 'Chuông Cha-cha',
    'Floor tom': 'Floor Tom',
    'Floor toms': 'Floor Tom',
    'Large Gongs': 'Cồng lớn',
    'Marching Bass Drum': 'Trống Bass diễu hành',
    'Marching Snare Drum': 'Trống Snare diễu hành',
    'Marching Snare Drum, Kevlar head (1 line)':
        'Trống Snare diễu hành, mặt Kevlar (1 dòng)',
    'Marching Snare Drum, rim only (1 line)':
        'Trống Snare diễu hành, chỉ vành (1 dòng)',
    'Marching Snare Drums': 'Trống Snare diễu hành',
    'Opera Gongs': 'Cồng Opera',
    'Percussion (1 line kit)': 'Percussion (bộ 1 dòng)',
    'Ribbon Crashers': 'Ribbon Crasher',
    'Side Drums': 'Trống phụ',
    'Sleigh Bell': 'Chuông xe trượt tuyết',
    'Small Gongs': 'Cồng nhỏ',
    'Snare Drums': 'Trống Snare',
    'Tenor Drum': 'Trống Tenor',
    'Tenor Drums': 'Trống Tenor',
    'Triangles': 'Tam giác',
    'Whips': 'Roi da Whip',
    'Whistles': 'Còi',
    'Wind Gongs': 'Cồng gió',

    # ---- a name stays a name, and its plural takes the singular's wording
    'Alfaias': 'Alfaia',
    'Bongo': 'Bongo',
    'Bongos': 'Bongo',
    'Cabasas': 'Cabasa',
    'Caxixis': 'Caxixi',
    'China Cymbals': 'China Cymbal',
    'Clash Cymbal': 'Clash Cymbal',
    'Congas': 'Conga',
    'Crash Cymbal': 'Crash Cymbal',
    'Crash Cymbals': 'Crash Cymbal',
    'Djembes': 'Djembe',
    'Flexatones': 'Flexatone',
    'Gourds': 'Gourd',
    'Guiros': 'Guiro',
    'H-hat': 'Hi-hat',
    'H-hats': 'Hi-hat',
    'Hi-hats': 'Hi-hat',
    'Jawbones': 'Jawbone',
    'Kayambas': 'Kayamba',
    'Kick Drum': 'Kick Drum',
    'Kick Drums': 'Kick Drum',
    'Maraca': 'Maraca',
    'Maracas': 'Maraca',
    'Pandeiros': 'Pandeiro',
    'R-tom': 'R-tom',
    'R-toms': 'R-tom',
    'Rainsticks': 'Rainstick',
    'Ratchets': 'Ratchet',
    'Ride Cymbal': 'Ride Cymbal',
    'Ride Cymbals': 'Ride Cymbal',
    'Roto-tom': 'Roto-tom',
    'Roto-toms': 'Roto-tom',
    'Shekeres': 'Shekere',
    'Sizzle Cymbals': 'Sizzle Cymbal',
    'Sogos': 'Sogo',
    'Splash Cymbals': 'Splash Cymbal',
    'Surdos': 'Surdo',
    'Suspended Cymbals': 'Suspended Cymbal',
    'Tam-tams': 'Tam-tam',
    'Temple Block': 'Mõ gỗ',
    'Temple Blocks': 'Mõ gỗ',
    'Thundersheets': 'Thundersheet',
    'Timbale': 'Timbale',
    'Timbales': 'Timbale',
    'Tom': 'Tom',
    'Tom-tom': 'Tom-tom',
    'Tom-toms': 'Tom-tom',
    'Toms': 'Tom',
    'Udus': 'Udu',
    'Vibraslaps': 'Vibraslap',

    # ---- rule 4: abbreviations and short labels, verbatim
    'Anv.': 'Anv.',
    'B. Dr.': 'B. Dr.',
    'B. Tr.': 'B. Tr.',
    'Bon.': 'Bon.',
    'Bon. Bell': 'Bon. Bell',
    'Bon. Bells': 'Bon. Bell',
    'Cab.': 'Cab.',
    'Cast.': 'Cast.',
    'Cax.': 'Cax.',
    'Ch. Cym.': 'Ch. Cym.',
    'Cl. Cym.': 'Cl. Cym.',
    'Clv.': 'Clv.',
    'Con.': 'Con.',
    'Cr. Cym.': 'Cr. Cym.',
    'Djem.': 'Djem.',
    'Fl. Tom.': 'Fl. Tom.',
    'Flex.': 'Flex.',
    'Gou.': 'Gou.',
    'Gui.': 'Gui.',
    'H. Ag.': 'H. Ag.',
    'Jaw.': 'Jaw.',
    'K. Dr.': 'K. Dr.',
    'Kay.': 'Kay.',
    'L. Ag.': 'L. Ag.',
    'L. G.': 'L. G.',
    'Mara.': 'Mara.',
    'O. G.': 'O. G.',
    'Pan.': 'Pan.',
    'R. Cr.': 'R. Cr.',
    'R. Cym.': 'R. Cym.',
    'Rain.': 'Rain.',
    'Rat.': 'Rat.',
    'S. G.': 'S. G.',
    'Shek.': 'Shek.',
    'Si. Dr.': 'Si. Dr.',
    'Sl. Bells': 'Sl. Bells',
    'Sn. Dr.': 'Sn. Dr.',
    'Sog.': 'Sog.',
    'Sp. Cym.': 'Sp. Cym.',
    'Sur.': 'Sur.',
    'Sus. Cym.': 'Sus. Cym.',
    'Sz. Cym.': 'Sz. Cym.',
    'T. Bl.': 'T. Bl.',
    'Tam.': 'Tam.',
    'Th.': 'Th.',
    'Timb.': 'Timb.',
    'Tom.': 'Tom.',
    'Tri.': 'Tri.',
    'Vib.': 'Vib.',
    'Vibs.': 'Vibs.',
    'W. G.': 'W. G.',
    'Wh.': 'Wh.',
    'Whist.': 'Whist.',
}

# ---------------------------------------------------------------- self-checks
real = {k: v for k, v in WORDING.items() if k in en}
absent = sorted(set(WORDING) - set(real))
if absent:
    print(f'NOT IN instrumentnames_en.xml ({len(absent)}):')
    for m in absent:
        print(f'  {m!r}')
    print()

mapping, pending, clashes, _ = load_batches()
if clashes:
    sys.exit('!! conflicting translations; fix them before writing')
after = dict(mapping)
after.update(real)

problems = score.check_consistency(after, en)
for stem in FAMILY:
    rows = [v for v, u in score.source_strings(entities).items()
            if family_of(u[0]) == stem]
    left = [v for v in rows if not after.get(v)]
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
    rows = [v for v, u in score.source_strings(entities).items()
            if family_of(u[0]) == stem]
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
