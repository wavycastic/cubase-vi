"""Round 77: manual reading fixes - inactive/passive chains, existing/audio-stream.

Usage:
  python tools/fix_reading77.py
  python tools/fix_reading77.py --write
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
    # 1. inactive -> chua bat / khong dung / tat
    'A reading/writing error occurred. This disk is not working normaly.':
        'Lỗi đọc/ghi đĩa. Đĩa này chạy không bình thường.',
    "Colors can't be changed for inactive Projects":
        'Project chưa bật không đổi được màu',
    'Delete Inactive Versions of All Tracks':
        'Xóa các Version không dùng của mọi Track',
    'Delete Inactive Versions of Selected Tracks':
        'Xóa các Version không dùng của Track đã chọn',
    'Deleted %i inactive versions (of %i tracks)':
        'Đã xóa %i Version không dùng (của %i Track)',
    'Inactive Cycle':
        'Cycle tắt',
    'Inactive Note Event Intensity':
        'Độ đậm Note Event chưa chọn',
    'Modulators are not displayed in inactive projects':
        'Project chưa bật không hiện Modulator',
    'Onscreen Window is not active.':
        'Cửa sổ Onscreen không bật.',
    'Passes: Remove Inactive Branchs':
        'Lượt xử lý: Xóa nhánh không dùng',
    'Remove Inactive':
        'Gỡ mục không dùng',
    "Tracks can't be added to inactive projects.":
        'Project chưa bật không thêm được Track.',
    "Tracks can't be deleted from inactive projects.":
        'Project chưa bật không xóa được Track.',

    # 2. single-word fixes
    'Notes Following a Change of Key Signature That Shows Cancellation Naturals':
        'Các nốt sau khi đổi hóa âm có hiện dấu bình khử',
    '- Automation keyframes outside of project borders have been discarded':
        '- Keyframe Automation ngoài ranh giới Project đã bỏ',
    'Activating/Deactivating of the Arranger Mode is not possible during recording':
        'Không bật/tắt được chế độ Arranger khi đang ghi',
    'Settings cannot be changed during recording':
        'Không đổi được cài đặt khi đang ghi',

    # 3. dang duoc -> active voice
    '%s is assigned to %d track(s).\\nDo you want to remove %s?':
        '%s đang gán cho %d Track.\\nGỡ bỏ %s không?',
    'A video with this file name is already in use. Please choose another name.':
        'Tên file này đã có Video dùng. Chọn tên khác.',
    "Bus '%s' is used in your project! Delete anyway?":
        "Bus '%s' đang dùng trong Project! Xóa luôn?",
    'Image under construction...':
        'Đang dựng hình ảnh...',
    'Multiple Sound Slots are selected. Only Output Mappings with identical values are shown.':
        'Đã chọn nhiều Sound Slot. Chỉ hiện Mapping đầu ra có giá trị giống nhau.',
    'Pitch is used, but does not match to Scale Assistant settings':
        'Pitch đang dùng nhưng không khớp cài đặt Scale Assistant',
    'Show Drum Sounds in use by Instrument':
        'Hiện âm thanh Drum mà Instrument đang dùng',
    'Some files are referenced by clips that are still in the Pool. These files have not been deleted.':
        'Một số file vẫn được các Clip trong Pool dùng tới. Những file này chưa xóa.',
    'The Expression Map is assigned to the following tracks:\\n%s':
        'Expression Map đang gán cho các Track sau:\\n%s',
    'The Pattern cannot be deleted because it is used by %i Pattern Events on the Track.':
        'Không xóa được Pattern vì %i Pattern Event trên Track đang dùng nó.',
    'The Pattern cannot be deleted because it is used by a Pattern Event on the Track.':
        'Không xóa được Pattern vì một Pattern Event trên Track đang dùng nó.',
    'This modifier combination is used by %s.\\nDo you want to overwrite it?':
        'Tổ hợp phím Modifier này đã có %s dùng.\\nGhi đè lên nó không?',
    'it is used in another Pool!':
        'nó đang dùng trong Pool khác!',

    # 4. se duoc -> active voice
    '%d conflicting audio event will be bounced.':
        '%d Audio Event xung đột sẽ Bounce.',
    '%d conflicting audio events will be bounced.':
        '%d Audio Event xung đột sẽ Bounce.',
    'A Brickwall limiter will be used to comply to this Max. True Peak Level':
        'Brickwall Limiter sẽ giữ mức True Peak tối đa này',
    'All settings from source will be transferred to new tracks (incl. automation). Audio file is dry on hard disk.':
        'Mọi cài đặt từ nguồn sẽ chuyển sang Track mới (gồm Automation). File Audio ở dạng Dry trên đĩa.',
    'Data Transfer failed.\\nTo avoid data loss, the data will remain in source database.\\n':
        'Không thể chuyển dữ liệu.\\nĐể tránh mất dữ liệu, dữ liệu sẽ giữ lại trong cơ sở dữ liệu nguồn.\\n',
    'External files will be copied into the working directory!':
        'File External sẽ sao chép vào thư mục làm việc!',
    'For each unique value that occurs in this column, a marker track is generated.':
        'Mỗi giá trị duy nhất trong cột này sẽ tạo một Marker Track.',
    'If locked, the track and file names of the rendered selection will be derived from the track and event names.':
        'Nếu khóa, tên Track và tên file của vùng chọn được Render sẽ lấy từ tên Track và tên Event.',
    'If locked, the track and file names of the rendered tracks will be derived from the track names.':
        'Nếu khóa, tên Track và tên file của các Track được Render sẽ lấy từ tên Track.',
    'Name already exists. A unique name is used instead.':
        'Tên đã tồn tại. Sẽ dùng tên duy nhất để thay thế.',
    'Other assigned pads will be transposed when changing the Root Key.':
        'Các Pad khác đã gán sẽ Transpose khi đổi Root Key.',
    'The project contains files or crossfades in 32-bit float format. Since OMF does not support this format, the files will be converted and exported as embedded data. Please note that this conversion might lead to clipping!':
        'Project chứa file hoặc Crossfade ở định dạng 32-bit float. Vì OMF không hỗ trợ định dạng này, các file sẽ chuyển đổi rồi Export dạng dữ liệu nhúng. Lưu ý chuyển đổi này có thể gây vỡ tiếng!',
    'The warp algorithm preset of one or several audio clip (s) is not supported by this program version. Preset (s) will be set to default.':
        'Phiên bản này không hỗ trợ Preset thuật toán Warp của một hoặc nhiều Audio Clip. Preset sẽ về mặc định.',
    'This operation will remove offline process histories.\\nAll edits will be frozen!':
        'Thao tác này sẽ xóa lịch sử xử lý Offline.\\nMọi chỉnh sửa sẽ Freeze!',
    'Warning: You cannot undo this operation!\\nOffline process histories will be removed.\\nAll edits will be frozen!':
        'Cảnh báo: Bạn không thể hoàn tác thao tác này!\\nLịch sử xử lý Offline sẽ bị xóa.\\nMọi chỉnh sửa sẽ Freeze!',

    # 5. da co san
    'The connection could not be created, as there is already a connection for that destination. A destination can only be assigned once to the same modulator.':
        'Không tạo được kết nối vì đích đó đã có kết nối. Một đích chỉ gán một lần cho cùng một Modulator.',
    'The destination parameter could not be selected, as there is already a connection for that destination. A destination can only be assigned once to the same modulator.':
        'Không chọn được tham số đích vì đích đó đã có kết nối. Một đích chỉ gán một lần cho cùng một Modulator.',

    # 6. existing / stream / script / keys / parts
    'Cannot remove existing audio stream from video file!':
        'Không gỡ được Audio Stream khỏi file Video!',
    "Script could not be imported. A Script for %s - %s already exists. Use the 'Delete Script' button first.":
        "Không Import được Script. Đã có Script cho %s - %s. Hãy xóa Script cũ bằng nút 'Xóa Script' trước.",
    'The key assignments are already used by:\\n\\n%s\\nDo you want to reassign the existing keys? Note that the previous assignments will be lost.':
        'Các phím này đã có chỗ dùng:\\n\\n%s\\nBạn có muốn gán lại không? Lưu ý gán cũ sẽ mất.',
    'Create new parts for each recording. Do not modify existing parts.':
        'Tạo Part mới cho mỗi lần ghi. Không sửa các Part hiện có.',
    'Create new parts, but remove any existing parts in the record range.':
        'Tạo Part mới, nhưng xóa mọi Part hiện có trong vùng ghi.',
    'Merge recorded data into existing parts.':
        'Gộp dữ liệu mới ghi vào các Part hiện có.',
    'Keep Existing Notes':
        'Giữ Note hiện có',
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
for k, v in list(changed.items())[:15]:
    print(f'  {k[:58]!r}')
    print(f'      {vi.get(k, "")[:100]!r}')
    print(f'   -> {v[:100]!r}')

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

print(f'\nupdated {n} batch occurrences across {len(glob.glob(os.path.join(BATCH_DIR, "*.json")))} files')
