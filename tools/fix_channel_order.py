#!/usr/bin/env python3
"""Repair the reversed "X Channel" family.

English puts the head noun last ("Input Channel"). The automated pass moved
it to the front, producing "Channel Input" - 112 strings.

Two passes, because the reversal is only safe when the whole value is the
phrase:

  simple    the value is exactly "Channel Word" or "Channel Words", so
            flipping back cannot touch anything else in the sentence
  manual    a sentence or label with other words, listed in WORDS, handled
            key by key

Nothing is written unless the result still contains "Channel" and no U+FFFD.

  python tools/fix_channel_order.py            # dry run
  python tools/fix_channel_order.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# Only these heads are real modifiers that belong in front of "Channel".
HEADS = {
    'Audio', 'Effect', 'FX', 'Input', 'Output', 'Frozen', 'Drum', 'Event',
    'Sampler', 'Phones', 'Resize', 'Metering', 'Separate', 'Search', 'Linked',
    'Identical', 'Extracted', 'Instrument', 'VCA', 'MixConsole', 'Mixer',
    'Group', 'Surround', 'Cue', 'Monitor', 'MIDI', 'Groove',
    'Sub', 'Side', 'Return', 'Narrow', 'Wide', 'Folder',
}
# "Channel Aftertouch" is the MIDI term and already reads correctly, so
# Aftertouch is deliberately absent from HEADS.

# a value made of nothing but the reversed phrase
SIMPLE = re.compile(r'^Channel ([A-Z][a-zA-Z]+)(s?)$')

# the value carries more words, so it is decided by hand
MANUAL = {
    'Colorize Selected Channel': 'Tô màu Channel đã chọn',
    'Colorize Tracks and MixConsole Channels':
        'Tô màu Track và Channel MixConsole',
    'Control Room Cue Channels': 'Cue Channel của Control Room',
    'Default Channel Position': 'Vị trí Channel mặc định',
    'EQ Comparison Channel': 'EQ Comparison Channel',
    'Enables/Disables Group Channel for Folder Track':
        'Bật/Tắt Group Channel cho Folder Track',
    'File: Load Selected Channels': 'File: Tải Channel đã chọn',
    'File: Save Selected Channels': 'File: Lưu Channel đã chọn',
    'Folding: Disable Group Channel': 'Folding: Tắt Group Channel',
    'Folding: Enable Group Channel': 'Folding: Bật Group Channel',
    'Group/Effect-Channel': 'Group/Effect Channel',
    'Host Input Channel': 'Host Input Channel',
    'Include MIDI Channel': 'Include MIDI Channel',
    'Input Group and Channel': 'Input Group and Channel',
    'Link/Unlink Selected Channels': 'Liên kết/Hủy liên kết Channel đã chọn',
    'MIDI Channel follows track selection':
        'MIDI Channel bám theo lựa chọn Track',
    'MIDI Controller Channel': 'MIDI Controller Channel',
    'MIDI Output Channel': 'MIDI Output Channel',
    'MIDI Send Group and Channel': 'MIDI Send Group and Channel',
    'Max. RMS All Channels': 'Max. RMS mọi Channel',
    'Naming Scheme - Single Channel': 'Quy tắc đặt tên - Single Channel',
    'Output Group and Channel': 'Output Group and Channel',
    'SMF: MIDI Channel': 'SMF: MIDI Channel',
    'L/R Channels from Surround': 'Channel L/R từ Surround',
    'Show/Hide: Audio Channels': 'Hiện/Ẩn: Audio Channel',
    'Show/Hide: Drum Channels': 'Hiện/Ẩn: Drum Channel',
    'Show/Hide: Effect Channels': 'Hiện/Ẩn: Effect Channel',
    'Show/Hide: Group Channels': 'Hiện/Ẩn: Group Channel',
    'Show/Hide: Input Channels': 'Hiện/Ẩn: Input Channel',
    'Show/Hide: Instrument Channels': 'Hiện/Ẩn: Instrument Channel',
    'Show/Hide: Output Channels': 'Hiện/Ẩn: Output Channel',
    'Show/Hide: Surround Channels': 'Hiện/Ẩn: Surround Channel',
    'Show/Hide: VCA Channels': 'Hiện/Ẩn: VCA Channel',
    'Show/Hide: VCA Fader Channels': 'Hiện/Ẩn: VCA Fader Channel',
    'Show/Hide: Mixer Channels': 'Hiện/Ẩn: Mixer Channel',
    'Show/Hide: Wide/Narrow Channels': 'Hiện/Ẩn: Wide/Narrow Channel',
    'Show/Hide: MIDI Channels': 'Hiện/Ẩn: MIDI Channel',
    'Show/Hide: Sampler Channels': 'Hiện/Ẩn: Sampler Channel',
    'Individual Channels': 'Channel riêng lẻ',
    'Used Channels': 'Channel đã dùng',
    'VST Instrument Channels': 'VST Instrument Channel',
    'Single Channel': 'Single Channel',
    'With Group Channel': 'Kèm Group Channel',
    'Splitting Channels...': 'Đang tách Channel...',
    'From Channel': 'Từ Channel',
}

fixes = {}

# --- simple: the whole value is the reversed phrase -------------------------
for k, v in vi.items():
    m = SIMPLE.match(v)
    if m and m.group(1) in HEADS:
        fixes[k] = f'{m.group(1)} Channel{m.group(2)}'

# --- manual ---------------------------------------------------------------
for k, new in MANUAL.items():
    if k in vi:
        fixes[k] = new

bad = [(k, v) for k, v in fixes.items()
       if '\ufffd' in v or 'Channel' not in v]
if bad:
    print('PROBLEM:')
    for k, v in bad:
        print(f'  {k!r} -> {v!r}')
    sys.exit(1)

print(f'simple reversals : {sum(1 for k, v in fixes.items() if k not in MANUAL)}')
print(f'manual           : {sum(1 for k in fixes if k in MANUAL)}')
print(f'total to change  : {sum(1 for k, v in fixes.items() if vi.get(k) != v)}')
print()
for k, v in list(fixes.items()):
    if vi.get(k) != v:
        print(f'  {k[:52]!r}\n      {vi[k]!r}\n   -> {v!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in fixes.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s)')
