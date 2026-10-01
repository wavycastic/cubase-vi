#!/usr/bin/env python3
"""Round 82: the Scaling / Zoom collision, found while checking round 81.

Round 81 fixed readability. Verifying its output with audit_readability2.py
turned up a term split the earlier rounds had not caught, and it is a
mistranslation rather than a style choice:

    "Application Scaling"              -> "Thu phóng ứng dụng"
    "User Interface Scaling: Decrease" -> "Thu phóng giao diện: Giảm"
    "User Interface Scaling: Increase" -> "Thu phóng giao diện: Tăng"

"Thu phóng" is Zoom, and Zoom is already 71 keys of English "Zoom" in this
map. So these three say Zoom in a place where Cubase means Scaling, which
gives the reader two names for one concept and the wrong one.

The map's own word for Scaling is "co giãn" - "Scale Automation Data" ->
"Co giãn dữ liệu Automation", "Equivalent Tempo Scaling" -> "Co giãn Tempo
tương đương" - and it is the right word: these three are HiDPI scale factors
in Preferences, percentages, not a view magnification. All three move to
"co giãn", which also removes the split.

  python tools/fix_reading82.py
  python tools/fix_reading82.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
PH = re.compile(r'%(?:(?:\.\d+)?[a-zA-Z%]|l)')

WORDING = {
    'Application Scaling': 'Co giãn ứng dụng',
    'User Interface Scaling: Decrease': 'Co giãn giao diện: Giảm',
    'User Interface Scaling: Increase': 'Co giãn giao diện: Tăng',
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

# The claim in the docstring: after this, no key says "thu phóng" while any
# key says "Zoom". Checked here rather than asserted, because a docstring that
# can go stale is worse than no docstring.
left = [k for k, v in vi.items() if 'thu phóng' in v.lower()
        and not any(k == r for r in real)]
if left:
    print('STILL SPLIT:')
    for k in left:
        print(f'  {k!r} -> {vi[k]!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k!r}')
    print(f'      {vi.get(k, "")!r}')
    print(f'   -> {v!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changed.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s) to batches')
