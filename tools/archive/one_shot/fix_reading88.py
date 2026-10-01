#!/usr/bin/env python3
"""Vòng 88: 40 chuỗi dịch sát từng chữ - đọc ra dịch, không ra tiếng Việt.

Có một nhận định sai cần sửa trước. Độ dài **không** phải vấn đề:

    3.234 chuỗi có nguồn >= 25 ký tự
    chênh lệch median   -2c   (tiếng Việt NGẮN hơn)
    chênh lệch max      +21c
    dài hơn >= 30c      0 chuỗi
    lặp từ             9 chuỗi cả bản dịch

`audit_clarity.py` báo giá trị dài nhất là 328 ký tự và nhìn như dài hơn tiếng
Anh, nhưng nó **cắt cụt** chuỗi Anh khi in: nguồn của nó dài 371 ký tự, nên bản
dịch ngắn hơn 43 ký tự. Cả hai công cụ đúng, một cái hiển thị sai.

Vậy nên lọc bằng **tỉ lệ từ**, không bằng độ dài: tiếng Việt trải dài hơn
tiếng Anh trên mỗi từ, nên `>= 1.30 từ` là ngưỡng đúng. Còn 380 chuỗi.

Năm lỗi thật trong vòng này, đều là **sai nghĩa** chứ không phải dài:

1. **Dịch cụm chức năng thành danh từ.** "with Content" là đơn vị đo - đo tới
   nội dung - nhưng thành "với nội dung" thì đọc như quan hệ giữa hai thứ.
   `Minimum Inter-Staff Gap with Content` -> `Khoảng cách tối thiểu giữa các
   khuông nhạc (tới nội dung)`.

2. **Dịch sai thuật ngữ.** `directions` trong ký âm là **chỉ dẫn** (ký hiệu
   viết kiểu pizz./arco), không phải "diễn tấu". `chỉ dẫn diễn tấu` là sai
   nghĩa, không chỉ dài.

3. **Cụm Anh để dạng "động từ + danh từ"** đọc không thành câu:
   `Kích thước di chuyển nội dung` <- "Sizing Moves Content". Người dùng không
   bao giờ đọc "kích thước di chuyển"; họ kéo cạnh. -> `Kéo cạnh để đổi kích
   thước`.

4. **Giữ từ bị động không cần.** "cho việc mã hoá" <- "for video encoding" ->
   "khi mã hoá". Từ `cho` + danh từ hóa là mẫu dịch máy.

5. **Lặp cấu trúc.** "Thuộc tính áp dụng cho ..., chỉ dẫn áp dụng cho ..."
   - hai lần "áp dụng cho" là nửa dòng.

Ngoài ra bỏ "các" khi không cần, bỏ "với" trong "các Track đã chọn" ->
"Track đã chọn", và rút gọn chỗ tiếng Anh dài thừa mà dịch sẵn dùng
ngắn hơn: `Các Part` -> `các Part`, `giá trị hiện tại (các Track đã chọn)` ->
`giá trị hiện tại (Track đã chọn)`.

  python tools/fix_reading88.py
  python tools/fix_reading88.py --write
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
MAP = os.path.join(ROOT, 'translations', 'vi.json')
TSV = os.path.join(ROOT, 'keys', 'all_strings.tsv')
WRITE = '--write' in sys.argv

vi = json.load(open(MAP, encoding='utf-8'))
src = {}
for line in open(TSV, encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

WORDING = {
    # ---- 1. đơn vị đo, không phải quan hệ
    'Minimum Inter-Staff Gap with Content':
        'Khoảng cách tối thiểu giữa khuông nhạc (tới nội dung)',
    'Minimum Inter-System Gap with Content':
        'Khoảng cách tối thiểu giữa dòng nhạc (tới nội dung)',

    # ---- 2. thuật ngữ sai nghĩa
    'Attributes apply to individual notes, directions apply to all following notes':
        'Thuộc tính áp dụng cho từng nốt, chỉ dẫn áp dụng cho các nốt phía sau',

    # ---- 3. danh từ + động từ -> động từ
    'Object Selection Tool: Sizing Moves Content':
        'Công cụ chọn đối tượng: Kéo cạnh để đổi kích thước',

    # ---- 4. từ bị động thừa
    'Disables hardware acceleration for video encoding.':
        'Tắt tăng tốc phần cứng khi mã hoá Video.',
    'Short-term intelligibility at cursor position':
        'Độ rõ tiếng ngắn hạn tại con trỏ',
    'Open Projects in Last Used View':
        'Mở Project theo chế độ xem dùng gần nhất',
    'Limit note pitches to this value':
        'Giới hạn cao độ nốt theo giá trị này',
    'Reset Pitch Curve Changes for Selection':
        'Đặt lại đường cong Pitch trong vùng chọn',
    'Rendered files include all source settings.':
        'File đã Render chứa toàn bộ cài đặt nguồn.',
    # The key holds a literal backslash-n, not a newline: all_strings.tsv
    # stores it escaped, so a real \n here would not match any key.
    'Processing Overload\\nClick to Reset Display':
        'Quá tải xử lý\\nNhấp để đặt lại',
    'Show Bar Numbers at Time Signature at System Object Positions':
        'Hiện số Bar tại số chỉ nhịp ở các vị trí đối tượng của dòng nhạc',
    'Cannot access Project Folder on server: %s':
        'Không truy cập thư mục Project trên máy chủ: %s',
    'Project size of %s exceeded during auto save!':
        'Kích thước Project %s vượt quá trong lúc tự động lưu!',

    # ---- 5. bỏ "các" thừa
    'All files have the specified attributes!':
        'Tất cả file đều có thuộc tính đã chỉ định!',
    'Export used attributes of these categories:':
        'Export thuộc tính đã dùng của các danh mục sau:',
    'Shows all found attributes for the selected results':
        'Hiện mọi thuộc tính tìm được của các kết quả đã chọn',
    'Treat Muted Audio Events like Deleted':
        'Coi Audio Event đã Mute như đã xóa',
    'Activate this option to hide deactivated parameters':
        'Bật tùy chọn này để ẩn tham số đã tắt',
    'Automatically Resolve Collisions Between Adjacent Staves and Systems':
        'Tự xử lý chồng lấn giữa khuông nhạc và dòng nhạc cạnh nhau',
    'Found participants without master: %s. Try to reconnect?':
        'Có người tham gia không có master: %s. Kết nối lại?',
    'No Formats available for current Input Stream/Mode!':
        'Không có định dạng nào khả dụng cho Input Stream/Mode hiện tại!',
    'Range Tool Splits Partly Selected Events':
        'Công cụ vùng tách các Event chọn một phần',
    'Track Display Settings: Active Track Only':
        'Cài đặt hiển thị Track: Chỉ Track đang hoạt động',
    'Merge recorded data into existing parts.':
        'Gộp dữ liệu đã ghi vào các Part hiện có.',
    'Fill Gaps with Current Value (Selected Tracks)':
        'Lấp chỗ trống bằng giá trị hiện tại (Track đã chọn)',
    'Freeze/Unfreeze Selected Tracks (with Current Settings)':
        'Freeze/Bỏ Freeze Track đã chọn (theo cài đặt hiện tại)',
    'Hardware Reset without releasing USB connection':
        'Đặt lại phần cứng mà không ngắt USB',
    'Please close all shared Projects first':
        'Hãy đóng các Project đang chia sẻ trước',
    'Set Bar Position (Move Following Bars)':
        'Đặt vị trí Bar (dời các Bar sau)',

    # ---- 6. "để ... thay thế" thành mệnh lệnh
    'Stretch or pitch factor out of range! Use real time preset instead.':
        'Hệ số co giãn hoặc Pitch vượt phạm vi! Dùng Preset thời gian thực.',
    'Write protected - maintain a personal copy?':
        'Chỉ đọc - giữ lại bản sao riêng?',
    'Temporary Link Mode - Sync all touched parameters of selected channels':
        'Chế độ liên kết tạm thời - Đồng bộ mọi tham số vừa chỉnh của Channel đã chọn',

    # ---- 7. số chỉ nhịp: "bằng nhau" -> "đều", "phức" -> "phức tạp"
    'Apply Click Pattern to Equal Signatures':
        'Áp dụng Click Pattern cho số chỉ nhịp đều',
    'Paste Click Pattern to Selected Signatures':
        'Dán Click Pattern vào số chỉ nhịp đã chọn',
    'Respect Maximum Duration for Rhythmic Slashes in Irregular Time Signatures':
        'Giữ thời lượng tối đa của dấu gạch chéo nhịp trong số chỉ nhịp bất thường',
    'Respect Maximum Duration for Rhythmic Slashes in Compound Time Signatures':
        'Giữ thời lượng tối đa của dấu gạch chéo nhịp trong số chỉ nhịp phức tạp',
    'For Notation and main Chord Symbols':
        'Dành cho ký âm và ký hiệu hợp âm chính',
    '"Assign to First Unassigned Pad": No Unassigned Pads':
        '"Gán vào Pad chưa gán đầu tiên": Không có Pad chưa gán',
    'Flatten Real Time Processing (VariAudio and Warp)':
        'Giữ cố định xử lý thời gian thực (VariAudio và Warp)',
    '     -> Change the instrument configuration before reloading this setup.':
        '     -> Thay đổi cấu hình nhạc cụ trước khi tải lại thiết lập này.',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

if len(real) != len(WORDING):
    for k in sorted(set(WORDING) - set(real)):
        problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    # placeholder phải khớp tuyệt đối
    ph = lambda s: sorted(re.findall(r'%[sd]|%\.\d+f|%[0-9]*\$?[sd]|\{\w*\}', s))
    if ph(v) != ph(src[k]):
        problems.append(f'placeholder: {k[:50]!r} {ph(src[k])} -> {ph(v)}')
    # xuống dòng phải giữ nguyên số lượng
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:50]!r} '
                        f'{src[k].count(chr(10))} -> {v.count(chr(10))}')
    # Khoảng trắng đầu/cuối phải GIỐNG NGUỒN, không phải bằng rỗng: vài giá trị
    # Cubase cố ý thụt lùi để mũi tên thẳng hàng ('     -> ...'), và bỏ đi thì
    # hỏng bố cục.
    lead = lambda s: s[:len(s) - len(s.lstrip())]
    trail = lambda s: s[len(s.rstrip()):]
    if (lead(v), trail(v)) != (lead(src[k]), trail(src[k])):
        problems.append(f'surrounding space: {k[:50]!r} '
                        f'{lead(src[k])!r}{trail(src[k])!r} -> '
                        f'{lead(v)!r}{trail(v)!r}')
    for c in v:
        if ord(c) < 0x20 and c not in '\t\n\r':
            problems.append(f'control char in {k[:40]!r}')
            break
    if '�' in v:
        problems.append(f'U+FFFD in {k[:40]!r}')

# Không được dài hơn bản cũ - đó là cả mục tiêu của vòng này
grew = [(k, len(vi.get(k, '')), len(v)) for k, v in real.items()
        if len(v) > len(vi.get(k, ''))]
for k, a, b in grew:
    problems.append(f'LONGER than before: {k[:50]!r} {a}c -> {b}c')

# Vẫn phải giữ thuật ngữ DAW bằng tiếng Anh
MUST_KEEP = ['Project', 'Part', 'Track', 'Event', 'Render', 'Preset', 'Pad',
             'Warp', 'VariAudio', 'Bar', 'Click Pattern', 'Pitch']
for k, v in real.items():
    for t in MUST_KEEP:
        if re.search(rf'\b{re.escape(t)}\b', src[k]) and t not in v:
            problems.append(f'term dropped: {t!r} in {k[:46]!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay     : {len(real)}')
print(f'cần đổi          : {len(changed)}')
print(f'ký tự             : '
      f'{sum(len(v) - len(vi.get(k, "")) for k, v in changed.items()):+d}')
print()
for k, v in changed.items():
    old = vi.get(k, '')
    print(f'  {len(old)}c -> {len(v)}c   {k[:52]}')
    print(f'      {old!r}')
    print(f'   -> {v!r}')

if not WRITE:
    print('\n(chạy thử - thêm --write để ghi)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changed.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
print(f'\nđã ghi {n} thay đổi vào batches')
