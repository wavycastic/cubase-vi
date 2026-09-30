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
| Key Signature | **số chỉ nhịp** |
| Time Signature | **số chỉ nhịp** |
| Chord Symbols | hóa biểu |
| Voice | bè |
| Ledger Line | dòng kẻ |
| Accidental | dấu hóa |
| Note (trường độ) | **giữ `Note`** → `Note 1/8` |
| Rhythm Dot | dấu chấm dôi |
| Slash | gạch chéo |

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

**Bài học đắt nhất của toàn bộ dự án.** `Flip Stems` từng dịch thành `Lật Đuôi
nốt` — lấy nhầm của Beam. Đợt 12 sửa nó thành `Lật thân nốt`; đợt 18 sửa
`Force Stems Down`; đợt 23 sửa `Slashes (with stems)`. Cả ba **đúng**.

Và ba key gốc vẫn ghi **ngược**:

```
Stem      ->  Đuôi nốt
Stem Down ->  Đuôi nốt Xuống
Stem Up   ->  Đuôi nốt Lên
```

Tức là bản dịch có **hai tên cho cùng một đối tượng âm nhạc**: `thân nốt` ở
câu, `đuôi nốt` ở danh từ. Sửa 3/5 mà không liệt kê cả họ.

Bài học: **tra bằng TỪ, không tra bằng key.** Ở đây mẫu là chữ `Stem`, không
phải chuỗi cụ thể. Mỗi khi dịch một mệnh đề chứa một thuật ngữ, phải
`grep` thuật ngữ đó trong `translations/vi.json` và sửa **mọi** chỗ khớp.

Cùng kiểu: `Accidental` là **dấu hóa**, không phải `dấu nhấn` (dấu nhấn là dấu
nhấn trong từ); `Flat` là **giảm** (nửa tông), không phải `phẳng`;
`Multi` (multi-timbral) là **bội**, không phải `đa kênh` (đa kênh là
multichannel).

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

### Ngoặc và động từ không được rơi

Cùng lớp với mất dấu `:` ở đợt 13, nhưng tệ hơn — chỉ còn **một** ngoặc:

```
Select Preset (rename using [Alt + click])  ->  Chọn Preset (đổi tên bằng [Alt + click]
```

Key có hai cặp ngoặc lồng nhau, giá trị chỉ còn một. Và:

```
Select Tool (Press [ALT] to draw events)  ->  Công cụ chọn (Nhấn [ALT] để vẽ Event)
```

Không còn chữ "Select" nào trong tiếng Việt — nhãn bắt đầu bằng danh từ nên đọc
thành "công cụ chọn", tức là **một menu khác**.

### `No.` là *số* — quyết định rồi thì phải áp cho hết

`No.` là viết tắt của **Number**, không phải phủ định. Trong khoảng 60 nhãn mở
đầu bằng `No`, bốn cái đã đẩy chữ `No` ra cuối như danh từ:

```
No Parameter   ->  Tham số No        ← "tham số số"
No Section     ->  Phần No           ← "phần số"
No Status Info ->  Thông tin No Status
No. of Frets  ->  No. của Frets
```

Cùng lớp với `Group` → `Gộp nhóm`: chữ bị coi là danh từ rồi đẩy hết xuống
cuối. Đây là lỗi đảo thứ tự từ ở dạng ngắn, chỉ lộ ra khi đọc.

**Đã dính ba lần.** Đợt 19 sửa `No. of Frets`, đợt 22 sửa `Scene No.`, đợt 24
sửa `Take No.` — mỗi lần một chuỗi. Sau đợt 22 tôi đã viết vào đây "hãy tra
bằng mẫu chứ không tra bằng key" rồi lại không làm. Ba lần là đủ để biết luật
này phải **thực thi**, không chỉ viết ra.

### `Version` giữ tiếng Anh — nhưng **chỉ ở nhãn**

43 nhãn chứa `Version`. 32 cái đã dùng `Version`, 11 cái dùng `phiên bản`:

```
Version          ->  Phiên bản
Track Versions   ->  Các phiên bản Track
VST Version      ->  VST Phiên bản        (còn sai thứ tự)
Software Version ->  Phần mềm Version     (nửa nọ nửa kia)
```

Nhất thống theo `Version` — vừa là đa số, vừa đúng luật "giữ thuật ngữ DAW bằng
tiếng Anh".

**Nhưng chạm tới câu văn thì dừng lại.** 31 câu chứa `phiên bản` đang **đúng**:
`mức phiên bản chương trình đã hỗ trợ`, `dữ liệu không được phiên bản chương
trình hỗ trợ` — ở đó `phiên bản` là từ tiếng Việt thông thường, `Version` sẽ
rờ rạc. Nên đây là **11 mục viết tay**, không phải thay thế bằng regex.

