"""Round 72: manual reading fixes for 180+ confusing strings, inverted terms, and mistranslations.

Major defect classes discovered and fixed in this round:

1. Retrospective Record (16 strings):
   Retrospective Record was mistranslated as "ghi hồi tố" (retroactive criminal prosecution/law!).
   In DAW production, everyone calls it "Retrospective Record" / "Retrospective Recording" / "bản ghi Retrospective".
   Fixed all 16 strings ("Empty Retrospective Record Buffer" -> "Xóa Retrospective Record Buffer", etc.).

2. Mute mistranslated as "Tắt tiếng" / "Đã tắt tiếng" (15 strings) & Strip Silence (1 string):
   AGENT.md explicitly forbids translating Mute to "Tắt tiếng" or "Câm".
   "Mute Events" -> was "Tắt tiếng Event", now "Mute các Event".
   "Mute all video tracks" -> was "Tắt tiếng tất cả Track video", now "Mute tất cả Video Track".
   "Strip Silence" -> was bizarrely mistranslated as "Tắt tiếng Strip" (mute the strip), now "Cắt bỏ khoảng lặng".

3. Armed tracks & Import all Media Files (6 strings):
   - "Arm All Audio Tracks" -> was "Track Arm All Audio", now "Bật sẵn sàng ghi cho tất cả Audio Track"
   - "Disarm All Audio Tracks" -> was "Track Disarm All Audio", now "Tắt sẵn sàng ghi cho tất cả Audio Track"
   - "Arm All Tracks" -> was "Sẵn sàng tất cả Track", now "Bật sẵn sàng ghi tất cả Track"
   - "Test Record Arming for all Tracks" -> was "Test Record Arming cho Track all", now "Kiểm tra sẵn sàng ghi cho tất cả Track"
   - "Track Record Arming Routing" -> was "Định tuyến ghi sẵn sàng của Track", now "Routing sẵn sàng ghi của Track"
   - "Import all Media Files" -> was "Import File all Media", now "Import tất cả file Media"

4. Snap terms & Snap Types (15 strings):
   - "Snap Point" -> was "Điểm bắt dính", now "Snap Point"
   - "Snap Type: Events / Events + Cursor / Grid + Cursor / etc." -> was "Loại bắt dính: ...", now "Loại Snap: ..."
   - "Use Snap from Drum Map" -> removed illegal parenthesis "(Snap)" -> "Dùng Snap từ Drum Map"
   - "Scale Assistant: Toggle Snap Live Input" -> was "Trợ lý Scale: Bật/Tắt bắt dính...", now "Scale Assistant: Bật/Tắt Snap Live Input"
   - "Snap Pitch Editing" -> was "Bắt dính chỉnh sửa Pitch", now "Snap chỉnh sửa Pitch"

5. Assistant Panel Names standardized (15 strings):
   - "Scale Assistant" -> was "Trợ lý Scale", now "Scale Assistant"
   - "Mapping Assistant" -> was "Trợ lý Mapping", now "Mapping Assistant"
   - "Touch Collect Assistant" -> was "Trợ lý Touch Collect", now "Touch Collect Assistant"
   - "Proximity Assistant" -> was "Trợ lý Proximity", now "Proximity Assistant"

6. MIDI Note On / Note Off, Velocity & Channel Messages (23 strings):
   - "Note On" -> was "Bật Note", now "Note On"
   - "Note Off" -> was "Tắt Note", now "Note Off"
   - "On Velocity" -> was "Bật Velocity", now "On Velocity"
   - "Off Velocity" -> was "Tắt Velocity", now "Off Velocity"
   - "Note Insert Velocity" -> was "Chèn Velocity của Note", now "Velocity khi chèn nốt"
   - "CCMode: All Notes Off / All Sound Off / OMNI On/Off" -> standardized to standard MIDI message names
   - "CC: Attack Time" -> was "CC: Thời gian tấn công" (military attack!), now "CC: Thời gian Attack"
   - "CC: Gen Purp 1..8" -> was "CC: Mục đích chung 1..8", now "CC: Gen Purp 1..4" / "CC: Gen Purpose 5..8"
   - "CC: Data Increment / Decrement" -> restored standard MIDI names
   - "CC: Portamento Control / Time" -> restored standard MIDI names
   - "Pitch Shift" -> was "Dịch cao độ", now "Pitch Shift"

7. Chord Modifiers consistency (6 strings):
   - "Chord Modifiers" -> was "Bộ thay đổi hợp âm", now "Modifier hợp âm"
   - "Tension Modifiers" -> was "Bộ thay đổi Tension", now "Modifier Tension"
   - "Transpose Modifiers", "Voicing Modifiers", "Pad Modifiers", "Tool Modifiers"

8. Bypass consistency (13 strings):
   - "Bypass" -> was "Bỏ qua", now "Bypass"
   - "Bypass: Channel Strip / EQs / Inserts / Modulators / Sends" -> was "Bỏ qua: ...", now "Bypass: ..."
   - "Bypassed" -> was "Đang bỏ qua", now "Đã Bypass"
   - "VariAudio / Warp Changes Bypass on/off" -> "Bật/Tắt Bypass thay đổi VariAudio / Warp"

9. Switch: code keys translated from code instead of US (10 strings):
   - "Switch: Activate Speakers" (US: "Control Room On/Off") -> was "Chuyển: Bật loa", now "Bật/Tắt Control Room"
   - "Switch: Click Active" (US: "Click On/Off") -> was "Chuyển sang Click đang hoạt động", now "Bật/Tắt Click"
   - "Switch: Dim Active" (US: "Dim Signal On/Off") -> was "Chuyển sang Dim đang hoạt động", now "Bật/Tắt tín hiệu Dim"
   - "Switch: Listen Cancel" (US: "Deactivate All Listen States") -> was "Chuyển: Hủy Listen", now "Tắt tất cả trạng thái Listen"
   - "Switch: Listen Enable" (US: "Enable/Disable Listen for Output (LE)") -> was "Chuyển sang Listen Bật", now "Bật/Tắt Listen cho đầu ra LE"
   - "Switch: Reference Level Active" (US: "Reference Level On/Off") -> was "Chuyển: Bật mức tham chiếu", now "Bật/Tắt mức tham chiếu"
   - "Switch: Source Select" (US: "Select Control Room Source") -> was "Chuyển: Chọn nguồn", now "Chọn nguồn Control Room"
   - "Switch: Speakers Select" (US: "Select Next Monitor") -> was "Chuyển: Chọn loa", now "Chọn Monitor tiếp theo"
   - "Switch: Talkback Active" (US: "Talkback On/Off") -> was "Chuyển sang Talkback đang hoạt động", now "Bật/Tắt Talkback"

10. Key-mismatch, inverted word order & UI mistranslations (45+ strings):
    - "Show/Hide Infoview" (US: "Show/Hide Info Line") -> was "Hiện/Ẩn Infoview", now "Hiện/Ẩn Info Line"
    - "Sync Channel Selection with Mixer" (US: "Sync Channel Selection with MixConsole") -> was "...với Mixer", now "...với MixConsole"
    - "VST Connections" (US: "Audio Connections") -> was "Kết nối VST", now "Audio Connections"
    - "Touch (Control)" (US: "Touch") -> removed tag -> "Touch"
    - "Fore" (US: "Forward") -> was "Fore", now "Tua tới"
    - "Hit" (US: "Confirm") -> was "Hit", now "Xác nhận"
    - "AppKey[Key]" (US: "Menu") -> was "AppKey", now "Phím Menu"
    - "MIDI Step Input" (US: "MIDI Input") -> was "Đầu vào Step MIDI", now "MIDI Input"
    - "Assume Skipping" (US: "Process Existing Clip") -> was "Giả định bỏ qua", now "Xử lý Clip hiện có"
    - "Autoscroll" (US: "Auto-Scroll On/Off") -> was "Cuộn tự động", now "Bật/Tắt Auto-Scroll"
    - "Activate/Deactivate" (US: "Activate/Deactivate Focused Object") -> was "...đối tượng đang tập trung", now "Bật/Tắt đối tượng đang Focus"
    - "Delete Tool" (US: "Erase Tool") -> was "Xóa công cụ" (delete the tool!), now "Công cụ xóa"
    - "Converter" (US: "Convert Files") -> was "Bộ chuyển đổi", now "Chuyển đổi file"
    - "Command[Key]" -> was "Lệnh", now "Command"
    - "End[Key]" -> was "Kết thúc", now "End"
    - "Increment Fade Out Length" -> was "Độ dài Increment Fade Out", now "Tăng độ dài Fade Out"
    - "Scan unknown File Types" -> was "Loại Scan unknown File", now "Quét các loại file không xác định"
    - "To Real Copy" / "Convert to Real Copy" -> was "Tới bản sao thật" / "Chuyển thành bản sao thật", now "Chuyển thành bản sao độc lập"
    - "Toggle Edit Group on Selected Tracks" -> was "Chuyển đổi Group sửa...", now "Bật/Tắt Group Editing trên Track đã chọn"
    - "Toggle Read Enable All Tracks" -> was "Bật/tắt đọc cho tất cả Track", now "Bật/Tắt Read Automation cho tất cả Track"
    - "Toggle Write Enable All Tracks" -> was "Bật/tắt ghi cho tất cả Track", now "Bật/Tắt Write Automation cho tất cả Track"
    - "Continue Writing on Transport Jump" -> was "Continue Writing trên Transport Jump", now "Tiếp tục ghi khi Transport nhảy vị trí"
    - "Punch on Play" -> was "Punch trên Play", now "Punch khi Play"
    - "Import Files on One Track" -> was "Import File trên Track One", now "Import các file trên một Track"
    - "Text Input on Left-Click" -> was "Text Input trên Left-Click", now "Nhập văn bản khi nhấp chuột trái"
    - "Double-click Destination" -> was "Nhấp đúp đích đến", now "Hành động khi nhấp đúp"
    - "Display Quantize" -> was "Hiển thị Quantize", now "Quantize hiển thị"
    - "Quantize MIDI Event Lengths" -> was "Độ dài Quantize MIDI Event", now "Quantize độ dài MIDI Event"
    - "Set Quantize to 1/1..1/128" -> "Đặt Quantize thành 1/1..1/128"
    - "Cycle" -> was "Lặp", now "Cycle"
    - "Track Loop Start" -> was "Track Loop Bắt đầu", now "Điểm đầu Track Loop"
    - "Track Loop End" -> "Điểm cuối Track Loop"
    - "Increment" / "Decrement" -> "Tăng" / "Giảm"
    - "Nudge: Move Audio / Move Fade" -> restored missing colon and proper verb
    - "Store" / "Store Pattern" / "Store Snapshot" -> simplified to "Lưu"
    - "Revert to last Setting" -> "Quay lại cài đặt gần nhất"
    - "The application was terminated..." -> "Ứng dụng bị buộc đóng do lỗi khi thực thi file sau:"
        \x27\u1ee8ng d\u1ee5ng b\u1ecb bu\u1ed9c \u0111\u00f3ng do l\u1ed7i khi th\u1ef1c thi file sau:\x27,\n    - "Temporary Link Mode..." -> "...Đồng bộ tất cả tham số vừa điều chỉnh..."
    - "Shows the automation track with the last touched parameter..." -> "Hiện Automation Track của tham số vừa điều chỉnh..."
    - "Adjust the Effective Position of the Chord Symbols" -> "Điều chỉnh vị trí thực tế của ký hiệu hợp âm"
    - "Length Decay" -> "Length Decay"
    - "Resample" -> "Resample"

Usage:
  python tools/fix_reading72.py
  python tools/fix_reading72.py --write
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
    # 1. Retrospective Record (16 strings)
    'Retrospective Record':
        'Retrospective Record',
    'Retrospective Recording':
        'Retrospective Recording',
    'Retrospective Record: Chords':
        'Retrospective Record: Hợp âm',
    'Empty Retrospective Record Buffer':
        'Xóa Retrospective Record Buffer',
    'Insert Retrospective Recording':
        'Chèn bản ghi Retrospective',
    'Insert MIDI Retrospective Recording in Editor':
        'Chèn bản ghi MIDI Retrospective vào Editor',
    'Insert Retrospective Recording from All MIDI Inputs on Selected Track':
        'Chèn bản ghi Retrospective từ tất cả MIDI Input vào Track đã chọn',
    'Insert Retrospective Recording from Track Input in Editor':
        'Chèn bản ghi Retrospective từ Track Input vào Editor',
    'MIDI Retrospective Record: Empty All Buffers':
        'MIDI Retrospective Record: Xóa tất cả Buffer',
    'MIDI Retrospective Record: Insert from All MIDI Inputs':
        'MIDI Retrospective Record: Chèn từ tất cả MIDI Input',
    'MIDI Retrospective Record: Insert from Track Input as Cycle Recording':
        'MIDI Retrospective Record: Chèn từ Track Input dưới dạng ghi theo Cycle',
    'MIDI Retrospective Record: Insert from Track Input as Linear Recording':
        'MIDI Retrospective Record: Chèn từ Track Input dưới dạng ghi tuyến tính',
    'MIDI Retrospective Recording':
        'MIDI Retrospective Recording',
    'Retrospective MIDI Recording':
        'Retrospective MIDI Recording',
    'Retrospective Cycle Recording is not supported in MIDI Editors':
        'Không hỗ trợ ghi Retrospective theo Cycle trong MIDI Editor',
    'Retrospective Record Buffer Size in Events':
        'Kích thước Retrospective Record Buffer theo Event',

    # 2. Mute / Strip Silence (16 strings)
    'Mute Events':
        'Mute các Event',
    'Mute Gaps':
        'Mute các khoảng trống',
    'Mute Input':
        'Mute Input',
    'Mute Sections':
        'Mute các Section',
    'Mute Silent Segments':
        'Mute các đoạn im lặng',
    'Mute Source Events':
        'Mute các Source Event',
    'Mute Source Tracks':
        'Mute các Source Track',
    'Mute all Inputs':
        'Mute tất cả Input',
    'Mute all video tracks':
        'Mute tất cả Video Track',
    'Mute section':
        'Mute Section',
    'Mute/Unmute Events':
        'Mute/Bỏ Mute các Event',
    'Mute/Unmute Objects':
        'Mute/Bỏ Mute các đối tượng',
    'Is Muted':
        'Đang Mute',
    'Muted':
        'Đã Mute',
    'Muted Slash Noteheads':
        'Đầu nốt gạch chéo Mute',
    'Strip Silence':
        'Cắt bỏ khoảng lặng',

    # 3. Arm / Armed & Import (6 strings)
    'Arm All Audio Tracks':
        'Bật sẵn sàng ghi cho tất cả Audio Track',
    'Disarm All Audio Tracks':
        'Tắt sẵn sàng ghi cho tất cả Audio Track',
    'Arm All Tracks':
        'Bật sẵn sàng ghi tất cả Track',
    'Test Record Arming for all Tracks':
        'Kiểm tra sẵn sàng ghi cho tất cả Track',
    'Track Record Arming Routing':
        'Routing sẵn sàng ghi của Track',
    'Import all Media Files':
        'Import tất cả file Media',

    # 4. Snap (15 strings)
    'Snap Point':
        'Snap Point',
    'Snap Type: Events':
        'Loại Snap: Event',
    'Snap Type: Events + Cursor':
        'Loại Snap: Event + Con trỏ',
    'Snap Type: Events + Grid + Cursor':
        'Loại Snap: Event + Grid + Con trỏ',
    'Snap Type: Grid + Cursor':
        'Loại Snap: Grid + Con trỏ',
    'Snap Type: Grid Relative':
        'Loại Snap: Grid tương đối',
    'Snap Type: Magnetic Cursor':
        'Loại Snap: Magnetic Cursor',
    'Snap Type: Shuffle':
        'Loại Snap: Shuffle',
    'Use Snap from Drum Map':
        'Dùng Snap từ Drum Map',
    'Scale Assistant: Toggle Snap Live Input':
        'Scale Assistant: Bật/Tắt Snap Live Input',
    'Scale Assistant: Toggle Snap Pitch Editing':
        'Scale Assistant: Bật/Tắt Snap chỉnh sửa Pitch',
    'Snap Pitch Editing':
        'Snap chỉnh sửa Pitch',
    'Snap Live Input':
        'Snap Live Input',
    'Snap Pitches to Scale Assistant Settings while editing':
        'Snap Pitch theo cài đặt Scale Assistant khi đang sửa',
    'Snap incoming Pitches to Scale Assistant settings':
        'Snap Pitch đầu vào theo cài đặt Scale Assistant',

    # 5. Assistant Panel Names (15 strings)
    'Scale Assistant':
        'Scale Assistant',
    'Scale Assistant: Quantize Pitches':
        'Scale Assistant: Quantize Pitch',
    'Scale Assistant: Toggle Show Scale Note Guides':
        'Scale Assistant: Bật/Tắt hướng dẫn nốt Scale',
    'Indicates the Scale Assistant status':
        'Chỉ báo trạng thái Scale Assistant',
    'Show Pitches from Scale Assistant':
        'Hiện Pitch từ Scale Assistant',
    'Pitch is used, but does not match to Scale Assistant settings':
        'Pitch đang được dùng, nhưng không khớp với cài đặt Scale Assistant',
    'Mapping Assistant':
        'Mapping Assistant',
    'Go to Mapping Assistant':
        'Tới Mapping Assistant',
    'MIDI Remote Mapping Assistant':
        'MIDI Remote Mapping Assistant',
    'Use the Mapping Assistant to Create a Mapping':
        'Dùng Mapping Assistant để tạo Mapping',
    'To use the Proximity Assistant, assign a chord to the preceding chord event.':
        'Để dùng Proximity Assistant, hãy gán một hợp âm cho Chord Event phía trước.',
    'Touch Assist (Activate Touch Collect Assistant)':
        'Touch Assist (Bật Touch Collect Assistant)',
    'Touch Collect Assistant':
        'Touch Collect Assistant',
    'Touch Collect Assistant Disabled':
        'Touch Collect Assistant đã tắt',
    'Touch Collect Assistant Enabled':
        'Touch Collect Assistant đã bật',

    # 6. MIDI Note On / Note Off & Velocity & CC (23 strings)
    'Note On':
        'Note On',
    'Note Off':
        'Note Off',
    'On Velocity':
        'On Velocity',
    'Off Velocity':
        'Off Velocity',
    'Note Insert Velocity':
        'Velocity khi chèn nốt',
    'CCMode: All Notes Off':
        'CCMode: All Notes Off',
    'CCMode: All Sound Off':
        'CCMode: All Sound Off',
    'CCMode: OMNI Off':
        'CCMode: OMNI Off',
    'CCMode: OMNI On':
        'CCMode: OMNI On',
    'CC: Attack Time':
        'CC: Thời gian Attack',
    'CC: Gen Purp 1':
        'CC: Gen Purp 1',
    'CC: Gen Purp 2':
        'CC: Gen Purp 2',
    'CC: Gen Purp 3':
        'CC: Gen Purp 3',
    'CC: Gen Purp 4':
        'CC: Gen Purp 4',
    'CC: Gen Purpose 5':
        'CC: Gen Purpose 5',
    'CC: Gen Purpose 6':
        'CC: Gen Purpose 6',
    'CC: Gen Purpose 7':
        'CC: Gen Purpose 7',
    'CC: Gen Purpose 8':
        'CC: Gen Purpose 8',
    'CC: Data Increment':
        'CC: Data Increment',
    'CC: Data Decrement':
        'CC: Data Decrement',
    'CC: Portamento Control':
        'CC: Portamento Control',
    'CC: Portamento Time':
        'CC: Portamento Time',
    'Pitch Shift':
        'Pitch Shift',

    # 7. Chord Modifiers (6 strings)
    'Chord Modifiers':
        'Modifier hợp âm',
    'Tension Modifiers':
        'Modifier Tension',
    'Transpose Modifiers':
        'Modifier Transpose',
    'Voicing Modifiers':
        'Modifier Voicing',
    'Pad Modifiers':
        'Modifier Pad',
    'Tool Modifiers':
        'Modifier công cụ',

    # 8. Bypass (13 strings)
    'Bypass':
        'Bypass',
    'Bypass: Channel Strip':
        'Bypass: Channel Strip',
    'Bypass: Channel Strip on Main Mix':
        'Bypass: Channel Strip trên Main Mix',
    'Bypass: EQs':
        'Bypass: EQ',
    'Bypass: EQs on Main Mix':
        'Bypass: EQ trên Main Mix',
    'Bypass: Inserts':
        'Bypass: Insert',
    'Bypass: Inserts on Main Mix':
        'Bypass: Insert trên Main Mix',
    'Bypass: Modulators':
        'Bypass: Modulator',
    'Bypass: Sends':
        'Bypass: Send',
    'Bypassed':
        'Đã Bypass',
    'VariAudio Changes Bypass on/off':
        'Bật/Tắt Bypass thay đổi VariAudio',
    'Warp Changes Bypass on/off':
        'Bật/Tắt Bypass thay đổi Warp',
    'Note Expression Bypass on/off':
        'Bật/Tắt Bypass Note Expression',

    # 9. Switch: keys (10 strings)
    'Switch: AFL/PFL':
        'AFL/PFL',
    'Switch: Activate Speakers':
        'Bật/Tắt Control Room',
    'Switch: Click Active':
        'Bật/Tắt Click',
    'Switch: Dim Active':
        'Bật/Tắt tín hiệu Dim',
    'Switch: Listen Cancel':
        'Tắt tất cả trạng thái Listen',
    'Switch: Listen Enable':
        'Bật/Tắt Listen cho đầu ra LE',
    'Switch: Reference Level Active':
        'Bật/Tắt mức tham chiếu',
    'Switch: Source Select':
        'Chọn nguồn Control Room',
    'Switch: Speakers Select':
        'Chọn Monitor tiếp theo',
    'Switch: Talkback Active':
        'Bật/Tắt Talkback',

    # 10. Key-mismatch & untranslated/inverted UI strings (61 strings)
    'Show/Hide Infoview':
        'Hiện/Ẩn Info Line',
    'Sync Channel Selection with Mixer':
        'Đồng bộ vùng chọn Channel với MixConsole',
    'VST Connections':
        'Audio Connections',
    'Touch (Control)':
        'Touch',
    'Fore':
        'Tua tới',
    'Hit':
        'Xác nhận',
    'AppKey[Key]':
        'Phím Menu',
    'MIDI Step Input':
        'MIDI Input',
    'Assume Skipping':
        'Xử lý Clip hiện có',
    'Autoscroll':
        'Bật/Tắt Auto-Scroll',
    'Activate/Deactivate':
        'Bật/Tắt đối tượng đang Focus',
    'Delete Tool':
        'Công cụ xóa',
    'Converter':
        'Chuyển đổi file',
    'Command[Key]':
        'Command',
    'End[Key]':
        'End',
    'Increment Fade Out Length':
        'Tăng độ dài Fade Out',
    'Scan unknown File Types':
        'Quét các loại file không xác định',
    'To Real Copy':
        'Chuyển thành bản sao độc lập',
    'Convert to Real Copy':
        'Chuyển thành bản sao độc lập',
    'Toggle Edit Group on Selected Tracks':
        'Bật/Tắt Group Editing trên Track đã chọn',
    'Toggle Read Enable All Tracks':
        'Bật/Tắt Read Automation cho tất cả Track',
    'Toggle Read Enable Selected Tracks':
        'Bật/Tắt Read Automation cho Track đã chọn',
    'Toggle Write Enable All Tracks':
        'Bật/Tắt Write Automation cho tất cả Track',
    'Toggle Write Enable Selected Tracks':
        'Bật/Tắt Write Automation cho Track đã chọn',
    'Continue Writing on Transport Jump':
        'Tiếp tục ghi khi Transport nhảy vị trí',
    'Punch on Play':
        'Punch khi Play',
    'Import Files on One Track':
        'Import các file trên một Track',
    'Text Input on Left-Click':
        'Nhập văn bản khi nhấp chuột trái',
    'Double-click Destination':
        'Hành động khi nhấp đúp',
    'Display Quantize':
        'Quantize hiển thị',
    'Quantize MIDI Event Lengths':
        'Quantize độ dài MIDI Event',
    'Cycle':
        'Cycle',
    'Track Loop Start':
        'Điểm đầu Track Loop',
    'Track Loop End':
        'Điểm cuối Track Loop',
    'Decrement':
        'Giảm',
    'Increment':
        'Tăng',
    'Nudge: Move Audio':
        'Nudge: Di chuyển Audio',
    'Nudge: Move Fade':
        'Nudge: Di chuyển Fade',
    'Store':
        'Lưu',
    'Store Pattern':
        'Lưu Pattern',
    'Store Snapshot':
        'Lưu Snapshot',
    'Revert to last Setting':
        'Quay lại cài đặt gần nhất',
    'The application was terminated with an error while executing the following file:':
        'Ứng dụng bị buộc đóng do lỗi khi thực thi file sau:',
    'The selected device port is used exclusively. This connection will be ended. Do you want to continue?':
        'Cổng thiết bị đã chọn đang được dùng độc quyền. Kết nối này sẽ bị ngắt. Bạn có muốn tiếp tục không?',
    'Temporary Link Mode - Sync all touched parameters of selected channels':
        'Chế độ liên kết tạm thời - Đồng bộ tất cả tham số vừa điều chỉnh của các Channel đã chọn',
    'Shows the automation track with the last touched parameter at top position':
        'Hiện Automation Track của tham số vừa điều chỉnh ở trên cùng',
    'Shows the last touched parameter when appending a new automation track':
        'Hiện tham số vừa điều chỉnh khi thêm một Automation Track mới',
    'Adjust the Effective Position of the Chord Symbols':
        'Điều chỉnh vị trí thực tế của ký hiệu hợp âm',
    'Length Decay':
        'Length Decay',
    'Resample':
        'Resample',
    'Set Quantize to 1/1':
        'Đặt Quantize thành 1/1',
    'Set Quantize to 1/2':
        'Đặt Quantize thành 1/2',
    'Set Quantize to 1/4':
        'Đặt Quantize thành 1/4',
    'Set Quantize to 1/8':
        'Đặt Quantize thành 1/8',
    'Set Quantize to 1/16':
        'Đặt Quantize thành 1/16',
    'Set Quantize to 1/32':
        'Đặt Quantize thành 1/32',
    'Set Quantize to 1/64':
        'Đặt Quantize thành 1/64',
    'Set Quantize to 1/128':
        'Đặt Quantize thành 1/128',
    'Attribute Display on Marker Events':
        'Hiển thị thuộc tính trên Marker Event',
    'Centered on Bar':
        'Căn giữa trong Bar',
    'Windows: Next Mixer':
        'Cửa sổ: MixConsole kế tiếp',
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
for k, v in list(changed.items())[:20]:
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
