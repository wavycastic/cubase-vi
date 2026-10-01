"""Round 78: 5-agent parallel sweep - transport/mixer/media/theory/ui fixes.

Consolidated from 5 subagent reports; lateral churn and regressions rejected.
Usage:
  python tools/fix_reading78.py
  python tools/fix_reading78.py --write
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
    # ---- transport ----
    'Activated: Cycle follows when locating to Markers':
        'Đã bật: Cycle theo khi nhảy tới Marker',
    'Cycle Follows When Locating to Markers':
        'Cycle theo khi nhảy tới Marker',
    'Automatically Set the Locators Whenever a Marker Is Located':
        'Tự đặt Locator mỗi khi nhảy tới Marker',
    'Active record location is not available.\\nRecord location is set to project folder.':
        'Không dùng được vị trí ghi hiện tại.\\nVị trí ghi đã về thư mục Project.',
    'Clicking record again during a recording cleans up and restarts the recording.':
        'Nhấp nút ghi lần nữa khi đang ghi sẽ bỏ bản đang ghi và ghi lại từ đầu.',
    'Clicking record again during a recording stops the current recording.':
        'Nhấp nút ghi lần nữa khi đang ghi sẽ dừng luôn.',
    'Do you want to reset the record folder of the selected tracks to the project directory?':
        'Đặt lại thư mục ghi của Track đã chọn về thư mục Project không?',
    'Record Destination when track is enabled for both part record and automation write':
        'Đích ghi khi Track bật cả ghi Part lẫn ghi Automation',
    "Record Mode has been changed to \\'Start Recording at Left Locator or Punch In\\'":
        "Chế độ ghi đã đổi thành 'Bắt đầu ghi tại Locator trái hoặc Punch In'",
    "Record Mode has been changed to \\'Start Recording at Project Cursor\\'":
        "Chế độ ghi đã đổi thành 'Bắt đầu ghi tại con trỏ Project'",
    "Record Mode has been changed to \\'Start Recording at Selection Start\\'":
        "Chế độ ghi đã đổi thành 'Bắt đầu ghi tại đầu vùng chọn'",
    'For proper tempo editing, the display has been switched to tempo linear mode!':
        'Để sửa Tempo cho chuẩn, màn hình đã chuyển sang Tempo tuyến tính!',
    'No grid editing when tempo is ramped!':
        'Không sửa được Grid khi Tempo chạy dốc!',
    "If 'Auto Apply Quantize' is active, 'Apply Quantize' has no effect":
        "Nếu bật 'Tự động áp dụng Quantize' thì 'Áp dụng Quantize' không chạy.",
    'MIDI Recordings are quantized automatically to the current Quantize Setting.':
        'MIDI mới ghi tự Quantize theo Quantize hiện tại.',
    'Please create hitpoints before using AudioWarp quantize for groups.':
        'Tạo Hitpoint trước khi AudioWarp Quantize cho nhóm.',
    'Retrospective Record Buffer Size in Events':
        'Cỡ Retrospective Record Buffer tính bằng Event',
    'Record buffered parameter values as One-Shots to notes':
        'Ghi giá trị tham số trong Buffer thành One-Shot cho các nốt',
    "'Edit Solo'/'Record in MIDI Editors' follow Focus":
        "'Sửa Solo'/'Record trong MIDI Editor' bám theo Focus",
    'Click in an empty area to reposition the cursor. Click an item to edit it.':
        'Nhấp chỗ trống để dời con trỏ. Nhấp một mục để sửa.',
    'Set Range to current Locator Range':
        'Đặt vùng chọn theo dải Locator hiện tại',
    'Locators to Selection\\nUse [ALT + click] to Exchange Locator Positions':
        'Đưa Locator về vùng chọn\\nDùng [ALT + nhấp chuột] để đổi chỗ hai Locator',

    # ---- mixer ----
    'Send 1': 'Send 1',
    'Send 2': 'Send 2',
    'Send 3': 'Send 3',
    'Send 4': 'Send 4',
    'Send Bus %d': 'Send Bus %d',
    'Insert 1': 'Insert 1',
    'Send on/off': 'Bật/Tắt Send',
    'Send Volume': 'Send Volume',
    'Insert [Channel Latency Overview]': 'Insert',
    'Insert & Strip Effects': 'Insert & Strip Effects',
    'Insert Effect': 'Insert Effect',
    'Change Insert Effect Configuration': 'Đổi cấu hình Insert Effect',
    'Channel Batch': 'Channel Batch',
    'Channel Destinations': 'Đích Channel',
    'Channel is Linked in Group %d': 'Channel đã liên kết trong Group %d',
    'VCA Tracks': 'VCA Track',
    'Stereo Dual Panner (Remote Control Devices only)':
        'Panner Stereo Dual (Chỉ dành cho Remote Control Device)',
    'Are you sure you want to assign channel volume to all cue sends?':
        'Bạn có chắc muốn gán Volume của Channel cho tất cả Cue Send không?',
    '"%s" will be removed from the link group with VCA Channel.\\nDo you want to keep the combined automation?':
        '"%s" sẽ bị gỡ khỏi Link Group cùng với VCA Channel.\\nGiữ Automation đã gộp không?',
    'The link group "%s" will be removed.\\nDo you want to keep the combined automation?':
        'Link Group "%s" sẽ bị gỡ.\\nGiữ Automation đã gộp không?',
    'Keep Combined Automation and Remove from Link Group':
        'Giữ Automation đã gộp và gỡ khỏi Link Group',
    'Combine Automation of VCA and Connected Channels':
        'Gộp Automation của VCA và Channel đã nối',
    'A feedback connection has been reset for channel "%s".':
        'Đã đặt lại kết nối Feedback của Channel "%s".',
    'Failed to parse VST Parameters Structure:\\n\\n%s\\nContext: %s':
        'Không đọc được cấu trúc VST Parameters:\\n\\n%s\\nNgữ cảnh: %s',
    'First channel that is used for channel rotation':
        'Channel đầu tiên để xoay Channel',
    'Input/Output routing and MIDI channel are set up correctly for playing':
        'Input/Output Routing và MIDI Channel đã chuẩn để phát',
    'Drag to Move EQ Band Settings\\nHold [ALT] to Copy':
        'Kéo để chuyển cài đặt EQ Band\\nGiữ [ALT] để sao chép',
    "Bus '%s' has settings you might want to keep! Delete anyway?":
        "Bus '%s' có cài đặt bạn muốn giữ! Xóa luôn?",
    'Move Channel Strip to Post-Inserts Position':
        'Chuyển Channel Strip tới Post-Inserts',
    'Post-Fader Send.\\nClick to move to pre-fader position.':
        'Send Post-Fader.\\nNhấp để chuyển sang Pre-Fader.',
    "Sends for channel '%s' have been discarded. This program version does not support sends in this type of channel.":
        "Send của Channel '%s' đã bỏ. Phiên bản này không hỗ trợ Send cho loại Channel này.",
    'The channel panner MixConvert has automatically been replaced by MixConvert V6 for Channel "%s". Your project may sound differently.':
        'Panner MixConvert đã tự đổi sang MixConvert V6 cho Channel "%s". Project có thể nghe khác.',
    'The connection could not be created, as the destination cannot be modulated. Modulation is restricted to automatable parameters of audio-related channels/tracks.':
        'Không tạo được kết nối vì đích không nhận Modulation. Chỉ tham số nhận Automation của Channel/Track Audio mới nhận Modulation.',
    'The destination parameter could not be selected, as the destination cannot be modulated. Modulation is restricted to automatable parameters of audio-related channels/tracks.':
        'Không chọn được tham số đích vì đích không nhận Modulation. Chỉ tham số nhận Automation của Channel/Track Audio mới nhận Modulation.',
    'Show/Hide Modulation Connections\\nIndicates if connections are active':
        'Hiện/Ẩn kết nối Modulation\\nCho biết kết nối nào đang chạy',
    'A new modulation connection has been created.':
        'Đã tạo kết nối Modulation mới.',
    'The Control Room is disabled! Do you want to enable it?':
        'Control Room đang tắt! Bật lên không?',
    'Are you sure you want to remove all modulation connections?':
        'Bạn có chắc muốn gỡ hết kết nối Modulation không?',

    # ---- media ----
    '- %i audio file(s) with invalid length inside the AAF file':
        '- %i file Audio sai độ dài trong file AAF',
    '- %i unresolved media reference(s) inside the AAF file':
        '- %i tham chiếu Media không tìm được trong file AAF',
    '- A wrong project bit rate will affect copied and consolidated audio files':
        '- Bit Rate của Project sai sẽ ảnh hưởng file Audio sao chép và gộp',
    "- The 'Export All to One File' option automatically converts wrong settings and file types and splits multi-channel files":
        "- Tùy chọn 'Export tất cả vào một file' tự chuyển cài đặt và loại file sai, đồng thời tách file đa kênh",
    '- The AAF file contains clips with different frame rates. Some clips must be aligned after import.':
        '- File AAF chứa Clip khác Frame Rate. Cần căn lại một số Clip sau khi Import.',
    'A setup information file is available for this script. Do you want to open this file?':
        'Có file thông tin thiết lập cho Script này. Mở file này không?',
    'ASIO-Guard has been disabled, because the ASIO Buffer Size is too large for the selected ASIO-Guard Level.\\n\\nIn Studio > Studio Setup > VST Audio System, you may want to select a smaller ASIO Buffer Size or a higher ASIO-Guard Level.':
        'ASIO-Guard đã tắt vì ASIO Buffer quá lớn so với mức ASIO-Guard đã chọn.\\n\\nTrong Studio > Thiết lập Studio > VST Audio System, hãy chọn ASIO Buffer nhỏ hơn hoặc mức ASIO-Guard cao hơn.',
    'Audio in musical mode cannot be sliced.\\nDo you want to disable musical mode?':
        'Audio ở chế độ Musical không Slice được.\\nTắt chế độ Musical không?',
    'Cannot replace audio in this video file.\\nPlease close all applications that are using this video file and try again!':
        'Không thay được Audio trong file Video này.\\nHãy đóng mọi ứng dụng đang dùng file Video này rồi thử lại!',
    'Copies of the selected video files with replaced audio are created.':
        'Tạo bản sao file Video đã chọn kèm Audio đã thay.',
    'Could not copy the audio data into the Clip Package!':
        'Không sao chép được dữ liệu Audio vào gói Clip!',
    'Could not extract audio stream %d of file ':
        'Không trích được Audio Stream %d của file ',
    'Could not open the file for reading.\\nIs the file already opened by another program?':
        'Không mở được file để đọc.\\nCó phải file đang mở ở chương trình khác không?',
    'Creates a single audio file from multiple selected tracks, events/parts from different tracks or from instrument/MIDI tracks with multiple outputs.':
        'Tạo một file Audio từ nhiều Track đã chọn, Event/Part khác Track, hoặc Instrument Track/MIDI Track có nhiều đầu ra.',
    'Determines how far before the actual hitpoint position the audio event is sliced':
        'Xác định Audio Event Slice trước vị trí Hitpoint thực tế bao xa',
    'Disk Cache Load\\nClick to Show Audio Performance Panel':
        'Mức Disk Cache\\nNhấn để hiện Bảng Hiệu năng Audio',
    'Do you want to convert the sample rate of clips in musical mode?\\nNote that converting them will not affect playback.':
        'Muốn chuyển Sample Rate của Clip ở chế độ Musical không?\\nChuyển xong vẫn phát như cũ.',
    'Error during file copy! The operation must be canceled!':
        'Lỗi khi sao chép file! Phải hủy thao tác!',
    'Export Clip Based Volume (OMF2.0 only)':
        'Export Volume theo Clip (chỉ OMF2.0)',
    'Flatten Real Time Processing (VariAudio and Warp)':
        'Giữ cố định xử lý thời gian thực (VariAudio và Warp)',
    'Select the media types for which the attribute settings will be displayed in the Inspector':
        'Chọn loại Media để hiện cài đặt thuộc tính trong Inspector',
    'Sorry, a timeout occurred during real time audio export.':
        'Rất tiếc, Export Audio thời gian thực bị quá giờ.',
    'The application was terminated with an error while executing the following file:':
        'Ứng dụng bị buộc đóng do lỗi khi chạy file sau:',
    'There are media files missing!\\nDo you want to keep the file description?':
        'Có File Media thiếu!\\nGiữ lại mô tả file không?',
    'You need to define the tempo of the audio clip before setting musical mode!':
        'Cần đặt Tempo của Audio Clip trước khi bật chế độ Musical!',
    'Reaching the 2GB limit of the OMF file format, some media will be missing...':
        'File OMF đã chạm giới hạn 2GB, sẽ thiếu một số Media...',
    'Warning: You cannot undo this operation!\\nOffline process histories will be removed.\\nAll edits will be frozen!':
        'Cảnh báo: Không hoàn tác được thao tác này!\\nLịch sử xử lý Offline sẽ mất.\\nMọi chỉnh sửa sẽ Freeze!',

    # ---- music-theory / notation ----
    'Allow 4-Note Chords':
        'Cho phép hợp âm 4 nốt',
    'As incoming MIDI Channels seem to be rotating, you should consider to create and use a Note Expression Input Device':
        'Vì MIDI Channel đầu vào xoay vòng, bạn nên tạo và dùng một thiết bị Note Expression Input',
    'Define chord by text input and add new chord with [Tab]':
        'Gõ tên hợp âm rồi nhấn [Tab] để thêm hợp âm mới',
    'Apply major chord with a major 7 and an augmented 5 to selection':
        'Áp dụng hợp âm trưởng với nốt 7 trưởng và nốt 5 tăng vào vùng chọn',
    'Insert a major chord with a major 7 and an augmented 5':
        'Chèn hợp âm trưởng với nốt 7 trưởng và nốt 5 tăng',
    'Previous & Next Chord':
        'Chord liền trước & kế tiếp',
    'Primary type is used for the main chord symbol':
        'Dùng loại chính cho ký hiệu hợp âm chính',
    'Scale Assistant: Toggle Snap Pitch Editing':
        'Scale Assistant: Bật/Tắt Snap khi sửa Pitch',
    'Set the root note of the scale':
        'Đặt Root Note của Scale',
    'You cannot remove the root note.':
        'Không gỡ được Root Note.',
    'The selected chords do not correspond to any scale':
        'Hợp âm đã chọn không khớp với Scale nào',
    'This key assignment is already used by "%s". Do you want to reassign this key? Note that the previous assignment will be lost.':
        'Phím này đã gán cho "%s". Gán lại không? Gán cũ sẽ mất.',
    'This option effectively takes precedence over showing cautionary accidentals on notes in the same or different octaves in the following bar. If this option is set to show a cautionary either with or without parentheses, then other cautionary accidentals that would otherwise appear later in the bar are suppressed.':
        'Tùy chọn này ưu tiên hơn việc hiện dấu hóa nhắc lại cho nốt cùng hoặc khác quãng tám ở Bar sau. Nếu đã chọn hiện dấu nhắc lại (có hoặc không có ngoặc), các dấu hóa nhắc lại khác trong Bar sẽ ẩn.',
    'This project contains a Chord Track. It cannot be displayed or edited. Tracks following the Chord Track may not be freely editable within the editors.':
        'Project này có Chord Track. Track đó không hiện và không sửa được. Track theo Chord Track có thể không sửa tùy ý trong Editor.',
    'To have initial states sent, open the Input Routing menu and select your Note Expression Input Device':
        'Để gửi trạng thái ban đầu, mở menu Input Routing và chọn thiết bị Note Expression Input',
    'Use Common Time Note Grouping for Cut Common Time Signatures':
        'Dùng gom nhóm Note Common Time cho số chỉ nhịp Cut Common Time',
    'When bar numbers are positioned at barlines, you may prefer dynamics to be placed closer to the staff than bar numbers, or vice versa. This has no effect for bar numbers centered on the bar, which are always placed outside dynamics.':
        'Khi số Bar đặt tại vạch nhịp, bạn có thể đặt Dynamics gần khuông nhạc hơn số Bar hoặc ngược lại. Không áp dụng với số Bar căn giữa Bar, luôn nằm ngoài Dynamics.',
    "Ruler Display Type has been changed to \\'Bar + Beats\\'.  This is required for Metronome Click Pattern Emphasis.":
        "Kiểu hiển thị Ruler đã đổi thành 'Bar + Beats'.  Cần kiểu này để làm nổi bật Pattern Click Metronome.",
    'Pitch Notation':
        'Ký âm Pitch',

    # ---- ui / project / general ----
    '"%s" is already used as key command by "%s->%s".\\nDo you want to reassign this existing key command?':
        '"%s" đã dùng làm phím tắt cho "%s->%s".\\nBạn có muốn gán lại phím tắt này không?',
    'Assign selected map to active track\\nUse [Click + Hold] or [ALT + Click] to follow map selection permanently.':
        'Gán Map đã chọn cho Track đang bật\\nDùng [nhấp chuột + giữ] hoặc [ALT + nhấp chuột] để luôn theo lựa chọn Map.',
    'Assign selected map to active track\\nUse [Click + Hold] or [ALT + Click] to deactivate.':
        'Gán Map đã chọn cho Track đang bật\\nDùng [nhấp chuột + giữ] hoặc [ALT + nhấp chuột] để tắt.',
    'Click and drag this page to move or copy it, or to swap it with another page.':
        'Nhấp và kéo trang này để di chuyển, sao chép hoặc đổi chỗ với trang khác.',
    'Create new empty Track Version and assign common version ID':
        'Tạo Track Version mới còn trống và gán ID chung cho các Version',
    'Do you really want to leave the page and discard your input?':
        'Bạn có muốn rời trang và bỏ phần đã nhập không?',
    'Learn mode: Assign the destination by clicking a parameter in your project.':
        'Chế độ Learn: Nhấp một tham số trong Project để gán đích.',
    'The Key Combination <%s> assigned to the Command <%s> is not currently available':
        'Tổ hợp phím <%s> đã gán cho lệnh <%s> hiện không dùng được',
    'The On-Screen Keyboard filtered this Key Command.':
        'Bàn phím ảo đã lọc phím tắt này.',
    'The connection could not be created, as the destination does not belong to this effect. Make sure to assign a destination that belongs to this effect.':
        'Không tạo được kết nối vì đích không thuộc Effect này. Hãy gán đích thuộc Effect này.',
    'The destination parameter could not be selected, as the destination does not belong to this effect. Make sure to assign a destination that belongs to this effect.':
        'Không chọn được tham số đích vì đích không thuộc Effect này. Hãy gán đích thuộc Effect này.',
    'Right-click for control setting.  |  Activate Learn mode for control assignment and additional options.':
        'Nhấp chuột phải để cài đặt điều khiển.  |  Bật chế độ Learn để gán điều khiển và xem thêm tùy chọn.',
    'Popup Toolbar (static one with modifier click)':
        'Nhấn phím Modifier + nhấp chuột để mở thanh công cụ cố định',
    'This computer has multiple network interfaces. Please determine which \\ninterface is connected to the Nuendo workgroup and select the \\ncorresponding IP address. \\n\\nThe subnet mask specifies in which range broadcast messages \\nare sent to identify other Nuendo workstations. The default subnet mask \\nis a common choice, please adopt it for your specific network adapter.\\n\\nTo reopen this dialog, deactivate the network and activate it again.':
        'Máy tính có nhiều card mạng. Hãy xem card nào đang nối vào nhóm Nuendo\\nrồi chọn IP \\ntương ứng. \\n\\nSubnet mask quyết định phạm vi gửi bản tin broadcast \\nđể tìm các máy Nuendo khác. Subnet mask mặc định \\nlà lựa chọn thường dùng, cứ giữ nguyên cho card mạng.\\n\\nĐể mở lại hộp thoại này, hãy tắt mạng rồi bật lại.',
    'A label field is linked to one or more controls on the surface and will automatically generate its text once the controls are mapped.':
        'Trường nhãn liên kết với một hoặc nhiều Control trên Surface và sẽ tự tạo chữ khi các Control được Mapping.',
    'Allows you to specify a range in the source project to be imported':
        'Chọn vùng trong Project nguồn để Import',
    'Allows you to toggle the state of the mapped function. If the hardware control or the %s function are in toggle mode, use the jump mode instead.':
        'Đổi trạng thái của chức năng đã Mapping. Nếu điều khiển phần cứng hoặc chức năng %s ở chế độ Bật/Tắt, hãy dùng chế độ Jump.',
    'Check your naming scheme, as it does not provide unique names for the files.':
        'Kiểm tra lại quy tắc đặt tên, vì nó không tạo tên duy nhất cho các file.',
    'The edit operations Cut, Delete, Draw, and Paste are not added to your favorites.':
        'Cut, Delete, Draw và Paste không thêm được vào Favorite.',
    'Placement Mode: Add your control to the surface.':
        'Chế độ đặt: Thêm điều khiển vào Surface.',
    'A macro cannot contain another macro including itself!':
        'Một Macro không thể chứa Macro khác, kể cả chính nó!',
    'Compares the value of the %s function to the control value, and approaches the two values in a smooth way. As soon as the values are identical, the function follows the control value.':
        'So sánh giá trị của chức năng %s với giá trị nút xoay, rồi đưa hai giá trị lại gần nhau cho mượt. Khi hai giá trị bằng nhau, chức năng sẽ bám theo nút xoay.',
    'Error during operation: %s \\nAll files created so far will be deleted.':
        'Lỗi khi thực hiện: %s \\nTất cả file đã tạo sẽ bị xóa.',
    'Shifting must be aborted, because the master track would be shifted into the negative!':
        'Phải dừng dời vì Master Track sẽ lùi qua điểm bắt đầu!',
    'The algorithm has been switched automatically to "Standard Solo" because VariAudio editing requires this.':
        'Thuật toán đã tự chuyển sang "Standard Solo" vì cần sửa VariAudio.',
    'The Clip Package will not contain a preview, because the project is not active.':
        'Gói Clip sẽ không có Preview vì Project chưa bật.',
    '"%s" will be removed from the link group.\\nDo you want to keep the combined automation?':
        '"%s" sẽ bị gỡ khỏi Link Group.\\nBạn có muốn giữ Automation kết hợp không?',
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
for k, v in list(changed.items())[:15]:
    print(f'  {k[:58]!r}')
    print(f'      {vi.get(k, "")[:100]!r}')
    print(f'   -> {v[:100]!r}')

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
