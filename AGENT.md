# AGENT.md — Quy tắc bắt buộc khi dịch Cubase 15

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ.

Nguồn chuẩn hoá: `keys/all_strings.tsv` (10.737 cặp key ⇄ tiếng Anh).

---

## 1. Kiểu dịch: LAI ANH - VIỆT TỰ NHIÊN (Vietglish chuyên ngành DAW)

Dịch theo cách làm nhạc, phòng thu Việt Nam giao tiếp thực tế:

- **Động từ, thao tác, trạng thái, giao diện**: Việt hoá ngắn gọn, chuẩn xác
  (`Thêm`, `Xóa`, `Gỡ bỏ`, `Nhân bản`, `Sửa`, `Mở`, `Lưu`, `Bật`, `Tắt`, `Ẩn`,
  `Hiện`, `Chọn`, `Tới`, `Đảo ngược`).
- **Thuật ngữ chuyên môn âm thanh & DAW**: **giữ nguyên tiếng Anh**, ghép tự
  nhiên vào ngữ pháp tiếng Việt.

### TUYỆT ĐỐI KHÔNG

- **KHÔNG mở ngoặc chú thích ở cuối**: `Thêm track âm thanh (Add Audio Tracks)` là
  **SAI** — nút bấm và menu bị tràn chữ, trông như từ điển. Đúng là `Thêm Audio Track`.
  Ngoại lệ duy nhất: **key gốc đã có ngoặc** thì được giữ, và khi đó dịch nội dung
  trong ngoặc sang tiếng Việt — `1/8 Note (Quaver)` → `Note 1/8, nốt móc đơn`.
- **KHÔNG dịch thuần Việt thuật ngữ chuẩn**:
  `Automation` → ~~Tự động hóa~~ · `Bounce` → ~~Nảy~~ · `Track` → ~~Rãnh~~ ·
  `Clip` → ~~Đoạn cắt~~ · `Freeze` → ~~Đóng băng~~ · `Quantize` → ~~Lượng tử hóa~~

---

## 2. THỨ TỪ TỪ — lỗi phổ biến nhất, đã sửa hơn 200 chuỗi

Tiếng Việt và tiếng Anh đặt danh từ chính **khác vị trí**. Đây là nguồn hỏng lớn
nhất trong bản dịch, nên kiểm tra trước mọi thứ khác.

| | Sai | Đúng |
|---|---|---|
| Tiếng Anh: danh từ chính **cuối** | `Bus Output`, `Track Analyzer`, `Preset Factory`, `Marker Warp`, `Channel Input` | `Output Bus`, `Analyzer Track`, `Factory Preset`, `Warp Marker`, `Input Channel` |
| Tiếng Việt: danh từ chính **trước** | `Channel Tên`, `Note Số` | `Tên Channel`, `Số Note` |
| Danh từ theo động từ Việt | `Gain EQ Band 1`, `Send Common Reverb` | `Gain của EQ Band 1`, `Common Reverb Send` |

- Giữ nguyên vị trí của danh từ chính so với key gốc.
- Với danh từ HLV + tiếng Anh (`Tên Channel`, `Số Note`, `Chế độ Value`):
  danh từ HLV đứng trước, tiếng Anh đứng sau. Đây là dạng **đúng**.
- Danh từ HLV + danh từ HLV: dùng `của` hoặc ghép trực tiếp
  (`Volume của Channel`, `Kích thước Channel Strip`).

### Không lặp giới từ

`to` không phải lúc nào cũng là `vào`. Nếu câu đã có động từ thì `vào` là thừa:

| Sai | Đúng |
|---|---|
| `Go vào Input` | `Tới đầu vào` |
| `Map vào Track Chord` | `Gán vào Chord Track` |
| `Next Chain Step\nDùng [ALT] + Click vào jump vào last chain step` | `... để nhảy tới chain step cuối cùng` |

`Thêm ... vào ...`, `Chèn ... vào ...`, `Map ... vào ...` là **đúng**.

### Giới từ chuyển đổi

`to` khi chuyển đổi nghĩa là `sang`, không phải `vào`:
`Convert Tracks: Mono to Multi-Channel` → `Chuyển đổi Track: Mono **sang** Multi-Channel`.

---

## 3. Bảng thuật ngữ DAW (BẮT BUỘC GIỮ TIẾNG ANH)

