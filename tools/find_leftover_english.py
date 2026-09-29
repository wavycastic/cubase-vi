#!/usr/bin/env python3
"""Isolate real leftover English sentences, hiding the technical labels.

audit_pure_english.py found 1,232 multi-word values with no Vietnamese. Most
are Cubase terminology that AGENT.md 2 says to keep ("ASIO Buffer", "Arranger
Chain") and those are correct as they are. This filter isolates the ones that
are actually wrong: a sentence carrying an English function word.

Prints them in translation-sized chunks so each can be rewritten by reading it,
not by pattern substitution.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

VIET = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
           'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')

# A sentence carries a finite verb. Requiring an article as well was too strict
# and hid real leftovers like "Export to MP3 is not supported for Surround
# channels" that begin with an imperative verb.
VERB = re.compile(
    r'\b(is|are|was|were|be|been|being|has|have|had|does|do|did|'
    r'cannot|can|could|will|would|should|may|might|must|'
    r'not|follow|follows|contain|contains|containsp|says|say|'
    r'match|matches|remain|remains|apply|applies|appear|appears|'
    r'require|requires|need|needs|use|uses|used|make|makes|keep|keeps|'
    r'seem|seems|become|becomes|mean|means|imply|implies|'
    r'start|starts|stop|stops|end|ends|open|opens|save|saves|'
    r'reset|resets|clear|clears|close|closes|select|selects|'
    r'disabled|enabled|activated|deactivated|possible|impossible|'
    r'available|unavailable|found|selected|locked|edited|saved)\b', re.I)

# A sentence also ends like one, or contains a negation. Cubase bullet items
# start with "- " and carry no terminal punctuation at all, so the leading
# marker counts as a terminator too.
TERMINAL = re.compile(r'[.!?]|\bnot\b|\bcannot\b|\bmust\b|\bunavailable\b|'
                      r'\bimpossible\b|\bdisabled\b|^\s*-\s', re.I)

# A value that is only placeholders, units or a filename pattern is not prose.
NOT_PROSE = re.compile(r'^[\s%.,\d:/-]*$|^\(%\.?\d+[ ]?[a-zA-Z]+\)$')


def is_prose(v):
    bare = re.sub(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]', ' ', v)
    if NOT_PROSE.match(v.strip()):
        return False
    return bool(VERB.search(bare)) and bool(TERMINAL.search(v))


leftover = []
for k, v in vi.items():
    if any(c in VIET for c in v):
        continue
    if is_prose(v):
        leftover.append((k, src.get(k, k), v))

leftover.sort(key=lambda x: x[0].lower())

out = os.path.join(ROOT, 'tools', 'leftover_english.txt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (k, s, v) in enumerate(leftover, 1):
        f.write(f'### {i:03d}\nKEY: {k}\nNOW: {v}\n\n')

print(f'values with no Vietnamese        : {sum(1 for v in vi.values() if not any(c in VIET for c in v))}')
print(f'... of which real English prose  : {len(leftover)}')
print(f'\nwrote {out}')
for i, (k, s, v) in enumerate(leftover[:10], 1):
    print(f'  {k[:70]!r}\n      -> {v[:70]!r}')
