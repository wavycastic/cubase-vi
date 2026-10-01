#!/usr/bin/env python3
"""Round 31 of reading: the last four gaps in the general catch-all.

Slices 5160, 5560, 6360 and 6660 - about 400 labels, and with them the S, U
and W blocks. Three families and one more word that was read as a different
word.

"Set ..." - about seventy keys, and roughly forty of them had a capital letter
in the middle of a Vietnamese phrase: "Dat Loai Controller", "Dat Do dai
Crossfade", "Dat Mau", "Dat Gia tri Automation". Vietnamese writes a verb
lowercase after "Dat". The same forty also left the noun in English in a dozen
cases - "Dat Destination Folder", "Dat Property", "Dat Project Folder",
"Dat Search Folder", "Dat Shape cho Pattern".

And two more of the round 12 scramble, in the pair that had already been fixed
once:

    "Separate Destination & Value" -> "Gia tri Separate Destination &"
    "Separate Label & Setting"     -> "Cai dat Separate Label &"

"Combined Destination & Value" was fixed in round 12. "Separate ..." is the
same label with the other half of the pair and had been missed. Same for
"Send ...", "Source ...", "Updating ...", "Smart Controls", "Until End" and
"Solo ...".

WORD READ AS A DIFFERENT WORD, the fourth of its kind:

    "Word Clock Output" -> "Tu Clock Dau ra"

  "Tu" is the Vietnamese for "word", as in a word of text. Word Clock is a
  clock sync signal - a single pulse per second that slaves run against. The
  other four Word Clock keys say "Word Clock" correctly, and "Word Spacing"
  correctly says "tu", so the map knows both senses. Here it picked the wrong
  one for the only key in the family that ends in Output.

    "You can join" -> "Ban can join"

  Four words, two of them English, no Vietnamese verb at all. This is the same
  key as "Can not join", which round 22 read and fixed to "Khong the tham gia
  Project." Two hundred keys apart, and the two halves of one question had
  gone in opposite directions.

    "White Keys" -> "Trang Key"
    "White Diamond Noteheads" -> "Trang Diamond Noteheads"

  Piano keys, and a notehead type - "Trang" in both, which is the English
  "white" left in place after a Vietnamese adjective.

"Smart Controls" had been reversed to "Dieu khien Smart" while its five
siblings all said "Smart Control". "Sound Slot" said "Am thanh Slot" while
"Add Sound Slot", "Remove Sound Slot" and "Move Sound Slot Up" all said
"Sound Slot". "Source Events" -> "Event Source" and "Source Tracks" ->
"Track Source" - both reversed, in a family where "Source Project" and
"Source Track" were already right.

  python tools/fix_reading31.py
  python tools/fix_reading31.py --write
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
    # "Set ..." - capital in the middle, or the noun left in English
    # ==================================================================
    'Set "%s" as Main Mix': 'Đặt "%s" làm Main Mix',
    'Set Automation Data': 'Đặt dữ liệu Automation',
    'Set Automation Terminator State':
        'Đặt trạng thái Automation Terminator',
    'Set Automation Value': 'Đặt giá trị Automation',
    'Set Color': 'Đặt màu',
    'Set Controller Type': 'Đặt loại Controller',
    'Set Crossfade Length': 'Đặt độ dài Crossfade',
    'Set Curve Type': 'Đặt loại đường cong',
    'Set Destination Folder': 'Đặt thư mục đích',
    'Set Event Color to Track Color': 'Đặt màu Event theo màu Track',
    'Set Event Description': 'Đặt mô tả Event',
    'Set Fine-Tune': 'Đặt tinh chỉnh',
    'Set Follow Global Transpose': 'Đặt bám theo Transpose toàn cục',
    'Set Locators to Selection Range': 'Đặt các Locator theo vùng chọn',
    'Set Main Value': 'Đặt giá trị chính',
    'Set Number of Channels': 'Đặt số Channel',
    'Set Number of Steps': 'Đặt số Step',
    'Set Origin Time': 'Đặt thời gian gốc',
    'Set Overlap': 'Đặt độ chồng lấn',
    'Set Pitch': 'Đặt cao độ',
    'Set Project Folder': 'Đặt thư mục Project',
    'Set Project Preview Start Position':
        'Đặt vị trí bắt đầu của Project Preview',
    'Set Property': 'Đặt thuộc tính',
    'Set Punch Points to Selection Range': 'Đặt Punch Point vào vùng chọn',
    'Set Range for Straighten Pitch Curve':
        'Đặt vùng cho đường cong Pitch đã làm thẳng',
    'Set Region End': 'Đặt cuối Region',
    'Set Region Start': 'Đặt đầu Region',
    'Set Release Length': 'Đặt độ dài Release',
    'Set Search Folder': 'Đặt thư mục tìm kiếm',
    'Set Secondary Value': 'Đặt giá trị phụ',
    'Set Shape for Pattern': 'Đặt hình dạng cho Pattern',
    'Set SMF Type': 'Đặt loại SMF',
    'Set Step Parameter': 'Đặt tham số Step',
    'Set Step Resolution': 'Đặt độ phân giải Step',
    'Set Tilt/Rotate Anchor': 'Đặt điểm tựa Tilt/Rotate',
    'Set Track Name': 'Đặt tên Track',
    'Set Track/Event Color': 'Đặt màu Track/Event',
    'Set Velocity Variance': 'Đặt phân tán Velocity',
    'Set Video Speed': 'Đặt tốc độ Video',
    'Selected Tracks (with Current Settings)':
        'Các Track đã chọn (theo cài đặt hiện tại)',
    'Selected Tracks...': 'Các Track đã chọn...',
    'Selection Brightness': 'Độ sáng vùng chọn',
    'Selection End Sample': 'Sample cuối vùng chọn',
    'Selection Start Sample': 'Sample đầu vùng chọn',
    'Selection Length in Samples': 'Độ dài vùng chọn tính bằng Sample',
    'Selection Mode': 'Chế độ vùng chọn',
    'Selection Options': 'Tùy chọn vùng chọn',
    'Selects Algorithm Preset': 'Chọn Preset thuật toán',
    'Selects the type of position message sent to the host':
        'Chọn loại thông điệp vị trí gửi tới Host',
    'Sends Reset': 'Đặt lại Send',
    'Separate Channels': 'Tách các Channel riêng',
    'Separate Pitches': 'Tách riêng các cao độ',
    'Some files could not be imported.': 'Một số file không thể import.',

    # ==================================================================
    # reversed, in families whose other half was already right
    # ==================================================================
    'Smart Controls': 'Smart Control',
    'Sound References': 'Sound Reference',
    'Sound References...': 'Sound Reference...',
    'Sound Slot': 'Sound Slot',
    'Sound Slots': 'Các Sound Slot',
    'SoundSlot Colors': 'Màu Sound Slot',
    'Source Events': 'Source Event',
    'Source Tracks': 'Source Track',
    'Source: Cue Sends': 'Source: Cue Sends',
    'Source: External Inputs': 'Source: External Input',
    'Source: Monitor Mix': 'Source: Monitor Mix',
    'Sources': 'Các nguồn',
    'Smallest Track Height To Show Data':
        'Chiều cao Track nhỏ nhất để hiện dữ liệu',
    'Snapshot Notes': 'Ghi chú Snapshot',
    'Snapshots': 'Các Snapshot',
    'Snapshots[MixConsole]': 'Các Snapshot',
    'Slurs': 'Các dấu luyến',
    'Solo All Clips': 'Solo tất cả Clip',
    'Solo All Parts': 'Solo tất cả Part',
    'Solo Editor Mode: Toggle Modes': 'Chế độ Solo Editor: Đảo chế độ',
    'Solo Front Channels': 'Solo các Channel trước',
    'Solo Input': 'Solo đầu vào',
    'Solo Instrument (Requires Drum Map)': 'Solo Instrument (yêu cầu Drum Map)',
    'Solo Left and Right Channels': 'Solo Channel Trái và Phải',
    'Solo Surround Channels': 'Solo các Channel Surround',
    'Sort By Vendor': 'Sắp xếp theo nhà cung cấp',
    'Sort Lanes by Pitch': 'Sắp xếp Lane theo cao độ',
    'Sort Step Lanes': 'Sắp xếp các Step Lane',
    'Updating Files': 'Đang cập nhật các file',
    'Updating Image on "%s"': 'Đang cập nhật hình ảnh trên "%s"',
    'Updating Plug-in Information': 'Đang cập nhật thông tin Plug-in',
    'Unlock Events': 'Mở khóa các Event',
    'Unmute Input': 'Bỏ Mute đầu vào',
    'Unreferenced Files:': 'Các file không được tham chiếu:',
    'Unsolo Input': 'Bỏ Solo đầu vào',
    'Unstressed': 'Không nhấn mạnh',
    'Unsupported Architecture': 'Kiến trúc không được hỗ trợ',
    'Until End': 'Cho tới cuối',
    'Untitled Color': 'Màu chưa đặt tên',
    'Updating Project Information...': 'Đang ghi thông tin Project...',
    'Writing MIDI Devices': 'Đang ghi MIDI Device',
    'Windows: Next Mixer': 'Cửa sổ: MixConsole tiếp theo',
    'Workspaces': 'Các Workspace',
    'Write for All Tracks': 'Ghi cho tất cả Track',

    # ==================================================================
    # the "Update ..." and "Use ..." families
    # ==================================================================
    'Update Configuration': 'Cập nhật cấu hình',
    'Update Display': 'Cập nhật hiển thị',
    'Update Favorite': 'Cập nhật mục yêu thích',
    'Update Image': 'Cập nhật hình ảnh',
    'Update Information for All Plug-ins':
        'Cập nhật thông tin cho tất cả Plug-in',
    'Update Proxies Error': 'Lỗi khi cập nhật Proxies',
    'Update Results': 'Cập nhật kết quả',
    'Update Selected Snapshot': 'Cập nhật Snapshot đã chọn',
    'Update Visibility Configuration': 'Cập nhật cấu hình hiển thị',
    'Use 9 Pin Device 1 for Machine Control':
        'Dùng thiết bị 9 chân 1 cho Machine Control',
    'Use 9 Pin Device 2 for Machine Control':
        'Dùng thiết bị 9 chân 2 cho Machine Control',
    'Use Bars & Beats Count-In': 'Dùng đếm nhịp theo Bar & Nhịp',
    'Use Chain Name': 'Dùng tên Chain',
    'Use Count': 'Dùng số đếm',
    'Use Custom Name': 'Dùng tên tùy chỉnh',
    'Use Custom Sounds': 'Dùng âm thanh tùy chỉnh',
    'Use Defaults': 'Dùng mặc định',
    'Use Existing Voices': 'Dùng các bè hiện có',
    'Use Global Settings': 'Dùng cài đặt toàn cục',
    'Use Hermode Tuning for Analysis': 'Dùng Hermode Tuning cho việc phân tích',
    'Use Inserts While Scrubbing': 'Dùng Insert khi Scrub',
    'Use Locators': 'Dùng các Locator',
    'Use Main Value': 'Dùng giá trị chính',
    'Use Monitored Tracks': 'Dùng các Track đang Monitor',
    'Use Mouse Wheel for Event Volume and Fades':
        'Dùng con lăn chuột cho âm lượng và Fade của Event',
    'Use Precount': 'Dùng phần đếm trước',
    'Use Previous Track Color': 'Dùng màu Track trước đó',
    'Upper Switch': 'Công tắc trên',
    'Write Protection': 'Bảo vệ ghi',
    'Write Automation On/Off': 'Bật/Tắt ghi Automation',
    'Write protected - maintain a personal copy?':
        'Bị bảo vệ ghi - duy trì một bản sao cá nhân?',

    # ==================================================================
    # a fourth "read as a different word": Word Clock is not "word"
    # ==================================================================
    'Word Clock Output': 'Đầu ra Word Clock',
    'You can join': 'Bạn có thể tham gia',
    'White Keys': 'Phím trắng',
    'White Diamond Noteheads': 'Đầu nốt Diamond trắng',
    'Wide Diamond Noteheads': 'Đầu nốt hình thoi rộng',
    'Whole Tone': 'Toàn cung',
    'Whistle': 'Còi',
    'Zones': 'Các Zone',
    'Solfege': 'Solfège',
    'by touching it on your controller':
        'bằng cách chạm vào nó trên Controller của bạn',
    '[Alt + click] to reset all meters':
        '[Alt + click] để đặt lại tất cả Meter',
    'Yamaha Category Name': 'Tên danh mục Yamaha',
    'Yamaha Category Status': 'Trạng thái danh mục Yamaha',
    'Yamaha Fingering Number': 'Số ngón Yamaha',
    'Yamaha Function Status': 'Trạng thái chức năng Yamaha',
    'Yamaha Guitar Track': 'Track Guitar Yamaha',
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
    print(f'  {k[:58]!r}\n      {vi.get(k, "")[:62]!r}\n   -> {v!r}')

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