| Thuật ngữ | Cách dùng trong câu tiếng Việt |
|---|---|
| Track | `Thêm Audio Track`, `Xóa Track đã chọn`, `Track Version mới` |
| Channel / Bus / FX / Group / VCA | `Màu Channel`, `Độ trễ Channel`, `Thêm Group Bus`, `FX Channel`, `VCA Fader` |
| Insert / Send / Slot | `Sửa Insert`, `Bật Send`, `Send Slot`, `Insert Slot` |
| Fader / Pan / Solo / Mute | `Mute Track`, `Solo Channel`, `Fader MIDI`, `Pan tiếng nhấp` |
| Meter / Metering | `Mức Meter`, `Metering Channel` |
| Metronome / Click | `Bật Click Metronome`, `Cài đặt Metronome`, `Âm thanh Click` |
| Marker / Locator | `Thêm Cycle Marker`, `Tới Left Locator`, `Cài đặt Marker` |
| Automation | `Ẩn tất cả Automation`, `Sửa Automation`, `Automation Track` |
| Clip / Event / Part / Pool | `Chọn tất cả Event`, `File trong Pool`, `Active Clip` |
| Quantize / Snap / Grid | `Áp dụng Quantize`, `Snap tới Zero`, `Cài đặt Grid` |
| Bounce / Render / Freeze / Warp | `Bounce vùng chọn`, `Render in Place`, `Freeze Track` |
| Velocity / Pitch / Note / Chord | `Fixed Velocity`, `Sửa Pitch`, `Xóa Note trùng`, `Chord Track` |
| Tempo / Timecode / Bar / Beat | `Đặt Tempo`, `Tap Tempo`, `Số Bar`, `1 Bar` |
| Fade / Punch | `Fade In`, `Punch In`, `Punch Out` |
| Buffer / Latency / Sample Rate | `Audio Buffer`, `Độ trễ Channel`, `Sample Rate` |
| ASIO / VST / Plug-in / Preset | `Thiết bị Audio ASIO`, `Quản lý Plug-in`, `Preset âm thanh` |
| MixConsole / Inspector / Zone | `Mở MixConsole`, `Lower Zone` |
| Export / Import | `Export Audio Mixdown`, `Import MIDI` |
| Arranger / Chain / Step | `Arranger Track`, `Arranger Chain`, `Chain Step` |
| Lane / Pattern / Expression | `Velocity Lane`, `Pattern`, `Note Expression` |
| Voicing / Tension / Articulation | `Adaptive Voicing`, `Thêm Tension`, `Articulation đã chọn` |
| Layout / Map / Mapping / Script | `Mở Layout`, `Key Map`, `MIDI Remote Mapping`, `Script` |
| Machine Control / Talkback / Cue | `Machine Control`, `Bật Talkback`, `Cue Send` |
| Chords / Symbols / Signature | `Chord Symbols`, `Time Signature` |

> **Lưu ý**: `nhịp độ`, `chu kỳ`, `cột nhịp` đều **sai** với key Cubase.
> Một measure là `Bar`, không phải `Cột nhịp` (nghĩa là *cột*).

---

## 4. Thuật ngữ bàn nhạc (Score Editor) — dùng tiếng Việt

Bàn nhạc không nằm trong bảng §3, nên dùng thuật ngữ âm nhạc tiếng Việt. Phải
**thống nhất**, không trộn hai kiểu trong cùng một khái niệm.

| Tiếng Anh | Tiếng Việt |
|---|---|
| Staff / Stave | khuông nhạc |
| Clef | khóa nhạc |
| Rest | dấu lặng |
| Beam | đuôi nốt |
| Stem / Stemlet | thân nốt / thân nốt nhỏ |
| Barline | vạch nhịp |
| Key Signature | hóa biểu |
| Time Signature | số chỉ nhịp |
| Voice | bè |
| Ledger Line | dòng kẻ |
| Accidental | dấu hóa |
| Note (trường độ) | **giữ `Note`** → `Note 1/8` |
| Rhythm Dot | dấu chấm nhịp |
| Slash (gạch nhịp) | gạch nhịp |

**`System` là từ ngữ cảnh — phải tra từng chuỗi:**

