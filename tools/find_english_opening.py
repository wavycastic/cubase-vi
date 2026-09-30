#!/usr/bin/env python3
"""Find values whose FIRST WORD is an English verb - the frame class again,
seen from the left edge.

Round 36's detector looks for four consecutive English words anywhere in the
value. This one is a much cheaper read of the same defect, and it catches the
frames that are shortest:

    "Importing audio stream from video file..."
      -> "Importing audio stream tu video file..."
    "Replacing audio stream in video file..."
      -> "Replacing audio stream trong video file..."
    "Cannot remove existing audio stream from video file!"
      -> "Khong the Gio bo existing audio stream tu video file!"

A Vietnamese sentence does not begin with a bare English -ing form. A label
does - but a label is short, and it has no Vietnamese in it to be a frame.

So the test is: first word is English, ends in -ing or is one of a few
frame-verbs, and the value goes on for more than 30 characters. Which leaves
out "MIDI Input" and every legitimate untranslated label.

  python tools/find_english_opening.py [minlen]
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 30

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# A VIETNAMESE LETTER, spelled with escapes on purpose. The obvious
# [A-ỿ] is U+0100 to U+1EF9, and it is WRONG: Vietnamese keeps its most
# common letters - a, a, e, e, o, o, u, u, d and their tone marks - in
# U+00C0 to U+00FF, which is BELOW the start of that range. So a value
# written entirely with those letters, like "Thêm bè", tested as NOT
# Vietnamese, and eight detectors built on this test were quietly looking
# at a subset of the map. Found in round 53, by a value that should have
# been reported and was not.
HAN = re.compile(r'[\u00c0-\u024f\u1e00-\u1eff]')
# a leading English word that is a verb form, so a frame rather than a label
OPEN = re.compile(
    r'^(?:[A-Z][a-z]+ing|[A-Z][a-z]+ed|'
    r'Failed|Cannot|Could not|Double-Click|Use|Using|Overwrite|Reset|'
    r'Merge|Convert|Apply|Choose|Select|Disable|Enable|Switch|Toggle|'
    r'Import|Export|Insert|Delete|Remove|Add|Open|Save|Close|Show|Hide|'
    r'Press|Click|Drag|Keep|Let|Make|Set|Start|Stop|Play|Record|Process)\b')

rows = []
for k, v in vi.items():
    if len(v) < MIN or not HAN.search(v):
        continue
    m = OPEN.match(v)
    if m:
        rows.append((k, v, m.group(0)))

rows.sort()
print(f'values over {MIN} chars that start with an English verb: {len(rows)}\n')
for k, v, w in rows:
    print(f'  {w:<10} {k[:62]!r}')
    print(f'  {"":<10} {v[:126]!r}')
