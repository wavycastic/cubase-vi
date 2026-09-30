#!/usr/bin/env python3
"""Sweep every domain for the round 33 defect: a long sentence whose only
Vietnamese is a preposition.

Rounds 33 and 34 found three of these by eye in `general` alone:

    "Click 'Start' to scan for unreferenced files"
      -> "Click 'Start' vao scan cho unreferenced files"
    "Found participants without master: %s. Try to reconnect?"
      -> "Found participants without master: %s. Try vao reconnect?"

audit_leak cannot see them, because the line does contain a Han character.
audit_quality's "fully untranslated prose" test cannot see them either, for
the same reason. So they are invisible to every existing check.

The signal is a ratio: a genuinely translated sentence is mostly Han plus the
DAW terms. One of these is mostly Latin with a stray "vao" or "voi". So -
count Han against Latin over values above 45 characters and list the worst.

This is a lead generator, not a rule. It points at 60 lines out of 10,737;
which of them are wrong is a reading job.

  python tools/find_thin_vietnamese.py [minlen] [top]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 45
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 80

HAN = re.compile(r'[Ā-ỿ]')
LATIN_WORD = re.compile(r'[A-Za-z]{2,}')
# terms that are legitimately kept in English and carry no Vietnamese with them
KEEP = {
    'MIDI', 'MTC', 'SMF', 'LTC', 'VST', 'VST2', 'VST3', 'ASIO', 'OSC', 'MPE',
    'MTC', 'U', 'TB', 'HQ', 'CPU', 'SMPTE', 'UL', 'API', 'CUDA', 'DPI', 'HiDPI',
}

rows = []
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
for k, v in vi.items():
    if len(v) < MINLEN or '�' in v:
        continue
    words = LATIN_WORD.findall(v)
    words = [w for w in words if w not in KEEP]
    if not words:
        continue
    han = len(HAN.findall(v))
    # ratio of Latin letters to Han letters
    lat = sum(len(w) for w in words)
    if lat == 0:
        continue
    r = lat / max(han, 1)
    if r > 1.2:
        rows.append((r, k, v, len(words)))

rows.sort(key=lambda t: -t[0])
print(f'values >= {MINLEN} chars with more Latin than Han: {len(rows)}')
print(f'showing {min(TOP, len(rows))}\n')
for r, k, v, nw in rows[:TOP]:
    print(f'  [{r:4.1f}] {k[:64]!r}')
    print(f'          {v[:130]!r}')