`grep` từ khóa rồi sửa từng dòng là cách đúng, nhưng **grep không quyết định**
cái nào sai — nó chỉ chỉ ra chỗ cần nhìn.

Đợt 19 sửa `No. of Frets` → `Số Frets`. Đợt 22 gặp `Scene No.` → `Cảnh Không`
— nghĩa là "cảnh không". Cùng lỗi, cách đã xử lý đúng, **nhưng quyết định không
lan sang chỗ thứ hai**. Một quy tắc đã nghĩ ra thì phải tra cả họ, không chỉ
chỗ vừa gặp.

### `Key Signature` là **số chỉ nhịp** — lỗi này do chính bảng luật sinh ra

Bảng §4 từng ghi `Key Signature | hóa biểu`. Sai. `hóa biểu` là **Chord
Symbols** (dòng chữ tên hợp âm như `Cm7` viết cạnh nốt); `Key Signature` (khoá
bấc) là **số chỉ nhịp** — cùng từ với `Time Signature`.

Lỗi đó đã truyền vào bản dịch ở **8 chuỗi**, một số rất dài:

```
Notes Following a Change of Key Signature That Shows Cancellation Naturals
  ->  Các nốt sau khi đổi hóa biểu có hiện dấu bình hủy bỏ
Key Signatures at Start of System Following First System
  ->  Hóa biểu ở đầu các dòng nhạc sau dòng nhạc đầu tiên
Position Bar Numbers at Start of System After Clef and Key Signature
  ->  Đặt số Bar ở đầu dòng nhạc sau khóa nhạc và hóa biểu
```

Đáng chú ý: đợt 22 và đợt 23 **đã phát hiện** cùng lỗi này ở `SMF: Key
signature` và `Sign.`, đã sửa, và đã ghi vào đây — mà không mở lại bảng §4 để
thấy nó là nguồn. Bản dịch làm đúng theo luật; **luật sai**.

Đây là bài học lớn nhất về tài liệu: một bảng thuật ngữ viết sai không tự báo
lỗi, và mọi lần sửa bản dịch theo nó đều *đúng theo luật*. Khi phát hiện một
lỗi thuật ngữ, phải sửa **cả bản dịch lẫn dòng trong bảng**, và phải `grep` lại
toàn bộ bản dịch theo từ khoá — ở đây là `hóa biểu`.

### `String` đã bị đọc thành **ba** nghĩa khác nhau

| Key | Nghĩa | Đã dịch thành |
|---|---|---|
| `From String`, `Add String Above` | MIDI String (bảng String của Cubase) | `String` |
| `String Tunings`, `Move To String 1..12` | dây đàn | `dây đàn` |
| `Replace Search String` | **chuỗi** tìm kiếm | `dây đàn` ← sai |

Ba lần, ba cách. Cùng một chữ ở ba key khác nhau phải tra **ngữ cảnh**, không
tra bằng từ điển. `String` chỉ đúng khi đứng một mình hoặc đi kèm
`Tuning`/`To String` (ghen dây đàn); đứng trong `Search ...` thì là *chuỗi*.

### `Replace ...` đảo ngữ cảnh, không chỉ đảo từ

```
Replace All Events and Parts      ->  Part Replace All Events and
Replace Recording in Editors      ->  Editor Replace Recording in
Restore Default Setup              ->  Thiết lap Restore Default
Restore Factory Presets           ->  Preset Restore Factory
Reload Track Preset               ->  Preset Reload Track
Resolve Missing Files             ->  File Resolve Missing
Reveal Parameter on Write         ->  Tham so Reveal tren Write
Resulting Video Files             ->  File Resulting Video
```

Cả bảy đều **tháo câu ra rồi ghép ngược**: phần đứng trước của giá trị là phần
đứng sau trong tiếng Anh.

### `Factory` đã có bốn cách dịch

`xuất xưởng` · `từ nhà sản xuất` · `Factory` · và một câu trộn lẫn hai cách.
Nhất thống theo `Factory`.

### `Word` trong `Word Clock` không phải *từ*

```
Word Clock Output  ->  Từ Clock Đầu ra      ← "Từ" = từ văn bản
Word Spacing       ->  Khoảng cách từ      ← đúng, "từ" ở đây là từ văn bản
```

