#!/usr/bin/env python3
"""The two things a reader complains about, in one place.

  [A] LONG  - values too wordy to fit a dialog or a toolbar button.
  [B] HARD  - values that are grammatical Vietnamese but hard to parse:
              noun-phrase stacks, bare English runs, doubled function words.

Both sections are candidates for human reading, not errors. Thresholds live at
the top of the file; run with --list to see the strings behind a signal.

Written for round 81, which is where readability stopped being hand-picked.
Use it to find the next batch instead of scrolling vi.json.

  python tools/audit_clarity.py
  python tools/audit_clarity.py --list A
  python tools/audit_clarity.py --list B --min 40
  python tools/audit_clarity.py --minlen 90        # only the worst offenders
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

VIET = re.compile(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
                  r'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]')
WORD = re.compile(r"[A-Za-zÀ-ỹ]+(?:[-'][A-Za-zÀ-ỹ]+)*")
MASK = re.compile(r'"[^"]*"|\'[^\']*\'|%(?:\.\d+)?[a-zA-Z%]|\{[^}]*\}')

# A Cubase label wraps or clips past roughly this width, and a sentence past
# this is the point where reading slows down. Both are heuristics, and the
# --minlen flag is there so you can move them without editing the file.
LONG_MIN = 78        # chars
HARD_MIN = 62        # chars

# Vietnamese function words and light verbs. A run of content words longer
# than this with none of them between is the "wall of nouns" complaint:
# Vietnamese marks case and number with separate syllables, so an English
# noun phrase translated word-for-word stops being skimmable.
STACK_MAX = 4
STOP = {'không', 'của', 'các', 'và', 'hoặc', 'được', 'là', 'có', 'cho',
        'với', 'từ', 'trong', 'này', 'đó', 'khi', 'nếu', 'để', 'theo', 'như',
        'mà', 'ở', 'ra', 'vào', 'lên', 'xuống', 'sau', 'trước', 'giữa',
        'cùng', 'cả', 'mỗi', 'mọi', 'nào', 'gì', 'ai', 'rồi', 'đã', 'sẽ',
        'bị', 'phải', 'muốn', 'cần', 'nên', 'vẫn', 'còn', 'chỉ', 'cũng',
        'một', 'hai', 'làm', 'dùng', 'chọn', 'tạo', 'xem', 'hiện'}

# 3+ English words in a row inside a sentence that has Vietnamese in it.
BARE3 = re.compile(r'\b(?:[A-Za-z]+\s+){2,}[A-Za-z]+\b')
# "Các Track và các Track" - the same word twice, which the eye reads as a
# mistake even when it is not.
DOUBLED = re.compile(r'\b(\w{2,})\s+\1\b', re.I)
# Pairs where both halves say the same thing. Each can go without the reader
# losing the meaning, which is what makes them padding rather than prose.
REDUNDANT = [
    'đã được', 'vẫn còn', 'có thể được', 'được cho phép',
    'trong trường hợp', 'hiện tại là', 'cùng một lúc', 'toàn bộ các',
    'những cái', 'các thứ', 'đi kèm với', 'ở phía', 'về việc',
    'do đó', 'theo hướng', 'được tính là',
]


def opt(flag, dflt):
    return int(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else dflt


long_hits, hard_hits = [], []
for k, v in vi.items():
    notes = []
    if len(v) >= LONG_MIN:
        notes.append(f'long {len(v)}c')
    bare = MASK.sub(' ', v)
    if VIET.search(v):
        m = BARE3.search(bare)
        if m and len(m.group(0).split()) >= 3:
            notes.append('english-run: ' + m.group(0).strip())
        d = DOUBLED.search(bare)
        if d:
            notes.append(f'doubled: {d.group(0)!r}')
        for phrase in REDUNDANT:
            if re.search(r'\b' + phrase + r'\b', bare, re.I):
                notes.append(f'redundant: {phrase}')
                break
        run = best = 0
        for w in WORD.findall(bare):
            if w.lower() in STOP:
                run = 0
            else:
                run += 1
                best = max(best, run)
        if best > STACK_MAX:
            notes.append(f'noun-stack x{best}')
    if not notes:
        continue
    rec = (k, v, notes)
    if len(v) >= LONG_MIN:
        long_hits.append(rec)
    if len(v) >= HARD_MIN and any(n != f'long {len(v)}c' for n in notes):
        hard_hits.append(rec)

long_hits.sort(key=lambda r: -len(r[1]))
hard_hits.sort(key=lambda r: (-len(r[2]), -len(r[1])))

mode = sys.argv[sys.argv.index('--list') + 1].upper() if '--list' in sys.argv else None
limit = opt('--min', 25)
minlen = opt('--minlen', LONG_MIN)
if '--minlen' in sys.argv:
    long_hits = [r for r in long_hits if len(r[1]) >= minlen]

print(f'clarity audit : {len(vi)} strings')
print(f'  [A] long   (>={LONG_MIN} chars)      : {len(long_hits)}')
print(f'  [B] hard   (>={HARD_MIN} + a signal) : {len(hard_hits)}\n')

if mode in (None, 'A'):
    print('=== [A] LONGEST values ===')
    for k, v, notes in long_hits[:limit]:
        print(f'\nEN: {src.get(k, "?")[:150]}')
        print(f'VI: {v}')
        print(f'    {"; ".join(notes)}  [{len(v)}c]')

if mode in (None, 'B'):
    print('\n=== [B] HARDEST to parse ===')
    for k, v, notes in hard_hits[:limit]:
        print(f'\nEN: {src.get(k, "?")[:150]}')
        print(f'VI: {v}')
        print(f'    {"; ".join(notes)}  [{len(v)}c]')

print('\n=== signal counts ===')
c = collections.Counter()
for _, _, notes in long_hits + hard_hits:
    for n in notes:
        c[re.sub(r'\s+x?\d+c?$', '', n.split(':')[0])] += 1
c['(strings)'] = len({k for k, _, _ in long_hits + hard_hits})
for name, n in c.most_common():
    print(f'  {name:16} {n}')
