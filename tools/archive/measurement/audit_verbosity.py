"""Đo độ dài dòng: tiếng Việt bao nhiêu so với tiếng Anh.

Tiếng Việt dịch từ tiếng Anh UI thường *ngắn hơn*, không dài hơn - nên tỉ lệ
ký tự là tín hiệu khách quan cho "dài dòng", khác với clarity.py long chỉ đếm
ngưỡng tuyệt đối.

Kèm phần đếm các từ đệm, vì đó là nguyên nhân chứ không phải triệu chứng.
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = r'E:\01_Projects\cubase-vi'
vi = json.load(open(f'{ROOT}\\translations\\vi.json', encoding='utf-8'))
src = {}
for line in open(f'{ROOT}\\keys\\all_strings.tsv', encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u

print(f'bản dịch: {len(vi):,}')

# ---------------------------------------------------------------- tỉ lệ độ dài
rows = []
for k, v in vi.items():
    e = src.get(k)
    if not e:
        continue
    # bỏ phần tiếng Anh còn sót, placeholder, và khoảng trắng thừa
    vc = re.sub(r'%[sd]|%\.\d+f|\{\w*\}', '', v)
    ec = re.sub(r'%[sd]|%\.\d+f|\{\w*\}', '', e)
    vc = re.sub(r'\s+', ' ', vc).strip()
    ec = re.sub(r'\s+', ' ', ec).strip()
    if len(ec) < 25:          # chuỗi ngắn không mang thông tin về dài dòng
        continue
    rows.append((len(vc) / len(ec), len(vc) - len(ec), k, e, v))

print(f'chuỗi nguồn >= 25 ký tự: {len(rows):,}')
r = sorted(x[0] for x in rows)
print()
print('tỉ lệ ký tự Việt/Anh:')
for p, label in ((0.10, 'p10'), (0.25, 'p25'), (0.50, 'median'),
                 (0.75, 'p75'), (0.90, 'p90'), (0.99, 'p99')):
    print(f'  {label:8} {r[int(p * (len(r) - 1))]:.2f}')

over = [x for x in rows if x[1] > 0]        # dài hơn
way = [x for x in rows if x[1] > 60]       # dài hơn nhiều
print()
print(f'  dài hơn tiếng Anh        : {len(over):>5}  ({len(over) * 100 // len(rows)}%)')
print(f'  dài hơn >= 60 ký tự      : {len(way):>5}  ({len(way) * 100 // len(rows)}%)')

# ---------------------------------------------------------------- từ đệm
FILLER = [
    (r'\bHãy\b', 'Hãy'),
    (r'\bVui lòng\b', 'Vui lòng'),
    (r'\bXin vui lòng\b', 'Xin vui lòng'),
    (r'\bBạn có thể\b', 'Bạn có thể'),
    (r'\bbạn có thể\b', 'bạn có thể'),
    (r'\bCó thể được\b', 'Có thể được'),
    (r'\bđược sử dụng để\b', 'được sử dụng để'),
    (r'\bSẽ được\b', 'Sẽ được'),
    (r'\bNếu muốn\b', 'Nếu muốn'),
    (r'\bBạn sẽ\b', 'Bạn sẽ'),
    (r'\bkhi bạn\b', 'khi bạn'),
    (r'\bĐể có thể\b', 'Để có thể'),
    (r'\bNói cách khác\b', 'Nói cách khác'),
    (r'\bCó nghĩa là\b', 'Có nghĩa là'),
]
print()
print('từ đệm:')
for pat, name in FILLER:
    n = sum(1 for v in vi.values() if re.search(pat, v))
    print(f'  {name:18} {n:>5}')

# ---------------------------------------------------------------- top offenders
print()
print('=== dài hơn nhiều nhất ===')
for ratio, delta, k, e, v in sorted(rows, key=lambda x: -x[1])[:12]:
    print(f'\n  +{delta}c  (VI {len(v)}c / EN {len(e)}c)')
    print(f'  EN: {e[:96]!r}')
    print(f'  VI: {v[:130]!r}')