- Trong Score Editor = một dòng nhạc → **`dòng nhạc`**
  (`Above System` → `Phía trên dòng nhạc`, `Inter-System Gap` → `Khoảng cách giữa các dòng nhạc`)
- Ngoài Score Editor = hệ điều hành → **`hệ thống`**
  (`System Link`, `File Hệ thống`, `khởi động lại hệ thống`)

**Tương tự, `Bar` cũng theo ngữ cảnh:**

- Ô nhịp trong ký âm → **`Bar`** (`1 Bar`, `nửa Bar`)
- Thanh giao diện → **`thanh`** (`Address Bar` → `Thanh địa chỉ`, `Menu Bar`, `Status Bar`)

**Các từ HLV không nằm trong §3 cũng giữ nguyên bên HLV** vì đọc tự nhiên hơn và
đã là đa số trong bản dịch: `con trỏ`, `bè`, `số chỉ nhịp`, `phát lại`, `hợp âm`,
`khuông nhạc`, `dấu lặng`, `đuôi nốt`, `khóa nhạc`.

### Trường độ nốt — số đứng trước, KHÔNG đảo

`16th` là **trường độ**, nên viết `Note 1/16`, không phải `Móc 16`. Lô tự động
từng đảo thứ tự 4 chuỗi theo đúng kiểu §2:

| Sai | Đúng |
|---|---|
| `Móc 8` · `Móc 16` · `Móc 32` · `Móc 64` | `Note 1/8` · `Note 1/16` · `Note 1/32` · `Note 1/64` |

Tương tự, số đứng **trước** danh từ: `100 Events` → `100 Event`, không phải
`Event 100`; `%d Channels` → `%d Channel`, không phải `Channel %d`.

### Không đảo hai thuật ngữ dễ lẫn của bàn nhạc

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Beam | **đuôi nốt** | thanh nối ngang các nốt |
| Stem | **thân nốt** | que nối dọc |

`Flip Stems` từng dịch thành `Lật Đuôi nốt` — lấy nhầm của Beam. Cùng kiểu:
`Accidental` là **dấu hóa**, không phải `dấu nhấn` (dấu nhấn là dấu nhấn trong từ);
`Flat` là **giảm** (nửa tông), không phải `phẳng`;
`Multi` (multi-timbral) là **bội**, không phải `đa kênh` (đa kênh là multichannel).

### Không dịch nửa vế

`Color Space` → `Màu Khoảng trống` đọc thành "khoảng trống". Chính key con của nó,
`Color Space Management`, lại đúng: `Quản lý không gian màu`.

Một nhãn hoặc một câu phải **dịch trọn** hoặc **giữ trọn bằng tiếng Anh** — không
để nửa. `Clear All` đã dịch thì `Clear Recent Paths` phải theo; `Multi Track`
giữ tiếng Anh thì `Multi` cũng phải nhất quán theo nghĩa của nó.

### Thứ tự `%s`

`%s` đi **trước** danh từ HLV: `%s Control` → `Điều khiển %s`, không phải
`%s Điều khiển`.

### `Command` và `Key Command` — hai từ, hai nghĩa

| Tiếng Anh | Tiếng Việt | Ví dụ |
|---|---|---|
| Key Command | **phím tắt** | `Assigned Key Commands` → `Phím tắt đã gán` · `Customized Key Commands` → `Phím tắt tùy chỉnh` · `Unassigned Key Commands` → `Phím tắt chưa gán` |
| Command | **lệnh** | `Basic Commands` → `Lệnh cơ bản` · `Other Commands` → `Lệnh khác` |

**Số ít và số nhiều phải giống nhau.** `Command` (số ít) từng để nguyên tiếng Anh
trong khi `Commands` (số nhiều) dịch là `Lệnh` — đúng kiểu "nửa chừng có một hệ
thống riêng" mà §3 cấm. Cũng không viết `Lệnh Assigned Key`: đó là §2 áp vào
một cụm đã dịch sẵn.

---

## 5. Thao tác giao diện cơ bản

