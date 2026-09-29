#!/usr/bin/env python3
"""Find Vietnamese that is grammatically possible but reads badly.

Nothing here is a missing translation or a wrong technical term - these are
strings a Vietnamese engineer would have to stop and re-read. Each rule names
a concrete machine-translation tell, and the output is meant to be read and
judged, not counted.

  python tools/audit_readability.py          summary
  python tools/audit_readability.py --list   every hit
"""
import json, os, re, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'), encoding='utf-8'))


# ---------------------------------------------------------------------------
# each rule: (name, compiled pattern, why it reads badly)
RULES = [
    # Vietnamese does not stack bare nouns with "của" the way English does
    # with "of": "cài đặt của của" is a broken calque.
    ('double của', re.compile(r'\bcủa\s+của\b', re.I),
     'hai từ "của" liền nhau - calque từ "of of"'),

    # "cho cho", "vào vào", "để để" - the same tell with other prepositions
    ('double preposition', re.compile(
        r'\b(cho\s+cho|vào\s+vào|để\s+để|với\s+với|làm\s+làm|'
        r'từ\s+từ|trong\s+trong)\b', re.I),
     'hai giới từ giống nhau liền nhau'),

    # English keeps the object after the verb ("select all tracks"), Vietnamese
    # moves it in front ("chọn tất cả Track"). A verb with a following English
    # noun and no Vietnamese noun is the calque showing through.
    ('verb + English object', re.compile(
        r'\b(Chọn|Thêm|Xóa|Nhân bản|Đặt|Hiện|Ẩn|Mở|Đóng|Lưu|Tải|Import|Export|'
        r'Bật|Tắt|Chèn|Ghi|Sửa|Đổi|Cắt|Dán)\s+'
        r'(all|every|each|other|new|old|first|last|next|previous|current|'
        r'selected|active|inactive|following|preceding|above|below|inside|'
        r'outside|between|available|enabled|disabled)\b', re.I),
     'động từ + danh từ tiếng Anh - vị trí từ theo tiếng Anh'),

    # "Có thể ... được" stacks two passive auxiliaries; one is enough.
    ('stacked passive', re.compile(r'\bCó thể\s+\w+\s+được\b', re.I),
     '"Có thể ... được" - hai động từ khuyết thiếu chồng nhau'),

    # "được ... của" - nominalisation where Vietnamese wants a verb.
    ('nominalisation', re.compile(
        r'\b(Việc|Quá trình|Sự việc)\s+\w+\s+của\b', re.I),
     'danh từ hoá vô nghĩa - tiếng Việt cần động từ'),

    # More than three consecutive capitalised words mid-sentence reads as a
    # phrase that was never translated.
    ('capital run', re.compile(r'(?<!^)(?<![.!?:]\s)(?<![\w"])\s'
                               r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,}'),
     '3 từ viết hoa liên tiếp giữa câu'),

    # "... của" hanging at the end with no owner.
    ('dangling của', re.compile(r'\bcủa\s*[:.]?\s*$'),
     '"của" treo ở cuối không có chủ thể'),

    # A colon or comma with nothing grammatical on one side.
    ('empty slot', re.compile(r'\(\s*\)|\[\s*\]|:\s*$|,\s*[,;]'),
     'dấu câu rỗng'),

    # The same word twice in a row.
    ('repeated word', re.compile(
        r'\b(\w{3,})\s+\1\b', re.I),
     'lặp từ'),

    # "được dùng cho ... được" - two passives in one clause.
    ('double được', re.compile(r'\bđược\s+[^.!?]{0,30}?\bđược\b'),
     'hai "được" trong một vế'),

    # A Vietnamese word where a preposition should be, from a botched swap.
    ('preposition swap', re.compile(
        r'\b(chọn|vào|thêm|đặt|xoá|xóa|gỡ)\s+(vào|cho|ra|đi)\b', re.I),
     'động từ + giới từ thừa'),

    # AGENT.md 2: "vào" is redundant only when the verb already carries the
    # direction, which in practice means the English verbs below. Vietnamese
    # verbs like "gán vào" or "chuyển vào" are natural and are not matched -
    # they need an object, which is what "vào" introduces.
    ('redundant vào', re.compile(
        r'\b(Go|Move|Map|Drag|Scroll|Synchronize|Kéo)\s+vào\s+'
        r'(?!thư mục|Group|thùng|Blocklist|Bus|Chord|bè)\w', re.I),
     'động từ đã chứa hướng + giới từ "vào" thừa'),

    # A very long noun-phrase stack with no verb: over 9 words before the first
    # Vietnamese verb-like word.
    ('long noun stack', re.compile(r'^(?:\S+\s+){9,}(?:và|hoặc|trong)\b', re.I),
     'chuỗi danh từ quá dài không có động từ'),

    # "không thể" followed by an English verb - the negation never got applied.
    ('untranslated negation', re.compile(
        r'\b(không thể|không được|không có)\s+[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}\b'
        r'(?![àáảãạăâêôơùúýĐ])', re.I),
     '"không thể" + cụm từ tiếng Anh - phủ định chưa được dịch'),
]

QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'|<[^>]*>|\[[^\]]*\]')


def analyse(v):
    bare = QUOTED.sub(' ', v)
    hits = []
    for name, pat, why in RULES:
        if pat.search(bare):
            hits.append((name, why))
    return hits


found = collections.defaultdict(list)
for k, v in vi.items():
    for name, why in analyse(v):
        found[name].append((k, v, why))

total = sum(len(x) for x in found.values())
print(f'strings audited          : {len(vi)}')
print(f'strings with a tell      : {len({k for x in found.values() for k, _, _ in x})}')
print(f'distinct tells triggered : {total}\n')
for name, items in sorted(found.items(), key=lambda x: -len(x[1])):
    print(f'  {name:22} {len(items):5}   {items[0][2]}')

if '--list' in sys.argv:
    for name, items in sorted(found.items(), key=lambda x: -len(x[1])):
        print(f'\n=== {name} ({len(items)}) ===')
        for k, v, _ in items[:40]:
            print(f'  {v[:96]!r}')
