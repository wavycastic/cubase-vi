#!/usr/bin/env python3
"""Classify every value that contains no Vietnamese character at all.

audit_quality.py only looked at values with a sentence-ending mark, so a short
English label slipped through. This asks the blunt question: of the values with
no Vietnamese, which are legitimately loanwords and which were never done?
"""
import json, os, re, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

VIET = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
           'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')

# A label made only of these is a Cubase term, a number, a unit or a file
# format - keeping it in English is what AGENT.md 2 asks for.
BENIGN_SINGLE = {
    # transport / sync
    'left', 'right', 'click', 'stop', 'play', 'record', 'loop', 'cycle',
    'punch', 'in', 'out', 'pre', 'post', 'count-in', 'tap', 'tempo',
    # channel strip
    'solo', 'mute', 'pan', 'gain', 'phase', 'width', 'trim', 'bypass',
    'insert', 'send', 'cue', 'bus', 'aux', 'group', 'fx', 'vca', 'master',
    'input', 'output', 'routing', 'direct', 'channel', 'strip', 'meter',
    # time
    'smpte', 'ltc', 'word', 'clock', 'sync', 'offset', 'frame', 'frames',
    'rate', 'bit', 'bits', 'mono', 'stereo', 'quad', '5.1', '7.1', '22.2',
    # notation
    'bar', 'bars', 'beat', 'beats', 'note', 'notes', 'chord', 'scale', 'clef',
    'rest', 'rests', 'beam', 'beams', 'staff', 'staves', 'system', 'systems',
    'time', 'signature', 'key', 'voices', 'voice', 'stem', 'stems', 'dot',
    'tie', 'slur', 'tuplet', 'grace', 'accidental', 'accidentals', 'ledger',
    # general DAW
    'track', 'tracks', 'clips', 'events', 'parts', 'pool', 'project', 'file',
    'folder', 'preset', 'plugin', 'plug-in', 'vst', 'asio', 'midi', 'automation',
    'quantize', 'snap', 'grid', 'freeze', 'render', 'bounce', 'warp', 'editor',
    'mixconsole', 'inspector', 'zone', 'transport', 'controller', 'surface',
    'marker', 'markers', 'locator', 'locators', 'velocity', 'pitch', 'fader',
    'scale', 'expression', 'articulation', 'voicing', 'tension', 'layout',
    'window', 'panel', 'menu', 'toolbar', 'page', 'dialog', 'view', 'mode',
    'offline', 'online', 'dry', 'wet', 'preview', 'active', 'enable', 'write',
    'read', 'lock', 'unlock', 'link', 'unlink', 'pin', 'group', 'folder',
    'default', 'custom', 'user', 'global', 'local', 'all', 'none', 'only',
    'color', 'colour', 'name', 'type', 'value', 'size', 'length', 'position',
    'start', 'end', 'begin', 'add', 'remove', 'delete', 'insert', 'select',
    'copy', 'paste', 'cut', 'undo', 'redo', 'open', 'close', 'save', 'load',
    'new', 'reset', 'set', 'get', 'edit', 'view', 'zoom', 'scroll', 'print',
    'export', 'import', 'bounce', 'process', 'processing', 'analyze', 'analyse',
    'tool', 'button', 'label', 'icon', 'image', 'text', 'font', 'color',
    # format / standard names
    'wav', 'aiff', 'mxf', 'aaf', 'omf', 'smf', 'mp3', 'flac', 'ogg', 'm4a',
    'adpcm', 'pcm', 'ebur128', 'ebu', 'lufs', 'lu', 'ppm', 'rms', 'true',
    'peak', 'dbtp', 'mid', 'sysex', 'cc', 'nrpn', 'mms', 'mmc', 'midi learn',
    'drum', 'sampler', 'halion', 'serum', 'eq', 'gate', 'comp', 'comppressor',
    'limiter', 'reverb', 'delay', 'chorus', 'distortion', 'filter', 'lowpass',
    'highpass', 'bandpass', 'notch', 'phaser', 'flanger', 'tremolo', 'vibrato',
    # cubase-specific proper names
    'cubase', 'nuendo', 'steinberg', 'vst3', 'aax', 'video', 'audio', 'mse',
    'media', 'com', 'expression', 'score', 'tablature', 'lyrics', 'chords',
}

UNIT = re.compile(r'^(?:%[\.\d]*[a-zA-Z]|\d+([.,]\d+)?\s*'
                   r'(k|m|g)?(b|bit|khz|hz|ms|s|f|px|dB|%|°|frames?)?)$', re.I)
PLACEHOLDER_ONLY = re.compile(r'^[\s%.,\d]*$')

pure_english = [(k, v) for k, v in vi.items()
                if not any(c in VIET for c in v)]

buckets = collections.defaultdict(list)
for k, v in pure_english:
    words = [w for w in re.split(r'[\s/:,\-_+()\[\]]+', v) if w]
    if not words:
        buckets['empty-ish'].append((k, v))
    elif PLACEHOLDER_ONLY.match(v) or UNIT.match(v):
        buckets['numbers/units'].append((k, v))
    elif all(w.lower().strip("'") in BENIGN_SINGLE for w in words):
        buckets['loanwords only'].append((k, v))
    elif len(words) == 1:
        buckets['single word - check'].append((k, v))
    else:
        buckets['MULTI-WORD - check'].append((k, v))

print(f'total strings              : {len(vi)}')
print(f'with Vietnamese            : {len(vi) - len(pure_english)}')
print(f'no Vietnamese at all       : {len(pure_english)}\n')
for name, items in sorted(buckets.items(), key=lambda x: -len(x[1])):
    print(f'  {name:22} {len(items):5}')

if '--list' in sys.argv:
    for name in ('MULTI-WORD - check', 'single word - check'):
        print(f'\n=== {name} ===')
        for k, v in buckets[name]:
            print(f'  {k[:74]!r}')
            print(f'      -> {v[:74]!r}')
