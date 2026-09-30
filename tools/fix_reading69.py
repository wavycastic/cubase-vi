"""Round 69: a whole clause dropped, and it was the warning.

    EN  "The project will be saved as '%s', \\nbecause the program is in an
         unstable state after crashing \\nand saving might lead to corrupted
         files. \\nThe original file will be left untouched. \\nPlease restart
         the program after this operation!"

    VI  "Project sẽ được lưu thành '%s', \\nvì chương trình đang ở trạng thái
         không ổn định sau khi bị sự cố. \\nFile gốc sẽ được giữ nguyên. \\nVui
         lòng khởi động lại chương trình sau thao tác này!"

Four lines in, three out. The missing one is "and saving might lead to
corrupted files" - so the dialog now says the program crashed, the original file
is untouched, and restart, and never mentions that SAVING IS WHAT CORRUPTS IT.
The one clause that tells the user why they should be careful is the one that is
gone.

This is the seventh instance of the project's most persistent defect, and the
pattern has never varied: what goes missing is always the CONSEQUENCE.

    round 44  three of five, including "uses more power"
    round 69  "and saving might lead to corrupted files"

And it survived 68 rounds and six detectors because every one of them counted
SENTENCES, and a sentence that ends inside another one is not a missing sentence.
find_dropped_sentences looks for a value with fewer . ! ? than its source; this
value has three full stops and three question marks... it has three full stops
and the source has three, because the dropped clause sat inside a sentence whose
full stop survived with the rest of it.

    tools/check_punctuation.py

A NEW CHECK, and the reason it found this. The project brief has always required
that line breaks survive exactly, and nothing in the pipeline looked at them:

    "bao toan 100% placeholder, dau hai cham, ?/!/., dau ba cham,
     so dong moi, khoang trang dau/cuoi"

Six things, and check_style.py enforced one of them. Placeholders were covered.
Question marks, exclamation marks, semicolons and ellipses are now covered and
were already clean - a result worth having, because "already clean" is only
meaningful if something checked. Line breaks were not covered, and that is
exactly where the defect was.

So the check is four marks plus a line-break count plus the leading and trailing
whitespace, and it runs over all 10,737 values in under a second. It is wired
into build.py, so this class cannot come back.

  python tools/fix_reading69.py
  python tools/fix_reading69.py --write
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
    'The project will be saved as \'%s\', \\nbecause the program is in an '
    'unstable state after crashing \\nand saving might lead to corrupted '
    'files. \\nThe original file will be left untouched. \\nPlease restart '
    'the program after this operation!':
        'Project sẽ được lưu thành \'%s\', \\nvì chương trình đang ở trạng '
        'thái không ổn định sau khi bị sự cố \\nvà việc lưu có thể dẫn tới '
        'file bị hỏng. \\nFile gốc sẽ được giữ nguyên. \\nVui lòng khởi động lại '
        'chương trình sau thao tác này!',
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
       or '\ufffd' in v or not v.strip() or '[RM]' in v
       or src[k].count('\\n') != v.count('\\n')]
if bad:
    print('PROBLEM (placeholder, U+FFFD, empty, [RM], or line breaks):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
for k, v in changed.items():
    print(f'  {k[:58]!r}')
    print(f'      {vi.get(k, "")[:110]!r}')
    print(f'   -> {v[:110]!r}')

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
print(f'\napplied {n} change(s)')
