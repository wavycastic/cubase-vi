"""Round 70: manual reading across all domains (media, general, music-theory, mixer, transport, notation).

Major classes of translation defects fixed in this round:

1. Legacy "Warp Tab" vs displayed "Warp Marker" (14 strings):
   Steinberg's legacy keys retain the old internal term "Warp Tab", but Steinberg
   updated English to "Warp Marker" across all UI, manuals, and 8 vendor translations
   (German "Warp-Marker", French "Marqueurs Warp"). Vietnamese blindly used "Warp Tab",
   even on keys where English was "Warp Markers" (e.g. "Warp Markers" -> "Warp Tabs",
   "Copy Warp Markers..." -> "Sao chép Warp Tab..."). Standardized to Warp Marker.

2. Tautological "Cắt lát Slice" and audio slicing (7 strings):
   "Slice[QP]" was translated as "Cắt lát Slice" (both the literal translation and
   the English term concatenated). Audio slicing at hitpoints was translated as
   "cắt lát" (cooking term). Standardized to Slice / cắt thành Slice / cắt Slice.

3. Film/Video "Pull-up/Pull-down" & "Pull Factor" mistranslated as "kéo" (12 strings):
   In film/broadcast post-production, pull-up/pull-down (+/-0.1% or +/-4%) is the standard
   clock adjustment for frame rate conversion (telecine). German and French keep
   "Pull", "Pull Factor", "Pull-up/Pull-down". Vietnamese translated it as "kéo lên/kéo xuống",
   "hệ số kéo", "kéo Word Clock", "kéo lên/xuống của Nuendo". Fixed to standard DAW terms.

4. "Start" button translated as "Phát" (Play) (2 strings):
   In "Click 'Start' to scan for unreferenced files", the prompt said "Nhấp 'Phát' để quét..."
   and the standalone key "Start" was translated as "Phát"! In all other languages, Start is
   Démarrer, Iniciar, Avvia, 开始. Standalone Start is "Bắt đầu".

5. "nốt cường" for quarter note (Crotchet) -> "nốt đen" (7 strings):
   In British music terminology, Crotchet is a quarter note (nốt đen in Vietnamese).
   It was bizarrely translated as "nốt cường" across 7 strings. Fixed to "nốt đen"
   while keeping "Note 1/4".

6. "Note 1/2 (nốt bán)" for Minim (half note / nốt trắng) (1 string):
   Minim is a half note (nốt trắng), not "nốt bán". Fixed to "Note 1/2 (nốt trắng)".

7. Enharmonic (đồng âm) mistranslated as "cảm điệu" (3 strings):
   "Enharmonic spelling", "Enharmonics from Chord Track" translated as "chính tả cảm điệu",
   "bộ cảm điệu". Enharmonic notes are nốt đồng âm. Fixed to "đồng âm" / "Enharmonic".

8. "Rehearsal Mark" mistranslated as "Dấu tập dượt" (3 strings):
   In musical scores, rehearsal marks are rehearsal marks (A, B, C...).
   "Yamaha Rehearsal Mark" was translated as "Dấu tập dượt Yamaha". Fixed.

9. "MIDI Controller Surface Editor" mistranslated as "Trình sửa bề mặt" (3 strings):
   A MIDI control surface is a "Surface". Calling it "bề mặt" (skin/tabletop surface)
   is absurd. Standardized to "MIDI Controller Surface Editor" and "Surface Editor".

10. Typo "trực tuyếp" (1 string):
    "Trong trường hợp không có Project nào trực tuyếp" -> "trực tuyến".

11. Trailing "thay vì." fragment (1 string):
    "Hệ số co giãn hoặc Pitch vượt ngoài dải! Hãy dùng Preset thời gian thực thay vì."
    Fixed to "...để thay thế."

12. "Vẻ ngoài" for notation text appearance (1 string):
    "Text or Symbol Appearance at Start of Subsequent Systems" -> "Kiểu hiển thị...",
    not "Vẻ ngoài" (personal physical looks).

13. "cổng thoại" / "cổng chương trình" for loudness gating (2 strings):
    In loudness metering (ITU-R BS.1770 / EBU R128), dialogue-gated and program-gated
    measurement were translated as "cổng thoại" and "cổng chương trình". Fixed to
    "theo hội thoại" and "theo Program".

14. "a change of key" mistranslated as "đổi số chỉ nhịp" in notation rule (1 string):
    Accidentals apply until the end of the bar or a change of key (đổi hóa âm/đổi giọng),
    not change of time signature (đổi số chỉ nhịp).

15. "MIDI Input" rule violations (7 strings):
    "từ mọi MIDI đầu vào vào..." -> "từ tất cả MIDI Input vào...", "VariAudio MIDI Đầu vào"
    -> "VariAudio MIDI Input", etc.

16. "Show/Hide Editor Visibility" translated as "khả năng hiển thị" (2 strings):
    Visibility tab/zone in Cubase Editor translated as "khả năng hiển thị của Editor".
    Fixed to "mục Visibility của Editor" and "thẻ Visibility".

17. Clumsy phrasing & duplicate prepositions (2 strings):
    "thay đổi Tempo hiện tại tại vị trí" -> "thay đổi Tempo tại vị trí con trỏ Project".
    "Cài đặt Channel hoặc Automation của các Track đã chọn không bằng nhau" -> "...không giống nhau".

Usage:
  python tools/fix_reading70.py
  python tools/fix_reading70.py --write
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
    # 1. Warp Markers (standardize from legacy "Warp Tab" to "Warp Marker")
    'Warp Markers':
        'Warp Marker',
    'Create Warp Tabs':
        'Tạo Warp Marker',
    'Create Warp Tabs from Hitpoints':
        'Tạo Warp Marker từ Hitpoint',
    'Creates Warp Tabs at Hitpoints':
        'Tạo Warp Marker tại Hitpoint',
    'Defines which hitpoint positions are used for creating Warp Tabs':
        'Xác định vị trí Hitpoint nào được dùng để tạo Warp Marker',
    'Delete Warp Tab':
        'Xóa Warp Marker',
    'Delete Warp Tabs':
        'Xóa các Warp Marker',
    'Edit Warp Tab':
        'Sửa Warp Marker',
    'Remove all Warp Tabs':
        'Gỡ bỏ tất cả Warp Marker',
    'Warp Tab Creation Rules':
        'Quy tắc tạo Warp Marker',
    'Copy Warp Markers from Selected Event':
        'Sao chép Warp Marker từ Event đã chọn',
    'Paste Warp Markers to Selected Events':
        'Dán Warp Marker vào Event đã chọn',
    'Phase-coherent AudioWarp operations require equal event lengths, positions, and warp markers. Click "Bounce" to create such events.':
        'Các thao tác AudioWarp đồng pha cần các Event có độ dài, vị trí và Warp Marker bằng nhau. Nhấp "Bounce" để tạo các Event như vậy.',
    'The audio material contains warp tabs or is in musical mode. If you slice it, warp tabs are removed and musical mode is deactivated.':
        'Chất liệu Audio chứa Warp Marker hoặc đang ở chế độ Musical. Nếu bạn cắt thành Slice, các Warp Marker sẽ bị gỡ bỏ và chế độ Musical sẽ bị tắt.',

    # 2. Slice
    'Slice[QP]':
        'Cắt Slice',
    'Set Minimum Length of a Hitpoint Slice':
        'Đặt độ dài tối thiểu của Slice Hitpoint',
    'Audio in musical mode cannot be sliced.\\nDo you want to disable musical mode?':
        'Audio ở chế độ Musical không thể cắt thành Slice.\\nBạn có muốn tắt chế độ Musical không?',
    'Determines how far before the actual hitpoint position the audio event is sliced':
        'Xác định khoảng cách trước vị trí Hitpoint thực tế mà Audio Event được cắt thành Slice',
    'Defines which hitpoint positions are used for slicing':
        'Xác định vị trí Hitpoint nào được dùng để cắt Slice',
    'Resets "Slice audio events at hitpoints"':
        'Đặt lại "Cắt Slice Audio Event tại Hitpoint"',
    'Slice audio events at hitpoints':
        'Cắt Slice Audio Event tại Hitpoint',

    # 3. Pull (film/video audio pull factor, not "kéo")
    'Pull Factor':
        'Pull Factor',
    'Audio Pull-up/Pull-down':
        'Audio Pull-up/Pull-down',
    'HW Pull Up/Down':
        'HW Pull Up/Down',
    'Nuendo Audio Pull Factor':
        'Pull Factor Audio Nuendo',
    "Nuendo's Pull Up/Down":
        'Pull Up/Down của Nuendo',
    'Project Audio Pull':
        'Audio Pull của Project',
    'Pull Word Clock':
        'Pull Word Clock',
    'Pull Up/Down:':
        'Pull Up/Down:',
    'Use Film Pull Factor (- 0.1%)':
        'Dùng Film Pull Factor (- 0.1%)',
    'Warning: Pull factor does not match the pull factor of the audio hardware.':
        'Cảnh báo: Pull Factor không khớp với Pull Factor của phần cứng Audio.',
    'Warning: Pull factor is not supported by the audio hardware':
        'Cảnh báo: Pull Factor không được phần cứng Audio hỗ trợ',
    'Warning: Pull factor is not supported by the audio hardware.':
        'Cảnh báo: Pull Factor không được phần cứng Audio hỗ trợ.',

    # 4. Start (standalone / scan button: "Bắt đầu", not "Phát")
    'Start':
        'Bắt đầu',
    "Click 'Start' to scan for unreferenced files":
        "Nhấp 'Bắt đầu' để quét các file không được tham chiếu",

    # 5. Note 1/4 (nốt đen, not "nốt cường")
    '1/4 Note (Crotchet)':
        'Note 1/4 (nốt đen)',
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nốt 1/8 (nốt móc đơn) trong số chỉ nhịp có mẫu số là Note 1/4 (nốt đen)',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nối đuôi nốt 1/8 (nốt móc đơn) trong số chỉ nhịp có mẫu số là Note 1/4 (nốt đen)',
    'Quarter Note (Crotchet) Denominator Time Signatures With Half-Bars':
        'Số chỉ nhịp có mẫu số là Note 1/4 (nốt đen) kèm nửa Bar',
    "If this option is activated, the Score Editor will produce, assuming 'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', a dotted slash followed by an undotted slash in 5/8, but five slashes in 5/4.":
        'Nếu tùy chọn này được bật và giả định "Thời lượng tối đa cho dấu gạch chéo nhịp" được đặt thành "Note 1/4 (nốt đen)", Score Editor sẽ tạo ra một gạch chéo có chấm theo sau bởi một gạch chéo không chấm ở 5/8, nhưng năm gạch chéo ở 5/4.',
    "If this option is activated, the Score Editor will produce, assuming 'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', two dotted slashes in 6/8, but six undotted slashes in 6/4.":
        'Nếu tùy chọn này được bật và giả định "Thời lượng tối đa cho dấu gạch chéo nhịp" được đặt thành "Note 1/4 (nốt đen)", Score Editor sẽ tạo ra hai gạch chéo có chấm ở 6/8, nhưng sáu gạch chéo không chấm ở 6/4.',
    "This specifies the maximum duration the Score Editor will produce for a rhythmic slash, without considering rhythm dots, and applies in all time signatures. For example, if you choose '1/4 Note (Crotchet)', the Score Editor will create four slashes in 2/2, and two dottet slashes in 6/8.":
        "Tùy chọn này xác định thời lượng tối đa mà Score Editor sẽ tạo cho một dấu gạch chéo nhịp, không tính các dấu chấm dôi, và áp dụng cho mọi số chỉ nhịp. Ví dụ, nếu bạn chọn 'Note 1/4 (nốt đen)', Score Editor sẽ tạo bốn gạch trong 2/2 và hai gạch có chấm trong 6/8.",

    # 6. Note 1/2 (nốt trắng, not "nốt bán")
    '1/2 Note (Minim)':
        'Note 1/2 (nốt trắng)',

    # 7. Enharmonic (đồng âm, not "cảm điệu")
    'Enharmonics from Chord Track':
        'Nốt đồng âm từ Chord Track',
    'Toggle Enharmonic Spelling':
        'Chuyển đổi chính tả Enharmonic',
    'Notes Eligible for a Cautionary Accidental Following an Enharmonically Equivalent Note':
        'Nốt đủ điều kiện hiện dấu hóa nhắc lại sau một nốt đồng âm tương đương',

    # 8. Rehearsal Mark (not "Dấu tập dượt")
    'Show Bar Numbers at Rehearsal Marks':
        'Hiện số Bar tại Rehearsal Mark',
    'Show Rehearsal Marks Below Bottom Staff':
        'Hiện Rehearsal Mark bên dưới khuông nhạc dưới cùng',
    'Yamaha Rehearsal Mark':
        'Yamaha Rehearsal Mark',

    # 9. Surface Editor (not "Trình sửa bề mặt")
    'MIDI Controller Surface Editor':
        'MIDI Controller Surface Editor',
    "No controller surface available. Enter the mandatory information, click OK, and create a surface in the 'MIDI Controller Surface Editor'.":
        "Không có Controller Surface nào khả dụng. Nhập thông tin bắt buộc, nhấp OK, rồi tạo một Surface trong 'MIDI Controller Surface Editor'.",
    'Close MIDI Controller Surface Editor and Open Mapping Assistant':
        'Đóng MIDI Controller Surface Editor và mở Mapping Assistant',

    # 10. Typo
    'Please select a project.\\nIn case no projects are online,\\nyou cannot join.':
        'Vui lòng chọn một Project.\\nTrong trường hợp không có Project nào trực tuyến,\\nbạn không thể tham gia.',

    # 11. "thay vì." -> "để thay thế."
    'Stretch or pitch factor out of range! Use real time preset instead.':
        'Hệ số co giãn hoặc Pitch vượt ngoài phạm vi! Hãy dùng Preset thời gian thực để thay thế.',

    # 12. "Vẻ ngoài" -> "Kiểu hiển thị"
    'Text or Symbol Appearance at Start of Subsequent Systems':
        'Kiểu hiển thị văn bản hoặc ký hiệu ở đầu các dòng nhạc tiếp theo',

    # 13. Loudness gating (not "cổng thoại" / "cổng chương trình")
    'Threshold for dialog-gated loudness measurement. If less speech is detected in audio, program-gated measurement is used.':
        'Ngưỡng cho phép đo Loudness theo hội thoại. Nếu phát hiện ít giọng nói trong Audio, phép đo theo Program sẽ được dùng.',
    'Threshold for dialogue-gated loudness measurement. If less speech is detected in audio, program-gated measurement is used':
        'Ngưỡng cho phép đo Loudness theo hội thoại. Nếu phát hiện ít giọng nói trong Audio, phép đo theo Program sẽ được dùng',

    # 14. Notation rule: change of key = đổi hóa âm, not "đổi số chỉ nhịp"
    'Accidentals apply to all notes at the same staff position (i.e. in one octave only), until the end of the bar or a change of key, whichever is sooner, and apply to all voices belonging to the same track.':
        'Dấu hóa áp dụng cho tất cả nốt ở cùng vị trí khuông nhạc (tức là chỉ trong một quãng tám), cho tới hết Bar hoặc khi đổi hóa âm, tùy cái nào đến trước, và áp dụng cho mọi bè thuộc cùng Track.',

    # 15. MIDI Input rule (keep English, avoid "vào vào")
    'Insert Retrospective Recording from All MIDI Inputs on Selected Track':
        'Chèn ghi hồi tố từ tất cả MIDI Input vào Track đã chọn',
    'Insert from All MIDI Inputs':
        'Chèn từ tất cả MIDI Input',
    'MIDI Retrospective Record: Insert from All MIDI Inputs':
        'Ghi hồi tố MIDI: Chèn từ tất cả MIDI Input',
    'VariAudio MIDI Input':
        'VariAudio MIDI Input',
    'Insert Retrospective Recording from Track Input in Editor':
        'Chèn ghi hồi tố từ Track Input vào Editor',
    'MIDI Retrospective Record: Insert from Track Input as Cycle Recording':
        'Ghi hồi tố MIDI: Chèn từ Track Input dưới dạng ghi theo Cycle',
    'MIDI Retrospective Record: Insert from Track Input as Linear Recording':
        'Ghi hồi tố MIDI: Chèn từ Track Input dưới dạng ghi tuyến tính',

    # 16. Visibility tab / section (not "khả năng hiển thị")
    'Show/Hide Editor Visibility':
        'Hiện/Ẩn mục Visibility của Editor',
    'All source tracks will be hidden. To show the tracks again, activate them on the Visibility tab.':
        'Tất cả Source Track sẽ bị ẩn. Để hiện lại Track, hãy bật chúng trên thẻ Visibility.',

    # 17. Clumsy phrasing & repetition
    'Tempo (changes the current tempo at the project cursor position)':
        'Tempo (thay đổi Tempo tại vị trí con trỏ Project)',
    'Warning: Channel settings or automation of selected tracks are not equal.\\n\\nDo you want to continue?':
        'Cảnh báo: Cài đặt Channel hoặc Automation của các Track đã chọn không giống nhau.\\n\\nBạn có muốn tiếp tục không?',
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
       or '\ufffd' in v or not v.strip() or '[RM]' in v
       or src[k].count('\\n') != v.count('\\n')]
if bad:
    print('PROBLEM (placeholder, U+FFFD, empty, [RM], or line breaks):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
for k, v in changed.items():
    print(f'  {k[:58]!r}')
    print(f'      {vi.get(k, "")[:110]!r}')
    print(f'   -> {v[:110]!r}')

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

print(f'\nupdated {n} batch occurrences across {len(glob.glob(os.path.join(BATCH_DIR, "*.json")))} files')
