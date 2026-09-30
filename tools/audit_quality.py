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
# One concept must have exactly one rendering, and that rendering is fixed by
# AGENT.md. The first entry of each list is the agreed form; anything else that
# turns up is a violation. Kept in sync with AGENT.md sections 3 and 4.
GLOSSARY = {
    # AGENT.md 3: Bar is a term to keep in English. "ô nhịp" and "Cột nhịp"
    # are both wrong - the latter means "column".
    'bar (measure)':      ['Bar', 'ô nhịp', 'cột nhịp', 'ô phách'],
    'system (score)':     ['dòng nhạc', 'hệ thống', 'System'],
    # AGENT.md 4: the score desk uses Vietnamese.
    'staff (score)':      ['khuông nhạc', 'Staff', 'khoang'],
    'clef':               ['khóa nhạc', 'Clef', 'khoá nhạc'],
    'rest':               ['dấu lặng', 'Rest', 'lặng'],
    'beam':               ['đuôi nốt', 'Beam', 'chày', 'quảng'],
    'stem':               ['thân nốt', 'Stem', 'cây nốt'],
    'barline':            ['vạch nhịp', 'Barline'],
    'ledger line':        ['dòng kẻ', 'ledger'],
    'key signature':      ['hóa biểu', 'Hóa biểu'],
    'time signature':     ['số chỉ nhịp', 'Time Signature'],
    'voice (music)':      ['bè', 'Voice', 'giọng'],
    # AGENT.md 3: Note and Chord are Cubase terms, but "nốt" and "hợp âm" read
    # better in running Vietnamese and are the majority, so both are allowed.
    'note (music)':       ['nốt', 'Note', 'note'],
    'chord':              ['hợp âm', 'Chord'],
    'scale':              ['Scale', 'thang', 'thang âm'],
}

# Some concepts legitimately carry two forms, because the Vietnamese word and
# the Cubase term are both correct for different things in the same map:
#   "nốt" in a sentence, "Note" in the note-duration fields
#   ("Note 1/8, nốt móc đơn" - Note stays English there by request)
#   "hợp âm" in a sentence, "Chord Track" / "Chord Pad" / "Chord Symbols"
#   "hệ thống" for the operating system, "dòng nhạc" for a line of the score
#   "bè" for a musical voice, "Voice" inside "Single Voice"
# Without this the report is several hundred lines of correct text, which is
# worse than no report at all: it trains the reader to skip the output.
BOTH_OK = {
    'note (music)': {'nốt', 'note'},
    'chord': {'hợp âm', 'chord'},
    'system (score)': {'dòng nhạc', 'hệ thống', 'system'},
    'voice (music)': {'bè', 'voice', 'giọng'},
    'scale': {'scale', 'thang', 'thang âm'},
}

violations = collections.defaultdict(list)
# Two entries have to be dropped before matching, because they are not
# alternative renderings at all:
#   "lặng" is a separate word inside "dấu lặng", so a word-boundary match
#     finds it in every correct value
#   "Hóa biểu" differs from "hóa biểu" only in case, so matching case-blind
#     reports every correct value as a conflict
# Order is preserved: forms[0] is the agreed rendering and is compared against,
# and a plain set would leave that position up to the hash order.
def _forms(fs):
    out = []
    for f in fs:
        low = f.lower()
        if low in out:
            continue
        # Drop a form that is a whole word inside a longer one: "lặng" sits
        # inside "dấu lặng". Keeping both makes every correct value look like
        # it mixes two renderings, because the shorter one always matches too.
        if any(g != low and len(g) > len(low)
               and re.search(r'(?<!\w)' + re.escape(low) + r'(?!\w)', g)
               for g in (x.lower() for x in fs)):
            continue
        out.append(low)
    return out


GLOSSARY = {c: _forms(fs) for c, fs in GLOSSARY.items()}

for k, v in vi.items():
    s = src.get(k, '').lower()
    lv = v.lower()
    for concept, forms in GLOSSARY.items():
        base = concept.split(' ')[0]
        if base not in s:
            continue
        present = {f for f in forms
                   if re.search(r'(?<!\w)' + re.escape(f) + r'(?!\w)', lv)}
        if not present or present <= BOTH_OK.get(concept, set()):
            continue
        # the agreed form is the first; anything else is drift
        if present - {forms[0]} or len(present) > 1:
            violations[concept].append((k, v, sorted(present)))

# ---------------------------------------------------------------- 3. reorder
# "Dấu lặng Beam over", "Mục này thuộc về" - a Vietnamese token, then an English
# word, then an English function word. Normal Vietnamese never does this.
REORDER = re.compile(
    r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]'
    r'[^.!?:]{0,40}?(?<![\w-])(over|under|with|for|from|into|through|across|'
    r'between|above|below|during|without|within)(?![\w-])', re.I)
# "after" and "before" were dropped from the pattern above: Cubase uses them
# inside fixed English compound names that are correct in any language,
# "After Fader Listen", "Click and Hold". They only follow a Vietnamese word
# here because the rest of the name stays English.
# A hyphen on either side rules a match out too, because then the word is a
# compound modifier, not a preposition: "Cross-Over", "Step-In", "Follow-Up".
REORDER = re.compile(
    r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]'
    r'[^.!?:]{0,40}?(?<![\w-])(over|under|with|for|from|into|through|across|'
    r'between|above|below|during|without|within)(?![\w-])', re.I)
# A quoted feature name is a proper noun and stays in English, so an English
# preposition inside one is not a reordering:
#     'Maximum Duration for Rhythmic Slashes' -> "... 'Maximum Duration for
#     Rhythmic Slashes' duoc dat thanh ..."
# The "for" there belongs to the name, not to the sentence. Round 39 hit this
# with two values that were correct.
QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'')
reordered = [k for k, v in vi.items()
             if REORDER.search(QUOTED.sub(' ', v))]

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
