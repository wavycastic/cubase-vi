#!/usr/bin/env python3
r"""Vòng 98: 74 chuỗi, #679-752. Đọc tuần tự, không lọc.

Ba lỗi, đều trong nhóm `All ...`.

1. `All Multi-Channel Tracks` -> `Tất cả **các** Track đa kênh`
2. `All Systems`               -> `Tất cả **các** dòng nhạc`

   Trong 55 chuỗi `All *`, chỉ bốn chỗ có "các", và hai chỗ đó là lỗi:

       All Events matching the filter conditions -> ... khớp **các** điều kiện lọc
           ("các" bám vào "điều kiện", không phải danh từ chính - đúng)
       All on Selected Tracks                   -> Tất cả trên **các** Track đã chọn
           ("các" bám vào "Track" sau giới từ "trên" - tiếng Việt cần dấu này)
       All Multi-Channel Tracks                  -> Tất cả **các** Track đa kênh   <- lỗi
       All Systems                               -> Tất cả **các** dòng nhạc      <- lỗi

   Còn lại 51 chuỗi `All *` đều là `Tất cả X`, không "các". "Tất cả" đã là
   "tất cả" rồi, thêm "các" là thừa. Cùng lý do #707 ngay cạnh
   (`All Mono Tracks` -> `Tất cả Mono Track`, không "các") cũng không "các".

3. `All Ratings` -> `Tất cả **Đánh giá**` - hoa giữa giá trị, còn hai anh em
   thì thường: `Rating` -> `Đánh giá`, `Rating Filter` -> `Bộ lọc đánh giá`.

**Không sửa, và ghi rõ vì sao — đây là cụm lớn, không phải lỗi lẻ:**

*Nhóm `Template` đang lệch theo cả hai hướng.* 10 chuỗi dùng "mẫu" (`Templates`
-> `Mẫu`, `Install Template` -> `Cài đật mẫu`, `Select Template` -> `Chọn mẫu`,
`Save as Template` -> `Lưu thành mẫu`...), 2 chuỗi giữ tiếng Anh
(`Project Templates` -> `Project Template`, `Load SyncStation Template` ->
giữ nguyên). AGENT.md §1 lại liệt kê `Template` trong 90 từ **giữ nguyên**.

Theo luật thì phải giữ cả 12. Theo đa số trong bản dịch thì phải dịch cả 12.
Hai chuỗi giữ còn lại có thể là cố ý: `SyncStation` là tên sản phẩm.

Đây là quyết định đã được nhiều vòng chốt, quy mô 12 chuỗi, và tôi không có
bằng chứng nào để lật. **Để nguyên, ghi ở đây** để lần sau biết đây là chỗ
*cần quyết*, không phải chỗ *đã quết*.

*`Allow Alterations`* -> `Cho phép chỉnh sửa`. Trong ký âm, "alteration" là
nâng/hạ nốt nửa cung, còn "chỉnh sửa" là "edit". Có vẻ sai nghĩa, nhưng bảng
chỉ có đúng một chuỗi này, không có anh em để đối chiếu, nên tôi không đoán.

  python tools/fix_reading98.py
  python tools/fix_reading98.py --write
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
    'All Multi-Channel Tracks': 'Tất cả Track đa kênh',
    'All Systems': 'Tất cả dòng nhạc',
    'All Ratings': 'Tất cả đánh giá',
}

# ------------------------------------------------------------------ tự kiểm
real = {k: v for k, v in WORDING.items() if k in src}
problems = []

for k in sorted(set(WORDING) - set(real)):
    problems.append(f'NOT IN Cubase: {k[:70]!r}')

for k, v in real.items():
    if v.count('\n') != src[k].count('\n'):
        problems.append(f'newline count: {k[:46]!r}')
    if '\ufffd' in v or any(ord(c) < 0x20 and c not in '\t\n\r' for c in v):
        problems.append(f'bad char in {k[:46]!r}')
    if v != v.strip():
        problems.append(f'surrounding space: {k[:46]!r}')

SIBLINGS = [
    ('All Mono Tracks', 'Tất cả Mono Track'),   # 1: ngay cạnh, cũng không "các"
    ('All Channels', 'Tất cả Channel'),
    ('All Clips', 'Tất cả Clip'),
    ('All Parts', 'Tất cả Part'),
    ('Rating', 'Đánh giá'),                    # 3
    ('Rating Filter', 'đánh giá'),
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy {k[:44]!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k[:40]!r} không chứa {must!r}')

# Sau khi sửa, "Tất cả" phải không còn "các" bám vào danh từ chính. Hai chỗ
# hợp lệ ("các điều kiện", "trên các Track") phải còn nguyên.
after = dict(vi)
after.update(real)
allf = {k: v for k, v in after.items() if k.startswith('All ')}
bad = {k: v for k, v in allf.items() if re.match(r'^Tất cả các\b', v)}
if bad:
    problems.append(f'"Tất cả các ..." còn sót: {bad}')
keep = [k for k in allf if 'các điều kiện' in allf[k]
        or 'trên các Track' in allf[k]]
if len(keep) != 2:
    problems.append(f'phép thử yếu: mong đợi 2 chỗ "các" hợp lệ, thấy {len(keep)}')

# Không được đụng vào cụm Template. Đếm khoá chứa "Template" mà giá trị dùng
# "mẫu", và so TRƯỚC với SAU thay vì so với con số viết tay - lần này tôi đếm
# tay ra 10, thực tế là 11.
#
# Phiên bản trước kiểm "emplate" trong *giá trị*; giá trị tiếng Việt là "mẫu"
# nên ra 0, rồi 0 == 0 nên **pass im lặng**. Đây là lần thứ ba một phép thử
# rỗng được đọc là sự thật. Nay bắt buộc phải ra khác 0.
def tpl_count(m):
    return sum(1 for k, v in m.items()
               if 'emplate' in k and 'mẫu' in v.lower())


tpl_before = tpl_count(vi)
if tpl_before == 0:
    problems.append('phép thử rỗng: cụm Template ra 0 - kiểm lại cách đếm')
if tpl_count(after) != tpl_before:
    problems.append(f'cụm Template bị đụng: {tpl_before} -> {tpl_count(after)}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print(f'[đối chiếu] "All *": {len(allf)} chuỗi, không còn "Tất cả các ..."; '
      f'còn {len(keep)} chỗ "các" hợp lệ')
print(f'[ghi nhận] cụm Template: {tpl_before} chuỗi dùng "mẫu" - chưa quyết, để nguyên')
print()
for k, v in changed.items():
    print(f'  {k[:36]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
