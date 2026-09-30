"""Round 79: 5-agent vet sweep - remaining passives, filler drops.

Consolidated from 5 subagent reports; regressions and lateral churn rejected.
Usage:
  python tools/fix_reading79.py
  python tools/fix_reading79.py --write
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
    # ---- vet passives ----
    '- Negative project start offset has been reset to zero':
        '- Đã đặt lại độ lệch bắt đầu Project âm về 0',
    'All connections routed to the side-chain inputs have been reset. Your project may sound differently.':
        'Đã đặt lại mọi kết nối tới đầu vào Side-Chain. Âm thanh Project có thể khác đi.',
    'Currently used in the following sound slots:\\n%s':
        'Các Sound Slot sau đang dùng:\\n%s',
    'Error in voice conversion. Some parts were processed in Auto mode instead.':
        'Lỗi chuyển đổi bè. Một số Part xử lý ở chế độ Auto thay thế.',
    'Multiple clips are selected. The displayed metadata refers to the first clip.':
        'Đã chọn nhiều Clip. Thông tin hiển thị là của Clip đầu tiên.',
    'One marker track was added before aborting.':
        'Đã thêm một Marker Track trước khi hủy.',
    'The device ports saved in the preset are already used. Applying this preset will replace any previous connections.':
        'Preset lưu các cổng thiết bị đang bận. Áp dụng Preset này sẽ thay mọi kết nối trước đó.',
    'The following plug-ins have been added to the Blocklist:':
        'Thêm các Plug-in sau vào Blocklist:',
    'The name is already in use, please enter a new name.':
        'Tên này trùng, vui lòng nhập tên mới.',
    'The port is currently used!\\nHiding it will disconnect it.':
        'Cổng này đang bận!\\nẨn đi sẽ ngắt kết nối.',
    'The project has been moved to a location that is read only!\\nPlease select a new project working directory!':
        'Project chuyển tới vị trí chỉ đọc!\\nVui lòng chọn thư mục làm việc mới cho Project!',
    'The time format was changed to Bars+Beats!':
        'Chuyển định dạng thời gian thành Bars+Beats!',
    'These were replaced by nearest new color.':
        'Đã thay chúng bằng màu mới gần nhất.',
    'This plug-in has been moved to the blocklist.':
        'Đã chuyển Plug-in này vào Blocklist.',
    'Your local user name is already used by another computer on the network. The network will be reset.':
        'Máy khác trong mạng đã dùng tên user này. Sẽ đặt lại mạng.',
    'To play Note Expressions, open the Input Routing menu and select your Note Expression Input Device':
        'Để phát Note Expression, mở menu Input Routing và chọn thiết bị Note Expression Input',
    ' (used by %s)':
        ' (do %s dùng)',
    '- No tracks are selected for export':
        '- Không chọn Track nào để Export',
    'All notes are recorded into the same part.':
        'Ghi mọi nốt vào cùng một Part.',
    "All projects must be closed before 'cleanup'!":
        "Đóng mọi Project trước khi 'dọn dẹp'!",
    'Project has not been saved.':
        'Chưa lưu Project.',
    "Project will be exported as\\n'%s'.":
        "Export Project thành\\n'%s'.",
    'The destination parameter has been changed.':
        'Đổi tham số đích.',
    'There are no tracks selected for download.':
        'Không chọn Track nào để tải về.',
    'This Favorite has already been added!':
        'Mục yêu thích này thêm rồi!',
    'Property Is Set':
        'Thuộc tính đã đặt',

    # ---- vui-long trims ----
    'Auto Save failed, because the project is corrupt.\\nPlease save the project under a new name and restart the program.':
        'Không tự động lưu được vì Project hỏng.\\nLưu Project sang tên mới rồi khởi động lại chương trình.',
    'Could not interpret the CSV file. Maybe the file is in the wrong CSV format?\\nPlease check the separator setting.\\nAn error was found near this position:\\n\\n':
        'Không đọc được file CSV. Có thể sai định dạng CSV?\\nKiểm tra dấu phân cách.\\nLỗi gần vị trí này:\\n\\n',
    'Could not interpret the CSV file. Please check your separator settings.\\nAn error was found near this position:\\n\\n':
        'Không đọc được file CSV. Kiểm tra dấu phân cách.\\nLỗi gần vị trí này:\\n\\n',
    'Network Collaboration activated, or network configuration changed.\\n\\nMultiple network interfaces found, please select:':
        'Đã bật cộng tác mạng hoặc đổi cấu hình mạng.\\n\\nTìm thấy nhiều card mạng, chọn:',
    'No Mappable Controller found, please connect a supported MIDI Controller':
        'Không thấy Controller gán được, kết nối MIDI Controller hỗ trợ',
    'No active project for import!\\nPlease create and set up a new project.':
        'Không có Project nào hoạt động để import!\\nTạo và thiết lập Project mới.',
    'Please select a project.\\nIn case no projects are online,\\nyou cannot join.':
        'Chọn một Project.\\nNếu không có Project trực tuyến,\\nkhông tham gia được.',
    'Reactivating the plug-in failed!\\nFor support information, please contact the plug-in vendor.':
        'Không kích hoạt lại được Plug-in!\\nLiên hệ nhà cung cấp Plug-in để hỗ trợ.',
    "The Locator Range is empty, inverted or its length has been changed. Please use 'Insert as Linear Recording.'":
        "Dải Locator trống, ngược hoặc đổi độ dài. Dùng 'Chèn dạng bản ghi tuyến tính'.",
    'The Setup provided on this page will be discontinued. Please use MIDI Remote in the lower zone of the Project window.':
        'Thiết lập trang này sắp bỏ. Dùng MIDI Remote ở Zone dưới cửa sổ Project.',
    'The clip of the selected audio event is in musical mode. Please turn off musical mode for the clip.':
        'Clip của Audio Event đã chọn đang ở chế độ Musical. Tắt chế độ Musical cho Clip.',
    'The clip of the selected audio event is in musical mode. \\nPlease turn off musical mode for the clip.':
        'Clip của Audio Event đã chọn đang ở chế độ Musical. \\nTắt chế độ Musical cho Clip.',
    "The plug-in could not be validated and has been moved to the blocklist. You can reactivate the plug-in, but please note that the operating system's protection may prevent the plug-in from loading. Please contact the manufacturer of the plug-in for an updated version.":
        'Plug-in không vượt qua kiểm tra nên vào Blocklist. Bật lại được, nhưng bảo vệ hệ điều hành có thể chặn Plug-in tải. Liên hệ nhà sản xuất Plug-in để lấy bản mới.',
    'The project file has been moved!\\nPlease confirm the project working directory!\\n\\nDocument path is: %s\\n\\nNew (1):\\t%s\\nOld (2):\\t%s':
        'File Project đã chuyển chỗ!\\nXác nhận thư mục làm việc của Project!\\n\\nĐường dẫn file là: %s\\n\\nMới (1):\\t%s\\nCũ (2):\\t%s',
    'The selected folder can result in a path length that is not allowed by the operating system.\\n\\nPlease select another folder.':
        'Thư mục đã chọn làm đường dẫn quá dài, hệ điều hành không cho phép.\\n\\nChọn thư mục khác.',
    'No name specified. Please enter a name.':
        'Chưa đặt tên. Nhập tên.',
    'No project is active. Please create or load a project.':
        'Không có Project nào hoạt động. Tạo hoặc tải Project.',
    'Please select an audio track':
        'Chọn Audio Track',
    'Please select an event.':
        'Chọn Event.',
    'Please select either tracks or a project!':
        'Chọn Track hoặc Project!',
    'The export range is empty. Please set the left and right locators.':
        'Dải Export trống. Đặt Left Locator và Right Locator.',
    'The name you entered is not a valid file name:\\n%s\\nPlease enter a new name.':
        'Tên vừa nhập không hợp lệ:\\n%s\\nNhập tên mới.',
    'The project has been moved to a location that is read only!\\nPlease select a new project working directory!':
        'Project đã chuyển tới vị trí chỉ đọc!\\nChọn thư mục làm việc mới cho Project!',

    # ---- thuc hien trims ----
    'All Events matching Filter Condition and perform Actions':
        'Tất cả Event khớp điều kiện lọc và chạy Action',
    'Perform Audio Export':
        'Export Audio',
    'Perform Export Selected Events':
        'Export các Event đã chọn',
    'Perform the actions on all events matching the filter conditions':
        'Chạy Action trên mọi Event khớp điều kiện lọc',
    'Error during operation: %s \\nAll files created so far will be deleted.':
        'Lỗi: %s \\nMọi file đã tạo sẽ bị xóa.',
    'Are you sure you want to delete the snapshot? \\nYou cannot undo this.':
        'Bạn có chắc muốn xóa Snapshot này không?\\nKhông hoàn tác được.',
    'Are you sure? You cannot undo this!':
        'Bạn có chắc không? Không hoàn tác được!',
    'Error during file copy! The operation must be canceled!':
        'Lỗi sao chép file! Phải hủy!',
    'Locked tracks cannot be changed with this operation.':
        'Không đổi được Track đã khóa.',
    'The remaining disk space (%s) is insufficient for this operation.\\nRequired space is about %s.':
        'Đĩa còn lại (%s) không đủ.\\nCần khoảng %s.',
    'There is not enough disk space for this operation!':
        'Không đủ dung lượng đĩa!',
    'This operation is not allowed.':
        'Không được phép.',
    'This operation will invalidate the VariAudio data.':
        'Làm hỏng dữ liệu VariAudio.',
    'This operation will remove offline process histories.\\nAll edits will be frozen!':
        'Xóa lịch sử xử lý Offline.\\nMọi chỉnh sửa sẽ Freeze!',
    'Warning: You cannot undo this operation!\\nOffline process histories will be removed.\\nAll edits will be frozen!':
        'Cảnh báo: Không hoàn tác được!\\nLịch sử xử lý Offline sẽ mất.\\nMọi chỉnh sửa sẽ Freeze!',
    'Warning: You cannot undo this!':
        'Cảnh báo: Không hoàn tác được!',
    'You cannot undo this operation! Do you want to continue?':
        'Không hoàn tác được! Bạn có muốn tiếp tục không?',

    # ---- transport/mixer remnants ----
    'Copy Automation of All Tracks (Locator Range)':
        'Sao chép Automation mọi Track (Dải Locator)',
    'Copy Automation of Selected Parameters (Locator Range)':
        'Sao chép Automation tham số đã chọn (Dải Locator)',
    'Copy Automation of Selected Tracks (Locator Range)':
        'Sao chép Automation các Track đã chọn (Dải Locator)',
    'Paste Automation to All Tracks (Locator Range)':
        'Dán Automation vào mọi Track (Dải Locator)',
    'Paste Automation to Selected Parameters (Locator Range)':
        'Dán Automation vào tham số đã chọn (Dải Locator)',
    'Paste Automation to Selected Tracks (Locator Range)':
        'Dán Automation vào Track đã chọn (Dải Locator)',
    'Automatically Adjust Grid at Current Grid-Resolution':
        'Tự động chỉnh Grid theo độ phân giải hiện tại',
    'Defines what happens DURING cycle recording...':
        'Chọn cách xử lý khi ghi Cycle...',
    'New parts are created in each cycle and all of them are played back.':
        'Mỗi Cycle tạo Part mới và phát lại tất cả.',
    'New parts are created in each cycle, but only the last one is played back (others are muted).':
        'Mỗi Cycle tạo Part mới, chỉ phát lại Part cuối (các Part khác bị Mute).',
    'Project Preview start set to project cursor position.':
        'Điểm bắt đầu Project Preview đặt tại con trỏ Project.',
    'Tempo events are generated up to the point, where an irregular tempo change is detected.\\nApply the Smooth Tempo function if the tempo of the material is assumed to be constant.':
        'Tempo Event tạo tới điểm phát hiện Tempo đổi bất thường.\\nDùng Smooth Tempo nếu Tempo đoạn nhạc ổn định.',
    "Activate this to send a 'Still' command instead of a 'Stop' command to RS422 Out":
        "Bật để gửi 'Still' thay vì 'Dừng' tới RS422 Out",
    'Activate this to send record commands to RS422 Out':
        'Bật để gửi lệnh ghi tới RS422 Out',
    'Activate this to send record commands to SyncStation MIDI Out':
        'Bật để gửi lệnh ghi tới SyncStation MIDI Out',
    'Bypass Channel Strip of All Visible Channels':
        'Bypass Channel Strip mọi Channel đang hiện',
    "Copy First Selected Channel's Settings":
        'Sao chép cài đặt Channel đã chọn đầu tiên',

    # ---- media/ui remnants ----
    '" already in Pool.\\nDo you want to create a new version or use the existing?':
        '" đã có trong Pool.\\nTạo Version mới hay dùng Version hiện có?',
    '" already in the Pool.\\nDo you want to create a new version?':
        '" đã có trong Pool.\\nTạo Version mới không?',
    '%s has detected that new audio drivers are available on your computer. Please select the audio driver for the audio hardware that you want to use with %s.':
        '%s phát hiện có Driver Audio mới trên máy. Chọn Driver Audio cho thiết bị Audio muốn dùng với %s.',
    '- %i event(s) with zero length inside the AAF file':
        '- %i Event dài 0 trong file AAF',
    '- A wrong project bit rate will affect copied and consolidated audio files':
        '- Bit Rate Project sai sẽ ảnh hưởng file Audio sao chép và gộp',
    'A file cannot be replaced if it has multiple edit versions!\\nInstead, new files can be created and replaced in the Pool!':
        'Không thay được file có nhiều phiên bản chỉnh sửa!\\nTạo file mới rồi thay trong Pool!',
    'A file name cannot contain any of the following characters':
        'Tên file không chứa ký tự sau',
    'A file named\\n%s\\nalready exists in the Pool.\\nIt is not possible to replace it.\\nPlease use another name or another location.':
        'File tên\\n%s\\nđã có trong Pool.\\nKhông thay được file này.\\nDùng tên khác hoặc vị trí khác.',
    'ASIO-Guard has been disabled, because the ASIO Buffer Size is too large for the selected ASIO-Guard Level.\\n\\nIn Studio > Studio Setup > VST Audio System, you may want to select a smaller ASIO Buffer Size or a higher ASIO-Guard Level.':
        'ASIO-Guard đã tắt vì ASIO Buffer quá lớn so với mức ASIO-Guard đã chọn.\\n\\nTrong Studio > Thiết lập Studio > VST Audio System, chọn ASIO Buffer nhỏ hơn hoặc mức ASIO-Guard cao hơn.',
    'All settings from source will be transferred to new tracks (incl. automation). Audio file is dry on hard disk.':
        'Mọi cài đặt từ nguồn chuyển sang Track mới (gồm Automation). File Audio ở dạng Dry trên đĩa.',
    'Could not open the file for reading.\\nIs the file already opened by another program?':
        'Không mở được file để đọc.\\nFile đang mở ở chương trình khác không?',
    'Creates a single audio file from multiple selected tracks, events/parts from different tracks or from instrument/MIDI tracks with multiple outputs.':
        'Tạo file Audio từ nhiều Track đã chọn, Event/Part khác Track, hoặc Instrument Track/MIDI Track nhiều đầu ra.',
    'Database removal failed because the database file is write protected.\\n':
        'Không xóa được cơ sở dữ liệu vì file bị bảo vệ ghi.\\n',
    'Do you want to adjust the Project Settings, or allow the Project to run at the\\ndifferent Sample Rate?':
        'Điều chỉnh cài đặt Project hay cho Project chạy ở\\nSample Rate khác?',
    '"%s" is already used as key command by "%s->%s".\\nDo you want to reassign this existing key command?':
        '"%s" đã dùng làm phím tắt cho "%s->%s".\\nGán lại phím tắt này không?',
    'Double-click to rename Link Group (Shift + Double-click to open Link Group Settings dialog)':
        'Nhấp đúp đổi tên Link Group ([SHIFT] + nhấp đúp mở hộp thoại cài đặt Link Group)',
    'The remaining disk space (%s) is insufficient for this operation.\\nRequired space is about %s.':
        'Đĩa còn lại (%s) không đủ cho thao tác này.\\nCần khoảng %s.',
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
for k, v in list(changed.items())[:12]:
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
