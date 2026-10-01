#!/usr/bin/env python3
"""Read the Vietnamese map by hand - the step AGENT.md §8.9 insists on.

  python tools/read.py long  [domain] [start] [count] [minlen]
  python tools/read.py short [domain] [start] [count] [maxlen]
  python tools/read.py page  <start> [count] [-q] [-w N]
  python tools/read.py sample [domain|all] [start] [count]
  python tools/read.py worklist [A|B|C|D] [limit]
  python tools/read.py inspect <query>

`long`    full sentences. That is where awkwardness lives and what a user
          actually complains about reading.
`short`   menu labels and button names, ~9,000 of one to six words. That is
          where term drift lives, because a label has no sentence to carry the
          meaning and is the first thing an automated pass gets wrong.
`page`    TUẦN TỰ theo thứ tự key, không lọc, không chấm điểm. This is the one
          that misses nothing: every string is read exactly once, in the order
          of keys/all_strings.tsv - the same order used to hand out blocks to
          several people reading in parallel without stepping on each other.
          Two earlier rounds filtered by word count first and got a list of long
          strings, which was wrong: long is not a defect. Read it all and there
          is nothing to filter and nowhere to skip.
`sample`  a random sample per domain, for judging overall feel.
`worklist` what is left untranslated, bucketed by value. Right now every
          bucket is 0 and that number is the point: keep it to prove it.
`inspect` one key across all nine original languages, which is what settles a
          term question. `read.py` prints the Vietnamese, `inspect` prints the
          evidence for it.

Five tools used to do this - read_long, read_short, page, sample_domain,
worklist, inspect_str - all reading the same two files. Round 193 merged them;
`long` and `short` were verified byte-identical to their originals before the
rest were folded in.

`domain` is any name from the table in `domain()` below, or `all`.
"""
import json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VI = os.path.join(ROOT, 'translations', 'vi.json')
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
XML = os.path.join(ROOT, 'keys', 'translation_original.xml')

vi = json.load(open(VI, encoding='utf-8'))
src = {}
ORDER = []
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
        ORDER.append(k)


def domain(k):
    """Which area of Cubase a key belongs to.

    The order below is PRIORITY order: a key is in exactly one bucket, so the
    first pattern that matches wins. `music-theory` is tested before `notation`
    because a key like "Chord Symbols" is music theory, not notation, and the
    naive version put it in notation and never revisited it.
    """
    s = k.lower()
    if re.search(r'\b(chord|voicing|tension|scale|articulation|harmony|note)\b', s):
        return 'music-theory'
    if re.search(r'\b(export|render|bounce|warp|audio|file|pool|import|media|'
                 r'format|bit|sample rate|fade|freeze|process)\b', s):
        return 'media'
    if re.search(r'\b(insert|send|eq|plugin|vst|bus|channel|fader|pan|routing|'
                 r'compressor|gate|limiter)\b', s):
        return 'mixer'
    if re.search(r'\b(locator|marker|cycle|transport|cursor|record|play|loop|'
                 r'tempo|quantize|grid|snap|scroll|zoom)\b', s):
        return 'transport'
    if re.search(r'\b(shortcut|key command|assign|menu|command|context|'
                 r'right.click|window|toolbar|panel|dialog|page)\b', s):
        return 'ui'
    if re.search(r'\b(score|stave|staff|system|bar|beat|clef|rest|notation|'
                 r'beam|ledger|signatur)\b', s):
        return 'notation'
    if re.search(r'\b(network|server|user|permission|shared|profile|'
                 r'project setup|template|preferences)\b', s):
        return 'project'
    return 'general'


def words(v):
    return re.findall(r'[A-Za-zÀ-ỹ]+', v)


def _long(v):
    return len(v) >= 45 and (len(words(v)) >= 6 or '\\n' in v)


# ------------------------------------------------------------------ long
def run_long(a):
    want = a[0] if a else 'all'
    start = int(a[1]) if len(a) > 1 else 0
    count = int(a[2]) if len(a) > 2 else 70
    minlen = int(a[3]) if len(a) > 3 else 45
    items = [(k, v) for k, v in vi.items()
             if len(v) >= minlen and (len(words(v)) >= 6 or '\\n' in v)
             and (want == 'all' or domain(k) == want)]
    items.sort()
    print(f'## {want}  {len(items)} long values  (showing {start}..{start+count})\n')
    for k, v in items[start:start + count]:
        print(f'EN: {src.get(k, "?")}')
        print(f'VI: {v}')
        print()


# ------------------------------------------------------------------ short
def run_short(a):
    want = a[0] if a else 'all'
    start = int(a[1]) if len(a) > 1 else 0
    count = int(a[2]) if len(a) > 2 else 90
    maxlen = int(a[3]) if len(a) > 3 else 44
    items = [(k, v) for k, v in vi.items()
             if not _long(v) and len(v) <= maxlen
             and (want == 'all' or domain(k) == want)]
    items.sort()
    print(f'## {want}  {len(items)} short values  (showing {start}..{start+count})\n')
    for k, v in items[start:start + count]:
        en = src.get(k, '?')
        print(f'{en}\n    {v}')
        if k != en:
            print(f'    <key: {k}>')
        print()


