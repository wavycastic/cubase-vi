#!/usr/bin/env python3
"""Readability: Vietnamese that is grammatical but hard to read, plus length.

Three detectors that used to live in three files, merged because they all answer
one question — "would a Vietnamese engineer have to stop and re-read this?".

  python tools/clarity.py                 summary (default)
  python tools/clarity.py long  [n]        values too wordy for a dialog
  python tools/clarity.py hard  [n]        noun stacks, doubled function words
  python tools/clarity.py --list <what>   every hit instead of a count

Nothing here is a missing translation or a wrong technical term. It is all
"candidates for human reading", per AGENT.md §8.9. **A section that has fired
on nothing for several rounds is a detector to switch off, not to keep** — see
the note on audit_clarity in AGENT.md §7.
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

LONG_MIN = 78        # a Cubase label wraps or clips past roughly this width
HARD_MIN = 62        # a sentence past this is where reading slows down
STACK_MAX = 4        # content words in a row with nothing between
MAXLEAK = 400        # longest English run inside a Vietnamese sentence


def words(v):
    return WORD.findall(MASK.sub(' ', v))


def unmasked(v):
    return MASK.sub(' ', v)


# ------------------------------------------------------------------ long
def sec_long(limit):
    hits = sorted(((len(v), k, v) for k, v in vi.items() if len(v) >= LONG_MIN),
                  reverse=True)
    print(f'clarity [long]  {len(hits)} values >= {LONG_MIN} chars')
    for n, k, v in hits[:limit]:
        print(f'  [{n:>4}] {k!r}\n         {v!r}')
    return len(hits)


# ------------------------------------------------------------------ hard
STOP = {'không', 'của', 'các', 'và', 'hoặc', 'được', 'là', 'có', 'cho',
        'với', 'từ', 'trong', 'này', 'đó', 'khi', 'nếu', 'để', 'theo', 'như',
        'mà', 'ở', 'ra', 'vào', 'lên', 'xuống', 'sau', 'trước', 'giữa',
        'cùng', 'cả', 'mỗi', 'mọi', 'nào', 'gì', 'ai', 'rồi', 'đã', 'sẽ',
        'bị', 'phải', 'muốn', 'cần', 'nên', 'vẫn', 'còn', 'chỉ', 'cũng',
        'một', 'hai', 'làm', 'dùng', 'chọn', 'tạo', 'xem', 'hiện'}


def sec_hard(limit):
    """Two structural tells only.

    There is deliberately NO "English word inside a Vietnamese sentence" signal
    here. It cannot be done by charset: `trong`, `cho`, `khi`, `ghi`, `theo`,
    `xung` are all pure-ASCII Vietnamese syllables, so any `[A-Za-z]+` rule
    flags them. That is exactly how audit_readability2.py came to report 1,171
    false positives whose five most frequent "English fragments" were
    trong/cho/khi/ghi/theo — all Vietnamese. Use `audit.py fragments` for
    that check: it prints the distinct words so a human can judge them.
    """
    hits = []
    for k, v in vi.items():
        if len(v) < HARD_MIN or not VIET.search(v):
            continue
        reasons = []
        run = best = 0
        for t in words(v):
            run = 0 if t.lower() in STOP else run + 1
            best = max(best, run)
        if best > STACK_MAX:
            reasons.append(f'stack {best}')
        for fn in ('của', 'và', 'không', 'là', 'bị', 'được'):
            if re.search(rf'\b{fn}\b[^.]{{0,40}}\b{fn}\b', v):
                reasons.append(f'double {fn}')
                break
        if reasons:
            hits.append((k, v, reasons))
    hits.sort(key=lambda x: x[0])
    print(f'clarity [hard]  {len(hits)} values >= {HARD_MIN} chars with a signal')
    for k, v, reasons in hits[:limit]:
        print(f'  {k!r}\n      {v!r}\n      {"; ".join(reasons)}')
    return len(hits)


SECS = {"long": sec_long, "hard": sec_hard}

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--list':
        a = a[1:]
    what = a[0] if a else 'all'
    limit = int(a[1]) if len(a) > 1 and a[1].isdigit() else 25
    if what in SECS:
        SECS[what](limit)
    elif what == 'all':
        n = sum(SECS[k](limit) for k in ('long', 'hard'))
        print(f'\nclarity audit : {len(vi)} strings — {n} signals in total')
    else:
        print(__doc__)
        sys.exit(2)