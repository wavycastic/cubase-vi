#!/usr/bin/env python3
r"""Vòng 93: 70 chuỗi, #303-372. Đọc tuần tự, không lọc.

Bốn lỗi, tất cả trong **một gia đình**: nhóm "Activate". Nhóm này dài và
đều, nên chỗ lệch rất dễ thấy khi đọc cạnh nhau.

1. `Activate` -> `Kích hoạt`, còn `Deactivate` -> `Tắt`.

   Cặp này lệch nhau: một bên "kích hoạt", một bên "tắt". Và cả nhóm
   `Activate ...` bên dưới đều dùng **"Bật"** (`Activate ASIO-Guard` ->
   `Bật ASIO-Guard`, `Activate Metronome` -> `Bật Metronome`). Nên `Activate`
   đứng riêng là thành viên lạc, và nó cũng là thành viên **lệch với cặp
   đối xứng** của nó. Sửa thành `Bật`, khớp `Deactivate` -> `Tắt`.

2. `Activate All Outputs` -> `Kích hoạt tất cả đầu ra`, còn `Activate Output`
   và `Activate Outputs` -> `Bật đầu ra`.

   Cùng một danh từ, hai động từ khác nhau, ngay sát nhau.

3. `Activate Effect` -> `Bật hiệu ứng`.

   Cả nhóm Effect giữ tiếng Anh, hơn mười anh em: `Add Effect`, `Add Effect
   Track`, `Add External Effect`, `Bypass Effect`, `Edit Effect "%s"`,
   `Change Insert Effect Configuration`, `Connect External Effect`... Chỉ
   `Activate Effect` dịch ra "hiệu ứng". Đây cũng đúng luật §1 của AGENT.md:
   `Effect` nằm trong 90 từ giữ nguyên tiếng Anh.

4. `Activate Extend Process Range` -> `Mở rộng dải xử lý`.

   **Mất hẳn động từ "Activate".** Cả nhóm đều có "Bật" ở đầu, riêng chuỗi
   này bắt đầu bằng động từ của `Extend`. Đây là loại lỗi mà không đọc cạnh
   anh em thì không thấy, vì bản dịch vẫn *đọc được* - nó chỉ sai nghĩa.

  python tools/fix_reading93.py
  python tools/fix_reading93.py --write
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
    # 1. khớp Deactivate -> Tắt và cả nhóm "Bật ..."
    'Activate': 'Bật',
    # 2. cùng danh từ với Activate Output(s)
    'Activate All Outputs': 'Bật tất cả đầu ra',
    # 3. cả nhóm Effect giữ tiếng Anh (và §1 của AGENT.md giữ "Effect")
    'Activate Effect': 'Bật Effect',
    # 4. mất hẳn "Activate"
    'Activate Extend Process Range': 'Bật mở rộng dải xử lý',
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

# Mỗi luật trên phải kiểm được bằng chính anh em, không bằng ý kiến.
SIBLINGS = [
    ('Deactivate', 'Tắt'),                     # 1: cặp đối xứng
    ('Activate ASIO-Guard', 'Bật'),            # 1: cả nhóm
    ('Activate Metronome', 'Bật'),
    ('Activate Output', 'Bật đầu ra'),         # 2: cùng danh từ
    ('Add Effect', 'Effect'),                  # 3: cả nhóm Effect
    ('Bypass Effect', 'Effect'),
    ('Edit Effect "%s"', 'Effect'),
    ('Activate Folder Group Track', 'Bật '),  # 4: cả nhóm có "Bật" ở đầu
]
for k, must in SIBLINGS:
    if k not in vi:
        problems.append(f'giả định sai: không thấy anh em {k!r}')
    elif must not in vi[k]:
        problems.append(f'giả định sai: {k!r} không chứa {must!r}')

if problems:
    print('PROBLEM:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'khóa viết tay : {len(real)}')
print(f'cần đổi      : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:40]!r}  {vi.get(k, "")!r}  ->  {v!r}')

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