| Thao tác tiếng Anh | Dịch tự nhiên | Ví dụ |
|---|---|---|
| Add... | Thêm... | `Add Track...` → `Thêm Track...` |
| Remove... | Gỡ bỏ... / Xóa... | `Remove Selected Tracks` → `Xóa Track đã chọn` |
| Duplicate... | Nhân bản... | `Duplicate Version` → `Nhân bản Version` |
| Edit... | Sửa... | `Edit Automation` → `Sửa Automation` |
| Select... | Chọn... | `Select All Events` → `Chọn tất cả Event` |
| Locate / Go to... | Tới... | `Go to Left Locator` → `Tới Left Locator` |
| Hide... / Show... | Ẩn... / Hiện... | `Hide All Automation` → `Ẩn tất cả Automation` |
| Export... / Import... | Export... / Import... | `Export Audio Mixdown` → `Export Audio Mixdown` |
| New... | ... mới / Tạo... | `New Project...` → `Project mới...` |
| Save As... | Lưu thành... | `Save As...` → `Lưu thành...` |
| Preferences... | Tùy chọn... | `Preferences...` → `Tùy chọn...` |
| Key Commands... | Phím tắt... | `Key Commands...` → `Phím tắt...` |
| Invert Selection | Đảo ngược vùng chọn | `Invert Selection` → `Đảo ngược vùng chọn` |

### Danh từ tính

Tính từ phải dịch, không để lại tiếng Anh:
`Độ dài Fixed` → `Độ dài cố định` · `Tên Full` → `Tên đầy đủ` ·
`Thêm Steps Randomly` → `Thêm Step ngẫu nhiên` · `Close Threshold` → `Ngưỡng đóng`.

### Không làm mất câu

Bản dịch phải **giữ trọn** nghĩa. Ba kiểu hay mất:

- mất vế cuối — `This option deletes the preferences ... This operation cannot
  be undone.` bị dịch còn `... sẽ bị gỡ bỏ.`
- mất cả đoạn — hộp thoại network interfaces chỉ còn 2 câu đầu trong 6 câu
- mất chủ thể — `Activate/Deactivate Focused Object` → `Bật/Tắt`

### Câu

- Viết lại **cả câu**, không thay từ rời. Câu tiếng Anh còn sót là lỗi, kể cả khi
  mọi từ đều là thuật ngữ DAW:
  `Not enough disk space available cho this operation` → `Không đủ dung lượng đĩa cho thao tác này.`
- Giữ dấu kết câu của key (`?` `!` `.`) và dấu ba chấm.
- Động từ sau `Không thể` phải viết thường: `Không thể tạo file`, không phải
  `Không thể Tạo file` — viết hoa giữa câu nghĩa là danh từ riêng.
- Văn bản trong ngoặc kép `'` `"` là tên tính năng hoặc giá trị mẫu: giữ nguyên.
- **Câu phải có chủ thể.** `Đạt giới hạn 2GB của định dạng file OMF, ...` thiếu
  chủ ngữ vì tiếng Anh bắt đầu bằng gerund. Viết `Đã đạt giới hạn ...`.

### Dịch nghĩa, không dịch từ

`interpret` một file CSV là **phân tích**, không phải `diễn giải`. `chữ` là
"letter", không phải "content". `emphasis` trong nhạc là **làm nổi bật**, không
phải `nhấn trọng âm`. Một số từ HLV dịch vội thành từ khác nghĩa:

| Sai | Đúng |
|---|---|
| `Aeolian (thứ tự nhiên)` | `Aeolian (thứ sáu tự nhiên)` |
| `ít chữ hơn ngưỡng` | `ít nội dung hơn ngưỡng` |
| `nhấn trọng âm Pattern` | `làm nổi bật Pattern` |
| `đo Loudness cổng thoại` | `đo Loudness theo hội thoại` |
| `Tôn trọng trường độ tối đa` | `Tuân thủ trường độ tối đa` |
| `Preset thời gian thực thay thế` | `Preset thời gian thực thay vì` |
| `dịch vào vùng âm` | `dịch sang vùng âm` |

`Aeolian` là bậc sáu của thang ngũ cung — viết `thứ sáu` mới đúng. Đọc như tên
thang, `thứ tự` ("thứ tự nhiên") lại rất thông dụng nên không bộ dò nào bắt được.

---

## 6. Placeholders (%s, %d, %i, %.3f...)

Giữ nguyên văn, không đổi thứ tự, không dịch nhầm vào tên biến.
Ví dụ: `Add %d Audio Tracks` → `Thêm %d Audio Track`.

