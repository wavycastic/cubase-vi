# AGENT.md — Quy tắc bắt buộc khi dịch Cubase 15

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ. Chuẩn hoá
theo `keys/all_strings.tsv` (10.737 cặp key ⇄ English).

**Tài liệu này nén.** Nó chỉ giữ (a) luật áp dụng hôm nay và (b) bằng chứng không
tái tạo được bằng cách đo lại. Chuyện đã xảy ra ở đợt nào nằm ở `git log`; lý do
viết một luật nằm trong docstring của công cụ sinh ra nó. **Đừng bổ sung ghi chép
đợt vào đây** — hãy viết vào docstring công cụ hoặc `docs/OPEN_QUESTIONS.md`.

Trước khi điều tra một cụm đang lệch, đọc `docs/OPEN_QUESTIONS.md`. Năm cụm
(`Filter`, `Template`, `Audio Performance`, tên nhạc cụ, `Auto X`) đã bị điều tra
lại từ 5 vòng khác nhau mỗi lần đều dừng ở "không đủ bằng chứng". Một mục chỉ
được xoá khi có (a) nhóm anh em buộc phải theo một hướng, hoặc (b) **người dùng
quyết**. Tỉ lệ 51/49 không phải (b).

## 0. ĐỪNG ĐOÁN — thứ tự tra bằng chứng khi một chuỗi mơ hồ

Bản dịch là **XML phẳng 10.737 mục, xếp A-Z, không có trường "nhóm", "màn hình"
hay "hộp thoại"**. Nên thấy `Spike` thì không có gì trong file cho biết nó là đỉnh
nhọn trên đường cong automation hay gai trên cây — và đã dịch sai thành "gai".
`Aspect` dịch thành "tỉ lệ khung hình" (`Aspect Ratio`) trong khi nó là góc nhìn
MediaBay. Mọi lỗi cùng loại đều xuất phát từ đúng chỗ này.

**Đi theo đúng thứ tự này, dừng ở bước đầu tiên cho ra câu trả lời:**

| # | Bước | Lệnh | Ra được gì |
|---|---|---|---|
| 1 | **Cụm `.rdata`** | `group_by_offset.py -k "<từ>"` | chuỗi nằm cạnh những gì trong code |
| 2 | **9 ngôn ngữ** | `read.py inspect "<từ>"` | nghĩa, khi tiếng Anh trơ trọi |
| 3 | **Gia đình** | `family.py <từ>` | các cách viết của anh em |
| 4 | **Hỏi người dùng** | ảnh chụp màn hình | chốt |

Bước 1 mạnh nhất và **rẻ nhất** — tự động, không cần mở Cubase. Đo được:

```
6.764 / 10.737 chuỗi (63,0%) có literal trong .rdata
chuỗi CÙNG NHÓM median cách nhau    73.824 byte
chuỗi KHÁC NHÓM median cách nhau 1.082.648 byte   → gần nhau hơn 14 lần
333 cụm, đã đặt tên hết (104 từ Key Commands, 229 tự đặt trong group_names.json)
```

Steinberg cấp phát literal theo module dịch vụ và các module đứng cạnh nhau, nên
**vị trí trong binary là nguồn nhóm thật**. Ví dụ nó đã xác nhận hai chỗ từng chỉ
đoán bằng "anh em nên đối xứng":

```
0x060F8EC0 'Keep Last'   0x060F8F28 'Stacked'   0x060F8FE8 'Mix-Stacked (No Mute)'
0x060FA3F0 'Cut Head'    0x060FA4C0 'Cut Tail'
```

**3.946 chuỗi (36,8%) không có literal ở đâu** — đã tìm mọi section, cả ASCII lẫn
UTF-16; `Show Horizontal Line`, `%d User(s)`, `+18 Scale` chỉ ra `.rsrc` và không
có chỗ nào khác. `deobf_scan` chạy rồi: 281 chuỗi, toàn đường dẫn `__FILE__`.
Với 36,8% đó **không có cách tĩnh nào** — dùng bước 2. Và phần lớn chúng là nhãn
ngắn, không có nhóm cũng không dịch sai.

**27 chuỗi bị lo vì quá chung** (`Transpose` ×85, `Right` ×34, `Full` ×34,
`BPM`, `Byte`, `Gain`…) — offset đầu tiên không nói được chuỗi đó thuộc module nào.

**Hai hướng RE đã chết — đừng thử lại:** (a) gom nhóm theo hàm gọi: mỗi hàm lá chỉ
dựng *một* nhãn (`Transport Panel` → 2 hàm, mỗi hàm đúng 1 chuỗi); (b) `xref.py`
với file offset báo "0 xrefs" — sai cách gọi, target ở `.rdata` phải dùng `--va`.

## 1. Kiểu dịch

- **Động từ / thao tác / trạng thái / giao diện** → Việt hoá ngắn gọn: `Thêm`,
  `Xóa`, `Gỡ bỏ`, `Nhân bản`, `Sửa`, `Mở`, `Lưu`, `Bật`, `Tắt`, `Ẩn`, `Hiện`,
  `Chọn`, `Tới`, `Đảo ngược`.
- **Thuật ngữ âm thanh & DAW** → **giữ tiếng Anh**, ghép vào ngữ pháp tiếng Việt.
- **Bảng màu (Color Setup / Palette)**: giữ nguyên tiếng Anh cho toàn bộ tên màu
  (White, Black, Red, Green, Blue, Yellow, Orange, Magenta, các biến thể Dark/Light,
  Black 50/70, Gray 5..90) theo yêu cầu người dùng. Các nhãn chức năng vẫn dịch
  bình thường (`Color` → `Màu`, `Colors` → `Màu sắc`, `Colorize` → `Tô màu`).
- **TUYỆT ĐỐI KHÔNG**: ngoặc chú thích ở cuối (`Thêm track (Add Audio Tracks)` —
  SAI, nhãn tràn chữ). Chỉ giữ ngoặc khi **key gốc đã có**, và khi đó dịch trong
  ngoặc. Cũng không dịch thuần Việt: `Automation`, `Bounce`, `Track`, `Clip`,
  `Freeze`, `Quantize`.

## 2. Thuật ngữ bắt buộc

**DAW — giữ tiếng Anh, 160 từ.** Nguồn chân lý là
`terms_do_not_translate.json` (68 cốt lõi + 90 mở rộng + 2 Score). **Tính từ file,
không tin tiêu đề** — năm 2024 tiêu đề ghi "70" nhưng list chỉ có 68.

Cách tìm từ nên cấm — **đừng** hỏi "thuật ngữ nào đã bị dịch" (16 ứng viên, không
cái nào sai). Hỏi: **thuật ngữ nào có MỘT chuỗi lệch khỏi gia đình?** — 18 lỗi.
`audit.py outlier` làm đúng việc đó.

**Bàn nhạc (Score Editor) — giữ nguyên thuật ngữ chuyên ngành:** vì Score Editor là
môi trường ký âm và khắc bản nhạc theo chuẩn quốc tế, toàn bộ thuật ngữ chuyên ngành
ký âm quốc tế giữ nguyên tiếng Anh: Staff/Stave · Clef · Barline · Stem · Beam ·
Accidental · Rest · Grace Note · Notehead · Arpeggio · Tuplet · Glissando · Trill ·
Fermata · Key Signature · Time Signature · Chord Symbols · Rhythm Dot · Ledger Line ·
Slur · Tie · Inversion · Interval · Swing · Cadence · Slash. Động từ thao tác và
giao diện chung vẫn Việt hoá tự nhiên.