`Word Clock` là **xung đồng hồ** (một xung mỗi giây để thiết bị ngoài đồng bộ),
không phải *word*. Bốn key `Word Clock` kia đều đúng — chỉ key kết thúc bằng
`Output` bị chọn nhầm nghĩa. Cùng lớp với `Replace Search String` →
`Dây đàn` (đợt 29).

### `Duration` là **thời lượng**, không phải `trường độ`

`trường độ` = **ngành/khoa** (một môn học, một khoa). Không phải độ dài.

8 chuỗi từng ghi `trường độ`:

```
- Maximum project duration for sample-precise object positions exceeded
  ->  Đã vượt quá trường độ tối đa của Project cho vị trí đối tượng ...
The Cautionary Accidentals options only apply when the Common Practice
accidental duration rule is used...
  ->  ... khi dùng quy tắc trường độ dấu hóa Thực hành chung
```

Lỗi này vào bản dịch bằng đường rất hiển nhiên: trong bảng cài đặt, `Duration`
đứng cạnh `Field`, và một lượt dịch nào đó đã đọc **hàng xóm** thay vì đọc
**từ**. Cùng cơ chế với `Word Clock` → `Từ`.

Bài học: trong bảng cài đặt, hai từ tiếng Anh đứng cạnh nhau thì **nguy hiểm
gấp đôi** — phải dịch từng từ một, không đọc cả cụm.

### `External` là **thuật ngữ**, không phải `bên ngoài`

`bên ngoài` = *outside* — nghĩa **đối lập**. `External` giữ tiếng Anh ở ~40 key
khác. Bốn câu trong **cùng một bảng** đọc sai:

```
External plug-in is used. Freezing will be done in real time.
  ->  Plug-in bên ngoài đang được dùng. ...
External files will be copied into the working directory!
  ->  Các file bên ngoài sẽ được sao chép vào thư mục làm việc!
External sync cannot be activated because Nuendo is the timecode master.
  ->  Đồng bộ bên ngoài không thể kích hoạt vì Nuendo là Timecode Master.
Do Not Connect Input/Output Busses When Loading External Projects
  ->  ... Khi tải Project bên ngoài
```

Bốn key **cùng họ**, **cùng bảng cài đặt** — nên nếu đã quyết định `External`
thì phải tra **toàn bộ họ**, không dừng ở key đang sửa. Đây là họ thứ sáu
dính lỗi "đọc một từ thành một từ khác".

### Câu tiếng Việt chỉ có **một** từ tiếng Việt

Lớp lỗi riêng của *câu dài* (nhãn ngắn không có):

```
Click 'Start' to scan for unreferenced files
  ->  Click 'Start' vào scan cho unreferenced files
Found participants without master: %s. Try to reconnect?
  ->  Found participants without master: %s. Try vào reconnect?
IP Conflict with client: %s - set client state to logged off.
  ->  IP Conflict với client: %s - set client state vào logged off
```

Từ tiếng Việt duy nhất là **giới từ `vào` / `với`** — thứ không đứng một mình
trong câu. Hai câu kia gần như **thuần tiếng Anh**. `audit_leak` không bắt vì
câu *có* chữ Hán.

Và câu dài hay bị **cắt mất vế sau**:

```
Picks up on the value of the %s function ... This results in smooth value
changes, but requires you to estimate the pickup value.
  ->  ... Điều này giúp thay đổi giá trị mượt mà hơn.
```

Mất đúng vế nói **cái giá** của tính năng. Khi đọc câu dài, phải đếm vế.

### Bảng luật **đúng** mà bản dịch vẫn trôi — `Chord Symbols`

Lỗi `Key Signature | hóa biểu` (mục trên) là **bảng sai**. Đợt 39 tìm ra
**chiều ngược lại**: bảng **đúng**, bản dịch **trôi**.

```
Chord Symbol    ->  Ký hiệu hợp âm
Chord Symbols   ->  Ký hiệu hợp âm
Show Chord Symbols
                 ->  Hiện Chord Symbols          ← cả hai cách trong cùng họ
```

Bảng §4 ghi `Chord Symbols | hóa biểu` từ lâu, nhưng 7 key chọn cách thứ hai.
Không ai đối chiếu chúng với bảng. Tệ hơn: 2 key khác **đưa nhầm từ ngược
chiều** — cụm tiếng Anh `the key signature` lại ra `hóa biểu`.

Nên từ nay: thấy một thuật ngữ trong chuỗi mới thì `grep` **từ đó**, không
grep key. Từ đó có mặt ở cả hai hướng.

### *"hợp âm X với nốt N"* ≠ *"hợp âm X cấp N"* — 16 key sai nhạc lý

