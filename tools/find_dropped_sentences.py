#!/usr/bin/env python3
"""Find long values with FEWER SENTENCES than their source.

The dropped-clause class has now turned up five times by hand:

  round 32  "Picks up on the value of the %s function ... This results in
             smooth value changes, BUT REQUIRES YOU TO ESTIMATE THE PICKUP
             VALUE."
             -> one sentence, the second half gone

  round 38  "When bar numbers are positioned at barlines, you may prefer
             dynamics to be placed closer to the staff than bar numbers, or
             vice versa. THIS HAS NO EFFECT FOR BAR NUMBERS CENTERED ON THE
             BAR, which are always placed outside dynamics."
             -> first sentence only

  round 38  "This option effectively takes precedence ... IF THIS OPTION IS
             SET TO SHOW A CAUTIONARY EITHER WITH OR WITHOUT PARENTHESES, THEN
             OTHER CAUTIONARY ACCIDENTALS ... ARE SUPPRESSED."
             -> first sentence only

  round 40  "The project contains files or crossfades in 32-bit float format.
             ... PLEASE NOTE THAT THIS CONVERSION MIGHT LEAD TO CLIPPING!"
             -> the warning about destroying the audio, gone

  round 44  "You have activated the Steinberg Audio Power Scheme. ... However,
             THIS ALSO INCREASES THE POWER CONSUMPTION of the computer. If
             power consumption is a concern, ... Further information ... can be
             found in the Steinberg Knowledge Base."
             -> one of five sentences survives

Five for five, the lost text is the clause with a CONDITION or a COST in it.
That is not a coincidence about this project: the English states the rule,
and the exception reads as an aside, so a translation pass drops the aside.

Counting sentences is mechanical, so it can be checked rather than read. The
count is a lead, not a verdict - a value legitimately has fewer sentences when
the source is a list of fragments - but the list is short.

  python tools/find_dropped_sentences.py [minlen]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 60

src = {}
longest = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
        # Cubase truncates the long keys, so a key of 60+ characters is a
        # prefix of its own English - the full text appears as ANOTHER row's
        # key. Without this the sentence count is the count of a prefix, and
        # the tool reports 1 -> 1 for strings that lost a sentence.
        longest.setdefault(k[:60], []).append(k)


def full(k):
    """The untruncated English for a key, if the table has exactly one."""
    cand = longest.get(k[:60], [])
    if len(cand) == 1 and len(cand[0]) > len(k):
        return cand[0]
    return src.get(k, '')


vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# a sentence ends at . ! or ?, and abbreviations do not count. A literal \n
# does NOT end a sentence - counting it made every multi-line string look
# short by one, which is noise.
ABBR = re.compile(
    r'(?:\b[A-Z]\.|\b(?:Mr|Mrs|Ms|Dr|Prof|vs|etc|Inc|Ltd|No|approx|cf|ca'
    r'|incl|excl)\.|\b(?:e\.g|i\.e)\.)(?=[,\s)\]]|$)')
SENT = re.compile(r'[.!?](?=[\s"\')\]]|$)')


def count(t):
    t = ABBR.sub('', t)
    # decimals and version numbers are not sentence ends
    t = re.sub(r'\d\.\d', '\0', t)
    return max(1, len(SENT.findall(t)))


rows = []
for k, v in vi.items():
    en = full(k)
    if len(en) < MIN or not en:
        continue
    a, b = count(en), count(v)
    if b < a:
        rows.append((a - b, a, b, k, en, v))

rows.sort(key=lambda t: (-t[0], t[3]))
print(f'values over {MIN} chars with fewer sentences than the source: '
      f'{len(rows)}\n')
for d, a, b, k, en, v in rows:
    print(f'  -{d}  ({a} -> {b})  {k[:70]!r}')
    print(f'      EN {en[:150]!r}')
    print(f'      VI {v[:150]!r}')
