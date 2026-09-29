#!/usr/bin/env python3
"""Re-scan translations/vi.json for English leaking into Vietnamese strings.

  python tools/audit_leak.py            # summary
  python tools/audit_leak.py --list     # every hit
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
MAP = os.path.join(ROOT, 'translations', 'vi.json')

src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(MAP, encoding='utf-8'))

# Function words that must never survive inside a Vietnamese clause.
# Deliberately excludes do / so / may / can - those are also real Vietnamese
# words, so flagging them would produce false alarms.
LEAK = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'than',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'does', 'did',
    'you', 'your', 'yours', 'this', 'that', 'these', 'those',
    'there', 'their', 'them', 'they', 'our', 'ours', 'we', 'us',
    'of', 'into', 'from', 'with', 'by', 'about',
    'for', 'in', 'on', 'at', 'to', 'as',
    'what', 'which', 'where', 'when', 'why', 'how',
    'cannot', 'could', 'would', 'should', 'will',
    'not', 'because', 'already',
    'replace', 'delete', 'select', 'remove', 'create',
    'used', 'use', 'want', 'wanted', 'possible', 'happened',
    # quantifiers: wrong inside a Vietnamese clause, fine as a whole label
    'all', 'none', 'only', 'every', 'each',
}

VIET = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị'
           'òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ')

# Standard DAW loanwords that AGENT.md requires us to keep in English, so
# "Fade In", "Punch In", "MIDI In" etc. are correct, not leakage.
LOANWORD = {
    'in', 'out', 'on', 'off', 'to', 'up', 'down', 'over', 'under',
    'fade', 'punch', 'midi', 'audio', 'video', 'track', 'channel', 'bus',
    'insert', 'send', 'cue', 'marker', 'locator', 'automation', 'quantize',
    'snap', 'grid', 'render', 'freeze', 'warp', 'tempo', 'time', 'bar',
    'beat', 'note', 'chord', 'scale', 'key', 'pattern', 'step', 'loop',
    'mix', 'master', 'solo', 'mute', 'editor', 'project', 'pool', 'part',
    'clip', 'event', 'preset', 'plugin', 'vst', 'eq', 'filter', 'link',
    'control', 'set', 'reset', 'move', 'copy', 'paste', 'save', 'load',
    'print', 'zoom', 'view', 'help', 'file', 'folder', 'window', 'menu',
    'panel', 'zone', 'strip', 'layout', 'export', 'import', 'record',
    'play', 'stop', 'close', 'open', 'edit', 'undo', 'redo', 'group',
    'select', 'name', 'type', 'value', 'level', 'size',
    'gain', 'pan', 'meter', 'peak', 'rms', 'true', 'bpm', 'hz',
    # bare label letters: "A/B setting", "Selection A", "Word Clock A"
    'a', 'b',
    # named Cubase edit operations: "Cut, Delete, Draw, and Paste"
    'delete', 'cut', 'draw', 'paste',
}

# English living inside a quoted span is a Cubase feature/file name and stays.
# Only text outside quotes is judged for leakage.
QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]')


def has_viet(s):
    return any(c in VIET for c in s)


def strip_named(s):
    return QUOTED.sub(' ', s)


# quantifiers are legitimate as a standalone label ("All", "None", "Only")
QUANTIFIER = {'all', 'none', 'only', 'every', 'each'}

# Official Cubase/MIDI command names that legitimately contain a quantifier
# and must stay in English verbatim.
NAMED_PHRASE = {
    'Nhạc cụ dùng Automation Read All và Write All',      # Automation Read All / Write All
    'Gửi thông điệp All Notes Off',                       # MIDI All Notes Off
}


def scan():
    out = []
    for k, v in vi.items():
        if not has_viet(v):
            continue
        if v in NAMED_PHRASE:
            continue
        bare = strip_named(v)
        words = [w.strip('.,;:!?()|').lower() for w in bare.split()]
        bad = {w for w in words if w in LEAK and w not in LOANWORD}
        # a lone quantifier is a real label, not leakage
        if len(words) <= 1:
            bad -= QUANTIFIER
        if bad:
            out.append((k, src.get(k, k), v, sorted(bad)))
    return out


hits = scan()

if __name__ == '__main__':
    print(f'strings audited        : {len(vi)}')
    print(f'Vietnamese strings     : {sum(1 for v in vi.values() if has_viet(v))}')
    print(f'English word leakage   : {len(hits)}')

    if hits:
        print()
        if '--list' in sys.argv:
            for i, (k, s, v, bad) in enumerate(hits, 1):
                print(f'[{i:03d}] {k!r}')
                print(f'      vi  : {v!r}')
                print(f'      leak: {bad}')
        else:
            for k, s, v, bad in hits[:12]:
                print(f'  {k!r}')
                print(f'      vi  : {v!r}')
                print(f'      leak: {bad}')
            if len(hits) > 12:
                print(f'  ... and {len(hits) - 12} more (use --list)')

    sys.exit(1 if hits else 0)
