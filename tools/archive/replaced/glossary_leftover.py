#!/usr/bin/env python3
"""The 26 values that are still English prose.

The automated pass also moved words around while substituting, producing
"Preset Not enough space for all controllers in" and "Trang Not on First
Page" - a stray Vietnamese word in front of a still-English sentence, which
reads worse than the untouched English. Rewritten here.
"""

WORDING = {
    '"%s" not possible for frozen tracks':
        'Không thể "%s" với các Track đã Freeze',
    '"%s" not possible for tracks that are recording':
        'Không thể "%s" với các Track đang ghi',
    '"%s" not possible for write protected tracks':
        'Không thể "%s" với các Track đang bị bảo vệ ghi',
    '"Pitch Visibility: Select Next Option" not possible because there are no '
    'note events in the editor':
        'Không thể "Pitch Visibility: Select Next Option" vì trong Editor không '
        'có Note Event nào',
    'Colorize Selected Events...': 'Tô màu Event đã chọn...',
    'Do not': 'Không',
    'Export to MP3 is not supported for Surround channels':
        'Không hỗ trợ Export sang MP3 cho Channel Surround',
    'Hide Folders That Are Not Scanned': 'Ẩn các thư mục chưa được quét',
    "Measurements below this value are not included in the 'Average "
    "Intelligibility' calculation":
        "Các phép đo dưới giá trị này không được tính vào phép tính "
        "'Average Intelligibility'",
    'MIDI Learn not available for this control':
        'MIDI Learn không khả dụng cho điều khiển này',
    'Modulators are not displayed in inactive projects':
        'Modulator không được hiện trong Project không hoạt động',
    'Not enough space for additional controller lane':
        'Không đủ chỗ cho thêm một Controller Lane',
    'Not enough space for all controllers in preset':
        'Không đủ chỗ cho tất cả Controller trong Preset',
    'Not enough space for all used controllers':
        'Không đủ chỗ cho tất cả Controller đang dùng',
    'Not enough space for velocity lane':
        'Không đủ chỗ cho Velocity Lane',
    'Not on First Page': 'Không ở trang đầu tiên',
    'Pitch Visibility cannot be activated because there are no note events in '
    'the editor':
        'Không thể bật Pitch Visibility vì trong Editor không có Note Event nào',
    'Retrospective Cycle Recording is not supported in MIDI Editors':
        'Không hỗ trợ Ghi hồi cứu theo chu kỳ trong MIDI Editor',
    'Scale Modifications in Follow Chord Track Mode impossible':
        'Không thể sửa Scale ở chế độ Follow Chord Track',
    'Scales cannot be edited when the Automatic Scales checkbox is activated':
        'Không thể sửa Scale khi ô Automatic Scales đang bật',
    'The created AAF file may not be usable for other hosts because:':
        'File AAF được tạo có thể không dùng được với các host khác vì:',
    'The file "%s" could not be opened': 'Không thể mở file "%s"',
    'The following plug-in is not responding:': 'Plug-in sau không phản hồi:',
    'The profile was not found': 'Không tìm thấy Profile',
    'The project could not be saved, because:\\n':
        'Không thể lưu Project, vì:\\n',
    'The selected path does not exist': 'Đường dẫn đã chọn không tồn tại',

    # --- bullet items: no terminal punctuation, so the earlier filter missed
    #     them, but they are still English sentences
    '- Check the Pool and search for missing audio files':
        '- Kiểm tra Pool và tìm các file Audio bị thiếu',
    '- Maximum project duration for sample-precise object positions exceeded':
        '- Đã vượt quá trường độ tối đa của Project cho vị trí đối tượng '
        'chính xác tới mức sample',
    '- No tracks are selected for export':
        '- Không có Track nào được chọn để Export',
}
