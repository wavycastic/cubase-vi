"""Find an English FUNCTION WORD sitting in a value outside quotes and brackets.

The frame class is a sentence with a Vietnamese preposition dropped into it:

    "Notes cho Which Accidentals Have Already Been Stated Within the Bar"
    "First channel that is used cho channel rotation"
    "Press up vao 5 keys vao Gan remote keys vao subsections"

Every one of them carries English FUNCTION WORDS - the, is, that, have, been,
up, to, in - and in a correct hybrid value those words only ever appear inside
a quoted feature name, a bracketed key chord, a menu path, or a DAW term.
Elsewhere they are a sentence that was never translated.

So the test is: strip the quoted spans, the bracketed spans, the menu paths and
the format specifiers; then count the English function words left over. Two or
more is a frame, and the list is short.

This is much sharper than the run-length test, which cannot tell "FFT Post EQ
Peak Hold Curve" (a term) from "First channel that is used" (a sentence), and
at a three-word run on short labels that difference is most of the list.

  python tools/find_function_words.py [minfunc]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINF = int(sys.argv[1]) if len(sys.argv) > 1 else 2

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# everything a correct value is allowed to keep in English
MASK = [
    re.compile(r'"[^"]*"'),                 # quoted feature name
    re.compile(r"'[^']*'"),                 # quoted feature name
    re.compile(r'\[[^\]]*\]'),              # [ALT + click], [SHIFT]
    re.compile(r'[\w%]+>[^\s,.]*'),          # Project>Convert>Tracks
    re.compile(r'%[-+ #0-9.]*[a-zA-Z%]'),   # %s, %.0f, %d\%d
    re.compile(r'\\n'),                      # literal line break
]

# English function words only. Deliberately excludes words that are also DAW
# terms or that Cubase prints: "mix", "monitor", "record", "send", "set",
# "show", "click", "control", "input", "output", "channel", "track", "scale",
# "note", "play", "stop", "start", "loop", "undo", "redo", "open", "close".
FUNC = set("""
a an the this that these those there here
is are was were be been being am
to of in on at by for with from into onto over under through across between
above below during without within until since than as so if then else when
while because although though whereas
have has had do does did done not no nor
and or but which who whom whose what
it its they them their he she his her
will would shall should can could may might must
each every any some all both either neither
""".split())

# Past participles are the other half of the same defect, and round 59 turned
# up one the function-word list had been blind to:
#
#     "Used in Project: %s"   ->  "Used trong Project: %s"
#
# An English past participle standing exactly where the Vietnamese verb belongs,
# with a Vietnamese preposition spliced after it. Not a function word by
# anyone's definition - which is precisely why it survived seventeen rounds. A
# frame does not need a function word in it to be a frame. It needs a VERB.
USED = set("""
used selected activated disabled enabled displayed shown hidden opened closed
created deleted added removed imported exported played stopped recorded
bypassed unlinked linked mapped assigned named saved loaded applied toggled
switched restored replaced copied moved resized reloaded synced updated
refreshed pressed released dragged dropped
""".split())
VERBISH = FUNC | USED


TOKEN = re.compile(r"[^\s]+")


def strip(v):
    for rx in MASK:
        v = rx.sub(' ', v)
    return v


def latin_words(text):
    """Whitespace tokens that are PURELY ASCII letters.

    A character-class scan is wrong here, and wrong in a way that invents
    findings: Vietnamese letters are letters, so [A-Za-z]+ cuts `cua` - the
    "a" in a Vietnamese word is an ASCII letter between two non-ASCII ones -
    and every one of those fragments then looks like the English article.
    A token is a word only if every character of it is ASCII.
    """
    for tok in TOKEN.findall(text):
        if tok.isascii() and tok.isalpha():
            yield tok


rows = []
for k, v in vi.items():
    if not HAN.search(v):
        continue
    hit = [w for w in latin_words(strip(v)) if w.lower() in VERBISH]
    if len(hit) >= MINF:
        rows.append((len(hit), k, v, hit))

rows.sort(key=lambda t: (-t[0], t[1]))
print(f'values with {MINF}+ English function words outside quotes and brackets: '
      f'{len(rows)}\n')
for n, k, v, hit in rows:
    print(f'  [{n}] {k[:64]!r}')
    print(f'      {v[:110]!r}')
    print(f'      {hit}')