```
Apply major chord with a 7 to selection
  ->  Áp dụng hợp âm trưởng cấp 7 vào vùng chọn
```

`hợp âm trưởng cấp 7` = Cmaj7. *"hợp âm trưởng với nốt 7"* = C + G — **hợp âm
cấp 7 chi phối**, hợp âm khác. Tiếng Anh nói hợp âm được **dựng từ nốt gốc rồi
thêm nốt**; tiếng Việt lại **đặt tên một loại hợp âm**. Khác hẳn.

Từ `với` chính là từ nói *nốt được cộng thêm*. Mất nó là đổi hợp âm:

| Tiếng Anh | Đúng |
|---|---|
| major chord **with a** 7 | hợp âm trưởng **với nốt** 7 |
| minor chord **with a** 6 | hợp âm thứ **với nốt** 6 |
| major chord **with a** major 7 | hợp âm trưởng **với nốt** 7 trưởng |
| suspended 4th chord **with a** 7 | hợp âm treo 4 **với nốt** 7 |

Còn `diminished 7th chord` / `half-diminished 7th chord` thì **giữ** `cấp N` —
đó mới là tên loại hợp âm.

### `Octave` = `quãng tám` trong câu, giữ `Octave` ở nhãn

25 key. 12 key dùng nó **như từ tiếng Anh** trong câu: `một octave`,
`cao hơn 1 octave`. Nhãn thì giữ: `Octave Line`, `Octave Symbol`,
`Octave Indicator` là **tên riêng của Cubase**.

### Bộ dò `reordered preposition` phải **bỏ qua ngoặc kép**

Đợt 39 có hai giá trị **đúng** bị báo động: chữ `for` nằm trong *tên tính năng
trong ngoặc kép* `"Maximum Duration for Rhythmic Slashes"`. Tên tính năng là
**danh từ riêng**, tiếng Anh giữ nguyên; `for` thuộc về cái tên, không thuộc
về câu. Đã vá `audit_quality.py` để xoá đoạn trong ngoặc kép trước khi dò.

### Lớp lớn nhất: **khung tiếng Anh, chỉ chèn giới từ tiếng Việt**

Đây là lớp lỗi mà **không bộ dò nào bắt được**, vì câu *có* tiếng Việt:

```
Notes for Which Accidentals Have Already Been Stated Within the Bar
  ->  Notes cho Which Accidentals Have Already Been Stated Within the Bar
Primary type is used for the main chord symbol
  ->  Primary type is used cho the main chord symbol
Press up to 5 keys to assign remote keys to subsections
  ->  Press up vào 5 keys vào Gán remote keys vào subsections
```

Câu tiếng Anh **đứng nguyên còn nguyên**; người dịch chỉ thay **đúng chỗ
giới từ tiếng Anh** bằng giới từ tiếng Việt rồi cho là xong. Không có gì bị
dịch sai — **không có gì được dịch**.

Cách phát hiện: `tools/find_english_frame.py` — một giá trị mang **4 từ tiếng
Anh liên tiếp** xuất hiện nguyên văn trong chính nguồn của nó thì đã bị *chú
thích*, chứ không phải *dịch*. Ngưỡng 4 vì thuật ngữ DAW tạo ra rất nhiều cụm
2–3 từ vô hại. `tools/dump_frames.py` in ra để đọc tay. `tools/
find_thin_vietnamese.py` là tỉ lệ Latin/Han — nó phát hiện ra lớp này.

Sau 2 đợt: 142 → 94, và **24 mục còn lại ở ngưỡng 5 đều đúng** (tên tính năng
trong ngoặc kép, đường dẫn menu, chuỗi định dạng).

Ngoài ra, cùng đợt quét ra hai thứ mà `audit_quality` báo 0:

```
The application was terminated unexpectedly  ->  application was terminated unexpectedly
The search returned no results              ->  search returned no results
```

Mất mạo từ `The` → **hết tiếng Việt**. Bộ dò "fully untranslated prose" hỏi
"có tiếng Việt không", mà `a` và `the` chính là toàn bộ chênh lệch.

### Lớp "mất vế": **7 lần trên 7, mất đúng vế có ĐIỀU KIỆN**

Đợt 32, 38, 38, 40, 44, 45, 45 — bảy lần phát hiện bằng tay, và **cả bảy** mất
đúng mệnh đề có *điều kiện* hoặc *cái giá*:

