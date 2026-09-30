#!/usr/bin/env python3
"""Round 83: four places where round 81 broke AGENT.md.

Round 81 was written while AGENT.md was unreadable - the file on disk was
142,411 bytes of null, so the rules had to be inferred from check_style.py
and the eighty earlier fix scripts. With the file readable again, four of
round 81's 61 changes turn out to violate it. All four are corrected here.

  1. `Pick-up` must stay English.

     AGENT.md, "### `Pick-up` -> **`Lấy đà`**": a previous round replaced
     "Lấy đà" (= pick up a drink) with the English "Pick-up" because the
     family already reads `Pick-up`, `Chế độ Pick-up`, `Bar Pick-up của:`.
     Round 81 then wrote "phải tự dò điểm bắt đầu" into a fourth member of
     that family, inventing a fourth name for one idea. Back to `Pick-up`.

  2. `to` means `sang`, not an arrow.

     AGENT.md §2, "Giới từ chuyển đổi": "`to` khi chuyển đổi nghĩa là `sang`",
     with the example `Mono to Multi-Channel` -> `Mono **sang** Multi-Channel`.
     Round 81 replaced "sang" with a literal `->` in three keys. Nothing in
     10,737 values uses an arrow to mean "becomes", so that was a new
     convention invented to save four characters. Same length, no invention.

  3. Two sentences lost their subject.

     AGENT.md §5, "Câu phải có chủ thể", and the "mất vế cuối" example in
     "Không làm mất câu" - which names one of these two very sentences as a
     past defect. Round 81 cut "Tùy chọn này" off the front of both, turning
     prose into a bare verb, and the second one had already been fixed once
     for exactly this. Subject restored.

  4. One more bare verb, this time by convention.

     10 of the 12 prose strings that begin "You can..." or "To <verb>" in
     this map keep a subject or a marker ("Bạn có thể", "Để", "Cần").
     Round 81 made this one an imperative, joining the minority of 2. It
     also happens to be the key where "Bạn" was already there and the round
     threw it away for no length gain worth having.

None of these undo round 81's savings except #3 and #4, which give back 25
characters between them to stay inside the rules.

  python tools/fix_reading83.py
  python tools/fix_reading83.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
PH = re.compile(r'%(?:(?:\.\d+)?[a-zA-Z%]|l)')

WORDING = {
    # 1. Pick-up back to English
    'Picks up on the value of the %s function as soon as the control reaches '
    'that value. This results in smooth value changes, but requires you to '
    'estimate the pickup value.':
        'Chức năng %s nhận giá trị khi Control tới đúng giá trị đó. Giá trị '
        'đổi mượt hơn nhưng phải tự dò điểm Pick-up.',

    # 2. `to` -> `sang`, not an arrow
    'Braced Staff to Braced Staff': 'Chuyển khuông nhạc có ngoặc sang có ngoặc',
    'Braced Staff to Unbraced Staff':
        'Chuyển khuông nhạc có ngoặc sang không ngoặc',
    'Staff Group to Staff Group': 'Chuyển nhóm khuông nhạc sang nhóm khuông nhạc',

    # 3. subject restored
    'This option deletes the preferences of current and older program '
    'installations and initializes the program with factory settings. Please '
    'be aware that all your custom settings will be removed. This operation '
    'cannot be undone.':
        'Tùy chọn này xóa Preferences của bản cài đặt hiện tại và các bản cũ, '
        'rồi đặt lại chương trình về cài đặt Factory. Mất toàn bộ cài đặt tùy '
        'chỉnh. Không hoàn tác được.',
    'This option disables your custom preferences and initializes the program '
    'with factory settings. Your preferences are available after restarting '
    'the program.':
        'Tùy chọn này tạm tắt Preferences tùy chỉnh và đặt lại chương trình '
        'về cài đặt Factory. Preferences dùng lại được sau khi khởi động lại.',

    # 4. "Bạn" was in this key already; round 81 dropped it for 11 characters
    'You can change your driver selection and settings at any time in the '
    'Studio Setup dialog (Studio menu > Studio Setup) in the VST Audio System '
    'section.':
        'Bạn có thể đổi Driver và cài đặt bất kỳ lúc nào trong hộp thoại Thiết '
        'lập Studio (menu Studio > Thiết lập Studio), phần VST Audio System.',
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

# The four claims this round makes about the map, each checked against the map
# AS IT WILL BE - not as it is now, or the guard just re-reports the very
# defects this round exists to fix.
after = dict(vi)
after.update(real)

problems = []

# 1. no value may name the pick-up point in anything but English
for k, v in after.items():
    if re.search(r'pick\s*up', k, re.I) and not re.search(r'pick-?up', v, re.I):
        problems.append(f'Pick-up not English: {k!r} -> {v!r}')

# 2. no arrow invented to mean "becomes". "%s->%s" is quoted straight out of
#    the English key command path and is not one of these.
for k, v in after.items():
    if '->' in re.sub(r'"[^"]*"|\'[^\']*\'', '', v) and re.search(
            r'\bto\b', k, re.I):
        problems.append(f'arrow for "to": {k!r} -> {v!r}')

# 3. these two keys must name their subject
for k in ('This option deletes the preferences of current and older program '
          'installations and initializes the program with factory settings. '
          'Please be aware that all your custom settings will be removed. '
          'This operation cannot be undone.',
          'This option disables your custom preferences and initializes the '
          'program with factory settings. Your preferences are available '
          'after restarting the program.'):
    if not real.get(k, '').startswith('Tùy chọn này'):
        problems.append(f'no subject: {k[:50]!r}')

# 4. the "You can..." prose key keeps "Bạn"
k4 = ('You can change your driver selection and settings at any time in the '
      'Studio Setup dialog (Studio menu > Studio Setup) in the VST Audio '
      'System section.')
if not real.get(k4, '').startswith('Bạn'):
    problems.append('no subject: driver selection key')

if problems:
    print('RULE STILL BROKEN:')
    for p in problems:
        print(f'  {p}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print(f'characters added : {sum(len(v) - len(vi.get(k, "")) for k, v in changed.items())}')
print()
for k, v in changed.items():
    old = vi.get(k, '')
    print(f'  {k[:56]!r}  {len(old)}c -> {len(v)}c')
    print(f'      {old!r}')
    print(f'   -> {v!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
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
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)
print(f'\napplied {n} change(s) to batches')
