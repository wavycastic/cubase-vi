#!/usr/bin/env python3
"""List every value with an untranslated English word, grouped, for reading.

probe version: prints a compact one-line-per-string report so a large batch can
be judged and written back by hand instead of by regex substitution.

  python tools/audit_fragments.py           count by word
  python tools/audit_fragments.py --list    every hit, with its key
"""
import json, os, re, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

ENGLISH = re.compile(
    r'\b(?:Activate|Deactivate|Assignment|Add|Remove|Select|Delete|Enable|'
    r'Disable|Apply|Save|Load|Open|Close|Use|Set|Get|Reset|Copy|Paste|Move|'
    r'Search|Read|Write|Show|Hide|Do|Is|Are|Was|Were|Be|Not|Can|Cannot|Will|'
    r'Must|Have|Has|The|This|That|These|Those|And|Or|But|For|From|Into|'
    r'With|Without|About|Of|To|By|At|On|In|Any|Every|Each|Only|When|While|'
    r'After|Before|If|Than|As|So|Because|Available|New|Old|First|Last|Next|'
    r'Previous|Current|Selected|Active|Inactive|Following|More|Less|Other|'
    r'Separate|Recommended|Machine|Controlled|Such|Its|Their|Them|They|We|'
    r'Our|You|Your|It|Everything|Nothing|Everyone|Some|Anybody|Everybody|'
    r'Please|Someone|Anyone|Nobody|Whose|Which|Where|While|Whether|'
    r'Arrangement|Arranger|Picture|Pictures|Text|Texts|List|Lists|Items|'
    r'Item|Lines|Line|Columes|Column|Rows|Row|Values|Value|Contents)\b')
# Export / Import / Insert / Record / Render / Play / Edit / Track / Channel /
# Marker / etc. are AGENT.md 2 loanwords and are deliberately absent above:
# they were the four most frequent "hits" and all of them were false alarms.

QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]')
VIET = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơ'
           'ờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')

rows = []
for k, v in vi.items():
    if not any(c in VIET for c in v):
        continue                       # pure label, handled elsewhere
    bare = QUOTED.sub(' ', v)
    hits = sorted({m.group(0) for m in ENGLISH.finditer(bare)})
    if hits:
        rows.append((k, v, hits))

by_word = collections.Counter()
for _, _, hits in rows:
    for h in hits:
        by_word[h] += 1

print(f'values with an untranslated English word : {len(rows)}')
print(f'distinct words                          : {len(by_word)}\n')
print('--- most frequent ---')
for w, n in by_word.most_common(30):
    print(f'  {w:16} {n:4}')

if '--list' in sys.argv:
    rows.sort(key=lambda x: (x[2][0].lower(), x[0]))
    for k, v, hits in rows:
        print(f'\n### {",".join(hits)}\nKEY: {k}\nNOW: {v}')
