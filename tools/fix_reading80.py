"""Round 80: manual unfiltered review - transport/mixer/media/general context fit.

Usage:
  python tools/fix_reading80.py
  python tools/fix_reading80.py --write
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
    # ---- transport: Cycle toggle consistency + panel name ----
    'Toggle: Cycle follows when locating to Markers':
        'Bật/Tắt: Cycle theo khi nhảy tới Marker',
    'Deactivated: Cycle follows when locating to Markers':
        'Đã tắt: Cycle theo khi nhảy tới Marker',
    'Max. Record Time':
        'Thời gian ghi tối đa',
    'Record: Start at Cursor/Left Locator/Selection':
        'Ghi: Bắt đầu tại con trỏ/Locator trái/vùng chọn',
    'Restore Marker Attribute Defaults':
        'Khôi phục thuộc tính Marker về mặc định',
    # Link quote + label must match (quoted-names detector)
    'Link Project and Lower Zone Editor Cursors':
        'Link con trỏ Editor giữa Project và Zone dưới',
    '"Link Project and Lower Zone Editor Cursors" not possible when using "Independent Track Loop"':
        '"Link con trỏ Editor giữa Project và Zone dưới" không khả dụng khi đang dùng "Track Loop độc lập"',
    '"Link Project and Lower Zone Editor Cursors" was turned off due to "Independent Track Loop"':
        '"Link con trỏ Editor giữa Project và Zone dưới" đã bị tắt do "Track Loop độc lập"',

    # ---- mixer: passive + pair unification ----
    'Agents: Show Channels that are Connected to the First Selected Channel':
        'Agents: Hiện các Channel nối tới Channel đầu tiên đã chọn',
    'Show Channels that are Connected to the First Selected Channel':
        'Hiện các Channel nối tới Channel đầu tiên đã chọn',
    'Cannot load settings of a channel "%s" into a channel "%s": Channel Type Mismatch.':
        'Không nạp được cài đặt của Channel "%s" vào Channel "%s": loại Channel không khớp.',
    'Do you really want to change the channel configuration?':
        'Bạn có thực sự muốn đổi cấu hình Channel không?',
    'Do you really want to remove the insert effect bank zone (%s)?':
        'Bạn có thực sự muốn gỡ Insert Effect Bank Zone (%s) không?',
    'Move Selected Tracks to New Folder with Group Channel':
        'Chuyển các Track đã chọn vào thư mục mới kèm Group Channel',
    'Move Channel Strip to Pre-Inserts Position':
        'Chuyển Channel Strip tới Pre-Inserts',
    'Pre-Fader Send.\\nClick to move to post-fader position.':
        'Send Pre-Fader.\\nNhấp để chuyển sang Post-Fader.',
    'Include MIDI Channel (for pre-configured multi-timbral external instruments - such as Samplers)':
        'Bao gồm MIDI Channel (cho External Instrument đa âm sắc cấu hình sẵn - như Sampler)',
    'Insert Input from Selected Track as Cycle Recording':
        'Chèn Input từ Track đã chọn dưới dạng ghi theo Cycle',
    'Insert Input from Selected Track as Linear Recording':
        'Chèn Input từ Track đã chọn dưới dạng ghi tuyến tính',
    'Insert as Linear Recording':
        'Chèn dưới dạng ghi tuyến tính',
    "The Locator Range is empty, inverted or its length has been changed. Please use 'Insert as Linear Recording.'":
        "Dải Locator trống, ngược hoặc đổi độ dài. Dùng 'Chèn dưới dạng ghi tuyến tính'.",
    'More than one channel are selected!\\nAre you sure you want to reset the selected Channels?':
        'Đã chọn nhiều Channel!\\nBạn có chắc muốn đặt lại các Channel đã chọn không?',
    'Combine Automation of VCA and Linked Channels':
        'Gộp Automation của VCA và Channel đã nối',

    # ---- media: typos + voice + order ----
    '- Check the Pool and convert all files to 16 or 24 bits':
        '- Kiểm tra Pool và chuyển mọi file sang 16 hoặc 24 bit',
    '- Check the Pool and convert all files to WAV, AIFF or MXF':
        '- Kiểm tra Pool và chuyển mọi file sang WAV, AIFF hoặc MXF',
    'Cannot add more tracks. The audio track count is at the limit.':
        'Không thêm được Track. Số Audio Track đã đạt giới hạn.',
    'Cannot add more tracks. The marker track count is at the limit.':
        'Không thêm được Track. Số Marker Track đã đạt giới hạn.',
    'Could not convert event (Master mob contains no valid media).':
        'Không chuyển đổi được Event (Master mob không chứa Media hợp lệ).',
    'Could not import all tracks! The data is corrupted.':
        'Không import được tất cả Track! Dữ liệu bị hỏng.',
    'Do you want to keep audio events at their sample positions?':
        'Bạn có muốn giữ các Audio Event tại vị trí Sample không?',
    'Export used attributes of these categories:':
        'Export thuộc tính đã dùng của các danh mục này:',
    'Audio Channels':
        'Audio Channel',
    'Exports the selected audio channel in real time.':
        'Export Audio Channel đã chọn theo thời gian thực.',
    'File "%s" does not exist. Do you want to remove it from the recent file list?':
        'File "%s" không tồn tại. Bạn có muốn gỡ nó khỏi danh sách file gần đây không?',
    'Maximum Load\\nClick to Show Audio Performance Panel':
        'Mức tải tối đa\\nNhấp để hiện Bảng Hiệu năng Audio',
    'Reaching the 2GB limit of the OMF file format, the followig media will not be embedded.':
        'File OMF đã chạm giới hạn 2GB, các Media sau sẽ không được nhúng.',
    'Sample rate is not supported for video export. Set the audio sample rate to 44,1 kHz or 48 kHz.':
        'Sample Rate không hỗ trợ Export Video. Đặt Sample Rate Audio thành 44.1 kHz hoặc 48 kHz.',
    "Tempo and signature tracks can only be imported if 'Bars+Beats' is selected as 'Primary Time Format'.":
        "Chỉ Import được Tempo Track và Signature Track khi đã chọn 'Bars+Beats' làm 'Primary Time Format'.",
    'The CSV file size exceeds 16 MB.\\nPlease split it into smaller sections.':
        'Kích thước file CSV quá 16 MB.\\nVui lòng chia nhỏ ra.',
    'The Clip Package contains automation. Import the automation, too?':
        'Gói Clip có Automation. Import Automation đó luôn không?',
    'The arranger track is not supported for video export. Deactivate arranger mode.':
        'Export Video không hỗ trợ Arranger Track. Tắt chế độ Arranger.',
    'The file already exists. Do you want to replace it?':
        'File đã tồn tại. Bạn có muốn thay nó không?',
    'The file is write protected! Do you want to replace it anyway?':
        'File chống ghi! Bạn vẫn muốn thay nó?',
    'The selected audio material is not suitable for tempo detection.':
        'Đoạn Audio đã chọn không phù hợp để nhận diện Tempo.',
    'The selected file path does not exist.\\nAction is canceled.':
        'Đường dẫn file đã chọn không tồn tại.\\nThao tác bị hủy.',
    'The selection cannot be moved to the trash because\\n%s\\n\\nDo you want to remove it from the Pool?':
        'Vùng chọn không chuyển vào thùng rác được vì\\n%s\\n\\nGỡ nó khỏi Pool không?',
    'Would you like to import all bitmaps in project folder?':
        'Import mọi ảnh bitmap trong thư mục Project không?',
    'The selection contains audio material with a sample rate that differs from the project sample rate.\\nBefore exporting a Clip Package, the audio clips have to be converted.':
        'Vùng chọn có đoạn Audio Sample Rate khác với Sample Rate của Project.\\nTrước khi Export gói Clip, cần chuyển các Audio Clip này.',

    # ---- general 0-100 ----
    '"%s" not possible for write protected tracks':
        'Không thể "%s" với Track chống ghi',
    '"Create Lanes from Versions" not possible for tracks that are recording':
        '"Tạo Lane từ Version" không khả dụng cho Track đang ghi',
    '"Create Versions from Lanes" not possible for tracks that are recording':
        '"Tạo Version từ Lane" không khả dụng cho Track đang ghi',
    '"Pitch Visibility: Select Next Option" not possible because no compatible instrument is connected':
        '"Hiển thị Pitch: Chọn tùy chọn kế tiếp" không khả dụng vì chưa kết nối nhạc cụ tương thích nào',
    "'%s' is not supported for clips in musical mode!":
        "'%s' không hỗ trợ Clip ở chế độ Musical!",
    "'Acoustic Feedback' When Inputting Notes With the Draw Tool":
        "'Phản hồi Acoustic' khi nhập nốt bằng Công cụ Draw",
    '- Maximum project duration for sample-precise object positions exceeded':
        '- Vượt quá thời lượng Project tối đa cho vị trí đối tượng chính xác đến Sample',
    'A controller script with the same name already exists. Use the MIDI Remote Manager to enable or delete it.':
        'Đã có Script Controller trùng tên. Dùng MIDI Remote Manager để bật hoặc xóa.',
    'Activate remote control for Voicings, Tensions and Transpose':
        'Bật điều khiển Remote cho Voicing, Tension và Transpose',
    'Activates MIDI Machine Control using these ports':
        'Bật MIDI Machine Control bằng các cổng này',
    'Added tracks of this type are currently not shown.':
        'Track mới thêm loại này hiện chưa hiển thị.',
    'All events in all clips on the active track can be selected and edited.':
        'Tất cả Event trong mọi Clip trên Track đang hoạt động đều chọn và sửa được.',
    'All events in all parts on the active track can be selected and edited.':
        'Tất cả Event trong mọi Part trên Track đang hoạt động đều chọn và sửa được.',
    'All events of the active clip can be selected and edited.':
        'Tất cả Event của Clip đang hoạt động đều chọn và sửa được.',
    'All events of the active part can be selected and edited.':
        'Tất cả Event của Part đang hoạt động đều chọn và sửa được.',
    'All source tracks will be hidden. To show the tracks again, activate them on the Visibility tab.':
        'Tất cả Source Track sẽ ẩn. Để hiện lại Track, bật chúng trên thẻ Visibility.',
    'Are you sure you want to remove all modulators of this track?':
        'Bạn có chắc muốn gỡ hết Modulator của Track này không?',
    'Attribute Counter (Number of items waiting to have their Attributes updated)':
        'Bộ đếm thuộc tính (số mục đang chờ cập nhật thuộc tính)',
    'Automatically Resolve Collisions Between Adjacent Staves and Systems':
        'Tự động xử lý chồng lấn giữa các khuông nhạc và dòng nhạc cạnh nhau',
    'Cannot add more tracks. The MIDI track count is at the limit.':
        'Không thêm được Track. Số MIDI Track đã đạt giới hạn.',
    'Cannot add more tracks. The VCA track count is at the limit.':
        'Không thêm được Track. Số VCA Track đã đạt giới hạn.',
    'Cannot add more tracks. The effect track count is at the limit.':
        'Không thêm được Track. Số Effect Track đã đạt giới hạn.',
    'Cannot add more tracks. The group track count is at the limit.':
        'Không thêm được Track. Số Group Track đã đạt giới hạn.',
    'Cannot add more tracks. The instrument track count is at the limit.':
        'Không thêm được Track. Số Instrument Track đã đạt giới hạn.',
    'Cannot add more tracks. The track count for this track type is at the limit.':
        'Không thêm được Track. Số Track loại này đã đạt giới hạn.',
    'Cannot add more tracks. The video track count is at the limit.':
        'Không thêm được Track. Số Video Track đã đạt giới hạn.',
    'Cannot save more MixConsole snapshots. The snapshot count is at the limit.':
        'Không lưu thêm được Snapshot MixConsole. Số Snapshot đã đạt giới hạn.',
    'Chords are determined by the specified setting':
        'Hợp âm tính theo cài đặt đã chọn',
    "Click 'Start' to scan for unreferenced files":
        "Nhấp 'Bắt đầu' để quét file không tham chiếu",
    'Close MIDI Controller Surface Editor and Open Mapping Assistant':
        'Đóng MIDI Controller Surface Editor và Mở Mapping Assistant',
    'Complete Signal Path + Master Effects':
        'Toàn bộ đường tín hiệu + Master Effect',
    'Complete Signal Path Including Groups and Sends':
        'Toàn bộ đường tín hiệu gồm Group và Send',
    'Complete Signal Path Including Groups and Sends, and Master FX':
        'Toàn bộ đường tín hiệu gồm Group, Send và Master FX',
    'Convert error - Please try to use different settings.':
        'Lỗi chuyển đổi - Vui lòng thử cài đặt khác.',
    'Convert to Project Settings and Copy to Project Folder If Needed':
        'Chuyển sang cài đặt Project và sao chép vào thư mục Project nếu cần',
    'Could not create the Clip Packages folder inside the project folder.':
        'Không tạo được thư mục Clip Packages trong thư mục Project.',

    # ---- general 160-230 ----
    'Found participants without master: %s. Try to reconnect?':
        'Tìm thấy người tham gia không có master: %s. Thử kết nối lại?',
    'Full Vertical expands the selection to include events from hidden controller lanes':
        'Full Vertical mở rộng vùng chọn gồm các Event từ Controller Lane đang ẩn',
    'Hide Plug-ins That Are in Active Collection':
        'Ẩn các Plug-in trong Collection đang dùng',
    'Hold values for Integrated, Range, and True Peak when playback stops':
        'Giữ giá trị Integrated, Range và True Peak khi ngừng phát',
    'How do you want to proceed for the listed tracks?':
        'Bạn muốn xử lý các Track trong danh sách thế nào?',
    'Include MIDI Patch (for multi-timbral external instruments with all sounds available on all channels - such as MIDI Expanders)':
        'Bao gồm MIDI Patch (cho External Instrument đa âm sắc có sẵn mọi âm thanh trên mọi Channel - như MIDI Expander)',
    'Indicates if Track Quick Controls are active':
        'Cho biết Quick Control của Track có bật không',
    'It is not possible to cut the selected range because the borders are inside a crossfade.':
        'Không cắt được vùng đã chọn vì ranh giới nằm trong Crossfade.',
    'Keep Plug-ins in Memory until the Application Quits':
        'Giữ Plug-in trong bộ nhớ đến khi ứng dụng thoát',
    'Keeps Silent Segments as Separate Events':
        'Giữ các Segment lặng thành Event riêng biệt',
    'Link All Word Clock Outputs (Where matching rate is possible)':
        'Nối mọi đầu ra Word Clock (khi khớp tần số)',
    'Listen to Surround Channels on Front Channels':
        'Nghe các Channel Surround qua Channel Front',
    'Minimizing files will clear the entire edit history!\\n\\nDo you want to continue?':
        'Thu gọn file sẽ xóa toàn bộ lịch sử chỉnh sửa!\\n\\nBạn có muốn tiếp tục không?',
    'Move Selected Tracks/Channels to First Available Position':
        'Chuyển Track/Channel đã chọn tới vị trí trống đầu tiên',
    'Move Selected Tracks/Channels to Last Available Position':
        'Chuyển Track/Channel đã chọn tới vị trí trống cuối cùng',
    'Move Selected Tracks/Channels to Next Available Position':
        'Chuyển Track/Channel đã chọn tới vị trí trống kế tiếp',
    'Move Selected Tracks/Channels to Previous Available Position':
        'Chuyển Track/Channel đã chọn tới vị trí trống trước đó',
    'Multiselection active: Changes are applied to all selected tracks. Settings for \'Voices\', \'Percussion\' or \'Strings and Tuning\' are not available in this mode.':
        'Đang chọn nhiều: Thay đổi áp dụng cho mọi Track đã chọn. Cài đặt \'Các bè\', \'Percussion\' hoặc \'Dây đàn và Tuning\' không dùng được ở chế độ này.',
    'Name as it is embedded in the medium & database':
        'Tên như nhúng trong Media & cơ sở dữ liệu',
    'Naming Scheme "%s" could not be found! Job will not be executed.':
        'Không tìm thấy quy tắc đặt tên "%s"! Tác vụ sẽ không chạy.',
    'No MIDI Remote Controller available. Controllers can be imported or created in the MIDI Remote Manager.':
        'Không có MIDI Remote Controller khả dụng. Có thể Import hoặc tạo Controller trong MIDI Remote Manager.',
    'No connected controller for the imported script found. In case you have a matching controller connected, select the MIDI ports below to activate it.':
        'Không tìm thấy Controller kết nối cho Script đã Import. Nếu bạn có Controller phù hợp đang cắm, hãy chọn cổng MIDI bên dưới để bật.',
    'Notes are sent out earlier to compensate for slow attack times':
        'Các nốt gửi sớm hơn để bù thời gian Attack chậm',
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
