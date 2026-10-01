#!/usr/bin/env python3
"""Fix the quantifier words (All / Every / Each / Only) left in English."""

CHUNK_B = {
    'Active Track Only': 'Chỉ Track đang hoạt động',
    'Add Every 2nd Step': 'Thêm mọi Step thứ hai',
    'Add Every 3rd Step': 'Thêm mọi Step thứ ba',
    'Add Every 4th Step': 'Thêm mọi Step thứ tư',
    'All Clips on Active Track': 'Tất cả Clip trên Track đang hoạt động',
    'All Key Commands': 'Tất cả phím tắt',
    'All Options': 'Tất cả tùy chọn',
    'All Parts on Active Track': 'Tất cả Part trên Track đang hoạt động',
    'All Track Modes to Global': 'Đặt tất cả chế độ Track thành toàn cục',
    'Are you sure you want to assign channel pan to all cue sends?':
        'Bạn có chắc muốn gán Pan của Channel cho tất cả Cue Send không?',
    'Are you sure you want to assign channel volume to all cue sends?':
        'Bạn có chắc muốn gán âm lượng của Channel cho tất cả Cue Send không?',
    'Attributes apply to individual notes, directions apply to all following notes':
        'Thuộc tính áp dụng cho từng nốt, chỉ dẫn áp dụng cho tất cả nốt phía sau',
    'Bypass Modulators of All Visible Channels': 'Bypass Modulator của mọi Channel đang hiện',
    'Collapse All': 'Thu gọn tất cả',
    'Connect Sends automatically for each newly created Channel':
        'Kết nối Send tự động cho mỗi Channel vừa tạo',
    'Could not import all resources!': 'Không thể Import tất cả tài nguyên!',
    'Disable all Talkbacks': 'Tắt tất cả Talkback',
    'Discard all changes to "%s"?': 'Hủy bỏ tất cả thay đổi đối với "%s"?',
    'Disconnect all Projects?': 'Ngắt kết nối tất cả Project?',
    'Expand All': 'Mở rộng tất cả',
    'Export All to One File': 'Export tất cả vào một file',
    'Hide: All Channel Types': 'Ẩn: mọi loại Channel',
    'Input Routing.\\nSet for all selected with [Shift + ALT + click].':
        'Input Routing.\\nĐặt cho tất cả mục đã chọn bằng [Shift + ALT + click].',
    'Instruments use Automation Read All and Write All':
        'Nhạc cụ dùng Automation Read All và Write All',
    'Legato Mode: Between Selected Notes Only': 'Chế độ Legato: chỉ giữa các nốt đã chọn',
    'Lists all tracks with hitpoints': 'Liệt kê mọi Track có Hitpoint',
    'Load All Mixer Settings': 'Tải toàn bộ cài đặt Mixer',
    'Load Chords Only': 'Chỉ tải hợp âm',
    'Load Players Only': 'Chỉ tải Player',
    'MIDI Retrospective Record: Insert from All MIDI Inputs':
        'Ghi MIDI hồi cứu: Chèn từ tất cả MIDI đầu vào',
    'Mute all Inputs': 'Mute tất cả đầu vào',
    'Output Routing.\\nSet for all selected with [Shift + ALT + click].':
        'Output Routing.\\nĐặt cho tất cả mục đã chọn bằng [Shift + ALT + click].',
    'Part/Clip Editing Mode: All Parts/Clips on Active Track':
        'Chế độ sửa Part/Clip: tất cả Part/Clip trên Track đang hoạt động',
    'Please close all shared Projects first': 'Vui lòng đóng tất cả Project đã chia sẻ trước',
    'Quantize to original groove positions only': 'Chỉ Quantize theo vị trí groove gốc',
    'Remove all Warp Tabs': 'Gỡ bỏ tất cả tab Warp',
    'Remove only': 'Chỉ gỡ bỏ',
    'Rendered files include all source settings.': 'File đã Render bao gồm mọi cài đặt nguồn.',
    'Restore All': 'Khôi phục tất cả',
    'Save All Mixer Settings': 'Lưu toàn bộ cài đặt Mixer',
    'Save Definition in Project Only': 'Chỉ lưu định nghĩa trong Project',
    'Select controller to set tensions for all chord pads':
        'Chọn Controller để đặt Tension cho tất cả Chord Pad',
    'Select controller to set voicings for all chord pads':
        'Chọn Controller để đặt Voicing cho tất cả Chord Pad',
    'Select controller to transpose all chord pads':
        'Chọn Controller để Transpose tất cả Chord Pad',
    'Selected Channels only': 'Chỉ các Channel đã chọn',
    'Send All Notes Off Message': 'Gửi thông điệp All Notes Off',
    'Set all Tracks to Musical Timebase': 'Đặt tất cả Track sang Timebase Musical',
    'Show All Send Automation': 'Hiện mọi Automation của Send',
    'Show All Smart Controls': 'Hiện mọi Smart Control',
    'Show All Tracks': 'Hiện tất cả Track',
    'Show All Volume Automation': 'Hiện mọi Automation âm lượng',
    'Show Beat Count Only': 'Chỉ hiện số đếm phách',
    'Show Error Messages Only': 'Chỉ hiện thông báo lỗi',
    'Show Log Messages Only': 'Chỉ hiện thông báo nhật ký',
    'Show Only Lanes with Steps': 'Chỉ hiện Lane có Step',
    'Show Only Selected Channels': 'Chỉ hiện Channel đã chọn',
    'Show Only Selected Folder': 'Chỉ hiện thư mục đã chọn',
    'Show VST Quick Controls for One Slot Only': 'Chỉ hiện VST Quick Control cho một Slot',
    'Show Velocity Lane Only': 'Chỉ hiện Velocity Lane',
    'Show all available Slots': 'Hiện tất cả Slot khả dụng',
    'Show all available Slots for Cue Sends': 'Hiện tất cả Slot khả dụng cho Cue Send',
    'Show all available Slots for Direct Routing': 'Hiện tất cả Slot khả dụng cho Direct Routing',
    'Show all available Slots for Inserts': 'Hiện tất cả Slot khả dụng cho Insert',
    'Show all available Slots for Modulators': 'Hiện tất cả Slot khả dụng cho Modulator',
    'Show all available Slots for Quick Controls': 'Hiện tất cả Slot khả dụng cho Quick Control',
    'Show all available Slots for Sends': 'Hiện tất cả Slot khả dụng cho Send',
    'Show only Sound Slots with Remote Trigger assignments':
        'Chỉ hiện Sound Slot có phép gán Remote Trigger',
    'Show/Hide all Unused Controllers': 'Hiện/Ẩn mọi Controller không dùng',
    'Show/Hide all VST Quick Controls': 'Hiện/Ẩn mọi VST Quick Control',
    'Show/Hide all unused Controllers': 'Hiện/Ẩn mọi Controller không dùng',
    'Show: All Channel Types': 'Hiện: mọi loại Channel',
    'Solo all Inputs': 'Solo tất cả đầu vào',
    'Suspend All Channel Linking': 'Tạm dừng liên kết toàn bộ Channel',
    'Suspend Reading All': 'Tạm dừng đọc tất cả',
    'Suspend Reading/Writing All': 'Tạm dừng đọc/ghi tất cả',
    'Suspend Writing All': 'Tạm dừng ghi tất cả',
    'Temporary Link Mode - Sync all touched parameters of selected channels':
        'Chế độ liên kết tạm thời - Đồng bộ mọi tham số đã chạm của các Channel đã chọn',
    'Toggle Read Enable All Tracks': 'Bật/tắt Read Enable cho tất cả Track',
    'Toggle Write Enable All Tracks': 'Bật/tắt Write Enable cho tất cả Track',
    'Unmute all Inputs': 'Bỏ Mute tất cả đầu vào',
    'Unsolo all Inputs': 'Bỏ Solo tất cả đầu vào',
    'Windows: Close All Plug-Ins for Selected Track/Channel':
        'Cửa sổ: Đóng tất cả Plug-in của Track/Channel đã chọn',
    'Yes to All': 'Có cho tất cả',
    'Zoom Tool Standard Mode: Horizontal Zooming Only':
        'Chế độ tiêu chuẩn của công cụ Zoom: chỉ Zoom ngang',
}
