#!/usr/bin/env python3
"""Author `instrumentnames_vi.xml` - the Score Editor's instrument names.

    python tools/score_instruments.py --extract        # English -> batch files
    python tools/score_instruments.py --build          # batch files -> the XML
    python tools/score_instruments.py --check          # coverage report
    python tools/score_instruments.py --status 120     # what is left, in context

The Score Editor is Steinberg's Dorico engine, `ScoringEngine.dll`, and it
localises itself from its own l10n folder rather than from translation.xml.
`ScoringEngine.dll` globs that folder, so a Vietnamese file is authoring work
rather than a binary patch.  See `cubelib/score.py` for the format.

The batch files are plain `{english: vietnamese}` JSON, one per instrument
family, in `translations/score/instruments/`, which is the shape the rest of
this repo already uses.  Only the five name fields are keyed on, so a
translation is written once and lands in every entity that uses that name -
624 entities, 1,126 distinct strings, 3,115 field instances.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from cubelib import score                                      # noqa: E402

L10N = os.path.join(r'E:\Steinberg\Cubase 15', 'Components',
                    'ScoringEngine', 'l10n')
SOURCE = os.path.join(L10N, 'instrumentnames_en.xml')
OUT = os.path.join(ROOT, 'build', 'instrumentnames_vi.xml')
BATCH_DIR = os.path.join(ROOT, 'translations', 'score', 'instruments')
REPORT = os.path.join(ROOT, 'build', 'instrumentnames_vi.txt')
VI_JSON = os.path.join(ROOT, 'translations', 'vi.json')

#: batch file stem -> the entityID segment it collects.  The families mirror
#: `instrumentname.*`, so a batch file is a coherent list a translator can
#: work through in one sitting.
FAMILIES = [
    ('brass', 'brass'),
    ('frets', 'fretted'),
    ('keyb', 'keyboard'),
    ('perc', 'pitchedpercussion'),
    ('percun', 'unpitched'),
    ('pluck', 'plucked'),
    ('str', 'strings'),
    ('wind', 'wind'),
    ('sing', 'singers'),
    ('band', 'band'),
    ('other', None),          # anything not matched above
]


def family_of(entity_id):
    """Which batch file an entity belongs to."""
    for stem, segment in FAMILIES:
        if segment is None:
            continue
        if f'.{segment}.' in entity_id or entity_id.endswith(f'.{segment}'):
            return stem
    return 'other'


def load_batches():
    """Every batch file, merged.  Later files win; clashes are reported.

    A key whose value is the empty string is a placeholder written by
    `--extract` and means "not translated yet", so it is kept out of the
    mapping: the builder then leaves that field in English rather than
    blanking it.  This lets the skeleton list every string a translator owes
    without pretending any of them are done.
    """
    merged, pending, clashes = {}, set(), []
    files = sorted(glob.glob(os.path.join(BATCH_DIR, '*.json')))
    for path in files:
        name = os.path.basename(path)
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        for key, value in data.items():
            if value == '':
                pending.add(key)
                continue
            pending.discard(key)
            if key in merged and merged[key] != value:
                clashes.append(f'{name}: {key!r} != {merged[key]!r}')
            merged[key] = value
    return merged, pending, clashes, [os.path.basename(f) for f in files]


def coverage(entities, mapping):
    """What is translated, measured on strings and on field slots.

    Three buckets, because a Vietnamese instrument name is legitimately the
    English one - `Zither`, `Aluphone`, `Oboe` - and counting that as
    untranslated would send a translator hunting for a difference that is not
    there.
    """
    total = done = same = 0
    slots = slots_done = 0
    missing = []
    for ent in entities:
        for value in ent.fields.values():
            if not value:
                continue
            slots += 1
            if value in mapping:
                slots_done += 1
    for value, users in score.source_strings(entities).items():
        total += 1
        if value in mapping:
            done += 1
            if mapping[value] == value:
                same += 1
        else:
            missing.append((family_of(users[0]), value, len(users)))
    return {'strings': total, 'translated': done, 'unchanged': same,
            'slots': slots, 'slots_done': slots_done, 'missing': missing}


def cmd_import(args):
    """Seed the batch files from the repo's own Vietnamese UI.

    Cubase's main string table already names about 150 of these instruments,
    and reusing those translations verbatim is what keeps the Score Editor
    calling a Conga a `Conga` in both places.  It also settles the house
    style rather than inventing one: the name stays English and only the
    register qualifier is translated - `Tenor Drum (High)` -> `Trống Tenor
    (Cao)`, `Conga` -> `Conga`.
    """
    with open(args.vi, encoding='utf-8') as fh:
        vi = json.load(fh)
    _, entities = score.read(args.source)
    strings = score.source_strings(entities)

    seeded, identity = [], []
    for value in sorted(strings):
        got = vi.get(value)
        if not got:
            continue
        # An identity mapping is a resolution too - a Conga is correctly
        # `Conga` - so it is recorded rather than left looking like a gap.
        (identity if got == value else seeded).append((value, got))

    # The batch files are the source of truth, so rewrite them with the seeds
    # in place rather than holding a second copy here.
    mapping, pending, clashes, _ = load_batches()
    if clashes:
        sys.exit('!! conflicting translations; fix them before importing')
    resolved = dict(seeded + identity)
    buckets = {stem: {} for stem, _ in FAMILIES}
    for value, users in strings.items():
        stem = family_of(users[0])
        buckets[stem][value] = resolved.get(value, mapping.get(value, ''))

    os.makedirs(BATCH_DIR, exist_ok=True)
    for stem, _ in FAMILIES:
        rows = dict(sorted(buckets[stem].items(), key=lambda kv: kv[0].lower()))
        with open(os.path.join(BATCH_DIR, f'{stem}.json'), 'w',
                  encoding='utf-8') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1, sort_keys=False)
            fh.write('\n')

    print(f'{len(seeded):>4} of {len(strings):,} instrument strings already '
          f'exist in the main UI table')
    print(f'{len(identity):>4} more are identical there, so they are already '
          'right')
    print(f'{len(strings) - len(seeded) - len(identity):>4} left to translate\n')
    for stem, _ in FAMILIES:
        todo = sum(1 for v in buckets[stem].values() if not v)
        print(f'  {stem:8} {todo:>4} to do')


def cmd_extract(args):
    text, entities = score.read(args.source)
    mapping, pending, clashes, existing = load_batches()
    if clashes:
        for c in clashes[:10]:
            print(f'!! conflicting translations: {c}', file=sys.stderr)
        sys.exit(1)

    buckets = {stem: {} for stem, _ in FAMILIES}
    for value, users in score.source_strings(entities).items():
        buckets[family_of(users[0])][value] = mapping.get(value, '')

    os.makedirs(BATCH_DIR, exist_ok=True)
    done = 0
    for stem, _ in FAMILIES:
        rows = dict(sorted(buckets[stem].items(), key=lambda kv: kv[0].lower()))
        path = os.path.join(BATCH_DIR, f'{stem}.json')
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1, sort_keys=False)
            fh.write('\n')
        todo = sum(1 for v in rows.values() if not v)
        done += len(rows) - todo
        print(f'  {stem:8} {len(rows):>5} strings   {todo:>5} to do   '
              f'-> {os.path.relpath(path, ROOT)}')
    print(f'\n{len(pending)} placeholders cleared, {done:,} translation(s) '
          f'carried over from {len(existing)} batch file(s)')
    print(f'{len(score.source_strings(entities)):,} distinct strings over '
          f'{len(entities)} entities, 5 name fields each')


def cmd_build(args):
    mapping, pending, clashes, files = load_batches()
    if not files:
        sys.exit(f'no batch files in {BATCH_DIR} - run --extract first')
    if clashes:
        for c in clashes[:10]:
            print(f'!! conflicting translations: {c}', file=sys.stderr)
        sys.exit(1)

    _, entities = score.read(args.source)
    known = set(score.source_strings(entities))
    report = score.build(args.source, mapping, args.out)
    problems = score.check_consistency(mapping, known)
    if problems:
        print(f'!! {len(problems)} consistency problem(s); the file above was '
              'written but should not be deployed:')
        for p in problems[:40]:
            print(f'   {p}')
        sys.exit(1)
    cov = coverage(entities, mapping)

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8', newline='') as fh:
        fh.write(f'source        {args.source}\n')
        fh.write(f'output        {args.out}  ({os.path.getsize(args.out):,} '
                 'bytes)\n')
        fh.write(f'entities      {report["entities"]} '
                 f'({report["unique"]} unique IDs)\n')
        fh.write(f'language      {report["language"]}  '
                 f'{report["language_markers"]} markers, retagged from '
                 f'{", ".join(report["mis_tagged"])}\n')
        fh.write(f'strings       {cov["translated"]:,} / {cov["strings"]:,} '
                 f'written, of which {cov["unchanged"]:,} identical to '
                 'English\n')
        fh.write(f'field slots   {cov["slots_done"]:,} / {cov["slots"]:,} '
                 f'({cov["slots_done"] * 100 // max(1, cov["slots"])}%)\n')
        fh.write(f'still to do   {len(cov["missing"]):,}\n')
        fh.write(f'unused keys   {len(report["unused"])}\n')
        for k in report['unused'][:50]:
            fh.write(f'  ?  {k!r}\n')

    print(f'wrote {args.out} ({os.path.getsize(args.out):,} bytes)')
    print(f'  {report["entities"]} entities, language {report["language"]}, '
          f'{report["language_markers"]} markers')
    print(f'  {cov["translated"]:,} / {cov["strings"]:,} strings written '
          f'({cov["unchanged"]:,} identical to English)')
    print(f'  {cov["slots_done"]:,} / {cov["slots"]:,} field slots '
          f'({cov["slots_done"] * 100 // max(1, cov["slots"])}%)')
    print(f'  {len(cov["missing"]):,} strings still to translate')
    if report['mis_tagged']:
        print(f'  retagged stray language marker(s) left in the source: '
              f'{", ".join(report["mis_tagged"])}')
    if report['unused']:
        print(f'  {len(report["unused"])} batch key(s) matched no entity - '
              f'see {os.path.relpath(REPORT, ROOT)}')
    print(f'report: {os.path.relpath(REPORT, ROOT)}')


def cmd_check(args):
    _, entities = score.read(args.source)
    mapping, pending, clashes, files = load_batches()
    cov = coverage(entities, mapping)
    todo = len(cov['missing'])
    print(f'batch files {len(files)}   keys {len(mapping) + len(pending):,}'
          f'   clashes {len(clashes)}')
    print(f'strings     {cov["translated"]:>6,} translated  '
          f'{cov["unchanged"]:>5,} identical to English  {todo:>5,} to do'
          f'   of {cov["strings"]:,}')
    print(f'field slots {cov["slots_done"]:>6,} / {cov["slots"]:,} '
          f'({cov["slots_done"] * 100 // max(1, cov["slots"])}%)')

    problems = score.check_consistency(mapping,
                                       set(score.source_strings(entities)))
    if clashes:
        problems = [f'{len(clashes)} conflicting translation(s)'] + problems
    if problems:
        print(f'\n!! {len(problems)} problem(s):')
        for p in problems[:40]:
            print(f'   {p}')
        if len(problems) > 40:
            print(f'   ... and {len(problems) - 40} more')
        sys.exit(1)
    print('\nno consistency problems')

    if args.verbose:
        by = {}
        for fam, value, n in cov['missing']:
            by.setdefault(fam, []).append((value, n))
        print('\nstill to translate, by family:')
        for fam in sorted(by):
            print(f'  {fam} ({len(by[fam])})')
            for value, n in by[fam][:args.verbose]:
                print(f'      {value!r}  x{n}')


def cmd_status(args):
    """Print the untranslated strings, grouped, for translation by hand."""
    _, entities = score.read(args.source)
    mapping, _, _, _ = load_batches()
    missing = []
    for value, users in score.source_strings(entities).items():
        if value not in mapping:
            missing.append((family_of(users[0]), value, len(users)))
    missing.sort()
    lo = max(0, args.start)
    for fam, value, n in missing[lo:lo + args.count]:
        print(f'{fam:8} x{n:<3} {value}')
    print(f'\n{lo + args.count} of {len(missing)} shown, '
          f'{len(missing)} strings left', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--source', default=SOURCE,
                    help='instrumentnames_en.xml (the template)')
    ap.add_argument('--out', default=OUT,
                    help='where to write instrumentnames_vi.xml')
    ap.add_argument('--vi', default=VI_JSON,
                    help='the main UI table to seed translations from')
    ap.add_argument('-v', '--verbose', action='count', default=0,
                    help='--check: show the strings that are left')
    ap.add_argument('--start', type=int, default=0, help='--status: skip N')
    ap.add_argument('--count', type=int, default=40, help='--status: how many')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('import', help='seed from translations/vi.json')
    sub.add_parser('extract', help='write the batch files')
    sub.add_parser('build', help='write instrumentnames_vi.xml')
    sub.add_parser('check', help='coverage report')
    sub.add_parser('status', help='list what is still untranslated')
    args = ap.parse_args()
    {'import': cmd_import, 'extract': cmd_extract, 'build': cmd_build,
     'check': cmd_check, 'status': cmd_status}[args.cmd](args)


if __name__ == '__main__':
    main()
