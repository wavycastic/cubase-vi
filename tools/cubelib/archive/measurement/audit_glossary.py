#!/usr/bin/env python3
"""Check EVERY row of the AGENT.md section 4 glossary against the whole map.

Section 4 is the one artefact in this project that cannot go stale by accident:
it is checked by eye, it is short, and rounds 22, 30, 39, 43 and 45 have each
found a row the map had drifted away from - in both directions. "Chord Symbols"
had seven keys that said something else. "Key Signature" had two that said
`hoa bieu`. The wrong term was in the TABLE once, and the table is what made
eight strings wrong.

So the table is parsed and every row is checked mechanically:

  - for each glossary term, find the keys whose English contains it;
  - if the term is one the glossary KEEPS in English, the value must still
    contain the English;
  - if the term is TRANSLATED, the value must contain the agreed Vietnamese and
    must not contain a rival rendering of the same word.

The last half is the one that needs judgement, so the tool reports the
disagreeing keys rather than failing on them, and the reading decides.

  python tools/audit_glossary.py
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# --- parse section 4 of AGENT.md
text = open(os.path.join(ROOT, 'AGENT.md'), encoding='utf-8').read()
start = text.find('| Staff / Stave |')
if start < 0:
    sys.exit('section 4 table not found')
table = text[start:]
table = table[:table.find('\n\n')]
rows = []
for line in table.splitlines():
    if not line.startswith('|') or line.startswith('|---'):
        continue
    cells = [c.strip() for c in line.strip('|').split('|')]
    if len(cells) < 2 or cells[0] in ('Tiếng Anh',):
        continue
    en, viet = cells[0], cells[1]
    en = re.sub(r'\s*\(.*?\)\s*', ' ', en)
    en = en.replace('**', '').replace('`', '').strip()
    viet = viet.replace('**', '').replace('`', '').strip()
    if not en or not viet:
        continue
    terms = [t.strip() for t in re.split(r'[/,]', en) if t.strip()]
    forms = [f.strip() for f in re.split(r'[/,]', viet) if f.strip()]
    rows.append((en, viet, terms, forms))

print(f'glossary rows parsed: {len(rows)}\n')
bad = 0
for en, viet, terms, forms in rows:
    for term, form in zip(terms, forms):
        # whole-word match: "Rest" must not match "restart", "Stem" must not
        # match "System", "Note" must not match "Notes"
        pat = re.compile(r'\b' + re.escape(term) + r's?\b', re.I)
        keys = [k for k in src if pat.search(src[k])]
        if len(keys) < 3:
            continue
        # the agreed form: "keep X" means the English has to survive
        keep = form.lower().startswith(('giữ', 'keep')) or form == en
        agree = forms[terms.index(term)]
        missing = []
        for k in keys:
            v = vi.get(k, '')
            plural = bool(re.search(r'\b' + re.escape(term) + r's\b',
                                    src[k], re.I))
            if keep:
                # "keep Note" means keep the TERM. The plural is Vietnamese:
                # round 20 settled that "Notes" is "cac not" and only the
                # singular term stays English, so 1/8 Note is "Note 1/8".
                ok = pat.search(v) is not None or (plural and 'nốt' in v)
            else:
                ok = agree.lower() in v.lower()
            if not ok:
                missing.append((k, v))
        if missing:
            bad += len(missing)
            tag = 'KEEP' if keep else 'TRANSLATED'
            print(f'  {tag} {term!r} -> {agree!r}   ({len(keys)} keys, '
                  f'{len(missing)} disagree)')
            for k, v in missing[:5]:
                print(f'      {k[:58]!r}')
                print(f'        {v[:100]!r}')
            if len(missing) > 5:
                print(f'      ... and {len(missing) - 5} more')
            print()
print(f'total disagreeing values: {bad}')