`System` và `Bar` theo ngữ cảnh: Score Editor → `System` / `Bar`; ngoài đó →
`hệ thống` / `thanh`. Từ HLV cũng giữ bên HLV: `con trỏ`, `bè`, `phát lại`, `hợp âm`.

Ba ngoại lệ đã đo, **đừng đo lại**:

| Ngoại lệ | Vì sao |
|---|---|
| `Voice` **không** giữ EN | Gia đình 36 chuỗi, 33 dịch `bè`; 9 ngôn ngữ gốc đều dùng nghĩa *thanh/giọng* (zh 声部, de Stimme). Liệt nó từng làm 2 chuỗi `Single Voice` lạc gia đình. |
| `Fermata`, `Ledger Line` | **0 key, 0 giá trị** trong Cubase 15. Giữ trong luật để sau dùng, nhưng đừng đi tìm để sửa. |
| 6 từ thêm (đợt 172) | `Slur` (→"dấu luyến"; *luyến* = lỗi lầm), `Inversion` (→"thể đảo"; *thể* = cỡ vải), `Interval` (thống nhất), `Tie`, `Swing`, `Cadence` — vì tìm thấy chúng **đang bị dịch sai nghĩa**. Sửa 19 chuỗi. |

**Bài học của 6 từ đó:** danh sách §2 phải khớp với map, và cả hai đều phải kiểm.
Viết luật rồi tin là xong là lỗi nguồn — đã xảy ra ở `Time Signature` (luật §3 bắt
`số chỉ nhịp`, §2 bắt giữ EN; 49 chuỗi theo §3 là bằng chứng §3 sai). Đợt 146–171 đã
sửa hết 49 chuỗi về giữ EN. `Chord` giữ nguyên `hợp âm` — xem bảng bên dưới.

## 3. Bẫy thuật ngữ — đọc sai ở đây là hỏng

| Sai → Đúng | Vì sao | Sai → Đúng | Vì sao |
|---|---|---|---|
| `Duration` → **thời lượng** | *trường độ* = ngành/khoa | `New` → **mới** | không phải *Tạo* |
| `Word Clock` → giữ `Word` | *Word Spacing* → *Khoảng cách từ* đúng | `Deactivate` → **Tắt** | *Hủy* = *cancel* |
| `External` → giữ `External` | *outside* = nghĩa **đối lập** | `Doubles` → **Note trùng** | ghi trùng, không dài gấp đôi |
| `Material` → **chất liệu** | không phải *tư liệu* | `Notehead` → giữ **Notehead** | thuật ngữ chuyên ngành ký âm |
| `Retrospective Record` → giữ Anh | *hồi tố* = 0 chuỗi | `Group` (danh từ) → **nhóm** | `Gộp` là động từ |
| `Factory` → giữ `Factory` | đã có 4 kiểu | `Command` → **lệnh** | `Key Command` → **phím tắt** |
| `Pick-up` → giữ **`Pick-up`** | không phải *Lấy đà* | `Scaling` → **co giãn** | *thu phóng* = `Zoom` |
| `Mouse Wheel` → **con lăn chuột** | không phải *cuộn chuột* | `Write Protection` → **bảo vệ ghi** | kể cả ở nhãn |
| `Flat` → **giảm** | nửa tông, không phải *phẳng* | `Multi` → **bội** | *đa kênh* = *multichannel* |
| `Symbol` / `Sign` | cùng **một** giá trị | `Octave` | `quãng tám` trong câu, `Octave` ở nhãn |
| `Version` (nhãn) → giữ | trong câu `phiên bản` đúng | chord **with a** 7 → **với nốt** 7 | `cấp 7` = Cmaj7 |
| `Sus` | **viết tắt hợp âm** (sus2/sus4), KHÔNG phải `Sustain` (pedal) | `Doubles` | |

**Danh từ vs động từ — cùng một từ, hai cách.** `Click` **vừa** là nút giữ EN
(`Click Pattern`, `Click & Count-In`) **vừa** là động từ (`click chuột` → `Nhấp`,
đúng). Cùng kiểu `Insert`, `Send`, `Note`, `Beat`, `Group`. Đo ở đợt 171: 115 chuỗi
có `Click` nhưng chỉ vài chuỗi giữ — vì nó là cả hai nghĩa.

| Từ | Giữ EN khi | Dịch khi |
|---|---|---|
| `Click` | `Click Pattern`, `Click & Count-In` (tên tính năng) | `click chuột` → `Nhấp` |
| `Insert` | `Insert 1`, `Insert Slots`, `Bypass Insert` | `insert …` → `chèn` |
| `Send` | `Send 1`, `Send Slots` | `send …` → `gửi` |
| `Chord` | **`Chord` KHÔNG dịch** (77 chuỗi `hợp âm`) | — |
| `Note` | `Note 1/8` (Score) | `note nhạc` → `nốt` |
| `Beat` | nhãn/đơn vị | văn xuôi → `nhịp` |
| `Group` | tên tính năng (`Group Track`, `Group %d`, `Group 1..4`) | `nhóm nốt` → `nhóm` |

**Ba ngoại lệ đã quyết, đừng mở lại:**

- **`Beat` dùng `nhịp`, KHÔNG `phách`** (đợt 173). *Phách* đúng nghĩa nhưng lạc khỏi
  17 chuỗi còn lại; 3 chuỗi lọt dùng nó.
- **`Noteheads` giữ nguyên 39/39.** 40 tên notehead đều mang đuôi `s` — đó là **mẫu
  tên**, không phải số nhiều cần bỏ. Ngược lại `Slurs`→`Slur`, `Clefs`→`Clef`,
  `Accidentals`→`Accidental`, `Tuplets`→`Tuplet`, `Bar Rests`→`Bar Rest` là đúng.
  **Cách đo lại được:** tách 3 nhóm (chỉ số ít / chỉ số nhiều / cả hai), đếm trong
  nhóm số nhiều bao nhiêu giá trị còn giữ `s`. Hầu hết *không* giữ → giữ là lỗi;
  *toàn bộ* giữ → mẫu tên.
- **`Set up X`** (20 nhãn): dịch `Set up` thành `Thiết lập` rồi **bỏ mặc danh từ** —
  `Thiết lập Attribute Columns`. Kiểm "câu có tiếng Việt" sẽ bỏ sót; phải đọc phần
  sau tiền tố. Cùng kiểu, `Replace / Restore / Reload / Resolve / Reveal /
  Resulting` — bảy giá trị **tháo câu ra ghép ngược**: `Restore Default Setup` →
  `Thiết lập Restore Default`.

**Luật phụ thuộc nguồn** (mục `src` trong `terms_do_not_translate.json`): `Bypass` cấm
`bỏ qua`, `Cycle` cấm `lặp` — cùng một từ Việt đúng ở nguồn này, sai ở nguồn kia. 13
`Bypass` đã sửa, nhưng 23 chuỗi `Ignore` **phải** giữ `bỏ qua`. Đây không phải chuyện
phức tạp hoá: một mẫu vô điều kiện sẽ chặn hết 23 chuỗi đúng.