### Dấu câu không được di chuyển

Dấu `:` `?` `!` `.` phải đứng đúng chỗ tiếng Anh đặt. Bốn lỗi thật đã qua:

| Tiếng Anh | Đã dịch sai | Đúng |
|---|---|---|
| `CC: Modulation` | `CC Modulation` | `CC: Modulation` |
| `Ch.` | `Ch` | `Ch.` |
| `Checked Chains ....` | `Checked Chains...` | `Checked Chains ....` |
| `Create new Project ?` | `Tạo ? Project` | `Tạo Project mới ?` |
| `Database creation failed.` | `Tạo cơ sở dữ liệu thất bại.` | `Không thể tạo cơ sở dữ liệu.` |

Dấu `?` nhảy vào giữa vế (`Tạo ? Project`) là hỏng chức năng: đọc lên là
"tạo cái gì đó không?". Và nếu tiếng Anh có khoảng trắng trước dấu (` ?`, ` !`)
thì giữ khoảng trắng đó, dù tiếng Việt không quen.

### Từ mang nghĩa không được rơi

`Create New Chain` → `Tạo Chain` là mất chữ **New** trong khi anh em giữ nguyên
(`Create New Folder`, `Create New MIDI Device`, `Create New Version`). Cùng kiểu:

```
Date + Time   ->  Thời gian Date +
Date / Time   ->  Thời gian Date /
```

Giá trị sau đó **không còn nói xem đang tạo cái gì** — chỉ còn "thời gian" rồi
một dấu cộng/trừ lơ lửng.

### Một họ nhãn phải giống nhau

| Họ | Lệch |
|---|---|
| `Controller Lane Setup` vs `Controller Lane Setup 1..16` | `Cài đặt` vs `Thiết lập` |
| `Deactivate All Mute/Solo/Solo States/Listen States` | ba cái `Hủy` (huỷ = cancel), một cái `Tắt` |
| `Delete Automation Spikes` vs `... of Selected Tracks` | `đỉnh nhọn` vs `gai` |
| `Dark Red/Blue/Yellow` vs `Dark Green/Magenta/Orange` | ba cái dịch, ba cái giữ tiếng Anh |
| `Bypass: EQs/Inserts/Modulators/Sends` | mất dấu `:` ở một cái, mất `s` ở ba cái |

Tìm họ bằng cách gom các key có cùng tiền tố rồi so **từng từ một**. Sửa một
cái trong họ mà không sửa anh em chỉ là thêm một biến thể nữa.

### Khung tiếng Việt bọc một mệnh đề tiếng Anh

Lớp lớn nhất mà **không bộ dò nào bắt được**: dịch từng từ theo thứ tự, xong
không ai đọc lại. Nhãn ra tiếng Anh trần với khung tiếng Việt:

```
Do you want to continue recording?   ->  Bạn có muốn continue recording không?
Do you want to copy video files too? ->  Bạn có muốn Sao chép video files too ...?
Device failed to open!                ->  Device failed vào open!
Divide by 2                           ->  Divide theo 2
Delete later events                   ->  Xóa later events
Displays follow locating device       ->  Thiết bị Displays follow locating
Different tracks                      ->  Different tracks
```

Bộ dò "rò rỉ tiếng Anh" **không** báo, vì từng từ nó thấy đều là từ nó mong
đợi: `Bạn có muốn` là tiếng Việt, `continue` là tiếng Anh, cả hai đều đúng ở
chỗ của nó. Lớp lỗi này chỉ lộ ra khi đọc.

Hai kiểu nặng nhất:

- **Mệnh đề tiếng Anh nằm nguyên trong câu**: `continue recording`, `video
  files too`, `failed vào open`, `later events`. Xóa hết, dịch lại.
- **Câu bị tháo rời**: `Thiết bị Displays follow locating` — câu đã bị bung,
  phần còn lại là một thiết bị bị "theo" bởi hai động từ tiếng Anh, không
  nói được điều gì. Cùng dạng:
  `Double-click opens Editor in Lower Zone` → `Editor Double-click opens
  trong Lower Zone`.

### Nhãn trường nhập — từ cần gõ phải ở cuối

