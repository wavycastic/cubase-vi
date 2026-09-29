#!/usr/bin/env python3
"""The same concept rendered two ways, aligned to one.

AGENT.md 2 lists Tempo as a term to keep in English, so the four "nhịp độ"
spellings are the defect and become "Tempo". Cycle was already 70:28 in favour
of the English form, so the 28 "chu kỳ" become "Cycle" too.

Terms AGENT.md does not mention are left on the Vietnamese side, because the
Vietnamese reads better and is already the majority:
  con trỏ / Cursor        "con trỏ" 58 : 43
  bè / Voice             "bè"      35 :  4
  số chỉ nhịp / Time Signature   38 :  2
  phát lại / Playback    17 : 10
  hợp âm / Chord        111 : 120  (both natural; "hợp âm" is the everyday word)
"""

WORDING = {
    # --- Tempo: AGENT.md 2 mandates the English -----------------------------
    'Add Tempo': 'Thêm Tempo',
    'Add Displayed Tempo': 'Thêm Tempo hiển thị',
    'Tempo': 'Tempo',
    'Adjust Current Tempo': 'Điều chỉnh Tempo hiện tại',
    'Set Tempo': 'Đặt Tempo',

    # --- Cycle: English already dominant, align the minority ---------------
    'Cycle Follows Range Selection': 'Cycle bám theo vùng chọn',
    'Creates new audio events for any recording or cycle.':
        'Tạo Audio Event mới cho mọi lần ghi hoặc Cycle.',
    'Removes any existing audio in the record range, but creates new audio '
    'events for each cycle in cycle record.':
        'Xóa mọi âm thanh có sẵn trong vùng ghi, nhưng tạo Audio Event mới cho '
        'mỗi Cycle khi ghi theo Cycle.',
    'Insert Input from Selected Track as Cycle Recording':
        'Chèn Input từ Track đã chọn dưới dạng bản ghi theo Cycle',
    'Insert as Cycle Recording': 'Chèn dưới dạng bản ghi theo Cycle',
    'Linear & Cycled MIDI Recording': 'Ghi MIDI tuyến tính & theo Cycle',
    'Defines what happens AFTER a linear or cycled recording...':
        'Xác định điều gì xảy ra SAU KHI ghi tuyến tính hoặc ghi theo Cycle...',
    'Defines what happens DURING cycle recording...':
        'Xác định điều gì xảy ra TRONG KHI ghi theo Cycle...',
    'New parts are created in each cycle, but only the last one is played back '
    '(others are muted).':
        'Các Part mới được tạo trong mỗi Cycle, nhưng chỉ Part cuối cùng được '
        'phát lại (những Part khác bị Mute).',
    'New parts are created in each cycle and all of them are played back.':
        'Các Part mới được tạo trong mỗi Cycle và tất cả đều được phát lại.',
    'Cycle History + Replace': 'Lịch sử Cycle + Thay thế',
    'Cycle History + Replace[RM]': 'Lịch sử Cycle + Thay thế[RM]',
    'Exactly Matching Cycle': 'Khớp chính xác Cycle',
    'Only the last cycle is kept.': 'Chỉ giữ lại Cycle cuối cùng.',
    'Preview Cycle': 'Xem trước Cycle',
    'The first note played in a new cycle deletes all later notes.':
        'Nốt đầu tiên được phát trong một Cycle mới sẽ xóa tất cả nốt sau đó.',
    'When selected, sent MIDI Clock will follow cycled project position':
        'Khi được chọn, MIDI Clock gửi đi sẽ bám theo vị trí Project theo Cycle',
    'When selected, sent MIDI Timecode will follow cycled project time':
        'Khi được chọn, MIDI Timecode gửi đi sẽ bám theo thời gian Project '
        'theo Cycle',

    # --- Position Marker: the odd one out was Vietnamese --------------------
    'Add and Edit Position Marker on Active Track':
        'Thêm và sửa Position Marker trên Track đang hoạt động',
    'Add and Edit Position Marker on Selected Track':
        'Thêm và sửa Position Marker trên Track đã chọn',
    'Reassign Position Marker IDs': 'Gán lại ID của Position Marker',
}
