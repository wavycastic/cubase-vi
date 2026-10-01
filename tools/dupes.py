#!/usr/bin/env python3
"""Every way one map entry can be a lie that no single-value check can see.

  python tools/dupes.py keys      near-duplicate keys whose VI drifted apart
  python tools/dupes.py values    two DIFFERENT keys sharing ONE value
  python tools/dupes.py json FILE duplicate keys inside one JSON file

`values` is the one that found the defects nothing else could see. Round 55:

    "Add Key Signature"   -> "Thêm số chỉ nhịp"
    "Add Time Signature"  -> "Thêm số chỉ nhịp"

Two menu items with identical text: the user cannot tell them apart, opens the
wrong one, and no log says why. Every other check in this project is
per-value, so two individually perfect values pass.

It is also what found, in round 189, that `Temple Block` and `Wood Block` —
two different instruments — both translated to `Mõ gỗ`.

`keys` is the opposite direction: Cubase ships the same label under several keys
that differ only by case, a trailing dot or an ellipsis. Those must not drift.
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VI = os.path.join(ROOT, 'translations', 'vi.json')


def load():
    return json.load(open(VI, encoding='utf-8'))


def load_src():
    src = {}
    p = os.path.join(ROOT, 'keys', 'all_strings.tsv')
    for line in open(p, encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, u = line.split('\t', 1)
            src[k] = u
    return src


# ---------------------------------------------------------------- keys
def canon(k):
    """Collapse the cosmetic differences between equivalent keys."""
    s = k.strip()
    s = re.sub(r'\s*\.\.\.$', '', s)          # trailing ellipsis
    s = re.sub(r'\s*\[RM\]$', '', s)           # right-click marker
    s = re.sub(r'\s*\[QP\]$', '', s)           # quantize-picker marker
    s = re.sub(r'\.\s*$', '', s)               # trailing dot
    return s.strip().lower()


def run_keys():
    vi = load()
    groups = collections.defaultdict(list)
    for k, v in vi.items():
        groups[canon(k)].append((k, v))

    drift = []
    for c, items in groups.items():
        if len(items) > 1 and len({v for _, v in items}) > 1:
            drift.append((c, sorted(items)))
    drift.sort(key=lambda x: -len(x[1]))
    print(f'near-duplicate key groups with differing Vietnamese: {len(drift)}\n')

    real = []
    for c, items in drift:
        stripped = {v.rstrip('.… ') for _, v in items}
        if len(stripped) > 1:
            real.append((c, items))
    print(f'... of which genuinely different wording: {len(real)}\n')
    for c, items in real[:30]:
        print(f'  canonical: {c!r}')
        for k, v in items:
            print(f'      {k!r:56} -> {v!r}')
        print()


# ---------------------------------------------------------------- values
HAN = re.compile(r'[À-ỹĐđ]')
WORD = re.compile(r"[a-z]+")
STOP = set("a an the of in on at to for with and or is are no".split())


def content(s):
    return {w for w in WORD.findall(s.lower()) if w not in STOP}


def run_values():
    src = load_src()
    vi = load()
    g = collections.defaultdict(list)
    for k, v in vi.items():
        if not HAN.search(v):
            continue          # an untranslated label is a label, not a bug
        g[v].append(k)

    rows = []
    for v, ks in g.items():
        if len(ks) < 2:
            continue
        # only interesting when the KEYS are not themselves the same words
        sets = [content(k) for k in ks]
        if all(s == sets[0] for s in sets):
            continue
        rows.append((len(ks), ks, v))
    rows.sort(key=lambda t: (-t[0], t[1][0]))
    print(f'collisions: {len(rows)} values shared by different keys\n')
    for n, ks, v in rows:
        print(f'  [{n}] {v[:76]!r}')
        for k in ks:
            print(f'       {k[:70]!r}   (EN: {src.get(k, "?")[:56]})')
        print()


# ---------------------------------------------------------------- json
def run_json(path):
    dups = []

    def hook(pairs):
        c = collections.Counter(k for k, _ in pairs)
        for k, n in c.items():
            if n > 1:
                dups.append((k, n))
        return dict(pairs)

    raw = open(path, encoding='utf-8').read()
    data = json.loads(raw, object_pairs_hook=hook)
    if not dups:
        print('no duplicate keys')
    else:
        print(f'{len(dups)} duplicate key(s):')
        for k, n in dups:
            print(f'  {k!r} x{n}')
        sys.exit(1)
    print(f'{len(data)} entries, all unique')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'keys':
        run_keys()
    elif mode == 'values':
        run_values()
    elif mode == 'json':
        run_json(sys.argv[2] if len(sys.argv) > 2 else VI)
    else:
        print(__doc__)
        sys.exit(2)