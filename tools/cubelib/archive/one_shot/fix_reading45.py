#!/usr/bin/env python3
r"""Round 45: the dropped-clause class gets a detector, and the detector finds
three more instances in strings that were read in rounds 32 to 40.

The class has now appeared by hand seven times, and every time the lost text is
the clause with a CONDITION or a COST in it:

  r32  "... but requires you to estimate the pickup value."
  r38  "This has no effect for bar numbers centered on the bar, which are
        always placed outside dynamics."
  r38  "If this option is set to show a cautionary either with or without
        parentheses, then other cautionary accidentals ... are suppressed."
  r40  "Please note that this conversion might lead to clipping!"
  r44  "However, this also increases the power consumption of the computer.
        If power consumption is a concern, ... Further information ... can be
        found in the Steinberg Knowledge Base."   (3 sentences of 5)
  r45  "For support information, please contact the plug-in vendor."
  r45  "... and use the 'Convert Z-Axis Pan Automation of Selected Tracks'
        function if needed."
  r45  "More recently, some composers have used these clefs as a substitute
        for octave lines."

Seven for seven, the English states the rule and the exception reads as an
aside, so the aside is what gets dropped. That is not a coincidence about this
project and it is worth a check rather than another reading pass.

  tools/find_dropped_sentences.py

Counting sentences is mechanical, so it can be checked. It took three attempts
to get the count honest:

  1. counting a literal \n as a sentence end reported 27 strings short by one,
     because every multi-line value ends with one;
  2. \b[A-Z][a-z]{0,4}\. for abbreviations swallowed the period of any short
     capitalised word - "Track." in "Khong the them Track. So MIDI Track da dat
     gioi han." was removed, and nine complete "Cannot add more tracks"
     messages were reported as losing a sentence;
  3. the keys of long strings are TRUNCATED in all_strings.tsv, so counting
     sentences in the key counts a prefix. The untruncated English exists as
     another row's key - and two rows can share a 60-character prefix, so the
     lookup has to insist on exactly one candidate or fall back.

That is three false-positive waves to get seven true positives, which is the
usual ratio for a detector of this kind and the reason the file says the list
is a lead and not a verdict. What it still misses: strings whose truncated key
prefix collides with a sibling, which is how two of the three were found - by
hand, while checking a detector's output.

  python tools/fix_reading45.py
  python tools/fix_reading45.py --write
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
    # three clauses dropped, all of them the "and if ..." half
    # ==================================================================
    'You are about to reactivate this plug-in at your own risk.\\nThis may '
    'impact the stability of the application and is not recommended.\\n\\nFor '
    'support information, please contact the plug-in vendor.\\n\\nIn the '
    'Plug-in Manager, use "Rescan All" to move reactivated plug-ins back to '
    'the Blocklist.':
        'Bạn sắp kích hoạt lại Plug-in này và tự chịu rủi ro.\\nĐiều này có '
        'thể ảnh hưởng đến độ ổn định của ứng dụng và không được khuyến '
        'nghị.\\n\\nĐể biết thông tin hỗ trợ, vui lòng liên hệ nhà cung cấp '
        'Plug-in.\\n\\nTrong Plug-in Manager, dùng "Quét lại tất cả" để đưa '
        'Plug-in trở lại Blocklist.',
    "Switching '3D Pan Mode' may invalidate existing 'Z-Axis Pan' automation. "
    "Please check your automation tracks and use the 'Convert Z-Axis Pan "
    "Automation of Selected Tracks' function if needed.":
        "Chuyển 'Chế độ Pan 3D' có thể làm mất hiệu lực Automation 'Pan trục "
        "Z' hiện có. Vui lòng kiểm tra các Automation Track và dùng chức năng "
        "'Chuyển đổi Automation Pan trục Z của Track đã chọn' nếu cần.",
    'Clefs with 8 above or below normally indicate that the instrument playing '
    'the music sounds an octave higher (for example, piccolo) or lower (for '
    'example, double bass, or tenor voice) than written. More recently, some '
    'composers have used these clefs as a substitute for octave lines. This '
    'option allows you to choose between the two approaches to '
    'octave-transposing clefs.':
        'Khóa nhạc có số 8 ở trên hoặc dưới thường chỉ định nhạc cụ diễn tấu '
        'cao hơn một quãng tám (như piccolo) hoặc trầm hơn một quãng tám (như '
        'double bass, giọng tenor) so với ký âm. Gần đây, một số nhạc sĩ đã '
        'dùng loại khóa này thay cho vạch quãng tám. Tùy chọn này cho phép bạn '
        'chọn giữa hai cách tiếp cận với khóa chuyển quãng tám.',
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
