#!/usr/bin/env python3
"""Round 32 of reading: the long values of the general catch-all.

499 sentences, of which this round read the first ninety. The short labels
are done; sentences turn out to have their own defect, and it is the one the
whole project has been fighting since round 2.

DURATION WAS "TRUONG DO". Eight strings:

    "- Maximum project duration for sample-precise object positions exceeded"
      -> "- Da vuot qua truong do toi da cua Project cho vi tri doi tuong ..."
    "Break All Secondary Beams at Rests When Duration Differs"
      -> "Ngat tat ca duoi not phu tai dau lang khi truong do khac nhau"
    "The Cautionary Accidentals options only apply when using the ..."
      -> "... chi ap dung khi dung quy tac truong do dau hoa"
    "This specifies the maximum duration the Score Editor will create ..."
      -> "... xac dinh truong do toi da ma Score Editor se tao cho mot ..."

"Truong do" is a FIELD OF STUDY - a university department, a discipline. It is
not a length. Duration is "thoi luong", and the map already uses that in about
forty keys, including the three "Maximum Duration" labels fixed in round 28.

It got there the way most of these errors get there: "Duration" beside
"Field" in the same settings panel, and a translation pass that read the
neighbour instead of the word.

The other class in this round is capital letters and untranslated nouns in the
middle of a Vietnamese question - the "Are you sure ...?" family, where four
of them said:

    "Ban co chac muon Tat tat ca additional outputs khong?"
    "Ban co chac muon go bo tat ca modulation connections khong?"
    "Ban co chac muon Dat lai tat ca cue sends khong?"
    "Ban co chac muon Tat tat ca outputs (except output "%s") khong?"

Three of the four keep the verb capitalised, which Vietnamese never does
except at the start of a sentence, and all four leave the object in English
while the sibling questions translate it.

And two of the round 12 scramble family, where the English label is quoted and
therefore has to stay in English but the surrounding Vietnamese had not been
written:

    "Pitch Visibility: Select Next Option" not possible because no compatible
    instrument is connected
      -> "Pitch Visibility: Select Next Option" khong kha dung vi khong co
         nhac cu tuong thich nao duoc ket noi

That one is actually right - the label is a feature name and stays. Which is
worth saying, because it is the exception that proves the rule: a quoted feature
name is not untranslated text.

  python tools/fix_reading32.py
  python tools/fix_reading32.py --write
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
    # ==================================================================
    # Duration is "thoi luong". "Truong do" is a field of study.
    # ==================================================================
    '- Maximum project duration for sample-precise object positions exceeded':
        '- Đã vượt quá thời lượng tối đa của Project cho vị trí đối tượng '
        'chính xác tới mức sample',
    'Break All Secondary Beams at Rests When Duration Differs':
        'Ngắt tất cả đuôi nốt phụ tại dấu lặng khi thời lượng khác nhau',
    'Notes Starting after the Start of the Bar of Multiple Beats in Duration':
        'Các nốt bắt đầu sau đầu Bar với thời lượng nhiều phách',
    'Notes Starting at the Start of the Bar or the Half-Bar of Multiple '
    'Beats in Duration':
        'Các nốt bắt đầu tại đầu Bar hoặc nửa Bar với thời lượng nhiều phách',
    'Respect Maximum Duration for Rhythmic Slashes in Compound Time Signatures':
        'Tôn trọng thời lượng tối đa cho dấu gạch chéo nhịp trong số chỉ '
        'nhịp phức',
    'Respect Maximum Duration for Rhythmic Slashes in Irregular Time Signatures':
        'Tôn trọng thời lượng tối đa cho dấu gạch chéo nhịp trong số chỉ '
        'nhịp bất thường',
    'The Cautionary Accidentals options only apply when the Common Practice '
    'accidental duration rule is used. A subset of options for the Modernist '
    'duration rule can be found in that section.':
        'Tùy chọn dấu hóa nhắc lại chỉ áp dụng khi dùng quy tắc thời lượng '
        'dấu hóa Thực hành chung. Một phần tùy chọn của quy tắc thời lượng '
        'Hiện đại nằm trong mục đó.',
    "This specifies the maximum duration the Score Editor will produce for a "
    "rhythmic slash, without considering rhythm dots, and applies in all time "
    "signatures. For example, if you choose '1/4 Note (Crotchet)', the Score "
    "Editor will create four slashes in 2/2, and two dottet slashes in 6/8.":
        'Tùy chọn này xác định thời lượng tối đa mà Score Editor sẽ tạo cho '
        'một dấu gạch chéo nhịp, không tính các dấu chấm dôi, và áp dụng cho '
        "mọi số chỉ nhịp. Ví dụ, nếu bạn chọn 'Note 1/4 (Crotchet)', Score "
        'Editor sẽ tạo bốn gạch trong 2/2 và hai gạch có chấm trong 6/8.',

    # ==================================================================
    # the "Are you sure ...?" family: capital verb, English object
    # ==================================================================
    'Are you sure you want to deactivate all additional outputs?':
        'Bạn có chắc muốn tắt tất cả đầu ra bổ sung không?',
    'Are you sure you want to deactivate all outputs (except output "%s")?':
        'Bạn có chắc muốn tắt tất cả đầu ra (trừ đầu ra "%s") không?',
    'Are you sure you want to remove all modulation connections?':
        'Bạn có chắc muốn gỡ bỏ tất cả kết nối Modulation không?',
    'Are you sure you want to reset all cue sends?':
        'Bạn có chắc muốn đặt lại tất cả Cue Send không?',
    'Are you sure you want to edit so many events?':
        'Bạn có chắc muốn sửa nhiều Event như vậy không?',
    'Are you sure you want to replace the plug-in "%s"?':
        'Bạn có chắc muốn thay thế Plug-in "%s" không?',
    'Are you sure you want to remove all modulators of this track?':
        'Bạn có chắc muốn gỡ bỏ tất cả Modulator của Track này không?',

    # ==================================================================
    # the "Cannot add more tracks ..." family, seven near-identical
    # sentences that all said "So luong"
    # ==================================================================
    'Cannot add more tracks. The MIDI track count is at the limit.':
        'Không thể thêm Track. Số MIDI Track đã đạt giới hạn.',
    'Cannot add more tracks. The VCA track count is at the limit.':
        'Không thể thêm Track. Số VCA Track đã đạt giới hạn.',
    'Cannot add more tracks. The effect track count is at the limit.':
        'Không thể thêm Track. Số Effect Track đã đạt giới hạn.',
    'Cannot add more tracks. The group track count is at the limit.':
        'Không thể thêm Track. Số Group Track đã đạt giới hạn.',
    'Cannot add more tracks. The instrument track count is at the limit.':
        'Không thể thêm Track. Số Instrument Track đã đạt giới hạn.',
    'Cannot add more tracks. The video track count is at the limit.':
        'Không thể thêm Track. Số Video Track đã đạt giới hạn.',
    'Cannot save more MixConsole snapshots. The snapshot count is at the limit.':
        'Không thể lưu thêm Snapshot MixConsole. Số Snapshot đã đạt giới hạn.',

    # ==================================================================
    # capitalisation and half-translated objects
    # ==================================================================
    'All parts specified in \'Part Editing Mode\' are used.':
        "Tất cả Part chỉ định trong 'Chế độ sửa Part' đều được sử dụng.",
    'All source tracks will be hidden. To show the tracks again, activate them '
    'on the Visibility tab.':
        'Tất cả Source Track sẽ bị ẩn. Để hiện lại Track, hãy bật chúng trên '
        'thẻ hiển thị.',
    'Allows you to toggle the state of the mapped function. If the hardware '
    'control or the %s function are in toggle mode, use the jump mode instead.':
        'Cho phép bạn chuyển đổi trạng thái của chức năng đã được Mapping. '
        'Nếu điều khiển phần cứng hoặc chức năng %s ở chế độ chuyển đổi, hãy '
        'dùng chế độ Jump.',
    'An error occurred while inserting the markers into the project.':
        'Đã xảy ra lỗi khi chèn các Marker vào Project.',
    'Attribute Counter (Number of items waiting to have their Attributes '
    'updated)':
        'Bộ đếm thuộc tính (số lượng mục đang chờ cập nhật thuộc tính)',
    'Attributes apply to individual notes, directions apply to all following '
    'notes':
        'Thuộc tính áp dụng cho từng nốt, chỉ dẫn diễn tấu áp dụng cho tất cả '
        'nốt phía sau',
    'Adds/subtracts the selected amount of frames to the position sent via '
    'RS422 Out (playback mode)':
        'Cộng/trừ số lượng Frame đã chọn vào vị trí gửi qua RS422 Out '
        '(chế độ phát)',
    'Add Selected Instrument "%s" to Favorites':
        'Thêm Instrument đã chọn "%s" vào Favorites',
    'Add Device (from a popup list of available devices)':
        'Thêm Device (từ danh sách Pop-up các Device khả dụng)',
    'A controller script with the same name already exists. Use the MIDI '
    'Remote Manager to enable or delete it.':
        'Đã có Script Controller cùng tên tồn tại. Dùng MIDI Remote Manager để '
        'bật hoặc xóa Script đó.',
    'A label field is linked to one or more controls on the surface and will '
    'automatically generate its text once the controls are mapped.':
        'Trường nhãn được liên kết với một hoặc nhiều Control trên Surface và '
        'sẽ tự động tạo văn bản khi các Control đã được Mapping.',
    'Activate remote control for Voicings, Tensions and Transpose':
        'Bật điều khiển từ xa cho các Voicing, Tension và Transpose',
    'All connections routed to the side-chain inputs have been reset. Your '
    'project may sound differently.':
        'Tất cả kết nối tới đầu vào Side-Chain đã được đặt lại. Âm thanh của '
        'Project có thể sẽ khác.',
    '- Negative project start offset has been reset to zero':
        '- Độ lệch bắt đầu Project âm đã được đặt lại về 0',
    '     -> Non-matching mixer channels will be removed!':
        '     -> Các MixConsole Channel không khớp sẽ bị gỡ bỏ!',
    '"Create Lanes from Versions" not possible for write protected tracks':
        '"Tạo Lane từ Version" không khả dụng cho Track bị bảo vệ ghi',
    '"Create Versions from Lanes" not possible for write protected tracks':
        '"Tạo Version từ Lane" không khả dụng cho Track bị bảo vệ ghi',
    '"%s" not possible for write protected tracks':
        'Không thể "%s" với các Track đang bị bảo vệ ghi',
    'Bypass Modulators of All Visible Channels':
        'Bypass Modulator của tất cả Channel đang hiện',
    'Bypass Modulator on/off.\\nModulator on/off with [ALT + click].':
        'Bật/tắt Bypass Modulator.\\nBật/tắt Modulator bằng [ALT + nhấp chuột].',
    'Bypass Module on/off.\\nModule on/off with [ALT + click].':
        'Bật/tắt Bypass Module.\\nBật/tắt Module bằng [ALT + nhấp chuột].',
    'A reading/writing error occurred. This disk is not working normaly.':
        'Đã xảy ra lỗi đọc/ghi. Đĩa này đang không hoạt động bình thường.',
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
       or '�' in v or not v.strip()]
if bad:
    print('PROBLEM (placeholder, U+FFFD or empty):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}')
print()
for k, v in changed.items():
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:70]!r}\n   -> {v!r}')

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