`Enter Custom Name` → `Tên Enter Custom` đọc thành "tên, nhập, tùy chỉnh": từ
người dùng phải gõ (`Custom`) nằm giữa câu bảo họ gõ. Cùng lỗi ở
`Enter Preset Name` → `Tên Enter Preset`, `Enter Model Name` → `Tên Enter
Model`, `Enter Punch In Position` → `Nhập Punch trong Position`.

### Một từ tiếng Anh bị đọc thành từ tiếng Anh khác

Nguy hiểm nhất vì **cả hai đều hợp lệ**, nên bộ dò nào cũng im:

| Tiếng Anh | Đọc nhầm thành | Đúng là | Đã dịch sai thành |
|---|---|---|---|
| `Half (I-V-I)` | Flat | **nửa** | `Giảm (I-V-I)` |
| `Ext. %d` | Extend | **External** | `Mở rộng %d` |
| `Group 1` | (động từ) | danh từ `nhóm` | `Gộp nhóm 1` |
| `Multi` | Multichannel | **bội** (multi-timbral) | `Đa kênh` |
| `Flatten` | Flat | làm phẳng | `Làm phẳng` ✅ |
| `Range` | Row | dải/vùng | `vùng` ✅ |

`Half` và `Flat` lệch nhau **một ký tự**, và bản dịch đang dùng chung một giá
trị `Giảm` cho cả hai. Khi sửa, tra **từng từ** xem nó là danh từ, động từ, tính
từ hay viết tắt — hai từ có thể giống nhau 26/27 ký tự mà nghĩa khác hẳn.

### `Group` là danh từ, `Gộp` là động từ

Chín nhãn trong bản dịch cũ ghi `Group ...` thành `Gộp nhóm ...`:
`Group`, `Group 1..4`, `Group Track`, `Group Tracks`, `Group Channels`,
`Group Editing`, `Group Track to Selected Tracks...`.

Tất cả đều là **danh từ** — tên của một đối tượng. `Gộp nhóm Track` bảo người
dùng *hợp nhất*, tức một hành động khác hẳn. Chỗ duy nhất "Group" thật sự là
động từ thì đã đúng sẵn (`Add Group Track` → `Thêm Group Track`) — nên dạng
danh từ chưa bao giờ được đối chiếu với nó.

Cùng kiểu: `Event End` → `Event Kết thúc`, `Event Start` → `Event Bắt đầu`,
`Event Display` → `Event Hiển thị`, `Estimated Pitch` → `Pitch Estimated`.

### `Deactivate` không phải `Hủy`

`Hủy` là **cancel**, huỷ bỏ việc đang làm. `Deactivate` là **tắt**.
`Deactivate All Mute States` → `Hủy tất cả trạng thái Mute` sai; ba anh em
(`Solo`, `Solo States`, `Listen States`) đã dùng `Tắt`.

---

## 7. Quy trình kiểm tra

Chạy theo thứ tự, dừng ngay khi một bước báo lỗi:

```powershell
python tools\merge_maps.py            # gộp batch -> translations/vi.json
python tools\check_style.py           # 3 luật cứng của AGENT.md
python tools\audit_leak.py            # từ chức năng tiếng Anh lọt vào câu
python tools\find_leftover_english.py # câu tiếng Anh chưa dịch
python tools\audit_quality.py         # thuật ngữ xung đột + trật tự từ
python tools\audit_fragments.py       # từ tiếng Anh lọt lẻ trong câu
python tools\audit_readability.py     # lặp từ, giới từ thừa, ngoặc rỗng
python tools\check_duplicate_keys.py  # nhóm key gần trùng lệch cách diễn đạt
python tools\fix_mojibake.py          # ký tự thay thế U+FFFD
python tools\build.py                 # sinh build/translation_vi.xml + validate
pwsh -File scripts\install.ps1 -Action install
```

Ba luật cứng của `check_style.py`:
1. Cấm ngoặc chú thích ở cuối, **trừ khi key gốc đã có ngoặc**.
2. Cấm dịch thuần Việt các thuật ngữ ở §1.
3. Placeholder phải khớp với key.

### Sửa bản dịch

Chỉ sửa chuỗi có **key tồn tại thật** trong `keys/all_strings.tsv`. Bảng quyết định
nằm trong `tools/glossary_*.py` và được `tools/apply_glossary.py` áp dụng — script này
từ chối ghi nếu key không tồn tại, placeholder lệch, hoặc giá trị chứa U+FFFD.

