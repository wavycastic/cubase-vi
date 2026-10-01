#!/usr/bin/env python3
"""Round 36: the "English frame" class, found by measurement instead of by eye.

Rounds 33 and 34 hit this three times by reading `general`. Then a Latin/Han
ratio sweep (tools/find_thin_vietnamese.py) turned up a dozen more, all of
them notation strings - the one domain whose long values had never been read.
The pattern is always the same:

    "Notes for Which Accidentals Have Already Been Stated Within the Bar"
      -> "Notes cho Which Accidentals Have Already Been Stated Within the Bar"
    "Primary type is used for the main chord symbol"
      -> "Primary type is used cho the main chord symbol"
    "First channel that is used for channel rotation"
      -> "First channel that is used cho channel rotation"
    "Shift the detected beat positions by half a beat"
      -> "Shift the detected beat positions theo half a beat"

The English sentence is standing there intact. A Vietnamese preposition was
put exactly where the English preposition was, and the string was filed as
done. Nothing is mistranslated - nothing is translated.

Four words, Vietnamese preposition, whole clause left in English:

    "Press up to 5 keys to assign remote keys to subsections"
      -> "Press up vao 5 keys vao Gan remote keys vao subsections"

Four "vao" in one line. This is the same defect as "Ban can join" from round
31 and "Click 'Start' vao scan cho unreferenced files" from round 33, and it
is the largest class still in the map.

NO DETECTOR COULD SEE IT, and the reason is worth writing down:
  - audit_leak counts English words, but the ratio test fails because the
    sentence HAS Vietnamese;
  - audit_quality's "fully untranslated prose" needs a sentence with no
    Vietnamese at all;
  - a human reading 6,834 short labels does not read 499 long ones.

So two new tools, both in this commit:

  tools/find_english_frame.py - a value carrying four or more consecutive
      English words that appear verbatim in its own source was annotated, not
      translated. Four is the threshold because DAW terms make runs of two
      and three common and harmless.
  tools/find_thin_vietnamese.py - the ratio sweep that found the class.

Both are lead generators. Which of the 142 hits are wrong is still a reading
job, and roughly half of them are quoted feature names that are CORRECT.

Alongside the frames, four more reversals and a family of "X Y in Z" labels
where X and Y are reversed:

    "Primary Parameter: Fine Decrease (Channel Level)"
      -> "Parameter: Fine Decrease (Channel Level) chinh"
    "Arbitrary Range Start Time in Primary Time Format"
      -> "Thoi gian Arbitrary Range Start trong Primary Time Format"

and three sentences that lost a word outright:

    "The following troubleshooting options are available:"
      -> "following troubleshooting options are available:"
    "The ASIO Sample Rate has changed:"
      -> "ASIO Sample Rate has changed:"
    "This project contains no MIDI track!"
      -> "project contains no MIDI track! nay"

  python tools/fix_reading36.py
  python tools/fix_reading36.py --write
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
    # the English frame, clause by clause
    # ==================================================================
    'Input/Output routing and MIDI channel are set up correctly for playing':
        'Input/Output routing và MIDI channel đã được thiết lập đúng để phát',
    'Notes for Which Accidentals Have Already Been Stated Within the Bar':
        'Các nốt mà dấu hóa đã được ghi trong Bar',
    'Notes That Subdivide Compound Beats, and Fill the Beat':
        'Các nốt phân chia nhịp phức và lấp đầy phách',
    'Notes at a Different Octave Within the Same Bar':
        'Các nốt ở quãng tám khác trong cùng Bar',
    'Notes at a Different Octave in the Following Bar':
        'Các nốt ở quãng tám khác trong Bar kế tiếp',
    'Notes at the Same Octave in the Following Bar':
        'Các nốt ở cùng quãng tám trong Bar kế tiếp',
    'Trills Where Upper Note Is Altered by Accidental Present in Key '
    'Signature':
        'Trill khi nốt trên bị thay đổi bởi dấu hóa có trong số chỉ nhịp',
    'First channel that is used for channel rotation':
        'Channel đầu tiên được dùng để xoay vòng Channel',
    'No compatible audio stream found in file:\\n':
        'Không tìm thấy audio stream tương thích trong file:\\n',
    'Shift the detected beat positions by half a beat':
        'Dịch các vị trí phách đã phát hiện nửa phách',
    'System Link is required for precise time alignment':
        'Cần có System Link để căn thời gian chính xác',
    'Primary type is used for the main chord symbol':
        'Loại chính được dùng cho hóa biểu chính',
    'Overdub Note Expression data in existing notes':
        'Ghi đè dữ liệu Note Expression vào các nốt đã có',
    'Sync Selection in Project Window and MixConsole':
        'Đồng bộ vùng chọn giữa Project Window và MixConsole',
    "Measure Effect's Loop Delay for Delay Compensation":
        "Đo Loop Delay của Effect để bù trễ",
    'Tap Tempo - Please keep tapping to set tempo':
        'Tap Tempo - Vui lòng tiếp tục gõ để đặt tempo',
    'Press up to 5 keys to assign remote keys to subsections':
        'Nhấn tối đa 5 phím để gán phím từ xa cho các phần con',
    'Show Cautionary Accidentals in Parentheses':
        'Hiện dấu hóa nhắc lại trong ngoặc',
    'Send machine control commads to selected SyncStation port':
        'Gửi lệnh machine control tới cổng SyncStation đã chọn',
    'Remaining Number of Beats defined in Audio File':
        'Số phách còn lại được xác định trong File Audio',
    'Double-Click opens Note Expression Editor':
        'Mở Note Expression Editor bằng nhấp đúp',
    'Double-Click opens Note Expression Editor On/Off':
        'Bật/tắt mở Note Expression Editor bằng nhấp đúp',
    "'Edit Solo'/'Record in MIDI Editors' follow Focus":
        "'Edit Solo'/'Record trong MIDI Editor' bám theo Focus",
    'Failed to parse VST Parameters Structure:\\n\\n%s\\nContext: %s':
        'Không phân tích được cấu trúc VST Parameters:\\n\\n%s\\nContext: %s',
    'Show File Extensions in Results List':
        'Hiện phần mở rộng File trong Danh sách kết quả',
    'Map Input Bus Metering to Audio Track (in Direct Monitoring)':
        'Gán Metering của Input Bus sang Audio Track (trong Direct Monitoring)',

    # ==================================================================
    # a word dropped
    # ==================================================================
    'The following troubleshooting options are available:':
        'Các tùy chọn khắc phục sự cố sau đây khả dụng:',
    'The ASIO Sample Rate has changed:': 'ASIO Sample Rate đã thay đổi:',
    'This project contains no MIDI track!': 'Project này không chứa MIDI Track nào!',
    'MIDI Send Group and Channel': 'MIDI Send Group và Channel',

    # ==================================================================
    # reversed
    # ==================================================================
    'Steinberg Master Track Xml File': 'File Xml Steinberg Master Track',
    'VariAudio - Show MIDI Reference Track': 'VariAudio - Hiện MIDI Reference Track',
    'Primary Parameter: Fine Decrease (Channel Level)':
        'Tham số chính: Fine Decrease (Mức Channel)',
    'Primary Parameter: Fine Increase (Channel Level)':
        'Tham số chính: Fine Increase (Mức Channel)',
    'Secondary Parameter: Fine Decrease (Pan Left-Right)':
        'Tham số phụ: Fine Decrease (Pan Trái-Phải)',
    'Secondary Parameter: Fine Increase (Pan Left-Right)':
        'Tham số phụ: Fine Increase (Pan Trái-Phải)',
    'Do you really want to remove the insert effect bank zone (%s)?':
        'Bạn có thực sự muốn gỡ bỏ Insert Effect Bank Zone (%s) không?',

    # ==================================================================
    # "X Y in Z" labels where X and Y are reversed
    # ==================================================================
    'Arbitrary Range Start Time in Primary Time Format':
        'Thời gian bắt đầu Range tùy ý trong Primary Time Format',
    'Arbitrary Range End Time in Primary Time Format':
        'Thời gian cuối Range tùy ý trong Primary Time Format',
    'New Range End Position in Selected Time Format':
        'Vị trí cuối Range mới trong Selected Time Format',
    'Range Start Position in Selected Time Format':
        'Vị trí đầu Range trong Selected Time Format',
    'Range End Position in Selected Time Format':
        'Vị trí cuối Range trong Selected Time Format',
    'New Range Length in Selected Time Format':
        'Độ dài Range mới trong Selected Time Format',

    # ==================================================================
    # small ones the sweep turned up
    # ==================================================================
    '- %i multichannel track(s) split to mono':
        '- %i Track đa kênh đã tách thành mono',
    'Creating new audio stream in video file':
        'Đang tạo audio stream mới trong file Video',
    'Type of New Controller Events: Toggle Step/Ramp':
        'Loại Event Controller mới: Bật/tắt Step/Ramp',
    'Pitchbend: Snap Pitchbend Events On/Off':
        'Pitchbend: Bật/tắt Snap Pitchbend Event',
    'Drum Editor: Show Note Length On/Off':
        'Drum Editor: Bật/tắt hiện độ dài nốt',
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
