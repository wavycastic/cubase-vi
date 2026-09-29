#!/usr/bin/env python3
"""Two defects that make a string hard to read without any obvious error:

  1. untranslated fragment - an English word sitting in a Vietnamese phrase
     where it is not a Cubase term ("Cho ph\u00e1p machine controlled cycle",
     "Activate/Deactivate Write tr\u00ean Play")

  2. term split - the same concept rendered two ways in the same map
     ("Th\u00eam nh\u1ecbp \u0111\u1ed9" vs "Th\u00eam Tempo", "T\u1ea1i Cursor" vs
     "t\u1ea1i v\u1ecb tr\u00ed con tr\u1ecf")

Rule 1 lists only words outside a strict allowlist, so Cubase terminology is
left alone. Rule 2 is a plain two-way search for a known pair.
"""
import json, os, re, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

VIET_CHARS = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
                 'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')
# a Vietnamese syllable ends in a vowel or in a consonant, never two in a row
VI_SYLL = re.compile(
    r'[a-zà-ỹ]+(?:[a-zà-ỹ]*(?=[à-ỹ](?![a-zà-ỹ])))?', re.I)

# Words that are Cubase terms, format names, or standard DAW vocabulary. Kept
# deliberately short: anything not here gets reported for review.
ALLOW = {
    # DAW objects / actions named by Cubase
    'track', 'channel', 'bus', 'fader', 'pan', 'insert', 'send', 'cue', 'solo',
    'mute', 'marker', 'locator', 'automation', 'quantize', 'snap', 'grid',
    'render', 'freeze', 'warp', 'warp', 'tempo', 'timecode', 'bar', 'beat',
    'buffer', 'latency', 'sample', 'rate', 'asio', 'vst', 'plugin', 'plug',
    'preset', 'mixconsole', 'inspector', 'zone', 'transport', 'pool', 'project',
    'clip', 'event', 'part', 'note', 'chord', 'scale', 'velocity', 'pitch',
    'expression', 'controller', 'surface', 'editor', 'score', 'media', 'audio',
    'video', 'instrument', 'midi', 'key', 'command', 'mcc', 'mms', 'sysex',
    'pitchbend', 'aftertouch', 'poly', 'mono', 'omni', 'cc', 'nrpn',
    'arranger', 'play', 'stop', 'record', 'loop', 'cycle', 'punch', 'post',
    'pre', 'fade', 'in', 'out', 'gain', 'phase', 'width', 'trim', 'bypass',
    'delay', 'reverb', 'chorus', 'filter', 'eq', 'comp', 'gate', 'limiter',
    'modulator', 'mapping', 'layout', 'window', 'dialog', 'panel', 'menu',
    'toolbar', 'page', 'tab', 'group', 'folder', 'file', 'name', 'type',
    'value', 'size', 'length', 'position', 'start', 'end', 'mode', 'view',
    'display', 'show', 'hide', 'enable', 'disable', 'activate', 'deactivate',
    'reset', 'apply', 'add', 'remove', 'delete', 'insert', 'select', 'copy',
    'paste', 'save', 'load', 'import', 'export', 'undo', 'redo', 'new', 'old',
    'user', 'global', 'local', 'default', 'custom', 'read', 'write', 'lock',
    'unlock', 'link', 'unlink', 'pin', 'active', 'inactive', 'selected',
    'default', 'window', 'online', 'offline', 'dry', 'wet', 'preview',
    'blocklist', 'whitelist', 'blacklist', 'host', 'wrapper', 'shell',
    'component', 'module', 'bundle', 'package', 'session', 'image', 'data',
    'list', 'box', 'column', 'row', 'field', 'label', 'button', 'check',
    'box', 'option', 'setting', 'settings', 'preference', 'preferences',
    'image', 'disk', 'drive', 'network', 'path', 'directory', 'server',
    'client', 'peer', 'stream', 'sync', 'word', 'clock', 'smpt', 'drop',
    'time', 'code', 'line', 'frame', 'block', 'sample', 'quantum', 'heads',
    'where', 'dither', 'noise', 'shaping', 'gain', 'hiss',
    # formats and standards
    'wav', 'aiff', 'aifc', 'mxf', 'aaf', 'omf', 'smf', 'mp3', 'flac', 'ogg',
    'mpeg', 'dv', 'avi', 'mov', 'bwf', 'adr', 'ebur', 'lufs', 'ppm', 'rms',
    'pcm', 'adpcm', 'dolby', 'atmos', 'mpeg', 'ascii', 'utf', 'csv', 'xml',
    'mac', 'intel', 'windows', 'linux', 'usb', 'rs', 'ltc', 'madi', 'word',
    'smpte', '9pin', 'pin', 'sdk', 'api', 'url', 'http', 'tcp', 'ip', 'id',
    'usb', 'mpe', 'gu', 'gui', 'ui', 'ok', 'esc', 'alt', 'ctrl', 'cmd',
    'shift', 'tab', 'enter', 'rm', 'l', 'r', 'tab',
    # music theory that AGENT.md-adjacent files already agreed on
    'note', 'bar', 'staff', 'stave', 'clef', 'rest', 'beam', 'stem', 'system',
    'signature', 'key', 'barline', 'ledger', 'accidental', 'tuplet', 'grace',
    'slur', 'tie', 'dot', 'voice', 'articulation', 'voicing', 'tension',
    'dynamics', 'tempo', 'cue', 'slash', 'chord',
    # misc words Cubase leaves in English inside a label
    'and', 'or', 'of', 'the', 'to', 'for', 'with', 'on', 'in', 'at', 'by',
    'from', 'as', 'is', 'be', 'not',
}

QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]|\{[^}]*\}')
# Cubase feature names: Capitalised words with no Vietnamese are proper names
PROPER = re.compile(r'^[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*')  # AudioWarp, VST3

fragments = collections.defaultdict(list)
for k, v in vi.items():
    bare = QUOTED.sub(' ', v)
    if not any(c in VIET_CHARS for c in v):
        continue                       # pure label, checked elsewhere
    for w in re.findall(r'\b[A-Za-z][A-Za-z\'-]*\b', bare):
        lw = w.lower().strip("'-")
        if not lw or lw in ALLOW or len(lw) < 2:
            continue
        # a Vietnamese syllable has a vowel; a pure English fragment here is
        # flagged so it can be judged by reading
        fragments[lw].append((k, v))

# ---------------------------------------------------------------- term splits
SPLITS = [
    ('Tempo / nhịp độ', r'\bnhịp độ\b', r'\bTempo\b'),
    ('Cycle / chu kỳ', r'\bchu kỳ\b', r'\bCycle\b'),
    ('Cursor / con trỏ', r'\bcon trỏ\b', r'\bCursor\b'),
    ('Position Marker / Marker vị trí', r'\bMarker vị trí\b',
     r'\bPosition Marker\b'),
    ('Voice / bè', r'\bbè\b', r'\bVoice\b'),
    ('Time Signature / số chỉ nhịp', r'\bsố chỉ nhịp\b', r'\bTime Signature\b'),
    ('Beaming / nối đuôi nốt', r'\bnối đuôi nốt\b', r'\bBeaming\b'),
    ('Playback / phát lại', r'\bphát lại\b', r'\bPlayback\b'),
    ('Recorder / bộ ghi', r'\bbộ ghi\b', r'\bRecorder\b'),
    ('Tempo Track / Track nhịp độ', r'\bTrack nhịp độ\b', r'\bTempo Track\b'),
    ('Chord / hợp âm', r'\bhợp âm\b', r'\bChord\b'),
    ('Staff / khuông nhạc', r'\bkhuông nhạc\b', r'\bStaff\b'),
    ('Rest / dấu lặng', r'\bdấu lặng\b', r'\bRest\b'),
    ('Clef / khóa nhạc', r'\bkhóa nhạc\b', r'\bClef\b'),
    ('Zoom / thu phóng', r'\bthu phóng\b', r'\bZoom\b'),
]

print(f'strings audited : {len(vi)}\n')
print('--- untranslated fragments (English word in a Vietnamese phrase) ---')
tot = 0
for w, items in sorted(fragments.items(), key=lambda x: -len(x[1])):
    tot += len(items)
    print(f'  {w:24} {len(items):4}   e.g. {items[0][1][:70]!r}')
print(f'  {"TOTAL":24} {tot:4}')

print('\n--- term rendered two ways ---')
for name, a, b in SPLITS:
    ca = sum(1 for v in vi.values() if re.search(a, v, re.I))
    cb = sum(1 for v in vi.values() if re.search(b, v, re.I))
    mark = '  SPLIT' if ca and cb else ''
    print(f'  {name:32} {ca:4} / {cb:4}{mark}')

if '--list' in sys.argv:
    print('\n=== fragment detail ===')
    for w, items in sorted(fragments.items(), key=lambda x: -len(x[1]))[:40]:
        print(f'\n  -- {w} ({len(items)}) --')
        for k, v in items[:8]:
            print(f'     {v[:92]!r}')
