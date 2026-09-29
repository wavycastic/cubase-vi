#!/usr/bin/env python3
"""Canonical score-notation glossary (Cubase 15 Score Editor).

AGENT.md 2 pins Bar / Beat / Note / Chord / Tempo as terms that stay English,
so a measure is "Bar" everywhere, never "ô nhịp" or "Cột nhịp".

The desk vocabulary Cubase uses in the Score Editor (System, Staff, Clef, Rest,
Beam, Stem, Barline) has solid Vietnamese equivalents, so Vietnamese is the
agreed rendering and the English leftovers are the defect.

"System" is genuinely ambiguous in Cubase: a line of music in the Score Editor,
the operating system everywhere else. Every rule is therefore per-string, never
a blind find/replace. Keys here are copied verbatim from keys/all_strings.tsv.
"""

WORDING = {
    # --- System as a line of music -----------------------------------------
    'Above System': 'Phía trên dòng nhạc',
    'Below System': 'Phía dưới dòng nhạc',
    'After First System': 'Sau dòng nhạc đầu tiên',
    'Start of System': 'Đầu dòng nhạc',
    '... with Systemic Barline if at Start of System':
        '... với vạch nhịp hệ thống nếu ở đầu dòng nhạc',
    'Above Top Staff of System':
        'Phía trên khuông nhạc trên cùng của dòng nhạc',
    'Above or Below Start of System':
        'Phía trên hoặc phía dưới đầu dòng nhạc',
    'Align Bar Numbers Across Width of System':
        'Căn chỉnh số Bar theo chiều rộng của dòng nhạc',
    'Fixed Number of Systems per Page':
        'Số dòng nhạc cố định trên mỗi trang',
    'System Dividers': 'Đường phân chia dòng nhạc',
    'Show System Dividers:': 'Hiện đường phân chia dòng nhạc:',
    'Staff Labels on First System': 'Nhãn khuông nhạc trên dòng nhạc đầu tiên',
    'Staff Labels on Subsequent System': 'Nhãn khuông nhạc trên dòng nhạc tiếp theo',
    'Inter-System Gap': 'Khoảng cách giữa các dòng nhạc',
    'Inter-System Gap In Fill View:': 'Khoảng cách giữa các dòng nhạc trong Fill View:',
    'Minimum Inter-System Gap with Content':
        'Khoảng cách tối thiểu giữa các dòng nhạc với nội dung',
    'Staves and Systems': 'Khuông nhạc và dòng nhạc',
    'Automatically Resolve Collisions Between Adjacent Staves and Systems':
        'Tự động giải quyết va chạm giữa các khuông nhạc và dòng nhạc lân cận',
    'Text or Symbol Appearance at Start of Subsequent Systems':
        'Hiển thị văn bản hoặc ký hiệu ở đầu các dòng nhạc tiếp theo',
    'Key Signatures at Start of System Following First System':
        'Hóa biểu ở đầu các dòng nhạc sau dòng nhạc đầu tiên',
    'Clefs at Start of Systems Following First System':
        'Khóa nhạc ở đầu các dòng nhạc sau dòng nhạc đầu tiên',
    'Cautionary Key Signature at End of System':
        'Hóa biểu nhắc lại tại cuối dòng nhạc',
    'Cautionary Time Signature at End of System':
        'Số chỉ nhịp nhắc lại tại cuối dòng nhạc',
    'Show Timecode at Start of First System':
        'Hiện Timecode ở đầu dòng nhạc đầu tiên',
    'Offset at Start of System': 'Offset tại đầu dòng nhạc',
    'Chord symbols appear either above the staves belonging to specific '
    'instruments as defined in Instrument Settings, or above the top staff in '
    'the system.':
        'Ký hiệu hợp âm hiện hoặc trên các khuông nhạc thuộc nhạc cụ cụ thể '
        'như định nghĩa trong cài đặt Instrument, hoặc trên khuông nhạc trên '
        'cùng của dòng nhạc.',

    # --- Staff --------------------------------------------------------------
    'Staff': 'Khuông nhạc',
    'Staff Labels': 'Nhãn khuông nhạc',
    'Staff Labels Show Track Name Instead of Instrument Name by Default':
        'Nhãn khuông nhạc hiện tên Track thay vì tên nhạc cụ theo mặc định',
    'Hide Empty Staves': 'Ẩn khuông nhạc trống',
    'Minimum Distance from Staff': 'Khoảng cách tối thiểu từ khuông nhạc',
    'Minimum Inter-Staff Gap with Content':
        'Khoảng cách tối thiểu giữa các khuông nhạc với nội dung',
    'Show Rehearsal Marks Below Bottom Staff':
        'Hiện dấu tập dượt bên dưới khuông nhạc dưới cùng',
    'Show in Abbreviated Staff Labels':
        'Hiện dưới dạng nhãn khuông nhạc viết tắt',
    'Show in Full Staff Labels': 'Hiện dưới dạng nhãn khuông nhạc đầy đủ',
    'Single-line Instruments': 'Nhạc cụ 1 dòng kẻ',

    # --- Clef ---------------------------------------------------------------
    'Clefs with Octave Indicators': 'Khóa nhạc kèm chỉ báo octave',
    'Hide Clefs': 'Ẩn khóa nhạc',
    'Show Clefs': 'Hiện khóa nhạc',

    # --- Rest ---------------------------------------------------------------
    'Show Bar Rests in Empty Bars': 'Hiện dấu lặng Bar trong các Bar trống',
    'Multi-Bar Rests': 'Dấu lặng nhiều ô nhịp',
    'Multi-Bar Rests and Bar Repeats': 'Dấu lặng nhiều ô nhịp và lặp lại Bar',

    # --- Beam / stem --------------------------------------------------------
    'Beam Together': 'Nối chung đuôi nốt',
    'Approach for Secondary Beam Groups': 'Cách áp dụng cho nhóm đuôi nốt phụ',
    'Slashes with Stems': 'Gạch chéo có thân nốt',
    'Use Stemlets': 'Dùng thân nốt nhỏ',

    # --- Bar as a musical term (AGENT.md 2) --------------------------------
    'Define Bars': 'Định nghĩa Bar',
    'Delete Bars': 'Xóa Bar',
    'Insert Bars': 'Chèn Bar',
    'Process Bars': 'Xử lý Bar',
    'Process Bars Dialog...': 'Hộp thoại Xử lý Bar...',
    'Replace Bars': 'Thay thế Bar',
    'Inside Bar Range': 'Vùng trong Bar',
    'Outside Bar Range': 'Vùng ngoài Bar',
    'Fixed Number of Bars per System': 'Số Bar cố định trên mỗi dòng nhạc',
    'Number of Bars defined in Audio File':
        'Số Bar được định nghĩa trong file Audio',
    'Number of Bars in Count-In': 'Số Bar trong phần đếm nhịp',
    'Beams and Rests': 'Đuôi nốt và dấu lặng',
    'Rests and Secondary Beam Groups': 'Dấu lặng và nhóm đuôi nốt phụ',
}
