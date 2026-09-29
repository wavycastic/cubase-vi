#!/usr/bin/env python3
"""Repair the 34 values that contain U+FFFD replacement characters.

Each was corrupted when text was pasted through a console that mangled a
multi-byte Vietnamese character. The intent is recovered from context.
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

MOJIBAKE = re.compile('\ufffd')

REPAIRS = {
    'Agents: Undo Visibility Change': 'Agent: Hoàn tác thay đổi hiển thị',
    'Are you sure you want to remove this modulator?':
        'Bạn có chắc muốn gỡ bỏ Modulator này không?',
    'AudioWarp Quantize On/Off': 'Bật/Tắt AudioWarp Quantize',
    'Break Beams at Half-Bar Beat Boundaries':
        'Ngắt đuôi nốt tại ranh giới phách của nửa ô nhịp',
    'Cannot replace audio in this video file.\\nPlease close all applications '
    'that are using this video file and try again!':
        'Không thể thay thế Audio trong file Video này.\\n'
        'Vui lòng đóng tất cả ứng dụng đang dùng file Video này và thử lại!',
    'Clear Recent Paths': 'Xóa Recent Paths',
    'Clear Source Profile': 'Xóa Source Profile',
    'Clear all Messages': 'Xóa tất cả Messages',
    'Create New Chain': 'Tạo Chain',
    'Delete Script - Only Scripts located in Local Folder can be deleted':
        'Xóa Script - Chỉ các Script nằm trong thư mục cục bộ mới có thể xóa',
    'Drag divider to allow recording of Inserts.\\nInserts above the line are '
    'recorded.\\nInserts below the line are played back.':
        'Kéo vạch phân cách để cho phép ghi Insert.\\n'
        'Insert phía trên dòng kẻ được ghi.\\n'
        'Insert phía dưới dòng kẻ được phát lại.',
    'Edit Channel Settings': 'Sửa cài đặt Channel',
    "In some hand-copied lead sheets, the key signature is shown only at the "
    "beginning of the first bar, and it is hidden on subsequent systems. To "
    "follow this convention, choose 'Hide Key Signatures'.":
        'Trong một số bản tổng phổ chép tay, hóa biểu chỉ hiện ở đầu ô nhịp '
        'đầu tiên và ẩn ở các dòng nhạc tiếp theo. '
        "Để theo quy ước này, hãy chọn 'Ẩn hóa biểu'.",
    'Linked': 'Đã liên kết',
    "Meters' Fallback": 'Tốc độ hồi Meter',
    'No project is active. Please create or load a project.':
        'Không có Project nào đang hoạt động. Vui lòng tạo hoặc tải một Project.',
    'North-East': 'Đông Bắc',
    'Note is playing': 'Note đang phát',
    'On (Keep Sound Slot Active)': 'Bật (Giữ Sound Slot hoạt động)',
    'Placement Mode: Move a control on your MIDI controller or add it manually.':
        'Chế độ đặt: Di chuyển một điều khiển trên MIDI Controller '
        'hoặc thêm thủ công.',
    "Ruler Display Type has been changed to \\'Bar + Beats\\' and the Grid Type "
    "to \\'Use Quantize\\'.  This is required for Metronome Click Pattern Emphasis.":
        "Kiểu hiển thị thước đo đã đổi thành 'Bar + Beats' và loại Grid thành "
        "'Dùng Quantize'. Điều này là bắt buộc để nhấn trọng âm "
        'Pattern Click Metronome.',
    'Ruler Mode: Bars+Beats Linear': 'Chế độ thước đo: Bars+Beats tuyến tính',
    'Show Bar Number at Start of System for Bar Split Over Break':
        'Hiện số ô nhịp ở đầu dòng nhạc cho ô nhịp bị tách qua chỗ ngắt',
    'Show Normal Bar Number If Coincident with Start of Multi-Bar Rest Showing Range':
        'Hiện số ô nhịp bình thường nếu trùng với điểm bắt đầu '
        'của dải dấu lặng nhiều ô nhịp',
    'Single-line Instruments': 'Nhạc cụ 1 dòng kẻ',
    'Slashes without Stems': 'Gạch chéo không có thân nốt',
    'Some of the tracks that you want to delete contain data/events.\\n'
    'Do you really want to delete the tracks?':
        'Một số Track bạn muốn xóa có chứa dữ liệu/Event.\\n'
        'Bạn có thực sự muốn xóa các Track này không?',
    'The Control Room is disabled! Do you want to enable it?':
        'Control Room đang bị tắt! Bạn có muốn bật nó không?',
    'This will remove all columns in the Results list (except Name) for this '
    'combination of media types.':
        'Thao tác này sẽ gỡ bỏ tất cả cột trong danh sách kết quả '
        '(ngoại trừ Tên) cho tổ hợp loại Media này.',
    'Time Signature (changes the time signature before the project cursor position)':
        'Số chỉ nhịp (đổi số chỉ nhịp phía trước vị trí con trỏ Project)',
    'Use Reference Level (Press [ALT] to set)':
        'Dùng mức tham chiếu (Nhấn [ALT] để đặt)',
    'Warning: A control with the defined MIDI message already exists. Please '
    'change the MIDI message settings of one of the controls.':
        'Cảnh báo: Điều khiển với thông điệp MIDI đã định nghĩa đã tồn tại. '
        'Vui lòng đổi cài đặt thông điệp MIDI của một trong các điều khiển.',
    'Your changes will be lost and you will have to re-analyse this audio.':
        'Các thay đổi của bạn sẽ bị mất và bạn sẽ phải phân tích lại đoạn Audio này.',
    '\\nContext: ': '\\nNgữ cảnh: ',
}

if __name__ == '__main__':
    vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                        encoding='utf-8'))

    broken = {k for k, v in vi.items() if MOJIBAKE.search(v)}
    print(f'values containing U+FFFD: {len(broken)}')
    missing = broken - set(REPAIRS)
    extra = set(REPAIRS) - broken
    if missing:
        print(f'  NO REPAIR DEFINED: {sorted(missing)}')
    if extra:
        print(f'  repair defined but value is clean: {sorted(extra)}')

    bad = [k for k, v in REPAIRS.items() if MOJIBAKE.search(v)]
    if bad:
        print(f'  REPAIR STILL BROKEN: {bad}')
        sys.exit(1)

    if not WRITE:
        print('\n(dry run - pass --write to apply)')
        sys.exit(0)

    applied = 0
    for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
        data = json.load(open(path, encoding='utf-8'))
        dirty = False
        for k, new in REPAIRS.items():
            if k in data and data[k] != new:
                data[k] = new
                dirty = True
                applied += 1
        if dirty:
            json.dump(data, open(path, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=2, sort_keys=True)
    print(f'applied {applied} repair(s)')
