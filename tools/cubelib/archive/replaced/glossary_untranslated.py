#!/usr/bin/env python3
"""Full Vietnamese for the 148 strings the automated pass left as English.

The earlier pass substituted a few prepositions into English prose
("... cho this operation") and dropped the sentence-final period, which is
worse than leaving English alone. These are rewritten properly here: DAW terms
stay English per AGENT.md, everything else becomes natural Vietnamese.
"""

WORDING = {
    # --- pool / file / edit versions ---------------------------------------
    "'%s' is not supported for clips in musical mode!":
        "'%s' không được hỗ trợ cho Clip ở chế độ musical!",
    'A file cannot be replaced if it has multiple edit versions!\\nInstead, '
    'new files can be created and replaced in the Pool!':
        'Không thể thay thế file nếu nó có nhiều phiên bản sửa!\\n'
        'Thay vào đó, bạn có thể tạo file mới rồi thay thế trong Pool!',
    'it is used in another Pool and it has more than one edit version!':
        'nó đang được dùng trong một Pool khác và có nhiều hơn một phiên bản sửa!',
    'it is used in another Pool!': 'nó đang được dùng trong một Pool khác!',
    'Some files are referenced by clips that are still in the Pool. These files '
    'have not been deleted.':
        'Một số file đang được tham chiếu bởi các Clip vẫn còn trong Pool. '
        'Những file này chưa bị xóa.',
    'The Clip Package contains automation. Import the automation, too?':
        'Gói Clip có chứa Automation. Bạn có muốn Import Automation đó không?',
    'The Clip Package will not contain a preview, because the project is not '
    'active.':
        'Gói Clip sẽ không chứa phần xem trước, vì Project không đang hoạt động.',

    # --- file system errors -------------------------------------------------
    'The file could not be opened because it contains invalid data.':
        'Không thể mở file vì nó chứa dữ liệu không hợp lệ.',
    'The file format is not supported.': 'Định dạng file không được hỗ trợ.',
    'The file is missing!': 'File không tồn tại!',
    'The file is write protected and cannot be replaced!':
        'File đang được bảo vệ ghi và không thể thay thế!',
    'The file/folder could not be found at this location.':
        'Không tìm thấy file/thư mục tại vị trí này.',
    'The folder should be empty!': 'Thư mục nên để trống!',
    'The folder that you selected in the Path field does not exist.':
        'Thư mục bạn chọn trong trường Path không tồn tại.',
    'The directory you specified is read only!\\n\\nPlease make a new selection!':
        'Thư mục bạn chỉ định chỉ cho phép đọc!\\n\\nVui lòng chọn mục khác!',
    'The project directory is read only!\\n\\nPlease make a new selection!':
        'Thư mục Project chỉ cho phép đọc!\\n\\nVui lòng chọn mục khác!',
    'The selected file path does not exist.\\nAction is canceled.':
        'Đường dẫn file đã chọn không tồn tại.\\nThao tác đã bị hủy.',
    'The selected folder can result in a path length that is not allowed by '
    'the operating system.\\n\\nPlease select another folder.':
        'Thư mục đã chọn có thể tạo ra đường dẫn dài vượt quá giới hạn của hệ '
        'điều hành.\\n\\nVui lòng chọn thư mục khác.',
    'Write Protection could not be removed for %d file.':
        'Không thể gỡ bỏ bảo vệ ghi cho %d file.',
    'Write Protection could not be removed for %d files.':
        'Không thể gỡ bỏ bảo vệ ghi cho %d file.',
    'Write Protection could not be set for %d file.':
        'Không thể đặt bảo vệ ghi cho %d file.',
    'Write Protection could not be set for %d files.':
        'Không thể đặt bảo vệ ghi cho %d file.',
    'The project is corrupt!': 'Project bị hỏng!',
    'Project has not been saved.': 'Project chưa được lưu.',

    # --- disk space ---------------------------------------------------------
    'Not enough disk space available for copying all files !\\n\\nAction '
    'cancelled!':
        'Không đủ dung lượng đĩa để sao chép tất cả file!\\n\\nThao tác đã bị hủy!',
    'Not enough disk space available for rendering.\\nAction is canceled.':
        'Không đủ dung lượng đĩa để Render.\\nThao tác đã bị hủy.',
    'There is not enough disk space for this operation!':
        'Không đủ dung lượng đĩa cho thao tác này!',
    'The remaining disk space (%s) is insufficient for this operation.\\n'
    'Required space is about %s.':
        'Dung lượng đĩa còn lại (%s) không đủ cho thao tác này.\\n'
        'Dung lượng cần thiết khoảng %s.',

    # --- plugin / component -------------------------------------------------
    "The plug-in '%s' could not be found. It has automatically been replaced by "
    "the compatible plug-in '%s' version '%s' in your project.":
        "Không tìm thấy Plug-in '%s'. Nó đã được tự động thay bằng Plug-in tương "
        "thích '%s' phiên bản '%s' trong Project của bạn.",
    "The plug-in '%s' could not be found. It has automatically been replaced by "
    "the plug-in '%s' version '%s' in your project.":
        "Không tìm thấy Plug-in '%s'. Nó đã được tự động thay bằng Plug-in '%s' "
        "phiên bản '%s' trong Project của bạn.",
    'The plug-in "%s" could not be found for Effect Channel "%d"!':
        'Không tìm thấy Plug-in "%s" cho Effect Channel "%d"!',
    'The plug-in "%s" could not be found for Instrument Track "%s"!':
        'Không tìm thấy Plug-in "%s" cho Instrument Track "%s"!',
    'The plug-in "%s" could not be found for Master Insert "%d"!':
        'Không tìm thấy Plug-in "%s" cho Master Insert "%d"!',
    'The plug-in "%s" could not be found for VST Synth "%d"!':
        'Không tìm thấy Plug-in "%s" cho VST Synth "%d"!',
    'The plug-in "%s" could not be found for VST Synth %d!':
        'Không tìm thấy Plug-in "%s" cho VST Synth %d!',
    'Plug-in report cannot be saved in the specified folder.':
        'Không thể lưu báo cáo Plug-in vào thư mục đã chỉ định.',
    'The component could not be terminated!': 'Không thể kết thúc thành phần!',
    'The BAIOS Component is missing!': 'Thiếu thành phần BAIOS!',
    'The Drum Machine component is not installed. Please re-install the '
    'application.':
        'Thành phần Drum Machine chưa được cài đặt. Vui lòng cài lại ứng dụng.',
    'The Sampler Track component is not installed. Please re-install the '
    'application.':
        'Thành phần Sampler Track chưa được cài đặt. Vui lòng cài lại ứng dụng.',
    'vstscanner for VST 3 Plug-ins not found!':
        'Không tìm thấy vstscanner cho VST 3 Plug-in!',
    'vstscannermaster for VST 3 Plug-ins not found!':
        'Không tìm thấy vstscannermaster cho VST 3 Plug-in!',
    'Verify failed for this node!': 'Kiểm tra thất bại với node này!',

    # --- project / channel limits ------------------------------------------
    "Channel '%s' contains more insert slots than supported by this program "
    'version. The slots are being discarded.':
        "Channel '%s' chứa nhiều ô Insert hơn mức phiên bản chương trình này hỗ "
        'trợ. Các ô đó đang bị loại bỏ.',
    "Channel '%s' contains more send slots than supported by this program "
    'version. The slots are being discarded.':
        "Channel '%s' chứa nhiều ô Send hơn mức phiên bản chương trình này hỗ "
        'trợ. Các ô đó đang bị loại bỏ.',
    'The project file contains more insert slots than supported by this program '
    'version. The slots are being discarded.':
        'File Project chứa nhiều ô Insert hơn mức phiên bản chương trình này hỗ '
        'trợ. Các ô đó đang bị loại bỏ.',
    'The project file contains more send slots than supported by this program '
    'version. The slots are being discarded.':
        'File Project chứa nhiều ô Send hơn mức phiên bản chương trình này hỗ '
        'trợ. Các ô đó đang bị loại bỏ.',
    'The project file contains more instrument slots than supported by this '
    'program version. The slots are being discarded.':
        'File Project chứa nhiều ô Instrument hơn mức phiên bản chương trình này '
        'hỗ trợ. Các ô đó đang bị loại bỏ.',
    "The project file contains '%s' data which is not supported by this program "
    'version. The data is being discarded.':
        "File Project chứa dữ liệu '%s' không được phiên bản chương trình này "
        'hỗ trợ. Dữ liệu đang bị loại bỏ.',
    "The project file contains '%s' data which is not supported by this program "
    'version. The data is ignored.':
        "File Project chứa dữ liệu '%s' không được phiên bản chương trình này "
        'hỗ trợ. Dữ liệu bị bỏ qua.',
    'The project file contains edit groups in folder tracks. This feature is '
    'not available in this program version.':
        'File Project chứa nhóm sửa trong các Folder Track. Tính năng này không '
        'có trong phiên bản chương trình này.',
    'The project file has been moved!\\nPlease confirm the project working '
    "directory!\\n\\nDocument path is: %s\\n\\nNew (1):\\t%s\\nOld (2):\\t%s":
        'File Project đã được di chuyển!\\n'
        'Vui lòng xác nhận thư mục làm việc của Project!\\n\\n'
        'Đường dẫn tài liệu là: %s\\n\\nMới (1):\\t%s\\nCũ (2):\\t%s',
    'The project contains no stereo output channel.':
        'Project không có Channel đầu ra stereo.',
    'The project contains no video. A black screen is exported.':
        'Project không có Video. Màn hình đen sẽ được Export.',
    'Project mappings are saved for the project only.':
        'Mapping của Project chỉ được lưu cho Project đó.',
    'Project will be exported as\\n\'%s\'.':
        'Project sẽ được Export thành\\n\'%s\'.',
    'This project contains a Chord Track. It cannot be displayed or edited. '
    'Tracks following the Chord Track may not be freely editable within the '
    'editors.':
        'Project này chứa Chord Track. Track đó không thể hiển thị hay sửa. '
        'Các Track đứng sau Chord Track có thể không sửa tùy ý trong các Editor.',
    'This project contains a transpose track. The track will be used for '
    'playback, but you cannot remove or edit it.':
        'Project này chứa Transpose Track. Track đó sẽ được dùng để phát lại, '
        'nhưng bạn không thể gỡ bỏ hay sửa nó.',
    'You should save the project now!\\nFile references in the stored version '
    'have become invalid!':
        'Bạn nên lưu Project ngay!\\nTham chiếu file trong phiên bản đã lưu đã '
        'trở nên không hợp lệ!',

    # --- routing / ports ----------------------------------------------------
    'A feedback connection has been reset for channel "%s".':
        'Kết nối phản hồi của Channel "%s" đã được đặt lại.',
    'The channel panner MixConvert has automatically been replaced by '
    'MixConvert V6 for Channel "%s". Your project may sound differently.':
        'Channel panner MixConvert đã được tự động thay bằng MixConvert V6 cho '
        'Channel "%s". Project của bạn có thể nghe khác đi.',
    'The project contains no stereo output channel.':
        'Project không có Channel đầu ra stereo.',
    'The selected device port is already used. Selecting the port for this bus '
    'will replace any previous connection.':
        'Cổng thiết bị đã chọn đang được dùng. Chọn cổng cho Bus này sẽ thay thế '
        'mọi kết nối trước đó.',
    'The device ports saved in the preset are already used. Applying this preset '
    'will replace any previous connections.':
        'Các cổng thiết bị lưu trong Preset đã được dùng. Áp dụng Preset này sẽ '
        'thay thế mọi kết nối trước đó.',
    'The port is currently used!\\nHiding it will disconnect it.':
        'Cổng này hiện đang được dùng!\\nẨn nó sẽ ngắt kết nối.',
    'The serial port %s could not be opened, because it was already opened by '
    'another application.':
        'Không thể mở cổng serial %s, vì nó đã được một ứng dụng khác mở.',
    'The serial port %s could not be opened.':
        'Không thể mở cổng serial %s.',
    'The serial port %s could not be opened. Error code %d':
        'Không thể mở cổng serial %s. Mã lỗi %d',
    'This External Plug-in "%s" is in use and cannot be removed!':
        'External Plug-in "%s" này đang được dùng và không thể gỡ bỏ!',
    'External plug-in is used. Audio-Mixdown must be done in real time!':
        'Đang dùng External Plug-in. Audio-Mixdown phải được thực hiện theo thời '
        'gian thực!',
    'The Studio can only have one "%s"!': 'Studio chỉ có thể có một "%s"!',
    'The chosen location was outside the User Preset Location. The file was '
    'saved directly in the User Presets.':
        'Vị trí đã chọn nằm ngoài vùng User Preset. File đã được lưu trực tiếp '
        'trong User Preset.',
    'The destination parameter has been changed.':
        'Tham số đích đã được thay đổi.',

    # --- locators / transport ----------------------------------------------
    'The Locator Range is empty. Please set the Left and Right Locator.':
        'Dải Locator đang trống. Vui lòng đặt Left Locator và Right Locator.',
    'The export range is empty. Please set the left and right locators.':
        'Dải Export đang trống. Vui lòng đặt Left Locator và Right Locator.',
    'The locator range is inverted. Please switch the locators.':
        'Dải Locator đang bị đảo ngược. Vui lòng hoán đổi hai Locator.',
    'The locator range is not set. Please set the locators.':
        'Dải Locator chưa được đặt. Vui lòng đặt các Locator.',
    'The locator range contains no video event. A black screen is exported.':
        'Dải Locator không có Video Event. Màn hình đen sẽ được Export.',
    'The first note played in a new cycle deletes all later notes.':
        'Nốt đầu tiên được phát trong một chu kỳ mới sẽ xóa tất cả các nốt sau đó.',
    'Tracks are recording!': 'Các Track đang ghi!',
    'Record only Specific Controller No.':
        'Chỉ ghi Controller cụ thể số.',
    'Removes any existing audio in the record range, but creates new audio '
    'events for each cycle in cycle record.':
        'Xóa mọi âm thanh có sẵn trong vùng ghi, nhưng tạo Audio Event mới cho '
        'mỗi chu kỳ khi ghi theo chu kỳ.',
    'Creates new audio events for any recording or cycle.':
        'Tạo Audio Event mới cho mọi lần ghi hoặc chu kỳ.',
    'Event cannot be moved.\\nOrigin is before project start.':
        'Không thể di chuyển Event.\\nĐiểm xuất phát nằm trước đầu Project.',
    'The selected events cannot be crossfaded.':
        'Không thể tạo Crossfade cho các Event đã chọn.',
    'The selected tracks contain audio parts.':
        'Các Track đã chọn có chứa Part Audio.',
    'The selected track types cannot be exported!':
        'Không thể Export các loại Track đã chọn!',
    'The selection could not be deleted!': 'Không thể xóa vùng chọn!',
    'The track archive cannot be imported!':
        'Không thể Import gói Track đã lưu!',
    'The tracks in this folder are not completely in sync.\\nGroup editing '
    'could fail!':
        'Các Track trong thư mục này không đồng bộ hoàn toàn.\\n'
        'Sửa nhóm có thể thất bại!',
    'The audio material contains warp tabs or is in musical mode. If you slice '
    'it, warp tabs are removed and musical mode is deactivated.':
        'Tư liệu Audio chứa tab Warp hoặc đang ở chế độ musical. Nếu bạn cắt '
        'nó, các tab Warp sẽ bị loại bỏ và chế độ musical sẽ bị tắt.',
    'The audio material is not overlapping.':
        'Tư liệu Audio không bị chồng lấn.',
    'The audio tempo cannot be changed!': 'Không thể thay đổi Tempo của Audio!',
    'The selected audio material is not suitable for tempo detection.':
        'Tư liệu Audio đã chọn không phù hợp để nhận diện Tempo.',
    'The selected material is not suitable for tempo detection.':
        'Tư liệu đã chọn không phù hợp để nhận diện Tempo.',
    'Please create hitpoints before using AudioWarp quantize for groups.':
        'Vui lòng tạo Hitpoint trước khi dùng AudioWarp Quantize cho nhóm.',
    'Tempo editing is not possible for editors without project relation.':
        'Không thể sửa Tempo trong các Editor không liên quan tới Project.',

    # --- editor / view ------------------------------------------------------
    'At least one track must be visible in the editor.':
        'Phải có ít nhất một Track hiển thị trong Editor.',
    'Click to add all parts to the editor.':
        'Nhấp để thêm tất cả Part vào Editor.',
    'Click and drag this page to move or copy it, or to swap it with another '
    'page.':
        'Nhấp và kéo trang này để di chuyển hoặc sao chép nó, hoặc để hoán đổi '
        'nó với một trang khác.',
    'Tip of the Day: This section provides an instant help and operation tips '
    'for the editor.':
        'Mẹo trong ngày: Mục này cung cấp trợ giúp nhanh và các mẹo thao tác cho '
        'Editor.',
    "All parts specified in 'Part Editing Mode' are used.":
        'Tất cả Part chỉ định trong \'Part Editing Mode\' đều được sử dụng.',
    'Drawing is not possible in this wave display mode!':
        'Không thể vẽ trong chế độ hiển thị dạng sóng này!',
    'Zoom Mode has been changed for Definition editing.':
        'Zoom Mode đã được thay đổi cho việc sửa Definition.',

    # --- score / chord symbols ---------------------------------------------
    'Chord:\\nThe pitch matches the current chord but is not in the current '
    'scale. Unusual - do the current chord and scale match?':
        'Hợp âm:\\nPitch khớp với hợp âm hiện tại nhưng không nằm trong Scale '
        'hiện tại. Khác thường - hợp âm và Scale hiện tại có khớp không?',
    'None:\\nThe pitch is not in the current chord or the current scale. This '
    'pitch adds a strong tension.':
        'None:\\nPitch không nằm trong hợp âm hiện tại cũng không nằm trong Scale '
        'hiện tại. Pitch này tạo ra một Tension mạnh.',
    'Scale:\\nThe pitch is in the current scale but not in the current chord. A '
    'good pitch for melody that adds some tension.':
        'Scale:\\nPitch nằm trong Scale hiện tại nhưng không nằm trong hợp âm '
        'hiện tại. Một Pitch tốt cho giai điệu và tạo thêm một chút Tension.',
    'Voicings cannot be applied. Too many notes found for at least one chord.':
        'Không thể áp dụng Voicing. Tìm thấy quá nhiều nốt trong ít nhất một '
        'hợp âm.',
    'Other assigned pads will be transposed when changing the Root Key.':
        'Các Pad được gán khác sẽ được Transpose khi đổi Root Key.',
    'Lock Chord Assignment on Pad': 'Khoá phép gán hợp âm trên Pad',
    'For each unique value that occurs in this column, a marker track is '
    'generated.':
        'Với mỗi giá trị duy nhất xuất hiện trong cột này, một Marker Track sẽ '
        'được tạo.',

    # --- MIDI controller surface -------------------------------------------
    'No connected MIDI Controllers found for this script.':
        'Không tìm thấy MIDI Controller đã kết nối cho Script này.',
    "No controller surface available. Enter the mandatory information, click OK, "
    "and create a surface in the 'MIDI Controller Surface Editor'.":
        'Không có Surface điều khiển nào khả dụng. Nhập các thông tin bắt buộc, '
        'nhấp OK, rồi tạo một Surface trong \'MIDI Controller Surface Editor\'.',
    'The MIDI Controller Surface contains invalid elements (highlighted in '
    'orange). You can leave the Surface Editor and those elements will be '
    'removed automatically, or you can stay and modify the elements.':
        'MIDI Controller Surface chứa các phần tử không hợp lệ (được tô sáng '
        'màu cam). Bạn có thể rời khỏi Surface Editor và các phần tử đó sẽ tự '
        'động bị loại bỏ, hoặc bạn có thể ở lại và sửa các phần tử.',
    'The MIDI Controller Surface did not contain any elements and was therefore '
    'not stored.':
        'MIDI Controller Surface không chứa phần tử nào nên không được lưu.',
    'Error in voice conversion. Some parts were processed in Auto mode instead.':
        'Lỗi khi chuyển đổi bè. Một số Part đã được xử lý ở chế độ Auto thay '
        'thế.',
    'Learn mode: Assign the destination by clicking a parameter in your project.':
        'Chế độ Learn: Gán tham số đích bằng cách nhấp vào một tham số trong '
        'Project của bạn.',
    'You are recording in Note Expression Overdub Mode - MIDI Note Input is '
    'deactivated.':
        'Bạn đang ghi ở chế độ Note Expression Overdub - MIDI Note Input đã bị '
        'tắt.',
    'Warning: You must define a MIDI message for this control.':
        'Cảnh báo: Bạn phải định nghĩa một thông điệp MIDI cho điều khiển này.',

    # --- loudness / analysis ------------------------------------------------
    'The quick loudness analysis failed. An internal error occurred.':
        'Phân tích Loudness nhanh thất bại. Đã xảy ra lỗi nội bộ.',
    'Real Time Algorithm has been deactivated because pitch or stretch factor '
    'lies outside the limits of the current preset.':
        'Real Time Algorithm đã bị tắt vì Pitch hoặc hệ số co giãn nằm ngoài giới '
        'hạn của Preset hiện tại.',
    'Threshold for dialog-gated loudness measurement. If less speech is '
    'detected in audio, program-gated measurement is used.':
        'Ngưỡng cho phép đo Loudness theo cổng thoại. Nếu phát hiện ít giọng nói '
        'hơn trong Audio, phép đo theo cổng chương trình sẽ được dùng.',
    'Threshold for dialogue-gated loudness measurement. If less speech is '
    'detected in audio, program-gated measurement is used':
        'Ngưỡng cho phép đo Loudness theo cổng thoại. Nếu phát hiện ít giọng nói '
        'hơn trong Audio, phép đo theo cổng chương trình sẽ được dùng',
    'This specifies the maximum duration the Score Editor will produce for a '
    "rhythmic slash, without considering rhythm dots, and applies in all time "
    "signatures. For example, if you choose '1/4 Note (Crotchet)', the Score "
    'Editor will create four slashes in 2/2, and two dottet slashes in 6/8.':
        'Tùy chọn này xác định trường độ tối đa mà Score Editor sẽ tạo cho một '
        'gạch nhịp, không tính các dấu chấm nhịp, và áp dụng cho mọi số chỉ '
        "nhịp. Ví dụ, nếu bạn chọn 'Note 1/4 (Crotchet)', Score Editor sẽ tạo "
        'bốn gạch trong 2/2 và hai gạch có chấm trong 6/8.',
    'When the page is less full than the threshold for justifying staves, no '
    'vertical justification occurs.':
        'Khi trang ít chữ hơn ngưỡng để căn đều khuông nhạc, sẽ không có việc căn '
        'theo chiều dọc.',

    # --- network / sharing --------------------------------------------------
    'Please select a user in the Global IP network folder.':
        'Vui lòng chọn một người dùng trong thư mục mạng Global IP.',
    'There are no tracks selected for download.':
        'Không có Track nào được chọn để tải về.',
    'There are no files for converting!': 'Không có file nào để chuyển đổi!',
    'No Formats available for current Input Stream/Mode!':
        'Không có định dạng nào khả dụng cho Input Stream/Mode hiện tại!',
    'No active project for import!\\nPlease create and set up a new project.':
        'Không có Project nào đang hoạt động để Import!\\n'
        'Vui lòng tạo và thiết lập một Project mới.',
    'Export path is not accessible.': 'Không truy cập được đường dẫn Export.',
    '2-Layer Mode (Middle, Top): use for Dolby Atmos\\n3-Layer Mode (Bottom, '
    'Middle, Top): use for MPEG-H, 22.2':
        '2-Layer Mode (Middle, Top): dùng cho Dolby Atmos\\n'
        '3-Layer Mode (Bottom, Middle, Top): dùng cho MPEG-H, 22.2',
    'Disables hardware acceleration for video encoding.':
        'Tắt tăng tốc phần cứng cho việc mã hoá Video.',
    'Data Transfer failed.\\nTo avoid data loss, the data will remain in source '
    'database.\\n':
        'Chuyển dữ liệu thất bại.\\nĐể tránh mất dữ liệu, dữ liệu sẽ được giữ lại '
        'trong cơ sở dữ liệu nguồn.\\n',
    'Downloads in progress. Please wait for next update.':
        'Đang tải về. Vui lòng chờ bản cập nhật tiếp theo.',
    'Do not ask again.': 'Không hỏi lại nữa.',
    'This option uses the preferences currently stored in the program.':
        'Tùy chọn này dùng các thiết lập đang được lưu trong chương trình.',
    'This profile requires \'3-Layer 3D Pan Mode\'. Please select it in the '
    "project settings, otherwise 'Z-Axis Pan' automation will be wrong.":
        'Profile này cần \'3-Layer 3D Pan Mode\'. Vui lòng chọn nó trong cài đặt '
        'Project, nếu không Automation \'Z-Axis Pan\' sẽ sai.',
    'Please select a column for Timecode In.':
        'Vui lòng chọn một cột cho Timecode In.',
    'Pool is ready for archive!': 'Pool đã sẵn sàng để lưu trữ!',
    'Project and video frame rate do not match.':
        'Frame rate của Project và Video không khớp.',
    'You activated the safe-start mode by pressing <Command> + <Shift> + <Alt> '
    'during program startup.':
        'Bạn đã kích hoạt chế độ safe-start bằng cách nhấn <Command> + <Shift> + '
        '<Alt> trong lúc khởi động chương trình.',
    'You activated the safe-start mode by pressing <Ctrl> + <Shift> + <Alt> '
    'during program startup.':
        'Bạn đã kích hoạt chế độ safe-start bằng cách nhấn <Ctrl> + <Shift> + '
        '<Alt> trong lúc khởi động chương trình.',
    'To save your changes for the selected job, please click \'Update Job\'.':
        'Để lưu các thay đổi cho tác vụ đã chọn, vui lòng nhấp \'Update Job\'.',
    'Video service does not respond. Waiting for video service...':
        'Dịch vụ video không phản hồi. Đang chờ dịch vụ video...',
    'The current chain contains no items. Add some items and then try again.':
        'Chain hiện tại không có mục nào. Hãy thêm một vài mục rồi thử lại.',
    'The selected track types cannot be exported!':
        'Không thể Export các loại Track đã chọn!',
}
