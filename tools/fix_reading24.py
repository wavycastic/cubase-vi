#!/usr/bin/env python3
"""Round 24 of reading: the S-T block of the general catch-all.

Four slices, 5660..6060, about 400 labels. The headline is a contradiction
that had been sitting in the map the whole time, between two of my own fixes.

STEM IS "THAN NOT", NOT "DUOI NOT". AGENT.md section 4 settles it: Beam is
"duoi not" and Stem is "than not". Round 15 fixed "Flip Stems" to "Lap than not"
and round 18 fixed "Force Stems Down" and round 23 fixed "Slashes (with
stems)". All three correct. And the three plain keys said the opposite:

    "Stem"      -> "Doi not"      ← the tail, which is Beam's word
    "Stem Down" -> "Doi not Xuong"
    "Stem Up"   -> "Doi not Len"

So the map had "than not" in the sentence keys and "doi not" in the noun
keys, for the same musical object. When I fixed three of the five I never
listed the family. This is the concrete cost of that omission, and it is the
clearest argument yet for grepping the pattern rather than the key: the
pattern here is the WORD, not the string.

"Take No." -> "Take Khong", the third "No." read as the negative. Round 19 fixed
"No. of Frets", round 22 fixed "Scene No.", and AGENT.md now has a rule saying
to grep for the pattern. I did not grep. Same mistake, third time.

Then the "Suspend Reading/Writing ..." family - twelve keys, and every one of
them left the verb in English:

    "Suspend Reading Inserts"  -> "Tam dung Reading Inserts"
    "Suspend Writing Volume"   -> "Tam dung Writing Volume"
    "Suspend Reading Others"   -> "Tam dung Reading Others"
    "Suspend Read States On/Off"  -> "Tam dung Read States On/Off"

And "Symbol" and "Sign" both became "Ky hieu", which is the same collision as
"Key Signature" and "Expression" in round 22 - two English words, one
Vietnamese value - except this time the second one was right and the first was
wrong. "Sign" is notation, "ky hieu" is correct. "Symbol" is Cubase's notehead
symbol type, so it keeps English.

Also reverted the "Switch" decision from round 18. I had changed "Left Switch"
to "Switch trai" on the grounds that Switch is a DAW term, then round 22
applied the same reasoning to "Left Switch:" and left "Cong tac trai:" alone in
the key above it. "Cong tac" is the ordinary Vietnamese word for a toggle and
matches "Switches" -> "Cong tac", so that is the form; the four Zone keys now
agree with the two Switch (momentary) keys.

  python tools/fix_reading24.py
  python tools/fix_reading24.py --write
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
    # Stem is "than not" - Beam's word was in the noun keys
    # ==================================================================
    'Stem': 'Thân nốt',
    'Stem Down': 'Thân nốt xuống',
    'Stem Up': 'Thân nốt lên',

    # ==================================================================
    # "No." as Number - third time, and the rule already said to grep
    # ==================================================================
    'Take No.': 'Số Take',
    'Take %d (incomplete)': 'Take %d (chưa hoàn thành)',

    # ==================================================================
    # "Sign" is notation; "Symbol" is Cubase's notehead symbol type
    # ==================================================================
    'Symbol': 'Symbol',
    'Symbols': 'Các Symbol',
    'Symbol Colors': 'Màu Symbol',
    'Sustain Pedal': 'Sustain Pedal',
    'Syncopation': 'Syncopation',

    # ==================================================================
    # the "Suspend Reading/Writing ..." family, verb left in English
    # ==================================================================
    'Suspend Reading Dynamics': 'Tạm dừng đọc Dynamics',
    'Suspend Reading Inserts': 'Tạm dừng đọc Insert',
    'Suspend Reading Mute': 'Tạm dừng đọc trạng thái Mute',
    'Suspend Reading Others': 'Tạm dừng đọc các trạng thái khác',
    'Suspend Reading Sends': 'Tạm dừng đọc Send',
    'Suspend Reading Volume': 'Tạm dừng đọc âm lượng',
    'Suspend Writing Dynamics': 'Tạm dừng ghi Dynamics',
    'Suspend Writing Inserts': 'Tạm dừng ghi Insert',
    'Suspend Writing Mute': 'Tạm dừng ghi trạng thái Mute',
    'Suspend Writing Others': 'Tạm dừng ghi các trạng thái khác',
    'Suspend Writing Sends': 'Tạm dừng ghi Send',
    'Suspend Writing Volume': 'Tạm dừng ghi âm lượng',
    'Suspend Read States On/Off': 'Bật/Tắt tạm dừng trạng thái đọc',
    'Suspend Write States On/Off': 'Bật/Tắt tạm dừng trạng thái ghi',
    'Suspend All Read/Write Automation':
        'Tạm dừng toàn bộ Đọc/Ghi Automation',
    'Suspend Preview Mode': 'Tạm dừng chế độ Preview',
    'Suspend Preview': 'Tạm dừng Preview',

    # ==================================================================
    # "Switch" back to "Cong tac" - round 18 and 22 disagreed with each
    # other; "Cong tac" is what "Switches" already said
    # ==================================================================
    'Left Switch': 'Công tắc trái',
    'Left Switch:': 'Công tắc trái:',
    'Right Switch': 'Công tắc phải',
    'Right Switch:': 'Công tắc phải:',
    'Lower Switch': 'Công tắc dưới',
    'Lower Switch:': 'Công tắc dưới:',
    'Switches': 'Công tắc',
    'Switch (momentary)': 'Công tắc (tạm thời)',
    'Switch (on/off)': 'Công tắc (bật/tắt)',
    'Switch (one shot)': 'Công tắc (one shot)',
    'Switch: Listen Cancel': 'Chuyển: Hủy Listen',

    # ==================================================================
    # reversed
    # ==================================================================
    'Swing & Offset': 'Swing & Offset',
    'Switch Presets/Hide Track Pictures':
        'Chuyển Preset/Ẩn hình ảnh Track',
    'Step Input': 'Đầu vào Step',
    'Step Lane Inspector': 'Step Lane Inspector',
    'Step Resolution': 'Độ phân giải Step',
    'Step Selection': 'Chọn Step',
    'Split Tool': 'Công cụ tách',
    'Strip Effects': 'Hiệu ứng của Strip',
    'Strip Presets': 'Preset của Strip',
    'Stretch Controller Data': 'Dữ liệu Controller co giãn',
    'Stretch Automation Data': 'Dữ liệu Automation co giãn',
    'Talkback Input Gain': 'Gain đầu vào Talkback',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Stop Updating Results': 'Dừng cập nhật kết quả',
    'Stop playback while winding': 'Dừng phát khi tua',
    'Store Color Set as Default': 'Lưu bảng màu làm mặc định',
    'Store Selected Items Only': 'Chỉ lưu các mục đã chọn',
    'Store as Defaults': 'Lưu làm mặc định',
    'Stream size of zero': 'Kích thước Stream bằng 0',
    'Start License Activation': 'Bắt đầu kích hoạt License',
    'Start Local and Slaves in Sync': 'Đồng bộ Local và Slave',
    'Start from Selection Start': 'Bắt đầu từ đầu vùng chọn',
    'Start time:': 'Thời gian bắt đầu:',
    'Start Preview Mode': 'Chế độ Preview bắt đầu',
    'Spacer in Seconds': 'Spacer tính bằng giây',
    'Spike Detection Range': 'Vùng phát hiện gai',
    'Splice Point Offset': 'Độ lệch điểm ghép',
    'Split repeated': 'Tách lặp lại',
    'Split Tied Steps': 'Tách các Step đã nối',
    'Synchronize with Drum Machine': 'Đồng bộ với Drum Machine',
    'String': 'String',
    'Suppress Playback': 'Tắt phát lại',
    'Suppressed Playback': 'Phát lại đã bị tắt',
    'Subtract': 'Trừ',
    'SyncStation ASIO Input': 'Đầu vào ASIO của SyncStation',
    'SyncStation Display Line 2': 'Dòng hiển thị 2 của SyncStation',
    'Tail in ms': 'Tail tính bằng ms',
    'Tags': 'Tag',
    'Tab': 'Tab',
    'Speaker Solo: Top Center': 'Solo loa: Trên chính giữa',
    'Speed Factor': 'Hệ số tốc độ',
    'StartStop': 'StartStop',
    'Status Line': 'Thanh trạng thái',
    'State Buttons': 'Nút trạng thái',
    'Strip Silence': 'Tắt tiếng Strip',
    'Strip Modules': 'Strip Module',
    'Strip Modules (Exclusive)': 'Strip Module (Độc quyền)',
    'Subsections': 'Các Subsection',
    'Surround channels': 'Các Surround Channel',

    # ==================================================================
    # "Split X" plural, and Segment called "doan"
    # ==================================================================
    'Split Channels': 'Tách Channel',
    'Split Files': 'Tách file',
    'Split MIDI Controllers': 'Tách MIDI Controller',
    'Split MIDI Events': 'Tách MIDI Event',
    'Split Steps': 'Tách các Step',
    'Split Segment (press [SHIFT] to glue)':
        'Tách Segment (nhấn [SHIFT] để dán nối)',
    'Spacer between Markers': 'Spacer giữa các Marker',
    'Split Range': 'Tách vùng',
    'Start Count': 'Bắt đầu đếm nhịp',
    'Start Key': 'Key bắt đầu',
    'Start Left': 'Bắt đầu bên trái',
    'Start Right': 'Bắt đầu bên phải',
    'Start Merge': 'Bắt đầu gộp',
    'Start Recording': 'Bắt đầu ghi',
    'Stop Jump Mode': 'Dừng chế độ Jump',
    'Step Amount': 'Lượng Step',
    'Steps': 'Các Step',
    'Switch Presets': 'Chuyển sang Preset',
    'Switch time base between Musical and Linear':
        'Chuyển Timebase giữa Musical và Linear',
    'Sync Selection': 'Đồng bộ vùng chọn',
    'Sync Visibility': 'Đồng bộ hiển thị',
    'Talkback Enabled': 'Talkback đã bật',
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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:62]!r}\n   -> {v!r}')

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
