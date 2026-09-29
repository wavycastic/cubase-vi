#!/usr/bin/env python3
"""Round 5 of reading: the mixer, label by label.

read_short.py covers the 9,000 menu labels and button names - the other half
of the map, and the half that had never been read. Every finding below came
from reading them, not from a rule.

The defect classes, largest first:

  1. a modifier left in English around a translated noun, in the numbered
     slot menu: "Insert 1 Edit" -> "Chen 1 Edit". The English "Edit" and
     "Enable" are commands, so the label is "Sua Insert 1" / "Bat Insert 1".
     16 keys, one loop.

  2. plural dropped from the slot groups: "Sends (Post-Fader)" -> "Send
     (Post-Fader)". The singular is a different concept - one send, not the
     send rack. 8 keys.

  3. scrambles where the head noun was put first and then the English verb was
     never translated:
       "Send Destination & Gain"     -> "Gain Send Destination &"
       "Use Default Send Level"      -> "Dung Muc Default Send"
       "Sync Channel Selection with Mixer" -> "Mixer Sync Channel Selection with"
       "Sync Track/Channel Type Filters"   -> "Filter Sync Track/Channel Type"
       "Track Record Arming Routing" -> "Track Ghi Arming Routing"
       "Metronome Click Pan"         -> "Pan Click Metronome"
       "VST Quick Controls"          -> "VST Nhanh Dieu khien"
       "New Insert Effect Bank Zone"  -> "moi Insert Effect Bank Zone"

  4. Cubase's internal bracketed keys, where the text inside the bracket is
     the part that matters and it was left half-done:
       "Direction [direction of a stem]" -> "Direction [direction cua a stem]"
         English, Vietnamese and English in one bracket
       "Link [short, verb]" -> "[short, verb]" never translated
       "Panner [Channel Latency Overview]" -> "Panner [Do tre Channel]"
         the bracket names a different panel than the key does

  5. term drift inside the domain, both directions:
       "MIDI Channel" -> "Kenh MIDI" while every sibling keeps "Channel"
       "VST Sound" -> "VST Am thanh" while "VST Sound Library" keeps English
       "VST Effects" -> "VST Hieu ung" while "Add Effect" keeps "Effect"
       "Group | Channel" -> "Gop nhom | Channel"

  6. one value that is simply wrong: "Audio Connections" -> "Ket noi VST".
     Audio Connections is the panel name and appears in many messages.

  python tools/fix_reading5.py
  python tools/fix_reading5.py --write
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
    # a value that is simply the wrong thing
    # ==================================================================
    'Audio Connections': 'Audio Connections',
    'Center channel': 'Center Channel',
    'VST Quick Controls': 'VST Quick Control',
    'MIDI Channel': 'MIDI Channel',
    'VST Sound': 'VST Sound',
    'VST Effects': 'VST Effects',
    'VST Modulators': 'VST Modulator',
    'VST Instrument Channels': 'VST Instrument Channel',
    'MIDI Send Destination': 'Đích của MIDI Send',
    'VST System Link': 'VST System Link',
    'Merge Mode (VST 3)': 'Chế độ Merge (VST 3)',
    'EQ/Filter Transition: Quick': 'Chuyển tiếp EQ/Filter: Quick',
    'EQ/Filter Transition: Soft': 'Chuyển tiếp EQ/Filter: Soft',
    'EQ/Filter Transition: <Quick>': 'Chuyển tiếp EQ/Filter: <Quick>',
    'EQ/Filter Transition: <Soft>': 'Chuyển tiếp EQ/Filter: <Soft>',

    # ==================================================================
    # scrambles: head noun moved to the front, English verb left behind
    # ==================================================================
    'Send Destination & Gain': 'Đích Send & Gain',
    'Send Destination & Gain (Compact)': 'Đích & Gain Send (Gọn)',
    'Send Destination, Gain & Send Controls':
        'Destination, Gain & Điều khiển Send',
    'Send Initial Value': 'Giá trị khởi tạo của Send',
    'Use Default Send Level': 'Dùng Send Level mặc định',
    'Sync Channel Selection with Mixer':
        'Đồng bộ lựa chọn Channel với Mixer',
    'Sync Selection to Channel/Track Selection':
        'Đồng bộ vùng chọn với lựa chọn Channel/Track',
    'Sync Track/Channel Type Filters':
        'Đồng bộ bộ lọc loại Track/Channel',
    'Track Record Arming Routing':
        'Định tuyến ghi sẵn sàng của Track',
    'Metronome Click Pan': 'Metronome Click Pan',
    'New Insert Effect Bank Zone': 'Tạo Insert Effect Bank Zone mới',
    'VST Channel Load': 'Tải VST Channel',
    'VST Channel Presets': 'VST Channel Preset',
    'VST FX Presets': 'VST FX Preset',
    'VST Instrument Presets': 'VST Instrument Preset',
    'Mixer Bank Channel Setup': 'Thiết lập Channel Mixer Bank',
    'Output Group and Channel Width (MIDI)':
        'Chiều rộng Output Group và Channel (MIDI)',
    'Routing Editor Slot %d - %s': 'Slot %d - %s của Routing Editor',
    'Primary Parameter: Decrease (Channel Level)':
        'Tham số chính: Giảm (Channel Level)',
    'Primary Parameter: Increase (Channel Level)':
        'Tham số chính: Tăng (Channel Level)',
    'Secondary Parameter: Decrease (Pan Left-Right)':
        'Tham số phụ: Giảm (Pan Left-Right)',
    'Secondary Parameter: Increase (Pan Left-Right)':
        'Tham số phụ: Tăng (Pan Left-Right)',
    'Pan Front-Rear': 'Pan Front-Rear',
    'Pan Left-Right': 'Pan Left-Right',
    'Pan Left-Right2': 'Pan Left-Right2',
    'Pan Volume': 'Pan Volume',
    'Reverb Send Effect': 'Reverb Send Effect',
    'Meters: Post Fader': 'Meter: Post Fader',
    'Meters: Pre Fader': 'Meter: Pre Fader',
    'Meters: Post Panner': 'Meter: Post Panner',
    'Move Insert Cursor To Part Start':
        'Di chuyển con trỏ Insert tới đầu Part',
    'Including Channel Settings': 'Cài đặt Channel liên quan',
    'Include Inserts': 'Bao gồm Insert',
    'Level Control (Output Channel)': 'Điều khiển Mức (Output Channel)',
    'Level Display (Output Channel)': 'Hiển thị Mức (Output Channel)',
    'Metering Channel Configuration: <%s>':
        'Cấu hình Metering Channel: <%s>',
    'Insert Event Type': 'Loại Event cần chèn',
    'Insert Length': 'Độ dài chèn',
    'Open/Close Insert Effect Editor': 'Mở/Đóng Insert Effect Editor',
    'Open Editor for Insert Effect': 'Mở Editor cho Insert Effect',
    'Notes and NoteExp VST 3 Tuning Curve':
        'Đường cong Tuning VST 3 cho Note và NoteExp',
    'Naming Scheme - Channel Batch Cycle Marker':
        'Quy tắc đặt tên - Channel Batch Cycle Marker',
    'Naming Scheme - Single Channel Cycle Marker':
        'Quy tắc đặt tên - Single Channel Cycle Marker',
    'Naming Scheme - Channel Batch Arranger Chain':
        'Quy tắc đặt tên - Channel Batch Arranger Chain',
    'Naming Scheme - Single Channel Arranger Chain':
        'Quy tắc đặt tên - Single Channel Arranger Chain',
    'Folders with Group Channel Show Automation':
        'Folder có Group Channel hiện Automation',
    'Listen Send Position': 'Vị trí Listen của Send',
    'Listen to Solo Channels on Center Channel':
        'Nghe các Channel Solo trên Channel Center',
    'Input Routing': 'Input Routing',
    'Output Routing': 'Output Routing',
    'Select Input Routing': 'Chọn Input Routing',
    'Select Output Routing': 'Chọn Output Routing',
    'Routing Target': 'Đích Routing',

    # ==================================================================
    # Cubase's bracketed internal keys - the bracket is the part that
    # matters and it was the part left undone
    # ==================================================================
    'Direction [direction of a stem]':
        'Direction [hướng của thân nốt]',
    'Link [short, verb]': 'Liên kết [ngắn, động từ]',
    'General [Metronom Setup]': 'Chung [Metronom Setup]',
    'Insert [Channel Latency Overview]':
        'Chèn [Tổng quan độ trễ Channel]',
    'Panner [Channel Latency Overview]':
        'Panner [Tổng quan độ trễ Channel]',
    'Strip [Channel Latency Overview]':
        'Strip [Tổng quan độ trễ Channel]',
    'View Mode: Fill View[Score View Option]':
        'View Mode: Fill View[Score View Option]',
    '[Mixer Track Number]': '[Số Track MixConsole]',

    # ==================================================================
    # "to X" became "vao X", or the verb stayed English
    # ==================================================================
    'Merge Mono to Multi-Channel': 'Gộp Mono thành Multi-Channel',
    'Split Multi-Channel to Mono': 'Tách Multi-Channel thành Mono',
    'Mono to Multi-Channel...': 'Chuyển Mono sang Multi-Channel...',
    'Multi-Channel to Mono...': 'Chuyển Multi-Channel sang Mono...',
    'Enable Talkback to Cue Channel': 'Bật Talkback tới Cue Channel',
    'Reset Cue Send to "%s"': 'Đặt lại Cue Send thành "%s"',
    'Set "%s" as Default Input Bus': 'Đặt "%s" làm Input Bus mặc định',
    'Send log files to Steinberg': 'Gửi file log cho Steinberg',
    'Send update for permission changes':
        'Gửi thông báo khi quyền thay đổi',
    'Send Controller': 'Gửi Controller',
    'Record Destination on conflict': 'Ghi vào đích khi xung đột',
    'Warn on Channel Configuration Change':
        'Cảnh báo khi cấu hình Channel thay đổi',
    'insert position': 'Vị trí chèn',
    'Select multi-channel input mode': 'Chọn chế độ Multi-Channel Input',
    'Select multi-out instrument return channel':
        'Chọn Return Channel của Instrument multi-out',
    'Skipping multi-channel track...': 'Đang bỏ qua Track đa kênh...',
    'No selected Channel!': 'Chưa chọn Channel!',
    'No more send slots available.': 'Không còn ô Send trống.',
    'Invalid Channel Count!': 'Số Channel không hợp lệ!',

    # ==================================================================
    # a word translated as the wrong word
    # ==================================================================
    # "dai" is a range; EQ Band is a band of the filter
    'Invert EQ Band %d': 'Đảo ngược EQ Band %d',
    'Invert EQ Settings': 'Đảo ngược cài đặt EQ',
    # phones is the Cubase channel name, not the Vietnamese word for headphone
    'Use Phones Channel as Preview Channel':
        'Dùng Phones Channel làm Preview Channel',
    'Phones': 'Phones',
    'CR Phones': 'CR Phones',
    'Show Color for Selected Channel':
        'Hiện màu cho Channel đã chọn',
    'Total Channel Latency': 'Tổng độ trễ Channel',
    'MIDI Remote Controller': 'MIDI Remote Controller',
    'Player Remote Control': 'Player Remote Control',
    'Pad Remote Control': 'Pad Remote Control',
    'Post-Fader Send.\\nClick to move to pre-fader position.':
        'Send Post-Fader.\\nNhấp để chuyển tới vị trí Pre-Fader.',

    # ==================================================================
    # capitalisation and word order drift against a sibling key
    # ==================================================================
    'Copy Channel Settings': 'Sao chép cài đặt Channel',
    'Paste Channel Settings': 'Dán cài đặt Channel',
    'Reduce Channel Width': 'Giảm chiều rộng Channel',
    'Set Insert Length': 'Đặt độ dài Insert',
    'Are you sure you want to reset all VST?':
        'Bạn có chắc muốn đặt lại tất cả VST không?',
    'Are you sure you want to reset this Channel?':
        'Bạn có chắc muốn đặt lại Channel này không?',
    'Are you sure you want to reset this EQ?':
        'Bạn có chắc muốn đặt lại EQ này không?',
    'Expand: Routing': 'Mở rộng: Routing',
    'Hide: All Channel Types': 'Ẩn: mọi loại Channel',
    'Show: All Channel Types': 'Hiện: mọi loại Channel',
    'Views: Routing': 'Chế độ xem: Routing',
    'Views: Channel Strip': 'Chế độ xem: Channel Strip',
    'Views: Direct Routing': 'Chế độ xem: Direct Routing',
    'Open/Close Direct Routing Section': 'Mở/Đóng phần Direct Routing',
    'Open/Close Fader Section': 'Mở/Đóng phần Fader',
    'Open/Close MIDI Fader Section': 'Mở/Đóng phần MIDI Fader',
    'Open/Close Routing Section': 'Mở/Đóng phần Routing',
    'Open/Close Send Effect Editor': 'Mở/Đóng Send Effect Editor',
    'Open/Close Surround Pan Section': 'Mở/Đóng phần Surround Pan',
    'Open Channel Latency Overview': 'Mở Tổng quan độ trễ Channel',
    'Channel Visibility Agents': 'Agent hiển thị Channel',
    'Channel Visibility Configurations': 'Cấu hình hiển thị Channel',
    'Channel Colors': 'Màu Channel',
    'Channel/Category': 'Channel/Danh mục',
    'Bypass: Channel Strip': 'Bypass: Channel Strip',
    'CC: Pan': 'CC: Pan',
    'Channel "%s" - Panner': 'Channel "%s" - Panner',
    'Group Channel': 'Group Channel',
    'Group | Channel': 'Group | Channel',
    'Go to Previous MixConsole Channel': 'Tới Channel MixConsole liền trước',
    'Go to Last Edited Channel': 'Tới Channel sửa lần cuối',
    'Insert Bars': 'Chèn Bar',
    'Insert Notes': 'Chèn Note',
    'Convert Program List To VST Presets':
        'Chuyển danh sách Program sang VST Preset',
    'Convert XML Presets To VST Presets':
        'Chuyển XML Preset sang VST Preset',
    'Locate VST Sound Library: %s': 'Định vị thư viện VST Sound: %s',
    'Pinned window follows VST channel selection':
        'Cửa sổ ghim bám theo lựa chọn VST Channel',
    'Track & MixConsole Channel Colors': 'Màu Channel của Track & MixConsole',
    'MixConsole Channel Strip Colors': 'Màu Channel Strip của MixConsole',
    'MixConsole Fader Colors': 'Màu Fader của MixConsole',
    'Show/Hide VST Quick Controls': 'Hiện/Ẩn VST Quick Control',
    'Show/Hide all VST Quick Controls': 'Hiện/Ẩn mọi VST Quick Control',
    'Show VST Quick Controls for One Slot Only':
        'Chỉ hiện VST Quick Control cho một Slot',
    'Set Remote-Control Focus for VST Quick Controls':
        'Đặt Remote-Control Focus cho VST Quick Control',
    'Set Remote-Control Focus for VST Quick Controls to Next Instrument':
        'Đặt tiêu điểm điều khiển từ xa cho VST Quick Control tới '
        'Instrument kế tiếp',
    'Set Remote-Control Focus for VST Quick Controls to Previous Instrument':
        'Đặt tiêu điểm điều khiển từ xa cho VST Quick Control tới '
        'Instrument liền trước',
    'Remote-Control Focus for VST Quick Controls follows track selection':
        'Remote-Control Focus cho VST Quick Control bám theo lựa chọn Track',
}

# ---------------------------------------------------------------------- #
# families
# ---------------------------------------------------------------------- #

# "Insert 1 Edit" -> "Sua Insert 1". Edit and Enable are commands in the
# numbered slot menu, so they cannot stay English after the noun moves.
SLOT_CMD = {'edit': 'Sửa {noun} {n}', 'enable': 'Bật {noun} {n}'}
for _k in list(src):
    m = re.fullmatch(r'(Insert|Send) (\d+) (Edit|Enable)', _k)
    if m:
        WORDING[_k] = SLOT_CMD[m.group(3).lower()].format(
            noun=m.group(1), n=m.group(2))

# "Sends (Post-Fader)" -> "Send (Post-Fader)". The singular names one send,
# the plural names the rack, so the plural has to survive.
PLURAL_SLOTS = {
    'Cues (Post-Fader)': 'Cues (Post-Fader)',
    'Cues  (Post-Fader)': 'Cues  (Post-Fader)',
    'Cues (Pre-Fader)': 'Cues (Pre-Fader)',
    'Sends (Post-Fader)': 'Sends (Post-Fader)',
    'Sends (Pre-Fader)': 'Sends (Pre-Fader)',
    'Inserts (Control Room)': 'Inserts (Control Room)',
    'Inserts (Post-Fader)': 'Inserts (Post-Fader)',
    'Inserts (Pre-Fader)': 'Inserts (Pre-Fader)',
    'All Cues (Selected Channels)': 'Tất cả Cues (Channel đã chọn)',
    'Send Slots': 'Send Slots',
}
for _k, _v in PLURAL_SLOTS.items():
    if _k in src:
        WORDING[_k] = _v

# Cubase writes the type name in lower case inside these two messages, but
# every other key capitalises Effect, Instrument and Modulator.
VST_LOWER = re.compile(r'%d VST (effect|instrument|modulator)')
for _k, _v in list(vi.items()):
    if VST_LOWER.search(_v) and _k in src:
        WORDING[_k] = VST_LOWER.sub(
            lambda m: '%d VST ' + m.group(1).capitalize(), _v)

# ---------------------------------------------------------------------- #

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
