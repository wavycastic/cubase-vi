#!/usr/bin/env python3
"""Round 38: the long values of the notation domain - 56 sentences, the only
domain besides `general` whose long values had never been read.

The frame class was found by measurement, in this domain, in round 36. Reading
the rest by hand turns up a different class, one that has now appeared in
every domain and every round since round 32:

THE SECOND SENTENCE DROPPED. Two of fifty-six, both about an exception:

    "This option effectively takes precedence over showing cautionary
     accidentals on notes in the same or different octaves in the following
     bar. If this option is set to show a cautionary either with or without
     parentheses, then other cautionary accidentals that would otherwise
     appear later in the bar are suppressed."
      -> "Tuy chon nay duoc uu tien hon so voi viec hien dau hoa nhac lai tren
         cac not o cung hoac khac octave trong Bar tiep theo."

    "When bar numbers are positioned at barlines, you may prefer dynamics to
     be placed closer to the staff than bar numbers, or vice versa. This has
     no effect for bar numbers centered on the bar, which are always placed
     outside dynamics."
      -> "Khi so Bar duoc dat tai vach nhip, ban co the chon dat sac thai gan
         khuong nhac hon so Bar hoac nguoc lai."

What is lost is the condition. In both, the first sentence states a rule and
the second states when it does NOT apply - and a Cubase user who only sees the
first sentence will set the option and get the wrong result, with nothing in
the tooltip to tell them why.

"Whichever is sooner" is also missing, which is the same class in miniature:

    "Accidentals apply to all notes at the same staff position ... until the
     end of the bar or a change of key, whichever is sooner, and apply to all
     voices belonging to the same track."
      -> "Dau hoa ap dung cho tat ca not o cung vi tri khuong nhac (trong mot
         octave), cho toi het Bar hoac khi doi giong, va ap dung cho tat ca
         be thuoc cung Track."

Three separate losses in one sentence: the "whichever is sooner", and "change
of key" read as "doi giong" - a change of key is "doi so chi nhip", "giong" is
the key of an instrument.

And the "bar offset" pair, where round 35 set "timecode offset" to "do lech
Timecode" but left its two siblings in this domain with "Offset Bar" in English.

  python tools/fix_reading38.py
  python tools/fix_reading38.py --write
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
    # the second sentence dropped - the one with the condition in it
    # ==================================================================
    'This option effectively takes precedence over showing cautionary '
    'accidentals on notes in the same or different octaves in the following '
    'bar. If this option is set to show a cautionary either with or without '
    'parentheses, then other cautionary accidentals that would otherwise '
    'appear later in the bar are suppressed.':
        'Tùy chọn này được ưu tiên hơn so với việc hiện dấu hóa nhắc lại trên '
        'các nốt ở cùng hoặc khác quãng tám trong Bar tiếp theo. Nếu tùy chọn '
        'này được đặt để hiện dấu nhắc lại có hoặc không có ngoặc, thì các dấu '
        'hóa nhắc lại khác vốn sẽ xuất hiện sau đó trong Bar sẽ bị ẩn.',
    'When bar numbers are positioned at barlines, you may prefer dynamics to '
    'be placed closer to the staff than bar numbers, or vice versa. This has '
    'no effect for bar numbers centered on the bar, which are always placed '
    'outside dynamics.':
        'Khi số Bar được đặt tại vạch nhịp, bạn có thể chọn đặt sắc thái gần '
        'khuông nhạc hơn số Bar hoặc ngược lại. Điều này không có tác dụng với '
        'số Bar căn giữa Bar, vốn luôn được đặt bên ngoài sắc thái.',

    # ==================================================================
    # "whichever is sooner", and "change of key"
    # ==================================================================
    'Accidentals apply to all notes at the same staff position (i.e. in one '
    'octave only), until the end of the bar or a change of key, whichever is '
    'sooner, and apply to all voices belonging to the same track.':
        'Dấu hóa áp dụng cho tất cả nốt ở cùng vị trí khuông nhạc (tức là chỉ '
        'trong một quãng tám), cho tới hết Bar hoặc khi đổi số chỉ nhịp, tùy '
        'cái nào đến trước, và áp dụng cho mọi bè thuộc cùng Track.',

    # ==================================================================
    # the bar offset pair, left in English by round 35
    # ==================================================================
    'You have modified the bar offset as well as the timecode offset! Do you '
    'want to keep the project content at its timecode positions or its bar '
    'positions?':
        'Bạn đã sửa đổi cả độ lệch Bar lẫn độ lệch Timecode! Bạn có muốn giữ '
        'nội dung Project tại vị trí Timecode hay vị trí Bar?',
    'You have modified the bar offset! Do you want to keep the project '
    'content at its bar positions?':
        'Bạn đã sửa đổi độ lệch Bar! Bạn có muốn giữ nội dung Project tại vị '
        'trí Bar không?',

    # ==================================================================
    # a word read as another word
    # ==================================================================
    'Number of Lines in Primary Beam Within Secondary Beam Groups':
        'Số nét trong đuôi nốt chính trong các nhóm đuôi nốt phụ',
    'Notation of Short-Long-Short Patterns That Cross the Half-Bar':
        'Ký âm các Pattern ngắn-dài-ngắn vượt qua nửa Bar',
    'After stopping, how many milliseconds before system can be restarted':
        'Sau khi dừng, cần bao nhiêu mili-giây trước khi có thể khởi động lại '
        'hệ thống',

    # ==================================================================
    # word order and missing "to"
    # ==================================================================
    '1/8 Notes (Quavers) in Simple Time Signatures With a Half-Bar':
        'Nốt 1/8 (nốt móc đơn) trong số chỉ nhịp đơn có nửa Bar',
    'Rests Within Groups of 1/8 Notes (Quavers) in Simple Time Signatures '
    'With a Half-Bar':
        'Dấu lặng trong nhóm nốt 1/8 (nốt móc đơn) ở số chỉ nhịp đơn có nửa Bar',
    '... with Systemic Barline if at Start of System':
        '... với vạch nhịp chung nếu ở đầu dòng nhạc',
    'Braced Staff to Braced Staff':
        'Chuyển từ khuông nhạc có ngoặc nhóm sang khuông nhạc có ngoặc nhóm',
    'Braced Staff to Unbraced Staff':
        'Chuyển từ khuông nhạc có ngoặc nhóm sang khuông nhạc không ngoặc nhóm',
    'Staff Group to Staff Group':
        'Chuyển từ nhóm khuông nhạc sang nhóm khuông nhạc',
    'Show Above Top Staff of System':
        'Hiện phía trên khuông nhạc trên cùng của dòng nhạc',
    'Show Bar Number at Start of System for Bar Split Over Break':
        'Hiện số Bar ở đầu dòng nhạc cho Bar bị ngắt giữa chừng',
    'Show Bar Numbers at Time Signature at System Object Positions':
        'Hiện số Bar tại số chỉ nhịp ở các vị trí đối tượng của dòng nhạc',
    'Show Normal Bar Number If Coincident with Start of Multi-Bar Rest '
    'Showing Range':
        'Hiện số Bar bình thường nếu trùng với điểm bắt đầu của dải dấu lặng '
        'nhiều Bar được hiện',
    "Ruler Display Type has been changed to \\'Bar + Beats\\'.  This is "
    'required for Metronome Click Pattern Emphasis.':
        "Kiểu hiển thị thước đo đã đổi thành 'Bar + Beats'.  Điều này là bắt "
        'buộc để làm nổi bật Pattern Click Metronome.',
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
