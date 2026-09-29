#!/usr/bin/env python3
"""Fix the 31 strings where English sits inside a Vietnamese phrase.

Same defect family as the earlier leak pass: the automated run translated
some words of an English key and left the rest, producing
"Đặt Spacer between Selected Events" or "Không thể Tạo Liên kết for:".
Each one is rewritten here.
"""

WORDING = {
    # --- "from" stranded at the front --------------------------------------
    'From Track Preset...': 'Từ Track Preset...',

    # --- freeze cache -------------------------------------------------------
    'The cache file for frozen channel "%s" could not be found. The channel '
    'will be unfrozen.':
        'Không tìm thấy file cache của Channel đã Freeze "%s". Channel sẽ được '
        'bỏ Freeze.',
    'The cache file for frozen instrument "%s" could not be found. The '
    'instrument will be unfrozen.':
        'Không tìm thấy file cache của Instrument đã Freeze "%s". Instrument sẽ '
        'được bỏ Freeze.',

    # --- AFL / listen mode --------------------------------------------------
    'Activate to use After Fader Listen Mode':
        'Bật để dùng chế độ After Fader Listen',
    'After Fader Listen Mode': 'Chế độ After Fader Listen',
    'Listen for All Visible Channels On/Off':
        'Bật/Tắt Listen cho mọi Channel đang hiện',

    # --- string / staff navigation -----------------------------------------
    'Add String Above': 'Thêm dây phía trên',
    'Add String Below': 'Thêm dây phía dưới',

    # --- "after" / "under" / "between" stranded mid-phrase ------------------
    'Allow Continue Writing after Transport Jump':
        'Cho phép tiếp tục ghi sau khi Transport nhảy',
    'Allow Rests Within Beams': 'Cho phép dấu lặng trong đuôi nốt',
    'Create Audio Images During Record': 'Tạo Audio Image trong lúc ghi',
    'Duplicate Selected Tracks without Data':
        'Nhân bản Track đã chọn mà không kèm dữ liệu',
    'Insert Reset Events after Record': 'Chèn Event đặt lại sau khi ghi',
    'Open Effect Editor After Loading it': 'Mở Effect Editor sau khi tải nó',
    'Open Sample Editor after Completion': 'Mở Sample Editor sau khi hoàn tất',
    'Select Events under Cursor': 'Chọn Event dưới con trỏ',
    'Stop after Automatic Punch Out': 'Dừng sau khi tự động Punch Out',
    'Use Time-Linear Count-In during Pre-roll':
        'Dùng Count-In dạng Time-Linear trong Pre-roll',
    'Hardware Reset without releasing USB connection':
        'Đặt lại phần cứng mà không ngắt kết nối USB',
    'Project size of %s exceeded during auto save!':
        'Kích thước Project %s vượt quá giới hạn trong lúc tự động lưu!',
    'Could not create link for:\\n': 'Không thể tạo liên kết cho:\\n',
    'Script could not be imported. A Script for %s - %s already exists. Use '
    "the 'Delete Script' button first.":
        'Không thể Import Script. Một Script cho %s - %s đã tồn tại. '
        "Vui lòng dùng nút 'Xóa Script' trước.",
    "Above Specific Instruments' Staves":
        "Khuông nhạc của các nhạc cụ cụ thể phía trên",
    "Disable 'Acoustic Feedback' during Playback":
        "Tắt 'Acoustic Feedback' trong lúc phát lại",
    'Set Random Values Between': 'Đặt giá trị ngẫu nhiên trong khoảng',
    'Set Relative Random Values Between':
        'Đặt giá trị ngẫu nhiên tương đối trong khoảng',
    'Set Spacer between Selected Events': 'Đặt Spacer giữa các Event đã chọn',
    'Switch between A/B Settings': 'Chuyển giữa cài đặt A/B',
    'Switch between different Peak Program Meter scale standards':
        'Chuyển giữa các tiêu chuẩn thang Peak Program Meter khác nhau',

    # --- Cross-Over / beam groups ------------------------------------------
    'Automation Mode - Cross-Over': 'Chế độ Automation - Cross-Over',
    'Number of Lines in Primary Beam Within Secondary Beam Groups':
        'Số dòng trong đuôi nốt chính trong các nhóm đuôi nốt phụ',
    'Beam over Rests': 'Nốt đuôi qua dấu lặng',
}
