"""Fixtures for the two halves of a detector: must fire, must not fire.

A regex filter that reports nothing looks exactly like a clean map. That is
how nine tools in this project sat on the class `[Ā-ỿ]` for seventeen rounds
and reported zero findings every time - not because the translation was clean
but because `re.compile(r'[Ā-ỿ]')` starts at U+0100, and Vietnamese sits at
U+00C0..U+00FF, entirely below it. Every value looked untranslated.

AGENT.md §7: "bộ dò báo 0" và "bộ dò hỏng" trông giống nhau. So a detector is
not trusted until it has been shown both a string it must catch and a string
it must leave alone.

Each case is (term, value, should_fire). The "should not fire" half is the
one that matters in practice: terms_do_not_translate.json gates all 10,737
values, so a single over-broad pattern blocks the whole pipeline.
"""
import os

# --- terms_do_not_translate.json: ways these terms were actually mistranslated
TERMS_BAD = [
    ('Automation', 'Áp dụng tự động hóa cho Track'),
    ('Track', 'Tạo rãnh mới'),
    ('Clip', 'Xóa đoạn cắt này'),
    ('Bounce', 'Nảy Event ra file'),
    ('Freeze', 'Đóng băng Track'),
    ('Quantize', 'Lượng tử hóa theo lưới'),
    ('Tempo', 'Đặt nhịp độ của Project'),
    ('Tempo', 'Chỉnh nhịp độ nhanh hơn'),
    ('Warp', 'Dùng bẻ cong để giữ cao độ'),
    ('Render', 'Kết xuất toàn bộ Project'),
    ('Plug-in', 'Quét lại các phần cắm'),
    ('Metronome', 'Bật máy đếm nhịp'),
    ('Transport', 'Bộ vận chuyển đang chạy'),
    ('Marker', 'Đặt dấu đánh dấu tại đầu Bar'),
    ('Locator', 'Định vị vị trí đã đảo chiều'),
    ('Mixer', 'Bộ trộn âm thanh của bạn'),
    ('Fader', 'Cần trượt của Channel 1'),
    ('Crossfade', 'Tạo chuyển tiếp mượt giữa hai đoạn'),

    # --- round 84: recovered from AGENT.md.bak, the 2,442-line original. The
    # 199-line compression kept the rules and dropped the evidence, so these
    # mistranslations had been fixed once and were unguarded ever since.
    ('Duration', 'Thời gian trường độ của Note'),
    ('Pick-up', 'Đặt điểm lấy đà'),
    ('Scaling', 'Thay đổi thu phóng giao diện'),
    ('Mouse Wheel', 'Dùng cuộn chuột để Zoom'),
    ('Notehead', 'Chọn đầu nối khác'),
    ('Retrospective Record', 'Ghi hồi tố'),
    ('Material', 'Thư viện tư liệu'),
    ('Word Clock', 'Đồng hồ từ đầu ra'),
    ('extension (file)', 'Phần mở rộng File không hợp lệ'),
    ('file dialog', 'Mở hộp thoại file'),
    ('Snap Point', 'Chọn điểm bắt dính'),
    ('Dynamic Velocity', 'Động lực Velocity'),
    ('Pitch Shift', 'Dịch cao độ của Audio'),
    ('Mute', 'Tắt tiếng Channel'),
    ('Dissolve Part', 'Hòa tan Part'),
    ('Assistant', 'Trợ lý Scale'),
    ('Note On', 'Bật Note'),
    ('On Velocity', 'Bật Velocity'),
    ('Off Velocity', 'Tắt Velocity'),
    ('Erase Tool', 'Xóa công cụ'),
    ('Surface Editor', 'Trình sửa bề mặt'),
    ('Quantize hiển thị', 'Hiển thị Quantize'),

    # --- round 85: one string left the family of 20 or more. The pattern is
    # only added because the bad rendering was the ONLY rendering of that
    # phrase in 10,737 keys - see terms_do_not_translate.json, _comment_outlier
    ('Ambisonics', 'Định dạng file Ambisonic'),
    ('Q-Factor', 'Hệ số Q'),
    ('Direct Monitoring', 'Monitoring trực tiếp'),
    ('Latch Buffer', 'Bộ đệm Latch'),
    ('Summing', 'Direct Routing (Cộng dồn)'),
    ('Chunk', 'Khối dữ liệu Broadcast Wave'),
    ('Post', 'Đang chạy Script xử lý hậu kỳ'),
    ('Meter', 'Đo hiệu năng Audio'),
    ('Monitor', 'Theo dõi hiệu năng Audio'),
    ('Chain', 'Kéo đổi thứ tự Modulator trong chuỗi tín hiệu'),
    ('Catch Range', 'Quantize trong dải bắt'),
    ('Subsection', 'Gán khu vực con vào khu vực cha'),
    ('Serial', 'Cổng nối tiếp 9-Pin'),
    ('Trim', 'Cắt Note Expression theo độ dài nốt'),
    ('Folding', 'Gập Track'),
]

