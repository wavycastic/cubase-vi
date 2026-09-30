"""Round 76: manual reading fixes - project/network, music-theory, media sentences.

Usage:
  python tools/fix_reading76.py
  python tools/fix_reading76.py --write
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
    # 1. project / network
    'Add selected Users to Permission Preset':
        'Thêm User đã chọn vào Preset Permission',
    'Remove selected Users from Permission Preset':
        'Gỡ User đã chọn khỏi Preset Permission',
    'Could not reconnect project to existing network files - unsharing project.':
        'Không kết nối lại được Project với file mạng hiện có - hủy chia sẻ Project.',
    'It is not possible to create a shared copy if the timebase of the tracks do not match.\\nA real copy was created instead.':
        'Không thể tạo bản sao chia sẻ nếu Timebase của các Track không khớp.\\nĐã tạo bản sao độc lập để thay thế.',
    'Merge Active Project To Selected Network Project':
        'Gộp Project đang bật vào Project mạng đã chọn',
    'Please select one of your shared projects.':
        'Vui lòng chọn một Project đã chia sẻ.',
    'Progress of active network transfers:':
        'Tiến trình truyền mạng đang chạy:',
    'Project Setup cannot be opened while recording.':
        'Không mở được thiết lập Project khi đang ghi.',
    'Script Archive has been imported, but included user mappings had to be skipped due to an error.':
        'Kho Script đã Import, nhưng Mapping người dùng kèm theo bị bỏ qua do lỗi.',
    'The Auto Saves folder cannot be created!\\nThere might be a problem of write permission.':
        'Không tạo được thư mục Auto Save!\\nCó thể do không có quyền ghi.',
    'This backup project cannot be renamed!\\nThere might be a problem of write permission.':
        'Bản sao lưu Project này không đổi tên được!\\nCó thể do không có quyền ghi.',
    'This option deletes the preferences of current and older program installations and initializes the program with factory settings. Please be aware that all your custom settings will be removed. This operation cannot be undone.':
        'Tùy chọn này xóa hết Preferences của bản cài đặt hiện tại và các bản cũ, rồi đặt lại chương trình về cài đặt Factory. Lưu ý toàn bộ cài đặt tùy chỉnh sẽ mất. Thao tác này không hoàn tác được.',
    'This option disables your custom preferences and initializes the program with factory settings. Your preferences are available after restarting the program.':
        'Tùy chọn này tạm tắt Preferences tùy chỉnh và đặt lại chương trình về cài đặt Factory. Preferences sẽ dùng lại được sau khi khởi động lại chương trình.',
    'This option uses the preferences currently stored in the program.':
        'Tùy chọn này dùng Preferences đang lưu trong chương trình.',
    'Timebase cannot be changed because there are shared copies used on other tracks!':
        'Không đổi được Timebase vì Track khác đang dùng các bản sao chia sẻ!',
    'To identify yourself in the network, you need a unique user name.\\nThis is usually supplied by the network administrator.\\nDo you want to enter the user name now?':
        'Để nhận diện trong mạng, bạn cần tên người dùng duy nhất.\\nThường do quản trị mạng cấp.\\nNhập tên người dùng ngay bây giờ không?',
    'Track Download into a shared project is not allowed.':
        'Không tải được Track vào Project đã chia sẻ.',
    'You cannot delete the active profile. Please select or activate another profile.':
        'Không xóa được Profile đang bật. Hãy chọn hoặc bật Profile khác.',
    'You may be prompted to establish a network or hardware connection.':
        'Bạn có thể phải mở kết nối mạng hoặc phần cứng.',

    # 2. music-theory wording
    '"Pitch Visibility: Select Next Option" not possible because there are no note events in the editor':
        'Không thể "Hiển thị Pitch: Chọn tùy chọn kế tiếp" vì Editor không có Note Event nào',
    "'X' Chords Mute Notes on Tracks That are in Follow Chord Track Mode":
        "Hợp âm 'X' sẽ Mute nốt trên Track ở chế độ Follow Chord Track",
    'Accidentals apply only to one note, and are shown on all modified notes; naturals are not shown, and notes modified by the key signature do not show accidentals.':
        'Dấu hóa chỉ tính cho một nốt, hiện trên mọi nốt đã đổi dấu; dấu bình không hiện, nốt đổi theo hóa âm cũng không hiện dấu hóa.',
    'Accidentals apply only to one note, and are shown on all notes, including unmodified notes (naturals) and notes modified by the key signature.':
        'Dấu hóa chỉ tính cho một nốt, hiện trên mọi nốt, kể cả nốt không đổi dấu (dấu bình) và nốt đổi theo hóa âm.',
    'Apply the currently effective chord on the chord track to the selected notes':
        'Áp dụng hợp âm Chord Track đang dùng cho các nốt đã chọn',
    'As incoming MIDI Channels seem to be rotating, you should consider to create and use a Note Expression Input Device':
        'Vì MIDI Channel đầu vào cứ đổi vòng, bạn nên tạo và dùng một thiết bị Note Expression Input',
    'Add the chord of the selected notes to the chord track':
        'Thêm hợp âm của nốt đã chọn vào Chord Track',
    'Analyze notes and add chords to chord track':
        'Phân tích nốt rồi thêm hợp âm vào Chord Track',
    'Cannot add more tracks. The chord track count is at the limit.':
        'Không thêm được Track. Chord Track đã đạt giới hạn.',
    'Cannot Edit VariAudio: No Note Segments Detected':
        'Không sửa được VariAudio: không thấy đoạn nốt nào',
    'Choose this option if the track data does not match the chords displayed on the chord track.':
        'Chọn nếu dữ liệu Track không khớp với hợp âm hiện trên Chord Track.',
    'Choose this option if the track data is already synchronized with the chord track.':
        'Chọn nếu dữ liệu Track đã đồng bộ với Chord Track.',
    'Chord & Scale:\\nThe pitch matches the current chord and scale. No added tension at all.':
        'Hợp âm & Scale:\\nPitch khớp cả hợp âm và Scale hiện tại. Không thêm Tension nào.',
    'Scale:\\nThe pitch is in the current scale but not in the current chord. A good pitch for melody that adds some tension.':
        'Scale:\\nPitch nằm trong Scale hiện tại nhưng ngoài hợp âm hiện tại. Pitch tốt cho giai điệu, tạo thêm chút Tension.',
    'None:\\nThe pitch is not in the current chord or the current scale. This pitch adds a strong tension.':
        'None:\\nPitch không nằm trong hợp âm hay Scale hiện tại. Pitch này tạo Tension mạnh.',
    'Chord:\\nThe pitch matches the current chord but is not in the current scale. Unusual - do the current chord and scale match?':
        'Hợp âm:\\nPitch khớp hợp âm hiện tại nhưng ngoài Scale hiện tại. Khác thường - hợp âm và Scale hiện tại có khớp không?',
    'Chord Pad Output Mode\\nOn: Output is sent to all record-enabled or monitored tracks.\\nOff: Output is sent exclusively to record-enabled or monitored tracks where Input Routing is set to Chord Pads.':
        'Chế độ đầu ra Chord Pad\\nBật: Đầu ra gửi tới mọi Track sẵn sàng ghi hoặc Monitor.\\nTắt: Đầu ra chỉ gửi riêng tới Track sẵn sàng ghi hoặc Monitor có Input Routing là Chord Pad.',
    'Chord symbols appear either above the staves belonging to specific instruments as defined in Instrument Settings, or above the top staff in the system.':
        'Ký hiệu hợp âm hiện trên khuông nhạc của nhạc cụ đã đặt trong cài đặt Instrument, hoặc trên khuông nhạc trên cùng của dòng nhạc.',
    'Define chord by text input and add new chord with [Tab]':
        'Gõ chữ để định nghĩa hợp âm rồi thêm hợp âm mới bằng [Tab]',
    'Double-Click opens Note Expression Editor On/Off':
        'Nhấp đúp để mở/tắt Note Expression Editor',
    'Hold chord until the next chord is played':
        'Giữ hợp âm tới khi hợp âm kế tiếp phát',
    "If this option is activated, the Score Editor will produce, assuming 'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', a dotted slash followed by an undotted slash in 5/8, but five slashes in 5/4.":
        'Nếu bật tùy chọn này và "Thời lượng tối đa cho dấu gạch chéo nhịp" đặt thành "Note 1/4 (nốt đen)", Score Editor sẽ tạo một gạch có chấm rồi một gạch không chấm ở 5/8, nhưng năm gạch ở 5/4.',
    "If this option is activated, the Score Editor will produce, assuming 'Maximum Duration for Rhythmic Slashes' is set to '1/4' Note (Crotchet)', two dotted slashes in 6/8, but six undotted slashes in 6/4.":
        'Nếu bật tùy chọn này và "Thời lượng tối đa cho dấu gạch chéo nhịp" đặt thành "Note 1/4 (nốt đen)", Score Editor sẽ tạo hai gạch có chấm ở 6/8, nhưng sáu gạch không chấm ở 6/4.',
    'Last played Chord Pad stays active even after its remote key is released':
        'Chord Pad vừa phát vẫn bật dù đã nhả phím Remote',
    'Move the second highest note an octave lower':
        'Đưa nốt cao thứ hai xuống một quãng tám',
    'Move the third highest note an octave lower':
        'Đưa nốt cao thứ ba xuống một quãng tám',
    'Move the second and fourth highest notes an octave lower':
        'Đưa nốt cao thứ hai và thứ tư xuống một quãng tám',
    'Inserts a scale that corresponds to all selected chords':
        'Chèn Scale khớp mọi hợp âm đã chọn',
    'This project contains a Chord Track. It cannot be displayed or edited. Tracks following the Chord Track may not be freely editable within the editors.':
        'Project này có Chord Track. Track đó không hiện hay sửa được. Các Track theo Chord Track có thể không sửa tùy ý trong Editor.',
    'Update scale events automatically when the chord track is edited':
        'Tự động cập nhật Scale Event khi sửa Chord Track',
    'Voicings cannot be applied. Too many notes found for at least one chord.':
        'Không áp được Voicing. Ít nhất một hợp âm có quá nhiều nốt.',
    'Warning: No processing for parts in Follow Chord Track mode':
        'Cảnh báo: Không xử lý các Part ở chế độ Follow Chord Track',
    'You are recording in Note Expression Overdub Mode - MIDI Note Input is deactivated.':
        'Bạn đang ghi ở chế độ Note Expression Overdub - MIDI Note Input đã tắt.',
    "To save the project as is, click 'Save'. Note that the project will no longer be compatible with program versions older than 13.0.30.":
        "Để giữ nguyên Project, nhấp 'Lưu'. Lưu ý Project sẽ không mở được trên bản chương trình cũ hơn 13.0.30.",
    'Trills Where Upper Note Is Altered by Accidental Present in Key Signature':
        'Trill khi nốt trên đổi theo dấu hóa có trong hóa âm',
    'All notes are sent on one channel. Please set up your Note Expression Input Device correctly.':
        'Mọi nốt gửi chung một Channel. Hãy thiết lập đúng thiết bị Note Expression Input.',
    'Time between Output Mapping and note event':
        'Thời gian giữa Output Mapping và Note Event',
    'Notes Eligible for a Cautionary Accidental Following an Enharmonically Equivalent Note':
        'Nốt được hiện dấu hóa nhắc lại sau nốt đồng âm',
    'On the First Occurrence of the Same Note in the Following Bar, Either at the Same or a Different Octave':
        'Ở lần đầu nốt đó xuất hiện trong Bar tiếp theo, dù cùng hay khác quãng tám',

    # 3. media sentences
    'There was a file error during bounce!\\nThe function had to be canceled!':
        'Lỗi file khi Bounce!\\nThao tác đã bị hủy!',
    'There was a problem accessing the following file:\\n\\n%s\\n\\nIgnore this file or ignore all files of the same file type (%s)?':
        'Không mở được file sau:\\n\\n%s\\n\\nBỏ qua file này hay bỏ qua mọi file cùng loại (%s)?',
    'These file(s) or folder(s) could not be copied to:':
        'Không sao chép được các file/thư mục này tới:',
    'These file(s) or folder(s) could not be deleted from disk:':
        'Không xóa được các file/thư mục này khỏi đĩa:',
    'These file(s) or folder(s) could not be moved into:':
        'Không chuyển được các file/thư mục này vào:',
    'This is the recommended setting for efficient audio processing performance. This leads to reasonable ASIO-Guard Latency and memory usage.':
        'Đây là cài đặt khuyên dùng để xử lý Audio hiệu quả. Cho độ trễ ASIO-Guard và mức dùng bộ nhớ hợp lý.',
    "This project file contains surround channels which are not supported by this program version. All surround channels are switched to 'stereo'.":
        "File Project này có Channel Surround mà phiên bản này không hỗ trợ. Mọi Channel Surround chuyển thành 'Stereo'.",
    'This will remove all columns in the Results list (except Name) for this combination of media types.':
        'Thao tác này sẽ xóa mọi cột trong danh sách kết quả (trừ Tên) với tổ hợp loại Media này.',
    'Threshold for dialog-gated loudness measurement. If less speech is detected in audio, program-gated measurement is used.':
        'Ngưỡng đo Loudness theo hội thoại. Nếu ít giọng nói trong Audio, phép đo sẽ theo Program.',
    'Threshold for dialogue-gated loudness measurement. If less speech is detected in audio, program-gated measurement is used':
        'Ngưỡng đo Loudness theo hội thoại. Nếu ít giọng nói trong Audio, phép đo sẽ theo Program',
    'Use a suitably equipped ASIO audio card as timecode source (not all ASIO cards support this!)':
        'Dùng card Audio ASIO tương thích làm nguồn Timecode (không phải card ASIO nào cũng hỗ trợ!)',
    'Use this setting for the highest audio processing performance (to play back many VST Instruments, for example). This leads to increased ASIO-Guard Latency and memory usage.':
        'Dùng cài đặt này để xử lý Audio mạnh nhất (ví dụ: phát nhiều VST Instrument). Độ trễ ASIO-Guard và mức dùng bộ nhớ sẽ tăng.',
    'Use this setting to set the ASIO-Guard Latency to the lowest level (to record automation, for example). This leads to reduced audio processing performance.':
        'Dùng cài đặt này để hạ độ trễ ASIO-Guard xuống thấp nhất (ví dụ: để ghi Automation). Hiệu năng xử lý Audio sẽ giảm.',
    'With format 2, the outputs are assigned to the default bus instead of mono child busses.':
        'Với định dạng 2, các đầu ra gán vào Bus mặc định thay vì các Bus con Mono.',
    "You can add cues on the 'Control Room' tab in the 'Audio Connections' window.":
        "Thêm Cue trên thẻ 'Control Room' trong cửa sổ 'Audio Connections'.",
    'You cannot apply this preset to an audio clip without losing its VariAudio edits. Do you want to continue?':
        'Không áp được Preset này cho Audio Clip mà không mất sửa đổi VariAudio. Bạn có muốn tiếp tục không?',
    "You cannot freeze a track with modulators.\\nTo reduce CPU load, you can use 'Render in Place' and disable the track.":
        "Không Freeze được Track có Modulator.\\nMuốn nhẹ CPU, dùng 'Render in Place' rồi tắt Track.",
    'You cannot freeze an inactive instrument!':
        'Không Freeze được nhạc cụ đang tắt!',
    'You have activated the Steinberg Audio Power Scheme.\\n\\nThe Steinberg Audio Power Scheme optimizes Windows power handling for best possible audio performance at\\nlow-latency ASIO settings. However, this also increases the power consumption of the computer.\\n\\nIf power consumption is a concern, please disable this option and increase the buffer size of your audio hardware.\\n\\nFurther information on the Steinberg Audio Power Scheme can be found in the Steinberg Knowledge Base.':
        'Bạn đã bật Steinberg Audio Power Scheme.\\n\\nSteinberg Audio Power Scheme tối ưu điện Windows để Audio chạy tốt nhất ở\\nASIO độ trễ thấp. Nhưng máy sẽ tốn điện hơn.\\n\\nNếu ngại tốn điện, hãy tắt tùy chọn này và tăng buffer của thiết bị Audio.\\n\\nĐọc thêm về Steinberg Audio Power Scheme trong Steinberg Knowledge Base.',
    'You need to define the tempo of the audio clip before setting musical mode!':
        'Cần định nghĩa Tempo của Audio Clip trước khi bật chế độ Musical!',
    'it is used in another Pool and it has more than one edit version!':
        'nó đang dùng trong Pool khác và có nhiều bản chỉnh sửa!',
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
