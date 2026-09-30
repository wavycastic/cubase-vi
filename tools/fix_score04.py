#!/usr/bin/env python3
"""Score Editor round 4: brass and woodwind, 320 strings.

These two families settle the last naming question left open by round 3, and
they settle it the same way `instrumentnames_ja.xml` and
`instrumentnames_de.xml` did.

A proper name is never translated; a variant descriptor is.

    English Horn        ja=イングリッシュホーン  de=Englisches Horn
    English Horns       ja=イングリッシュホーン  de=Englische Hörner

    French Horn         ja=フランスホルン        de=Französisches Horn
    Marching French Horn ja=...                  de=Marschtrompete in F

Japanese transliterates `English Horn` and German translates the adjective,
which looks like a disagreement until you notice that the same instrument is
also called `Cor Anglais` - a French name for a thing whose English name
contains an adjective.  That is what a proper name looks like.  `Alphorn`,
`Wagner Tuba`, `Cimbasso`, `Ophicleide`, `Didgeridoo`, `Bansuri` are the
same kind of thing, and round 3's `Charango` and `Cuatro` were decided the
same way.

A descriptor says which member of a family this is, and that is the
language's business: round 3 turned `Acoustic Guitar` into `Guitar acoustic`
and `7-string Electric Guitar` into `Guitar điện 7 dây`, and this round does
the same for the two words that are descriptors rather than names:

    Marching French Horn  ->  French Horn diễu hành
    Valve Trombone        ->  Trombone van

`Baroque Trumpet` stays as it is, because `Baroque` is a loanword in all
three languages - バロックトランペット, Barocktrompete - and not a descriptor
the way `Electric` is.

`Horn (alto)` and `Horn (basso)` are identity, which is round 3's rule 2: a
register that is already a music loanword stays exactly where it is.

The abbreviations run to about 130 of these 320 strings, and all of them keep
their spelling.  That is the pattern in all nine shipped catalogues: `Tbn`,
`Tpt`, `V. Tbn.`, `Cbsn`, `Min-bsn`, `Sno Rec.` and the rest are fixed-width
labels for a narrow part column.

Two keys carry a trailing space, `Picc. Cl. ` and `S. Cl. `.  They map to
themselves, which `cubelib.score.build` permits because an identity mapping
introduces nothing.

  python tools/fix_score04.py
  python tools/fix_score04.py --write
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
FAMILY = ('brass', 'wind')

_, entities = score.read(SOURCE)
en = set(score.source_strings(entities))

WORDING = {
    # ================================================================ brass
    # abbreviations, verbatim
    'A. Hn': 'A. Hn',
    'A. Tbn.': 'A. Tbn.',
    'A. Tbns': 'A. Tbn.',
    'Alp.': 'Alp.',
    'B. Tba': 'B. Tba',
    'B. Tbas': 'B. Tba',
    'B. Tbn.': 'B. Tbn.',
    'B. Tbns': 'B. Tbn.',
    'B. Tpt': 'B. Tpt',
    'B. Tpts': 'B. Tpt',
    'Bar. Bug.': 'Bar. Bug.',
    'Bar. Hn': 'Bar. Hn',
    'Bar. Hns': 'Bar. Hn',
    'Bar. Tpt': 'Bar. Tpt',
    'Bar. Tpts': 'Bar. Tpt',
    'Br.': 'Br.',
    'Cb. Bug.': 'Cb. Bug.',
    'Cb. Tba': 'Cb. Tba',
    'Cb. Tbas': 'Cb. Tba',
    'Cb. Tbn': 'Cb. Tbn',
    'Cb. Tbn.': 'Cb. Tbn.',
    'Cimb.': 'Cimb.',
    'Cor.': 'Cor.',
    'Crt': 'Crt',
    'Crts': 'Crt',
    'Euph.': 'Euph.',
    'F. Hn': 'F. Hn',
    'F. Hns': 'F. Hn',
    'Flug.': 'Flug.',
    'Flugelhorn': 'Flugelhorn',
    'Flugelhorns': 'Flugelhorn',
    'Hn': 'Hn',
    'Hns': 'Hn',
    'M. F. Hn': 'M. F. Hn',
    'Mln.': 'Mln.',
    'Mln. Bug.': 'Mln. Bug.',
    'Oph.': 'Oph.',
    'Picc. Tpt': 'Picc. Tpt',
    'S. Bug.': 'S. Bug.',
    'S. Crt': 'S. Crt',
    'S. Crts': 'S. Crt',
    'Serp.': 'Serp.',
    'Sousa.': 'Sousa.',
    'T. Hn': 'T. Hn',
    'T. Tba': 'T. Tba',
    'T. Tbas': 'T. Tba',
    'T. Tbn.': 'T. Tbn.',
    'T. Tbns': 'T. Tbn.',
    'Tba': 'Tba',
    'Tbas': 'Tba',
    'Tbn': 'Tbn',
    'Tbn.': 'Tbn.',
    'Tbns': 'Tbn',
    'Ten. Tpt': 'Ten. Tpt',
    'Ten. Tpts': 'Ten. Tpt',
    'Tpt': 'Tpt',
    'Tpts': 'Tpt',
    'V. Tbn.': 'V. Tbn.',
    'V. Tbns': 'V. Tbn.',
    'Wr Tba': 'Wr Tba',
    'Wr Tbas': 'Wr Tba',

    # proper names and loanword registers
    'Alpenhorn': 'Alpenhorn',
    'Alphorn': 'Alphorn',
    'Alphorns': 'Alphorn',
    'Alpine Horn': 'Alpine Horn',
    'Alpine Horns': 'Alpine Horn',
    'Alto Horn': 'Alto Horn',
    'Alto Horns': 'Alto Horn',
    'Alto Trombone': 'Alto Trombone',
    'Baritone Bugle': 'Baritone Bugle',
    'Baritone Bugles': 'Baritone Bugle',
    'Baritone Horn': 'Baritone Horn',
    'Baritone Horns': 'Baritone Horn',
    'Baroque Trumpet': 'Baroque Trumpet',
    'Baroque Trumpets': 'Baroque Trumpet',
    'Bass Trombone': 'Bass Trombone',
    'Bass Trombones': 'Bass Trombone',
    'Bass Trumpet': 'Bass Trumpet',
    'Bass Trumpets': 'Bass Trumpet',
    'Bass Tuba': 'Bass Tuba',
    'Bass Tubas': 'Bass Tuba',
    'Contrabass Bugle': 'Contrabass Bugle',
    'Contrabass Bugles': 'Contrabass Bugle',
    'Contrabass Trombone': 'Contrabass Trombone',
    'Contrabass Trombones': 'Contrabass Trombone',
    'Contrabass Tuba': 'Contrabass Tuba',
    'Cornet': 'Cornet',
    'Cornets': 'Cornet',
    'Cornett': 'Cornett',
    'Cornetts': 'Cornett',
    'Euphonium': 'Euphonium',
    'Euphoniums': 'Euphonium',
    'French Horn': 'French Horn',
    'French Horns': 'French Horn',
    'Horn': 'Horn',
    'Horn (alto)': 'Horn (alto)',
    'Horn (basso)': 'Horn (basso)',
    'Horns': 'Horn',
    'Marching French Horn': 'French Horn diễu hành',
    'Marching French Horns': 'French Horn diễu hành',
    'Mellophone': 'Mellophone',
    'Mellophone Bugle': 'Mellophone Bugle',
    'Mellophone Bugles': 'Mellophone Bugle',
    'Mellophones': 'Mellophone',
    'Ophicleide': 'Ophicleide',
    'Piccolo Trumpet': 'Piccolo Trumpet',
    'Piccolo Trumpets': 'Piccolo Trumpet',
    'Serpent': 'Serpent',
    'Serpents': 'Serpent',
    'Soprano Bugle': 'Soprano Bugle',
    'Soprano Bugles': 'Soprano Bugle',
    'Soprano Cornet': 'Soprano Cornet',
    'Soprano Cornets': 'Soprano Cornet',
    'Sousaphone': 'Sousaphone',
    'Sousaphones': 'Sousaphone',
    'Tenor Horn': 'Tenor Horn',
    'Tenor Horns': 'Tenor Horn',
    'Tenor Trombone': 'Tenor Trombone',
    'Tenor Trombones': 'Tenor Trombone',
    'Tenor Trumpet': 'Tenor Trumpet',
    'Tenor Trumpets': 'Tenor Trumpet',
    'Tenor Tuba': 'Tenor Tuba',
    'Tenor Tubas': 'Tenor Tuba',
    'Trombone': 'Trombone',
    'Trombones': 'Trombone',
    'Trumpet': 'Trumpet',
    'Trumpets': 'Trumpet',
    'Tuba': 'Tuba',
    'Tubas': 'Tuba',
    'Wagner Tuba': 'Wagner Tuba',
    'Wagner Tubas': 'Wagner Tuba',
    'Zink': 'Zink',
    'Zinks': 'Zink',

    # the two descriptors that are the language's
    'Cimbasso': 'Cimbasso',
    'Cimbassos': 'Cimbasso',
    'Valve Trombone': 'Trombone van',
    'Valve Trombones': 'Trombone van',

    # ================================================================ wind
    # abbreviations, verbatim - including the two that carry a trailing space
    'A. Cl.': 'A. Cl.',
    'A. Fl.': 'A. Fl.',
    'A. Rec.': 'A. Rec.',
    'A. Sax.': 'A. Sax.',
    'B Cl.': 'B Cl.',
    'B. Cl.': 'B. Cl.',
    'B. Fl.': 'B. Fl.',
    'B. Ob.': 'B. Ob.',
    'B. Rec.': 'B. Rec.',
    'B. Sax.': 'B. Sax.',
    'Bagp.': 'Bagp.',
    'Bans.': 'Bans.',
    'Bar. Ob.': 'Bar. Ob.',
    'Bar. Sax.': 'Bar. Sax.',
    'Bas. Hn': 'Bas. Hn',
    'Bas. Hns': 'Bas. Hn',
    'Bsn': 'Bsn',
    'Bsns': 'Bsn',
    'C Mel. Sax.': 'C Mel. Sax.',
    'C. A.': 'C. A.',
    'C. A. Cl.': 'C. A. Cl.',
    'Cb. Cl.': 'Cb. Cl.',
    'Cb. Fl.': 'Cb. Fl.',
    'Cb. Sax.': 'Cb. Sax.',
    'Cbsn': 'Cbsn',
    'Cbsns': 'Cbsn',
    'Cl.': 'Cl.',
    'Des. Rec.': 'Des. Rec.',
    'Didg.': 'Didg.',
    'Dud.': 'Dud.',
    'Eng. Hn': 'Eng. Hn',
    'Eng. Hns': 'Eng. Hn',
    'Fl.': 'Fl.',
    'Flag.': 'Flag.',
    'Harm.': 'Harm.',
    'Heckl.': 'Heckl.',
    'M-S. Sax.': 'M-S. Sax.',
    'Min-bsn': 'Min-bsn',
    'Min-bsns': 'Min-bsn',
    'Ob.': 'Ob.',
    'Ob. d\'A.': 'Ob. d\'A.',
    'Oca.': 'Oca.',
    'P-pipes': 'P-pipes',
    'P. Fl.': 'P. Fl.',
    'Picc.': 'Picc.',
    'Picc. Cl.': 'Picc. Cl.',
    'Picc. Cl. ': 'Picc. Cl. ',
    'Picc. Sax.': 'Picc. Sax.',
    'S. Cl.': 'S. Cl.',
    'S. Cl. ': 'S. Cl. ',
    'S. Fl.': 'S. Fl.',
    'S. Rec.': 'S. Rec.',
    'S. Sax.': 'S. Sax.',
    'Shaku.': 'Shaku.',
    'Sheh.': 'Sheh.',
    'Sno Cl.': 'Sno Cl.',
    'Sno Rec.': 'Sno Rec.',
    'Sno Sax.': 'Sno Sax.',
    'Spr. Sax.': 'Spr. Sax.',
    'SubCb. Sax.': 'SubCb. Sax.',
    'T. Rec.': 'T. Rec.',
    'T. Sax.': 'T. Sax.',
    'T. Whist.': 'T. Whist.',
    'Ten.': 'Ten.',
    'Tr. Fl.': 'Tr. Fl.',
    'Tr. Rec.': 'Tr. Rec.',

    # proper names and loanword registers
    'Alto Clarinet': 'Alto Clarinet',
    'Alto Clarinets': 'Alto Clarinet',
    'Alto Flute': 'Alto Flute',
    'Alto Flutes': 'Alto Flute',
    'Alto Recorder': 'Alto Recorder',
    'Alto Recorders': 'Alto Recorder',
    'Alto Saxophone': 'Alto Saxophone',
    'Alto Saxophones': 'Alto Saxophone',
    'Bagpipes': 'Bagpipes',
    'Bansuri': 'Bansuri',
    'Bansuris': 'Bansuri',
    'Baritone Oboe': 'Baritone Oboe',
    'Baritone Oboes': 'Baritone Oboe',
    'Baritone Saxophone': 'Baritone Saxophone',
    'Baritone Saxophones': 'Baritone Saxophone',
    'Basset Horn': 'Basset Horn',
    'Basset Horns': 'Basset Horn',
    'Bass Clarinet': 'Bass Clarinet',
    'Bass Clarinets': 'Bass Clarinet',
    'Bass Flute': 'Bass Flute',
    'Bass Flutes': 'Bass Flute',
    'Bass Oboe': 'Bass Oboe',
    'Bass Oboes': 'Bass Oboe',
    'Bass Recorder': 'Bass Recorder',
    'Bass Recorders': 'Bass Recorder',
    'Bass Saxophone': 'Bass Saxophone',
    'Bass Saxophones': 'Bass Saxophone',
    'Bassoon': 'Bassoon',
    'Bassoons': 'Bassoon',
    'Bawu': 'Bawu',
    'C Melody Saxophone': 'C Melody Saxophone',
    'C Melody Saxophones': 'C Melody Saxophone',
    'Clarinet': 'Clarinet',
    'Clarinets': 'Clarinet',
    'Contra Alto Clarinet': 'Contra Alto Clarinet',
    'Contra Alto Clarinets': 'Contra Alto Clarinet',
    'Contrabass Clarinet': 'Contrabass Clarinet',
    'Contrabass Clarinets': 'Contrabass Clarinet',
    'Contrabass Flute': 'Contrabass Flute',
    'Contrabass Flutes': 'Contrabass Flute',
    'Contrabass Saxophone': 'Contrabass Saxophone',
    'Contrabass Saxophones': 'Contrabass Saxophone',
    'Contrabassoon': 'Contrabassoon',
    'Contrabassoons': 'Contrabassoon',
    'Cor Anglais': 'Cor Anglais',
    'Descant Recorder': 'Descant Recorder',
    'Descant Recorders': 'Descant Recorder',
    'Didgeridoo': 'Didgeridoo',
    'Didgeridoos': 'Didgeridoo',
    'Duduk': 'Duduk',
    'Duduks': 'Duduk',
    'English Horn': 'English Horn',
    'English Horns': 'English Horn',
    'Flageolet': 'Flageolet',
    'Flageolets': 'Flageolet',
    'Flute': 'Flute',
    'Flutes': 'Flute',
    'Harmonica': 'Harmonica',
    'Harmonicas': 'Harmonica',
    'Heckelphone': 'Heckelphone',
    'Heckelphones': 'Heckelphone',
    'Mezzo-soprano Saxophone': 'Mezzo-soprano Saxophone',
    'Mezzo-soprano Saxophones': 'Mezzo-soprano Saxophone',
    'Mini-bassoon': 'Mini-bassoon',
    'Mini-bassoon (Quart)': 'Mini-bassoon (Quart)',
    'Mini-bassoon (Quint)': 'Mini-bassoon (Quint)',
    'Mini-bassoons': 'Mini-bassoon',
    'Nai': 'Nai',
    'Nais': 'Nai',
    'Oboe': 'Oboe',
    'Oboe d\'Amore': 'Oboe d\'Amore',
    'Oboe d\'Amores': 'Oboe d\'Amore',
    'Oboes': 'Oboe',
    'Ocarina': 'Ocarina',
    'Ocarinas': 'Ocarina',
    'Pan Flute': 'Pan Flute',
    'Pan Flutes': 'Pan Flute',
    'Panpipes': 'Panpipes',
    'Piccolo': 'Piccolo',
    'Piccolo Clarinet': 'Piccolo Clarinet',
    'Piccolo Clarinets': 'Piccolo Clarinet',
    'Piccolo Saxophone': 'Piccolo Saxophone',
    'Piccolo Saxophones': 'Piccolo Saxophone',
    'Piccolos': 'Piccolo',
    'Shakuhachi': 'Shakuhachi',
    'Shakuhachis': 'Shakuhachi',
    'Shehnai': 'Shehnai',
    'Shehnais': 'Shehnai',
    'Sopranino Clarinet': 'Sopranino Clarinet',
    'Sopranino Recorder': 'Sopranino Recorder',
    'Sopranino Recorders': 'Sopranino Recorder',
    'Sopranino Saxophone': 'Sopranino Saxophone',
    'Sopranino Saxophones': 'Sopranino Saxophone',
    'Soprano Clarinet': 'Soprano Clarinet',
    'Soprano Clarinets': 'Soprano Clarinet',
    'Soprano Flute': 'Soprano Flute',
    'Soprano Flutes': 'Soprano Flute',
    'Soprano Recorder': 'Soprano Recorder',
    'Soprano Recorders': 'Soprano Recorder',
    'Soprano Saxophone': 'Soprano Saxophone',
    'Soprano Saxophones': 'Soprano Saxophone',
    'Soprillo Saxophone': 'Soprillo Saxophone',
    'Soprillo Saxophones': 'Soprillo Saxophone',
    'Subcontrabass Saxophone': 'Subcontrabass Saxophone',
    'Subcontrabass Saxophones': 'Subcontrabass Saxophone',
    'Tenor Recorder': 'Tenor Recorder',
    'Tenor Recorders': 'Tenor Recorder',
    'Tenor Saxophone': 'Tenor Saxophone',
    'Tenor Saxophones': 'Tenor Saxophone',
    'Tenoroon': 'Tenoroon',
    'Tenoroons': 'Tenoroon',
    'Tin Whistle': 'Tin Whistle',
    'Tin Whistles': 'Tin Whistle',
    'Treble Flute': 'Treble Flute',
    'Treble Flutes': 'Treble Flute',
    'Treble Recorder': 'Treble Recorder',
    'Treble Recorders': 'Treble Recorder',
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

problems = score.check_consistency(after, en)
for stem in FAMILY:
    left = [v for v in score.source_strings(entities)
            if family_of(score.source_strings(entities)[v][0]) == stem
            and not after.get(v)]
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