```
"... but requires you to estimate the pickup value."
"This has no effect for bar numbers centered on the bar."
"If this option is set to show a cautionary either with or without
 parentheses, then other cautionary accidentals ... are suppressed."
"Please note that this conversion might lead to clipping!"
"However, this also increases the power consumption of the computer. If power
 consumption is a concern, ... Further information ..."
"For support information, please contact the plug-in vendor."
"... and use the 'Convert Z-Axis Pan Automation of Selected Tracks' function
 if needed."
```

Không phải ngẫu nhiên: tiếng Anh **nói luật trước, nói ngoại lệ sau**, nên vế sau
trông như *chú thích* — và vế sau là thứ bị bỏ.

Nên có bộ dò: `tools/find_dropped_sentences.py` — đếm số câu (`.` `!` `?`) của
giá trị so với nguồn.

**Ba lần phải sửa bộ đếm mới ra bảy lỗi thật** — tỉ lệ bình thường:

1. coi `\n` là cuối câu → **27** chuỗi báo mất 1 câu, vì mọi giá trị nhiều dòng
   đều kết thúc bằng nó;
2. viết tắt `\\b[A-Z][a-z]{0,4}\\.` → **nuốt mất dấu chấm** của mọi từ viết hoa
   ngắn, khiến 9 câu `Cannot add more tracks` **đầy đủ** bị báo mất câu;
3. **key dài bị cắt cụt** trong `all_strings.tsv`, nên đếm trong key là đếm một
   *tiền tố*. Bản tiếng Anh đầy đủ nằm ở **key của dòng khác** — và hai dòng
   có thể trùng tiền tố 60 ký tự, nên phải yêu cầu **đúng một** ứng viên.

Còn sót: chuỗi mà tiền tố key trùng với anh em — hai trong ba lỗi ở đợt này do
tìm **tay** khi kiểm tra đầu ra của bộ dò.

### Tên trong ngoặc kép phải khớp **bản dịch của nhãn**

Không phải "tên trong ngoặc kép giữ tiếng Anh" — đó là **phiên bản sai đầu tiên**,
và nó sai 4 vòng liên tiếp (đợt 45, 46, 47 đều sửa theo nó rồi lại hỏng).

**Luật đúng: tên trong ngoặc kép phải khớp đúng những gì nhãn của nó dịch ra.**

Vì Cubase đã Việt hoá thì **menu hiện tên đã Việt hoá**, nên trích tên tiếng
Anh cũng sai, y như trích một chuỗi tiếng Việt mà menu không có:

```
'Part Editing Mode'   nhãn dịch là "Chế độ sửa Part"  ->  trích 'Chế độ sửa Part'  ĐÚNG
'Z-Axis Pan'          KHÔNG có nhãn tên đó              ->  giữ tiếng Anh          ĐÚNG
```

Cả hai đều đúng, và **chỉ tra nhãn** mới phân biệt được.

Bộ dò: `tools/find_quoted_names.py` — với mỗi tên trong ngoặc kép, tra nhãn có
tên tiếng Anh **đúng bằng** tên đó, đọc bản dịch nhãn, rồi so. Sửa:
`tools/fix_quoted_names.py` — **sinh bản thay từ bản dịch của chính nhãn**, không
viết tay 41 dòng. 41 dòng viết tay là 41 cơ hội sai, và bảng đó sẽ chứa **bản
sao thứ hai của bộ thuật ngữ** — đó chính là cách `Key Signature | hóa biểu` xảy ra.

**Ngoại lệ: tên nút / giá trị dropdown** giữ tiếng Anh vì đó là **chữ in trên
nút**:

```
Record Enable   nhãn dịch là "Bật ghi"
Activate "Record Enable" or "Monitor" ...
  ->  Bật "Bật ghi" hoặc "Monitor"      ← "bật bật ghi", vô nghĩa
```

Nên: `Record Enable`, `Monitor`, `Solo`, `Read`, `Write`, `Any` — giữ tiếng Anh.
Còn `Save` thì **không** — Cubase hiện `Lưu`, nên phải trích `'Lưu'`.

Bộ dò cũng phát hiện được **3 nhãn còn sót tiếng Anh** (vì nó tra nhãn):

```
Hide Key Signatures  ->  Ẩn Key Signatures      (anh em "Hide Clefs" là "Ẩn khóa nhạc")
Hook Only            ->  Chỉ Hook
Search for File      ->  Search cho File
```

### `Retrospective Record` = `ghi hồi tố` — **không phải** `hồi cứu`

`hồi cứu` = *recovery* (hộp đen máy bay, xem lại video). `hồi tố` = *retroactive*
(lương hồi tố, thuốc hồi tố). Cubase ghi lại cái bạn **vừa chơi** → `ghi hồi tố`.
14 key, một tính năng, **hai cách**.

