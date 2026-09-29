#!/usr/bin/env python3
"""Last notation batch: Staff, Barline, Beam, Voice, Time Signature, System.

These desk terms had Vietnamese agreed in glossary_notation.py, but a second
set of keys was missed. Bringing them onto the same wording is what makes the
Score Editor read as one language instead of three.
"""

WORDING = {
    # --- Staff --------------------------------------------------------------
    'Notation Staff to Tablature': 'Chuyển khuông nhạc ký âm sang Tablature',
    'Staff Group to Staff': 'Chuyển nhóm khuông nhạc sang khuông nhạc',
    'Staff Group to Staff Group': 'Chuyển nhóm khuông nhạc sang nhóm khuông nhạc',
    'Staff to Staff': 'Chuyển khuông nhạc sang khuông nhạc',
    'Staff to Staff Group': 'Chuyển khuông nhạc sang nhóm khuông nhạc',
    'Timecode Staff to Staff': 'Chuyển khuông nhạc Timecode sang khuông nhạc',
    'Staff Settings...': 'Cài đặt khuông nhạc...',

    # --- Barline ------------------------------------------------------------
    'Centered on Barline': 'Căn giữa trên vạch nhịp',
    'Left-Aligned on Barline': 'Căn trái trên vạch nhịp',

    # --- Beam ---------------------------------------------------------------
    'Rests in Beam Groups': 'Dấu lặng trong nhóm đuôi nốt',
    'Secondary Beam Groups': 'Nhóm đuôi nốt phụ',
    'Set Partial Beam Direction': 'Đặt hướng đuôi nốt phụ',
    'Set Partial Beam Direction Left': 'Đặt hướng đuôi nốt phụ sang trái',
    'Set Partial Beam Direction Right': 'Đặt hướng đuôi nốt phụ sang phải',
    'Split Beam': 'Tách đuôi nốt',
    'Split Secondary Beam': 'Tách đuôi nốt phụ',
    'Split Secondary Beams': 'Tách các đuôi nốt phụ',
    'Reset Beaming': 'Đặt lại nối đuôi nốt',
    'Beaming 1/8 Notes (Quavers) Together in 1/4 Note (Crotchet) '
    'Denominator Time Signatures':
        'Nối đuôi nốt móc đơn 1/8 trong số chỉ nhịp mẫu số Note cường 1/4',

    # --- Voice --------------------------------------------------------------
    'Activate Voice': 'Bật bè',
    'Add Voice': 'Thêm bè',
    'Assign Voices to Notes': 'Gán bè cho các nốt',
    'Chord Track - Assign Voices to Notes': 'Chord Track - Gán bè cho các nốt',
    'Bass to Lowest Voice': 'Bass vào bè thấp nhất',
    'Map To Voice': 'Gán vào bè',
    'Remove Highest Voice': 'Gỡ bỏ bè cao nhất',
    'Remove Voice': 'Gỡ bỏ bè',
    'Voice': 'Bè',
    'Voice Colors': 'Màu các bè',

    # --- Time Signature -----------------------------------------------------
    'Add Displayed Time Signature': 'Thêm số chỉ nhịp hiển thị',
    'Add Time Signature': 'Thêm số chỉ nhịp',
    'Choose Time Signature for Count-In :':
        'Chọn số chỉ nhịp cho Count-In :',
    'Custom Time Signature': 'Số chỉ nhịp tùy chỉnh',
    'Defined Time Signature of Audio File':
        'Số chỉ nhịp được định nghĩa của file Audio',
    'Enter Time Signature': 'Nhập số chỉ nhịp',
    'Insert Time Signature Event': 'Chèn Event số chỉ nhịp',
    'Insert Time Signature Event...': 'Chèn Event số chỉ nhịp...',
    'Time Signature': 'Số chỉ nhịp',
    'Use Custom Time Signature': 'Dùng số chỉ nhịp tùy chỉnh',
    'Duplicate Notes to Multiple Voices': 'Nhân bản các nốt sang nhiều bè',
    '1/16 Notes (Semiquavers) in 1/8 Note (Quaver) Denominator Time '
    'Signatures':
        'Nốt 1/16 trong số chỉ nhịp mẫu số nốt móc đơn 1/8',
    '1/32 Notes (Demisemiquavers) in 1/16 Note (Semiquaver) Denominator Time '
    'Signatures':
        'Nốt 1/32 trong số chỉ nhịp mẫu số nốt móc kép 1/16',
    '1/8 Notes (Quavers) in 1/4 Note (Crotchet) Denominator Time Signatures':
        'Nốt móc đơn 1/8 trong số chỉ nhịp mẫu số nốt cường 1/4',
    'Insert Time Signature Event': 'Chèn Time Signature Event',
    'Insert Time Signature Event...': 'Chèn Time Signature Event...',
    'Quarter Note (Crotchet) Denominator Time Signatures With Half-Bars':
        'Số chỉ nhịp mẫu số nốt cường 1/4 kèm nửa Bar',
    'Time Signatures With Half-Bars': 'Số chỉ nhịp kèm nửa Bar',
    'Respect Maximum Duration for Rhythmic Slashes in Compound Time '
    'Signatures':
        'Tôn trọng trường độ tối đa cho gạch nhịp trong số chỉ nhịp phức',
    'Respect Maximum Duration for Rhythmic Slashes in Irregular Time '
    'Signatures':
        'Tôn trọng trường độ tối đa cho gạch nhịp trong số chỉ nhịp bất thường',

    # --- System as a line of music -----------------------------------------
    'All Systems': 'Tất cả các dòng nhạc',
}
