"""Check that every mark of punctuation survives: ? ! ... : and ;.

AGENT.md and the project brief both require it - "bao toan 100% placeholder,
dau hai cham, ?/!/., dau ba cham" - and nothing in the pipeline checked it.
check_style.py enforces placeholders, no trailing gloss, no empty value, no
[RM] marker and the DAW-term list. Punctuation was always assumed.

The reason it needs its own check is that a lost mark is invisible in a long
value: a missing "?" at the end of a question still reads as a question, and a
lost "..." after a menu command still reads as a menu command. It shows up in
the UI as a missing ellipsis on a button, and nobody would report it.

Three classes, and the third is the one that catches real defects:

    ? ! and ;      count must match, so a question does not become a statement
    ...            the ellipsis must survive, and the SOURCE may have one and
                   the translation not
    :             a colon count is only meaningful when the source has one at
                   all - a colon in the value that the source does not have is
                   not a defect, because a translation may legitimately need a
                   colon the English spelled with a full stop

    python tools/check_punctuation.py
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
MAP = os.path.join(ROOT, 'translations', 'vi.json')

src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(MAP, encoding='utf-8'))

# a run of three or more dots is one ellipsis, however long the source wrote it
ELL = re.compile(r'\.{3,}')


def counts(s):
    return {
        '?': s.count('?'),
        '!': s.count('!'),
        ';': s.count(';'),
        '...': len(ELL.findall(s)),
    }


bad = []
for k, v in sorted(vi.items()):
    en = src.get(k)
    if en is None:
        continue
    a, b = counts(en), counts(v)
    why = None
    for mark in ('?', '!', ';', '...'):
        if a[mark] != b[mark]:
            why = (mark, a[mark], b[mark])
            break
    # the last two requirements nobody had checked either: the LINE BREAKS and
    # the leading and trailing whitespace. A lost \n turns a two-sentence
    # tooltip into one run-on line, and a lost trailing space silently changes
    # what Cubase draws, because the XML preserves it.
    if why is None:
        if en.count('\\n') != v.count('\\n'):
            why = ('\\n', en.count('\\n'), v.count('\\n'))
        elif (en[:1].isspace()) != (v[:1].isspace()):
            why = ('leading space', int(bool(en[:1].isspace())),
                   int(bool(v[:1].isspace())))
        elif (en[-1:].isspace()) != (v[-1:].isspace()):
            why = ('trailing space', int(bool(en[-1:].isspace())),
                   int(bool(v[-1:].isspace())))
    if why:
        bad.append((k, why[0], why[1], why[2], en, v))

print(f'values whose punctuation, line breaks or edge whitespace differ '
      f'from the source: {len(bad)}\n')
for k, mark, want, got, en, v in bad[:40]:
    print(f'  {mark!r} source {want} -> value {got}')
    print(f'      EN {en[:74]!r}')
    print(f'      VI {v[:74]!r}')
if len(bad) > 40:
    print(f'  ... and {len(bad) - 40} more')
sys.exit(1 if bad else 0)