# --- correct values that a sloppier pattern would flag
TERMS_GOOD = [
    'Đặt Tempo của Project',
    'Xóa Track đã chọn',
    'Mở MixConsole',
    'Đặt độ trễ Channel',
    'Bạn có thể đặt Fader cao hơn',
    'Nghỉ một chút rồi chơi tiếp',      # "nghi" + "mot": Rest must not fire
    'Đầu nốt dấu lặng',                 # "lặng" is inside "dấu lặng"
    'Lưới bị thiếu',                    # "luoi" + "bi": Grid must not fire
    'Ẩn khóa nhạc',                     # "khoa" + "am", not "khoa nhac"
    'Số chỉ nhịp 3/4',                  # Time Signature is correct Vietnamese
    'Ảnh Video dài hơn Clip',
    'Nốt trùng ở hai bè',
    'Preset âm thanh đã lưu',
    # round 85 patterns must stay narrow. Each of these was the reason a
    # similar-looking pattern was NOT added: the Vietnamese word is correct
    # somewhere else in the map, so a pattern on the bare word would block it.
    'Mở Ambisonics Decoder',          # must not read as "Ambisonic" + typo
    'Thiết lập thẻ',                  # "thẻ" = Tab, correct
    'Áp dụng hợp âm vào vùng chọn',    # "vùng chọn" = selection, correct
    'Xóa tất cả bộ đệm',              # "bộ đệm" without Latch, correct
    'Phần đệm',                       # padding, correct
    'Khối',                           # Blocks, correct
    'Track Folding: Bật Group Channel',
    'Hiện Direct Monitoring',
    'Bật/Tắt Catch Range',
    'Gán Section cho Subsection',
    'Cổng Parallel 9-Pin',            # Serial's opposite; pattern is exact
    'Trim the beginning',             # Trim as a verb, correct
    'Chunk nhớ',                      # Cache noun, not Broadcast Wave Chunk
    'Q-Factor của EQ Band 1',
    # 'bỏ qua' and 'lặp' are correct for Ignore/Skip/Repeat - see CONDITIONAL
    'Bỏ qua các hàng đầu tiên',
    'Lặp lại Loop',
    'Region lặp lại Bar',
]

# --- round 84: rules that are wrong only for some sources. 13 Bypass strings
# were fixed to stop saying "Bỏ qua" (round 72), but 23 Ignore/Skip/Discard
# strings legitimately say "Bỏ qua", and 18 Repeat strings say "lặp lại".
# A pattern with no source test would block every one of them - AGENT.md §7,
# a detector that cries wolf stops being read.
#
# (source, value, term that must fire)
CONDITIONAL = [
    ('Bypass Insert', 'Bỏ qua Insert', 'Bypass'),
    ('Bypass EQ of all Channels', 'Bỏ qua EQ của tất cả Channel', 'Bypass'),
    # same word, different source term: must NOT fire
    ('Ignore First Rows', 'Bỏ qua các hàng đầu tiên', None),
    ('Skip', 'Bỏ qua', None),
    ('Discard', 'Bỏ qua', None),
    ('Cycle Marker', 'Marker Lặp', 'Cycle'),
    ('Cycle Activation via Marker', 'Bật Cycle bằng Marker', None),  # keeps Cycle
    ('Repeat', 'Lặp lại', None),
    ('Bar Repeat Region', 'Region lặp lại Bar', None),
    ('Repeat Forever', 'Lặp vô hạn', None),
]

# --- every placeholder shape that actually occurs in all_strings.tsv, with the
# count the grep found. A placeholder pattern that misses one of these makes
# the "placeholders match" test pass on a string whose %s was dropped.
PLACEHOLDERS_SEEN = {
    '%s': 606, '%d': 288, '%i': 38, '%.3f': 12, '%.1f': 10,
    '%.2f': 8, '%02d': 6, '%.0f': 4, '%1.0f': 2, '%l': 2,
}

# --- find_english_frame.py: 4+ English words copied verbatim from the source
# is a frame, not a translation. The threshold is 4 rather than 1 because at 1
# it produced 72 items and the 24 that survived at 5 were all correct
# (feature names in quotes, menu paths, format strings).
FRAMES_BAD = [
    'Notes cho Which Accidentals Have Already Been Stated Within the Bar',
    'Primary type is used cho the main chord symbol',
]


def load():
    """Return [(term, compiled_regex)] - rules that hold in every context.

    Uses tools/termspec.py, so the tests and check_style.py read the same
    spec. Conditional rules (those with a `src` partner) are excluded here:
    they cannot be tested without a source string. test_translation.py tests
    those separately against real (src, val) pairs.
    """
    import sys
    tools = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import termspec
    return termspec.rules_for_tests()
