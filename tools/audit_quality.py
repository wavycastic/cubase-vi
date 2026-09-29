#!/usr/bin/env python3
"""Measure how much of the map is actually untranslated or off-glossary.

Three separate defects the previous audit could not see:
  1. fully untranslated  - value has no Vietnamese letter at all
  2. glossary violation  - a concept rendered with the wrong term
  3. reordered leakage   - Vietnamese word ... English function word
"""
import json, os, re, collections, sys

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


def has_viet(s):
    return any(c in VIET for c in s)


# ---------------------------------------------------------------- 1. untranslated
# A real untranslated sentence carries an English function word. Labels made of
# loanwords only ("CC10 : Pan", "29.97 fps", "%s: Ins. %d") are correct and must
# not be counted, so require a function word, not just any English.
SENTENCE = re.compile(
    r'\b(is|are|was|were|be|been|being|has|have|had|does|do|did|'
    r'cannot|could|will|would|should|may|might|must|'
    r'the|this|that|these|those|there|their|they|them|we|our|you|your|'
    r'not|no|if|when|while|after|before|while|please|'
    r'and|or|but|for|from|into|with|without|within|about|of|to|by)\b', re.I)
SENT_END = re.compile(r'[.!?]')

untranslated = [k for k, v in vi.items()
                if not has_viet(v)
                and SENT_END.search(src.get(k, ''))
                and SENTENCE.search(src.get(k, ''))]

# ---------------------------------------------------------------- 2. glossary
# One concept must have exactly one rendering. Left = what is already agreed,
# the scan reports every other variant that is currently in the map.
GLOSSARY = {
    'bar (measure)':      ['ô nhịp', 'Bar', 'cột nhịp', 'ô phách'],
    'system (score)':     ['dòng nhạc', 'hệ thống', 'System'],
    'staff (score)':      ['khuông nhạc', 'Staff', 'khoang'],
    'clef':               ['khóa nhạc', 'Clef', 'khoá nhạc'],
    'rest':               ['dấu lặng', 'Rest', 'lặng'],
    'beam':               ['đuôi nốt', 'Beam', 'chày', 'quảng'],
    'note (music)':       ['nốt', 'Note', 'note'],
    'chord':              ['hợp âm', 'Chord'],
    'scale':              ['Scale', 'thang', 'thang âm'],
    'voice (music)':      ['bè', 'Voice', 'giọng'],
    'stem':               ['thân nốt', 'Stem', 'cây nốt'],
    'ledger line':        ['dòng kẻ', 'ledger'],
    'key signature':      ['hóa biểu', 'Hóa biểu'],
    'time signature':     ['số chỉ nhịp', 'Time Signature'],
    'barline':            ['vạch nhịp', 'Barline'],
}

violations = collections.defaultdict(list)
for k, v in vi.items():
    s = src.get(k, '').lower()
    for concept, forms in GLOSSARY.items():
        base = concept.split(' ')[0]
        if base not in s:
            continue
        present = [f for f in forms if f in v]
        if len(present) > 1 or (present and present[0] not in forms[:1]):
            violations[concept].append((k, v, present))

# ---------------------------------------------------------------- 3. reorder
# "Dấu lặng Beam over", "Mục này thuộc về" - a Vietnamese token, then an English
# word, then an English function word. Normal Vietnamese never does this.
REORDER = re.compile(
    r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]'
    r'[^.!?:]{0,40}?\b(over|under|with|for|from|into|through|across|'
    r'between|above|below|after|before|during|without|within)\b', re.I)
reordered = [k for k, v in vi.items() if REORDER.search(v)]

print(f'strings total                    : {len(vi)}')
print(f'with any Vietnamese             : {sum(1 for v in vi.values() if has_viet(v))}')
print()
print(f'[1] fully untranslated prose     : {len(untranslated)}')
print(f'[2] glossary concepts in conflict: {len(violations)}')
print(f'[3] reordered English preposition: {len(reordered)}')

if '--list' in sys.argv:
    print('\n=== [1] untranslated ===')
    for k in untranslated:
        print(f'  {src.get(k, "")!r}')
    print('\n=== [3] reordered ===')
    for k in reordered:
        print(f'  {vi[k]!r}')
    print('\n=== [2] glossary ===')
    for c, items in violations.items():
        print(f'\n  -- {c} ({len(items)}) --')
        for k, v, forms in items[:6]:
            print(f'     {forms} {v[:88]!r}')
