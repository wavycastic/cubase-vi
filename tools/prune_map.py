#!/usr/bin/env python3
"""Move map entries that have no matching <String Key> out of vi.json.

Those are guesses that never existed in Cubase's table. Keeping them in vi.json
means the build silently skips them and the map looks healthier than it is, so we
park them in translations/unmatched.json for later.

Usage: python tools/prune_map.py [--dry-run]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda *p: os.path.join(ROOT, *p)
TSV, MAP, OUT = T('keys', 'all_strings.tsv'), T('translations', 'vi.json'), T('translations', 'unmatched.json')
dry = '--dry-run' in sys.argv

if not os.path.exists(TSV):
    sys.exit(f'missing {TSV}\nrun: python tools/list_strings.py keys\\translation_original.xml keys\\all_strings.tsv')

keys = {l.split('\t', 1)[0] for l in open(TSV, encoding='utf-8').read().splitlines()[1:] if '\t' in l}
m = json.load(open(MAP, encoding='utf-8'))

bad = {k: v for k, v in m.items() if k not in keys}
good = {k: v for k, v in m.items() if k in keys}

print(f'{len(m)} entries: {len(good)} match a real <String Key>, {len(bad)} do not')
for k in bad:
    print(f'  no such key: {k!r}')

if not dry and bad:
    prev = {}
    if os.path.exists(OUT):
        prev = json.load(open(OUT, encoding='utf-8'))
    prev.update(bad)
    json.dump(prev, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    json.dump(good, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'\nmoved {len(bad)} -> {os.path.relpath(OUT, ROOT)}; vi.json now {len(good)} entries')

    # strip them from the batch files too, otherwise the next merge brings them back
    import glob
    for b in glob.glob(T('translations', 'batches', '*.json')):
        bd = json.load(open(b, encoding='utf-8'))
        dropped = [k for k in bad if k in bd]
        if not dropped:
            continue
        bd = {k: v for k, v in bd.items() if k not in bad}
        json.dump(bd, open(b, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print(f'  pruned {len(dropped)} from {os.path.relpath(b, ROOT)}')

    print('Use tools/suggest_keys.py to find the real key for those.')
elif dry and bad:
    print('\n(dry run, nothing written)')
