#!/usr/bin/env python3
"""Round 27 of reading: the M-N block, the first gap.

I claimed in round 26's message that general was read end to end. It was not -
I had skipped the slices at 3060, 3160, 3260 and 3360 while working through
the alphabet, and then written "read end to end" in the commit. Four hundred
labels, of which this round read the first three hundred.

  python tools/fix_reading27.py
  python tools/fix_reading27.py --write
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
    # English with a Vietnamese preposition wedged into it
    # ==================================================================
    'MIDI Learn available for this control':
        'MIDI Learn khả dụng cho Control này',
    'Merge recorded data into existing parts.':
        'Gộp dữ liệu đã ghi vào các Part hiện có.',
    'MIDI Out port for MIDI Machine Control data':
        'Cổng MIDI Out cho dữ liệu MIDI Machine Control',
    'MIDI Max. Feedback in ms': 'Feedback tối đa của MIDI tính bằng ms',
    'MIDI Remote: Pick for Mapping': 'MIDI Remote: Chọn để Mapping',
    'Machine position follows mouse edits': 'Vị trí máy bám theo chỉnh sửa chuột',
    'MIDI Modifiers (Not for Add-ons)': 'MIDI Modifier (không dùng cho Add-on)',

    # ==================================================================
    # "Modifier" was rendered three ways inside one family
    # ==================================================================
    'MIDI Modifiers': 'MIDI Modifier',
    'MIDI Modifiers Active': 'MIDI Modifier đang bật',
    'MIDI Modifiers Bypass': 'Bypass MIDI Modifier',
    'MIDI Modifiers Bypass on/off': 'Bật/Tắt Bypass MIDI Modifier',
    'MIDI Modifiers On/Off': 'Bật/Tắt MIDI Modifier',
    'Modifiers': 'Các Modifier',
    'Meters\' Fallback': 'Dự phòng của Meter',

    # ==================================================================
    # "MIDI Message" said "MIDI Thong bao" in two keys, "MIDI Message" in
    # three, and "thong diep" in two more
    # ==================================================================
    'MIDI Message': 'MIDI Message',
    'MIDI Messages': 'MIDI Message',
    'MIDI Message Bytes': 'Byte của MIDI Message',
    'MIDI Message Name': 'Tên MIDI Message',
    'MIDI Message or Input Movement':
        'MIDI Message hoặc chuyển động đầu vào',

    # ==================================================================
    # reversed
    # ==================================================================
    'Make Unique Name': 'Tạo tên duy nhất',
    'Make unique name': 'Tạo tên duy nhất',
    'Measure Loudness': 'Đo Loudness',
    'Meter Select': 'Chọn Meter',
    'Meter Count': 'Số Meter',
    'MIDI Step Input': 'Đầu vào Step MIDI',
    'MIDI Step Input (Suspended)': 'Đầu vào Step MIDI (Tạm dừng)',
    'MIDI Output Port': 'Cổng đầu ra MIDI',
    'MIDI Output Ports': 'Cổng đầu ra MIDI',
    'MIDI SysEx Editor': 'Trình sửa MIDI SysEx',
    'MIDI Timecode Destinations': 'Đích đến MIDI Timecode',
    'MIDI Timecode Follows Project Time':
        'MIDI Timecode bám theo thời gian Project',
    'MIDI Timecode Source': 'Nguồn MIDI Timecode',
    'MMC Device ID': 'ID thiết bị MMC',
    'MMC Input': 'Đầu vào MMC',
    'MMC Output': 'Đầu ra MMC',
    'MTC Input': 'Đầu vào MTC',
    'Monitor Select: 1': 'Monitor: Chọn 1',
    'Monitor Select: 2': 'Monitor: Chọn 2',
    'Monitor Select: 3': 'Monitor: Chọn 3',
    'Monitor Select: 4': 'Monitor: Chọn 4',
    'Monitor Sources': 'Nguồn Monitor',
    'Mixer Bank Zone': 'Mixer Bank Zone',
    'Mixer Presets': 'Preset của Mixer',
    'More Tracks': 'Thêm Track',
    'Modulation Depth': 'Độ sâu Modulation',
    'Modify All Pad Voicings': 'Sửa Voicing của tất cả Pad',
    'Modify All Pad Tensions': 'Sửa Tension của tất cả Pad',
    'Modify Volume Curve': 'Sửa đường cong âm lượng',
    'Modify Signature': 'Sửa số chỉ nhịp',
    'Modify project offset': 'Sửa độ lệch của Project',

    # ==================================================================
    # "Machine Control" said "Dieu khien Machine" in one key and
    # "Machine Control" in six
    # ==================================================================
    'Machine Control': 'Machine Control',
    'Machine Control Destination': 'Đích của Machine Control',
    'MixConsole Lower Zone': 'Lower Zone của MixConsole',
    'MixConsole Section Colors': 'Màu các phần của MixConsole',
    'MixConsole Snapshot Recall Settings':
        'Cài đặt gọi lại Snapshot của MixConsole',
    'MixConsole Snapshot Recall Settings...':
        'Cài đặt gọi lại Snapshot của MixConsole...',
    'MixConsole Snapshots': 'Các Snapshot của MixConsole',
    'MixConsole Snapshots Functions': 'Chức năng Snapshot của MixConsole',
    'Mix Monitor Signal with Playback Signal':
        'Trộn tín hiệu Monitor với tín hiệu Playback',

    # ==================================================================
    # untranslated
    # ==================================================================
    'Manual Adjust': 'Điều chỉnh thủ công',
    'Mapped Ports': 'Các cổng đã ánh xạ',
    'Maximum Duration for Rhythmic Slashes':
        'Thời lượng tối đa cho dấu gạch chéo nhịp',
    'Maximum Peak Level in dBFS': 'Mức đỉnh tối đa tính bằng dBFS',
    'Maximum Undo Steps': 'Số bước Undo tối đa',
    'Maximum Number of Auto Save Files': 'Số file tự động lưu tối đa',
    'Maximum Backup Files': 'Số file Backup tối đa',
    'Minimum Distance from Other Objects':
        'Khoảng cách tối thiểu từ đối tượng khác',
    'Minimum Gaps': 'Khoảng trống tối thiểu',
    'Minimum Time Closed': 'Thời gian đóng tối thiểu',
    'Minimum Time Open': 'Thời gian mở tối thiểu',
    'Missing attributes...': 'Thiếu thuộc tính...',
    'More information...': 'Thêm thông tin...',
    'More Options': 'Thêm tùy chọn',
    'More Tensions': 'Thêm Tension',
    'More Tensions ([ALT] - mouse wheel on pad)':
        'Thêm Tension ([ALT] - cuộn chuột trên pad)',
    'Move Range': 'Di chuyển vùng',
    'Move Signature': 'Di chuyển số chỉ nhịp',
    'Move MIDI Controllers': 'Di chuyển MIDI Controller',
    'MSB Control Nr': 'Số Control MSB',
    'Matching Scales': 'Scale khớp',
    'Make Direct Offline Processing Permanent':
        'Chuyển Direct Offline Processing thành vĩnh viễn',

    # ==================================================================
    # "Max. X" and "Min. X" where the bound had drifted away from the
    # thing it bounds
    # ==================================================================
    'Max. RMS All Channels': 'RMS tối đa mọi Channel',
    'Max. Sample Value': 'Giá trị Sample tối đa',
    'Max. Step Length': 'Độ dài Step tối đa',
    'Max. True Peak Level': 'Mức True Peak tối đa',
    'Max. Value': 'Giá trị tối đa',
    'Min. Sample Value': 'Giá trị Sample tối thiểu',
    'Min. Step Length': 'Độ dài Step tối thiểu',
    'Min. Value': 'Giá trị tối thiểu',
    'Maximum Peak Level': 'Mức đỉnh tối đa',
    'Maximum Momentary Loudness': 'Loudness Momentary tối đa',
    'Maximum Short-Term Loudness': 'Loudness ngắn hạn tối đa',
    'Minimum Length': 'Độ dài tối thiểu',
    'Minimum Number of Tracks': 'Số Track tối thiểu',
    'Meter Peak Level\\n[Click] to reset': 'Mức đỉnh Meter\\n[Click] để đặt lại',
    'Mixer Bank Shift Left': 'Chuyển Mixer Bank sang trái',
    'Mixer Bank Shift Right': 'Chuyển Mixer Bank sang phải',
    'Moods': 'Mood',
    'Modulators': 'Các Modulator',
    'Modulators/Inserts/EQs/Sends': 'Modulators/Inserts/EQs/Sends',
    'Markers': 'Các Marker',
    'Mappings': 'Các Mapping',
    'Mapping Scopes': 'Các phạm vi Mapping',
    'Monitors': 'Các Monitor',
    'Macros': 'Các Macro',
    'Merge MIDI': 'Gộp MIDI trong Loop',
    'Merge Mono Tracks': 'Gộp các Mono Track',
    'Mixer Channels': 'Các Mixer Channel',
    'MixConsole Channels': 'Các MixConsole Channel',
    'MediaBay Aspects': 'Các MediaBay Aspect',
    'Missing': 'Bị thiếu',
    'Missing Files:': 'Các file bị thiếu:',
    'Missing Plug-ins': 'Các Plug-in bị thiếu',
    'Missing Ports': 'Các cổng bị thiếu',
    'Missing Thumbnail Cache': 'Bị thiếu bộ nhớ đệm Thumbnail',
    'Missing Track Version': 'Bị thiếu Track Version',
    'Move Event/Range to Selected Track':
        'Di chuyển Event/vùng tới Track đã chọn',
    'Move Events': 'Di chuyển các Event',
    'Move Events to Origin': 'Di chuyển Event tới điểm gốc',
    'Move to Group': 'Chuyển tới Group',
    'Middle': 'Ở giữa',
    'Minimum': 'Nhỏ nhất',
    'Meters: Hold Forever': 'Meter: Giữ vĩnh viễn',
    'Meters: Hold Peaks': 'Meter: Giữ đỉnh',
    'Meters: Input': 'Meter: Đầu vào',
    'Meters: Reset': 'Meter: Đặt lại',
    'Meters\' Peak Hold Time': 'Thời gian giữ đỉnh của Meter',
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
