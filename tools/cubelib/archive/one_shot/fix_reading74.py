"""Round 74: manual reading fixes - simplify confusing machine translations.

Usage:
  python tools/fix_reading74.py
  python tools/fix_reading74.py --write
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
    # 1. Driver Audio - unify "trinh dieu khien Audio" -> "Driver Audio"
    '%s has detected that new audio drivers are available on your computer. Please select the audio driver for the audio hardware that you want to use with %s.':
        '%s phát hiện có Driver Audio mới trên máy. Hãy chọn Driver Audio cho thiết bị Audio muốn dùng với %s.',
    'If you are using the built-in audio connections of your computer, please select the corresponding audio driver.':
        'Nếu dùng kết nối Audio có sẵn của máy, hãy chọn Driver Audio tương ứng.',
    'If you reconnect the hardware and the dialog does not close automatically, select the corresponding ASIO driver from the list and click "OK".':
        'Nếu đã cắm lại thiết bị mà hộp thoại không tự đóng, hãy chọn Driver ASIO tương ứng rồi nhấn "OK".',
    'If you want to use another audio hardware, please select the corresponding ASIO driver from the list below and click "OK".':
        'Nếu muốn dùng thiết bị Audio khác, hãy chọn Driver ASIO tương ứng trong danh sách rồi nhấn "OK".',
    'Click here to open the driver control panel.':
        'Nhấp vào đây để mở bảng điều khiển Driver.',
    'Please update your graphics card driver or switch to a more effective graphics card.':
        'Vui lòng cập nhật Driver card đồ họa hoặc đổi sang card đồ họa khỏe hơn.',
    'The audio driver could not be loaded.\\nPlease make sure your audio hardware is connected correctly to your computer.':
        'Không tải được Driver Audio.\\nHãy kiểm tra thiết bị Audio đã cắm đúng vào máy chưa.',
    'The audio hardware using the "%s" audio driver was removed from the computer.':
        'Thiết bị Audio dùng Driver Audio "%s" đã bị tháo khỏi máy.',
    'To ensure that you actually hear audio from %s, please select the driver of your audio interface from the list below. This is required for correct routing of playback and recording signals to your audio hardware.':
        'Để nghe được Audio từ %s, hãy chọn Driver của Audio Interface trong danh sách. Cần chọn đúng để đưa tín hiệu phát và ghi ra thiết bị Audio.',
    'You can change your driver selection and settings at any time in the Studio Setup dialog (Studio menu > Studio Setup) in the VST Audio System section.':
        'Bạn có thể đổi Driver và cài đặt bất kỳ lúc nào trong hộp thoại Thiết lập Studio (menu Studio > Thiết lập Studio), phần VST Audio System.',

    # 2. "chat lieu Audio" (audio material) -> "doan Audio"
    'Do you want to modify all events that refer to the same audio material?':
        'Bạn có muốn sửa tất cả Event cùng dùng một đoạn Audio gốc không?',
    'In Single Voice mode, the notes are mapped to the selected voice (monophonic material only)':
        'Ở chế độ Single Voice, các nốt được gán vào bè đã chọn (chỉ dùng cho nốt đơn âm)',
    'Multiple tempos were detected in the selected event. \\nApply the Smooth Tempo function if the tempo of the material is assumed to be constant.':
        'Phát hiện nhiều Tempo trong Event đã chọn. \\nDùng chức năng Smooth Tempo nếu Tempo của đoạn nhạc là ổn định.',
    'Tempo events are generated up to the point, where an irregular tempo change is detected.\\nApply the Smooth Tempo function if the tempo of the material is assumed to be constant.':
        'Các Tempo Event được tạo tới điểm phát hiện Tempo đổi bất thường.\\nDùng chức năng Smooth Tempo nếu Tempo của đoạn nhạc là ổn định.',
    'The project contains events that use\\nthe same audio material as the event in this editor!\\nClick "New Version" if processing should apply\\nonly to the edited event!':
        'Project có các Event dùng\\ncùng đoạn Audio gốc với Event trong Editor này!\\nNhấp "Version mới" nếu chỉ muốn xử lý\\ncho Event đang sửa!',
    'The selection contains audio material that is processed with the "Solo" algorithm.\\nBefore exporting a Clip Package, you need to change the algorithm or use the Bounce Selection\\ncommand on the Audio menu for the following events:':
        'Vùng chọn có đoạn Audio đang dùng thuật toán "Solo".\\nTrước khi Export gói Clip, hãy đổi thuật toán hoặc dùng lệnh Bounce Selection\\ntrong menu Audio cho các Event sau:',
    'The selection contains audio material with a sample rate that differs from the project sample rate.\\nBefore exporting a Clip Package, the audio clips have to be converted.':
        'Vùng chọn có đoạn Audio Sample Rate khác với Sample Rate của Project.\\nTrước khi Export gói Clip, cần chuyển đổi các Audio Clip này.',
    'You have selected regions for processing\\nthat refer to overlapping audio material!':
        'Các Region đã chọn để xử lý\\nđang dùng đoạn Audio bị chồng lấn!',
    'The audio material contains warp tabs or is in musical mode. If you slice it, warp tabs are removed and musical mode is deactivated.':
        'Đoạn Audio chứa Warp Marker hoặc đang ở chế độ Musical. Nếu cắt thành Slice, Warp Marker sẽ mất và chế độ Musical sẽ tắt.',
    'The audio material is not overlapping.':
        'Đoạn Audio không chồng lấn.',

    # 3. "anh xa" (mapped) -> "gan"
    'Action Mapping':
        'Gán hành động',
    'Mapped Ports':
        'Cổng đã gán',

    # 4. Preview / metadata
    'The Clip Package will not contain a preview, because the project is not active.':
        'Gói Clip sẽ không có Preview vì Project không hoạt động.',
    'Multiple clips are selected. The displayed metadata refers to the first clip.':
        'Nhiều Clip đang được chọn. Thông tin hiện tại là của Clip đầu tiên.',

    # 5. "cuc bo" (Local) -> keep "Local" / "tren may nay"
    'Delete Script - Only Scripts located in Local Folder can be deleted':
        'Xóa Script - Chỉ xóa được Script trong thư mục Local',
    'Local Drives':
        'Ổ đĩa Local',
    'Local Harddisks':
        'Ổ cứng Local',
    'Local Loop':
        'Loop Local',
    'Local Voicing':
        'Voicing Local',
    'Playback Toggle triggers Local Preview':
        'Bật/tắt nghe thử tại chỗ',
    "The volume database being removed could contain database entries that are shown in the Results list.\\nWould you like to import all database entries from drive '%s' into your local MediaBay database?":
        "Ổ đĩa đang gỡ có thể chứa các mục đang hiện trong danh sách kết quả.\\nBạn có muốn Import tất cả mục từ ổ đĩa '%s' vào MediaBay trên máy này không?",
    "The volume database being unmounted could contain database entries that are shown in the Results list.\\nWould you like to import all database entries from drive '%s' into your local MediaBay database?":
        "Ổ đĩa đang ngắt kết nối có thể chứa các mục đang hiện trong danh sách kết quả.\\nBạn có muốn Import tất cả mục từ ổ đĩa '%s' vào MediaBay trên máy này không?",
    'Users in Local Network':
        'Người dùng trong mạng Local',
    'Your local user name is already used by another computer on the network. The network will be reset.':
        'Tên user trên máy này đã bị máy khác trong mạng dùng. Mạng sẽ được đặt lại.',

    # 6. "Che do sua" -> "Che do Edit"
    "All clips specified in 'Clip Editing Mode' are used.":
        "Dùng tất cả Clip đã chọn trong 'Chế độ Edit Clip'.",
    "All parts specified in 'Part Editing Mode' are used.":
        "Dùng tất cả Part đã chọn trong 'Chế độ Edit Part'.",
    'Bypass will disable the MIDI Learn Mode (only manual placement possible) and the automatic selection in Edit Mode. Bypass should be used when MIDI controller sends frequent undesired MIDI messages.':
        'Bypass sẽ tắt chế độ MIDI Learn (chỉ đặt tay được) và tự chọn trong Chế độ Edit. Nên dùng Bypass khi MIDI Controller gửi liên tục tín hiệu MIDI ngoài ý muốn.',
    'Clip Editing Mode':
        'Chế độ Edit Clip',
    'Clip Editing Mode:':
        'Chế độ Edit Clip:',
    'Edit Mode: Make changes to one or more items.':
        'Chế độ Edit: Sửa một hoặc nhiều mục.',
    'Part Editing Mode':
        'Chế độ Edit Part',
    'Part Editing Mode:':
        'Chế độ Edit Part:',
    'Part/Clip Editing Mode: Active Part/Clip':
        'Chế độ Edit Part/Clip: Part/Clip đang bật',
    'Part/Clip Editing Mode: All Parts/Clips':
        'Chế độ Edit Part/Clip: Tất cả Part/Clip',
    'Part/Clip Editing Mode: All Parts/Clips on Active Track':
        'Chế độ Edit Part/Clip: Tất cả Part/Clip trên Track đang bật',
    'Part/Clip Editing Mode: Toggle All & Active Parts/Clips':
        'Chế độ Edit Part/Clip: Đảo tất cả & Part/Clip đang bật',
    "Solo Editor Mode: Solo follows 'Part/Clip Editing Mode'":
        "Chế độ Solo Editor: Solo bám theo 'Chế độ Edit Part/Clip'",
    "Solo follows 'Clip Editing Mode'":
        "Solo bám theo 'Chế độ Edit Clip'",
    "Solo follows 'Part Editing Mode'":
        "Solo bám theo 'Chế độ Edit Part'",

    # 7. MIDI Remote pickup / jump help - plain words
    'Sends a new value to the %s function as soon as you move the control. This can result in abrupt value changes.':
        'Gửi giá trị mới tới chức năng %s ngay khi bạn xoay nút. Giá trị có thể bị nhảy đột ngột.',
    'Picks up on the value of the %s function as soon as the control reaches that value. This results in smooth value changes, but requires you to estimate the pickup value.':
        'Nhận giá trị của chức năng %s khi nút xoay tới đúng giá trị đó. Giá trị đổi mượt hơn nhưng bạn phải tự dò đúng vị trí.',
    'Compares the value of the %s function to the control value, and approaches the two values in a smooth way. As soon as the values are identical, the function follows the control value.':
        'So sánh giá trị của chức năng %s với giá trị nút xoay, rồi đưa hai giá trị lại gần nhau một cách mượt mà. Khi hai giá trị bằng nhau, chức năng sẽ bám theo nút xoay.',

    # 8. Shift / align / slots / load
    'Shifting must be aborted, because the master track would be shifted into the negative!':
        'Phải dừng dịch chuyển vì Master Track sẽ bị lùi qua điểm bắt đầu!',
    'Event volume curves on the selected tracks are not aligned.':
        'Đường cong âm lượng Event trên các Track đã chọn không khớp nhau.',
    'Event fade times on the selected tracks are not aligned.':
        'Thời gian Fade của Event trên các Track đã chọn không đều nhau.',
    "Channel '%s' contains more insert slots than supported by this program version. The slots are being discarded.":
        "Channel '%s' có nhiều ô Insert hơn mức phiên bản này hỗ trợ. Các ô đó sẽ bị bỏ.",
    "Channel '%s' contains more send slots than supported by this program version. The slots are being discarded.":
        "Channel '%s' có nhiều ô Send hơn mức phiên bản này hỗ trợ. Các ô đó sẽ bị bỏ.",
    "The project file contains '%s' data which is not supported by this program version. The data is being discarded.":
        "File Project chứa dữ liệu '%s' mà phiên bản này không hỗ trợ. Dữ liệu đó sẽ bị bỏ.",
    'The project file contains more insert slots than supported by this program version. The slots are being discarded.':
        'File Project có nhiều ô Insert hơn mức phiên bản này hỗ trợ. Các ô đó sẽ bị bỏ.',
    'The project file contains more instrument slots than supported by this program version. The slots are being discarded.':
        'File Project có nhiều ô Instrument hơn mức phiên bản này hỗ trợ. Các ô đó sẽ bị bỏ.',
    'The project file contains more send slots than supported by this program version. The slots are being discarded.':
        'File Project có nhiều ô Send hơn mức phiên bản này hỗ trợ. Các ô đó sẽ bị bỏ.',
    'In this mode, only program plug-ins are loaded.':
        'Ở chế độ này, chỉ tải Plug-in đi kèm chương trình.',
    "You deactivated the loading of third party plug-ins by pressing '%s' during program startup.\\nIn this mode, only Steinberg plug-ins are loaded.":
        "Bạn đã tắt tải Plug-in bên thứ ba bằng cách nhấn '%s' khi khởi động.\\nỞ chế độ này, chỉ tải Plug-in của Steinberg.",
    "The plug-in could not be validated and has been moved to the blocklist. You can reactivate the plug-in, but please note that the operating system's protection may prevent the plug-in from loading. Please contact the manufacturer of the plug-in for an updated version.":
        'Plug-in không vượt qua kiểm tra nên đã bị đưa vào Blocklist. Bạn có thể bật lại, nhưng cơ chế bảo vệ của hệ điều hành có thể chặn Plug-in tải. Vui lòng liên hệ nhà sản xuất Plug-in để lấy bản mới hơn.',
    'External plug-in is used. Freezing will be done in real time.':
        'Đang dùng External Plug-in. Việc Freeze sẽ chạy theo thời gian thực.',
    'Warn if real time mixdown is required in order to include external plug-in.':
        'Cảnh báo nếu cần Mixdown theo thời gian thực để gộp External Plug-in.',

    # 9. Arranger + Surface
    'Select Active Arranger Chain + Functions':
        'Chọn Arranger Chain đang bật + chức năng',
    'The MIDI Controller Surface contains invalid elements (highlighted in orange). You can leave the Surface Editor and those elements will be removed automatically, or you can stay and modify the elements.':
        'MIDI Controller Surface có thành phần không hợp lệ (bôi cam). Bạn có thể thoát Surface Editor để tự xóa, hoặc ở lại để sửa.',
    'The MIDI Controller Surface did not contain any elements and was therefore not stored.':
        'MIDI Controller Surface không có thành phần nào nên không lưu.',
    'Show Surface Element Rectangles':
        'Hiện khung thành phần Surface',

    # 10. License (license = License, copyright stays)
    'Error: Archive Info contains license but compression is switched off!':
        'Lỗi: Thông tin Archive có License nhưng đã tắt nén!',
    'Find out more on how to activate your time-limited licenses permanently, or remove expired licenses.':
        'Tìm hiểu thêm cách kích hoạt vĩnh viễn License dùng thử, hoặc xóa License hết hạn.',
    'License check for content could not be completed! Do you want to retry?':
        'Không kiểm tra được License của nội dung! Thử lại không?',
    'No valid License found. The program will quit now.':
        'Không thấy License hợp lệ. Chương trình sẽ thoát ngay.',
    'Some content could not be loaded. Either, licenses are missing, or time-limited licenses have expired:':
        'Một số nội dung không tải được. Hoặc thiếu License, hoặc License dùng thử đã hết hạn:',
    'The program is running with a limited license. \\nYou may use it for another %s and it can be started %d more time(s).':
        'Chương trình đang chạy bằng License giới hạn. \\nBạn có thể dùng thêm %s và khởi động thêm %d lần nữa.',
    "The program is running with a limited license. \\nYou may use it for another %s. \\nTo activate a permanent license, please run the 'eLicenser Control Center'.":
        "Chương trình đang chạy bằng License giới hạn. \\nBạn có thể dùng thêm %s. \\nĐể kích hoạt License vĩnh viễn, hãy chạy 'eLicenser Control Center'.",

    # 11. Log / Intelligibility
    'If this error persists, please send the following log files to Technical Support:':
        'Nếu lỗi còn tiếp diễn, hãy gửi các file Log sau tới Hỗ trợ Kỹ thuật:',
    'Log Messages':
        'Thông điệp Log',
    'Logging':
        'Tạo Log',
    'Show Log Messages Only':
        'Chỉ hiện thông điệp Log',
    'Toggle Logging':
        'Bật/Tắt tạo Log',
    'Average Intelligibility':
        'Độ rõ tiếng trung bình',
    'Enable Intelligibility Measurement':
        'Bật đo độ rõ tiếng',
    'Intelligibility':
        'Độ rõ tiếng',
    'Jump to Next Range with Low Intelligibility':
        'Tới vùng kế tiếp có độ rõ tiếng thấp',
    'Jump to Previous Range with Low Intelligibility':
        'Tới vùng trước đó có độ rõ tiếng thấp',
    "Measurements below this value are not included in the 'Average Intelligibility' calculation":
        "Các phép đo dưới giá trị này không tính vào 'Độ rõ tiếng trung bình'",
    'Short-Term Intelligibility':
        'Độ rõ tiếng ngắn hạn',
    'Short-term intelligibility at cursor position':
        'Độ rõ tiếng ngắn hạn tại vị trí con trỏ',

    # 12. Modifier / Remote / usage
    "Click the 'Assign' Button while Holding Down Modifier Keys":
        "Nhấp nút 'Gán' trong khi giữ phím Modifier",
    'No Modifier':
        'Không có phím Modifier',
    'Popup Toolbar (static one with modifier click)':
        'Nhấn phím Modifier + click để mở dạng thanh công cụ cố định',
    'This modifier combination is used by %s.\\nDo you want to overwrite it?':
        'Tổ hợp phím Modifier này đang được dùng bởi %s.\\nBạn có muốn ghi đè lên nó không?',
    'Press up to 5 keys to assign remote keys to sections':
        'Nhấn tối đa 5 phím để gán phím Remote cho các khu vực',
    'Press up to 5 keys to assign remote keys to subsections':
        'Nhấn tối đa 5 phím để gán phím Remote cho các khu vực con',
    'Notes play when triggering chords or sections':
        'Nốt kêu khi bấm hợp âm hoặc các khu vực',
    'Notes play when triggering sections':
        'Nốt kêu khi bấm các khu vực',
    'Assign subsection to section':
        'Gán khu vực con vào khu vực cha',
    'Inserts State (Bypass Inserts with click/Context-menu shows usage)':
        'Trạng thái Insert (Nhấp để Bypass Insert / Chuột phải xem chi tiết)',
    'Modulators State (Bypass Modulators with click/Context-menu shows usage)':
        'Trạng thái Modulator (Nhấp để Bypass Modulator / Chuột phải xem chi tiết)',
    'Sends State (Bypass Sends with click/Context-menu shows usage)':
        'Trạng thái Send (Nhấp để Bypass Send / Chuột phải xem chi tiết)',

    # 13. Octave Offset -> Do lech Octave
    'Octave Offset':
        'Độ lệch Octave',
    'Octave Offset (Use Left/Right Arrow Keys to modify)':
        'Độ lệch Octave (Dùng phím mũi tên Trái/Phải để chỉnh)',
    'Octave Offset from C3':
        'Độ lệch Octave tính từ C3',
    'Voicing Range: Octave Offset from C3':
        'Voicing Range: Độ lệch Octave tính từ C3',

    # 14. Misc simplifications
    'Global mappings are saved with the program. They are available in all projects.':
        'Mapping toàn cục lưu theo chương trình. Dùng được trong mọi Project.',
    'Jump Mode (determines when the next live section will play)':
        'Jump Mode (quyết định khi nào đoạn live kế tiếp sẽ phát)',
    'Lock Layout\\nPrevents track visibility changes of the layout':
        'Khóa Layout\\nKhông cho đổi hiển thị Track của Layout',
    'Synchronize Plug-in Program Selection to Track Selection':
        'Đồng bộ Program của Plug-in theo Track đã chọn',
    'Sync Layout reflects the event selection in project':
        'Sync Layout bám theo vùng chọn Event trong Project',
    'Steps or lane settings will not transfer losslessly to the new mode.\\n\\nDo you want to continue?':
        'Step hoặc cài đặt Lane sẽ không giữ nguyên khi đổi chế độ.\\n\\nBạn có muốn tiếp tục không?',
    'Set Relative Random Values Between':
        'Đặt giá trị Random tương đối',
    'Select Available Device Panels (that will fit into this space)':
        'Chọn Panel thiết bị dùng được (vừa khung này)',
    'Selects the type of position message sent to SyncStation MIDI Out':
        'Chọn loại bản tin vị trí gửi tới SyncStation MIDI Out',
    'Selects the type of position message sent to the host':
        'Chọn loại bản tin vị trí gửi tới Host',
    'No tracks are armed: Some machines require armed tracks to perform auto edit.':
        'Không có Track nào sẵn sàng ghi: Một số máy cần Track sẵn sàng ghi để tự động sửa.',
    'No Track found with Monitoring enabled.':
        'Không thấy Track nào đang bật Monitor.',
    'Network Collaboration activated, or network configuration changed.\\n\\nMultiple network interfaces found, please select:':
        'Đã bật cộng tác mạng, hoặc cấu hình mạng đã đổi.\\n\\nTìm thấy nhiều card mạng, vui lòng chọn:',
    'This computer has multiple network interfaces. Please determine which \\ninterface is connected to the Nuendo workgroup and select the \\ncorresponding IP address. \\n\\nThe subnet mask specifies in which range broadcast messages \\nare sent to identify other Nuendo workstations. The default subnet mask \\nis a common choice, please adopt it for your specific network adapter.\\n\\nTo reopen this dialog, deactivate the network and activate it again.':
        'Máy tính có nhiều card mạng. Hãy xem card nào đang nối vào nhóm Nuendo\\nrồi chọn IP \\ntương ứng. \\n\\nSubnet mask quyết định phạm vi gửi bản tin broadcast \\nđể tìm các máy Nuendo khác. Subnet mask mặc định \\nlà lựa chọn thường dùng, cứ giữ nguyên cho card mạng của bạn.\\n\\nĐể mở lại hộp thoại này, hãy tắt mạng rồi bật lại.',
    'Respect Maximum Duration for Rhythmic Slashes in Compound Time Signatures':
        'Giữ đúng thời lượng tối đa cho dấu gạch chéo nhịp trong số chỉ nhịp phức',
    'Respect Maximum Duration for Rhythmic Slashes in Irregular Time Signatures':
        'Giữ đúng thời lượng tối đa cho dấu gạch chéo nhịp trong số chỉ nhịp bất thường',
    'The Cautionary Accidentals options only apply when the Common Practice accidental duration rule is used. A subset of options for the Modernist duration rule can be found in that section.':
        'Tùy chọn dấu hóa nhắc lại chỉ dùng khi chọn quy tắc Cổ điển. Một số tùy chọn của quy tắc Hiện đại nằm trong mục đó.',
    'This option effectively takes precedence over showing cautionary accidentals on notes in the same or different octaves in the following bar. If this option is set to show a cautionary either with or without parentheses, then other cautionary accidentals that would otherwise appear later in the bar are suppressed.':
        'Tùy chọn này ưu tiên hơn việc hiện dấu hóa nhắc lại cho nốt cùng hoặc khác quãng tám ở Bar sau. Nếu đã chọn hiện dấu nhắc lại (có hoặc không có ngoặc), các dấu hóa nhắc lại khác trong Bar sẽ bị ẩn.',
    'When bar numbers are positioned at barlines, you may prefer dynamics to be placed closer to the staff than bar numbers, or vice versa. This has no effect for bar numbers centered on the bar, which are always placed outside dynamics.':
        'Khi số Bar đặt tại vạch nhịp, bạn có thể đặt Dynamics gần khuông nhạc hơn số Bar hoặc ngược lại. Không áp dụng với số Bar căn giữa Bar, vốn luôn nằm ngoài Dynamics.',
    'The selected folder can result in a path length that is not allowed by the operating system.\\n\\nPlease select another folder.':
        'Thư mục đã chọn có thể làm đường dẫn quá dài, hệ điều hành không cho phép.\\n\\nVui lòng chọn thư mục khác.',
    'Switch between different alignment level standards (not applicable to Digital and K-System scales)':
        'Chuyển tiêu chuẩn thang đo mức (không áp dụng cho thang Digital và K-System)',
    'System Link is required for precise time alignment':
        'Cần System Link để căn thời gian chuẩn',
    'You have modified the bar offset as well as the timecode offset! Do you want to keep the project content at its timecode positions or its bar positions?':
        'Bạn đã đổi cả Bar Offset lẫn Timecode Offset! Giữ nội dung Project theo vị trí Timecode hay vị trí Bar?',
    'You have modified the bar offset! Do you want to keep the project content at its bar positions?':
        'Bạn đã đổi Bar Offset! Giữ nội dung Project theo vị trí Bar không?',
    'You have modified the timecode offset. Do you want keep the project content at its timecode positions?':
        'Bạn đã đổi Timecode Offset. Giữ nội dung Project theo vị trí Timecode không?',
    'After stopping, how many milliseconds before system can be restarted':
        'Sau khi dừng, phải đợi bao nhiêu mili-giây mới khởi động lại được',
    'How many frames of timecode are read before starting system':
        'Số Frame Timecode đọc trước khi khởi động',
    'How many frames of timecode must be missing before system is stopped':
        'Số Frame Timecode bị mất thì dừng',
    'Could not connect to CoreMIDI. You should restart your System.':
        'Không kết nối được CoreMIDI. Bạn nên khởi động lại máy.',
    "An unexpected error occurred. The system's description is: ":
        'Đã xảy ra lỗi không mong muốn. Hệ thống báo: ',
    'To have initial states sent, open the Input Routing menu and select your Note Expression Input Device':
        'Để gửi trạng thái ban đầu, hãy mở menu Input Routing và chọn thiết bị Note Expression Input của bạn',
    'To play Note Expressions, open the Input Routing menu and select your Note Expression Input Device':
        'Để phát Note Expression, hãy mở menu Input Routing và chọn thiết bị Note Expression Input của bạn',
    'To use Chord Pads activate "Monitor" of tracks where Input Routing is set to Chord Pads':
        'Để dùng Chord Pad, hãy bật "Monitor" của các Track có Input Routing là Chord Pad',
    'To use Chord Pads activate "Record Enable" or "Monitor" of tracks where Input Routing is set to Chord Pads':
        'Để dùng Chord Pad, hãy bật "Record Enable" hoặc "Monitor" của các Track có Input Routing là Chord Pad',
    'The live input is mapped to the chord track based on the selected mode':
        'Tín hiệu vào trực tiếp được gán vào Chord Track theo chế độ đã chọn',
    'The project contains files or crossfades in 32-bit float format. Since OMF does not support this format, the files will be converted and exported as embedded data. Please note that this conversion might lead to clipping!':
        'Project chứa file hoặc Crossfade ở định dạng 32-bit float. Vì OMF không hỗ trợ định dạng này, các file sẽ được chuyển đổi và export dạng dữ liệu nhúng. Lưu ý chuyển đổi này có thể gây vỡ tiếng!',
    'Do you really want to leave the page and discard your input?':
        'Bạn có thực sự muốn rời trang và bỏ những gì đã nhập?',
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
