#!/usr/bin/env python3
"""Repair the reversed "Modifier Head" family across every Cubase noun.

English puts the head noun last: "Output Bus", "Analyzer Track",
"Factory Presets", "Warp Markers". The automated pass moved it to the front,
producing "Bus Output", "Track Analyzer", "Preset Factory", "Marker Warp".

The reversal is only safe when the Vietnamese is exactly the two words in the
opposite order - then flipping back cannot disturb a sentence. Longer values
are left alone and reported for reading.

  python tools/fix_word_order.py            # dry run
  python tools/fix_word_order.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))

# Head nouns Cubase puts last. Anything not listed is not trusted to be a head.
HEADS = {
    'Channel', 'Bus', 'Track', 'Preset', 'Marker', 'Locator', 'Event', 'Clip',
    'Part', 'Note', 'Voice', 'Lane', 'Slot', 'Fader', 'Window', 'Page',
    'Panel', 'Tool', 'Ruler', 'Cue', 'VCA', 'Meter', 'Display', 'Control',
    'Menu', 'Bar', 'Snapshot', 'Playlist', 'Controller', 'Surface', 'Editor',
    'Filter', 'Plugin', 'Expression', 'Step', 'Pattern', 'Chord', 'Scale',
    'Send', 'Insert', 'Group', 'Effect', 'Automation', 'Tempo', 'Key',
    'Collection', 'Folder', 'Version', 'Layout', 'Zoom', 'View', 'Strip',
    'Node', 'Parameter', 'Value', 'Setting', 'Mode', 'Type', 'Level',
    'Threshold', 'Name', 'Number', 'Count', 'Gain', 'Pan', 'Width', 'Phase',
    'Trim', 'Delay', 'Bypass', 'Setup', 'Table', 'List', 'Field', 'Button',
    'Option', 'Section', 'Row', 'Column', 'Cell', 'Entry', 'Point', 'Range',
    'Start', 'End', 'Position', 'Length', 'Size', 'Offset', 'Panner',
    'Message', 'Mapping', 'Assignment', 'Target', 'Source', 'Destination',
    'Input', 'Output', 'Record', 'Take', 'Punch', 'Grid', 'Quantize', 'Snap',
    'Warp', 'Hitpoint', 'Region', 'Signature', 'Clef', 'Rest', 'Beam', 'Stem',
    'Accidental', 'Staff', 'System', 'Picture', 'Info', 'Status', 'Item',
    'Ruler', 'Anchor', 'Tab', 'Slot', 'Scene', 'Chain', 'Mix', 'Log',
}

# key is exactly "Modifier Head" (one word each, both capitalised)
KEY_PAIR = re.compile(r'^([A-Z][A-Za-z0-9]*)\s+([A-Z][A-Za-z0-9]*)$')
# value is exactly "Head modifier", the two words swapped
VI_PAIR = re.compile(r'^(\S+)\s+(\S+)$')

fixes, skipped = {}, []

for k, v in vi.items():
    m = KEY_PAIR.match(k)
    if not m:
        continue
    mod, head = m.group(1), m.group(2)
    if head not in HEADS:
        continue
    # the Vietnamese must be the same two words, swapped
    vm = VI_PAIR.match(v)
    if not vm:
        continue
    a, b = vm.group(1), vm.group(2)
    if a.casefold() == head.casefold() and b.casefold() == mod.casefold():
        fixes[k] = f'{mod} {head}'
    elif a.casefold() == mod.casefold() and b.casefold() == head.casefold():
        continue                      # already correct
    else:
        skipped.append((k, v))

print(f'reversible pairs found : {len(fixes)}')
print(f'not a clean swap       : {len(skipped)}')
print(f'values to change       : {sum(1 for k, v in fixes.items() if vi[k] != v)}')
print()
for k, v in list(fixes.items())[:20]:
    print(f'  {k[:44]!r}\n      {vi[k]!r}\n   -> {v!r}')
if len(fixes) > 20:
    print(f'  ... and {len(fixes) - 20} more')

if '--skipped' in sys.argv:
    print('\n=== not a clean swap (read these) ===')
    for k, v in skipped:
        print(f'  {k[:56]!r}\n      {v[:60]!r}')

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
