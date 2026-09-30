"""Find the extractor's DISAMBIGUATION gloss left inside a translated value.

    "Link [short, verb]"      ->  "Lien ket [ngan, dong tu]"
    "Direction [direction of a stem]"
                              ->  "Direction [huong cua than not]"
    "Panner [Channel Latency Overview]"
                              ->  "Panner [Tong quan do tre Channel]"

Round 66 established the mechanism: when two labels share an English, the
extractor puts a marker in the KEY - "[Key]", "[Mouse]", "{{Noun}}", "[RM]",
"[direction of a stem]" - and Cubase looks the translation up by that Key, not
by the English. All eight vendors rely on it, and several of them give the two
keys different translations for the same English to prove it.

Which means the marker is addressed to the extractor and to nobody else. It is
not part of the label, and a translation that echoes it back has printed the
extractor's private note on screen:

    Lien ket [ngan, dong tu]        <- the Vietnamese user reads this

This is AGENT.md rule 1 - no dictionary-style parenthetical at the end of a
value - and rule 1 does not catch it, because the KEY has a bracket too and the
rule skips those. The guard is right for a bracket the SOURCE had, and wrong
for a bracket the extractor invented: "Chord Pad Output Mode\nOn: Output is
sent to..." has no invented bracket, while "Link [short, verb]" has one and the
English inside it is a note to the translator, not text anyone will read.

So the test is: a bracketed span in the VALUE that is not a key chord, not a
placeholder, and not a source bracket. Those three are real; anything else is a
note that leaked.

  python tools/find_gloss_in_value.py
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
BRACKET = re.compile(r'\[([^\]]*)\]|\{\{([^{}]*)\}\}')
# A key chord, which after round 54 can be Vietnamese: [ALT + nhan chuột],
# [nhan chuột + giu], [Shift + ALT + nhan chuột].
#
# The letter class is [^\W\d_] - any Unicode letter - and NOT [A-Za-zÀ-ỹ]. That
# range is U+00C0 to U+01FF, which is the SAME trap as the [Ā-ỿ] class in round
# 53: it misses every Vietnamese tone mark, so "nhan chuột" does not match and
# the detector then reports fifty-nine hits, all of them correct.
CHORD = re.compile(r'^(?:[^\W\d_][\w]*|\.|,)'
                   r'(?:\s*[+\-]?\s*(?:[^\W\d_][\w]*|\.|,)){0,3}$')
ONE = re.compile(r'^[^\W\d_][\w]*$')
PUNCT = re.compile(r'^[.,;:/]$')
JOINED = re.compile(r'[+\-]')


def is_chord(inner):
    """A key chord after round 54 is a +-joined list, or a single token.

    Not "short". Two wrong versions of the short test are both instructive:

      a class of [A-Za-zÀ-ỹ] misses every Vietnamese tone mark - the SAME trap
      as [Ā-ỿ] in round 53 - and the detector then reports 59 hits, all of them
      correct values;

      allowing up to four tokens reports 3 hits, because "[huong cua than not]"
      and "[VariAudio Pitch Snap Mode]" are four words and look like a chord.
    """
    if JOINED.search(inner):
        return True
    if PUNCT.match(inner.strip()):
        return True                       # Num[.] - a key named by its face
    if ONE.match(inner.strip()):
        return True                       # [ALT], [CTRL], [Tab]
    # "[nhan chuôt]" is two words with no joiner, because round 54 replaced
    # click with a two-word Vietnamese phrase inside the bracket
    return inner.strip().lower() in ('nhấp chuột', 'click')

rows = []
for k, v in vi.items():
    if not HAN.search(v):
        continue                           # a value with no Vietnamese at all
    for m in BRACKET.finditer(v):
        inner = (m.group(1) or m.group(2) or '').strip()
        if not inner or '%' in inner:
            continue                       # empty, or a placeholder
        if is_chord(inner):
            continue                       # a key chord
        if m.start() == 0:
            # a marker at the FRONT is the marker being TRANSLATED, which is
            # what it is for: "[Mixer Track Number]" -> "[So Track MixConsole]",
            # "[Track Type: Group]" -> "[Loai Track: Group]". Correct as it is.
            continue
        rows.append((k, m.group(0), v))

print(f'bracketed spans in a value that are neither a chord nor a source '
      f'bracket: {len(rows)}\n')
for k, b, v in rows:
    print(f'  {k[:62]!r}')
    print(f'      EN {src.get(k, "?")[:66]!r}')
    print(f'      VI {v[:80]!r}')
    print(f'      ^ {b!r}')
