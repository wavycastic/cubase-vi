#!/usr/bin/env python3
"""Round 13 of reading: the A-B block of the general catch-all.

Six slices, 195..860, about 570 labels. Most of it is already good - the
defects are concentrated in four families, and three of them are the same
reversed-noun-phrase shape as AGENT.md section 2, just short enough that the
automated passes did not see them.

  1. "<Noun> <Verb>" where the English is "<Verb> <Noun>":

        "As One Event"        -> "Event As One"
        "As Separate Events"  -> "Event As Separate"
        "As Block Events"     -> "Event As Block"
        "Bank Select"         -> "Bank Chon"
        "Below Selected Track"-> "Track Below Selected"
        "Auto Select Controllers" -> "Controller Auto Select"
        "Border Style"        -> "Duong vien Phong cach"
        "Add Track Instrument..." -> "Them Instrument Track..."
        "Append Chain Name"   -> "Ten Append Chain"

  2. The Bypass family, where one entry in four was scrambled and the
     plural flipped around:

        "Bypass: EQs"       -> "Bypass EQs"          (colon lost)
        "Bypass: Inserts"   -> "Bypass: Insert"
        "Bypass: Modulators"-> "Bypass: Modulator"
        "Bypass: Sends"     -> "Bypass: Send"
        "Bypass: Inserts on Main Mix" -> "Inserts Bypass: tren Main Mix"

  3. Eight BWF labels where the measurement and its bound came apart:

        "BWF Max. Momentary Loudness" -> "Loudness BWF Max. Momentary"
        "BWF Max. True Peak Level"    -> "Muc BWF Max. True Peak"

     which is not just a scramble - "Max" no longer attaches to anything, so
     the label does not say which way the number goes. Two keys each, one
     with and one without the dot after Max, exactly as Cubase ships them.

  4. Wrong senses that read as if they were right:

        "Activate/Deactivate Read for All Tracks"  -> "...ghi doc..."
          "ghi doc" is "write-read"; the Write twin reads "...ghi ghi..." -
          the verb twice. Neither sibling is about writing when it says read.
        "Added tracks of this type are currently not shown."
          -> "Cac Track loai nay vua them hien dang bi an." "vua them" is
          "just added"; the sentence means tracks that were added earlier
          are hidden - a state, not an action.
        "Application Scaling" -> "Ti le ung dung". A scale is a ratio;
          scaling the interface is zooming it. Same error as the one fixed
          on "User Interface Scaling".
        "Add String Above" -> "Them day phia tren". String is Cubase's MIDI
          String here, not a guitar string - the same fix as "From String".
        "Adjust Fades to Range" -> "Can Fade theo vung". "Can" is align; the
          verb is adjust.

  And about thirty labels left half in English next to a translated sibling:
  "Add Signature", "Add Length", "Add Path", "Add Property", "Add Title",
  "Add Direction", "Add Internet Connection", "Add Displayed Key Signature",
  "Appearance of ... Arpeggios", "All Messages", "All Types: (", "Bring To
  Front", "Byte Position 1/2" (their 0 and 3 are translated), and three that
  contradict a decision made elsewhere: "Add Effect" and "Add External Effect"
  render Effect as "hieu ung" while every other Effect key keeps it, and
  "Bypass Effect" does the same.

  python tools/fix_reading13.py
  python tools/fix_reading13.py --write
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
    # reversed: "<Noun> <Verb>" for an English "<Verb> <Noun>"
    # ==================================================================
    'As One Event': 'Thành một Event',
    'As Separate Events': 'Thành các Event riêng biệt',
    'As Block Events': 'Thành Block Event',
    'Bank Select': 'Chọn Bank',
    'Below Selected Track': 'Track bên dưới Track đã chọn',
    'Auto Select Controllers': 'Tự động chọn Controller',
    'Border Style': 'Kiểu đường viền',
    'Add Track Instrument...': 'Thêm Track Instrument...',
    'Append Chain Name': 'Nối thêm tên Chain',
    'Average CC Value': 'Giá trị CC trung bình',
    'Bottom of Track List': 'Cuối danh sách Track',
    'Apply Project Logical Preset': 'Áp dụng Logical Preset cho Project',
    'Apply Project Logical Presets':
        'Áp dụng các Logical Preset cho Project',
    'Automation Return Time': 'Thời gian Return Automation',

    # ==================================================================
    # the Bypass: family - keep the colon and the English plural
    # ==================================================================
    'Bypass: EQs': 'Bypass: EQs',
    'Bypass: Inserts': 'Bypass: Inserts',
    'Bypass: Modulators': 'Bypass: Modulators',
    'Bypass: Sends': 'Bypass: Sends',
    'Bypass: Inserts on Main Mix': 'Bypass: Inserts trên Main Mix',
    'Bypass: EQs on Main Mix': 'Bypass: EQs trên Main Mix',
    'Bypass Modulators of All Visible Channels':
        'Bypass Modulator của tất cả Channel đang hiện',

    # ==================================================================
    # BWF: the measurement and its bound had come apart, so "Max" was
    # floating in the middle attached to nothing
    # ==================================================================
    'BWF Max. Momentary Loudness': 'Loudness Momentary tối đa của BWF',
    'BWF Max Momentary Loudness': 'Loudness Momentary tối đa của BWF',
    'BWF Max. Short-term Loudness': 'Loudness Short-term tối đa của BWF',
    'BWF Max Short-term Loudness': 'Loudness Short-term tối đa của BWF',
    'BWF Max. True Peak Level': 'Mức True Peak tối đa của BWF',
    'BWF Max True Peak Level': 'Mức True Peak tối đa của BWF',

    # ==================================================================
    # wrong senses
    # ==================================================================
    'Activate/Deactivate Read for All Tracks':
        'Bật/Tắt đọc cho tất cả Track',
    'Activate/Deactivate Write for All Tracks':
        'Bật/Tắt ghi cho tất cả Track',
    'Activate/Deactivate Write for All Tracks: Is Writing':
        'Bật/Tắt ghi cho tất cả Track: Đang ghi',
    'Added tracks of this type are currently not shown.':
        'Các Track đã thêm loại này hiện đang không hiển thị.',
    'Application Scaling': 'Thu phóng ứng dụng',
    'Add String Above': 'Thêm String phía trên',
    'Adjust Fades to Range': 'Điều chỉnh Fade theo vùng',
    'Bass to Lowest Voice': 'Bass sang bè thấp nhất',
    'Beats in Original Length': 'Số phách theo độ dài gốc',
    'Beaming: Reset Beaming': 'Nối đuôi nốt: Đặt lại nối đuôi nốt',
    'Between Locators': 'Ở giữa hai Locator',
    'Automation Pass': 'Lượt Automation',
    'Apply MIDI Velocity Variance': 'Áp dụng phân tán Velocity MIDI',
    'Append Selected In Arranger Chain':
        'Thêm mục đã chọn vào Arranger Chain',
    'Add Selected as Database Slaves':
        'Thêm mục đã chọn làm Database Slave',
    'Add Selected Effect "%s" to Favorites':
        'Thêm Effect đã chọn "%s" vào Favorites',
    'Add MediaBay Aspect': 'Thêm MediaBay Aspect',
    'Adaptive Voicings': 'Adaptive Voicings',
    'Alternative Key Sets': 'Các bộ Key Set thay thế',
    'Activate Punch In': 'Bật Punch In',
    'Activate Punch Out': 'Bật Punch Out',
    # "can" is align; the English verb is adjust
    'Bars+Beats Linear': 'Bar+Nhịp tuyến tính',
    'Bypass Function Learn Mode': 'Bypass chế độ Learn MIDI Function',
    'Bypass Effect': 'Bypass Effect',
    'Add Effect': 'Thêm Effect',
    'Add External Effect': 'Thêm Effect ngoài',
    'Black Keys': 'Phím đen',
    'Background Color Modulation': 'Modulation màu nền',
    'Bring To Front': 'Đưa lên trước',
    'Basic Colors': 'Màu cơ bản',
    'BroadCast Wave Options': 'Tùy chọn Broadcast Wave',
    'Appearance of Down Arpeggios': 'Hình dạng của Arpeggio đi xuống',
    'Appearance of Up Arpeggios': 'Hình dạng của Arpeggio đi lên',
    'Audition Sound Reference': 'Nghe thử Sound Reference',
    'Add Selection as Sound Reference':
        'Thêm vùng chọn làm Sound Reference',
    'Audition Click Sounds': 'Nghe thử âm thanh Click',

    # ==================================================================
    # left in English next to a translated sibling
    # ==================================================================
    'Add New Signature...': 'Thêm số chỉ nhịp mới...',
    'Add Signature': 'Thêm số chỉ nhịp',
    'Add Displayed Key Signature': 'Thêm Key Signature hiển thị',
    'Add Length': 'Thêm độ dài',
    'Add Path': 'Thêm đường dẫn',
    'Add Property': 'Thêm thuộc tính',
    'Add Processes': 'Thêm Process',
    'Add Title': 'Thêm tiêu đề',
    'Add Direction': 'Thêm hướng',
    'Add Internet Connection': 'Thêm kết nối Internet',
    'All Messages': 'Tất cả thông điệp',
    'All Types: (': 'Tất cả loại: (',
    'Apply voice-leading rules automatically':
        'Tự động áp dụng các quy tắc voice-leading',
    'Applying Normalization to Loudness Ref...':
        'Đang áp dụng Normalization cho Loudness Ref...',
    'As Recommended by Instrument': 'Theo khuyến nghị của Instrument',
    'Are you sure you want to activate all cue sends?':
        'Bạn có chắc muốn bật tất cả Cue Send không?',
    'Are you sure you want to remove "%s" ?':
        'Bạn có chắc muốn gỡ bỏ "%s" không?',
    'Byte Position 1': 'Vị trí byte 1',
    'Byte Position 2': 'Vị trí byte 2',

    # ==================================================================
    # "Auto <verb>": the map is two-thirds "<term> tu dong"
    # (Auto Crossfades, Auto Join, Auto LFO, Automatic Scales) against three
    # that put the adverb first
    # ==================================================================
    'Auto Apply': 'Áp dụng tự động',
    'Auto Save': 'Lưu tự động',
    'Auto Save Interval': 'Khoảng thời gian lưu tự động',
    'Auto Select': 'Chọn tự động',
    'Autoscroll': 'Cuộn tự động',

    # ==================================================================
    # case and agreement
    # ==================================================================
    'Add Down': 'Thêm xuống',
    'Add Up': 'Thêm lên',
    'Add Left': 'Thêm sang trái',
    'Add Right': 'Thêm sang phải',
    'Add Plug-in': 'Thêm Plug-in',
    'Add Steps': 'Thêm các Step',
    'Add Steps Randomly': 'Thêm các Step ngẫu nhiên',
    'Add "%s" as Monitor Source %d': 'Thêm "%s" làm Monitor Source %d',
    'Articulations & Mutual Exclusion Groups':
        'Articulation & nhóm loại trừ lẫn nhau',
    'Banks': 'Các Bank',
    'Barlines': 'Các vạch nhịp',
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