**Bộ thuật ngữ giữ EN đã chốt** (đều có mặt trong `terms_do_not_translate.json`, đừng
viết lại ở đây): `Automation Read/Write` (nút **R**/**W** — tuyệt đối không dịch
thành "đọc"/"ghi", gây nhầm với `Record`) · `Record Enable` · `Nudge` · `Jog`/
`Shuttle`/`Scrub` · `Precount` · `Bit Depth` · `Strip Silence` · `Saturation` ·
`Normalize` · `Integrated Loudness` · `Short-Term Loudness` · `Chord Assistant` ·
`Circle of Fifths` · `Proximity` · `Detect Silence` · `Acoustic Feedback` ·
`Bank Select` · `Track Archive` · `Thumbnail Cache` · `Pan Law` ·
`Simple Crossfade Editor` · `Equalizers` (bỏ chữ "Các") · `Functions Browser` ·
`Lower Zone` (khớp `Left Zone`/`Right Zone`) · `Hermode Tuning` (không đảo thành
`tuning Hermode`) · `Send 1..4 Out/Pre` (không ngô nghê) · `Auto-Scroll` ·
`Thumbnail Cache` · `Zoom` ≠ `Scaling`.

**Ba bộ dò đã dùng và bỏ — đừng chạy lại:** phủ định (280 ứng viên, tiếng Việt phủ
định bằng `Tắt`/`Bỏ`/`Gỡ`) · tra `keep_english` (mọi ứng viên đều là *nghĩa thường
trong văn xuôi* — `part of the channel`, `has no effect`) · key trùng tiền tố có
giá trị bằng nhau (13 cặp, tất cả là marker `[...]` của key theo §6).

**Bốn cụm đã điều tra xong — đừng đo lại:**

| Cụm | Kết luận |
|---|---|
| **`Switch: Activate Speakers`** → `Bật/Tắt Control Room` | **Trông như lỗi copy-paste, nhưng ĐÚNG.** `<us>` gốc là `Control Room On/Off`, cả 8 ngôn ngữ đều dịch "Control Room" — **key bị cũ**. Đây là bài học đắt nhất: **mọi ứng viên phải tra `<us>` trước khi sửa.** |
| **`Note #` → `Số Note`** | 5/9 ngôn ngữ giữ `Note #`, nhưng `CC No.` đã dịch `Số CC`, và hai cái là **cùng một ý**. Giữ là đúng và nhất quán. |
| **`Assume Skipping` → `Xử lý Clip hiện có`** | Key tiếng Anh lệch nghĩa với **cả 8 ngôn ngữ còn lại**. Lỗi di truyền của Steinberg; dịch theo đa số là đúng. |
| **`Respell`, `Respell Using Note Name Above/Below`** | `Respell` là động từ nhạc lý, §2 giữ nguyên thuật ngữ ký âm, dịch sẽ mất sắc thái. Cũng giữ `Beaming: Beam Together` → `Nối Beam: Nối chung` dù hơi lặp, vì `Verbalken` của Đức cũng lặp. |

**Ba chuỗi `key` ≠ `<us>` đã đóng băng** — `MIDI Step Input` / `Slip Event` /
`Pre/Post Fader`. Người dùng trả lời "chưa check", xem mục 6 của
`docs/OPEN_QUESTIONS.md`. **Đừng hỏi lại, đừng sửa.**

### Bẫy KHÔNG có máy nào canh — mỗi dòng một bẫy, đã sửa xong nhưng luật phải nhớ

Đợt 195 đo 7 phương án thuật toán: **5/7 cho ra nhiễu**. Các bẫy dưới đây **không
thuộc loại đó** — không phải đếm, mà là so nghĩa, nên máy không thấy.

| Bẫy | Luật |
|---|---|
| `-oo dB` / `-inf dB` | **KHÔNG** thay bằng `-∞ dB`. 9/9 và 6/9 catalogue Steinberg giữ nguyên chữ nguồn. Đợt 186 sửa ngược lại sau khi máy Việt-hoá. |
| `maj3` `sus4/11` `min3/#9` | **Định danh nhịp giữ nguyên hoa/thường của nguồn.** Máy hay Việt-hoa ký hiệu. Anh em `Triads with maj9` / `min9` viết **thường** — theo chúng. |
| `Sine` / `Square` / `Triangle` | zh ghi `正弦`/`方波`/`三角波` = **tên dạng sóng**, KHÔNG phải notehead. Nhóm `Triangle Up Noteheads` giữ EN là chuyện khác. `Ramp` đã giữ EN từ trước, nên cả ba phải về EN để đồng bộ. |
| `Natural/Harmonic/Melodic Minor` | Cả **ba** giữ EN. Đợt 172 chốt `Natural Minor`, 186 đồng bộ hai cái kia — dịch "melodic" thành *giai điệu* là thành *melody*. |
| `Family Name` | KHÔNG dịch `họ` — **`họ` = họ tên (surname)**, sai nghĩa hoàn toàn. Đây là trường metadata họ sản phẩm; `Add Family` → `Thêm Family`, `iXML Family UID` giữ EN. |
| `Unfold Tracks` | `Mở` là lệnh *Open*. `Unfold` là *bung ra* (đối với `Fold` → `Gấp`). Đúng là `Mở rộng`, khớp `Expand/Collapse Folder` → `Mở rộng/Thu gọn`. |
| `Generic` | `Chung` làm nó **trùng giá trị với `General`**. 5 anh em đều giữ `Generic`. |
| `Record only Specific Controller No.` | Đừng để vỡ thành `Chỉ ghi Controller cụ thể số.` |
| `CCMode:` · `Direct Offline Processing:` | Tiền tố `Word: ` là **nhãn**, phải đứng đầu giá trị và giữ tiếng Anh. |
| `Assum Skipping` (thiếu `u`) | Lỗi chính tả **của nguồn**, dịch theo ý nghĩa. `audit.py typos` liệt kê 3 lỗi nguồn: `pich`, `occured`, `the the`. |
| `-oo` dấu gạch nối | Quy ước có sẵn, đừng "sửa": dấu `-` trong `Medium-high` và dấu `.` trong `No.` đều bị bỏ trong giá trị. Khi viết bộ dò phải **miễn trừ** hai ký tự này. |

**Cách tìm nhanh nhất — MỘT CHUỖI LỆCH KHỎI GIA ĐÌNH.** Đợt 186, 187 và 191 đều ra
lỗi thật bằng cách này: gom nhóm theo từ đầu tiên (`tools/family.py <từ>`), đếm số
cách viết, rồi đọc **chuỗi lạc**. Rẻ nhất là `value == key` trong khi anh em đã dịch —
ứng viên tức thì. Hai chiều đều phải soi: **một chuỗi giữ EN trong khi 180 anh em dịch**
(`Show` → `Hiện`) **và ngược lại** (`Show Clefs` giữ EN khi 180 chuỗi `Show X` dịch).

**Hai nhạc cụ khác nhau, một tên** là lớp lỗi nguy hiểm nhất: `Temple Block` và
`Wood Block` cùng ra `Mõ gỗ` — 5/9 ngôn ngữ phân biệt (de `Templeblock`/`Holzblock`,
fr `Bloc chinois`/`Wood-block`), nghĩa là **hai pad khác nhau trong Drum Editor hiện
cùng một tên**. Cách phát hiện: `Counter` trên **`value`**, rồi ghép `key` vào đọc tay.
`dupes.py values` làm đúng việc đó.

## 4. Thứ tự từ và câu

- **Danh từ chính giữ vị trí.** Anh đặt ở cuối → `Output Bus`, `Analyzer Track`; Việt
  đặt trước → `Tên Channel`, `Số Note`, `Chế độ Value`. Cả hai dạng **đúng**. HLV +
  tiếng Anh: `Tên Channel`; HLV + HLV: `Volume của Channel`.
- Số đứng **trước**: `100 Events` → `100 Event`; `%d Channels` → `%d Channel`.
- `to` khi **chuyển đổi** là `sang` (không phải `vào`, không phải mũi tên):
  `Mono to Multi-Channel` → `Mono **sang** Multi-Channel`. `vào` thừa khi câu đã có
  động từ (`Go vào Input` → `Tới đầu vào`), nhưng `Thêm ... vào ...` là **đúng**.
- **Viết lại cả câu**, không thay từ rời — kể cả khi mọi từ đều là thuật ngữ DAW.
- **Câu phải có chủ thể.** `Đạt giới hạn ...` thiếu chủ ngữ → `Đã đạt giới hạn ...`.
  Giữ dấu kết câu và dấu ba chấm của key.
- **Đừng cắt mất câu.** Tiếng Anh **nói luật trước, ngoại lệ sau** nên vế sau trông như
  chú thích và là vế **bị bỏ** — mất đúng thứ nói *cái giá* của tính năng. Câu dài: **đếm vế**.
- **Tên trong ngoặc kép phải khớp bản dịch của nhãn** — vì menu hiện tên đã Việt hoá.
  `'Part Editing Mode'` → trích `'Chế độ sửa Part'`. Ngoại lệ: tên nút / giá trị
  dropdown giữ tiếng Anh (`Record Enable`, `Monitor`, `Solo`, `Read`, `Write`, `Any`)
  vì đó là chữ **in trên nút**. `Save` thì không — Cubase hiện `Lưu`.
- **Không dịch nửa vế**: dịch thì dịch trọn, giữ thì giữ trọn, không để nửa.

## 5. Văn phong — bỏ bị động, rút gọn

Phải là **tiếng Việt đời thường**, không phải tiếng Việt do máy dịch.

**Khó dịch thì để tiếng Anh. Đừng ép.** Người dùng chốt (đợt 165). Bản dịch vòng vẫn
đọc được thì dịch; **không đọc được thì giữ nguyên tiếng Anh** — một câu tiếng Anh còn
hơn một câu tiếng Việt sai nghĩa. Không phải "lười": chỉ khi đã thử và còn vướng.
- Cờ đỏ: dịch từ tiếng Anh **có một nghĩa đúng** sang từ tiếng Việt **khác nghĩa**.
  Đợt 165: `…used **these clefs**…` → `…loại **khóa** này…` (khóa = key, không phải
  clef). Chỗ này **giữ `Clef`** mới đúng.
- Cờ đỏ thứ hai: hiểu là dịch được nhưng **đọc lông nhằng** (`nương`, `thiết bị đầu
  vào và đầu ra mạng` cho `network interface`). Viết lại cho tự nhiên; tới mức không
  tự nhiên được thì giữ EN.
- **Cấm để lại chỗ dở dang**: sửa nửa câu còn tệ hơn để nguyên.
- **Vẫn phải giữ bất biến kỹ thuật (§6)** kể cả khi giữ EN. `build.py punct` không
  ngoại lệ.

| Viết sai | Viết đúng |
|---|---|
| `đã được` / `sẽ được` / `đang được` | `đã` / `sẽ` / `đang` |
| `đã bị loại bỏ` | `đã bỏ` |
| `Không thể chỉnh sửa VariAudio` | `Không sửa được VariAudio` |
| `không thể được Modulation` | `không nhận Modulation` |
| `Bạn phải khởi động lại ứng dụng` | `Cần khởi động lại ứng dụng` |
| `Thực hiện Audio Export` | `Export Audio` |
| `Vui lòng nhập tên` | `Nhập tên` |
| `các hành động` | `Action` |
| `đã chứa` | `có` |
| `sẽ bị gỡ bỏ` | `sẽ mất` |
| `đang có hiệu lực` | `đang dùng` |
| `Có thể do vấn đề về quyền ghi` | `Có thể do không có quyền ghi` |
| `Thư mục Project chỉ cho phép đọc` | `Thư mục Project chỉ đọc` |
| `làm mất hiệu lực` | `làm hỏng` |
| `Ngưỡng cho phép đo` | `Ngưỡng đo` (*threshold* ≠ *allowed threshold*) |
| `dấu bình hủy bỏ` | `dấu bình khử` |
| `Tái sử dụng` | `Dùng lại` |
| `hộp thoại file` | `cửa sổ duyệt file` |
| `audio stream` | `Audio Stream` |

Giữ **mạo từ** khi làm chủ thể, bỏ khi thừa.

**`inactive` đổi nghĩa theo ngữ cảnh.** Bốn nghĩa: không dùng / chưa bật (Version,
Project) · đang tắt (Cycle) → `tắt` · tính năng bị hỏng → `chưa chọn` (đối chiếu bản
Đức) · đĩa hỏng → `đang chạy không bình thường`. `đang không hoạt động bình thường` =
dịch máy cho "not working normally".

**Cubase GHÉP CHUỖI Ở RUNTIME — giá trị tiếng Việt lọt thẳng vào UI.** Đợt 170, người
dùng chụp màn hình thấy `Thêm Nhóm Track`, `Thêm Hop âm Track`, `Thêm Transpose Track
Track`. Menu là khuôn **`Add %s Track`** → `Thêm %s Track`, và `%s` lấy từ **key đơn
lẻ**. `Add Group Track` → `Thêm Group Track` đúng, nhưng key `Group` lại là `Nhóm`.
- **Key đơn lẻ (`Group`, `Chord`, `Folder`, `TransposeTrack`…) quan trọng ngang chuỗi
  dài** — giá trị của nó đi vào UI qua `%s`.
- **`TransposeTrack` (không space)** là chuỗi điền `%s`; 8/9 ngôn ngữ gốc không có
  chữ "track" (de=`Transposition`, jp=`移調`). Giá trị đúng: `Transpose`.
- **Đã quét toàn bộ khuôn:** 265 chuỗi có `%s`, 49 có danh từ
  Track/Channel/Bus/Event/Part/Clip/Lane/Zone — **đều đúng**. 152 key đơn lẻ giá trị
  tiếng Việt (`Color`, `Align`, `Create`…) là nút độc lập, không ghép.
- **Nhãn ghép ở giao diện, không có trong map:** `Thời gian ghi từ đá` (Transport),
  `Đầu vào/E` (bị cột hẹp cắt) — Cubase ghép/chỉnh lúc runtime. **Đừng đi tìm trong
  `vi.json`.**
- **Bài học sâu:** 169 vòng kiểm đều pass mà UI vẫn có 4 lỗi. Công cụ kiểm bản dịch,
  **không kiểm cách Cubase ghép chuỗi**. Chỉ nhìn màn hình mới thấy.

**`ui-navigation.json` LUÔN THẮNG — đây là bẫy merge.** `merge_maps.py` dùng
`sorted()`, mà `u` > `r` nên file này đứng **sau** mọi `round_*.json`. Sửa ở
`round_NNN.json` mà key đó có trong `ui-navigation.json` sẽ **bị ghi đè im lặng**
(đợt 168: 3 chuỗi `Add … Track to Selected Tracks…`). `vi.json` vẫn đúng về kiểm
tra nên không báo lỗi. **Sửa thì sửa cả hai file**, hoặc xoá key ở
`ui-navigation.json`. Luôn merge xong đối chiếu lại giá trị.

**Rút gọn: đừng để bộ dò tự cắt.** Đợt 166 thử cắt `Vui lòng` bằng regex và nó làm
**hỏng 11/33 chuỗi** — chữ thường sau `.` và sau `\n\n`. Vì tiền tố lọc không biết
vị trí câu. **Cắt bằng tay, rồi kiểm hoa/thường bằng assert.** Chỉ dùng regex để **tìm
ra ứng viên**, không để ghi.

## 6. Bất biến kỹ thuật — giữ nguyên 100%

Placeholder `%s %d %i %.3f` · dấu hai chấm · `?` `!` `.` · dấu ba chấm · **số dòng
mới** · **khoảng trắng đầu/cuối**. Xuống dòng bằng **`\n` hai ký tự**, không phải
newline thật. Bộ dò placeholder phải khớp cả `%1.0f` và `%02d` —
`r'%(?:\.\d+)?[a-zA-Z%]'` bỏ sót cả hai; dùng `cubelib.placeholders.PLACEHOLDER`.

- **`[RM]` thuộc về KEY, tuyệt đối không được nằm trong giá trị** — nó sẽ **hiện lên
  màn hình** cạnh nhãn ở read-mode. Cả tám nhà cung cấp đều dịch cặp đó giống nhau và
  không ai đặt nhãn vào giá trị. Marker `[RM] [Score View Option] [Key] [vocal]` là
  marker riêng của Cubase, nằm trong key — giữ nguyên.
- **Key ≠ English.** Cột 1 và cột 2 của TSV khác nhau: `AppKey[Key]`→`Menu`,
  `Delete Tool`→`Erase Tool`, `Check Files`→`Find Missing Files` — theo **key**.
  283 chuỗi lệch, đã kiểm độ dài: **0 chuỗi rút ngắn quá 60%**, tức không rơi nội dung
  chỗ nào.
- File Cubase đang chạy: bản **`full` 5.322.854 byte** (đủ 9 ngôn ngữ + `vi`). Bản rút
  gọn `translation_vi_en.xml` chỉ 1.443.882 byte, chỉ dùng khi `-Variant en` —
  **`install.ps1` mặc định lại là `en`**, cài nhầm thì Cubase có thể không hiện tiếng
  Việt. Khi kiểm bằng ảnh chụp, **luôn `-Variant full`**. `install.ps1` ghi `.bak` cạnh
  mọi file. PowerShell báo `String: 0` là **sai** (`.String` trùng `System.String`) —
  kiểm bằng Python.

## 7. Bẫy công cụ

- **Dải ký tự tiếng Việt.** `[\u00c0-\u024f\u1e00-\u1eff]` là đúng. `[Ā-ỿ]` là **sai** —
  tiếng Việt nằm ở `U+00C0…U+00FF`, **dưới** đầu khoảng đó, và 9 công cụ đã âm thầm
  chỉ xem một phần bản dịch.
- **Bẫy ASCII — đã giết nhiều bộ dò, gặp lại 5 lần.** `trong`, `cho`, `khi`, `ghi`,
  `theo`, `vao`, `voi`, `hay` là tiếng Việt viết bằng **ký tự ASCII thuần**. Hệ quả:
  (a) cổng `HAN.search(v)` làm **những bản dịch tệ nhất** — dựng từ đám từ chức năng —
     không vượt qua; (b) không thể phân biệt "từ Anh lọt" bằng ký tự, nên
     `audit_readability2.py` đã báo **1.171 báo động giả** với 5 "từ Anh phổ biến
     nhất" đều là tiếng Việt. Dùng **từ điển tiếng Anh tường minh** và in ra **từ đã
     rút gọn** để đọc tay (`audit.py fragments`), không đếm.
- **Bẫy hoa/thường.** Kiểm bằng `tok[0].isupper()`, **không** dùng lớp ký tự
  `[A-ZÀ-ỸĐ]` — vì `đ` (U+0111) **nằm trong** dải `À-Ỹ`, nên bản dùng lớp ký tự báo
  động giả cho `đã`, `đó`, `đối`.
- **`[A-ZÀ-ỸĐ]` cho chữ thường cũng vậy** — bộ dò hoa/thường phải dùng `0x00C0–0x00FF`
  + `0x1E00–0x1EFF`, và phải cho vị trí 0 vào tập "đầu câu", nếu không mọi chuỗi đều báo.
- **"Bộ dò báo 0" và "bộ dò hỏng" trông giống nhau.** Thử một giá trị biết đúng vào bộ
  dò trước khi tin kết quả. `tools/tests/test_detectors.py` làm việc này cho 24 bộ dò.
- **Cổng `needs_src` sai làm bộ dò chết âm thầm.** `numbers` từng báo 0 vì đánh dấu
  `needs_src=False`, nên `src` rỗng và **mọi giá trị đều bị bỏ qua** — số 0 trông rất
  đẹp và hoàn toàn vô nghĩa.
- Bộ dò đếm CÂU bỏ sót vế mất **ở giữa** câu (số dấu chấm vẫn khớp) — phải so **số
  dòng**; `build.py punct` đã nối vào `build.py`.
- `all_strings.tsv` có thể **cắt cụt key dài**; hai dòng có thể trùng tiền tố 60 ký tự.
  Khi tra bằng key, yêu cầu **đúng một** ứng viên — dùng `_full()`, không dùng `src[k]`.
- **Đừng dùng độ dài làm tín hiệu.** Đợt 88 đo rồi sai (§8.10); đợt 195 thử lại với
  "so với trung vị 8 anh em", ra 108 và **đuôi toàn báo giả** — vì tiếng Việt gọn hơn
  Đức và Nga. Lặp lại lần nữa cũng vậy.
- **Bốn báo động giả đã biết:** (1) `Tên Channel`/`Số Note` trông đảo nhưng đúng;
  (2) `gán vào`/`chuyển vào` cần `vào`; (3) `lặng` nằm trong `dấu lặng`, `Over` trong
  `Cross-Over` khớp `\b` sau gạch nối; (4) `build.py style` cấm ngoặc `(ms)` ở cuối dù
  là đơn vị — sửa **giá trị**, đừng sửa luật.
- **Bộ dò báo động giả nhiều lần còn tệ hơn không có bộ dò:** nó dạy người đọc bỏ qua
  báo cáo. `audit.py --all` tách **LỖI THẬT** khỏi **DẪN ĐƯỜNG** chính vì vậy — 10 bộ
  dò luôn ra danh sách để đọc tay và không bao giờ im.

## 8. Bài học về cách sửa

1. **Tra bằng TỪ, không tra bằng key.** Thấy thuật ngữ trong chuỗi mới thì `grep` **từ
   đó** trong `vi.json` và sửa **mọi** chỗ khớp. Sửa 1/5 rồi dừng là thêm biến thể.
   Luật viết trong AGENT.md **không tự lan** — phải quét lại bằng TỪ khóa luật.
2. **Bảng thuật ngữ viết sai không tự báo lỗi.** Sửa **cả bản dịch lẫn dòng luật** —
   `Key Signature | hóa biểu` đã sinh 8 chuỗi sai vì luật sai.
3. **Bảng sửa cũ LÀ một lệnh ghi đè.** Đợt 193 dọn 149 script 1-lần vào
   `tools/archive/` vì lịch sử cho thấy `glossary_readthrough.py` chạy cuối đã xoá
   `Lệnh` của `fix_reading4.py` mỗi lần chạy. **Đừng chạy lại chúng.**
4. **Sau khi ghi, đếm lại từ mình vừa xoá** — không thì bản sửa tạo ra chính lỗi nó đi
   sửa. Kiểm `NOT IN CUBASE` **trước** khi `--write`. **Hai từ Anh đứng cạnh nhau thì
   nguy hiểm gấp đôi** — dịch từng từ một (`Duration` cạnh `Field`).
5. **Luật và bản dịch lệch nhau ở quy mô lớn thì luật có thể sai, không phải map.** Đo
   trước, sửa luật, đừng sửa hàng chục chuỗi.
6. **Một bộ dò đúng vẫn tạo báo động giả nếu thiếu ngữ cảnh.** `grep` chỉ ra chỗ cần
   nhìn, không quyết định đúng sai.
7. **Đừng lẫn các bộ dò tên gần giống.** `audit.py outlier` tìm chuỗi lạc khỏi gia
   đình; `audit.py terms` hỏi 9 anh em về một thuật ngữ; `audit.py quality` kiểm thuật
   ngữ xung đột. Ba việc khác nhau.
8. **Chỉ thêm mẫu cấm khi cách dịch sai là cách dịch DUY NHẤT.** `thẻ` bắn 13 chuỗi
   (`Thiết lập thẻ` = Tab, đúng), `vùng` bắn 213 (`vùng chọn` đúng).
9. Lỗi đảo trong câu dài, cách diễn đạt khó đọc, mất câu, sai nghĩa chỉ lộ ra khi **đọc
   thật**. Đọc tay là bước cuối: `tools/read.py long|short <miền> <bắt đầu>`, và
   `read.py page <bắt đầu>` nếu cần **không bỏ sót** chỗ nào.

10. **ĐỪNG dùng số liệu thay cho việc đọc. Hai vòng đã làm sai theo đúng cách đó.**
    - Đợt 88 lọc bằng *tỉ lệ số từ*, ra 380 chuỗi "dài". **Sai**: 3.234 chuỗi có
      nguồn ≥ 25 ký tự thì trung vị bản dịch **ngắn hơn 2 ký tự**, lệch dài nhất
      `+21c`, **không chuỗi nào dài hơn 30 ký tự**. `clarity.py long` báo giá trị dài
      nhất 328c và *in ra trông dài hơn tiếng Anh* — nhưng nó **cắt cụt** chuỗi Anh:
      nguồn dài 371c, tức bản dịch **ngắn hơn 43c**. Cả hai đúng, một cái hiển thị sai.
    - Đợt 89 đo tiếp, giả thuyết *mất ngữ cảnh vì key chỉ là chuỗi Anh*. **Cũng sai**:
      83 chuỗi Anh dùng ở nhiều hơn một entry, và **không chuỗi nào** khác vai trò.
    - Cái thật, chỉ lộ ra khi **đặt hai chuỗi cạnh nhau**: `Import Audio File` →
      `'Import file Audio'` cạnh `Import Audio Files` → `'Import File Audio'` — lệch
      hoa/thường, mỗi cái rời ra đều đọc được.
    - **Cơ:** key là *chuỗi tiếng Anh*, không id, không đường dẫn, không vai trò. Nên
      **gia đình = các chuỗi cùng nói một thứ**, cách tìm gần nhất là **từ đầu tiên**:
      `tools/family.py <từ>`.
    - Khi đọc: `Channel` và `Channel ` là **hai key khác nhau**, giữ khoảng trắng là
      đúng. `Db` cạnh `dB` là **chính Steinberg viết**.

11. **PHÉP THỬ RỖNG LUÔN PASS. Đừng đọc 0 là sự thật — bốn lần đã hỏng.**
    - Đợt 95: tìm `"chỉ dẫn diễn tấu"` ra **0**, tưởng đã sạch. Thật ra giá trị bắt đầu
      bằng `Chỉ` **hoa**, tôi tìm chuỗi **thường**. Đợt 104 dính lại y hệt, hai lần.
    - Đợt 96: quét `"bộ lọc"` chỉ trong khoá **ngắn hơn 34 ký tự**, bỏ sót 15 chỗ, rồi
      định sửa cụm `Filter` theo tỉ lệ 17/32. Tỉ lệ 51/49 không phải bằng chứng.
    - Đợt 98: đếm cụm `Template` bằng `if 'emplate' in v` — nhưng **giá trị** là tiếng
      Việt (`Mẫu`), chữ đó nằm ở **khoá**. Đúng phải là `if 'emplate' in k and 'mẫu' in v`.
    - **Cơ chung:** mọi phép thử tìm phải có **chốt rỗng** — tìm ra 0 chỗ thì **báo
      lỗi**, không được coi là "đã sạch". Và **đừng so với con số viết tay**: đợt 98
      đếm tay ra 10, thực tế 11; hãy so **trước với sau** trên cùng một cách đếm.
    - Cùng lớp: `score.FORBIDDEN` là `dict` khoá **số** còn test tra `c` là **ký tự** →
      không bao giờ khớp.
    - **`.lower()` không bỏ dấu.** "lượt" là **một** ký tự (`ự` U+1EE3), không phải hai.
      Viết kim ASCII `luot` thì **không bao giờ khớp** "lượt". Đúng: kim tiếng Việt +
      `.lower()` cả hai bên.
    - **Trước khi sửa ứng viên, tra `<us> gốc`.** `Switch: Activate Speakers` trông như
      lỗi copy-paste nhưng **đúng**; `Assume Skipping` lệch nghĩa với cả 8 ngôn ngữ.

12. **ĐỪNG gọi một sửa đổi là "đối xứng" trước khi tra anh em. Đợt 200 tôi tự
    làm rồi tự nhân bản.** Câu `All parts in editor are used.` là **dòng trạng thái**
    trong Info Line, tôi đổi thành `Dùng tất cả Part trong Editor.` — đọc ra là
    mệnh lệnh. Ở đợt 199 tôi thấy anh em `All clips in editor are used.` cùng
    dạng, tôi gọi đó là *"đối xứng hoàn hảo"* và **nhân bản lỗi**. Người dùng
    bắt lỗi. Bài học:
    - **Sửa 1 chuỗi phải hỏi anh em nó đang nói gì — câu nào trong nhóm đang
      ĐÚNG thì câu đó là mẫu.** Ở đây `All audio files are used` →
      `Tất cả file Audio đều đang dùng` **đã có sẵn** và đúng; 5 chuỗi, 1 đúng,
      4 sai. Mẫu nằm ngay trong map mà tôi không đọc.
    - **Câu trạng thái ≠ mệnh lệnh.** `are/is + <từ>` ở nguồn là *đang* gì đó;
      tiếng Việt phải giữ `đang`. Bộ dò `status` canh việc này (56 chuỗi trạng
      thái, dẫn đường, có chốt chống báo giả: **nguồn cũng ra lệnh thì giá trị
      ra lệnh là đúng**).

## 9. Quy trình kiểm tra

Dừng ngay khi một bước báo lỗi.

**Mười công cụ, đủ dùng.** `tools/*.py` còn lại đúng 10 file dịch; nhóm
`inject_wavehook` / `memscan` / `set_prefs`… là tính năng khác.

```powershell
python tools\merge_maps.py --check      # gộp batch -> vi.json, bắt key trùng
python tools\build.py style             # 5 luật cứng (xem dưới)
python tools\build.py punct             # ? ! ; ... xuống dòng, khoảng trắng đầu/cuối
python tools\audit.py                   # liệt kê 24 bộ dò
python tools\audit.py --all             # chạy hết, TÁCH lỗi thật khỏi dẫn đường
python tools\audit.py leak              # từ chức tiếng Anh còn sót trong câu Việt
python tools\audit.py numbers           # số trong nguồn phải còn trong giá trị
python tools\audit.py fragments         # TỪNG TỪ Anh còn lại, rút gọn để đọc tay
python tools\audit.py terms             # thuật ngữ ca zh và jp đều giữ, ta đã dịch
python tools\audit.py quality           # chưa dịch hẳn + thuật ngữ xung đột + giới từ đảo
python tools\audit.py quotes            # tên trong ngoặc kép lệch với nhãn nó trích dẫn
python tools\audit.py rm                # khoá [RM] lệch với khoá gốc
python tools\audit.py gloss             # ghi chú phân biệt của extractor lọt vào bản dịch
python tools\audit.py dropped           # mất câu so với nguyên văn
python tools\audit.py same_en           # một tiếng Anh, hai bản dịch
python tools\audit.py mojibake          # U+FFFD (thêm --write để vá)
python tools\audit.py outlier           # chuỗi lạc khỏi gia đình thuật ngữ
python tools\audit.py status            # câu TRẠNG THÁI (EN) bị dịch thành mệnh lệnh (VI)
python tools\dupes.py keys              # khoá gần trùng -> hai cách viết
python tools\dupes.py values            # hai key KHÁC nhau -> một giá trị
python tools\clarity.py                 # long  dài  |  hard  khó đọc
python tools\tests\run.py               # 172 test: bất biến + độ nhạy + bộ dò
python tools\family.py <từ>             # đọc cả gia đình chuỗi cùng từ đầu
python tools\group_by_offset.py         # nhóm chuỗi theo vị trí trong .rdata
python tools\group_by_offset.py -k <từ>  # cụm của một chuỗi — BƯỚC 1, mạnh nhất
python tools\group_by_offset.py -c <tên> # đọc một cụm
python tools\group_by_offset.py --gap 200  # cụm mịn hơn (mặc định 4000)
python tools\group_by_offset.py --ambiguous # chuỗi quá chung nên bị lo
python tools\group_by_offset.py --uncovered # chuỗi không có literal trong code
python tools\read.py long|short <miền> <bắt đầu>   # đọc tay
python tools\read.py page  <bắt đầu> [số]          # đọc TUẦN TỰ, không lọc
python tools\read.py inspect <từ>                   # một khoá, đủ 9 ngôn ngữ gốc
python tools\check_translation_build.py # build\translation_vi.xml = bản gốc + <vi>
python tools\score_instruments.py check # Score Editor: trùng key + 4 bất biến
python tools\build.py                   # sinh build/translation_vi.xml + validate
pwsh -File scripts\install.ps1 -Action install -Variant full
```

**`check_translation_build.py` giữ đúng tiền đề của cả dự án.** Nó chứng minh bằng cơ
chế, không phải bằng lời: file build **bỏ các dòng `<vi>` đi thì ra đúng bằng
`keys\translation_original.xml`, từng byte**; 10.737 entry, mỗi entry đúng 10 khối
`<us>…<ru><vi>`; không `<us>…<ru>` nào bị đổi; mọi `<vi>` bằng đúng `vi.json`; và dòng
`<vi>` thụt lùi **đúng bằng 9 anh em** nó.

**5 luật cứng của `build.py style`**: (1) cấm ngoặc chú thích cuối trừ khi key gốc có;
(2) cấm dịch thuần Việt thuật ngữ §1 — **64 mẫu trong `terms_do_not_translate.json`**;
(3) placeholder phải khớp; (4) giá trị không rỗng; (5) cấm `[RM]`. Luật 5 **duy nhất
không mang tính thẩm mỹ** — nó ngăn chữ lên màn hình.

**`tests/test_detectors.py` là bài test quan trọng nhất trong kho.** Nó đặt lại giá trị
cũ của **từng lớp lỗi đã thật sự sửa** và hỏi bộ dò có bắt không, rồi khẳng định các
điểm mù **vẫn còn mù**. Bản dịch sạch **không** chứng minh bộ dò mạnh — bản dịch sạch
và bộ dò mù nhìn từ bên ngoài giống hệt nhau.

## 10. Score Editor — bộ luật đặt tên nhạc cụ

Score Editor là `ScoringEngine.dll` (lõi Dorico), **không** dùng `translation.xml`. Hai
loại file, hai quy trình:

| file | công cụ | quy trình |
| --- | --- | --- |
| `instrumentnames_vi.xml` | `tools/score_instruments.py` | `import` → `build` → `check` |
| `strings_vi.qm` | — | chưa làm |

`instrumentnames_en.xml` có 624 entity và **1.126 chuỗi phân biệt** trong 3.115 ô
(`uiName`, `singularFullName`, `singularShortName`, `pluralFullName`,
`pluralShortName`). Chỉ 5 ô đó được dịch; `<name>`, `<gender>`, `<inheritanceMask>`,
`<parentEntityID>` **giữ nguyên ở mọi ngôn ngữ**. Viết bằng **cắt chuỗi**, không
re-serialise: file dùng CRLF, tab, `<?xml version="1.0" ?>`, `<x/>` cho ô rỗng, và
entity `aluphone` xếp `<name>` **trước** `<entityID>`.

### 6 luật — lấy từ 9 catalogue Steinberg, không phải từ khẩu vị

1. **Tên riêng không dịch; tính ngữ mô tả thì dịch.** `Banjo`, `Charango`, `Cuatro`,
   `Alphorn`, `Cimbasso`, `Didgeridoo`, `Bansuri`, `Guitarrón`, `Wagner Tuba` giữ
   nguyên. Còn `Acoustic`, `Electric`, `Fretless`, `Classical`, `Jazz`, `Steel-string`,
   `Semi-acoustic`, `Resonator` và tên nước thì dịch: `Electric Guitar` →
   **`Guitar điện`**, `Classical Guitar` → **`Guitar cổ điển`**, `Resonator Guitar` →
   **`Guitar cộng hưởng`**.
2. **Chữ viết tắt không bao giờ đổi.** ~130/320 chuỗi của `brass`+`wind` là chữ viết
   tắt, và cả 9 catalogue đều giữ nguyên: `Tbn`, `Tpt`, `V. Tbn.`, `Cbsn`, `Min-bsn`,
   `Ac. B. Gtr`, `Ban.`, `Dul.`. Chúng là nhãn cố định cho cột tên bè — dài thêm là vỡ
   bố cục. **Số nhiều của chữ viết tắt thì rút gọn**: `Ac. B. Gtrs` → `Ac. B. Gtr`.
3. **Tiếng Việt không có số nhiều, nên số nhiều lấy đúng từ của số ít.** `Pianos` →
   `Piano`, `Mezzo-sopranos` → `Mezzo-soprano`, `Basses` → `Bass`, `Cajons` → `Cajon`.
4. **Từ bên trong ngoặc thì dịch, viết hoa chữ đầu, giữ ngoặc.** Đây là khuôn mẫu mà
   40 chuỗi seed đã viết ra: `Bongo (High)` → `Bongo (Cao)`, `Tenor Drum
   (Medium-high)` → `Trống Tenor (Trung bình cao)`, `Tabla baya (larger)` → `Tabla baya
   (Lớn hơn)`. Nhưng `(Quinto)`, `(Requinto)`, `(Super Tumba)`, `(pedal)` **giữ** —
   đó là tên của biến thể, không phải thanh bậc.
5. **Thanh bậc đã là mượn ngữ thì giữ nguyên chỗ nó đứng.** `Alto Balalaika`,
   `Bass Balalaika`, `Contrabass Balalaika`, `Prima/Secunda Balalaika`,
   `Piccolo Domra`, `Tenor Lute`, `Tenor Banjo`, `Horn (alto)`, `Horn (basso)`. Đức
   dịch giữ nó ở đầu (`Alt-Balalaika`, `Kontrabass-Balalaika`), Nhật cũng vậy. Không
   engine nào dịch cả, nên ta cũng không.
6. **Tên miền dịch khi tiếng Việt có từ thật.** `Brass` → `Bộ đồng`, `Wind` → `Gió`,
   `Keyboard` → `Bàn phím`, `Voice` → `Bè`, `Triangle` → `Tam giác`, `Whistle` → `Còi`;
   nhưng giữ `Percussion`, `Drum`, `Snare`, `Tambourine` — vì tiếng Việt không có từ nào
   dùng được cho chúng. Vì vậy `Strings` → `Bộ dây`, `Woodwind` → `Bộ gió`, còn
   `Drum Set` → `Drum Set`.

### Tiếng Anh lọt là hợp lệ, và đó là điểm cần nói rõ

**591 / 1.126 chuỗi (52%) giữ nguyên tiếng Anh** — và đây là kết quả đúng, không phải
chỗ sót. Người Việt gọi "guitar", "piano", "kora", "cổ điển" chứ không gọi "đàn
ghi-ta". Vì thế **đừng** dùng `audit.py leftover` vào `translations/score/`, và **đừng**
ép mọi giá trị khác tiếng Anh. Trái lại là sai: `Snare` → `Trống Snare`? Không — `Snare`
giữ nguyên, còn `Side Drum` → `Trống phụ` là đúng, vì "snare" không có từ Việt còn
"drum phụ" thì có.

### Bốn bất biến của `score_instruments.py check`

Nó dừng ngay khi lỗi:

1. Giá trị không rỗng, không ký tự điều khiển, không U+FFFD, không khoảng trắng
   đầu/cuối. **Ngoại lệ**: map giống hệt thì miễn — vài ô gốc mang khoảng trắng cuối
   (`<O. M. >`) và giữ nguyên là câu trả lời đúng.
2. Mọi key phải có thật trong `instrumentnames_en.xml` — lỗi gõ trong batch không được
   lọt.
3. Giá trị chỉ được **ngắn hơn** key bằng đúng đuôi số nhiều (`s`/`es`/`n`).
   `Agogôs` → `Agogô` hợp lệ, `Charangos` → `Charang` là bậy.
4. Số nhiều đã dịch phải khớp số ít. Map **giống hệt** được miễn: số nhiều tiếng Anh
   giữ nguyên tiếng Anh không phải chỗ lệch của ta. Ngoại lệ có tên: `Voice`/`Voices` —
   một dòng hát vs cả phần bè.

### Hai lỗi trong chính code của dự án này

Do `tests/test_score.py` phát hiện — đúng loại lỗi mà §3 cảnh báo, nên ghi lại:

- `score.FORBIDDEN` là `dict.fromkeys` của **số**, còn chỗ kiểm tra lại tra
  `c in FORBIDDEN` với `c` là **ký tự**. Khớp không bao giờ xảy ra, nên `check_text`
  trả về một chuỗi có byte NUL. Nay là `frozenset` ký tự.
- `source_strings` đếm `uiName` và `singularFullName` là hai người dùng, nên
  `--status` báo đội gấp đôi số bè mỗi chuỗi tiết kiệm được. Nay khử trùng theo entity.

Hai lỗi **trong file của Steinberg**: 8/8 file không-Anh giữ entity
`instrumentname.pitchedpercussion.aluphone` ở `kEnglish`; file Đức còn thêm
`marching.snare.drum.rim`. Cùng cái entity mang `<customVariantString/>` mà Steinberg
thêm tay vào bản tiếng Anh rồi copy sang các bản dịch mà quên dán nhãn lại. Thêm nữa,
`<language>` xuất hiện **625 lần** (một ở đầu, 624 ở entity), và 5 ô tên rỗng
(`cajon.low` mất short/plural, `clarinet.contra.alto.eflat` mất plural).
`score_instruments.py build` ghi **đồng nhất** cả 625 marker thành `kVietnamese` và
liệt kê `mis_tagged`, để lỗi của nguồn không bị sao chép. Chi tiết ở `docs/RESEARCH.md`.

## 11. Cubase Hub — `hubservice.dll`

Cubase Hub là module độc lập tại `Components\hubservice.dll`. Nó sở hữu bảng XML gồm
**89 chuỗi riêng** (chứa `Create Empty Project...`, `Recent`, `Tutorials`, `Deals`,
`User Manuals`, `Hub Settings`, `Choose File...`) nhúng trực tiếp trong binary. Các
chuỗi này không nằm trong `translation.xml` chính; khi chạy tiếng Việt nếu chưa patch
bảng XML trong DLL thì các nhãn riêng của Hub sẽ tự động fallback về tiếng Anh `<us>`.
Chi tiết kỹ thuật và danh sách chuỗi xem tại `docs/HUBSERVICE.md`.