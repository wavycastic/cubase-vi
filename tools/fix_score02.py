#!/usr/bin/env python3
"""Score Editor round 2: the two percussion families, 190 strings.

Round 1 covered voices, the band, keyboards and strings.  This takes `perc`
(pitched percussion) and `other` (the catch-all: gamelan, drum kits, world
instruments, the staff names), which are the two families the main UI table
had the least to say about - `import` seeded nothing in `perc` at all.

The rules are round 1's, applied.  Two of them needed settling first, and
both were settled by reading the main table rather than by taste.

  1. Section names are translated only where Vietnamese has a real word.

     The main table gives `Brass` -> `Bộ đồng`, `Wind` -> `Gió`,
     `Keyboard` -> `Bàn phím`, `Voice` -> `Bè`, but leaves `Percussion` ->
     `Percussion`, `Drum` -> `Drum`, `Snare` -> `Snare`, `Tambourine` ->
     `Tambourine`.  That is not an inconsistency, it is the same rule: name it
     when Vietnamese has a name, keep the English when it does not.  So
     `Woodwind` -> `Bộ gió` and `Strings` -> `Bộ dây` (round 1) follow
     `Brass`, while `Drum Set` -> `Drum Set` follows `Drum`, and
     `Percussion` stays as round 1's seed already had it.

  2. `Staff` is `khuông nhạc`, per AGENT.md.

     `Grand staff` -> `Khuông nhạc lớn`, `Bass staff` -> `Khuông nhạc Bass`,
     `Treble staff` -> `Khuông nhạc Sol`.  The treble one is named after its
     clef, `khóa nhạc` in AGENT.md's table, so `Sol` is the reading; saying
     "khuông nhạc khóa Sol" would be a staff that has a clef, which is not
     what a staff is.

  3. `Bell` and `Cymbal` are head nouns and do get translated - the seeds
     already show `Bongo Bell` -> `Chuông Bongo`, `Sleigh Bells` ->
     `Chuông xe trượt tuyết`, `Marching Cymbals` -> `Chũm chọe diễu hành`.
     So `Tubular Bells` -> `Chuông ống`, `Alpine Bells` -> `Chuông Alpine`,
     `Antique Cymbals` -> `Chũm chọe cổ`.  Where the word is the modifier
     instead, only the modifier moves: `Bell Lyre` -> `Lyre có chuông`.

  4. Jargon with no settled Vietnamese stays English, as `Snare` and
     `Doumbeks` already do.  So `(1 spock)` and `(2 spocks)` are kept - a
     marching drum stick is not a "que", and inventing a word for it would be
     the kind of neat solution AGENT.md rule 8 warns against.

  5. `O. M. ` has a trailing space in the source.  It maps to itself, which
     `cubelib.score.build` allows without the whitespace check precisely
     because an identity mapping introduces nothing.

  python tools/fix_score02.py
  python tools/fix_score02.py --write
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
FAMILY = ('perc', 'other')

_, entities = score.read(SOURCE)
en = set(score.source_strings(entities))

WORDING = {
    # ---- perc: abbreviations, then the instruments themselves
    'A. Glock.': 'A. Glock.',
    'A. Met.': 'A. Met.',
    'A. Xyl.': 'A. Xyl.',
    'Alm.': 'Alm.',
    'Almglocken': 'Almglocken',
    'Alp. Bells': 'Alp. Bells',
    'Alpine Bells': 'Chuông Alpine',
    'Alto Glockenspiel': 'Alto Glockenspiel',
    'Alto Glockenspiels': 'Alto Glockenspiel',
    'Alto Metallophone': 'Alto Metallophone',
    'Alto Metallophones': 'Alto Metallophone',
    'Alto Xylophone': 'Alto Xylophone',
    'Alu.': 'Alu.',
    'Aluphone': 'Aluphone',
    'Aluphones': 'Aluphone',
    'Ant. Cym.': 'Ant. Cym.',
    'Antique Cymbals': 'Chũm chọe cổ',
    'B. Met.': 'B. Met.',
    'B. Xyl.': 'B. Xyl.',
    'Bass Metallophone': 'Bass Metallophone',
    'Bass Metallophones': 'Bass Metallophone',
    'Bass Xylophone': 'Bass Xylophone',
    'Bass Xylophones': 'Bass Xylophone',
    'Bell L.': 'Bell L.',
    'Bell Lyre': 'Lyre có chuông',
    'Bell Lyres': 'Lyre có chuông',
    'C-bell': 'C-bell',
    'C-bells': 'C-bell',
    'Chim.': 'Chim.',
    'Chimes': 'Chimes',
    'Cim.': 'Cim.',
    'Cimbalom': 'Cimbalom',
    'Cimbaloms': 'Cimbalom',
    'Cowbell': 'Cowbell',
    'Cowbells': 'Cowbell',
    'Crot.': 'Crot.',
    'Crotales': 'Crotales',
    'G. Harm.': 'G. Harm.',
    'Glass Harmonica': 'Glass Harmonica',
    'Glass Harmonicas': 'Glass Harmonica',
    'Glock.': 'Glock.',
    'Glockenspiel': 'Glockenspiel',
    'Glockenspiels': 'Glockenspiel',
    'H-bells': 'H-bells',
    'H. Dul.': 'H. Dul.',
    'Hammered Dulcimer': 'Dulcimer gõ bằng que',
    'Hammered Dulcimers': 'Dulcimer gõ bằng que',
    'Handbells': 'Handbell',
    'Harp': 'Harp',
    'Harps': 'Harp',
    'Hp': 'Hp',
    'Hps': 'Hp',
    'Ken.': 'Ken.',
    'Kenong': 'Kenong',
    'Kenongs': 'Kenong',
    'Mar.': 'Mar.',
    'Marimba': 'Marimba',
    'Marimbas': 'Marimba',
    'S. Glock.': 'S. Glock.',
    'S. Met.': 'S. Met.',
    'S. Xyl.': 'S. Xyl.',
    'San.': 'San.',
    'Santoor': 'Santoor',
    'Santoors': 'Santoor',
    'Slen.': 'Slen.',
    'Slenthem': 'Slenthem',
    'Slenthems': 'Slenthem',
    'Soprano Glockenspiel': 'Soprano Glockenspiel',
    'Soprano Glockenspiels': 'Soprano Glockenspiel',
    'Soprano Metallophone': 'Soprano Metallophone',
    'Soprano Metallophones': 'Soprano Metallophone',
    'Soprano Xylophone': 'Soprano Xylophone',
    'St. Dr.': 'St. Dr.',
    'St. P.': 'St. P.',
    'Steel Drum': 'Steel Drum',
    'Steel Drums': 'Steel Drum',
    'Steel Pan': 'Steel Pan',
    'Steel Pans': 'Steel Pan',
    'T. Gongs': 'T. Gongs',
    'Timp.': 'Timp.',
    'Timpani': 'Timpani',
    'Tub. Bells': 'Tub. Bells',
    'Tubular Bells': 'Chuông ống',
    'Tuned Cowbells': 'Cowbell tinh chỉnh',
    'Tuned Gongs': 'Cồng tinh chỉnh',
    'Vibraphone': 'Vibraphone',
    'Vibraphones': 'Vibraphone',
    'Xyl.': 'Xyl.',
    'Xylophone': 'Xylophone',
    'Xylophones': 'Xylophone',
    'Xylor.': 'Xylor.',
    'Xylorimba': 'Xylorimba',
    'Xylorimbas': 'Xylorimba',

    # ---- other
    'Ag.': 'Ag.',
    'Agogôs': 'Agogô',
    'B. D.': 'B. D.',
    'Bass staff': 'Khuông nhạc Bass',
    'Box': 'Hộp gõ',
    'Boxes': 'Hộp gõ',
    'Br. Dr.': 'Br. Dr.',
    'Brake Drums': 'Brake Drum',
    'Caj.': 'Caj.',
    'Cajon': 'Cajon',
    'Cajons': 'Cajon',
    'Cuí.': 'Cuí.',
    'Cuíca': 'Cuíca',
    'Cuícas': 'Cuíca',
    'Cym.': 'Cym.',
    'Dou.': 'Dou.',
    'Doumbeks': 'Doumbek',
    'Dr.': 'Dr.',
    'Drum Set': 'Drum Set',
    'Drum Set (Basic)': 'Drum Set (Cơ bản)',
    'Drum Set (Full)': 'Drum Set (Đầy đủ)',
    'Drum Sets': 'Drum Set',
    'F. Cym.': 'F. Cym.',
    'F. S.': 'F. S.',
    'Finger Cymbal': 'Finger Cymbal',
    'Finger Snap': 'Finger Snap',
    'Fl. toms': 'Floor Tom',
    'G. A.': 'G. A.',
    'Gong Agengs': 'Gong Ageng',
    'Gr.': 'Gr.',
    'Grand staff': 'Khuông nhạc lớn',
    'H. C.': 'H. C.',
    'H. Dr.': 'H. Dr.',
    'Hand Clap': 'Vỗ tay',
    'Hand Drums': 'Trống tay',
    'J. Bl.': 'J. Bl.',
    'Jam Block': 'Jam Block',
    'Jam Blocks': 'Jam Block',
    'K. A.': 'K. A.',
    'K. K.': 'K. K.',
    'Kemp.': 'Kemp.',
    'Kempyang and Ketuk': 'Kempyang và Ketuk',
    'Kempyangs': 'Kempyang',
    'Kempyangs and Ketuks': 'Kempyang và Ketuk',
    'Kendhang Agengs': 'Kendhang Ageng',
    'Ket.': 'Ket.',
    'Ketuks': 'Ketuk',
    'M. T.': 'M. T.',
    'Marching Bass Drums': 'Trống Bass diễu hành',
    'Marching Cymbal': 'Chũm chọe diễu hành',
    'Marching Cymbals': 'Chũm chọe diễu hành',
    'Marching Tenor Drums (1 spock)': 'Trống Tenor diễu hành (1 spock)',
    'Marching Tenor Drums (2 spocks)': 'Trống Tenor diễu hành (2 spocks)',
    'Mark Trees': 'Mark Tree',
    'O. M.': 'O. M.',
    'O. M. ': 'O. M. ',
    'Ondes Martenot': 'Ondes Martenot',
    'Ondes Martenots': 'Ondes Martenot',
    'Pat.': 'Pat.',
    'Perc.': 'Perc.',
    'S. Bass': 'S. Bass',
    'S. Basses': 'S. Bass',
    'Samp.': 'Samp.',
    'Samplers': 'Sampler',
    'Shak.': 'Shak.',
    'Shakers': 'Shaker',
    'Sl.': 'Sl.',
    'Sn.': 'Sn.',
    'Snares': 'Snare',
    'Sto.': 'Sto.',
    'Synth Bass': 'Synth Bass',
    'Synth Basses': 'Synth Bass',
    'Tab.': 'Tab.',
    'Tabla': 'Tabla',
    'Tabla (larger)': 'Tabla (Lớn hơn)',
    'Tabla (smaller)': 'Tabla (Nhỏ hơn)',
    'Tablas': 'Tabla',
    'Taikos': 'Trống Taiko',
    'Tamb.': 'Tamb.',
    'Tambourines': 'Tambourine',
    'Ten. Dr.': 'Ten. Dr.',
    'Th.': 'Th.',
    'Theremin': 'Theremin',
    'Theremins': 'Theremin',
    'Tim.': 'Tim.',
    'Tko': 'Tko',
    'Tkos': 'Tko',
    'Tn.': 'Tn.',
    'Tr.': 'Tr.',
    'Treble staff': 'Khuông nhạc Sol',
    'W. Bl.': 'W. Bl.',
    'Wada.': 'Wada.',
    'Wadaikos': 'Wadaiko',
    'Wood Block': 'Mõ gỗ',
    'Wood Blocks': 'Mõ gỗ',
    'Woodwind': 'Bộ gió',
    'Ww.': 'Ww.',
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
        continue                      # identity introduces nothing
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

# Round 1's rule 3, still enforced: a plural takes its singular's wording.
for k, v in real.items():
    sing = k[:-1] if k.endswith('s') else None
    if sing and sing in after and after[sing] != v:
        problems.append(f'plural differs from its singular: {k!r} -> {v!r} '
                        f'but {sing!r} -> {after[sing]!r}')

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
