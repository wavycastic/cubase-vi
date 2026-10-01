#!/usr/bin/env python3
"""Round 51: the project domain, the last of the eight. 30 sentences, and the
shortest round in the project - which is itself the finding.

Fifty-one rounds of reading have produced batches of 200, 143, 54, 40, 30, 19,
15, 4. This one is 8. Every other domain needed dozens of corrections; this one
needed almost none. The reason is visible in the strings: the project domain is
dominated by short, formulaic sentences about permissions and networks, which
have few words to get wrong, and by strings that were already correct because
they were never touched by a bad pass.

That is worth knowing. It means the remaining risk in the map is NOT spread
evenly, and the domains worth re-reading are the ones with long prose - the
media, notation and general tooltips - not the dialog confirmations.

Five fixes, and three of them are the standing classes:

    "Add selected Users to Permission Preset"
      -> "Them nguoi dung da chon vao Preset Permission"
    "Remove selected Users from the User Pool"     (round 42)
      -> "Go bo cac User da chon khoi User Pool"

`nguoi dung` is in thirty-nine keys, `User` in one. Round 42 moved that one
key the wrong way - it read the key in front of it, which said "User Pool", and
copied. This is the mirror image of the mistake rounds 41 and 50 caught in the
other direction, and the reason the rule is "grep the WORD", never "match the
neighbour".

    "This option uses the preferences currently saved in the program."
      -> "Tuy chon nay dung cac thiet lap dang duoc luu trong chuong trinh."

`thiet lap` against `tuy chon` in thirty-five keys, in the same paragraph as two
sentences that say `tuy chon`. Preferences is one word with two Vietnamese
renderings and the domain has both.

And two readings that a detector cannot see because nothing is wrong with the
shape of the sentence:

    "Network address invalid or ambiguous."
      -> "Dia chi mang khong hop le hoac khong xac dinh."

"khong xac dinh" is UNDETERMINED. An address that is ambiguous is one that
matches more than one machine - which is exactly why Cubase asks you to pick an
interface. The message says the address could not be determined, which is a
different fault and the wrong instruction to follow.

    "Progress of active network transfers:"
      -> "Tien trinh cac lan truyen qua mang dang chay:"

"Tien trinh" is the progress, so "Tien trinh ... dang chay" says the progress is
running. It is the TRANSFERS that are active.

  python tools/fix_reading51.py
  python tools/fix_reading51.py --write
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
    # "nguoi dung" in thirty-nine keys, "User" in one - and round 42 is
    # what put it there
    # ==================================================================
    'Remove selected Users from the User Pool':
        'Gỡ bỏ những người dùng đã chọn khỏi User Pool',
    'Remove selected Users from Permission Preset':
        'Gỡ bỏ những người dùng đã chọn khỏi Preset Permission',
    'Script Archive has been imported, but included user mappings had to be '
    'skipped due to an error.':
        'Kho lưu trữ Script đã được import, nhưng các Mapping người dùng bị bỏ '
        'qua do có lỗi.',

    # ==================================================================
    # preferences is "tuy chon" in thirty-five keys
    # ==================================================================
    'This option uses the preferences currently stored in the program.':
        'Tùy chọn này dùng các tùy chọn hiện đang được lưu trong chương trình.',

    # ==================================================================
    # ambiguous means more than one machine matches, which is why Cubase
    # asks you to pick an interface - "khong xac dinh" is a different
    # fault and the wrong instruction to follow
    # ==================================================================
    'Network address invalid or ambiguous.':
        'Địa chỉ mạng không hợp lệ hoặc không rõ ràng.',

    # ==================================================================
    # it is the transfers that are active, not the progress
    # ==================================================================
    'Progress of active network transfers:':
        'Tiến trình các lần truyền mạng đang hoạt động:',
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
       or '�' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v!r}')

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
