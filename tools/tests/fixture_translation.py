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
    """Return [(term, compiled_regex)] for the forbidden-translation filter."""
    import json
    import re
    # tests/ -> tools/ -> repo root
    root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    spec = json.load(
        open(os.path.join(root, 'terms_do_not_translate.json'),
             encoding='utf-8'))
    out = []
    for term, pats in spec['forbidden'].items():
        if term.startswith('_'):
            continue
        for p in pats:
            out.append((term, re.compile(p, re.I)))
    return out
