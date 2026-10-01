#!/usr/bin/env python3
"""Round 6 of reading: the score desk, label by label.

The notation domain is where the two languages meet most often, and it shows.

  1. "System" decided wrongly six times. AGENT.md section 4 is explicit that
     System is a line of music inside the score and the operating system
     everywhere else, and these six are all score keys:

        "System"                -> "He thong"   should be "dong nhac"
        "System Break"          -> "Break he thong"
        "System Exclusive"      -> "Exclusive he thong"
        "Minimum Number of Staves in System" -> "... trong he thong"

  2. "Cross Staff" read as "change staff". Cross in music notation means to
     move a note onto the neighbouring staff so one person can read it, which
     is what the submenu is for: "Cross to Staff Above", "Cross to Staff
     Below". "Doi khuong nhac" says nothing about crossing.

  3. the head noun moved to the front of a label, which is section 2 of
     AGENT.md again but on two-word labels the earlier rules did not reach:

        "Score Direction"      -> "Score Huong"
        "Score Dynamic"        -> "Score Dong luc"
        "Score Editor Operation" -> "Score Editor Thao tac"
        "Pitch Notation"       -> "Pitch Ky am"
        "Pitch Visibility"     -> "Pitch Hien thi"
        "Timecode Staff"       -> "Timecode Khuong nhac"
        "Staff Visibility"     -> "Khuong nhac Hien thi"
        "Flatten: Convert Beat Track" -> "Track Flatten: Convert Beat"

  4. "Staves" left in English inside a Vietnamese sentence, and "khuong" with
     the "nhac" dropped: "Khuong co ngoac sang khuong co ngoac".

  5. Cubase has one key here, "View Mode: Fill View[Score View Option]",
     and the marker was correct in it. Nothing to fix - recorded because the
     same pattern did produce real errors elsewhere.

  6. Notation itself is split down the middle, and the split is defensible
     except that the menu labels went the wrong way:
       running sentence  -> "ky am"      (reads better in Vietnamese prose)
       menu label        -> "Notation"   (the name in the Cubase menu)
     "For Notation" and "Notation and Tablature" are menu labels and were
     translated; "Notation Settings" was not. The sentence keys are left
     alone.

  python tools/fix_reading6.py
  python tools/fix_reading6.py --write
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
    # System = a line of music, not the operating system (AGENT.md 4)
    # ==================================================================
    'System': 'Dòng nhạc',
    'System Break': 'Ngắt dòng nhạc',
    'System Exclusive': 'Dòng nhạc độc quyền',
    'Minimum Number of Staves in System':
        'Số khuông nhạc tối thiểu trên mỗi dòng nhạc',

    # ==================================================================
    # Cross in notation is not "change"
    # ==================================================================
    'Cross Staff': 'Chuyển qua khuông nhạc',
    'Cross Staff: Cross to Staff Above':
        'Chuyển qua khuông nhạc: Chuyển lên khuông trên',
    'Cross Staff: Cross to Staff Below':
        'Chuyển qua khuông nhạc: Chuyển xuống khuông dưới',
    'Cross Staff: Move to Staff Above':
        'Chuyển qua khuông nhạc: Di chuyển lên khuông trên',
    'Cross Staff: Move to Staff Below':
        'Chuyển qua khuông nhạc: Di chuyển xuống khuông dưới',
    'Cross Staff: Reset to Original Staff':
        'Chuyển qua khuông nhạc: Đặt lại về khuông gốc',

    # ==================================================================
    # head noun moved to the front of a label
    # ==================================================================
    'Score Direction': 'Hướng trong Score',
    'Score Dynamic': 'Động lực trong Score',
    'Score Editor Operation': 'Thao tác Score Editor',
    'Pitch Notation': 'Ký âm cao độ',
    'Pitch Visibility': 'Hiển thị Pitch',
    'Timecode Staff': 'Khuông nhạc Timecode',
    'Below Timecode Staff': 'Phía dưới Khuông nhạc Timecode',
    'Timecode Staff to Staff':
        'Chuyển từ Khuông nhạc Timecode sang khuông nhạc',
    'Staff Visibility': 'Hiển thị khuông nhạc',
    'Flatten: Convert Beat Track': 'Flatten: Chuyển Beat Track',

    # ==================================================================
    # "khuong" lost its "nhac", "Staves" stayed English
    # ==================================================================
    'Braced Staff to Braced Staff':
        'Chuyển khuông nhạc có ngoặc sang khuông nhạc có ngoặc',
    'Braced Staff to Unbraced Staff':
        'Chuyển khuông nhạc có ngoặc sang khuông nhạc không ngoặc',
    'Allow Individual Staves of Multi-Staff Instruments to Be Hidden':
        'Cho phép ẩn từng khuông nhạc của nhạc cụ nhiều khuông',
    'When Min. Staves Exceeded': 'Khi vượt quá số khuông nhạc tối thiểu',

    # ==================================================================
    # Notation: menu label keeps the Cubase name, running text says "ky am"
    # ==================================================================
    'For Notation': 'Dành cho Notation',
    'Notation and Tablature': 'Notation và Tablature',
    'Notation Staff to Tablature':
        'Chuyển Khuông nhạc Notation sang Tablature',
    'Notation of Short-Dotted Long Patterns':
        'Notation của Pattern ngắn-có chấm-dài',
    'Notation of Short-Long-Short Patterns':
        'Notation của Pattern ngắn-dài-ngắn',
    'Notation of Short-Long-Short Patterns That Cross the Half-Bar':
        'Notation các Pattern ngắn-dài-ngắn vượt qua nửa Bar',
    'Notation only': 'Chỉ Notation',
    'Full Score': 'Full Score',

    # ==================================================================
    # untranslated or half-translated
    # ==================================================================
    'Centered on Bar': 'Căn giữa trên Bar',
    'Hide in Score': 'Ẩn trong Score',
    'MIDI Events Shown in Score': 'Hiện MIDI Event trong Score',
    "Use System Timestamp for '%s' Inputs":
        "Dùng System Timestamp cho đầu vào '%s'",

    # ==================================================================
    # Beat: "phach" is the majority and the correct music word
    # ==================================================================
    'Beat': 'Phách',
    'Show Beat Count Only': 'Chỉ hiện số phách',

    # ==================================================================
    # capitalisation against a sibling key
    # ==================================================================
    'Change Notation Settings': 'Đổi cài đặt Notation',
    'Open Notation Settings': 'Mở cài đặt Notation',
    'Open Score Settings': 'Mở cài đặt Score',
    'Show Bar Numbers': 'Hiện số Bar',
    'Set Beat Position': 'Đặt vị trí Beat',
    'Use System Setting': 'Dùng cài đặt System',

    # ==================================================================
    # "Nối chung đuôi nốt" reads oddly; the verb goes last in Vietnamese
    # ==================================================================
    'Beam Together': 'Nối đuôi nốt chung',
    'Beaming: Beam Together': 'Nối đuôi nốt: Nối chung',
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
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:64]!r}\n   -> {v!r}')

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