Đợt đọc tay thì đặt bảng vào `tools/fix_reading<N>.py`. **Mỗi đợt một file riêng,
không chép bảng của đợt trước vào.** Đây chính là cái bẫy đã làm hỏng hai
quyết định:

- `glossary_readthrough.py` giữ `'Command': 'Command'` và vì chạy cuối nên xoá
  `Lệnh` của `fix_reading4.py` **mỗi lần chạy**.
- `fix_reading14.py` ban đầu liệt kê lại 98 key của `fix_reading13.py`. Không
  sai hôm đó, nhưng nếu sau này có quyết định tốt hơn cho `Add Up` thì đợt 14
  sẽ ghi đè ngược lại đợt 15. Bảng cũ **là** một lệnh ghi đè.

Script tự báo `NOT IN CUBASE` cho key không tồn tại — nhưng chỉ báo được sau khi
đã viết bảng, nên cứ kiểm `NOT IN CUBASE` **trước** khi `--write`.

### Key không phải lúc nào cũng bằng tiếng Anh

Cột 1 (`key`) và cột 2 (English) của `keys/all_strings.tsv` khác nhau ở nhiều key:

| key | English |
|---|---|
| `AppKey[Key]` | `Menu` |
| `Assume Skipping` | `Process Existing Clip` |
| `BWF Max Momentary Loudness` | `BWF Max. Momentary Loudness` |
| `Check Files` | `Find Missing Files` |
| `Delete Tool` | `Erase Tool` |
| `Add Device (from a popup list of available devices)` | `... pop-up list ...` |

Bảng quyết định khóa theo **key**. Trước đây `read_short.py` in ra cột English
nên tôi viết bảng theo English rồi script báo 2 key "không có trong Cubase" —
và suýt sửa nhầm hai chuỗi đang đúng. Nay `read_short.py` in thêm
`<key: ...>` cho mọi key khác English.

Marker `[RM]`, `[Score View Option]`, `[Key]`, `[vocal]` là **marker riêng của
Cubase**, nằm trong key. Giữ nguyên, không phải rò rỉ tiếng Anh.

### Đọc tay vẫn là bước cuối

Các bộ dò bắt được lỗi **có mẫu**. Lỗi kiểu đảo trong câu dài, cách diễn đạt
khó đọc, mất câu, hay từ dịch sai nghĩa chỉ lộ ra khi đọc thật. Đợt gần nhất,
đọc tay 1.150 chuỗi dài theo 5 miền tìm được 201 chuỗi — trong đó có lớp lớn
mà **không bộ dò nào bắt được**:

- `Activate/Deactivate Focused Object` → `Bật/Tắt` (mất chủ thể)
- một hộp thoại 6 câu còn lại 2 câu
- `Aeolian (nat. minor)` → `Aeolian (thứ tự nhiên)` (sai nghĩa)

Công cụ để đọc: `python tools/read_long.py <miền> <bắt đầu> <số>`, in ra cặp
English / tiếng Việt. `python tools/read_short.py <miền> <bắt đầu> <số>` cho
nhãn ngắn. `python tools/sample_domain.py <miền> <bắt đầu> <số>` cho mọi giá
trị kể cả nhãn ngắn.

### Ba lần rule báo động giả

Ghi lại để không lặp lại:

1. `Tên Channel`, `Số Note`, `Chế độ Value` trông như đảo nhưng **đúng** —
   tiếng Việt đặt danh từ trước. 201 chuỗi phải giữ nguyên.
2. `gán vào`, `chuyển vào` là cách nói tự nhiên, cần `vào` để dẫn tân ngữ.
   Rule "vào thừa" bắt nhầm 14 chuỗi đúng rồi phải siết lại.
3. `lặng` là một từ riêng bên trong `dấu lặng`; khớp không ràng giới từ thì
   `audit_quality` báo xung đột cho **mọi** chuỗi đúng. Tương tự `Hóa biểu` /
   `hóa biểu` chỉ khác hoa-thường, và `Over` trong `Cross-Over` khớp `\b` sau
   dấu gạch nối.

Một bộ dò báo động giả nhiều lần hơn còn tệ hơn không có bộ dò: nó dạy người
đọc bỏ qua báo cáo.
