#!/usr/bin/env python3
"""Untranslated English fragments left inside Vietnamese phrases.

The earlier passes worked on whole sentences. These are the leftovers: one
English verb, adjective or noun stranded where a Vietnamese word belongs.

  "Nothing to Add"                      -> "Nothing vào Add"
  "Apply major chord to selection"      -> "Apply major chord vào selection"
  "Global Snapshot: Apply"              -> "toàn cục Snapshot: Apply"
  "Missing Current Project Colors"      -> "Màu sắc Missing Current Project"
  "Get Default Parameter Name"          -> "Tên Get Default Parameter"
  "Drag vào Di chuyển ...\nHold [ALT] vào Copy"

Arranger, Assignment, Machine, In, Fade, Punch, Count-In, Info Line, Status
Line, List Editor and the like are Cubase feature names and are left alone.
Keys are copied verbatim from keys/all_strings.tsv.
"""

WORDING = {
    # --- Activate / Deactivate toggles -------------------------------------
    'Activate/Deactivate Write on Play': 'Bật/Tắt ghi khi phát',
    'Activate/Deactivate Learn Mode': 'Bật/Tắt chế độ Learn',
    'Activate/Deactivate Assignment Inspection View':
        'Bật/Tắt chế độ xem kiểm tra phép gán',
    'Switch: Activate Speakers': 'Chuyển: Bật loa',
    'Switch: Reference Level Active': 'Chuyển: Bật mức tham chiếu',
    'ASIO Latency Compensation Active by Default':
        'ASIO Latency Compensation bật theo mặc định',
    'Keep Current Project Active': 'Giữ Project hiện tại hoạt động',
    'Merge Active Project To Selected Network Project':
        'Gộp Project đang hoạt động vào Project mạng đã chọn',
    'Use Active MIDI Controllers': 'Dùng MIDI Controller đang hoạt động',
    'Select Active Arranger Chain + Functions':
        'Chọn Arranger Chain đang hoạt động + Chức năng',
    'Preview Active On/Off': 'Bật/Tắt Preview Active',

    # --- Add ----------------------------------------------------------------
    'Nothing to Add': 'Không có gì để thêm',
    'Select Track: Add Next': 'Chọn Track: Thêm tiếp theo',
    'Select Track: Add Prev': 'Chọn Track: Thêm trước đó',
    'Chord Editing - Add to Chord Track':
        'Sửa hợp âm - Thêm vào Chord Track',
    'MIDI Modifiers (Not for Add-ons)': 'MIDI Modifier (Không dùng cho Add-on)',

    # --- Apply ... to selection: the whole chord family was untranslated ----
    'Apply major chord to selection': 'Áp dụng hợp âm trưởng cho vùng chọn',
    'Apply minor chord to selection': 'Áp dụng hợp âm thứ cho vùng chọn',
    'Apply augmented chord to selection':
        'Áp dụng hợp âm tăng cho vùng chọn',
    'Apply diminished triad to selection':
        'Áp dụng hợp âm ba giảm cho vùng chọn',
    'Apply diminished 7th chord to selection':
        'Áp dụng hợp âm giảm cấp 7 cho vùng chọn',
    'Apply half-diminished 7th chord to selection':
        'Áp dụng hợp âm nửa giảm cấp 7 cho vùng chọn',
    'Apply suspended fourth chord to selection':
        'Áp dụng hợp âm treo cấp 4 cho vùng chọn',
    'Apply suspended second chord to selection':
        'Áp dụng hợp âm treo cấp 2 cho vùng chọn',
    'Apply Click Pattern to Equal Signatures':
        'Áp dụng Click Pattern cho các số chỉ nhịp bằng nhau',
    'Apply Color of Folder Track Automatically':
        'Tự động áp dụng màu của Folder Track',
    'Auto Apply': 'Tự động áp dụng',
    'Toggle Auto Apply': 'Bật/tắt tự động áp dụng',
    'Global Snapshot: Apply': 'Snapshot toàn cục: Áp dụng',

    # --- Arranger naming ----------------------------------------------------
    'Naming Scheme - Channel Batch Arranger Chain':
        'Quy tắc đặt tên - Arranger Chain Channel hàng loạt',
    'Naming Scheme - Single Channel Arranger Chain':
        'Quy tắc đặt tên - Arranger Chain một Channel',
    'You have to select at least one Arranger Chain.':
        'Bạn phải chọn ít nhất một Arranger Chain.',
    'Activates Arranger Mode': 'Bật chế độ Arranger',
    'Converting arrangement...': 'Đang chuyển đổi bố cục...',

    # --- Available ----------------------------------------------------------
    'Move Selected Tracks/Channels to First Available Position':
        'Di chuyển Track/Channel đã chọn tới vị trí khả dụng đầu tiên',
    'Move Selected Tracks/Channels to Last Available Position':
        'Di chuyển Track/Channel đã chọn tới vị trí khả dụng cuối cùng',
    'Move Selected Tracks/Channels to Next Available Position':
        'Di chuyển Track/Channel đã chọn tới vị trí khả dụng kế tiếp',
    'Move Selected Tracks/Channels to Previous Available Position':
        'Di chuyển Track/Channel đã chọn tới vị trí khả dụng trước đó',
    'No Cue Available': 'Không có Cue khả dụng',
    'No Editor Available': 'Không có Editor khả dụng',
    'No Options Available.': 'Không có tùy chọn khả dụng.',
    'No Parameters Available': 'Không có tham số khả dụng',
    'No Parameters Available.': 'Không có tham số khả dụng.',
    'Set Highest Available Scale Note': 'Đặt Note Scale khả dụng cao nhất',
    'Set Lowest Available Scale Note': 'Đặt Note Scale khả dụng thấp nhất',
    'Set up Available Controllers...': 'Thiết lập Controller khả dụng...',

    # --- Column / list / line ----------------------------------------------
    'Generate Column Headings': 'Tạo tiêu đề cột',
    'Restore Default Column Widths': 'Khôi phục độ rộng cột mặc định',
    'Split Using Column:': 'Tách theo cột:',
    'Keep Editor Contents': 'Giữ nội dung Editor',
    'Keep Editor Contents On/Off': 'Giữ nội dung Editor Bật/Tắt',
    'Delete Log Entry from List': 'Xóa mục Log khỏi List',
    'Highlight Suggestions from List Tab':
        'Đánh dấu gợi ý từ thẻ List',
    'Show List Assistant Colors': 'Hiện màu cho List Assistant',
    'Clear List': 'Xóa List',

    # --- Copy / get / reset -------------------------------------------------
    'Drag to Move EQ Band Settings\\nHold [ALT] to Copy':
        'Kéo để di chuyển cài đặt EQ Band\\nGiữ [ALT] để sao chép',
    'Global Copy': 'Sao chép toàn cục',
    'New Copy': 'Tạo bản sao',
    'To Real Copy': 'Tới bản sao thật',
    'Copy Current Collection': 'Sao chép Collection hiện tại',
    'First Repeat of Current Chain Step':
        'Lặp lại đầu tiên của Chain Step hiện tại',
    'Last Repeat of Current Chain Step':
        'Lặp lại cuối cùng của Chain Step hiện tại',
    'Missing Current Project Colors': 'Thiếu màu của Project hiện tại',
    'Reset Current Picture': 'Đặt lại Picture hiện tại',
    'Get Default Parameter Name': 'Lấy tên tham số mặc định',
    'Parts Get Track Names': 'Parts lấy tên Track',
    'Extract First Patch': 'Trích xuất Patch đầu tiên',
    'Rename First Selected Track': 'Đổi tên Track đã chọn đầu tiên',
    'Synchronize Track Data with Chord Track First':
        'Đồng bộ dữ liệu Track với Chord Track trước',
    'Switch Presets/Hide Track Pictures':
        'Chuyển Preset / Ẩn Picture Track',

    # --- Read / Write enable ------------------------------------------------
    'Toggle Read Enable Selected Tracks':
        'Bật/tắt Read Enable cho Track đã chọn',
    'Toggle Write Enable Selected Tracks':
        'Bật/tắt Write Enable cho Track đã chọn',

    # --- last / first -------------------------------------------------------
    'Go to Last Edited Channel': 'Tới Channel sửa lần cuối',
    'Keep Last': 'Giữ lần cuối',
    'Keep Last[RM]': 'Giữ lần cuối[RM]',
    'Use Last Applied Color': 'Dùng màu đã áp dụng lần cuối',
    'First Line Indent': 'Thụt lề dòng đầu tiên',
    'Show Vertical Line': 'Hiện đường thẳng đứng',
    'Single Line Only': 'Chỉ một dòng',
    'Show Marker Lines': 'Hiện đường Marker',
    'Sustain Pedal Appearance for Continuation of Line':
        'Hiển thị Sustain Pedal khi nối tiếp dòng',
    'Sustain Pedal Appearance for Start of Line':
        'Hiển thị Sustain Pedal khi bắt đầu dòng',
    'Tools - Show Horizontal Cross Hair Cursor Line':
        'Công cụ - Hiện đường ngang của con trỏ chữ thập',
    'Tools - Show Vertical Cross Hair Cursor Line':
        'Công cụ - Hiện đường dọc của con trỏ chữ thập',

    # --- load ---------------------------------------------------------------
    'Average Real Time Load': 'Tải trung bình thời gian thực',
    'Maximum Load': 'Tải tối đa',

    # --- export wording -----------------------------------------------------
    'Select Attributes to Export:': 'Chọn thuộc tính để Export:',
    'Select Marker Tracks for Export': 'Chọn Marker Track để Export',
    'Export Sample Rate': 'Export Sample Rate',
    'Export Sample Size': 'Export kích thước Sample',
    'Export as': 'Export thành',
    'Export as Type 0': 'Export thành Type 0',
    'Export list as text': 'Export list dưới dạng text',
    'Export List': 'Export danh sách',
    'Export Resolution': 'Export độ phân giải',
    'Export MIDI Device Setup': 'Export cài đặt thiết bị MIDI',
    'Export Setup': 'Export cài đặt',
    'Export Warnings': 'Export cảnh báo',
    'Export Audio Mixdown of entire Project':
        'Export Audio Mixdown của toàn bộ Project',
    'Export Muted Events with Volume -inf dB':
        'Export Event bị Mute với Volume -inf dB',
    'Exporting arrangement...': 'Đang Export bố cục...',
    'Exporting audio file: %s': 'Đang Export file Audio: %s',
    'Exporting audio track: %s': 'Đang Export Track Audio: %s',
    'Exporting events...': 'Đang Export Event...',
    'Exporting tracks...': 'Đang Export Track...',
    'Exporting video file...': 'Đang Export file Video...',
    'Exporting video file: %s': 'Đang Export file Video: %s',
    'Exporting video track: %s': 'Đang Export Track Video: %s',
    'Exporting video...': 'Đang Export Video...',
    'Exporting audio...': 'Đang Export Audio...',

    # --- misc ---------------------------------------------------------------
    'Some content could not be loaded. Either, licenses are missing, or '
    'time-limited licenses have expired:':
        'Một số nội dung không thể tải. Hoặc là thiếu bản quyền, hoặc bản quyền '
        'có thời hạn đã hết hạn:',
    'No Auto Disable': 'Không tự động tắt',
    'Audio Pre-Record Seconds': 'Số giây ghi trước của Audio',
    'Audio Record Mode': 'Chế độ ghi Audio',
}
