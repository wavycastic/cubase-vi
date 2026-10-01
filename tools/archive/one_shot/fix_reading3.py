#!/usr/bin/env python3
"""Round 3 of reading. Five domains read by hand (general, transport,
music-theory, notation, mixer/media/ui/project), 1.150 long values.

The pattern rules from the previous rounds found nothing here. What reading
found, in order of size:

  1. a whole family of tooltips left half in English
     "Cue Sends Bypass on/off.  |  Reset với [CTRL + click]" - the whole
     second sentence untranslated and the trailing period dropped.
  2. 4 keys whose value lost the object entirely, reading as a non-sentence:
     "Activate/Deactivate Focused Object" -> "Bật/Tắt"
  3. number moved in front of the noun: "100 Events" -> "Event 100"
  4. note durations flipped: "16th" -> "Móc 16"
  5. the reversed head-noun defect again, in values short enough that the
     earlier two-word rule could not reach: "Thêm Preset Multiple",
     "Offset Octave", "Trang Meters per"
  6. a genuinely wrong translation: "Aeolian (nat. minor)" ->
     "Aeolian (thứ tự nhiên)". "thứ tự" means "order"; natural minor is
     "thứ sáu tự nhiên". Read as a scale name, "thứ tự" reads fine, which is
     why every rule passed it.

Groups 1 and 3-5 are handled by pattern because they are exact. Everything
else is a hand-written decision keyed by the real key from all_strings.tsv.

  python tools/fix_reading3.py
  python tools/fix_reading3.py --write
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

# ===========================================================================
# hand-written decisions
# ===========================================================================
WORDING = {
    # -----------------------------------------------------------------
    # value lost its object, or was scrambled
    # -----------------------------------------------------------------
    'Activate/Deactivate':
        'Bật/Tắt đối tượng đang tập trung',
    'MIDI Retrospective Record: Insert from Track Input as Cycle Recording':
        'Ghi hồi tố MIDI: Chèn từ đầu vào Track dưới dạng ghi theo Cycle',
    'MIDI Retrospective Record: Insert from Track Input as Linear Recording':
        'Ghi hồi tố MIDI: Chèn từ đầu vào Track dưới dạng ghi tuyến tính',
    'Display Warning before Deleting Non-Empty Tracks':
        'Hiện cảnh báo trước khi xóa Track có dữ liệu',
    'Complete Signal Path Including Groups and Sends':
        'Toàn bộ đường truyền tín hiệu gồm Group và Send',
    'Slashed Noteheads (Bottom Left to Top Right)':
        'Đầu nốt có gạch chéo (từ dưới lên trên)',
    'Slashed Noteheads (Top Left to Bottom Right)':
        'Đầu nốt có gạch chéo (từ trên xuống dưới)',
    'No Mappable Controller found, please connect a supported MIDI Controller':
        'Không tìm thấy Controller nào gán được, vui lòng kết nối một MIDI '
        'Controller được hỗ trợ',
    'Pitch Visibility switched off because there are no note events in the '
    'editor':
        'Đã tắt Pitch Visibility vì trong Editor không có Note Event nào',
    'The plug-in could not be validated and has been moved to the blocklist. '
    'You can reactivate the plug-in, but please note that the operating '
    "system's protection may prevent the plug-in from loading. Please contact "
    'the manufacturer of the plug-in for an updated version.':
        'Plug-in không thể xác thực và đã được chuyển vào Blocklist. Bạn có thể '
        'kích hoạt lại, nhưng lưu ý cơ chế bảo vệ của hệ điều hành có thể ngăn '
        'Plug-in nạp. Vui lòng liên hệ nhà sản xuất để có phiên bản mới hơn.',
    "The 'Normal', 'Narrow, Serif' and 'Narrow, Sans Serif' designs all use "
    "the 'Music Font' font style, which must be a SMuFL-compliant music font, "
    "such as Bravura. The 'Plain Font' design uses the 'Text Font' font style, "
    'which can use any standard text font.':
        "Các kiểu 'Normal', 'Narrow, Serif' và 'Narrow, Sans Serif' đều dùng "
        "kiểu phông 'Music Font', phải là phông nhạc tuân thủ SMuFL như "
        "Bravura. Kiểu 'Plain Font' dùng kiểu phông 'Text Font', có thể dùng "
        'bất kỳ phông chữ tiêu chuẩn nào.',
    'The Cautionary Accidentals options only apply when the Common Practice '
    "accidental duration rule is used. A subset of options for the Modernist "
    'duration rule can be found in that section.':
        'Tùy chọn dấu hóa nhắc lại chỉ áp dụng khi dùng quy tắc trường độ '
        'dấu hóa Thực hành chung. Một phần tùy chọn của quy tắc trường độ '
        'Hiện đại nằm trong mục đó.',
    'Track Display Settings: All Visible Tracks':
        'Cài đặt hiển thị Track: tất cả Track đang hiện',
    'Track Display Settings: Toggle Modes':
        'Cài đặt hiển thị Track: đảo chế độ',

    # -----------------------------------------------------------------
    # reversed head noun - too short or too mixed for fix_word_order.py
    # -----------------------------------------------------------------
    'Add Multiple Presets': 'Thêm nhiều Preset',
    'Add Track Instrument...': 'Thêm Instrument Track...',
    'Octave Offset (Use Left/Right Arrow Keys to modify)':
        'Offset Octave (Dùng phím mũi tên Trái/Phải để chỉnh)',
    'Meters per Page': 'Số Meter mỗi trang',
    'Meters: Hold Forever': 'Meter: Giữ vĩnh viễn',
    "Meters' Peak Hold Time": 'Thời gian giữ đỉnh của Meter',
    "Meters' Fallback": 'Tốc độ suy giảm của Meter',
    'Include Inserts for Instrument Tracks':
        'Bao gồm Insert cho Instrument Track',
    'Include Inserts for Sampler Tracks':
        'Bao gồm Insert cho Sampler Track',
    'Include Inserts for Instruments/Sampler Tracks':
        'Bao gồm Insert cho Instrument Track/Sampler Track',
    'Add Individual Setting': 'Thêm cài đặt riêng',
    'Add Mutual Exclusion Group': 'Thêm nhóm loại trừ lẫn nhau',
    'Articulations & Mutual Exclusion Groups':
        'Articulation & Nhóm loại trừ lẫn nhau',

    # -----------------------------------------------------------------
    # genuinely wrong
    # -----------------------------------------------------------------
    # "thứ tự" means "order". Natural minor is the sixth mode, "thứ sáu".
    'Aeolian (nat. minor)': 'Aeolian (thứ sáu tự nhiên)',
    'Write protected - maintain a personal copy?':
        'Bị chống ghi - duy trì một bản sao cá nhân?',
    'Fewer Tensions ([ALT] - mouse wheel on pad)':
        'Ít Tension hơn ([ALT] - cuộn chuột trên pad)',
    'Align Centers': 'Căn giữa ngang',
    'Align Middles': 'Căn giữa dọc',
    'Align Bottoms': 'Căn đáy',
    'Align Tops': 'Căn đỉnh',
    'Align Lefts': 'Căn trái',
    'Align Rights': 'Căn phải',
    'These were replaced by nearest new color.':
        'Các mục này đã được thay bằng màu mới gần với màu đã chọn nhất.',
    'Switch Between Program-Gated and Dialogue-Gated Loudness Measurement':
        'Chuyển giữa đo Loudness theo Program và theo hội thoại',
    'Respect Maximum Duration for Rhythmic Slashes in Compound Time '
    'Signatures':
        'Tuân thủ trường độ tối đa cho gạch nhịp trong số chỉ nhịp phức',
    'Respect Maximum Duration for Rhythmic Slashes in Irregular Time '
    'Signatures':
        'Tuân thủ trường độ tối đa cho gạch nhịp trong số chỉ nhịp bất thường',
    'Stretch or pitch factor out of range! Use real time preset instead.':
        'Hệ số co giãn hoặc Pitch vượt ngoài dải! Hãy dùng Preset thời gian '
        'thực thay vì.',
    'Shifting must be aborted, because the master track would be shifted into '
    'the negative!':
        'Phải hủy việc dịch chuyển, vì Master Track sẽ bị dịch sang vùng âm!',

    # -----------------------------------------------------------------
    # term drift: AGENT.md says Cycle, not "chu kỳ"; Arranger Chain, not
    # "Chuỗi Arranger"
    # -----------------------------------------------------------------
    'Activated: Cycle follows when locating to Markers':
        'Đã bật: Cycle bám theo khi định vị tới Marker',
    'Set up MIDI Cycle-Record Modes (Requires Cycle Mode)':
        'Thiết lập chế độ ghi MIDI theo Cycle (Yêu cầu chế độ Cycle)',
    "Start Mode has been changed to \\'Start from Selection or Cycle Start\\'":
        'Chế độ Start đã được đổi thành \'Bắt đầu từ vùng chọn hoặc đầu Cycle\'',
    'One or more jobs were skipped because channels, cycle markers or Arranger '
    'Chains could not be found.':
        'Một hoặc nhiều tác vụ bị bỏ qua vì không tìm thấy Channel, Cycle Marker '
        'hoặc Arranger Chain.',
    'Bar': 'Bar',

    # -----------------------------------------------------------------
    # "vào" where the English means a conversion, or nothing at all
    # -----------------------------------------------------------------
    '2-Layer to 3-Layer': 'Chuyển từ 2-Layer sang 3-Layer',
    '3-Layer to 2-Layer': 'Chuyển từ 3-Layer sang 2-Layer',
    '- Reset complex transitions to linear transitions':
        '- Đặt lại transition phức tạp thành transition tuyến tính',
    '- %i multichannel track(s) split to mono':
        '- %i multichannel track(s) đã tách thành mono',
    'Addition to PFX': 'Bổ sung cho PFX',
    'Adapt to Pattern': 'Thích ứng với Pattern',
    'Auto-Zoom to Event': 'Auto-Zoom tới Event',
    '%s from %d to %d': '%s từ %d đến %d',
    'MIDI Retrospective Record: Insert from Track Input as Cycle Recording':
        'Ghi hồi tố MIDI: Chèn từ đầu vào Track dưới dạng ghi theo Cycle',
    'Jump to Next Range with Low Intelligibility':
        'Tới Vùng kế tiếp có độ rõ nhận thấp thấp',
    'Listen to Surround Channels on Front Channels':
        'Nghe các Channel Surround qua các Channel Front',
    'MIDI In port for MIDI Machine Control data':
        'Cổng MIDI In cho dữ liệu MIDI Machine Control',

    # -----------------------------------------------------------------
    # "to X" replaced by the literal verb "vào", which reads as neither
    # language
    # -----------------------------------------------------------------
    'Destination Path is invalid for copying or consolidation':
        'Destination Path không hợp lệ để sao chép hoặc hợp nhất',
    'Currently used in the following sound slots:\\n%s':
        'Đang được dùng trong các sound slot sau:\\n%s',
    'Defines which hitpoint positions are used for slicing':
        'Xác định các vị trí Hitpoint nào được dùng để cắt lát',
    'Drag to change order of modulators in signal chain':
        'Kéo để đổi thứ tự các Modulator trong chuỗi tín hiệu',
    'Drag to change order of modules in signal path':
        'Kéo để đổi thứ tự các Module trong đường truyền tín hiệu',
    'Invert Direction for Horizontal Mouse Wheel Scrolling':
        'Đảo chiều cuộn ngang bằng con lăn chuột',
    'Hold values for Integrated, Range, and True Peak when playback stops':
        'Giữ giá trị Integrated, Range và True Peak khi dừng phát',
    'Release Driver when Application is in Background':
        'Nhả Driver khi ứng dụng chạy nền',
    'Only available for Instrument, Drum, and Sampler Tracks':
        'Chỉ khả dụng cho Instrument Track, Drum Track và Sampler Track',
    'Allow different Sample Rates': 'Cho phép các Sample Rate khác nhau',
    'Allow Alterations': 'Cho phép chỉnh sửa',
    'Allow Editing in Results List': 'Cho phép sửa trong danh sách kết quả',
    'Add steps as shapes': 'Thêm Step dưới dạng Shape',
    'Additional RS422-Out settings': 'Cài đặt RS422-Out bổ sung',
    'Shows all defined attributes for the selected results':
        'Hiện tất cả thuộc tính đã định nghĩa của các kết quả đã chọn',
    'Shows all found attributes for the selected results':
        'Hiện tất cả thuộc tính tìm được của các kết quả đã chọn',
    'Sync Layout reflects the event selection in project':
        'Sync Layout phản ánh vùng chọn Event trong Project',
    'Rhythmic Slash Grouping in Compound Time Signatures':
        'Nhóm gạch nhịp trong số chỉ nhịp phức',
    'Rhythmic Slash Grouping in Irregular Time Signatures':
        'Nhóm gạch nhịp trong số chỉ nhịp bất thường',
    'Dialogue-gated loudness measurement according to ITU-R BS.1770':
        'Đo Loudness theo hội thoại theo ITU-R BS.1770',
    'Program-gated loudness measurement according to EBU R 128':
        'Đo Loudness theo Program theo EBU R 128',
    'Dialogue-gated loudness measurement if at least 15% speech is detected':
        'Đo Loudness theo hội thoại nếu phát hiện ít nhất 15% tiếng nói',
    'Warning: Recursive definition of Variable \'%s\'!':
        'Cảnh báo: Định nghĩa Variable \'%s\' bị đệ quy!',
    'Use Steinberg\'s \'Time Base\' device for Machine Control':
        'Dùng thiết bị \'Time Base\' của Steinberg cho Machine Control',
    'Use Steinberg\'s SyncStation device for Machine Control':
        'Dùng thiết bị SyncStation của Steinberg cho Machine Control',
    'Maximum Number of Rhythm Dots Allowed in Compound Beats':
        'Số dấu chấm nhịp tối đa được phép trong nhịp phức',
    'Maximum Number of Rhythm Dots Allowed in Simple Beats':
        'Số dấu chấm nhịp tối đa được phép trong nhịp đơn',
    'Notes Following Grace Notes That Introduce an Accidental':
        'Nốt sau nốt lạc nhạc có dấu hóa',
    'Notes Following Trills That Introduce an Accidental':
        'Nốt sau mô tức có dấu hóa',
    'Notes Following a Cue That Introduces an Accidental':
        'Nốt sau dấu nhắc có dấu hóa',
    'Notes Eligible for a Cautionary Accidental Following an Enharmonically '
    'Equivalent Note':
        'Nốt đủ điều kiện hiện dấu hóa nhắc lại sau một nốt cùng cao độ',
    'Initial assignment of input movements to VST Note Expressions':
        'Phân gán ban đầu các chuyển động đầu vào cho VST Note Expression',
    'Remote note for transposing the last played chord pad downwards':
        'Note Remote để hạ thấp Chord Pad vừa phát',
    'Remote note for transposing the last played chord pad upwards':
        'Note Remote để nâng cao Chord Pad vừa phát',
    'Snap Pitches to Scale Assistant Settings while editing':
        'Snap Pitch theo cài đặt Scale Assistant khi đang sửa',
    'Punch in previewing parameters now':
        'Punch In và xem trước tham số ngay bây giờ',
    'Punch in previewing parameters when transport starts':
        'Punch In và xem trước tham số khi bắt đầu phát',
    'Punch out on reaching right locator + Punch in previewing parameters on '
    'reaching left locator':
        'Punch Out khi tới Locator phải + Punch In và xem trước tham số khi '
        'tới Locator trái',
    'Record Destination when track is enabled for both part record and '
    'automation write':
        'Ghi vào đích khi Track được bật cho cả ghi Part và ghi Automation',
    'Allow machine controlled cycle': 'Cho phép Cycle do máy điều khiển',
    'Colors can\'t be changed for inactive Projects':
        'Không thể đổi màu cho Project không hoạt động',
    'Activate/Deactivate Read for All Tracks':
        'Bật/Tắt ghi đọc cho tất cả Track',
    'Activate/Deactivate Write for All Tracks':
        'Bật/Tắt ghi ghi cho tất cả Track',
    'Activate/Deactivate Write for All Tracks: Is Writing':
        'Bật/Tắt ghi ghi cho tất cả Track: Đang ghi',
    'Change Instrument Type for Active Track':
        'Đổi loại Instrument cho Track đang hoạt động',
    'Change Instrument Type for Active Track...':
        'Đổi loại Instrument cho Track đang hoạt động...',
    'Change Pitch of selected Notes via MIDI Input':
        'Đổi Pitch của các Note đã chọn qua đầu vào MIDI',
    'Active track for editing': 'Track đang hoạt động để sửa',
    "Actor's Name": 'Tên diễn viên',
    'Add Next to Selection': 'Thêm ngay sau vùng chọn',
    'Add Previous to Selection': 'Thêm ngay trước vùng chọn',
    'Add Selected Effect "%s" to Favorites':
        'Thêm Effect "%s" đã chọn vào mục yêu thích',
    'Add Selected Instrument "%s" to Favorites':
        'Thêm Instrument "%s" đã chọn vào mục yêu thích',
    'Add MediaBay Aspect': 'Thêm khía cạnh MediaBay',
    'Add New Pattern...': 'Thêm Pattern mới...',
    'Add New Signature...': 'Thêm Signature mới...',
    'Add Device (from a popup list of available devices)':
        'Thêm Device (từ danh sách bật lên các Device khả dụng)',
    'Adaptive Voicings': 'Adaptive Voicing',
    'Type of New Controller Events: Toggle Step/Ramp':
        'Loại Event của Controller mới: Step/Ramp',
    'Track-to-port mapping and track number already correspond to the default '
    'settings.':
        'Mapping Track sang cổng và số Track đã khớp với cài đặt mặc định.',
    'Meter Peak Level\\n[Click] to reset':
        'Đỉnh Meter\\n[Click] để đặt lại',
    'Meter Peak Level\\n[Click] to reset\\n[Alt + Click] to reset all meters':
        'Đỉnh Meter\\n[Click] để đặt lại\\n[Alt + Click] để đặt lại tất cả '
        'Meter',
    'Modulators are not displayed in inactive projects':
        'Không hiển thị Modulator trong Project không hoạt động',
    'Move Selected Tracks/Channels to Previous Available Position':
        'Di chuyển Track/Channel đã chọn tới vị trí khả dụng liền trước',
    'Type of newly created events (e.g. when created with Draw Tool)':
        'Loại Event mới tạo (ví dụ: khi tạo bằng công cụ vẽ Draw)',
    'Number of samples after which a new automation event is processed.':
        'Số Sample sau đó một Automation Event mới được xử lý.',
    'Name already exists. A unique name is used instead.':
        'Tên đã tồn tại. Một tên duy nhất sẽ được dùng thay thế.',
    'Secondary type is used below the primary type if space allows':
        'Loại phụ được dùng bên dưới loại chính nếu còn đủ chỗ',
    "Ruler Display Type has been changed to \\'Bar + Beats\\' and the Grid Type "
    "to \\'Use Quantize\\'.  This is required for Metronome Click Pattern "
    "Emphasis.":
        'Kiểu hiển thị thước đo đã đổi thành \'Bar + Beats\' và loại Grid thành '
        '\'Dùng Quantize\'. Điều này là bắt buộc để làm nổi bật Pattern Click '
        'Metronome.',
    "Ruler Display Type has been changed to \\'Bar + Beats\\'.  This is "
    "required for Metronome Click Pattern Emphasis.":
        'Kiểu hiển thị thước đo đã đổi thành \'Bar + Beats\'. Điều này là bắt '
        'buộc để làm nổi bật Pattern Click Metronome.',
    'Invalid input. MP3 only supports mono and stereo channels.':
        'Dữ liệu đầu vào không hợp lệ. MP3 chỉ hỗ trợ Channel Mono và Stereo.',
    'Link All Word Clock Outputs (Where matching rate is possible)':
        'Liên kết tất cả đầu ra Word Clock (ở nơi tần số có thể khớp)',
    'Select Available Device Panels (that will fit into this space)':
        'Chọn Panel thiết bị khả dụng (vừa với không gian này)',
    'Global mappings are saved with the program. They are available in all '
    'projects.':
        'Mapping toàn cục được lưu cùng chương trình. Chúng khả dụng trong mọi '
        'Project.',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) Denominator '
    'Time Signatures':
        'Nối đuôi các nốt móc đơn 1/8 trong số chỉ nhịp mẫu số nốt cường 1/4',
    'Multiselection active: Changes are applied to all selected tracks. '
    "Settings for 'Voices', 'Percussion' or 'Strings and Tuning' are not "
    'available in this mode.':
        'Đang chọn nhiều: Các thay đổi được áp dụng cho tất cả Track đã chọn. '
        "Cài đặt cho 'Voices', 'Percussion' hoặc 'Strings and Tuning' không "
        'khả dụng ở chế độ này.',
    'Absolute Mode - Force all parameters to the same value':
        'Chế độ Absolute - Ép mọi tham số về cùng một giá trị',
    'Add or drop processes here!': 'Thêm hoặc thả Process vào đây!',
    'Nuendo and SyncStation configurations settings are inconsistent.':
        'Cài đặt cấu hình của Nuendo và SyncStation không nhất quán.',
    'Part/Clip Editing Mode: Toggle All & Active Parts/Clips':
        'Chế độ sửa Part/Clip: Đảo tất cả & Part/Clip đang hoạt động',
    'Rests Substituting One of the Short Notes in Short-Long-Short Patterns':
        'Dấu lặng thay thế một nốt ngắn trong các Pattern ngắn-dài-ngắn',
    'To save your changes for the selected job, please click \'Update Job\'.':
        'Để lưu các thay đổi cho tác vụ đã chọn, vui lòng nhấp \'Update Job\'.',
}

# ---------------------------------------------------------------------- #
# the "Use ... vào Đặt lại" family keeps the English verb, so a substitution
# cannot finish the job. Four keys, named explicitly.
# ---------------------------------------------------------------------- #
for _k, _name in (
        ('Set Channel Type Filter\\nUse [CTRL + click] to Reset Channel Type '
         'Filter', 'Channel'),
        ('Set Track Type Filter\\nUse [CTRL + click] to Reset Track Type '
         'Filter', 'Track')):
    if _k in src:
        WORDING[_k] = (f'Đặt {_name} Type Filter\\n'
                       f'Dùng [CTRL + nhấp] để đặt lại {_name} Type Filter')
for _k, _name in (
        ('Set Channel Visibility Agents\\nUse [ALT]-Click to Reset Channel '
         'Visibility Agents', 'Channel'),
        ('Set Track Visibility Agents\\nUse [ALT]-Click to Reset Track '
         'Visibility Agents', 'Track')):
    if _k in src:
        WORDING[_k] = (f'Đặt {_name} Visibility Agents\\n'
                       f'Dùng [ALT] + nhấp để đặt lại {_name} Visibility '
                       'Agents')
if 'Click to Select Click Sound File' in src:
    WORDING['Click to Select Click Sound File'] = \
        'Nhấp để chọn File âm thanh Click'

# "%d Channels" -> "Channel %d" is the same flip as "100 Events", but a
# blanket rule would also catch "Channel %d", which is already right. So the
# rule is dropped and these two are listed.
for _k in ('%d Channels', '%d channels'):
    if _k in src:
        WORDING[_k] = '%d Channel'

# ---------------------------------------------------------------------- #
# families, exact enough to be safe
# ---------------------------------------------------------------------- #

# "X Bypass on/off.\nReset with [CTRL + click]." - the whole second sentence
# was left English and the trailing period dropped.
RE_BYPASS = re.compile(
    r'^([A-Za-z0-9]+(?: [A-Za-z0-9]+)*) Bypass on/off\.\\nReset với '
    r'\[CTRL \+ click\]$')

# "Click vào X" - a botched swap left "vào" in place of the English verb.
# Only the two shapes that carry no English verb of their own are matched;
# anything longer is left for reading, because the verb usually survives.
RE_CLICK_VAO = [
    (re.compile(r'^Click vào (.+)$'), r'Click để \1'),
    (re.compile(r'\bClick vào (.+)$'), r'Click để \1'),
    (re.compile(r'\b\[Click\] vào reset\b'), '[Click] để đặt lại'),
]

# "100 Events" -> "Event 100": the number was moved behind the noun.
RE_NUM_AFTER = re.compile(r'^(Event|Sample|Frame|Beat|Bar) (\d+)$')

# note duration flipped: "16th" -> "Móc 16"
NOTE_FLIP = {
    '8th': 'Note 1/8', '16th': 'Note 1/16', '32th': 'Note 1/32',
    '64th': 'Note 1/64',
}

# "Agents:" is the menu, the English is plural
for _k in list(vi):
    if _k.startswith('Agents: ') and vi[_k].startswith('Agent: '):
        WORDING[_k] = 'Agents: ' + vi[_k][len('Agent: '):]

# ---------------------------------------------------------------------- #

fixes = {}
real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

# The family rules run first, then the hand-written table is laid over them.
# Order matters: "Use [ALT]-Click vào Đặt lại" matches RE_CLICK_VAO, but the
# substitution only removes "vào" and leaves "Use ... để Đặt lại", so the key
# is listed in WORDING as well and must win.
for k, v in vi.items():
    m = RE_BYPASS.match(v)
    if m:
        fixes[k] = (f'Bật/tắt Bypass {m.group(1)}.\\n'
                    'Đặt lại bằng [CTRL + nhấp].')
    for rx, rep in RE_CLICK_VAO:
        new = rx.sub(rep, v)
        if new != v:
            fixes[k] = new
            break
    m = RE_NUM_AFTER.match(v)
    if m:
        fixes[k] = f'{m.group(2)} {m.group(1)}'

for k, v in real.items():
    fixes[k] = v

# "%d Channels" -> "Channel %d" is handled by hand above, not by a rule:
# the rule cannot tell it from the correct "Channel %d".

# the note-duration flip is keyed by value, so map it back to keys
for k, v in vi.items():
    if v in NOTE_FLIP:
        fixes[k] = NOTE_FLIP[v]

bad = [(k, v) for k, v in fixes.items()
       if sorted(PH.findall(src.get(k, ''))) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src.get(k, "?")!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in fixes.items() if vi.get(k) != v}
byhand = sum(1 for k in changed if k in real)
print(f'hand-written keys : {len(real)}')
print(f'family matches   : {len(changed) - byhand}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:56]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v!r}')

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
