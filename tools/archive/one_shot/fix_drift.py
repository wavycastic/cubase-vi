#!/usr/bin/env python3
"""Repair the near-duplicate drift groups and any mojibake.

  python tools/fix_drift.py            # dry run
  python tools/fix_drift.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

# Replacement character U+FFFD and the classic mis-decoded sequences.
MOJIBAKE = re.compile('[\ufffd]|Ã[\x80-\xbf]|â€[\x80-\xbf]')

# (key, correct Vietnamese) - the group's agreed wording
FIXES = {
    # Channel must stay English (AGENT.md loanword), not 'Kênh'
    'Channel': 'Channel',
    # unify MIDI file wording
    'MIDI file': 'File MIDI',
    'Export MIDI file': 'Export File MIDI',
    'Export file MIDI': 'Export File MIDI',
    # case drift on the same label
    'Choose location': 'Chọn Location',
    'Clear all Messages': 'Xóa tất cả Messages',
    'Make unique name': 'Tên Make Unique',
    'Not set': 'Chưa đặt',
    'Not Set': 'Chưa đặt',
    # ellipsis pairs must agree apart from the dots
    'Auto Fades Settings...': 'Cài đặt Auto Fades...',
    'Generate Harmony Voices...': 'Tạo bè Hòa âm...',
    'Generate Harmony Voices': 'Tạo bè Hòa âm',
    'Logical Editor...': 'Logical Editor...',
    'MixConsole Snapshot Recall Settings...': 'Cài đặt gọi lại Snapshot MixConsole...',
    'MixConsole Snapshot Recall Settings': 'Cài đặt gọi lại Snapshot MixConsole',
    'Others...': 'Khác...',
    'Others': 'Khác',
    'Page Setup...': 'Thiết lập Page...',
    'Page Setup': 'Thiết lập Page',
    'Presets...': 'Presets...',
    'Plug-Ins': 'Plug-ins',
    '4-note chords': 'Hợp âm 4 nốt',
    '4-Note Chords': 'Hợp âm 4 nốt',
    '1 beat': '1 Beat',
    '1 Beat': '1 Beat',
    '%d channels': 'Channel %d',
    '%d Channels': 'Channel %d',
    '(none)': '(không có)',
    '(None)': '(không có)',
    'Activate track': 'Bật Track',
    'New Parts[RM]': 'Tạo Parts[RM]',
    'New Parts': 'Tạo Parts',
    'Keep Last[RM]': 'Giữ Last[RM]',
    'Keep Last': 'Giữ Last',
    'Keep History[RM]': 'Giữ History[RM]',
    'Ornate Ped.': 'Ký hiệu Ped nghệ thuật',
    'Ornate Ped': 'Ký hiệu Ped nghệ thuật',
}

vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))

print('--- mojibake present in the map ---')
moj = [(k, v) for k, v in vi.items() if MOJIBAKE.search(v)]
for k, v in moj:
    print(f'  {k!r} -> {v!r}')
if not moj:
    print('  (none)')

print('\n--- drift fixes ---')
pending = {}
for k, new in FIXES.items():
    cur = vi.get(k)
    if cur is None:
        print(f'  SKIP (not a key): {k!r}')
        continue
    if cur != new:
        pending[k] = new
        print(f'  {k!r}\n      {cur!r}\n   -> {new!r}')

if MOJIBAKE.sub('X', 'X') and moj:
    print(f'\nWARNING: {len(moj)} value(s) still contain mojibake; '
          f'fix those by hand before shipping.')

if not WRITE:
    print(f'\n(dry run - {len(pending)} change(s); pass --write to apply)')
    sys.exit(0)

for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, new in pending.items():
        if k in data and data[k] != new:
            data[k] = new
            dirty = True
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)

left = [k for k in pending if k not in
        {kk for p in glob.glob(os.path.join(BATCH_DIR, '*.json'))
         for kk in json.load(open(p, encoding='utf-8'))}]
print(f'\napplied {len(pending) - len(left)} change(s)')
if left:
    print(f'WARNING not present in any batch: {left}')