Đây là lần thứ ba trong tháng này một tính năng bị vẽ ra hai kiểu — `Material`
(đợt 43), `audio stream` (đợt 41) — và **nguyên nhân luôn giống nhau**: không ai
đối chiếu key mới với bảy key đã có sẵn. Nên cách sửa luôn là **grep từ**.

### Tên tính năng **trong ngoặc kép** phải giữ nguyên tiếng Anh

Đợt 32 đã chốt: tên tính năng trong ngoặc kép là **danh từ riêng**, không phải
tiếng Anh chưa dịch. Đợt 46 thấy hai key vi phạm:

```
"Converting automation data may invalidate existing 'Z-Axis Pan' automation."
  ->  "... Automation 'Pan trục Z' hiện có."
"This profile requires '3-Layer 3D Pan Mode'. ... otherwise 'Z-Axis Pan'
 automation will be wrong."
  ->  "... 'Z-Axis Pan' sẽ sai."
```

Phải khớp **đúng chữ trên bảng điều khiển**, nếu không người dùng tìm không thấy.

## Mốc: đã đọc tay **toàn bộ** 10.737 chuỗi

| Miền | Nhãn ngắn | Câu dài | Ghi chú |
|---|---|---|---|
| `general` | 6.834 | 499 | đợt 19, 31–37 |
| `notation` | — | 56 | đợt 38 |
| `music-theory` | — | 100 | đợt 39, 40 |
| `media` | — | 205 | đợt 41–44 |
| `mixer` | — | 103 | đợt 46, 47 |
| `transport` | — | 96 | đợt 49 |
| `ui` | — | 49 | đợt 50 |
| `project` | — | 30 | đợt 51 |

Đợt 51 (`project`) chỉ có **6 sửa** — ngắn nhất trong 51 đợt. Nguyên nhân nằm
ngay trong chuỗi: miền `project` toàn câu ngắn, công thức, về quyền và mạng, **ít
từ để sai**; và phần lớn chúng **chưa từng bị một lượt dịch tệ đụng vào**.

**Hệ quả quan trọng:** rủi ro còn lại **không phân bổ đều**. Miền đáng đọc lại
là miền có **văn xuôi dài** (`media`, `notation`, `general`) — không phải các hộp
thoại xác nhận.

Bộ dò hiện có (tất cả chạy sạch trừ 1 báo động giả đã biết):

```
tools/find_english_frame.py      4+ từ tiếng Anh nguyên văn từ nguồn   -> 84 (đều đúng)
tools/find_english_opening.py    câu bắt đầu bằng động từ tiếng Anh    -> 24 (đều nhãn)
tools/find_dropped_sentences.py  ít câu hơn nguồn                       ->  1 (giả)
tools/find_quoted_names.py       tên trong ngoặc kép lệch nhãn         ->  0
tools/find_thin_vietnamese.py    tỉ lệ Latin/Han cao                    -> dẫn đường
```

### `Material` = `chất liệu` — **không phải** `tư liệu`

`tư liệu` = *documents* (từ thư viện). `chất liệu` = *material*, và nó phủ **cả
hai** nghĩa: `chất liệu Audio` (audio material) và `chất liệu đơn âm`
(monophonic material). 9 key, một từ.

Đây chính là lỗi `String` của đợt 29 (MIDI string, dây đàn, chuỗi) — **một từ
tiếng Anh, đọc thành hai từ tiếng Anh khác**. Nó cứ tái diễn vì mỗi key mới
trông như một quyết định mới.

**Một danh từ tiếng Anh — một danh từ tiếng Việt.** Quyết định một lần, áp
dụng khắp nơi. Đây là lý do phải `grep` **từ** chứ không `grep` key.

### Câu tiếng Việt thiếu **dấu trạng ngữ** (`được`)

```
"... a parameter of a VST 2 plug-in cannot be modulated."
  ->  "... tham số của Plug-in VST 2 không thể Modulation."
```

Tiếng Việt cần `được`: **X không thể *được* Modulation**. Thiếu nó thì câu
đọc thành *"tham số đó không phải là Modulation"* — nghĩa **đảo ngược**. Cùng lỗi
với `có thể Automation` → phải là `có thể **nhận** Automation`.

### Quan hệ từ dồn lên danh từ — 6 chuỗi trong một họ

```
The project file contains '%s' data which is not supported by this
program version.
  ->  File Project chứa dữ liệu '%s' không được phiên bản chương trình
      này hỗ trợ.
```

