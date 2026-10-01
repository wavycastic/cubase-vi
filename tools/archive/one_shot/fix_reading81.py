#!/usr/bin/env python3
"""Round 81: the strings that are hard to read, and the ones that are long.

Everything through round 80 hunted for defects that are *wrong*: a leaked
English word, a term rendered two ways, a broken placeholder, a marker on the
screen that should not be there. Those rounds are all clean now. This round
hunts the other kind, which is not wrong so much as tiring to read:

  [LONG]   Vietnamese padding an English label that already fit.
           "Delete overlaps, Close Gaps and Crossfade..." is 41 characters of
           English and was rendered as 50 characters of Vietnamese, and the
           extra words are all glue: "phần", "và tạo", "các". Every one of them
           can go without the reader losing anything.

  [STACK]  A run of six or more content words with no Vietnamese word between
           them. Vietnamese marks case, gender and number with separate
           syllables, so a 7-word English noun phrase expanded word-for-word
           becomes a Vietnamese wall that the eye slides off. This is the
           single most common readability complaint in the map.

  [WORDY]  Filler that a Vietnamese writer would not have written:
           "Nếu ngại tốn điện, hãy tắt..." - "ngại" is a hesitation word that
           does not belong in a dialog. Same for "các mục đang hiện", "tương
           ứng", "bạn có thể cần" where "cần" alone says it.

Nothing here changes what a string means or which Cubase term it names. DAW
vocabulary stays in English per AGENT.md; %-placeholders and the two literal
\newline dialogs are preserved exactly. Only the padding comes off.

  python tools/fix_reading81.py
  python tools/fix_reading81.py --write
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

# --------------------------------------------------------------------------
# [LONG] Padding removed. Left column: what the reader used to have to push
# through. Right column: same meaning, fewer syllables.
# --------------------------------------------------------------------------
SHORTER = {
    # --- Score Editor: "trong số chỉ nhịp có mẫu số là X" is nine words of
    # glue around a denominator that is already a fraction. The English says
    # "in 1/4 Note (Crotchet) Denominator Time Signatures" and Cubase shows
    # the fraction in the dialog, so "mẫu số Note 1/4" carries it.
    '1/16 Notes (Semiquavers) in 1/8 Note (Quaver) Denominator Time Signatures':
        'Nốt 1/16 (nốt móc kép) với mẫu số nốt 1/8 (nốt móc đơn)',
    '1/32 Notes (Demisemiquavers) in 1/16 Note (Semiquaver) Denominator Time '
    'Signatures':
        'Nốt 1/32 (nốt móc ba) với mẫu số nốt 1/16 (nốt móc kép)',
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nốt 1/8 (nốt móc đơn) với mẫu số Note 1/4 (nốt đen)',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) Denominator '
    'Time Signatures':
        'Nối chung đuôi nốt 1/8 với mẫu số Note 1/4 (nốt đen)',
    'Quarter Note (Crotchet) Denominator Time Signatures With Half-Bars':
        'Số chỉ nhịp mẫu số Note 1/4 (nốt đen) kèm nửa Bar',

    # --- "Chuyển từ X sang Y" repeated the noun twice. The arrow is what the
    # English "to" means; the two full phrases were 13 words for 5 of English.
    'Braced Staff to Braced Staff':
        'Chuyển khuông nhạc có ngoặc -> có ngoặc',
    'Braced Staff to Unbraced Staff':
        'Chuyển khuông nhạc có ngoặc -> không ngoặc',
    'Staff Group to Staff Group':
        'Chuyển nhóm khuông nhạc -> nhóm khuông nhạc',

    # --- "Object Selection Tool:" is a 3-word menu prefix, then 2 words of
    # subject. "Công cụ chọn đối tượng: Kích thước..." keeps the prefix and
    # drops the restated verb.
    'Object Selection Tool: Normal Sizing':
        'Công cụ chọn đối tượng: Kích thước thường',
    'Object Selection Tool: Sizing Moves Content':
        'Công cụ chọn đối tượng: Kích thước di chuyển nội dung',
    'Object Selection Tool: Sizing Applies Time Stretch':
        'Công cụ chọn đối tượng: Kích thước áp dụng Time Stretch',

    # --- "các"/"và"/"tạo" glue
    'Delete overlaps, Close Gaps and Crossfade...':
        'Xóa chồng lấn, đóng khoảng trống, Crossfade...',
    'Remove Unavailable Plug-ins from All Collections':
        'Gỡ Plug-in không khả dụng khỏi mọi Collection',
    'Freeze/Unfreeze Selected Tracks (with Current Settings)':
        'Freeze/Bỏ Freeze Track đã chọn (theo cài đặt hiện tại)',
    'Invalid input. MP3 only supports mono and stereo channels.':
        'Dữ liệu vào không hợp lệ. MP3 chỉ hỗ trợ Mono và Stereo.',
    'Shows all defined attributes for the selected results':
        'Hiện thuộc tính đã định nghĩa của kết quả đã chọn',
    'Defines what happens AFTER a linear or cycled recording...':
        'Xác định việc ghi sau khi ghi tuyến tính hoặc ghi Cycle...',
    'Text or Symbol Appearance at Start of Subsequent Systems':
        'Kiểu hiển thị văn bản hoặc ký hiệu đầu dòng nhạc tiếp theo',
    'Automatically Resolve Collisions Between Adjacent Staves and Systems':
        'Tự xử lý chồng lấn giữa khuông nhạc và dòng nhạc cạnh nhau',
    'Set Transparency for Comparison Channel Curve':
        'Đặt độ trong suốt cho đường cong so sánh',
    'Apply Click Pattern to Equal Signatures':
        'Áp dụng Click Pattern cho số chỉ nhịp bằng nhau',
    'Show Above Top Staff of System':
        'Hiện trên khuông nhạc cao nhất của dòng nhạc',
    'All participants active - Response Times: ':
        'Mọi bên đều hoạt động - Thời gian phản hồi: ',

    # --- "Tùy chọn này xác định thời lượng tối đa mà Score Editor sẽ tạo
    # cho một dấu gạch chéo nhịp" - 14 words before the reader learns anything.
    "This specifies the maximum duration the Score Editor will produce for a "
    "rhythmic slash, without considering rhythm dots, and applies in all time "
    "signatures. For example, if you choose '1/4 Note (Crotchet)', the Score "
    "Editor will create four slashes in 2/2, and two dottet slashes in 6/8.":
        "Thời lượng tối đa của một dấu gạch chéo nhịp, không tính dấu chấm "
        "dôi, áp dụng cho mọi số chỉ nhịp.\nChọn 'Note 1/4 (nốt đen)': 2/2 "
        "tạo bốn gạch, 6/8 tạo hai gạch có chấm.",
}

# --------------------------------------------------------------------------
# [WORDY] Filler a Vietnamese writer would not type.
# --------------------------------------------------------------------------
WORDY = {
    'Use this setting for the highest audio processing performance (to play '
    'back many VST Instruments, for example). This leads to increased '
    'ASIO-Guard Latency and memory usage.':
        'Cài đặt này cho hiệu năng Audio cao nhất (ví dụ: phát nhiều VST '
        'Instrument). Tăng độ trễ ASIO-Guard và mức dùng bộ nhớ.',
    'If you have an audio interface with multiple inputs and outputs, you '
    'might need to configure your routing afterwards in the Audio Connections '
    'dialog (Studio menu > Audio Connections).':
        'Nếu Audio Interface có nhiều đầu vào và đầu ra, cần chỉnh lại Routing '
        'trong hộp thoại Audio Connections (menu Studio > Audio Connections).',
    'To ensure that you actually hear audio from %s, please select the driver '
    'of your audio interface from the list below. This is required for correct '
    'routing of playback and recording signals to your audio hardware.':
        'Để nghe được Audio từ %s, chọn Driver của Audio Interface trong danh '
        'sách. Cần chọn đúng để đưa tín hiệu phát và ghi ra thiết bị.',
    'You can change your driver selection and settings at any time in the '
    'Studio Setup dialog (Studio menu > Studio Setup) in the VST Audio System '
    'section.':
        'Đổi Driver và cài đặt bất kỳ lúc nào trong hộp thoại Thiết lập Studio '
        '(menu Studio > Thiết lập Studio), phần VST Audio System.',
    'Compares the value of the %s function to the control value, and '
    'approaches the two values in a smooth way. As soon as the values are '
    'identical, the function follows the control value.':
        'Chức năng %s tiến dần tới giá trị Control cho mượt. Khi hai giá trị '
        'bằng nhau, chức năng bám theo Control.',
    'Picks up on the value of the %s function as soon as the control reaches '
    'that value. This results in smooth value changes, but requires you to '
    'estimate the pickup value.':
        'Chức năng %s nhận giá trị khi Control tới đúng giá trị đó. Giá trị '
        'đổi mượt hơn nhưng phải tự dò điểm bắt đầu.',
    'Use this option if the current control is inverted when compared to the '
    'actual VST parameter':
        'Dùng tùy chọn này nếu Control hiện tại ngược với tham số VST',
    'The plug-in could not be validated and has been moved to the blocklist. '
    'You can reactivate the plug-in, but please note that the operating '
    "system's protection may prevent the plug-in from loading. Please contact "
    'the manufacturer of the plug-in for an updated version.':
        'Plug-in không vượt qua kiểm tra nên vào Blocklist. Bật lại được, nhưng '
        'bảo vệ hệ điều hành có thể chặn Plug-in tải. Liên hệ nhà sản xuất để '
        'lấy bản mới.',
    'This option deletes the preferences of current and older program '
    'installations and initializes the program with factory settings. Please '
    'be aware that all your custom settings will be removed. This operation '
    'cannot be undone.':
        'Xóa Preferences của bản cài đặt hiện tại và các bản cũ, rồi đặt lại '
        'chương trình về cài đặt Factory. Mất toàn bộ cài đặt tùy chỉnh. Không '
        'hoàn tác được.',
    'This option disables your custom preferences and initializes the program '
    'with factory settings. Your preferences are available after restarting '
    'the program.':
        'Tạm tắt Preferences tùy chỉnh và đặt lại chương trình về cài đặt '
        'Factory. Preferences dùng lại được sau khi khởi động lại.',
    'You have activated the Steinberg Audio Power Scheme.\\n\\nThe Steinberg '
    'Audio Power Scheme optimizes Windows power handling for best possible '
    'audio performance at\\nlow-latency ASIO settings. However, this also '
    'increases the power consumption of the computer.\\n\\nIf power '
    'consumption is a concern, please disable this option and increase the '
    'buffer size of your audio hardware.\\n\\nFurther information on the '
    'Steinberg Audio Power Scheme can be found in the Steinberg Knowledge '
    'Base.':
        'Bạn đã bật Steinberg Audio Power Scheme.\\n\\nTối ưu điện Windows để '
        'Audio chạy tốt nhất ở\\nASIO độ trễ thấp. Nhưng máy sẽ tốn điện '
        'hơn.\\n\\nNếu không muốn tốn điện, hãy tắt tùy chọn này và tăng '
        'buffer của thiết bị Audio.\\n\\nĐọc thêm trong Steinberg Knowledge '
        'Base.',
    'You are about to reactivate this plug-in at your own risk.\\nThis may '
    'impact the stability of the application and is not recommended.\\n\\nFor '
    'support information, please contact the plug-in vendor.\\n\\nIn the '
    'Plug-in Manager, use "Rescan All" to move reactivated plug-ins back to '
    'the Blocklist.':
        'Bạn sắp kích hoạt lại Plug-in này và tự chịu rủi ro.\\nCó thể ảnh '
        'hưởng tới độ ổn định của ứng dụng, không nên làm.\\n\\nCần hỗ trợ, '
        'liên hệ nhà cung cấp Plug-in.\\n\\nTrong Plug-in Manager, dùng "Quét '
        'lại tất cả" để đưa Plug-in trở lại Blocklist.',
    'The selection contains audio material that is processed with the "Solo" '
    'algorithm.\\nBefore exporting a Clip Package, you need to change the '
    'algorithm or use the Bounce Selection\\ncommand on the Audio menu for '
    'the following events:':
        'Vùng chọn có đoạn Audio đang dùng thuật toán "Solo".\\nTrước khi '
        'Export gói Clip, đổi thuật toán hoặc dùng lệnh Bounce Selection\\n'
        'trong menu Audio cho các Event sau:',
    'To identify yourself in the network, you need a unique user name.\\nThis '
    'is usually supplied by the network administrator.\\nDo you want to enter '
    'the user name now?':
        'Cần tên người dùng duy nhất để nhận diện trong mạng.\\nThường do quản '
        'trị mạng cấp.\\nNhập tên người dùng ngay bây giờ không?',
    'The volume database being unmounted could contain database entries that '
    "are shown in the Results list.\\nWould you like to import all database "
    "entries from drive '%s' into your local MediaBay database?":
        "Ổ đĩa đang ngắt kết nối có thể chứa mục đang hiện trong danh sách "
        "kết quả.\\nBạn có muốn Import mọi mục từ ổ đĩa '%s' vào MediaBay trên "
        'máy này không?',
    'The volume database being removed could contain database entries that are '
    "shown in the Results list.\\nWould you like to import all database "
    "entries from drive '%s' into your local MediaBay database?":
        "Ổ đĩa đang gỡ có thể chứa mục đang hiện trong danh sách kết quả.\\n"
        "Bạn có muốn Import mọi mục từ ổ đĩa '%s' vào MediaBay trên máy này "
        'không?',
    'No controller surface available. Enter the mandatory information, click '
    "OK, and create a surface in the 'MIDI Controller Surface Editor'.":
        "Không có Controller Surface khả dụng. Nhập thông tin bắt buộc, nhấp OK, "
        "rồi tạo Surface trong 'MIDI Controller Surface Editor'.",
    'In general, the voice in which notes appear does not influence the '
    'appearance of cautionary accidentals. However, for complex music on '
    'instruments with multiple staves, you may prefer to allow cautionary '
    'accidentals to appear for notes at the same pich and octave in other '
    'voices.':
        'Nhìn chung, bè chứa nốt không ảnh hưởng tới dấu hóa nhắc lại. Tuy '
        'nhiên, với nhạc phức tạp trên nhạc cụ nhiều khuông, có thể cho dấu '
        'hóa nhắc lại hiện ở các bè khác cho nốt cùng cao độ và quãng tám.',
    'The MIDI Controller Surface contains invalid elements (highlighted in '
    'orange). You can leave the Surface Editor and those elements will be '
    'removed automatically, or you can stay and modify the elements.':
        'MIDI Controller Surface có thành phần không hợp lệ (bôi cam). Thoát '
        'Surface Editor thì chúng tự xóa, hoặc ở lại để sửa.',
}

# --------------------------------------------------------------------------
# [STACK] Doubled and stacked nouns, plus a doubled "bộ".
# --------------------------------------------------------------------------
STACK = {
    # "các nhạc cụ cụ thể" - the plural marker and the adjective collide, and
    # the reader hits "cụ cụ" with no pause. "đã chọn" is what the dialog does.
    "Above Specific Instruments' Staves":
        'Khuông nhạc phía trên nhạc cụ đã chọn',

    # "đã được X" is a passive that adds a syllable and nothing else.
    'Indicates if Hitpoints are calculated': 'Chỉ báo Hitpoint đã tính chưa',
    'Indicates if a grid is defined': 'Chỉ báo Grid đã định nghĩa chưa',
    'Not available, because Drum Map is set': 'Không khả dụng vì đã đặt Drum Map',
    'Parent Object Is Selected': 'Đối tượng cha đã chọn',

    # "nút xoay" is wrong for "the control". In the Modulation Matrix a
    # control is the destination parameter, not a knob; the tooltip talks
    # about a value that is being compared, which no knob does. The map
    # already says "Control" in 243 other keys, so this also removes a split.
    'Compares the value of the %s function to the control value, and '
    'approaches the two values in a smooth way. As soon as the values are '
    'identical, the function follows the control value.':
        'Chức năng %s tiến dần tới giá trị Control cho mượt. Khi hai giá trị '
        'bằng nhau, chức năng bám theo Control.',
    'Picks up on the value of the %s function as soon as the control reaches '
    'that value. This results in smooth value changes, but requires you to '
    'estimate the pickup value.':
        'Chức năng %s nhận giá trị khi Control tới đúng giá trị đó. Giá trị '
        'đổi mượt hơn nhưng phải tự dò điểm bắt đầu.',
    'Sends a new value to the %s function as soon as you move the control. '
    'This can result in abrupt value changes.':
        'Gửi giá trị mới tới chức năng %s khi di chuyển Control. Giá trị có '
        'thể nhảy đột ngột.',
    'Use the control on your hardware to retrieve its MIDI messages.':
        'Dùng Control trên thiết bị để lấy thông điệp MIDI.',
    'Warning: You must define a MIDI message for this control.':
        'Cảnh báo: Bạn phải đặt thông điệp MIDI cho Control này.',
    'Warning: A control with the defined MIDI message already exists. Please '
    'change the MIDI message settings of one of the controls.':
        'Cảnh báo: Đã có Control dùng thông điệp MIDI này. Hãy đổi thông điệp '
        'MIDI của một trong các Control.',
    'by touching it on your controller': 'bằng cách chạm vào Control đó',

    # "User Attribute" was two things at once: two keys said "User
    # Attribute" and six said "thuộc tính người dùng". The English name is
    # what the rest of the Attribute family uses ("Marker Attribute"), so all
    # eight go to the English form.
    'Add User Attribute': 'Thêm User Attribute',
    'Define User Attributes...': 'Định nghĩa User Attribute...',
    'Remove User Attribute': 'Gỡ User Attribute',
    'Removing User Attributes:': 'Đang gỡ User Attribute:',
    'Set up User Attributes': 'Thiết lập User Attribute',
    'User Attributes': 'User Attribute',
    'User Attribute Name': 'Tên User Attribute',
    'User Attribute Type': 'Loại User Attribute',
}

WORDING = {}
WORDING.update(SHORTER)
WORDING.update(WORDY)
WORDING.update(STACK)

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

# A readability round must never make a string longer. The "Control" family
# is the one place where that is easy to do by accident - "nút" is three
# characters and "Control" is seven - so the rule is checked, not trusted.
longer = [(k, vi.get(k, ''), v) for k, v in real.items()
          if vi.get(k) != v and len(v) > len(vi.get(k, ''))]
if longer:
    print('LONGER THAN BEFORE:')
    for k, old, new in longer:
        print(f'  {k[:56]!r}  {len(old)}c -> {len(new)}c')
        print(f'      {old!r}')
        print(f'   -> {new!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
cut = sum(len(vi.get(k, '')) - len(v) for k, v in changed.items())
print(f'characters removed: {cut}')
print()
for k, v in sorted(changed.items(), key=lambda kv: -(len(vi.get(kv[0], '')) - len(kv[1]))):
    old = vi.get(k, '')
    print(f'  {k[:56]!r}  {len(old)}c -> {len(v)}c')
    print(f'      {old[:118]!r}')
    print(f'   -> {v[:118]!r}')

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
print(f'\napplied {n} change(s) to batches')
