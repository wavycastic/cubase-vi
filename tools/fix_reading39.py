#!/usr/bin/env python3
"""Round 39: the long values of the music-theory domain - 100 sentences, and
the first one to find a GLOSSARY row the map itself had drifted away from.

`Chord Symbols` is `hoa bieu` - AGENT.md section 4, settled since round 22.
Seven keys say "Ky hieu hop am":

    Chord Symbol    ->  Ky hieu hop am
    Chord Symbols   ->  Ky hieu hop am
    Show Chord Symbols
                     ->  Hien Chord Symbols
    For Notation and main Chord Symbols
                     ->  Danh cho ky am va ky hieu hop am chinh

This is EXACTLY the bug AGENT.md documents at line 389, one row over. That
entry is about the glossary saying `Key Signature | hoa bieu` when `hoa bieu`
is Chord Symbols - the wrong term got into the rule, the rule spread, and
fixing the instances did not stop it because the wrong word was still in the
file. Here the rule is RIGHT and the map drifted: seven keys picked a second
rendering of the same term, and nobody compared them against the table.

Same sentence, same drift, in the opposite direction - two keys where the
ENGLISH word "key signature" was rendered as "hoa bieu":

    "Accidentals apply only to one note, and are shown on all modified notes;
     naturals are not shown, and notes modified by the key signature do not
     show accidentals."
      -> "... va cac not bien doi theo hoa bieu khong hien dau hoa."

So the wrong term is now in the map from BOTH directions. The lesson sharpens:
when a glossary term turns up in a new string, grep the term, not the key.

THE MUSICAL ERROR. Nine keys in one family, and they are not all the same
thing:

    "Apply major chord with a 7 to selection"
      -> "Ap dung hop am truong cap 7 vao vung chon"

`Hop am truong cap 7` is Cmaj7. "A major chord with a 7" is C plus G - a
dominant seventh, a different chord. The English says the chord is BUILT FROM
a root and then EXTENDED; the Vietnamese names a chord type instead. The same
error in six more:

    "Apply major chord with a major 7"        -> "hop am truong cap 7 truong"
    "Apply major chord with a major 7 and an augmented 5"
                                             -> "hop am truong cap 7 truong va not tang 5"
    "Apply minor chord with a 6"              -> "hop am thu cap 6"
    "Apply minor chord with a 7"              -> "hop am thu cap 7"
    "Apply minor chord with a 7 and a flat 5"-> "hop am thu cap 7 va not giam 5"
    "Apply suspended fourth chord with a 7"  -> "hop am treo cap 4 not 7"

"Chord with a N" is `hop am X voi not N` - the word "voi" is what says the
note is ADDED. Without it the sentence names a different chord.

And `Octave`, which the glossary never had: 25 keys, of which twelve use it
inside a sentence as if it were an English word - "mot octave", "cao hon 1
octave". Vietnamese music says `quang tam`. The labels stay English because
`Octave Line`, `Octave Symbol` and `Octave Indicator` are Cubase names.

  python tools/fix_reading39.py
  python tools/fix_reading39.py --write
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
    # Chord Symbols is "hoa bieu" - the glossary is right, seven keys
    # had drifted to a second rendering
    # ==================================================================
    'Chord Symbol': 'Hóa biểu',
    'Chord Symbols': 'Hóa biểu',
    'Chord Symbols Preset': 'Preset hóa biểu',
    'Custom Chord Symbols': 'Hóa biểu tùy chỉnh',
    'Show Chord Symbols': 'Hiện hóa biểu',
    'For Notation and main Chord Symbols': 'Dành cho ký âm và hóa biểu chính',
    'Adjust the Effective Position of the Chord Symbols':
        'Điều chỉnh vị trí hiệu dụng của hóa biểu',
    'Chord symbols appear either above the staves belonging to specific '
    'instruments as defined in Instrument Settings, or above the top staff '
    'in the system.':
        'Hóa biểu hiện hoặc trên các khuông nhạc thuộc nhạc cụ cụ thể như định '
        'nghĩa trong cài đặt Instrument, hoặc trên khuông nhạc trên cùng của '
        'dòng nhạc.',

    # ==================================================================
    # ... and the wrong term coming in from the other direction
    # ==================================================================
    'Accidentals apply only to one note, and are shown on all modified notes; '
    'naturals are not shown, and notes modified by the key signature do not '
    'show accidentals.':
        'Dấu hóa chỉ áp dụng cho một nốt, và hiện trên tất cả nốt được biến '
        'đổi; dấu bình không hiện, và các nốt bị thay đổi theo số chỉ nhịp '
        'không hiện dấu hóa.',
    'Accidentals apply only to one note, and are shown on all notes, including '
    'unmodified notes (naturals) and notes modified by the key signature.':
        'Dấu hóa chỉ áp dụng cho một nốt, và hiện trên tất cả nốt, bao gồm '
        'nốt không biến đổi (dấu bình) và nốt bị thay đổi theo số chỉ nhịp.',

    # ==================================================================
    # "chord with a N" is a chord BUILT FROM A ROOT and EXTENDED.
    # Naming a chord type instead is a different chord.
    # ==================================================================
    'Apply major chord with a 7 to selection':
        'Áp dụng hợp âm trưởng với nốt 7 vào vùng chọn',
    'Apply major chord with a major 7 to selection':
        'Áp dụng hợp âm trưởng với nốt 7 trưởng vào vùng chọn',
    'Apply major chord with a major 7 and an augmented 5 to selection':
        'Áp dụng hợp âm trưởng với nốt 7 trưởng và nốt tăng 5 vào vùng chọn',
    'Apply minor chord with a 6 to selection':
        'Áp dụng hợp âm thứ với nốt 6 vào vùng chọn',
    'Apply minor chord with a 7 to selection':
        'Áp dụng hợp âm thứ với nốt 7 vào vùng chọn',
    'Apply minor chord with a major 7 to selection':
        'Áp dụng hợp âm thứ với nốt 7 trưởng vào vùng chọn',
    'Insert a major chord with a 7': 'Chèn hợp âm trưởng với nốt 7',
    'Insert a major chord with a major 7': 'Chèn hợp âm trưởng với nốt 7 trưởng',
    'Insert a major chord with a major 7 and an augmented 5':
        'Chèn hợp âm trưởng với nốt 7 trưởng và nốt tăng 5',
    'Insert a minor chord with a 6': 'Chèn hợp âm thứ với nốt 6',
    'Insert a minor chord with a 7': 'Chèn hợp âm thứ với nốt 7',
    'Insert a minor chord with a 7 and a flat 5':
        'Chèn hợp âm thứ với nốt 7 và nốt giáng 5',
    'Insert a minor chord with a major 7':
        'Chèn hợp âm thứ với nốt 7 trưởng',
    'Apply suspended fourth chord with a 7 to selection':
        'Áp dụng hợp âm treo 4 với nốt 7 vào vùng chọn',
    'Apply suspended second chord with a 7 to selection':
        'Áp dụng hợp âm treo 2 với nốt 7 vào vùng chọn',
    'Insert a suspended fourth chord with a 7':
        'Chèn hợp âm treo 4 với nốt 7',
    'Insert a suspended second chord with a 7':
        'Chèn hợp âm treo 2 với nốt 7',

    # ==================================================================
    # Octave is "quang tam" in a sentence; the labels stay English
    # ==================================================================
    'Duplicate the root note (one octave higher)':
        'Nhân bản nốt gốc (cao hơn 1 quãng tám)',
    'Duplicate the tenor (one octave higher)':
        'Nhân bản giọng Tenor (cao hơn 1 quãng tám)',
    'Equal Pitch - all Octaves': 'Cùng Pitch - mọi quãng tám',
    'Equal Pitch - same Octave': 'Cùng Pitch - cùng quãng tám',
    'Move the second and fourth highest notes an octave lower':
        'Chuyển nốt cao thứ hai và thứ tư xuống thấp hơn một quãng tám',
    'Move the second highest note an octave lower':
        'Chuyển nốt cao thứ hai xuống thấp hơn một quãng tám',
    'Move the third highest note an octave lower':
        'Chuyển nốt cao thứ ba xuống thấp hơn một quãng tám',
    'Shift Notes down One Octave': 'Dịch Note xuống một quãng tám',
    'Shift Notes up One Octave': 'Dịch Note lên một quãng tám',
    'Octave Offset': 'Lệch quãng tám',
    'Octave Offset from C3': 'Lệch quãng tám tính từ C3',
    'Octave Offset (Use Left/Right Arrow Keys to modify)':
        'Lệch quãng tám (Dùng phím mũi tên Trái/Phải để chỉnh)',
    'Keep Transpose in Octave Range': 'Giữ Transpose trong Vùng quãng tám',
    'Voicing Range: Octave Offset from C3':
        'Voicing Range: Lệch quãng tám tính từ C3',
    'On the First Occurrence of the Same Note in the Following Bar, Either at '
    'the Same or a Different Octave':
        'Ở lần xuất hiện đầu tiên của cùng nốt đó trong Bar tiếp theo, dù ở '
        'cùng hoặc khác quãng tám',
    'Suppress Cautionary Accidentals at Same Pitch and Octave in Other Voices '
    'on the Same Instrument':
        'Ẩn dấu hóa nhắc lại ở cùng Pitch và quãng tám trong các bè khác trên '
        'cùng nhạc cụ',

    # ==================================================================
    # the notation labels, where a translator had put in commas instead
    # of parentheses
    # ==================================================================
    '1/16 Notes (Semiquavers) in 1/8 Note (Quaver) Denominator Time '
    'Signatures':
        'Nốt 1/16 (nốt móc kép) trong số chỉ nhịp có mẫu số là nốt 1/8 '
        '(nốt móc đơn)',
    '1/32 Notes (Demisemiquavers) in 1/16 Note (Semiquaver) Denominator Time '
    'Signatures':
        'Nốt 1/32 (nốt móc ba) trong số chỉ nhịp có mẫu số là nốt 1/16 '
        '(nốt móc kép)',
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nốt 1/8 (nốt móc đơn) trong số chỉ nhịp có mẫu số là nốt 1/4 '
        '(nốt cường)',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) '
    'Denominator Time Signatures':
        'Nối đuôi nốt 1/8 (nốt móc đơn) trong số chỉ nhịp có mẫu số là nốt 1/4 '
        '(nốt cường)',
    '1/8 Note (Quaver) Beams When Adjacent Tuplet Starts or Ends With an 1/8 '
    'Note':
        'Đuôi nốt 1/8 (nốt móc đơn) khi liên nhịp liền kề bắt đầu hoặc kết thúc '
        'bằng nốt 1/8',

    # ==================================================================
    # small
    # ==================================================================
    'Notes Eligible for a Cautionary Accidental Following an Enharmonically '
    'Equivalent Note':
        'Nốt đủ điều kiện hiện dấu hóa nhắc lại sau một nốt cảm điệu tương đương',
    'Cannot Edit VariAudio: No Note Segments Detected':
        'Không thể sửa VariAudio: không phát hiện đoạn nốt nào',
    'All notes are sent on one channel. Please set up your Note Expression '
    'Input Device correctly.':
        'Tất cả nốt được gửi trên cùng một Channel. Vui lòng thiết lập thiết '
        'bị Note Expression đầu vào chính xác.',
    'As incoming MIDI Channels seem to be rotating, you should consider to '
    'create and use a Note Expression Input Device':
        'Vì các MIDI Channel đầu vào dường như đang luân phiên, bạn nên cân '
        'nhắc tạo và dùng một thiết bị Note Expression đầu vào',
    'If this option is activated, the Score Editor will produce, assuming '
    "'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', "
    'a dotted slash followed by an undotted slash in 5/8, but five slashes in '
    '5/4.':
        'Nếu tùy chọn này được bật và giả định "Maximum Duration for '
        'Rhythmic Slashes" được đặt thành "Note 1/4 (Crotchet)", Score Editor '
        'sẽ tạo ra một gạch chéo có chấm theo sau bởi một gạch chéo không chấm '
        'ở 5/8, nhưng năm gạch chéo ở 5/4.',
    'If this option is activated, the Score Editor will produce, assuming '
    "'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', "
    'two dotted slashes in 6/8, but six undotted slashes in 6/4.':
        'Nếu tùy chọn này được bật và giả định "Maximum Duration for '
        'Rhythmic Slashes" được đặt thành "Note 1/4 (Crotchet)", Score Editor '
        'sẽ tạo ra hai gạch chéo có chấm ở 6/8, nhưng sáu gạch chéo không chấm '
        'ở 6/4.',
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
