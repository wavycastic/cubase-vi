#!/usr/bin/env python3
"""Vietnamese that parses but does not read naturally.

Grouped by the tell that exposed it, because the fix differs by group:

  verb + English object   the object stayed after the verb, which is English
                          order. Vietnamese puts it in front
  untranslated negation   "Không thể read source file" - the negation was
                          applied but the verb was not translated
  repeated word           "Vùng Vùng chọn", "Mở Editor Editor"
  dangling của            "Send 'Shuttle' instead của 'FF/Rewind'" - a
                          Vietnamese "của" where English had none
  capital run             a quoted or literal name never translated, or a
                          preposition glued onto a quoted name

Keys are copied verbatim from keys/all_strings.tsv.
"""

WORDING = {
    # --- verb + English object: the object belongs in front ----------------
    'Activate selected profile': 'Bật Profile đã chọn',
    'Delete selected profile': 'Xóa Profile đã chọn',
    'Duplicate selected profile': 'Nhân bản Profile đã chọn',
    'Export selected profile as file': 'Export Profile đã chọn thành file',
    'Load available update': 'Tải bản cập nhật khả dụng',
    'Load next Program': 'Tải Program kế tiếp',
    'Load previous Program': 'Tải Program trước đó',
    'Open New Projects': 'Mở các Project mới',
    'Open Other...': 'Mở mục Khác...',
    'Select New': 'Chọn mục Mới',
    'Select Other': 'Chọn mục Khác',
    'Select Next Marker': 'Chọn Marker kế tiếp',
    'Select Previous Marker': 'Chọn Marker trước đó',
    'Select Next Player': 'Chọn Player kế tiếp',
    'Select Previous Player': 'Chọn Player trước đó',
    'Select Next Time Format': 'Chọn định dạng thời gian kế tiếp',
    'Select Next Track': 'Chọn Track kế tiếp',
    'Select Previous Track': 'Chọn Track trước đó',
    'Select Active Arranger Chain': 'Chọn Arranger Chain đang hoạt động',
    'Show Active Clip': 'Hiện Clip đang hoạt động',
    'Show Next Page': 'Hiện trang kế tiếp',
    'Delete Selected Player': 'Xóa Player đã chọn',
    'Delete Selected Snapshot': 'Xóa Snapshot đã chọn',
    'Rename Selected Player': 'Đổi tên Player đã chọn',
    'Save Selected Channels': 'Lưu cài đặt Channel đã chọn',
    'Save Selected Channels...': 'Lưu cài đặt Channel đã chọn...',
    'Load Selected Channels': 'Tải cài đặt Channel đã chọn',
    'Load Selected Channels...': 'Tải cài đặt Channel đã chọn...',
    'Use Current Pan Settings': 'Dùng cài đặt Pan hiện tại',
    'Use Current Mix Levels': 'Dùng mức Mix hiện tại',
    "Copy First Selected Channel's Settings":
        'Sao chép cài đặt của Channel đã chọn đầu tiên',
    'Add Selected Effect "%s" to Favorites':
        'Thêm Effect đã chọn "%s" vào mục yêu thích',
    'Add Selected Instrument "%s" to Favorites':
        'Thêm Instrument đã chọn "%s" vào mục yêu thích',
    'Add new profile with factory settings':
        'Thêm Profile mới với cài đặt xuất xưởng',

    # --- untranslated negation ---------------------------------------------
    'Cannot read source file': 'Không thể đọc file nguồn',
    'Cannot write OMF media: %s': 'Không thể ghi media OMF: %s',
    'Could not read OMF file!': 'Không thể đọc file OMF!',
    'No Controller Lanes Presets': 'Không có Preset Controller Lane',
    'No MIDI Controller Connected': 'Không có MIDI Controller nào kết nối',
    'No MIDI Controller selected': 'Chưa chọn MIDI Controller',
    'No Supported Editor Open': 'Không có Editor được hỗ trợ nào đang mở',
    'No Tempo Change necessary!': 'Không cần thay đổi Tempo!',
    'No audio dropouts detected': 'Không phát hiện điểm rớt Audio nào',
    'No more inserts slots available.': 'Không còn ô Insert trống',
    'No more send slots available.': 'Không còn ô Send trống',
    'No unassigned pad available': 'Không có Pad chưa gán nào khả dụng',
    'No valid Composition found.': 'Không tìm thấy Composition hợp lệ nào',

    # --- repeated word ------------------------------------------------------
    'Selection Range': 'Vùng chọn',
    'Range Selection': 'Chọn vùng',
    'Repeat Forever': 'Lặp vô hạn',
    'Open Editor Commands open Editors in Lower Zone':
        'Lệnh Open Editor mở Editor trong Lower Zone',
    'Track Display Settings: Active Track Only':
        'Cài đặt hiển thị Track: chỉ Track đang hoạt động',
    'Track Display Settings: All Visible Tracks':
        'Cài đặt hiển thị Track: tất cả đang hiện',
    'Track Display Settings: Show/Hide Tracks in Editor':
        'Cài đặt hiển thị Track: Hiện/Ẩn Track trong Editor',
    'Track Display Settings: Toggle Modes':
        'Cài đặt hiển thị Track: Đảo chế độ',
    '"Assign to First Unassigned Pad": No Unassigned Pads':
        '"Gán cho Pad chưa gán đầu tiên": Không có Pad chưa gán nào',
    'Insert Retrospective Recording from All MIDI Inputs on Selected Track':
        'Chèn bản ghi hồi cứu từ mọi MIDI đầu vào vào Track đã chọn',
    'Tempo (changes the current tempo at the project cursor position)':
        'Thay đổi Tempo hiện tại tại vị trí con trỏ Project',

    # --- dangling "của" from an English "instead of" ------------------------
    "Send 'Shuttle' instead of 'FF/Rewind'": "Gửi 'Shuttle' thay cho 'FF/Rewind'",
    "Send 'Still' instead of 'Stop'": "Gửi 'Still' thay cho 'Stop'",
    'Copy of ': 'Bản sao của ',
    'Pick-up Bar of:': 'Bar lấy đà của:',

    # --- leftover verb + English object -------------------------------------
    'Add selected Users to Permission Preset':
        'Thêm người dùng đã chọn vào Preset Permission',
    'Remove selected Users from Permission Preset':
        'Gỡ bỏ người dùng đã chọn khỏi Preset Permission',
    'Number of record enabled tracks': 'Số Track đang bật ghi',
    'Other Project Settings': 'Cài đặt Project khác',
    'Perform Export Selected Events': 'Thực hiện Export các Event đã chọn',
    'Toggle Selected Track': 'Bật/tắt Track đã chọn',
}
