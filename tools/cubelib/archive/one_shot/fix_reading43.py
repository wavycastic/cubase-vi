#!/usr/bin/env python3
"""Round 43: the media domain, long values 120-170.

`Material` has THREE renderings in the map, and this is the `String` mistake
again - one English word, read as two different English words.

    "The selected audio material is not suitable for tempo detection."
      -> "Tu lieu Audio da chon khong phu hop de nhan dien Tempo."
    "The audio material is not overlapping."
      -> "Tu lieu Audio khong bi chong lan."
    "Do you want to modify all events that refer to the same audio material?"
      -> "... tham chieu toi cung chat lieu Audio khong?"      (round 41)
    "In Single Voice mode, the notes are mapped to the selected voice
     (monophonic material only)"
      -> "... (chi danh cho chat lieu don am)"                (round 39)

`Tu lieu` is DOCUMENTS - a library word. `Chat lieu` is MATERIAL, and it covers
both senses: "chat lieu Audio" for the audio and "chat lieu don am" for the
monophonic one. So six keys converge on `chat lieu` and none on `tu lieu`.

The lesson is round 29's `String` (MIDI string, guitar string, text string) and
it keeps recurring because each new key looks like a fresh decision. One
English noun, one Vietnamese noun - decided once, applied everywhere.

`cannot be modulated` is missing its adverbial marker, in all four keys of the
family:

    "... as a parameter of a VST 2 plug-in cannot be modulated."
      -> "... tham so cua Plug-in VST 2 khong the Modulation."

Vietnamese needs the marker: "X khong the DUOC Modulation". Without it the
sentence says the parameter is not called Modulation. "Modulation chi gioi han
cho cac tham so co the Automation" has the same problem, and "co the
Automation" should be "co the nhan Automation" - receive automation.

And the warp sentence, which had a lowercase feature name in the middle:

    "The audio material contains warp markers or is in musical mode. If you
     slice it, warp markers are removed and musical mode is deactivated."
      -> "Tu lieu Audio chua tab Warp hoac dang o che do musical. Neu ban cat
         no, cac tab Warp se bi loai bo va che do musical se bi tat."

"tab Warp" - round 42 established that the name is Warp Tab. And "che do
musical" lowercase in the middle of a sentence, where every sibling says
"che do Musical". "cat no" should also be "cat lat", as round 41 established.

Three of the "The project file contains ..." sentences read

    "... chua du lieu '%s' khong duoc phien ban chuong trinh nay ho tro."

which stacks the relative clause onto the noun - "data that this program
version does not support" is fine in English and unreadable in Vietnamese.
Split it. Five of them, in one family, and two more with "nhieu o Insert hon
muc phien ban chuong trinh nay ho tro".

  python tools/fix_reading43.py
  python tools/fix_reading43.py --write
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
    # Material is "chat lieu" in all six keys - "tu lieu" is documents
    # ==================================================================
    'The selected audio material is not suitable for tempo detection.':
        'Chất liệu Audio đã chọn không phù hợp để nhận diện Tempo.',
    'The audio material is not overlapping.':
        'Chất liệu Audio không bị chồng lấn.',
    'The selected material is not suitable for tempo detection.':
        'Chất liệu đã chọn không phù hợp để nhận diện Tempo.',
    'The project contains events that use\\nthe same audio material as the '
    'event in this editor!\\nClick "New Version" if processing should '
    'apply\\nonly to the edited event!':
        'Project chứa các Event dùng\\ncùng chất liệu Audio với Event trong '
        'Editor này!\\nNhấp "Version mới" nếu muốn xử lý chỉ áp dụng\\ncho Event '
        'đã chỉnh sửa!',
    'The selection contains audio material that is processed with the "Solo" '
    'algorithm.\\nBefore exporting a Clip Package, you need to change the '
    'algorithm or use the Bounce Selection\\ncommand on the Audio menu for '
    'the following events:':
        'Vùng chọn chứa chất liệu Audio được xử lý bằng thuật toán "Solo".'
        '\\nTrước khi Export gói Clip, bạn cần đổi thuật toán hoặc dùng lệnh '
        'Bounce Selection\\ntrên menu Audio cho các Event sau:',
    'The selection contains audio material with a sample rate that differs '
    'from the project sample rate.\\nBefore exporting a Clip Package, the '
    'audio clips have to be converted.':
        'Vùng chọn chứa chất liệu Audio có Sample Rate khác với Sample Rate của '
        'Project.\\nTrước khi Export gói Clip, các Audio Clip cần được chuyển '
        'đổi.',

    # ==================================================================
    # a lowercase feature name and a lowercase Musical mid-sentence
    # ==================================================================
    'The audio material contains warp tabs or is in musical mode. If you '
    'slice it, warp tabs are removed and musical mode is deactivated.':
        'Chất liệu Audio chứa Warp Tab hoặc đang ở chế độ Musical. Nếu bạn cắt '
        'lát nó, các Warp Tab sẽ bị gỡ bỏ và chế độ Musical sẽ bị tắt.',

    # ==================================================================
    # "khong the Modulation" - Vietnamese needs the adverbial marker
    # ==================================================================
    'The connection could not be created, as a parameter of a VST 2 plug-in '
    'cannot be modulated. Use the VST 3 plug-in version instead.':
        'Không thể tạo kết nối vì tham số của Plug-in VST 2 không thể được '
        'Modulation. Hãy dùng phiên bản Plug-in VST 3 thay thế.',
    'The destination parameter could not be selected, as a parameter of a VST '
    '2 plug-in cannot be modulated. Use the VST 3 plug-in version instead.':
        'Không thể chọn tham số đích vì tham số của Plug-in VST 2 không thể '
        'được Modulation. Hãy dùng phiên bản Plug-in VST 3 thay thế.',
    'The connection could not be created, as the destination cannot be '
    'modulated. Modulation is restricted to automatable parameters of '
    'audio-related channels/tracks.':
        'Không thể tạo kết nối vì đích không thể được Modulation. Modulation '
        'chỉ giới hạn ở các tham số có thể nhận Automation của Channel/Track '
        'liên quan đến Audio.',
    'The destination parameter could not be selected, as the destination '
    'cannot be modulated. Modulation is restricted to automatable parameters '
    'of audio-related channels/tracks.':
        'Không thể chọn tham số đích vì đích không thể được Modulation. '
        'Modulation chỉ giới hạn ở các tham số có thể nhận Automation của '
        'Channel/Track liên quan đến Audio.',

    # ==================================================================
    # the relative clause stacked onto the noun, five in one family
    # ==================================================================
    "The project file contains '%s' data which is not supported by this "
    'program version. The data is being discarded.':
        "File Project chứa dữ liệu '%s' mà phiên bản chương trình này không hỗ "
        'trợ. Dữ liệu đang bị loại bỏ.',
    "The project file contains '%s' data which is not supported by this "
    'program version. The data is ignored.':
        "File Project chứa dữ liệu '%s' mà phiên bản chương trình này không hỗ "
        'trợ. Dữ liệu bị bỏ qua.',
    'The project file contains edit groups in folder tracks. This feature is '
    'not available in this program version.':
        'File Project chứa nhóm chỉnh sửa trong các Folder Track. Tính năng này '
        'không có trong phiên bản chương trình này.',
    'The project file contains more insert slots than supported by this '
    'program version. The slots are being discarded.':
        'File Project chứa nhiều ô Insert hơn mức phiên bản chương trình này '
        'hỗ trợ. Các ô đó đang bị loại bỏ.',
    'The project file contains more instrument slots than supported by this '
    'program version. The slots are being discarded.':
        'File Project chứa nhiều ô Instrument hơn mức phiên bản chương trình này '
        'hỗ trợ. Các ô đó đang bị loại bỏ.',
    'The project file contains more send slots than supported by this program '
    'version. The slots are being discarded.':
        'File Project chứa nhiều ô Send hơn mức phiên bản chương trình này hỗ '
        'trợ. Các ô đó đang bị loại bỏ.',
    'The warp algorithm preset of one or several audio clip (s) is not '
    'supported by this program version. Preset (s) will be set to default.':
        'Preset thuật toán Warp của một hoặc nhiều Audio Clip không được hỗ trợ '
        'bởi phiên bản chương trình này. Preset sẽ được đặt về mặc định.',

    # ==================================================================
    # small
    # ==================================================================
    'The project could not be replaced!\\nIt has been stored as new file "%s" '
    'instead!':
        'Không thể thay thế Project!\\nNó đã được lưu thành file mới "%s" thay cho '
        'file cũ!',
    'The project file was created with %s.\\nAlthough that program is able to '
    'read %s project files in general,\\nthe two might not be fully '
    'compatible, so you may want to keep the original file.\\n\\nDo you want '
    'to overwrite the project file or create a new file?':
        'File Project được tạo bằng %s.\\nDù chương trình đó nhìn chung có thể đọc '
        'file Project của %s,\\nhai bên có thể không hoàn toàn tương thích, nên bạn '
        'có thể muốn giữ lại file gốc.\\n\\nBạn có muốn ghi đè lên file Project hay '
        'tạo file mới?',
    'The export range is empty. Please set the left and right locators.':
        'Dải Export đang trống. Vui lòng đặt Left Locator và Right Locator.',
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