# ------------------------------------------------------------------ page
def run_page(a):
    """Sequential, unfiltered. `-q` prints key + VI only; `-w N` sets EN width."""
    flags = [x for x in a if x.startswith('-')]
    pos = [x for x in a if not x.startswith('-')]
    start = int(pos[0]) if pos else 0
    count = int(pos[1]) if len(pos) > 1 else 60
    quiet = '-q' in flags or '--quiet' in flags
    width = 0
    if '-w' in flags:
        width = int(a[a.index('-w') + 1])
    elif '--width' in flags:
        width = int(a[a.index('--width') + 1])

    if start >= len(ORDER):
        sys.exit(f'start {start} vượt quá {len(ORDER)} chuỗi')
    block = ORDER[start:start + count]

    print(f'#{start}..{start + len(block) - 1} của {len(ORDER)}  '
          f'(còn {len(ORDER) - start - len(block)})')
    if not quiet:
        w = width or 40
        print(f'{"#":>5}  {"EN":<{w}}  VI')
        print('-' * (8 + w + 2))
    for i, k in enumerate(block, start):
        if quiet:
            print(f'{i:>5}  {k}')
            print(f'        {vi[k]}')
        else:
            w = width or 40
            print(f'{i:>5}  {src.get(k, "?")[:w]:<{w}}  {vi[k]}')


# ------------------------------------------------------------------ sample
def run_sample(a):
    want = a[0] if a else None
    start = int(a[1]) if len(a) > 1 else 0
    count = int(a[2]) if len(a) > 2 else 60

    buckets = {}
    for k, v in vi.items():
        buckets.setdefault(domain(k), []).append((k, v))
    if want and want != 'all':
        buckets = {want: buckets.get(want, [])}

    random.seed(7)
    for name, items in sorted(buckets.items()):
        if want and want != 'all' and name != want:
            continue
        print(f'\n######## {name}  ({len(items)} strings) ########')
        for k, v in items[start:start + count]:
            print(f'  EN: {src.get(k, "?")[:110]}')
            print(f'  VI: {v[:110]}')


# ------------------------------------------------------------------ worklist
def run_worklist(a):
    """What is left untranslated, bucketed by how much it is worth."""
    def has_ph(s):
        return bool(re.search(r'%[0-9dsfx]|%l|\{', s))

    have = set(vi)
    rows = [(k, u) for k, u in ((l.split('\t', 1) for l in
              open(TSV, encoding='utf-8').read().splitlines()[1:] if '\t' in l))]
    untr = [(k, u) for k, u in rows if k not in have]
    print(f'total {len(rows):,}  translated {len(rows)-len(untr):,}  '
          f'remaining {len(untr):,}\n')

    buckets = {
        'A. short UI labels (<=22 chars, no placeholders)':
            lambda k, u: len(u) <= 22 and not has_ph(u),
        'B. medium (23-45 chars, no placeholders)':
            lambda k, u: 23 <= len(u) <= 45 and not has_ph(u),
        'C. long (46-90, no placeholders)':
            lambda k, u: 46 <= len(u) <= 90 and not has_ph(u),
        'D. with placeholders':
            lambda k, u: has_ph(u) and len(u) <= 80,
    }
    sel = {}
    for name, f in buckets.items():
        sel[name] = [(k, u) for k, u in untr if f(k, u)]
        print(f'{name:44} {len(sel[name]):,}')

    what = a[0] if a else 'A'
    limit = int(a[1]) if len(a) > 1 else 400
    key = next((n for n in sel if n.startswith(what)), None)
    items = sel.get(key, [])
    print(f'\n--- {key}: showing {min(limit, len(items))} of {len(items)} ---')
    for k, u in items[:limit]:
        print(f'{u}')


# ------------------------------------------------------------------ inspect
def run_inspect(a):
    """One key across all nine original languages. This is what settles a term."""
    q = a[0] if a else ''
    xml = open(XML, encoding='utf-8').read()
    pat = re.compile(r'<String Key="([^"]*' + re.escape(q) + r'[^"]*)">(.*?)</String>',
                     re.S | re.IGNORECASE)
    matches = list(pat.finditer(xml))
    print(f"Found {len(matches)} matching keys for '{q}':\n")
    for m in matches[:30]:
        k = m.group(1)
        langs = dict(re.findall(r'<(\w+)>(.*?)</\1>', m.group(2), re.S))
        print(f'KEY: {k}')
        print(f" US: {langs.get('us', '')}")
        print(f" DE: {langs.get('de', '')}")
        print(f" FR: {langs.get('fr', '')}")
        print(f" VI: {vi.get(k, '<MISSING>')}")
        print('-' * 50)


MODES = {'long': run_long, 'short': run_short, 'page': run_page,
         'sample': run_sample, 'worklist': run_worklist, 'inspect': run_inspect}

if __name__ == '__main__':
    a = sys.argv[1:]
    mode = a[0] if a else 'long'
    if mode in MODES:
        MODES[mode](a[1:])
    else:
        print(__doc__)
        sys.exit(2)