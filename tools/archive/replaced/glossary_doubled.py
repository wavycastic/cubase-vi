#!/usr/bin/env python3
"""The doubled "vào", and the same defect with other verbs.

"to" was substituted for "vào" even where the English sentence already had a
verb, leaving "Go vào Input" and "Next Chain Step\\nUse [ALT]-Click vào jump
vào last chain step". The English order was kept as well: "Go vào Channel
Next Edited" instead of "Tới Channel sửa kế tiếp".

"Thêm ... vào ..." and "Chèn ... vào ..." are correct Vietnamese and are not
touched. Keys are copied verbatim from keys/all_strings.tsv.
"""

WORDING = {
    # --- Go to: "Tới" already carries the direction, "vào" was redundant ----
    'Go to Input': 'Tới đầu vào',
    'Go to Output': 'Tới đầu ra',
    'Go to Mapping Assistant': 'Tới Trợ lý Mapping',
    'Go to MIDI Controller Surface': 'Tới MIDI Controller Surface',
    'Go to Next Fade': 'Tới Fade kế tiếp',
    'Go to Previous Fade': 'Tới Fade trước đó',
    'Go to Next Edited Channel': 'Tới Channel sửa kế tiếp',
    'Go to Last Edited Channel': 'Tới Channel sửa lần cuối',
    'Go to Next MixConsole Channel': 'Tới Channel MixConsole kế tiếp',
    'Go to Previous MixConsole Channel': 'Tới Channel MixConsole trước đó',
    'Go to Next Marker/Project End': 'Tới Marker kế tiếp/Cuối Project',

    # --- Map to -------------------------------------------------------------
    'Map to Chord Track': 'Gán vào Chord Track',
    'Chord Track - Map to Chord Track': 'Chord Track - Gán vào Chord Track',
    'The live input is mapped to the chord track based on the selected mode':
        'Đầu vào trực tiếp được gán vào Chord Track dựa trên chế độ đã chọn',
    'The notes are mapped to the chord track based on the selected mode':
        'Các nốt được gán vào Chord Track dựa trên chế độ đã chọn',

    # --- Drag / Scroll ------------------------------------------------------
    'Drag to change order of items':
        'Kéo để đổi thứ tự các mục',
    'Drag to change order of modulators in signal chain':
        'Kéo để đổi thứ tự các Modulator trong signal chain',
    'Drag to change order of modules in signal path':
        'Kéo để đổi thứ tự các Module trong signal path',
    'Scroll to selected Track': 'Cuộn tới Track đã chọn',

    # --- Set / Move / Locators ---------------------------------------------
    'Set Audio Event to Selection': 'Đặt Audio Event theo vùng chọn',
    'Set Region to Selection': 'Đặt Region theo vùng chọn',
    'Set Event Color to Track': 'Đặt màu Event theo Track',
    'Locators to Selection': 'Đưa Locator về vùng chọn',
    'Move Event/Range to Selected Track':
        'Di chuyển Event/vùng tới Track đã chọn',
    'Move Configuration to Position': 'Di chuyển Configuration tới vị trí',
    'Move Markers to Track': 'Di chuyển Marker tới Track',
    'Move Selection to new Track Version':
        'Di chuyển vùng chọn sang Track Version mới',
    'Event/Range to Selected Track': 'Event/vùng tới Track đã chọn',
    'Extract to Track': 'Trích xuất vào Track',
    'Effect Track to Selected Tracks...': 'Track Effect tới Track đã chọn...',
    'VCA Track to Selected Tracks...': 'Track VCA tới Track đã chọn...',
    'Connected to MIDI Track': 'Đã kết nối tới MIDI Track',
    'Synchronize Plug-in Program Selection to Track Selection':
        'Đồng bộ lựa chọn Program của Plug-in với lựa chọn Track',

    # --- chain step jump ----------------------------------------------------
    'Next Chain Step\\nUse [ALT]-Click to jump to last chain step':
        'Chain Step kế tiếp\\nDùng [ALT] + Click để nhảy tới chain step cuối cùng',
    'Previous Chain Step\\nUse [ALT]-Click to jump to first chain step':
        'Chain Step trước đó\\nDùng [ALT] + Click để nhảy tới chain step đầu tiên',

    # --- folding / convert --------------------------------------------------
    'Folding: Move Tracks To New Folder with Group Channel':
        'Gộp Track: Chuyển Track vào thư mục mới kèm Group Channel',
    'Convert audio files to new rate?':
        'Chuyển đổi file Audio sang rate mới?',
}
