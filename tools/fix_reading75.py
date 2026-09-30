"""Round 75: manual reading fixes - plain everyday Vietnamese for long messages.

Usage:
  python tools/fix_reading75.py
  python tools/fix_reading75.py --write
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
    # 1. External Plug-in + export case
    'External plug-in is used. Audio-Mixdown must be done in real time!':
        'Đang dùng External Plug-in. Audio-Mixdown phải chạy theo thời gian thực!',
    'The project contains no video. A black screen is exported.':
        'Project không có Video. Màn hình đen sẽ được Export.',

    # 2. read-only / preset / pool file names
    'The project directory is read only!\\n\\nPlease make a new selection!':
        'Thư mục Project chỉ đọc!\\n\\nVui lòng chọn mục khác!',
    'There already is a preset named\\n"%s"!\\nDo you want to overwrite it?':
        'Đã có Preset tên\\n"%s"!\\nBạn có muốn ghi đè lên nó không?',
    'There already is a preset named\\n"%s"!\\nIt is read only. You cannot overwrite it!':
        'Đã có Preset tên\\n"%s"!\\nNó đang ở chế độ chỉ đọc. Bạn không thể ghi đè lên nó!',
    'A file named\\n%s\\nalready exists in the Pool.\\nIt is not possible to replace it.\\nPlease use another name or another location.':
        'File tên\\n%s\\nđã có trong Pool.\\nKhông thay thế được file này.\\nHãy dùng tên khác hoặc vị trí khác.',

    # 3. failed/request/loudness leftovers
    'Configuration data request failed.':
        'Không lấy được dữ liệu cấu hình.',
    'Revision data request failed.':
        'Không lấy được dữ liệu bản sửa đổi.',
    'The tracks in this folder are not completely in sync.\\nGroup editing could fail!':
        'Các Track trong thư mục này chưa đồng bộ hẳn.\\nSửa nhóm có thể lỗi!',
    'There can be only one master automation track!':
        'Chỉ có một Master Automation Track duy nhất!',
    'There is only very little recording time left on the disk you selected!\\nDo you want to continue?':
        'Đĩa đã chọn chỉ còn ghi được rất ít!\\nBạn có muốn tiếp tục không?',
    'These were replaced by nearest new color.':
        'Chúng đã được thay bằng màu mới gần nhất.',

    # 4. in-use / exists / rename
    'This External Plug-in "%s" is in use and cannot be removed!':
        'External Plug-in "%s" đang dùng nên không gỡ được!',
    'This Track Version does not exist on these selected tracks:':
        'Track Version này không có trên các Track đã chọn:',
    'This backup project "%s" will be renamed "%s"':
        'Bản sao lưu Project "%s" sẽ đổi tên thành "%s"',
    'This backup project "%s" will be renamed to "%s"':
        'Bản sao lưu Project "%s" sẽ đổi tên thành "%s"',
    'This data requires a Pitchbend Range of at least %d semitones.':
        'Dữ liệu này cần dải Pitchbend ít nhất %d nửa cung.',
    'Select Defined Favorite':
        'Chọn Favorite đã đặt',
    'This is not a Defined Favorite':
        'Đây không phải Favorite đã đặt',
    "This macro is used in another macro ('%s'). Deleting it will remove it from that macro as well.":
        "Macro này đang dùng trong Macro khác ('%s'). Xóa Macro này cũng gỡ nó khỏi Macro đó.",
    'This name is already used by another macro. Macro names must be unique. Please type in a new name.':
        'Tên này đã có Macro khác dùng. Tên Macro phải duy nhất. Vui lòng nhập tên mới.',

    # 5. invalidate -> lam hong
    'This operation may invalidate the VariAudio data.':
        'Thao tác này có thể làm hỏng dữ liệu VariAudio.',
    'This operation will invalidate the VariAudio data.':
        'Thao tác này sẽ làm hỏng dữ liệu VariAudio.',
    "Converting automation data may invalidate existing 'Z-Axis Pan' automation. Do you want to convert it anyway?":
        "Chuyển đổi dữ liệu Automation có thể làm hỏng Automation 'Z-Axis Pan' hiện có. Vẫn chuyển đổi?",
    "Switching '3D Pan Mode' may invalidate existing 'Z-Axis Pan' automation. Please check your automation tracks and use the 'Convert Z-Axis Pan Automation of Selected Tracks' function if needed.":
        "Chuyển 'Chế độ 3D Pan' có thể làm hỏng Automation 'Z-Axis Pan' hiện có. Kiểm tra các Automation Track và dùng chức năng 'Chuyển đổi Automation Z-Axis Pan của các Track đã chọn' nếu cần.",
    'This plug-in will be disabled when Constrain Delay Compensation is active':
        'Plug-in này sẽ tắt khi Constrain Delay Compensation đang bật',

    # 6. project-content sentences
    'This project contains a transpose track. The track will be used for playback, but you cannot remove or edit it.':
        'Project này có Transpose Track. Track đó sẽ phát lại, nhưng bạn không gỡ hay sửa được nó.',
    'This project contains pictures which are not part of your library. \\nDo you want to add them to the library to make them available in other projects?':
        'Project này có hình ảnh ngoài thư viện. \\nThêm chúng vào thư viện để dùng trong các Project khác không?',
    'This project does not contain any notepad data.':
        'Project này không có dữ liệu ghi chú nào.',
    'This will modify the project settings!\\nAll other tracks that have no own settings will be affected as well!\\nDo you want to continue?':
        'Thao tác này sẽ đổi cài đặt Project!\\nMọi Track khác không có cài đặt riêng cũng đổi theo!\\nBạn có muốn tiếp tục không?',
    'This will remove all inactive redo branches.\\n\\nDo you want to continue?':
        'Thao tác này sẽ xóa mọi nhánh Redo không dùng.\\n\\nBạn có muốn tiếp tục không?',
    'This will remove tracks that contain data!\\nDo you want to continue?':
        'Thao tác này sẽ xóa các Track đang có dữ liệu!\\nBạn có muốn tiếp tục không?',
    'This will reset all port names and make all ports visible!':
        'Thao tác này sẽ đặt lại mọi tên cổng và hiện tất cả cổng!',
    "To save your changes for the selected job, please click 'Update Job'.":
        "Để lưu thay đổi của tác vụ đã chọn, hãy nhấp 'Cập nhật tác vụ'.",

    # 7. transport wording
    'Toggle: Cycle follows when locating to Markers':
        'Bật/Tắt: Cycle bám theo khi định vị tới Marker',
    'Toggle between Track View and Meter View':
        'Chuyển giữa chế độ xem Track và Meter',
    'Track %s exceeds the number of tracks supported by the application. The track is kept, but cannot be modified.':
        'Track %s vượt quá số Track ứng dụng hỗ trợ. Track vẫn giữ lại nhưng không sửa được.',
    'Transform events and delete all events not matching the filter':
        'Biến đổi Event và xóa mọi Event không khớp với bộ lọc',
    'Type of newly created events (e.g. when created with Draw Tool)':
        'Loại Event mới tạo (ví dụ: khi tạo bằng công cụ Draw)',
    'Use MIDI Machine Control (set the MIDI ports used below)':
        'Dùng MIDI Machine Control (chọn cổng MIDI bên dưới)',
    'Use the control on your hardware to retrieve its MIDI messages.':
        'Gạt nút trên thiết bị để nhận thông điệp MIDI của nó.',
    'Use the internal mode (when this program is the center of your world)':
        'Dùng chế độ nội bộ (khi phần mềm này là trung tâm)',
    'Video service does not respond. Waiting for video service...':
        'Dịch vụ Video không phản hồi. Đang chờ...',
    'Warning: A control with the defined MIDI message already exists. Please change the MIDI message settings of one of the controls.':
        'Cảnh báo: Đã có nút dùng thông điệp MIDI này. Hãy đổi cài đặt thông điệp MIDI của một trong các nút.',
    'Warning: You must define a MIDI message for this control.':
        'Cảnh báo: Bạn phải đặt một thông điệp MIDI cho nút này.',
    'When deactivated, no timecode is sent to SyncStation MIDI Out':
        'Khi tắt, không có Timecode nào gửi tới SyncStation MIDI Out',
    'When deactivated, no timecode is sent to the host':
        'Khi tắt, không có Timecode nào gửi tới Host',
    'Send MIDI Clock in Stop Mode':
        'Gửi MIDI Clock khi đang dừng',
    'When selected, MIDI Clock will be sent in Stop Mode as well':
        'Khi chọn, MIDI Clock cũng gửi cả khi đang dừng',
    'When selected, sent MIDI Clock will follow cycled project position':
        'Khi chọn, MIDI Clock gửi đi sẽ chạy theo vị trí Project trong Cycle',
    'When selected, sent MIDI Timecode will follow cycled project time':
        'Khi chọn, MIDI Timecode gửi đi sẽ chạy theo thời gian Project trong Cycle',
    'Write protection (a checkmark in this column prevents an entry from being overwritten)':
        'Chống ghi (dấu tích ở cột này giữ mục khỏi bị ghi đè)',
    'You are trying to activate Track Version "%s", id:%d (on track "%s").':
        'Bạn đang bật Track Version "%s", id:%d (trên Track "%s").',
    'You cannot move events in front of the project start time.':
        'Bạn không thể kéo Event ra trước điểm bắt đầu Project.',
    'You must restart the application for the HiDPI setting change to take effect.':
        'Cần khởi động lại ứng dụng để thay đổi cài đặt HiDPI có hiệu lực.',
    'You must restart the application for the language switch to take effect.':
        'Cần khởi động lại ứng dụng để chuyển đổi ngôn ngữ có hiệu lực.',
    'You must restart the application for the processing precision to take effect.':
        'Cần khởi động lại ứng dụng để độ chính xác xử lý có hiệu lực.',
    'You must restart the application for the profile switch to take effect.':
        'Cần khởi động lại ứng dụng để chuyển đổi Profile có hiệu lực.',
    'You must restart the application for these changes to take effect!':
        'Cần khởi động lại ứng dụng để các thay đổi này có hiệu lực!',
    'You should save the project now!\\nFile references in the stored version have become invalid!':
        'Bạn nên lưu Project ngay!\\nTham chiếu file trong bản đã lưu đã hỏng!',
    'by touching it on your controller':
        'bằng cách chạm vào nút đó trên Controller',
    'Return to Start Position on Stop':
        'Quay về vị trí bắt đầu khi dừng',
    "\\'Return to Start Position on Stop\\' has been activated":
        "'Quay về vị trí bắt đầu khi dừng' đã bật",
    "\\'Return to Start Position on Stop\\' has been deactivated":
        "'Quay về vị trí bắt đầu khi dừng' đã tắt",
    '\\nThe previous version of the project has been left unchanged.':
        '\\nPhiên bản trước của Project vẫn giữ nguyên.',

    # 8. record / tempo phrasing
    "Recording starts at the left locator position, or at the 'Punch In' position, if 'Punch In' is activated.":
        "Bắt đầu ghi tại vị trí Locator trái, hoặc tại vị trí 'Punch In' nếu 'Punch In' đang bật.",
    'Remove irregular tempo jumps and smooth the tempo curve':
        'Xóa các đoạn Tempo nhảy bất thường và làm mượt đường cong Tempo',
    'Selecting a different tool will end the tempo detection session. Do you want to continue?':
        'Chọn công cụ khác sẽ kết thúc nhận diện Tempo. Bạn có muốn tiếp tục không?',
    'Shows the marker ID of a marker event displayed on a marker track':
        'Hiện ID Marker của Marker Event trên Marker Track',
    "Start Mode has been changed to \\'Start from Cycle Start\\'":
        "Chế độ Start đã đổi thành 'Bắt đầu từ đầu Cycle'",
    "Start Mode has been changed to \\'Start from Project Cursor Position\\'":
        "Chế độ Start đã đổi thành 'Bắt đầu từ vị trí con trỏ Project'",
    "Start Mode has been changed to \\'Start from Selection Start\\'":
        "Chế độ Start đã đổi thành 'Bắt đầu từ đầu vùng chọn'",
    "Start Mode has been changed to \\'Start from Selection or Cycle Start\\'":
        "Chế độ Start đã đổi thành 'Bắt đầu từ vùng chọn hoặc đầu Cycle'",
    'Tap Tempo - Not possible while recording':
        'Tap Tempo - Không gõ được khi đang ghi',
    'Tap Tempo - Please keep tapping to set tempo':
        'Tap Tempo - Gõ tiếp để đặt Tempo',
    'Tempo Recording Slider (Adjust Slider While in Play Mode)':
        'Thanh trượt ghi Tempo (Chỉnh khi đang phát)',
    'Tempo editing is not possible for editors without project relation.':
        'Không sửa được Tempo trong Editor không thuộc Project.',
    'The detected tempo lies outside the valid tempo range.':
        'Tempo nhận diện nằm ngoài dải Tempo hợp lệ.',
    'The locator range is inverted. Please switch the locators.':
        'Dải Locator bị ngược. Vui lòng hoán đổi hai Locator.',
    'The locator range is not set. Please set the locators.':
        'Dải Locator chưa đặt. Vui lòng đặt các Locator.',
    'The selected material is not suitable for tempo detection.':
        'Đoạn đã chọn không phù hợp để nhận diện Tempo.',
    "Track '%s' has a linear timebase. If you change the project tempo, the events will not follow. This program version does not allow you to switch the timebase.":
        "Track '%s' dùng Timebase tuyến tính. Nếu đổi Tempo của Project, các Event sẽ không bám theo. Phiên bản này không cho đổi Timebase.",
    'Transport stays in Play Mode even if External Timecode Stops':
        'Transport vẫn phát dù Timecode External dừng',
    'Use Metronome Click Pattern Level for Grid Line Emphasis':
        'Dùng mức Click Pattern Metronome để làm nổi bật đường Grid',
    'Zoom Mode has been changed for Definition editing.':
        'Zoom Mode đã đổi để sửa Definition.',
    'Zoom Tool Standard Mode: Horizontal Zooming Only':
        'Chế độ Zoom chuẩn: chỉ Zoom ngang',
    'Tools - Show Horizontal Cross Hair Cursor Line':
        'Công cụ - Hiện đường Cross-Hair ngang',
    'Tools - Show Vertical Cross Hair Cursor Line':
        'Công cụ - Hiện đường Cross-Hair dọc',
    'Insert tempo event at last playback start position':
        'Chèn Tempo Event tại vị trí phát lần trước',
    "Ramps/Curves are not supported on Tracks that are set to MIDI channel 'Any'":
        "Track đặt MIDI Channel là 'Any' không dùng được Ramp/Đường cong",
    'Randomize Parameters. Press [Alt] to limit randomization to parameters used in VST Quick Controls.':
        'Ngẫu nhiên hóa tham số. Nhấn [Alt] để chỉ áp dụng cho tham số dùng trong VST Quick Control.',
    'Remote-Control Focus for VST Quick Controls follows track selection':
        'Remote-Control Focus cho VST Quick Control bám theo Track đã chọn',
    'Rendered files include channel settings, group channel settings, send effect settings, and Master bus settings.':
        'File đã Render gồm cài đặt Channel, Group Channel, Send Effect và Master Bus.',
    'Rendered files include channel settings, group track settings, and send effect settings.':
        'File đã Render gồm cài đặt Channel, Group Track và Send Effect.',
    'Rendered files include insert effect, EQ, and channel strip settings.':
        'File đã Render gồm Insert Effect, EQ và Channel Strip.',
    "Sends for channel '%s' have been discarded. This program version does not support sends in this type of channel.":
        "Send của Channel '%s' đã bị bỏ. Phiên bản này không hỗ trợ Send trong loại Channel này.",

    # 9. mixer connection / port sentences
    'The channel panner MixConvert has automatically been replaced by MixConvert V6 for Channel "%s". Your project may sound differently.':
        'Channel panner MixConvert đã tự thay bằng MixConvert V6 cho Channel "%s". Âm thanh của Project có thể sẽ khác.',
    'The connection could not be created, as a parameter of a VST 2 plug-in cannot be modulated. Use the VST 3 plug-in version instead.':
        'Không tạo được kết nối vì Plug-in VST 2 không nhận Modulation. Hãy dùng bản Plug-in VST 3.',
    'The connection could not be created, as the destination is not part of the channel. Make sure to assign a destination that is part of the channel.':
        'Không tạo được kết nối vì đích không nằm trong Channel này. Hãy gán đích khác trong Channel này.',
    'The destination parameter could not be selected, as a parameter of a VST 2 plug-in cannot be modulated. Use the VST 3 plug-in version instead.':
        'Không chọn được tham số đích vì Plug-in VST 2 không nhận Modulation. Hãy dùng bản Plug-in VST 3.',
    'The destination parameter could not be selected, as the destination is not part of the channel. Make sure to assign a destination that is part of the channel.':
        'Không chọn được tham số đích vì đích không nằm trong Channel này. Hãy gán đích khác trong Channel này.',
    'The connection could not be created, as the destination cannot be modulated. Modulation is restricted to automatable parameters of audio-related channels/tracks.':
        'Không tạo được kết nối vì đích không nhận Modulation. Chỉ tham số Automation được của Channel/Track Audio mới nhận Modulation.',
    'The destination parameter could not be selected, as the destination cannot be modulated. Modulation is restricted to automatable parameters of audio-related channels/tracks.':
        'Không chọn được tham số đích vì đích không nhận Modulation. Chỉ tham số Automation được của Channel/Track Audio mới nhận Modulation.',
    'The selected device port is already used. Selecting the port for this bus will replace any previous connection.':
        'Cổng thiết bị đã chọn đang dùng. Chọn cổng cho Bus này sẽ thay mọi kết nối trước đó.',
    'The selected device port is used exclusively. This connection will be ended. Do you want to continue?':
        'Cổng thiết bị đã chọn đang dùng độc quyền. Kết nối này sẽ bị ngắt. Bạn có muốn tiếp tục không?',
    "This profile requires '3-Layer 3D Pan Mode'. Please select it in the project settings, otherwise 'Z-Axis Pan' automation will be wrong.":
        "Profile này cần '3-Layer 3D Pan Mode'. Hãy chọn trong cài đặt Project, nếu không Automation 'Z-Axis Pan' sẽ sai.",
    'Use this option if the current control is inverted when compared to the actual VST parameter':
        'Dùng tùy chọn này nếu nút hiện tại bị ngược so với tham số VST',
    'VST System Link has been deactivated because of too many receive errors!':
        'VST System Link đã tắt vì lỗi nhận tín hiệu quá nhiều!',
    'You cannot browse VST Sound archive files.':
        'Bạn không thể mở file nén VST Sound.',

    # 10. media sentences
    "Instrument doesn't send any audio to the application!\\nDo you want to continue?":
        "Nhạc cụ không phát ra tín hiệu Audio nào!\\nBạn có muốn tiếp tục không?",
    'Invalid file: Only H264 encoded files are supported.':
        'File không hợp lệ: Chỉ hỗ trợ file mã H264.',
    'MPEX algorithms are not supported by this program version. If you want to modify the process, you can use an Elastique algorithm. To keep the processed audio, you can make all processes permanent.':
        'Phiên bản này không hỗ trợ thuật toán MPEX. Muốn sửa xử lý, bạn có thể dùng thuật toán Elastique. Để giữ Audio đã xử lý, hãy giữ cố định toàn bộ xử lý.',
    'MPEX algorithms are not supported by this program version. To modify the process, you can reprocess using a ZTX algorithm. To keep the processed audio, you can make all processes permanent.':
        'Phiên bản này không hỗ trợ thuật toán MPEX. Muốn sửa xử lý, bạn có thể xử lý lại bằng thuật toán ZTX. Để giữ Audio đã xử lý, hãy giữ cố định toàn bộ xử lý.',
    'Make All Permanent':
        'Giữ cố định tất cả',
    'Make Direct Offline Processing Permanent':
        'Giữ cố định Direct Offline Processing',
    'Make Extension Permanent':
        'Giữ cố định Extension',
    'Make Track Extension Permanent':
        'Giữ cố định Extension của Track',
    'Map Input Bus Metering to Audio Track (in Direct Monitoring)':
        'Gán Meter của Input Bus sang Audio Track (trong Direct Monitoring)',
    'Missing files will be exported as media references.':
        'File thiếu sẽ Export dạng tham chiếu Media.',
    'If you are using the built-in audio connections of your computer, please select "%s".':
        'Nếu dùng kết nối Audio có sẵn của máy, hãy chọn "%s".',
    'If you have an audio interface with multiple inputs and outputs, you might need to configure your routing afterwards in the Audio Connections dialog (Studio menu > Audio Connections).':
        'Nếu Audio Interface có nhiều đầu vào và đầu ra, bạn có thể cần chỉnh lại Routing trong hộp thoại Audio Connections (menu Studio > Audio Connections).',
    'Import dropped File as single Part':
        'Import file thả vào thành một Part duy nhất',
    'No compatible audio stream found in file:\\n':
        'Không tìm thấy Audio Stream tương thích trong file:\\n',
    'One or more channels cannot be exported with the selected audio codec.\\nThese channels have been deselected.':
        'Một hoặc nhiều Channel không Export được bằng codec Audio đã chọn.\\nCác Channel này sẽ bị bỏ chọn.',
    'Open file dialog to browse for all missing files':
        'Mở cửa sổ duyệt file để tìm mọi file bị thiếu',
    'Open file dialog to browse for the selected file':
        'Mở cửa sổ duyệt file để tìm file đã chọn',
    'Parts of the project file are invalid. The file could not be loaded completely!':
        'Một số phần của file Project không hợp lệ. Không tải hết được file!',
    'Please select audio events with fade times > 0!':
        'Hãy chọn các Audio Event có Fade > 0!',
    'Press [Esc] to cancel the process and terminate the video service.':
        'Nhấn [Esc] để hủy quá trình và tắt dịch vụ Video.',
    'Reaching the 2GB limit of the OMF file format, some media will be missing...':
        'Đã chạm giới hạn 2GB của định dạng file OMF, sẽ thiếu một số Media...',
    'Remaining Number of Beats defined in Audio File':
        'Số nhịp còn lại trong File Audio',
    'Remove selected Users from the User Pool':
        'Gỡ người dùng đã chọn khỏi User Pool',
    'Add new User to your User Pool':
        'Thêm người dùng mới vào User Pool',
    'Removes any existing audio in the record range, but creates new audio events for each cycle in cycle record.':
        'Xóa mọi Audio có sẵn trong vùng ghi, nhưng tạo Audio Event mới cho mỗi Cycle khi ghi theo Cycle.',
    'Removes any previous audio in the record range.':
        'Xóa mọi Audio trước đó trong vùng ghi.',
    'Replacing audio stream in video file...':
        'Đang thay thế Audio Stream trong file Video...',
    'Select the media types for which the attribute settings will be displayed in the Inspector':
        'Chọn loại Media hiện cài đặt thuộc tính trong Inspector',
    'Set to a value greater than 0 if you want to skip the first rows of the file.':
        'Đặt giá trị lớn hơn 0 để bỏ qua các hàng đầu của file.',
    'Show File Extensions in Results List':
        'Hiện đuôi File trong danh sách kết quả',
    'The following VST2 plug-ins are in use. Please consider replacing them with their VST3 versions:':
        'Các Plug-in VST2 sau đang dùng. Hãy cân nhắc đổi chúng sang bản VST3:',
    'The following troubleshooting options are available:':
        'Các tùy chọn khắc phục sự cố hiện có:',
    'The inserted event will not be visible according to your filter settings!':
        'Event mới chèn sẽ không hiện theo cài đặt bộ lọc!',
    'The master track cannot be shifted with this operation. Do you want to continue?':
        'Master Track không dịch chuyển được bằng lệnh này. Bạn có muốn tiếp tục không?',
    'The name is already in use, please enter a new name.':
        'Tên này đã được dùng, vui lòng nhập tên mới.',
    "The plug-in '%s' could not be found. It has automatically been replaced by the compatible plug-in '%s' version '%s' in your project.":
        "Không tìm thấy Plug-in '%s'. Nó đã tự thay bằng Plug-in tương thích '%s' bản '%s' trong Project.",
    "The plug-in '%s' could not be found. It has automatically been replaced by the plug-in '%s' version '%s' in your project.":
        "Không tìm thấy Plug-in '%s'. Nó đã tự thay bằng Plug-in '%s' bản '%s' trong Project.",
    'The port is currently used!\\nHiding it will disconnect it.':
        'Cổng này đang được dùng!\\nẨn đi sẽ ngắt kết nối.',
    'The selection is used in the project!\\nDo you want to remove all occurrences from the project?':
        'Vùng chọn đang dùng trong Project!\\nXóa mọi chỗ dùng nó khỏi Project không?',
    'The selection is in use and cannot be moved to the trash because\\n%s\\n\\nDo you want to remove it from the Pool and remove all occurrences from the project?':
        'Vùng chọn đang dùng nên không chuyển vào thùng rác được vì\\n%s\\n\\nGỡ nó khỏi Pool và xóa mọi chỗ dùng nó khỏi Project không?',
    'The serial port %s could not be opened, because it was already opened by another application.':
        'Không mở được cổng Serial %s vì ứng dụng khác đang mở nó.',
    'The specified range is too short for loudness analysis. Please specify a range of at least 4 seconds.':
        'Vùng đã chọn quá ngắn để phân tích Loudness. Hãy chọn vùng dài ít nhất 4 giây.',
    'The audio device port or midi device assignments of this Favorite are already in use. Reuse them and add to External Effects?':
        'Cổng Audio Device hoặc thiết bị MIDI của Favorite này đang dùng. Dùng lại và thêm vào External Effect?',
    'The audio device port or midi device assignments of this Favorite are already in use. Reuse them and add to External Instruments?':
        'Cổng Audio Device hoặc thiết bị MIDI của Favorite này đang dùng. Dùng lại và thêm vào External Instrument?',
    'Reuse':
        'Dùng lại',
    'The cache file for frozen channel "%s" could not be found. The channel will be unfrozen.':
        'Không thấy file cache của Channel đã Freeze "%s". Channel sẽ bỏ Freeze.',
    'The cache file for frozen instrument "%s" could not be found. The instrument will be unfrozen.':
        'Không thấy file cache của Instrument đã Freeze "%s". Instrument sẽ bỏ Freeze.',
    'The chosen location was outside the User Preset Location. The file was saved directly in the User Presets.':
        'Vị trí đã chọn ngoài User Preset. File đã lưu thẳng vào User Preset.',
    'The created AAF file may not be usable for other hosts because:':
        'File AAF tạo ra có thể không mở được trên phần mềm khác vì:',
    'The file could not be opened because it contains invalid data.':
        'Không mở được file vì dữ liệu không hợp lệ.',
    'The file is write protected and cannot be replaced!':
        'File đang chống ghi nên không thay thế được!',
    'The name you entered is not a valid file name:\\n%s\\nPlease enter a new name.':
        'Tên vừa nhập không phải tên file hợp lệ:\\n%s\\nVui lòng nhập tên mới.',
    'The original file sounds different than the edited clip.\\n Do you still want to open the original file?':
        'File gốc nghe khác với Clip đã chỉnh sửa.\\n Bạn vẫn muốn mở file gốc chứ?',
    'The original project uses media from an embedded AAF file.\\nEven after backup, those media will still refer to the original AAF file.\\n':
        'Project gốc dùng Media từ file AAF đã nhúng.\\nDù đã sao lưu, các Media đó vẫn trỏ về file AAF gốc.\\n',
    'The project contains SDII-files. These files cannot be exported as references and will be included in the OMF file.':
        'Project chứa file SDII. Các file này không Export dạng tham chiếu được mà sẽ gộp vào file OMF.',
    'The project could not be replaced!\\nIt has been stored as new file "%s" instead!':
        'Không thay được Project!\\nĐã lưu thành file mới "%s" thay thế!',
    "The project file contains '%s' data which is not supported by this program version. The data is ignored.":
        "File Project chứa dữ liệu '%s' mà phiên bản này không hỗ trợ. Dữ liệu bị bỏ qua.",
    'The project file contains edit groups in folder tracks. This feature is not available in this program version.':
        'File Project có Edit Group trong Folder Track. Phiên bản này không có tính năng đó.',
    'The project file has been moved!\\nPlease confirm the project working directory!\\n\\nDocument path is: %s\\n\\nNew (1):\\t%s\\nOld (2):\\t%s':
        'File Project đã chuyển chỗ!\\nVui lòng xác nhận thư mục làm việc của Project!\\n\\nĐường dẫn file là: %s\\n\\nMới (1):\\t%s\\nCũ (2):\\t%s',
    'The project file was created with %s.\\nAlthough that program is able to read %s project files in general,\\nthe two might not be fully compatible, so you may want to keep the original file.\\n\\nDo you want to overwrite the project file or create a new file?':
        'File Project được tạo bằng %s.\\nDù chương trình đó đọc được file Project của %s,\\nhai bản có thể không tương thích hẳn, nên bạn nên giữ file gốc.\\n\\nBạn có muốn ghi đè file Project hay tạo file mới?',
    'The project file was created with %s.\\nIf you overwrite it, you will not be able to open it with the original program again!\\n\\nDo you want to overwrite the project file or create a new file?':
        'File Project được tạo bằng %s.\\nNếu ghi đè, bạn sẽ không mở lại được bằng chương trình gốc!\\n\\nBạn có muốn ghi đè file Project hay tạo file mới?',
    "The project references media from an embedded AAF file which cannot be shared.\\nTo be able to share those media use the Pool's Convert Files function.":
        'Project tham chiếu Media từ file AAF đã nhúng không chia sẻ được.\\nĐể chia sẻ các Media đó, hãy dùng Convert Files của Pool.',
    'The project uses media from an embedded AAF file.\\n Those media cannot be copied.':
        'Project dùng Media từ file AAF đã nhúng.\\n Các Media đó không sao chép được.',
    "The project will be saved as '%s', \\nbecause the program is in an unstable state after crashing \\nand saving might lead to corrupted files. \\nThe original file will be left untouched. \\nPlease restart the program after this operation!":
        "Project sẽ lưu thành '%s', \\nvì chương trình chập chờn sau khi crash, \\nlưu lúc này có thể làm hỏng file. \\nFile gốc giữ nguyên. \\nHãy khởi động lại chương trình sau bước này!",
    'Verify your installation!':
        'Kiểm tra bản cài đặt!',
    'You must save your project before writing the MIDI file to the project folder.':
        'Bạn phải lưu Project trước khi ghi file MIDI vào thư mục Project.',
    'Your changes will be lost and you will have to re-analyse this audio.':
        'Thay đổi sẽ mất và bạn sẽ phải phân tích lại đoạn Audio này.',
    'An exception occurred. Save your work and restart the application.\\nThe exception was thrown because of the plug-in :\\n\\n':
        'Đã xảy ra lỗi ngoại lệ. Hãy lưu việc đang làm và khởi động lại ứng dụng.\\nLỗi phát sinh do Plug-in :\\n\\n',
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