Tiếng Anh chịu được (chỉ từ hạn định đứng sau danh từ). Tiếng Việt phải **tách**:
`chứa dữ liệu '%s' **mà** phiên bản chương trình này không hỗ trợ`.

### `Mouse Wheel` là **con lăn chuột**, không phải `cuộn chuột`

`cuộn` = *scroll* (hành động cuộn). `con lăn chuột` = *mouse wheel* (cái thiết
bị). Sáu key họ Pad đều ghi `cuộn chuột`:

```
Fewer Tensions ([ALT] - mouse wheel on pad)   ->  Ít Tension hơn ([ALT] - cuộn chuột trên pad)
Next Voicing (mouse wheel on pad)             ->  Voicing kế tiếp (cuộn chuột trên pad)
Transpose Up ([SHIFT] - mouse wheel on pad)   ->  Transpose lên ([SHIFT] - cuộn chuột trên pad)
```

Cả hai từ **đều đã có trong bản dịch** và cả hai đều **đúng ở key khác**:
`Scroll to Selected Channel` → `Cuộn tới Channel đã chọn` (đúng — key đó
thật sự về cuộn), `Use Mouse Wheel for Event Volume and Fades` → `Dùng con lăn
chuột...` (đúng). Họ Pad chọn nhầm.

**Bài học:** khi một từ tiếng Việt có **hai từ tiếng Anh về nó**, phải tra cả
hai nghĩa trong bản dịch trước — `cuộn`/`lăn`, `ngoài`/`External`,
`chuỗi`/`dây đàn`, `từ`/`Word Clock`.

### `Write Protection` = `bảo vệ ghi`, **kể cả nhãn** — không chỉ câu

Đợt 31 chốt `Write Protection` = `bảo vệ ghi` vì hai câu anh em đã dùng từ đó.
Nhưng 4 key còn giữ `chống ghi`, trong đó có **chính nhãn mà các câu sinh ra**:

```
Write protection (a checkmark in this column prevents an entry from being
overwritten)
  ->  Chống ghi (dấu tích ở cột này ngăn mục không bị ghi đè)
```

Sửa câu mà không sửa nhãn là **chính là** cách mà phần tách này sinh ra.

### `số` (một con số) khác `số lượng` (một lượng)

Câu báo giới hạn không cần *lượng*:

```
Cannot add more tracks. The audio track count is at the limit.
  ->  Không thể thêm Track. Số lượng Audio Track đã đạt giới hạn.
```

Đợt 32 sửa 7 trong 9 câu `Cannot add more tracks` và **bỏ sót 4** — chính là
4 câu còn lại. Sửa *một câu đại diện* của họ rồi dừng là sai; phải đếm hết.

### Bốn lần "đọc một từ thành một từ khác"

`Half` → `Giảm` (flat) · `Ext.` → `Mở rộng` (extend) · `String` → `Dây đàn`
(text string) · `Word` → `Từ` (text word). Cả bốn đều **đọc đúng về mặt hình
thức, sai về nghĩa**, và cả bốn đều không thể bị bộ dò nào bắt.

Nên khi một key có **nhiều nghĩa**, phải tra key anh em cùng họ trước khi dịch —
rồi so cả những key đã tưởng là đúng.

### `Symbol` và `Sign` — cùng ra một giá trị

`Symbol` (loại đầu nốt của Cubase) và `Sign` (ký hiệu ký âm) đều thành
`ký hiệu`. `Sign` giữ `ký hiệu`; `Symbol` giữ `Symbol`.

### `Set up X` — dịch cả tiền tố rồi bỏ mặc danh từ

Họ `Set up ...` có 20 nhãn, và 13 cái dịch `Set up` thành `Thiết lập` rồi **bỏ
đối tượng**:

```
Set up Attribute Columns  ->  Thiết lập Attribute Columns
Set up Cell Layout        ->  Thiết lập Cell Layout
Set up Items              ->  Thiết lập Items
Set up Status Line        ->  Thiết lập Status Line
Set up Tabs               ->  Thiết lập Tabs
```

Tệ hơn họ `No ...`: ở đây nửa tiếng Việt **đã có** nên nhìn như đã dịch. Kiểm
`toàn câu có tiếng Việt` sẽ bỏ sót, phải đọc phần sau tiền tố.

### `Doubles` là Note *trùng*, không phải nốt *lặp đôi*

`Delete Doubles` → `Xóa Note trùng` (đúng) nhưng `Skip Doubles` →
`Bỏ qua nốt lặp đôi` (sai) — cách hai trăm key. `Doubles` là nốt lặp do ghi
trùng, không phải nốt dài gấp đôi.

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

