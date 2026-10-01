"""Round 71: manual reading fixes 98 confusing strings, inverted terms, and mistranslations.

Major defect classes discovered and fixed in this round:

1. "Chord Symbol" mistranslated as "Hóa biểu" (9 strings):
   A Chord Symbol (C, Dm, G7) is a "Ký hiệu hợp âm" (chord symbol written above staves).
   The previous translation bizarrely translated it as "Hóa biểu" (which means Key Signature!).
   Key Signature was already correctly translated as "Hóa âm", but Chord Symbol had taken over
   "Hóa biểu" (e.g. "Show Chord Symbols" -> "Hiện hóa biểu", "Chord Symbols Preset" -> "Preset hóa biểu").
   Corrected all 9 strings to "Ký hiệu hợp âm".

2. MIDI "System Exclusive" mistranslated as "Dòng nhạc độc quyền" (1 string):
   SysEx (System Exclusive message in MIDI) was mistranslated as "Dòng nhạc độc quyền"
   because the translator confused MIDI "System" with score "System" (dòng nhạc) and
   "Exclusive" with "độc quyền". Restored to standard "System Exclusive".

3. "Right Arrow[Key]" raw "[Key]" extractor tag leaked into value (1 string):
   Translated as "Arrow[Key] phải" with the literal extractor tag in the string.
   Up/Down/Left were all "Phím mũi tên...". Fixed to "Phím mũi tên phải".

4. Extractor disambiguation brackets leaked into values (5 strings):
   In keys where the English text has NO brackets, the extractor's key-disambiguating
   brackets were erroneously placed in the translated values:
   - "General [Metronom Setup]" -> was "Chung [Metronom Setup]", now "Chung"
   - "Bass 2[vocal]" -> was "Bass 2 [vocal]", now "Bass 2"
   - "[Transition Soft]" -> was "[Chuyển tiếp mềm]", now "Mềm" (US is "Soft")
   - "[Mixer Track Number]" -> was "[Số Track MixConsole]", now "Số Track" (US is "Track Number")
   - "[Track Type: Group]" -> was "[Loại Track: Group]", now "Group" (US is "Group")

5. Programming jargon "phép gán" (assignment operator) replaced with natural terms (23 strings):
   Throughout the UI for key commands, remote triggers, control surfaces, and chord pads,
   "assignment" was translated as "phép gán" (computer science programming assignment operator).
   Turned into natural Vietnamese: "mục gán", "thiết lập gán", "hợp âm đã gán", "phím đã gán".

6. Inverted garbled commands & splash messages (9 strings):
   - "Process All Selected Events" -> was "Event Process All Selected", now "Xử lý tất cả Event đã chọn"
   - "Process Logical Preset" -> was "Preset Process Logical", now "Xử lý Logical Preset"
   - "Process Project Logical Editor" -> dropped the verb, now "Xử lý Project Logical Editor"
   - "Include Audio Events" -> was "Event Include Audio", now "Bao gồm Audio Event"
   - "Include MIDI Channel" -> was raw English, now "Bao gồm MIDI Channel"
   - "Using Track Preset..." -> was "Preset Using Track...", now "Dùng Track Preset..."
   - "Reading Project File" -> was "File Reading Project", now "Đang đọc file Project"
   - "Writing Project Information..." -> was "Thông tin Writing Project...", now "Đang ghi thông tin Project..."
   - "Locate Track File" -> was "File Locate Track", now "Định vị file Track"

7. "Range to ..." commands with literal "Vùng vào..." (6 strings):
   - "Range to Next Event" -> was "Vùng vào Event k��� tiếp", now "Vùng chọn tới Event kế tiếp"
   - "Range to Previous Event" -> was "Vùng vào Event trước", now "Vùng chọn tới Event liền trước"
   - "Range to Next Hitpoint" -> was "Vùng vào Hitpoint kế tiếp", now "Vùng chọn tới Hitpoint kế tiếp"
   - "Range to Previous Hitpoint" -> was "Vùng vào Hitpoint trước", now "Vùng chọn tới Hitpoint liền trước"
   - "Range to Next Audio Segment" -> was "Vùng vào Next Audio Segment", now "Vùng chọn tới Audio Segment kế tiếp"
   - "Range to Previous Audio Segment" -> was "Vùng vào Previous Audio Segment", now "Vùng chọn tới Audio Segment liền trước"

8. "Zoom to ..." commands standardized to "Zoom tới ..." (5 strings):
   - "Zoom to Event" -> "Zoom tới Event" (was "Zoom theo Event")
   - "Zoom to Locators" -> "Zoom tới Locator" (was "Zoom theo Locator")
   - "Zoom to Selection" -> "Zoom tới vùng chọn" (was "Zoom theo vùng chọn")
   - "Zoom to Selection (Horiz.)" -> "Zoom tới vùng chọn (Ngang)"
   - "Zoom to Selection Horizontally" -> "Zoom tới vùng chọn theo chiều ngang"

9. Editor naming consistency & inverted word order (11 strings):
   - "Plug-in Editors 'Always on Top'" -> was "Trình sửa Plug-in...", now "Plug-in Editor 'Luôn ở trên cùng'"
   - "MIDI Hex Editor" -> "MIDI Hex Editor"
   - "MIDI SysEx Editor" -> "MIDI SysEx Editor"
   - "Patch Bank Editor" -> "Patch Bank Editor"
   - "Open Sample Editor in Window" -> was "Mở Editor Sample trong Window", now "Mở Sample Editor trong Window"
   - "Open Pattern Editor in Window" -> was "Mở Editor Pattern trong Window", now "Mở Pattern Editor trong Window"
   - "Click Pattern Editor" -> was "Editor Click Pattern", now "Click Pattern Editor"
   - "Tempo Track Editor" -> was "Editor Tempo Track", now "Tempo Track Editor"
   - "Tempo Track Editor (Inactive) - %s" -> now "Tempo Track Editor (Không hoạt động) - %s"
   - "Tempo Track Editor - %s" -> now "Tempo Track Editor - %s"
   - "Activate Tempo Track..." -> now "...mở Tempo Track Editor của Project"

10. Musical terminology & awkward phrasing fixes (28 strings):
    - "Unslashed Grace Note" -> was "Nốt lạc không gạch chéo", now "Nốt Grace không có gạch chéo"
    - "Dynamic Velocity" -> was "Động lực Velocity", now "Dynamic Velocity"
    - "Toggle Enharmonic Spelling" -> was "Chuyển đổi chính tả Enharmonic", now "Đổi cách ghi nốt đồng âm"
    - "lead sheet" -> was "bản tổng phổ chép tay" (full score!), now "bản lead sheet chép tay"
    - "Solo Defeat" in "Solo (Solo Defeat with...)" -> was "Bỏ Solo", now "Solo Defeat"
    - "Enter Locator Range Duration" -> was raw English, now "Nhập thời lượng dải Locator"
    - "When the page is less full than..." -> was "Khi trang ít đầy hơn...", now "Khi độ lấp đầy của trang chưa đạt ngưỡng..."
    - "Audio Connections..." -> was "Kết nối Audio...", now matches dialog "Audio Connections..."
    - "Open Audio Connections..." -> was "Mở kết nối Audio...", now "Mở Audio Connections..."
    - "Sync Selection in Project Window and MixConsole" -> was raw "Project Window", now "cửa sổ Project"
    - "Temporary Disabled" -> was "Disabled tạm thời", now "Tạm thời tắt"
    - "Auto Adjust" -> was "Adjust tự động", now "Tự động điều chỉnh"
    - "Auto Join" -> was "Join tự động", now "Auto Join"
    - "Pre/Post Fader" -> was "Fader Pre/Post", now "Pre/Post Fader"
    - "Sliced" -> was "Đã cắt lát", now "Đã tạo Slice"
    - "Sliced audio cannot be switched to musical mode." -> was "Audio đã cắt lát...", now "Audio đã tạo Slice..."
    - "Sets a fixed focus..." / "Sets the focus..." -> was "tiêu điểm", now "Focus"
    - Safe mode Preferences options: avoided awkward stutter "Tùy chọn này xóa các tùy chọn..." -> "Tùy chọn này xóa toàn bộ Preferences..."
    - "Popup Toolbar..." -> was "...nhấp phím bổ trợ", now "...nhấn phím bổ trợ + click"
    - "Keep Freeze Files" -> was raw English plural, now "Giữ các file Freeze"
    - "...The function had to be canceled!" -> was "Chức năng đã phải bị hủy!", now "Thao tác đã phải bị hủy!"
    - "Open/Save MIDI SysEx file" -> "Mở/Lưu file MIDI SysEx"
    - "Pre Filters" -> "Pre Filter"

Usage:
  python tools/fix_reading71.py
  python tools/fix_reading71.py --write
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
    # 1. Chord Symbol (was "Hóa biểu"!)
    'Chord Symbol':
        'Ký hiệu hợp âm',
    'Chord Symbols':
        'Ký hiệu hợp âm',
    'Chord Symbols Preset':
        'Preset ký hiệu hợp âm',
    'Show Chord Symbols':
        'Hiện ký hiệu hợp âm',
    'Custom Chord Symbols':
        'Ký hiệu hợp âm tùy chỉnh',
    'Adjust the Effective Position of the Chord Symbols':
        'Điều chỉnh vị trí hiệu dụng của ký hiệu hợp âm',
    'For Notation and main Chord Symbols':
        'Dành cho ký âm và ký hiệu hợp âm chính',
    'Primary type is used for the main chord symbol':
        'Loại chính được dùng cho ký hiệu hợp âm chính',
    'Chord symbols appear either above the staves belonging to specific instruments as defined in Instrument Settings, or above the top staff in the system.':
        'Ký hiệu hợp âm hiển thị ở trên các khuông nhạc của nhạc cụ cụ thể như định nghĩa trong cài đặt Instrument, hoặc ở trên khuông nhạc trên cùng của dòng nhạc.',

    # 2. System Exclusive (was "Dòng nhạc độc quyền"!)
    'System Exclusive':
        'System Exclusive',

    # 3. Arrow[Key] (was "Arrow[Key] phải"!)
    'Right Arrow[Key]':
        'Phím mũi tên phải',

    # 4. Extractor brackets in values
    'General [Metronom Setup]':
        'Chung',
    'Bass 2[vocal]':
        'Bass 2',
    '[Transition Soft]':
        'Mềm',
    '[Mixer Track Number]':
        'Số Track',
    '[Track Type: Group]':
        'Group',

    # 5. Phép gán -> gán / thiết lập gán
    'Clear All Assignments':
        'Xóa tất cả mục gán',
    'Remove All Assignments':
        'Gỡ bỏ tất cả mục gán',
    'Remove Assignment':
        'Gỡ bỏ mục gán',
    'Remove all control assignments?':
        'Gỡ bỏ tất cả Control đã gán?',
    'Reset User Command Assignments':
        'Đặt lại các lệnh đã gán của người dùng',
    'Reset to Default Assignments':
        'Đặt lại về thiết lập gán mặc định',
    'Save Input Assignment':
        'Lưu thiết lập gán Input',
    'Load Input Assignment':
        'Tải thiết lập gán Input',
    'Lock Chord Assignment on Pad':
        'Khóa hợp âm đã gán trên Pad',
    'Activate/Deactivate Assignment Inspection View':
        'Bật/Tắt chế độ kiểm tra mục gán',
    'Do you really want to remove all Quick Control assignments?':
        'Bạn có thực sự muốn gỡ bỏ tất cả Quick Control đã gán không?',
    'Learn MIDI assignment for selected Note Expression parameter':
        'Gán MIDI Learn cho tham số Note Expression đã chọn',
    'Show Automated QC Assignments':
        'Hiện các Quick Control được gán tự động',
    'Show only Sound Slots with Remote Trigger assignments':
        'Chỉ hiện các Sound Slot có gán Remote Trigger',
    'The key assignments are already used by:\\n\\n%s\\nDo you want to reassign the existing keys? Note that the previous assignments will be lost.':
        'Các phím gán này đã được dùng bởi:\\n\\n%s\\nBạn có muốn gán lại các phím hiện có không? Lưu ý rằng thiết lập gán trước đó sẽ bị mất.',
    'This key assignment is already used by "%s". Do you want to reassign this key? Note that the previous assignment will be lost.':
        'Phím này đã được gán cho "%s". Bạn có muốn gán lại phím này không? Lưu ý rằng thiết lập gán trước đó sẽ bị mất.',
    'This operation will change all chord assignments and cannot be undone.':
        'Thao tác này sẽ thay đổi tất cả hợp âm đã gán và không thể hoàn tác.',
    'This operation will remove the chord assignments from the selected pads and cannot be undone.':
        'Thao tác này sẽ gỡ bỏ hợp âm đã gán khỏi các Pad đã chọn và không thể hoàn tác.',
    'This will reset the command assignment to the factory default.':
        'Thao tác này sẽ đặt lại lệnh đã gán về mặc định Factory.',
    'The audio device port or midi device assignments of this Favorite are already in use. Reuse them and add to External Effects?':
        'Cổng Audio Device hoặc thiết bị MIDI đã gán cho Favorite này đang được sử dụng. Tái sử dụng và thêm vào External Effect?',
    'The audio device port or midi device assignments of this Favorite are already in use. Reuse them and add to External Instruments?':
        'Cổng Audio Device hoặc thiết bị MIDI đã gán cho Favorite này đang được sử dụng. Tái sử dụng và thêm vào External Instrument?',
    'Click and drag this cell to move or copy it, or to swap it with another cell. | Double-click to change the control assignment.':
        'Nhấp và kéo ô này để di chuyển hoặc sao chép, hoặc hoán đổi với ô khác. | Nhấp đúp để đổi Control đã gán.',
    'Overwrite the existing assignments?':
        'Ghi đè các thiết lập gán hiện tại?',

    # 6. Inverted / garbled commands
    'Process All Selected Events':
        'Xử lý tất cả Event đã chọn',
    'Process Logical Preset':
        'Xử lý Logical Preset',
    'Process Project Logical Editor':
        'Xử lý Project Logical Editor',
    'Include Audio Events':
        'Bao gồm Audio Event',
    'Include MIDI Channel':
        'Bao gồm MIDI Channel',
    'Using Track Preset...':
        'Dùng Track Preset...',

    # 7. Splash / progress inverted strings
    'Reading Project File':
        'Đang đọc file Project',
    'Writing Project Information...':
        'Đang ghi thông tin Project...',
    'Locate Track File':
        'Định vị file Track',

    # 8. Range to ...
    'Range to Next Event':
        'Vùng chọn tới Event kế tiếp',
    'Range to Previous Event':
        'Vùng chọn tới Event liền trước',
    'Range to Next Hitpoint':
        'Vùng chọn tới Hitpoint kế tiếp',
    'Range to Previous Hitpoint':
        'Vùng chọn tới Hitpoint liền trước',
    'Range to Next Audio Segment':
        'Vùng chọn tới Audio Segment kế tiếp',
    'Range to Previous Audio Segment':
        'Vùng chọn tới Audio Segment liền trước',

    # 9. Zoom to ...
    'Zoom to Event':
        'Zoom tới Event',
    'Zoom to Locators':
        'Zoom tới Locator',
    'Zoom to Selection':
        'Zoom tới vùng chọn',
    'Zoom to Selection (Horiz.)':
        'Zoom tới vùng chọn (Ngang)',
    'Zoom to Selection Horizontally':
        'Zoom tới vùng chọn theo chiều ngang',

    # 10. Editors
    'Plug-in Editors "Always on Top"':
        'Plug-in Editor "Luôn ở trên cùng"',
    'MIDI Hex Editor':
        'MIDI Hex Editor',
    'MIDI SysEx Editor':
        'MIDI SysEx Editor',
    'Patch Bank Editor':
        'Patch Bank Editor',
    'Open Sample Editor in Window':
        'Mở Sample Editor trong Window',
    'Open Pattern Editor in Window':
        'Mở Pattern Editor trong Window',
    'Click Pattern Editor':
        'Click Pattern Editor',
    'Tempo Track Editor':
        'Tempo Track Editor',
    'Tempo Track Editor (Inactive) - %s':
        'Tempo Track Editor (Không hoạt động) - %s',
    'Tempo Track Editor - %s':
        'Tempo Track Editor - %s',
    'Activate Tempo Track (use [CTRL + click] to open project tempo track editor)':
        'Bật Tempo Track (dùng [CTRL + nhấp chuột] để mở Tempo Track Editor của Project)',

    # 11. Music terms & awkward phrases
    'Unslashed Grace Note':
        'Nốt Grace không có gạch chéo',
    'Dynamic Velocity':
        'Dynamic Velocity',
    'Toggle Enharmonic Spelling':
        'Đổi cách ghi nốt đồng âm',
    "In some hand-copied lead sheets, the clef is shown only at the beginning of the first bar, and it is hidden on subsequent systems. To follow this convention, choose 'Hide Clefs'.":
        "Trong một số bản lead sheet chép tay, khóa nhạc chỉ hiện ở đầu Bar đầu tiên và ẩn ở các dòng nhạc tiếp theo. Để theo quy ước này, hãy chọn 'Ẩn khóa nhạc'.",
    "In some hand-copied lead sheets, the key signature is shown only at the beginning of the first bar, and it is hidden on subsequent systems. To follow this convention, choose 'Hide Key Signatures'.":
        "Trong một số bản lead sheet chép tay, hóa âm chỉ hiện ở đầu Bar đầu tiên và ẩn ở các dòng nhạc tiếp theo. Để theo quy ước này, hãy chọn 'Ẩn hóa âm'.",
    'Solo (Solo Defeat with [ALT + Ctrl + click])':
        'Solo (Solo Defeat bằng [ALT + Ctrl + nhấp chuột])',
    'Enter Locator Range Duration':
        'Nhập thời lượng dải Locator',
    'When the page is less full than the threshold for justifying staves, no vertical justification occurs.':
        'Khi độ lấp đầy của trang chưa đạt ngưỡng căn đều khuông nhạc, sẽ không căn đều theo chiều dọc.',
    'Audio Connections...':
        'Audio Connections...',
    'Open Audio Connections...':
        'Mở Audio Connections...',
    'Sync Selection in Project Window and MixConsole':
        'Đồng bộ vùng chọn giữa cửa sổ Project và MixConsole',
    'Temporary Disabled':
        'Tạm thời tắt',
    'Auto Adjust':
        'Tự động điều chỉnh',
    'Auto Join':
        'Auto Join',
    'Pre/Post Fader':
        'Pre/Post Fader',
    'Sliced':
        'Đã tạo Slice',
    'Sliced audio cannot be switched to musical mode.':
        'Audio đã tạo Slice không thể chuyển sang chế độ Musical.',
    'Sets a fixed focus to the %s function that is picked for mapping.':
        'Đặt Focus cố định cho chức năng %s được chọn để Map.',
    'Sets the focus according to the track selection.':
        'Đặt Focus theo vùng chọn Track.',
    'This option deletes the preferences of current and older program installations and initializes the program with factory settings. Please be aware that all your custom settings will be removed. This operation cannot be undone.':
        'Tùy chọn này xóa toàn bộ Preferences của bản cài đặt hiện tại và các bản cũ hơn, rồi khởi tạo lại chương trình với cài đặt Factory. Lưu ý rằng toàn bộ cài đặt tùy chỉnh của bạn sẽ bị gỡ bỏ. Thao tác này không thể hoàn tác.',
    'This option disables your custom preferences and initializes the program with factory settings. Your preferences are available after restarting the program.':
        'Tùy chọn này tạm tắt Preferences tùy chỉnh của bạn và khởi tạo chương trình với cài đặt Factory. Preferences của bạn sẽ khả dụng lại sau khi khởi động lại chương trình.',
    'This option uses the preferences currently stored in the program.':
        'Tùy chọn này sử dụng Preferences hiện đang lưu trong chương trình.',
    'Popup Toolbar (static one with modifier click)':
        'Thanh công cụ Pop-up (Cố định khi nhấn phím bổ trợ + click)',
    'Keep Freeze Files':
        'Giữ các file Freeze',
    'There was a file error during bounce!\\nThe function had to be canceled!':
        'Đã xảy ra lỗi file trong khi Bounce!\\nThao tác đã phải bị hủy!',
    'Open MIDI SysEx file':
        'Mở file MIDI SysEx',
    'Save MIDI SysEx file':
        'Lưu file MIDI SysEx',
    'Pre Filters':
        'Pre Filter',
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
