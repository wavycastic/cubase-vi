#!/usr/bin/env python3
"""Round 48: make every quoted name match the label it names.

41 values quote a feature name that does not read the way its own label reads.
The rule, which took four rounds to state properly:

    a quoted name must match what the LABEL is translated to

Not "quoted names stay English" - that was the wrong first version. In a
localised Cubase the menu shows the localised name, so quoting the English is
just as wrong as quoting a Vietnamese string the menu does not contain.

    'Part Editing Mode'  -> label is "Che do sua Part", so the quote is
                            'Che do sua Part'. Already right; do not touch.
    'Z-Axis Pan'         -> no label by that name; the parameter is called
                            Z-Axis Pan in the automation lane in every
                            language. English is right; do not touch.

The class is mechanical once the rule is stated, so this script proposes the
replacement from the label's own translation rather than from a hand-written
table - which is the point. Forty-one hand-written entries would be forty-one
fresh chances to be wrong about a name, and the table would encode a second
copy of the glossary, which is how `Key Signature | hoa bieu` happened.

Three of the findings are not quote faults at all - they are LABELS with the
English still in them, which the tool surfaced because it looks labels up:

    "Hide Key Signatures" -> "An Key Signatures"
    "Hook Only"           -> "Chi Hook"
    "Search for File"     -> "Search cho File"

Those are in a small hand-written table below, because "make it match the label"
is circular when the label is the thing that is wrong.

  python tools/fix_quoted_names.py
  python tools/fix_quoted_names.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
PH = re.compile(r'%(?:(?:\.\d+)?[a-zA-Z%]|l)')

# --- labels that still carry their English, which the tool found by looking
# --- them up while chasing a quote. Circular to fix automatically.
LABELS = {
    'Hide Key Signatures': 'Ẩn số chỉ nhịp',      # sibling "Hide Clefs" is
    'Hook Only': 'Chỉ Móc',                       # "An khoa nhac"
    'Search for File': 'Tìm kiếm File',
}

HAN = re.compile(r'[Ā-ỿ]')
Q = re.compile(r"'([^'\\]{3,60})'|\"([^\"\\]{3,60})\"")


def clean(s):
    return s.replace('\\', '').strip()


# Names that stay English inside a quote even though their label is
# Vietnamese. `Record Enable` is one: the sentence is
#     Activate "Record Enable" or "Monitor" of MIDI or Instrument Tracks
# and the label is "Bat ghi", so the rule would give
#     Bat "Bat ghi" hoac "Monitor"
# which says "enable enable-record". `Monitor`, quoted in the same sentence and
# kept English in forty-eight labels, is the other: these are channel-strip
# BUTTON names, and a button is named by what is printed on it.
BUTTONS = {'Record Enable', 'Monitor', 'Solo', 'Monitor Level', 'Read', 'Write',
           'Any', 'or'}

changed = dict(LABELS)


def fix_quotes(vi_map):
    out = {}
    for k, v in vi_map.items():
        en = src.get(k, '')
        if not en:
            continue
        a = {clean(m.group(1) or m.group(2)) for m in Q.finditer(en)}
        if not a:
            continue
        new = v
        for name in a:
            if name == 'or' or len(name) < 4 or name in BUTTONS:
                continue
            label = vi_map.get(name, src.get(name, None))
            if label is None:
                continue
            want = clean(label)
            if not HAN.search(want) or want == name:
                continue      # the label is English too: nothing to match
            if want in new:
                continue      # already quoted as the label translates
            # replace the quoted name, whichever quote character it used
            for q in ("'", '"'):
                if f'{q}{name}{q}' in new:
                    new = new.replace(f'{q}{name}{q}', f'{q}{want}{q}')
            if new != v:
                out[k] = new
    return out


# the note-value labels use commas; the sentences use parentheses. Same
# parenthesised form as round 36 gave the sentences, so the quotes match.
NOTE_LABELS = {}
for _en, _vi in (('1/8 Note (Quaver)', 'Note 1/8 (nốt móc đơn)'),
                ('1/16 Note (Semiquaver)', 'Note 1/16 (nốt móc kép)'),
                ('1/32 Note (Demisemiquaver)', 'Note 1/32 (nốt móc ba)'),
                ('1/2 Note (Minim)', 'Note 1/2 (nốt bán)'),
                ('1/4 Note (Crotchet)', 'Note 1/4 (nốt cường)')):
    if _en in src:
        NOTE_LABELS[_en] = _vi

changed.update(NOTE_LABELS)

# Four the lookup cannot reach: two quotes where the Vietnamese drifted from the
# label in a way no pattern catches, one half-quoted name, and one button that
# IS localised and so has to follow its label. Round 40 had put 'Save' back to
# English on the grounds that a button label is a proper noun - true of
# "Record Enable", which is printed in English on the channel strip, and not
# true of Save, which Cubase renders as "Luu".
EXTRA = {
    '"Assign to First Unassigned Pad": No Unassigned Pads':
        '"Gán vào Pad chưa gán đầu tiên": Không có Pad chưa gán nào',
    'Pedal lines always show some text or symbol at the start of subsequent '
    'systems, unless the \'Hook Only\' appearance is chosen for the start of '
    'the line. This option determines whether or not the text or symbol that '
    'appears should be in parentheses.':
        "Đường pedal luôn hiện văn bản hoặc ký hiệu ở đầu các dòng nhạc tiếp "
        "theo, trừ khi chọn 'Chỉ Móc' cho đầu dòng. Tùy chọn này xác định ký hiệu "
        'có nằm trong ngoặc hay không.',
    'Resets "Slice audio events at hitpoints"':
        'Đặt lại "Cắt lát Audio Event tại Hitpoint"',
    'This specifies the maximum duration the Score Editor will produce for a '
    'rhythmic slash, without considering rhythm dots, and applies in all time '
    'signatures. For example, if you choose \'1/4 Note (Crotchet)\', the Score '
    'Editor will create four slashes in 2/2, and two dottet slashes in 6/8.':
        'Tùy chọn này xác định thời lượng tối đa mà Score Editor sẽ tạo cho một '
        'dấu gạch chéo nhịp, không tính các dấu chấm dôi, và áp dụng cho mọi số '
        "chỉ nhịp. Ví dụ, nếu bạn chọn 'Note 1/4 (nốt cường)', Score Editor sẽ tạo "
        'bốn gạch trong 2/2 và hai gạch có chấm trong 6/8.',
    'To save the project as is, click \'Save\'. Note that the project will no '
    'longer be compatible with program versions older than 13.0.30.':
        "Để lưu Project như hiện tại, nhấp 'Lưu'. Lưu ý rằng Project sẽ không còn "
        'tương thích với các phiên bản chương trình cũ hơn 13.0.30.',
}
changed.update({k: v for k, v in EXTRA.items() if k in src})

# Two passes: the quotes have to be matched against the labels as they will be
# AFTER this round, or the five note-value labels move and the three sentences
# that quote them keep the old form.
stage = dict(vi)
stage.update(changed)
changed.update(fix_quotes(stage))

# The English quotes only half the name - "'1/4' Note (Crotchet)'" - so the
# lookup cannot see it, and round 39 had already written the half-quote as
# "Note 1/4 (Crotchet)". It has to follow the label like any other quote.
for _k, _v in list(changed.items()):
    if '"Note 1/4 (Crotchet)"' in _v:
        changed[_k] = _v.replace('"Note 1/4 (Crotchet)"',
                                 '"Note 1/4 (nốt cường)"')
    elif '"Note 1/4 (nốt cường)"' not in _v and vi.get(_k, '').find(
            '"Note 1/4 (Crotchet)"') >= 0:
        changed[_k] = vi[_k].replace('"Note 1/4 (Crotchet)"',
                                     '"Note 1/4 (nốt cường)"')

real = {k: v for k, v in changed.items() if k in src}
missing = sorted(set(changed) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '�' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

diff = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'keys considered    : {len(real)}')
print(f'total to change    : {len(diff)}')
print()
for k, v in diff.items():
    print(f'  {k[:60]!r}')
    print(f'      {vi.get(k, "")[:110]!r}')
    print(f'   -> {v[:110]!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in diff.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s)')