### `New` là *mới*, không phải `Tạo`

32 nhãn mở đầu bằng `New`, và 28 cái dịch `New` thành `Tạo`:

```
New Attribute  ->  Tạo Attribute      New Library  ->  Tạo Library
New Bank       ->  Tạo Bank           New Preset   ->  Tạo Preset
New Folder     ->  Tạo Folder         New Track    ->  Tạo Track
...
```

Hai anh em lại đúng: `New Project` → `Project mới`, `New Version` → `Phiên bản
mới` — **vì vậy 28 cái kia chưa bao giờ được đối chiếu với ai**. Người dùng đọc
`Tạo Track` trong menu sẽ hiểu là *tạo* một Track, không phải *Track mới*.

### `No.` là *số*, không phải *không phải*

`No. of Frets` → `No. của Frets`. Ở đây `No.` là viết tắt của **Number**. Trong
khoảng 60 nhãn mở đầu bằng `No`, bốn cái đã đẩy chữ `No` ra cuối như danh từ:

```
No Parameter   ->  Tham số No        ← "tham số số"
No Section     ->  Phần No           ← "phần số"
No Status Info ->  Thông tin No Status
```

Cùng lớp với `Group` → `Gộp nhóm`: chữ bị coi là danh từ rồi đẩy hết xuống
cuối. Đây là lỗi đảo thứ tự từ ở dạng ngắn, chỉ lộ ra khi đọc.

### Không tự sửa chính tả Cubase

`Myxolydian` → `Mixolydian` và `Myxolydic9/11` → `Mixolydic 9/11`. Bản dịch đã
"tự sửa" chính tả của Cubase, khiến tiếng Việt **mâu thuẫn** với tiếng Anh mà
người dùng vừa bấm. Tên tính năng thì giữ nguyên, kể cả khi có vẻ sai.

### `Notehead` là **đầu nốt**, không phải `đầu nối`

`đầu nối` = joint, terminal, connector. Khoảng 40 nhãn dùng `đầu nốt` (đầu của
nốt). Đợt 14 tôi sửa `Default Noteheads` → `Đầu nối mặc định` và đợt 15 sửa
`Hidden Noteheads` → `Các đầu nối đang ẩn` — **tự tạo ra biến thể thứ hai**
trong lúc đang sửa thứ khác. Đến đợt 20 mới thấy, vì `Plus Noteheads` và
`Muted Slash Noteheads` vẫn còn `đầu nốt` và không ai trong họ đứng cạnh hai
bản của tôi.

Bài học: sửa một chuỗi trong một họ thì phải liệt kê **cả họ** ra, kể cả những
cái tưởng là đã ổn.

### Không tự sửa mệnh đề tiếng Anh

`Pattern Event / Track` → `Track Pattern Event /` và `Pre/Post MIDI Modifiers and
Inserts` → `Inserts Pre/Post MIDI Modifiers and`: hai chuỗi gốc đã bị tháo ra
và ghép lại thành hai chuỗi khác. Chỉ còn chứa cùng các từ.

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

### Bốn lần rule báo động giả

Ghi lại để không lặp lại:

1. `Tên Channel`, `Số Note`, `Chế độ Value` trông như đảo nhưng **đúng** —
   tiếng Việt đặt danh từ trước. 201 chuỗi phải giữ nguyên.
2. `gán vào`, `chuyển vào` là cách nói tự nhiên, cần `vào` để dẫn tân ngữ.
   Rule "vào thừa" bắt nhầm 14 chuỗi đúng rồi phải siết lại.
3. `lặng` là một từ riêng bên trong `dấu lặng`; khớp không ràng giới từ thì
   `audit_quality` báo xung đột cho **mọi** chuỗi đúng. Tương tự `Hóa biểu` /
   `hóa biểu` chỉ khác hoa-thường, và `Over` trong `Cross-Over` khớp `\b` sau
   dấu gạch nối.
4. `check_style` cấm ngoặc `(...)` ở cuối giá trị, trừ khi key đã có ngoặc. Nó
   khớp cả khi phần trong ngoặc chỉ là **ký hiệu đơn vị xuất hiện ngay trong
   key**: `Inhibit Restart ms` → `Thời gian chặn khởi động lại (ms)` bị báo,
   dù `(ms)` là đơn vị chứ không phải chú thích từ điển. Sửa giá trị, đừng sửa
   luật: viết `Thời gian chặn khởi động lại, tính bằng ms`.

Một bộ dò báo động giả nhiều lần hơn còn tệ hơn không có bộ dò: nó dạy người
đọc bỏ qua báo cáo.
