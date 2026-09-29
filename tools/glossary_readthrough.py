#!/usr/bin/env python3
"""Found by reading the map domain by domain, not by pattern.

Everything here reads wrong in Vietnamese. Grouped by the shape of the defect:

  word order flipped   the noun phrase stayed in English order around the
                       Vietnamese verb: "Send Common Reverb", "Gain EQ Band 1",
                       "Danh mục Channel/", "Panner Channel \"%s\" -"
  preposition wrong    "vào" where "sang" or "thành" is meant
  broken               a Vietnamese word landed in the middle of English
  inconsistent         the same Cubase term rendered two ways

Keys are copied verbatim from keys/all_strings.tsv.
"""

WORDING = {
    # ======================================================================
    # word order flipped
    # ======================================================================
    'CC: FX1 Reverb Send': 'CC: FX1 Reverb Send',
    'CC: FX2 Send': 'CC: FX2 Send',
    'CC: FX3 Chorus Send': 'CC: FX3 Chorus Send',
    'CC: FX4 Variation Send': 'CC: FX4 Variation Send',
    'CC: FX5 Send': 'CC: FX5 Send',
    'Common Reverb Send': 'Common Reverb Send',
    'Change Insert Effect Configuration': 'Thay đổi cấu hình Effect Insert',
    'Change channel of notes': 'Đổi Channel của các nốt',
    'Channel "%s" - Panner': 'Panner của Channel "%s"',
    'Channel/Category': 'Channel/Danh mục',
    'Colorize Selected Channel': 'Tô màu Channel đã chọn',
    'Color Menu': 'Menu màu',
    'Mute All Audio Effects in Bus': 'Mute toàn bộ Effect Audio của Bus',
    'EQ Band 1 Gain': 'Gain EQ Band 1',
    'EQ Band 2 Gain': 'Gain EQ Band 2',
    'EQ Band 3 Gain': 'Gain EQ Band 3',
    'EQ Band 4 Gain': 'Gain EQ Band 4',
    'EQ Band 1 Q-Factor': 'Q-Factor của EQ Band 1',
    'EQ Band 2 Q-Factor': 'Q-Factor của EQ Band 2',
    'EQ Band 3 Q-Factor': 'Q-Factor của EQ Band 3',
    'EQ Band 4 Q-Factor': 'Q-Factor của EQ Band 4',
    'Channel Strip Drive Level': 'Mức Drive của Channel Strip',
    'Channel Strip Morph Factor': 'Hệ số Morph của Channel Strip',
    'Global IP Network': 'IP Network toàn cục',
    'Channel Visibility Agents': 'Agent hiển thị Channel',
    'AVI Video File': 'File Video AVI',
    'Activate Extend Process Range': 'Mở rộng dải xử lý',
    'Define User Attributes...': 'Định nghĩa thuộc tính người dùng...',
    'Delete selected Permission Preset': 'Xóa Preset Permission đã chọn',
    'Delete program preferences': 'Xóa thiết lập chương trình',
    'Disable program preferences': 'Tắt thiết lập chương trình',
    'Choose Unique User Name': 'Chọn tên người dùng duy nhất',
    'Merge Project into Network Project': 'Gộp Project vào Project mạng',
    'Click the \'Assign\' Button while Holding Down Modifier Keys':
        'Nhấp nút \'Gán\' trong khi giữ các phím bổ trợ',
    'Assign Additional Key': 'Gán phím bổ sung',
    'Assign subsection to section': 'Gán phần con vào phần cha',

    # ======================================================================
    # preposition wrong
    # ======================================================================
    'Convert Tracks: Mono to Multi-Channel':
        'Chuyển đổi Track: Mono sang Multi-Channel',
    'Convert Tracks: Multi-Channel to Mono':
        'Chuyển đổi Track: Multi-Channel sang Mono',
    'Convert Z-Axis Pan Automation To 2-Layer':
        'Chuyển đổi Automation Z-Axis Pan sang 2-Layer',
    'Convert Z-Axis Pan Automation To 3-Layer':
        'Chuyển đổi Automation Z-Axis Pan sang 3-Layer',
    'Add Effect Track to Send %d...': 'Thêm Effect Track vào Send %d...',
    'Add Effect Track to Selected Tracks...':
        'Thêm Effect Track vào Track đã chọn...',
    'Add VCA Track to Selected Tracks...':
        'Thêm VCA Track vào Track đã chọn...',
    'Add Group Track to Selected Tracks...':
        'Thêm Group Track vào Track đã chọn...',
    'Effect Track to Selected Tracks...': 'Effect Track tới Track đã chọn...',
    'VCA Track to Selected Tracks...': 'VCA Track tới Track đã chọn...',

    # ======================================================================
    # broken - a Vietnamese word landed mid-English
    # ======================================================================
    'Bypass Insert on/off.\\nInsert on/off with [ALT + click].':
        'Bật/tắt Bypass Insert.\\nBật/tắt Insert bằng [ALT + nhấp].',
    'Bypass Modulator on/off.\\nModulator on/off with [ALT + click].':
        'Bật/tắt Bypass Modulator.\\nBật/tắt Modulator bằng [ALT + nhấp].',
    'Bypass Module on/off.\\nModule on/off with [ALT + click].':
        'Bật/tắt Bypass Module.\\nBật/tắt Module bằng [ALT + nhấp].',
    'Channel Strip Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Channel Strip.\\nĐặt lại bằng [CTRL + nhấp].',
    'Direct Routing Bypass on/off.\\nReset with [CTRL + click].':
        'Bật/tắt Bypass Direct Routing.\\nĐặt lại bằng [CTRL + nhấp].',
    'Are you sure you want to edit so many events?':
        'Bạn có chắc muốn sửa nhiều Event như vậy không?',
    'Blind Panel': 'Bảng mù',

    # ======================================================================
    # inconsistent wording
    # ======================================================================
    'Add Channel to Link Group "%s"': 'Thêm Channel vào Link Group "%s"',
    'Add VCA Channel to Link Group "%s"':
        'Thêm VCA Channel vào Link Group "%s"',
    'Create VCA Channel for Link Group "%s"':
        'Tạo VCA Channel cho Link Group "%s"',
    'Add Profile': 'Thêm Profile',
    'Channel Batch': 'Channel hàng loạt',
    'Channel Destinations': 'Nơi nhận của Channel',
    'Channel Rotation': 'Xoay vòng Channel',
    'Channel Selection': 'Lựa chọn Channel',
    'Cues  (Post-Fader)': 'Cue  (Post-Fader)',
    'Cues (Post-Fader)': 'Cue (Post-Fader)',
    'Cues (Pre-Fader)': 'Cue (Pre-Fader)',
    'Clear EQ Band': 'Xóa EQ Band',
    'Copy EQ Band': 'Sao chép EQ Band',
    'Attach Channel to Left Edge': 'Gắn Channel vào cạnh trái',
    'Attach Channel to Right Edge': 'Gắn Channel vào cạnh phải',
    'Add New Page': 'Thêm Page mới',
    'Add Panel': 'Thêm Panel',
    # "Command" is "Lệnh". This entry used to say 'Command': 'Command', on the
    # grounds that it is a Cubase feature name - but its own plural was already
    # "Lệnh", and its bracketed twin "Command[Key]" is "Lệnh" too. A bare
    # English label next to two translated ones is the "nửa chừng có một hệ
    # thống riêng" that AGENT.md section 3 forbids. Fixed here rather than in
    # the fix_*.py scripts because this module is applied last and would have
    # undone them.
    'Command': 'Lệnh',
    'Context Variable': 'Biến ngữ cảnh',
    'Network address invalid or ambiguous.':
        'Địa chỉ mạng không hợp lệ hoặc không xác định.',
    'Install Template': 'Cài đặt Template',
    'Edit History Preferences': 'Tùy chọn lịch sử chỉnh sửa',
    'Create new empty Track Version and assign common version ID':
        'Tạo Track Version rỗng mới và gán ID chung cho các version',
    'A setup information file is available for this script. Do you want to '
    'open this file?':
        'Có sẵn file thông tin thiết lập cho Script này. Bạn có muốn mở file '
        'này không?',
    '" already in Pool.\\nDo you want to create a new version or use the '
    'existing?':
        '" đã có trong Pool.\\nBạn có muốn tạo Version mới hay dùng Version '
        'hiện có?',
}
