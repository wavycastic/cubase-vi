"""Round 64: the ui domain, read by hand, and the last big two-way split.

MIDI INPUT AND MIDI OUTPUT. Both are LABELS in the map - "MIDI Input" -> "MIDI
Input" and "MIDI Output" -> "Dau ra MIDI" - and the families around them do not
agree on either:

    "MIDI Input"                -> "MIDI Input"          the label, English
    "MIDI Inputs"               -> "Dau vao MIDI"
    "All MIDI Inputs"           -> "Tat ca dau vao MIDI"
    "Activate MIDI Input"       -> "Bat dau vao MIDI"
    "Assign from MIDI Input"    -> "Gan tu dau vao MIDI"
    "Change Pitch of selected Notes via MIDI Input"
                                 -> "... qua dau vao MIDI"
    "Scanning MIDI Inputs"      -> "Dang quet MIDI Input"     English
    "Toggle MIDI Input"         -> "Chuyen doi MIDI Input"    English
    "Select MIDI Input Port"    -> "Chon MIDI Input Port"    English

Eight one way, three the other, and the label settles it. The project rule is
that a name the label prints is the name a sentence uses - which is the same
rule that produced the Add Voice fix in round 53 and the Start fix beside it.
"Chon MIDI Input Port" already follows it; "Bat MIDI Input" did not.

And one of them contradicts round 52 as well:

    "Deactivate External MIDI Inputs" -> "Tat dau vao MIDI ngoai"

Round 52 decided External is a TERM and left it English in six labels, after
fixing seven prose values that had translated it. "ngoai" is outside, which is
the opposite sense, and it is what round 52 was looking for.

PAGE. In the score and print panels "Page" is a real page and eleven keys say
"trang" - but in THIS domain, the window and panel one, the family says "Page"
in twenty keys, and two values here say "trang". Also:

    "User Page"            -> "Trang User"          the odd one
    "Add User Page"        -> "Them User Page"
    "User Page Options"    -> "Tuy chon User Page"

And the two values that show it as the NEXT one rather than naming it, which is
the same defect as "Them so chi nhp hien thi" from round 55 - a sentence that
describes an item instead of naming it, so the reader cannot match it to the
menu entry above it.

    "Show Next Page"       -> "Hien trang ke tiep"   <- not "Page" at all
    "Show Next Meter Page" -> "Hien trang Meter ke tiep"
    "Show Previous Page"   -> "Hien Page lien truoc"   <- does name it

And one from the same read, where a redundant pair reads as a stutter:

    "A Separate Window of the Extension is Open"
      -> "Mot cua so rieng biet cua Extension dang mo"

"Rieng biet" is a single word meaning separate, and "cua so rieng" already says
it.

  python tools/fix_reading64.py
  python tools/fix_reading64.py --write
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

WORDING = {
    # ==================================================================
    # the label says "MIDI Input"; eight values had said "dau vao MIDI"
    # and three had said "MIDI Input"
    # ==================================================================
    'MIDI Input': 'MIDI Input',
    'MIDI Inputs': 'MIDI Input',
    'All MIDI Inputs': 'Tất cả MIDI Input',
    'Activate MIDI Input': 'Bật MIDI Input',
    'Assign from MIDI Input': 'Gán từ MIDI Input',
    'Change Pitch of selected Notes via MIDI Input':
        'Đổi Pitch của các Note đã chọn qua MIDI Input',
    'Deactivate External MIDI Inputs': 'Tắt External MIDI Input',
    'Select MIDI Input Port': 'Chọn Cổng MIDI Input',
    'MIDI Input Port': 'Cổng MIDI Input',
    'MIDI Input Ports': 'Cổng MIDI Input',
    'Note Expression MIDI Input': 'MIDI Input Note Expression',
    'Step/MIDI Input': 'Step/MIDI Input',

    # the same split, the other direction: three values say "dau ra MIDI"
    'MIDI Output': 'MIDI Output',
    'MIDI Outputs': 'MIDI Output',
    'MIDI Output Port': 'Cổng MIDI Output',
    'MIDI Output Ports': 'Cổng MIDI Output',
    'Select MIDI Output': 'Chọn MIDI Output',
    'Select MIDI Output Port': 'Chọn Cổng MIDI Output',

    # ==================================================================
    # in THIS domain Page is English, in twenty keys. Two say "trang".
    # ==================================================================
    'User Page': 'User Page',
    'Meters per Page': 'Số Meter mỗi Page',
    'Number of Cells Per Page :': 'Số ô mỗi Page',

    # ==================================================================
    # a sentence that DESCRIBES an item instead of NAMING it
    # ==================================================================
    'Show Next Page': 'Hiện Page kế tiếp',
    'Show Next Meter Page': 'Hiện Page Meter kế tiếp',

    'A Separate Window of the Extension is Open':
        'Một cửa sổ riêng của Extension đang mở',

    # found by find_quoted_names AFTER the table above was written, which is
    # the tool doing the job it exists for: the sentence quotes the label, and
    # the label had just changed underneath it
    "In 'All MIDI Inputs'": "Trong 'Tất cả MIDI Input'",
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
for k, v in changed.items():
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:76]!r}\n   -> {v[:76]!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changed.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s)')
