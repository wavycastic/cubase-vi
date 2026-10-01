#!/usr/bin/env python3
"""Round 85: 62 outliers, 18 real defects, 15 new forbidden patterns.

Where this round's findings come from
------------------------------------
Not from reading a glossary. From the shape of the map itself: a DAW term that
the translation keeps in 20 keys and translates in one is not a translation
decision, it is a string that fell out of the family. `audit_outlier.py` finds
that shape; 62 terms have it.

Most of the 62 are not defects, and the reason is worth recording:

  `Insert` 115 translated / 40 kept   -> "chèn" is the verb. Correct.
  `Beam` 22 translated / 0 kept       -> AGENT.md §2: Beam = đuôi nốt. Correct.
  `Threshold` 8 / 0                   -> §5 already fixed "Ngưỡng cho phép đo".

The first attempt (tools/audit_domain.py) asked "which domain terms got
translated?" and returned 16 candidates, of which zero were wrong - it had
proposed banning things §2 requires translated. The question was wrong. Not
"which terms were translated" but "which term has one string that disagrees
with its own family".

The 18 real defects
-------------------
  Ambisonics File Format   -> "Ambisonic"     missing the s; 3 siblings keep it
  Q-Factor                 -> "Hệ số Q"      4 siblings keep "Q-Factor"
  Direct Monitoring        -> "trực tiếp"    15 siblings keep "Direct"
  Latch Buffer             -> "Bộ đệm"      9 siblings keep "Buffer"
  Removeable Media         -> "Ổ đĩa di động" 47 siblings keep "Media"
  Direct Routing (Summing) -> "Cộng dồn"     3 siblings keep "Summing"
  Broadcast Wave Chunk     -> "Khối dữ liệu" 6 siblings keep "Chunk"
  Stream Copy Error        -> "luồng tín hiệu" §5 fixed this class already
  Streams                  -> "Luồng tín hiệu" 10 siblings keep "Stream"
  Running Post Process...  -> "hậu kỳ"       19 siblings keep "Post"
  Video Player             -> "Trình phát"   19 siblings keep "Player"
  Audio Performance Meter  -> "Đo"           20 siblings keep "Meter"
  Audio Performance Monitor-> "Theo dõi"     36 siblings keep "Monitor"
  signal chain             -> "chuỗi tín hiệu" 50 siblings keep "Chain"
  Catch Range              -> "dải bắt"     5 siblings keep "Catch"
  subsection/section       -> "khu vực con/cha" 6 siblings keep "Subsection"
  9 Pin Serial Port        -> "Cổng nối tiếp" 4 siblings keep "Serial"
  Track Folding (2)        -> "Gập Track"    8 siblings keep "Folding"
  Region %d                -> "Vùng %d"      20 siblings keep "Region"

What did NOT get a pattern, and why
-----------------------------------
`thẻ` (13 strings, `vùng` 213, `tam giác` 2, `bộ nhớ đệm` 2, `thẻ người
dùng` 2) each render something that is right at least once:

    thẻ   -> "Set up Tabs" = "Thiết lập thẻ"    (right)
             "Removing User Tag" = "thẻ người dùng" (wrong)
    vùng  -> 213 strings, "vùng chọn" (selection) is right in most of them

A pattern is only added when the bad rendering is the ONLY rendering - that
is `tools/_decide.py`, and it is why this round adds 15 patterns and not 23.
The remaining 8 are fixed as strings, where a pattern would block correct
neighbours. AGENT.md §7: a detector that cries wolf is worse than none.

  python tools/fix_reading85.py
  python tools/fix_reading85.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from cubelib.placeholders import PLACEHOLDER

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

WORDING = {
    # 1. missing letter: the family writes "Ambisonics Decoder" / "Ambisonics
    #    Encoder" / "Ambisonics File" - this one drops the s
    # AGENT.md §6: key != English. The key is "Ambisonic File Format" and the
    # English column is "Ambisonics File Format" - the missing s is in the KEY,
    # not in the translation. Writing the key into WORDING would have been
    # correct; the guard below is what caught it.
    'Ambisonic File Format': 'Định dạng file Ambisonics',

    # 2-5. term kept by the family, translated in one string
    'Q-Factor': 'Q-Factor',
    'Direct Monitoring': 'Direct Monitoring',
    'Latch Buffer': 'Latch Buffer',
    'Removeable Media': 'Media có thể tháo',

    # 6. Summing is the Cubase term for summing busses
    'Direct Routing (Summing)': 'Direct Routing (Summing)',

    # 7. Chunk is the container term; "Khối dữ liệu" loses the sense of a
    #    fixed-size block
    'Broadcast Wave Chunk': 'Broadcast Wave Chunk',

    # 8-9. §5 already ruled "audio stream" -> "Audio Stream"; these two
    #      predate or missed it
    'Stream Copy Error': 'Lỗi sao chép Audio Stream',
    'Streams': 'Audio Stream',

    # 10-11. Post and Player are names, not ordinary words
    'Running Post Process Script': 'Đang chạy Script Post Process',
    'Video Player': 'Video Player',

    # 12-13. "Audio Performance Meter" is a panel name. Note both keys differ
    #        only in the last word, so translating one and not the other gives
    #        the same Vietnamese phrase for two different panels.
    'Audio Performance Meter': 'Audio Performance Meter',
    'Audio Performance Monitor': 'Audio Performance Monitor',

    # 14. "signal chain" is lowercase in the source, so this is prose
    'Drag to change order of modulators in signal chain':
        'Kéo để đổi thứ tự Modulator trong signal chain',

    # 15. Catch Range is the quantize option; 5 siblings keep "Catch"
    'Quantize in Catch Range': 'Quantize trong Catch Range',

    # 16. Section/Subsection are Zone concepts
    'Assign subsection to section': 'Gán Subsection vào Section',

    # 17. Serial (as opposed to Parallel) - 4 siblings keep "Serial"
    '9 Pin Serial Port': 'Cổng Serial 9-Pin',

    # 18. Folding is a Zone display term
    'Track Folding': 'Track Folding',
    'Deep Track Folding': 'Deep Track Folding',

    # 19. Region is a Locator-family term; 20 siblings keep it
    'Region %d': 'Region %d',

    # 20. the pattern check caught this one: "Cắt Note Expression" was the
    #     only value rendering Trim as a Vietnamese verb, against 6 siblings
    #     that keep it. Found by the round's own guard, not by hand.
    'Trim Note Expression to Note Length': 'Trim Note Expression theo độ dài nốt',
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()
    sys.exit(1)

bad = [(k, v) for k, v in real.items()
       if sorted(PLACEHOLDER.findall(src[k])) != sorted(PLACEHOLDER.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

# Every claim this round makes, checked against the map AS IT WILL BE.
after = dict(vi)
after.update(real)

problems = []

# 1. the two "Audio Performance" keys must not collapse to one phrase
if after['Audio Performance Meter'] == after['Audio Performance Monitor']:
    problems.append('Audio Performance Meter and Monitor are now identical')

# 3. no value may contradict the pattern this round is adding
BANNED = {
    r'\bambisonic\b(?!s)': 'Ambisonics',
    r'\bhệ số q\b': 'Q-Factor',
    r'monitoring trực tiếp': 'Direct Monitoring',
    r'bộ đệm latch': 'Latch Buffer',
    r'cộng dồn': 'Summing',
    r'khối dữ liệu': 'Chunk',
    r'xử lý hậu kỳ': 'Post',
    r'đo hiệu năng': 'Meter',
    r'theo dõi hiệu năng': 'Monitor',
    r'chuỗi tín hiệu': 'Chain',
    r'\bdải bắt\b': 'Catch Range',
    r'khu vực cha': 'Subsection',
    r'cổng nối tiếp': 'Serial',
    r'cắt note expression': 'Trim',
}
for k, v in after.items():
    for rx, term in BANNED.items():
        if re.search(rx, v, re.I):
            problems.append(f'rule still broken ({term}): {k[:50]!r}')

if problems:
    print('RULE STILL BROKEN:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print(f'characters added : '
      f'{sum(len(v) - len(vi.get(k, "")) for k, v in changed.items())}')
print()
for k, v in changed.items():
    old = vi.get(k, '')
    print(f'  {k[:56]!r}  {len(old)}c -> {len(v)}c')
    print(f'      {old!r}')
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