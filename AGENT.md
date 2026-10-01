# AGENT.md — Quy tắc bắt buộc khi dịch Cubase 15

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ. Chuẩn hoá
theo `keys/all_strings.tsv` (10.737 cặp key ⇄ English). Bản rút gọn từ 2.442 dòng —
lịch sử 80 đợt đọc tay ở `…\Temp\opencode\AGENT.md.bak`, đọc khi cần biết *vì sao* một
luật tồn tại, không phải để tra luật.

## 1. Kiểu dịch

- **Động từ / thao tác / trạng thái / giao diện** → Việt hoá ngắn gọn: `Thêm`,
  `Xóa`, `Gỡ bỏ`, `Nhân bản`, `Sửa`, `Mở`, `Lưu`, `Bật`, `Tắt`, `Ẩn`, `Hiện`,
  `Chọn`, `Tới`, `Đảo ngược`.
- **Thuật ngữ âm thanh & DAW** → **giữ tiếng Anh**, ghép vào ngữ pháp tiếng Việt.
- **Bảng màu (Color Setup / Palette)**: giữ nguyên tiếng Anh cho toàn bộ tên màu
  (White, Black, Red, Green, Blue, Yellow, Orange, Magenta, các biến thể Dark/Light,
  Black 50/70, Gray 5..90) theo yêu cầu người dùng. Các nhãn chức năng vẫn dịch
  bình thường (`Color` -> `Màu`, `Colors` -> `Màu sắc`, `Colorize` -> `Tô màu`).
- **TUYỆT ĐỐI KHÔNG**: ngoặc chú thích ở cuối (`Thêm track (Add Audio Tracks)` — SAI,
  nhãn tràn chữ). Chỉ giữ ngoặc khi **key gốc đã có**, và khi đó dịch trong ngoặc.
  Cũng không dịch thuần Việt: `Automation`, `Bounce`, `Track`, `Clip`, `Freeze`, `Quantize`.

## 2. Thuật ngữ bắt buộc

**DAW — giữ tiếng Anh (160 từ).**

68 từ cốt lõi: Track · Channel · Bus · FX · Group · VCA · Insert · Send · Slot · Fader · Pan · Solo · Mute · Meter · Metronome · Click · Marker · Locator · Automation · Clip · Event · Part · Pool · Quantize · Snap · Grid · Bounce · Render · Freeze · Warp · Velocity · Pitch · Note · Chord · Tempo · Timecode · Bar · Beat · Fade · Punch · Buffer · Latency · Sample Rate · ASIO · VST · Plug-in · Preset · MixConsole · Inspector · Zone · Export · Import · Arranger · Chain · Step · Lane · Pattern · Expression · Voicing · Tension · Articulation · Layout · Map · Mapping · Script · Machine Control · Talkback · Cue
>
> Vẫn là **160 từ** (`terms_do_not_translate.json`): 68 + 90 + 2 từ Score ở dưới
> (`Key Signature`, `Time Signature`). Năm 2024 tiêu đề ghi "70" nhưng list chỉ có
> 68; đợt 161 gỡ `Voice` nhưng không sửa tiêu đề. **Tính từ file, không tin tiêu đề.**

90 từ mở rộng: Project · Audio · Controller · Cycle · Bypass · Remote · Effect · Monitor · Video · Routing · Bank · Loop · Transpose · Loudness · Assistant · Media · Strip · Focus · VariAudio · SyncStation · Player · Score · Logical · Listen · Region · Band · Crossfade · Clock · Panner · Workspace · Snapshot · Room · Hitpoint · Gain · Surface · Sampler · Transport · Retrospective · Learn · Shuttle · Pitchbend · Extension · Wave · Modulation · Frame · Dynamics · Modulator · Factory · ASIO-Guard · MediaBay · Mixdown · Layer · Ruler · SysEx · High-Cut · Side-Chain · Profile · Macro · Pre-roll · Phase · Tuning · Trim · Patch · Multi-Channel · Low-Cut · Word · Folding · Post-Fader · Dynamic · Pedal · Permission · Pre-Fader · Subsection · Post-roll · Downmix · Module · Count-In · CCMode · NoteExp · Latch · Thru · Z-Axis · Remote-Control · AudioWarp · Transformer · Scripting · Cache · Studio · Offline · Mixer

> ~~`Time Signature` và `Chord Symbols` đã gỡ khỏi danh sách vì §3 bắt dùng tiếng Việt;
> map theo §3 (49 chuỗi)~~ **— hủy (đợt 171).** Rounds 146–171 đã sửa hết 49 chuỗi
> đó sang `Time Signature` giữ EN, khớp danh sách Score bên dưới và khớp
> `keep_english`. `Chord Symbols` chỉ còn 2 chuỗi, đều giữ EN. Bỏ dòng này thay
> vì để lại nó là một luật ngược với map — đúng loại vi phạm §8.2.
> 90 từ "mở rộng" đo trên 10.737 chuỗi:
> nguồn ≥5 lần, bản dịch dịch ≤2 lần (`terms_do_not_translate.json`).
>
> **Cách tìm từ nên cấm** — đừng hỏi "thuật ngữ nào đã bị dịch" (16 ứng viên, **không
> cái nào sai**). Hỏi: **thuật ngữ nào có MỘT chuỗi lệch khỏi gia đình?** — 18 lỗi.

**Bàn nhạc (Score Editor) — giữ nguyên thuật ngữ chuyên ngành:** Vì Score Editor là
môi trường ký âm và khắc bản nhạc (notation/engraving) chuyên sâu theo chuẩn quốc tế,
toàn bộ thuật ngữ chuyên ngành ký âm quốc tế được giữ nguyên tiếng Anh (Staff/Stave ·
Clef · Barline · Stem · Beam · Accidental · Rest · Grace Note · Notehead · Arpeggio ·
Tuplet · Glissando · Trill · Fermata · Key Signature · Time Signature · Chord Symbols ·
Rhythm Dot · Ledger Line · Slur · Tie · Inversion · Interval · Swing · Cadence · Slash).
Động từ thao tác và giao diện chung vẫn Việt hóa tự nhiên: Thêm, Xóa, Ẩn, Hiện, Sửa,
Thiết lập, Mở, Đóng, Lật (Flip)...

> **2 từ trong danh sách không tồn tại trong Cubase 15** (đợt 171 đo: 0 key, 0 giá
> trị): `Fermata`, `Ledger Line`. Giữ trong luật để sau này dùng được — nhưng **đừng
> đi tìm để sửa**, sẽ tốn thời. `Grace Note` chỉ có 2 chuỗi và đang trộn
> (`Unslashed Grace Note` giữ EN, `Slashed Grace Note` → `Nốt Grace có Slash`).
> Còn 3 từ Score khác đã kiểm là giữ EN đúng: `Clef`, `Tuplet`, `Rhythm Dot`.
>
> **6 từ thêm ở đợt 172 — vì tìm thấy chúng ĐANG bị dịch sai nghĩa:**
> `Slur` (→"dấu luyến", *luyến* = lỗi lầm), `Inversion` (→"thể đảo", *thể* = cỡ vải),
> `Interval` (→"khoảng"/"quãng", phải thống nhất), `Tie` (→"dấu nối"), `Swing`,
> `Cadence`. **Bài học: danh sách §2 phải khớp với map, và cả hai đều phải kiểm** —
> viết luật rồi tin là xong là lỗi nguồn (đã xảy ra ở `Time Signature`).
> Đã sửa 19 chuỗi. Riêng `Chord` giữ nguyên `hợp âm` — xem bảng bên trên.

`System` và `Bar` theo ngữ cảnh: Score Editor → `System` / `Bar`; ngoài đó →
`hệ thống` / `thanh`. Từ HLV cũng giữ bên HLV: `con trỏ`, `bè`, `phát lại`, `hợp âm`.

> `Voice` **không** giữ tiếng Anh — đã gỡ khỏi danh sách Score Editor ở trên (đợt
> 161). Gia đình `Voice` đo được 36 chuỗi, 33 chuỗi dịch `bè`; 9 ngôn ngữ gốc đều
> dùng nghĩa *thanh/giọng* (zh 声部, de Stimme, ru голос). Dòng này trước đây liệt
> `Voice` vào danh sách giữ EN, làm cho 2 chuỗi `Single Voice` lạc khỏi gia đình.

## 3. Bẫy thuật ngữ — đọc sai ở đây là hỏng

| Sai → Đúng | Vì sao | Sai → Đúng | Vì sao |
|---|---|---|---|
| `Duration` → **thời lượng** | *trường độ* = ngành/khoa | `New` → **mới** | không phải *Tạo* |
| `Word Clock` → giữ `Word` | *Word Spacing* → *Khoảng cách từ* đúng | `Deactivate` → **Tắt** | *Hủy* = *cancel* |
| `External` → giữ `External` | *outside* = nghĩa **đối lập** | `Doubles` → **Note trùng** | ghi trùng, không dài gấp đôi |
| `Material` → **chất liệu** | không phải *tư liệu* | `Notehead` → giữ **Notehead** | thuật ngữ chuyên ngành ký âm |
| `Retrospective Record` → giữ Anh | đợt 72 đảo lại; *hồi tố* = 0 chuỗi | `Group` (danh từ) → **nhóm** | `Gộp` là động từ |
| `Factory` → giữ `Factory` | đã có 4 kiểu | `Command` → **lệnh** | `Key Command` → **phím tắt** |
| `Pick-up` → giữ **`Pick-up`** | không phải *Lấy đà* | `Scaling` → **co giãn** | *thu phóng* = `Zoom` |
| `Mouse Wheel` → **con lăn chuột** | không phải *cuộn chuột* | `Write Protection` → **bảo vệ ghi** | kể cả ở nhãn |
| `Flat` → **giảm** | nửa tông, không phải *phẳng* | `Multi` → **bội** | *đa kênh* = *multichannel* |
| `Symbol` / `Sign` | cùng **một** giá trị | `Octave` | `quãng tám` trong câu, `Octave` ở nhãn |
| `Version` (nhãn) → giữ | trong câu `phiên bản` đúng | chord **with a** 7 → **với nốt** 7 | `cấp 7` = Cmaj7 |

**`Set up X`** (20 nhãn): dịch `Set up` thành `Thiết lập` rồi **bỏ mặc danh từ** —
`Thiết lập Attribute Columns`. Kiểm "câu có tiếng Việt" sẽ bỏ sót; phải đọc phần sau
tiền tố. Cùng kiểu, `Replace / Restore / Reload / Resolve / Reveal / Resulting` — bảy giá
trị **tháo câu ra ghép ngược**: `Restore Default Setup` → `Thiết lập Restore Default`.

**Luật phụ thuộc nguồn** (mục `src` trong `terms_do_not_translate.json`): `Bypass` cấm
`bỏ qua`, `Cycle` cấm `lặp` — cùng một từ Việt đúng ở nguồn này, sai ở nguồn kia. 13
`Bypass` đã sửa ở đợt 72, nhưng 23 chuỗi `Ignore` **phải** giữ `bỏ qua`.

**Danh sách 160 từ = thuật ngữ DAW, KHÔNG phải mọi lần xuất hiện.** Đo ở đợt 171:
115 chuỗi có `Click` nhưng chỉ vài chuỗi giữ — vì `Click` **vừa** là nút (giữ `Click
Pattern`) **vừa** là động từ (`click chuột` → `Nhấp`, đúng). Tương tự `Insert` (nút
giữ EN / động từ `chèn`), `Send` (nút giữ / động từ `gửi`).

| Từ | Giữ EN khi | Dịch khi |
|---|---|---|
| `Click` | `Click Pattern`, `Click & Count-In` (tên tính năng) | `click chuột` → `Nhấp` |
| `Insert` | `Insert 1`, `Insert Slots`, `Bypass Insert` | `insert …` → `chèn` |
| `Send` | `Send 1`, `Send Slots` | `send …` → `gửi` |
| `Chord` | **`Chord` KHÔNG dịch** (77 chuỗi `hợp âm`) | — xem dòng dưới |
| `Note` | `Note 1/8` (Score) | `note nhạc` → `nốt` |
| `Beat` | nhãn/đơn vị | văn xuôi → `nhịp` |
| `Group` | tên tính năng (`Group Track`) | `nhóm nốt` → `nhóm` |

> **`Beat` dùng `nhịp`, KHÔNG `phách`** (đợt 173): 17 chuỗi `nhịp` trước, 3 chuỗi
> lọt dùng `phách` — *phách* đúng nghĩa nhưng lạc khỏi 17 chuỗi còn lại.
> **`Group` đánh số phải giữ EN** (đợt 173): `Group %d`, `Group 1..4` là tên tính
> năng nhưng lọt sang `Nhóm %d`/`Nhóm 1`, trong khi `Group` đơn lẻ đã giữ EN. Văn
> xuôi vẫn `nhóm` (`nhóm nốt`, `nhóm phụ`) — **9 chuỗi đó đúng, đừng đụng**.

> **Automation Read / Write & Thuật ngữ âm thanh số (đợt 174):**
> - **`Read / Write` trong Automation giữ EN:** Nút **R** và **W** trên channel, menu và phím tắt
>   phải là `Read Automation`, `Write Automation`, `Read/Write Automation` — tuyệt đối không dịch
>   thành "đọc" và "ghi" (gây nhầm lẫn nghiêm trọng với `Record` - ghi âm).
> - **`Nudge` giữ EN:** Không dùng từ bình dân "nhích" trong thanh công cụ/menu DAW chuyên nghiệp.
> - **Thuật ngữ Audio đồng bộ EN:** `Precount` (khớp với `Count-In`), `Bit Depth` (khớp với `Sample Rate`),
>   `Strip Silence` (công cụ xử lý Audio kinh điển), `Saturation` (màu âm analog/tape, không phải
>   "độ bão hòa" màu sắc), `Normalize` (chuẩn hóa biên độ/loudness số).

> **Chuẩn Loudness, Chord Assistant & Menu Audio (đợt 175):**
> - **Chuẩn đo Loudness giữ EN:** `Integrated Loudness`, `Short-Term Loudness` giữ EN (đồng bộ với
>   `Momentary Loudness` và lệnh `Normalize theo Integrated Loudness`). Loại bỏ tình trạng cấn cá
>   khi thanh đo Metering lúc ghi "ngắn hạn", "tích hợp" lúc lại ghi tiếng Anh.
> - **Chord Assistant giữ EN:** `Circle of Fifths` (loại bỏ dịch ngô nghê "vòng tròn quãng năm")
>   và `Proximity` (loại bỏ dịch "độ gần" như khoảng cách vật lý).
> - **Menu Audio giữ EN:** `Detect Silence` (cùng với `Strip Silence` trên menu `Audio > Advanced`).

> **Acoustic Feedback, Bank Select & Filter Slope (đợt 176):**
> - **Sửa lỗi dịch ngược `Filter Slope: <%s>`:** Thành `Độ dốc Filter: <%s>` (khớp với `Chọn độ dốc Filter`,
>   `Độ dốc High-Cut`, `Độ dốc Low-Cut`).
> - **`Acoustic Feedback` giữ EN:** Nút nghe thử nốt trên thanh công cụ MIDI Editor giữ EN, loại bỏ
>   dịch từng từ "Phản hồi Acoustic" (gây hiểu nhầm sang hiện tượng hú mic).
> - **`Bank Select` giữ EN:** Chuẩn MIDI Controller CC0/CC32 giữ EN trong danh sách MIDI CC, khớp
>   với `Portamento`, `Modulation`, `Breath Control`...

> **Jog Wheel & Track Archive (đợt 177):**
> - **`Jog` giữ EN:** Bộ ba vận chuyển DAW `Jog / Shuttle / Scrub` phải đồng bộ. `Jog sang trái`,
>   `Jog sang phải`, loại bỏ dịch thành "nhích" (từ bình dân).
> - **`Track Archive` giữ EN:** Menu `File > Import > Track Archive...` và các thông báo lỗi liên quan
>   phải giữ `Track Archive`, loại bỏ dịch thành "Lưu trữ Track..." (nghe như nút bấm sao lưu).

> **Send Initial Value, Auto-Scroll, Thumbnail Cache & Pan Law (đợt 178):**
> - **Sửa lỗi dịch sai ngữ nghĩa `Send Initial Value`:** Thành `Gửi giá trị khởi tạo` (lệnh gửi tới thiết
>   bị MIDI, bản dịch cũ tưởng nhầm là kênh hiệu ứng Send nên dịch "Giá trị khởi tạo của Send").
> - **Nút bấm Toolbar `Auto-Scroll`:** Đồng bộ với `Auto-Scroll (Tạm dừng)`, cập nhật cả `ui-navigation.json`.
> - **Đồng bộ `Thumbnail Cache`:** Bỏ "bộ nhớ đệm Thumbnail", khớp với `Cache` trong danh sách thuật ngữ.
> - **Chuẩn phòng thu `Pan Law`:** `Pan Law của Project`, `Stereo Pan Law`.

> **Simple Crossfade Editor, Equalizers & Functions Browser (đợt 179):**
> - **`Simple Crossfade Editor` giữ EN:** Loại bỏ "Trình sửa Crossfade đơn giản" (Editor duy nhất bị dịch
>   "trình sửa" trong toàn bộ map). Đồng bộ với `Crossfade Editor` và toàn bộ các Editor khác.
> - **Tab `Equalizers` giữ EN:** Bỏ chữ "Các" trên đầu đề tab/rack, đồng bộ với `Inserts`, `Sends`, `Strip`.
> - **Khớp tên UI `Functions Browser`:** `qua Trình duyệt Functions` (thay vì "Trình duyệt chức năng").

> **Sửa dứt điểm Record Enable & Arm/Disarm (đợt 180):**
> - **`Record Enable` trong `ui-navigation.json`:** Sửa tận gốc key `'Record Enable': 'Record Enable'`
>   để ngăn `merge_maps.py` âm thầm ghi đè lại thành "Bật ghi".
> - **`Arm / Disarm`:** Chuyển `Bật/Tắt sẵn sàng ghi` dài dòng thành `Bật/Tắt Record Enable cho tất cả Track`.
> - **`Read/Write-Enable`:** Đổi `Cho phép đọc/ghi` thành `Bật Read/Write` (khớp với Automation Read/Write).

> **Bộ 3 chế độ Sizing của Object Selection Tool (đợt 181):**
> - **Đồng bộ hành động Sizing:** Chuyển từ danh từ cụt ("Kích thước...") thành hành động rõ ràng
>   `Đổi kích thước thông thường`, `Đổi kích thước di chuyển nội dung` (Slip edit),
>   `Đổi kích thước áp dụng Time Stretch`. Sửa lỗi dịch sai của `Sizing Moves Content`
>   (trước dịch thành "Kéo cạnh để đổi kích thước" vốn là định nghĩa của Normal Sizing).

> **Đồng bộ 100% Lower Zone (đợt 182):**
> - **Đưa 7 chuỗi dịch nửa vời `Zone dưới` về `Lower Zone`:** Khớp hoàn toàn với `Left Zone`, `Right Zone`,
>   `Lower Zone` trên thanh công cụ và cửa sổ Project.

> **Ngoại lệ đã chốt — `Chord` dịch `hợp âm` (77 chuỗi).** Dù `Chord` nằm trong
> 68 từ cốt lõi, thực tế đo được: 77 chuỗi dùng `hợp âm`, và anh em giữ EN chỉ là
> **tên tính năng** (`Chord Track`, `Chord Pad`, `Chord Symbol`). Sửa danh sách thì
> sai; đây là điển tượng của "thuật ngữ vừa DAW vừa chuyên ngành". **Không đổi** —
> nhưng phải biết để không "sửa theo luật" rồi hỏng 77 chuỗi.

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

Phải là **tiếng Việt đời thường**, không phải tiếng Việt do máy dịch. Đợt 75/77/79 sửa
358 chuỗi vì đúng mấy nguyên tắc này.

> **Khó dịch thì để tiếng Anh. Đừng ép.** Người dùng chốt (đợt 165). Bản dịch vòng
> vẫn đọc được thì dịch; **không đọc được thì giữ nguyên tiếng Anh** — một câu
> tiếng Anh còn hơn một câu tiếng Việt sai nghĩa. Không phải "lười": chỉ khi đã thử
> và còn vướng.
> - Cờ đỏ, dừng lại: dịch từ tiếng Anh **có một nghĩa đúng** sang từ tiếng Việt
>   **khác nghĩa**. Đợt 165: `…used **these clefs**…` → `…loại **khóa** này…`
>   (khóa = key, không phải clef). Chỗ này **giữ `Clef`** mới đúng.
> - Cờ đỏ thứ hai: hiểu là dịch được nhưng **đọc lông nhằng** (`nương`, `thiết bị
>   đầu vào và đầu ra mạng` cho `network interface`). Viết lại cho tự nhiên; tới
>   mức không tự nhiên được thì giữ EN.
> - **Cấm để lại chỗ dở dang**: sửa nửa câu còn tệ hơn để nguyên. §4 đã cấm
>   dịch nửa vế; quy tắc này mở rộng điều đó sang *toàn câu*.
> - **Vẫn phải giữ bất biến kỹ thuật (§6)** kể cả khi giữ EN: dấu câu, placeholder,
>   `\n`, khoảng trắng đầu/cuối. `check_punctuation.py` không ngoại lệ.
>
> **Cubase GHÉP CHUỖI Ở RUNTIME — giá trị tiếng Việt lọt thẳng vào UI.** Đợt 170,
> người dùng chụp màn hình thấy `Thêm Nhóm Track`, `Thêm Hop âm Track`,
> `Thêm Transpose Track Track`. Nguyên nhân: menu là khuôn **`Add %s Track`**
> → `Thêm %s Track`, và `%s` lấy từ **key đơn lẻ**. Kiểm tra JSON cho thấy
> `'Add Group Track' -> 'Thêm Group Track'` **đúng**, nhưng key `'Group'` lại là
> `'Nhóm'` → menu ra `Thêm Nhóm Track`.
> - **Vì vậy: key đơn lẻ (`Group`, `Chord`, `Folder`, `TransposeTrack`…) quan
>   trọng ngang chuỗi dài.** Giá trị của nó đi vào UI qua `%s`, nên dịch sai
>   sẽ lộ ra ngay. Sửa cả hai vế: `Group` → `Group` cho khớp `Group Track`.
> - **`TransposeTrack` (không space) là chuỗi điền `%s`**, 8/9 ngôn ngữ gốc
>   không chữ "track" (de=`Transposition`, jp=`移調`). Đặt `Transpose Track` →
>   lặp thành `Track Track`. Giá trị đúng: `Transpose`.
> - **Bài học sâu:** 169 vòng kiểm đều pass mà UI vẫn có 4 lỗi. Công cụ kiểm
>   bản dịch, **không kiểm cách Cubase ghép chuỗi**. Chỉ nhìn màn hình mới thấy.
>   Khi nghi ngờ UI, kiểm key `%s` và key đơn lẻ trước, đừng đụng vào chuỗi dài.
> - **Đã quét toàn bộ khuôn:** 265 chuỗi có `%s`, trong đó 49 có danh từ
>   Track/Channel/Bus/Event/Part/Clip/Lane/Zone — **đều đúng**. Chỉ
>   `Add %s Track` là lỗi. 152 key đơn lẻ giá trị tiếng Việt (`Color`, `Align`,
>   `Create`…) là nút độc lập, không ghép — **không phải lỗi**.
> - **Nhãn ghép ở giao diện, không tìm thấy trong map:** `Thời gian ghi từ đá`
>   (Transport) và `Đầu vào/E` (bị cột hẹp cắt) — Cubase ghép/chỉnh ở runtime,
>   không phải chuỗi có key. **Đừng đi tìm chúng trong `vi.json`.**

> **`ui-navigation.json` LUÔN THẮNG — đây là bẫy merge.** `merge_maps.py` dùng
> `sorted()`, mà `u` > `r` nên file này đứng **sau** mọi `round_*.json`. Sửa ở
> `round_NNN.json` mà key đó có trong `ui-navigation.json` sẽ **bị ghi đề im lặng**
> (đợt 168: 3 chuỗi `Add … Track to Selected Tracks…`). `vi.json` vẫn đúng về
> kiểm tra nên không báo lỗi. **Sửa thì sửa cả hai file**, hoặc xoá key ở
> `ui-navigation.json`. Luôn merge xong đối chiếu lại giá trị.

> **Rút gọn: đừng để bộ dò tự cắt.** Đợt 166 thử cắt `Vui lòng` bằng regex và nó
> làm **hỏng 11/33 chuỗi** — chữ thường sau `.` và sau `\n\n`
> (`…cài đặt. Thử dùng…` thành `…cài đặt. thử dùng…`). Vì tiền tố lọc không biết
> vị trí câu. **Cắt bằng tay, rồi kiểm hoa/thường bằng assert.** Chỉ dùng regex để
> **tìm ra ứng viên**, không để ghi.
>
> **Đo quy tắc này (đợt 165) — cả 4 cách săn đều ra báo động giả.** Ghi lại để
> không phải đo lại:
> - `audit_clarity` [B] "khó đọc": 313 chuỗi. Đọc 30 chuỗi đầu — **không lỗi nào**;
>   dài vì nguyên văn dài, `english-run` là cụm thuật ngữ đúng.
> - Từ lặp ≥3 lần trong một value: **74 chuỗi**. Đọc 25 — tất cả lặp vì **nguyên văn
>   lặp** (`Channel` 6 lần vì EN cũng 6 lần). Đếm từ không phân biệt nguyên văn.
> - `của…của`, `bị…bị`, `không…không` lặp trong 40 ký tự: **15 chuỗi**, đọc hết —
>   đều là cú pháp Việt đúng (`Vị trí của Event vượt quá ranh giới của Part`).
> - Khoảng trắng thừa trước `:` — **9 chuỗi**, cả 9 đều **có** trong nguồn
>   (`CC01 : Modulation`, `Switch Layout :`). Chính Steinberg viết vậy.
>
> **Kết luận:** bộ dò bằng mẫu không bắt được lỗi này — §8.9 đã nói "lỗi chỉ lộ ra
> khi **đọc thật**". Muốn săn lỗi văn phong thì phải đọc tay (`read_long.py`), và
> quy tắc là **so từng cặp với nguồn 9 ngôn ngữ**, không phải đếm mẫu.

- **Bỏ bị động `... được`** — dấu hiệu rõ nhất của câu dịch máy: `đã được` → `đã` ·
  `sẽ được` → `sẽ` · `đang được` → `đang` · `đã bị loại bỏ` → `đã bỏ` · `Không thể
  chỉnh sửa VariAudio` → `Không sửa được VariAudio` · `không thể được Modulation` →
  `không nhận Modulation`.
- **Bỏ giọng ra lệnh và từ thừa.** `Bạn phải khởi động lại ứng dụng` → `Cần khởi động
  lại ứng dụng` · `Thực hiện Audio Export` → `Export Audio` · `Vui lòng nhập tên` →
  `Nhập tên` · `các hành động` → `Action`. Bỏ lặp: `gồm cài đặt Channel, Group Channel,
  Send Effect và Master Bus` → bỏ `cài đặt` ở cuối.
- **Rút từ dư.** `đã chứa` → `có` · `sẽ bị gỡ bỏ` → `sẽ mất` · `đang có hiệu lực` →
  `đang dùng` · `Có thể do vấn đề về quyền ghi` → `Có thể do không có quyền ghi` ·
  `Thư mục Project chỉ cho phép đọc` → `Thư mục Project chỉ đọc`. Giữ **mạo từ**
  khi làm chủ thể, bỏ khi thừa.
- **`inactive` đổi nghĩa theo ngữ cảnh.** Bốn nghĩa: không dùng / chưa bật (Version,
  Project) · đang tắt (Cycle) → `tắt` · tính năng bị hỏng → `chưa chọn` (đối chiếu
  bản Đức) · đĩa hỏng → `đang chạy không bình thường`. `đang không hoạt động bình
  thường` = dịch máy cho "not working normally".
- **Từ hay dịch sai nghĩa:** `làm mất hiệu lực` → `làm hỏng` · `Ngưỡng cho phép đo` →
  `Ngưỡng đo` (*threshold* ≠ *allowed threshold*) · `dấu bình hủy bỏ` → `dấu bình khử` ·
  `Tái sử dụng` → `Dùng lại` · `hộp thoại file` → `cửa sổ duyệt file` · `audio stream`
  → `Audio Stream`.

## 6. Bất biến kỹ thuật — giữ nguyên 100%

Placeholder `%s %d %i %.3f` · dấu hai chấm · `?` `!` `.` · dấu ba chấm ·
**số dòng mới** · **khoảng trắng đầu/cuối**. Xuống dòng bằng **`\n` hai ký tự**,
không phải newline thật. Bộ dò placeholder phải khớp cả `%1.0f` và `%02d` —
`r'%(?:\.\d+)?[a-zA-Z%]'` bỏ sót cả hai; dùng `cubelib.placeholders.PLACEHOLDER`.

- **`[RM]` thuộc về KEY, tuyệt đối không được nằm trong giá trị** — nó sẽ **hiện lên
  màn hình** cạnh nhãn ở read-mode. Cả tám nhà cung cấp đều dịch cặp đó giống nhau và
  không ai đặt nhãn vào giá trị. Marker `[RM] [Score View Option] [Key] [vocal]` là
  marker riêng của Cubase, nằm trong key — giữ nguyên.
- **Key ≠ English.** Cột 1 và cột 2 của TSV khác nhau: `AppKey[Key]`→`Menu`,
  `Delete Tool`→`Erase Tool`, `Check Files`→`Find Missing Files` — theo **key**.
- File Cubase đang chạy: bản **`full` 5.322.928 byte** (đủ 9 ngôn ngữ + `vi`).
  Bản rút gọn `translation_vi_en.xml` chỉ 1.443.882 byte, chỉ dùng khi
  `-Variant en` — **`install.ps1` mặc định lại là `en`**, cài nhầm thì Cubase có
  thể không hiện tiếng Việt. Khi kiểm bằng ảnh chụp, **luôn `-Variant full`**.
  `install.ps1` ghi `.bak` cạnh mọi file; `keys/translation_original.xml` là nguồn
  của cả hai bản. PowerShell báo `String: 0` là **sai** (`.String` trùng
  `System.String`) — kiểm bằng Python.

## 7. Bẫy công cụ

- **`[Ā-ỿ]` là SAI** — tiếng Việt nằm ở `U+00C0…U+00FF`, dưới đầu khoảng đó. 9 công cụ
  đã âm thầm chỉ xem một phần bản dịch. Đúng: `[\u00c0-\u024f\u1e00-\u1eff]`.
- **"bộ dò báo 0" và "bộ dò hỏng" trông giống nhau.** Thử một giá trị biết đúng vào bộ
  dò trước khi tin kết quả. Mọi ký tự đại diện phải kiểm bằng giá trị mẫu.
- Bộ dò đếm CÂU bỏ sót vế mất **ở giữa** câu (số dấu chấm vẫn khớp) — phải so **số
  dòng**; `check_punctuation.py` đã nối vào `build.py`.
- `all_strings.tsv` có thể **cắt cụt key dài**; hai dòng có thể trùng tiền tố 60 ký tự.
  Khi tra bằng key, yêu cầu **đúng một** ứng viên.
- Bốn báo động giả đã biết: (1) `Tên Channel`/`Số Note` trông đảo nhưng đúng;
  (2) `gán vào`/`chuyển vào` cần `vào`; (3) `lặng` nằm trong `dấu lặng`, `Over`
  trong `Cross-Over` khớp `\b` sau gạch nối; (4) `check_style` cấm ngoặc `(ms)` ở
  cuối dù là đơn vị — sửa **giá trị**, đừng sửa luật. Bộ dò báo động giả nhiều lần
  còn tệ hơn không có bộ dò: nó dạy người đọc bỏ qua báo cáo.

## 8. Bài học về cách sửa

1. **Tra bằng TỪ, không tra bằng key.** Thấy thuật ngữ trong chuỗi mới thì `grep` **từ
   đó** trong `vi.json` và sửa **mọi** chỗ khớp. Sửa 1/5 rồi dừng là thêm biến thể.
2. **Bảng thuật ngữ viết sai không tự báo lỗi.** Sửa **cả bản dịch lẫn dòng luật** —
   `Key Signature | hóa biểu` đã sinh 8 chuỗi sai vì luật sai.
3. **Mỗi đợt một file `fix_reading<N>.py`, không chép bảng của đợt trước.** Bảng cũ **là**
   một lệnh ghi đè: `glossary_readthrough.py` chạy cuối đã xoá `Lệnh` của `fix_reading4.py`
   mỗi lần chạy.
4. **Sau khi ghi, đếm lại từ mình vừa xoá** — không thì bản sửa tạo ra chính lỗi nó đi sửa.
   Kiểm `NOT IN CUBASE` **trước** khi `--write`. Trong bảng cài đặt, **hai từ Anh đứng cạnh
   nhau thì nguy hiểm gấp đôi** — dịch từng từ một (`Duration` cạnh `Field`).
5. **Luật và bản dịch lệch nhau ở quy mô lớn thì luật có thể sai, không phải map.** §3
   chốt `Time Signature = số chỉ nhịp`; §2 lại bắt giữ tiếng Anh. 49 chuỗi theo §3 là
   bằng chứng §3 đúng. Đo trước, sửa luật, đừng sửa 49 chuỗi.
6. **Một bộ dò đúng vẫn tạo báo động giả nếu thiếu ngữ cảnh.** `audit_split.py` xếp
   `Latency → độ trễ` lên đầu, nhưng lịch sử cho thấy *Độ trễ Channel* là ví dụ **được
   duyệt**. `grep` chỉ ra chỗ cần nhìn, không quyết định đúng sai.
7. **Bốn bộ dò tên gần giống, đừng lẫn.** `audit_terms.py` liệt kê cách diễn đạt của một
   thuật ngữ; `audit_split.py` hỏi thuật ngữ §2 nào đang bị dịch; `audit_outlier.py` tìm
   chuỗi lạc khỏi gia đình; `audit_domain.py` hỏi theo miền — **toàn báo động giả**.
8. **Chỉ thêm mẫu cấm khi cách dịch sai là cách dịch DUY NHẤT.** `thẻ` bắn 13 chuỗi
   (`Thiết lập thẻ` = Tab, đúng), `vùng` bắn 213 (`vùng chọn` đúng) — sửa chuỗi. Đợt 85:
   15 mẫu, 8 lỗi sửa tay.
9. Lỗi đảo trong câu dài, cách diễn đạt khó đọc, mất câu, sai nghĩa chỉ lộ ra khi **đọc
   thật**. Đọc tay là bước cuối: `read_long.py` / `sample_domain.py <miền> <bắt đầu>`.

10. **ĐỪNG dùng số liệu thay cho việc đọc. Hai vòng đã làm sai theo đúng cách đó.**
    - Đợt 88 lọc bằng *tỉ lệ số từ*, ra 380 chuỗi "dài". **Sai**: 3.234 chuỗi có
      nguồn ≥ 25 ký tự thì trung vị bản dịch **ngắn hơn 2 ký tự**, lệch dài nhất
      `+21c`, và **không chuỗi nào dài hơn 30 ký tự**. `audit_clarity.py` báo giá
      trị dài nhất 328c và *in ra trông dài hơn tiếng Anh* — nhưng nó **cắt cụt**
      chuỗi Anh: nguồn dài 371c, tức bản dịch **ngắn hơn 43c**. Cả hai đúng, một
      cái hiển thị sai. Lặp từ: 9 chuỗi cả bản dịch.
    - Đợt 89 đo tiếp, giả thuyết thứ hai: *mất ngữ cảnh vì key chỉ là chuỗi
      Anh*. **Cũng sai**: 83 chuỗi Anh dùng ở nhiều hơn một entry, và **không
      chuỗi nào** khác vai trò. Không có chỗ nào mất ngữ cảnh để lo.
    - Cái thật, và chỉ lộ ra khi **đặt hai chuỗi cạnh nhau**:
      `Import Audio File → 'Import file Audio'` cạnh
      `Import Audio Files → 'Import File Audio'` — lệch hoa/thường, mỗi cái
      rời ra đều đọc được. Đợt 89 sửa 8 chuỗi thuộc loại này.
    - **Cơ:** key là *chuỗi tiếng Anh*, không id, không đường dẫn, không vai trò.
      Nên **gia đình = các chuỗi cùng nói một thứ**, và cách tìem gần nhất là
      **từ đầu tiên**. Dùng `tools/family.py <từ>`.
    - Khi đọc: `Channel` và `Channel ` là **hai key khác nhau**, giữ khoảng trắng
      là đúng. `Db` cạnh `dB` là **chính Steinberg viết**, không phải việc của
      ta. `DRY`/`Dry`, `OFFLINE`/`Offline` đã khác nhau ở tiếng Anh gốc.

11. **PHÉP THỬ RỖNG LUÔN PASS. Đừng đọc 0 là sự thật — ba lần đã hỏng.**
    - Đợt 95: tìm `"chỉ dẫn diễn tấu"` trong `vi.json` ra **0**, tưởng đợt 88 đã
      sạch. Thật ra giá trị bắt đầu bằng `Chỉ` **hoa**, tôi tìm chuỗi **thường**.
      Bỏ phân biệt hoa/thường thì ra **1** — chỗ đó lọt sót từ đợt 88.
    - Đợt 96: quét `"bộ lọc"` chỉ trong khoá **ngắn hơn 34 ký tự**, bỏ sót 15
      chỗ, rồi định sửa cụm `Filter` theo tỉ lệ 17/32. Tỉ lệ 51/49 không phải
      bằng chứng, và sửa 17 chuỗi theo đa số yếu là đúng loại lỗi đã mắc 4 lần.
    - Đợt 98: đếm cụm `Template` bằng `if 'emplate' in v` — nhưng **giá trị** là
      tiếng Việt (`Mẫu`), chữ đó nằm ở **khoá**. Ra 0, rồi so `0 == 0` → pass.
      Đúng phải là `if 'emplate' in k and 'mẫu' in v`.
    - **Cơ chung:** mọi phép thử đếm hoặc tìm trong `fix_readingNN.py` phải có
      **chốt rỗng** — tìm ra 0 chỗ thì **báo lỗi**, không được coi là "đã sạch".
      Và **đừng so với con số viết tay**: đợt 98 đếm tay ra 10, thực tế 11; hãy so
      **trước với sau** trên cùng một cách đếm.
    - Cùng lớp với `score.FORBIDDEN` là `dict` khoá **số** còn test tra `c` là
      **ký tự** → không bao giờ khớp, `check_text` trả về chuỗi có byte NUL.
    - **Biến thể phân biệt hoa/thường — đã dính 4 lần** (đợt 95, 104 ×2). Kim
      tìm chuỗi viết **thường** không khớp giá trị bắt đầu bằng chữ **Hoa**.
    - **Cạm bẫy kèm theo:** `.lower()` **không bỏ dấu**. "lượt" là **một** ký tự
      (`ự` U+1EE3), không phải hai. Viết kim ASCII `luot` thì **không bao giờ
      khớp** "lượt". Đúng phải là: **kim tiếng Việt + `.lower()` cả hai bên**.

## 9. Quy trình kiểm tra

Dừng ngay khi một bước báo lỗi.

```powershell
python tools\merge_maps.py --check      # gộp batch -> vi.json, bắt key trùng
python tools\check_style.py             # 5 luật cứng (xem dưới)
python tools\audit_quality.py           # thuật ngữ xung đột + trật tự từ
python tools\audit_leak.py              # 8 bộ dò chữ (xem README): Anh lọt câu / lọt
python tools\find_leftover_english.py   # lẻ, câu chưa dịch, mất vế, khung Anh, ngoặc
python tools\audit_fragments.py         # kép lệch, key trùng, U+FFFD
python tools\find_dropped_sentences.py
python tools\find_english_frame.py
python tools\find_quoted_names.py
python tools\check_duplicate_keys.py
python tools\fix_mojibake.py
python tools\audit_clarity.py           # [A] dài  [B] khó đọc
python tools\audit_outlier.py           # chuỗi lạc khỏi gia đình thuật ngữ
python tools\tests\run.py               # 146 test: bất biến + bộ dò
python tools\family.py <từ>            # đọc cả gia đình chuỗi cùng từ đầu
python tools\family.py -a              # nhóm còn dùng hai kiểu ghi (chốt hồi quy)
python tools\read_long.py <miền> <bắt đầu>  # đọc tay: câu dài, chỗ vướng nằm ở đây
python tools\check_translation_build.py # build\translation_vi.xml = bản gốc + <vi>
python tools\score_instruments.py check # Score Editor: trùng key + 4 bất biến
python tools\build.py                   # sinh build/translation_vi.xml + validate
python tools\score_instruments.py build # sinh build/instrumentnames_vi.xml
pwsh -File scripts\install.ps1 -Action install
```

**Trước khi điều tra một cụm đang lệch, đọc `docs/OPEN_QUESTIONS.md`.** Năm cụm
(`Filter`, `Template`, `Audio Performance`, tên nhạc cụ, `Auto X`) đã bị điều tra
lại từ 5 vòng khác nhau mỗi lần đều dừng ở "không đủ bằng chứng". File đó ghi
bằng chứng **một lần** và điều kiện để xoá một mục. Đừng đo lại.
Một mục chỉ được xoá khi có (a) nhóm anh em buộc phải theo một hướng, hoặc
(b) **người dùng quyết**. Tỉ lệ 51/49 không phải (b).

**`check_translation_build.py` giữ đúng tiền đề của cả dự án.** Nó chứng minh
bằng cơ chế, không phải bằng lời: file build **bỏ các dòng `<vi>` đi thì ra
đúng bằng `keys\translation_original.xml`, từng byte**; 10.737 entry, mỗi entry
đúng 10 khối `<us>…<ru><vi>`; không `<us>…<ru>` nào bị đổi; mọi `<vi>` bằng
đúng `vi.json`; và dòng `<vi>` thụt lùi **đúng bằng 9 anh em** nó.

Bản cũ viết thẳng `\t\t` trong `build_translation.py`, nên `<vi>` lệch 1 tab so với
9 anh em, và `<language key="vi">` lệch 1 tab theo hướng ngược lại — `<vi>` nhìn
như anh em của `</String>` chứ không phải con của nó. XML không quan tâm, nhưng
diff 10.737 dòng thì có. Nay thụt lùi lấy từ chính file.

**5 luật cứng của `check_style.py`**: (1) cấm ngoặc chú thích cuối trừ khi key gốc có;
(2) cấm dịch thuần Việt thuật ngữ §1 — nay **64 mẫu** trong `terms_do_not_translate.json`;
(3) placeholder phải khớp; (4) giá trị không rỗng; (5) cấm `[RM]`. Luật 5 **duy nhất
không mang tính thẩm mỹ** — nó ngăn chữ lên màn hình.

## 10. Score Editor — bộ luật đặt tên nhạc cụ

Score Editor là `ScoringEngine.dll` (lõi Dorico), **không** dùng `translation.xml`.
Nó tự lấy chuỗi từ `Components\ScoringEngine\l10n\`. Hai loại file, hai quy trình:

| file | công cụ | quy trình |
| --- | --- | --- |
| `instrumentnames_vi.xml` | `tools/score_instruments.py` | `import` → 5 vòng `fix_scoreNN.py` → `build` |
| `strings_vi.qm` | `tools/score_strings.py` | chưa làm |

`instrumentnames_en.xml` có 624 entity và **1.126 chuỗi phân biệt** trong 3.115 ô
(`uiName`, `singularFullName`, `singularShortName`, `pluralFullName`,
`pluralShortName`). Chỉ 5 ô đó được dịch; `<name>`, `<gender>`,
`<inheritanceMask>`, `<parentEntityID>` **giữ nguyên ở mọi ngôn ngữ**. Viết bằng
**cắt chuỗi**, không re-serialise: file dùng CRLF, tab, `<?xml version="1.0" ?>`
(có khoảng trắng trước `?>`), `<x/>` cho ô rỗng, và entity `aluphone` xếp
`<name>` **trước** `<entityID>`.

### 6 luật — lấy từ 9 catalogue Steinberg, không phải từ khẩu vị

`instrumentnames_ja.xml` và `instrumentnames_de.xml` đã phải trả lời đúng câu hỏi
này, và chúng **thống nhất trên từng chuỗi**. Đọc cột `ja=` / `de=` của
`tools/tests` hay file gốc rồi làm theo:

1. **Tên riêng không dịch; tính ngữ mô tả thì dịch.** `Banjo`, `Charango`,
   `Cuatro`, `Alphorn`, `Cimbasso`, `Didgeridoo`, `Bansuri`, `Guitarrón`,
   `Wagner Tuba` giữ nguyên. Còn `Acoustic`, `Electric`, `Fretless`,
   `Classical`, `Jazz`, `Steel-string`, `Semi-acoustic`, `Resonator` và tên nước
   thì dịch: `Electric Guitar` → **`Guitar điện`**, `Classical Guitar` →
   **`Guitar cổ điển`**, `Resonator Guitar` → **`Guitar cộng hưởng`**.

2. **Chữ viết tắt không bao giờ đổi.** ~130/320 chuỗi của `brass`+`wind` là chữ
   viết tắt, và cả 9 catalogue đều giữ nguyên: `Tbn`, `Tpt`, `V. Tbn.`,
   `Cbsn`, `Min-bsn`, `Ac. B. Gtr`, `Ban.`, `Dul.`. Chúng là nhãn cố định cho cột
   tên bè trong bản nhạc — dài thêm là vỡ bố cục. **Số nhiều của chữ viết tắt thì
   rút gọn**: `Ac. B. Gtrs` → `Ac. B. Gtr`.

3. **Tiếng Việt không có số nhiều, nên số nhiều lấy đúng từ của số ít.** `Pianos` →
   `Piano`, `Mezzo-sopranos` → `Mezzo-soprano`, `Basses` → `Bass`, `Cajons` →
   `Cajon`. `check_consistency` kiểm: có key số ít thì hai giá trị phải bằng nhau.

4. **Từ bên trong ngoặc thì dịch, viết hoa chữ đầu, giữ ngoặc.** Đây là khuôn mẫu
   mà 40 chuỗi seed đã viết ra: `Bongo (High)` → `Bongo (Cao)`, `Tenor Drum
   (Medium-high)` → `Trống Tenor (Trung bình cao)`, `Tabla baya (larger)` →
   `Tabla baya (Lớn hơn)`. Nhưng `(Quinto)`, `(Requinto)`, `(Super Tumba)`,
   `(pedal)` **giữ** — đó là tên của biến thể, không phải thanh bậc.

5. **Thanh bậc đã là mượn ngữ thì giữ nguyên chỗ nó đứng.** `Alto Balalaika`,
   `Bass Balalaika`, `Contrabass Balalaika`, `Prima/Secunda Balalaika`,
   `Piccolo Domra`, `Tenor Lute`, `Tenor Banjo`, `Horn (alto)`, `Horn (basso)`.
   Đức dịch giữ nó ở đầu (`Alt-Balalaika`, `Kontrabass-Balalaika`), Nhật cũng vậy
   (アルト + バラライカ). Không engine nào dịch cả, nên ta cũng không.

6. **Tên miền dịch khi tiếng Việt có từ thật.** Bảng chính đã quyết: `Brass` →
   `Bộ đồng`, `Wind` → `Gió`, `Keyboard` → `Bàn phím`, `Voice` → `Bè`, `Triangle`
   → `Tam giác`, `Whistle` → `Còi`; nhưng giữ `Percussion`, `Drum`, `Snare`,
   `Tambourine` — vì tiếng Việt không có từ nào dùng được cho chúng. Vì vậy
   `Strings` → `Bộ dây`, `Woodwind` → `Bộ gió`, còn `Drum Set` → `Drum Set`.

### Tiếng Anh lọt là hợp lệ, và đó là điểm cần nói rõ

**591 / 1.126 chuỗi (52%) giữ nguyên tiếng Anh** — và đây là kết quả đúng, không
phải chỗ sót. Người Việt gọi "guitar", "piano", "kora", "cổ điển" chứ không gọi
"đàn ghi-ta". Bảng chính đã chốt sẵn 146 chuỗi theo đúng cách đó
(`tools/score_instruments.py import` nhập 88 chuỗi có sẵn + 58 chuỗi trùng).

Vì thế **đừng** dùng `find_leftover_english.py` vào `translations/score/`, và
**đừng** ép mọi giá trị khác tiếng Anh. Trái lại là sai: `Snare` → `Trống Snare`?
Không — `Snare` giữ nguyên, còn `Side Drum` → `Trống phụ` là đúng, vì "snare" không
có từ Việt còn "drum phụ" thì có.

### Bốn bất biến của `check_consistency`

`python tools\score_instruments.py check` dừng ngay khi lỗi:

1. Giá trị không rỗng, không ký tự điều khiển, không U+FFFD, không khoảng trắng
   đầu/cuối. **Ngoại lệ**: map giống hệt thì miễn — vài ô gốc mang khoảng trắng
   cuối (`<O. M. >`) và giữ nguyên là câu trả lời đúng.
2. Mọi key phải có thật trong `instrumentnames_en.xml` — lỗi gõ trong batch không
   được lọt.
3. Giá trị chỉ được **ngắn hơn** key bằng đúng đuôi số nhiều (`s`/`es`/`n`).
   `Agogôs` → `Agogô` hợp lệ, `Charangos` → `Charang` là bậy.
4. Số nhiều đã dịch phải khớp số ít. Map **giống hệt** được miễn: số nhiều tiếng
   Anh giữ nguyên tiếng Anh không phải chỗ lệch của ta. Ngoại lệ có tên:
   `Voice`/`Voices` — một dòng hát vs cả phần bè.

### Lỗi tìm ra khi làm Score Editor

Chi tiết ở `docs/RESEARCH.md`. Hai lỗi **trong file của Steinberg**:

- 8/8 file không-Anh giữ entity `instrumentname.pitchedpercussion.aluphone` ở
  `kEnglish`; file Đức còn thêm `marching.snare.drum.rim`. Cùng cái entity mang
  `<customVariantString/>` mà Steinberg thêm tay vào bản tiếng Anh rồi copy sang
  các bản dịch mà quên dán nhãn lại.
- `<language>` xuất hiện **625 lần** (một ở đầu, 624 ở entity), và 5 ô tên rỗng
  (`cajon.low` mất short/plural, `clarinet.contra.alto.eflat` mất plural).

`tools/score_instruments.py build` ghi **đồng nhất** cả 625 marker thành
`kVietnamese` và liệt kê `mis_tagged`, để lỗi của nguồn không bị sao chép.

Hai lỗi **trong code của chính repo này**, do `tools/tests/test_score.py` phát hiện
— đúng loại lỗi mà §3 cảnh báo, nên ghi lại ở đây:

- `score.FORBIDDEN` là `dict.fromkeys` của **số**, còn chỗ kiểm tra lại tra
  `c in FORBIDDEN` với `c` là **ký tự**. Khớp không bao giờ xảy ra, nên
  `check_text` vẫy về một chuỗi có byte NUL. Bộ dò mới bắt được.
  Nay là `frozenset` ký tự.
- `source_strings` đếm `uiName` và `singularFullName` là hai người dùng, nên
  `--status` báo ��ội gấp đôi số bè mỗi chuỗi tiết kiệm được. Nay khử trùng
  theo entity.

## 11. Cubase Hub — `hubservice.dll`

Cubase Hub là module độc lập tại `Components\hubservice.dll`. Nó sở hữu bảng XML gồm
**89 chuỗi riêng** (chứa `Create Empty Project...`, `Recent`, `Tutorials`, `Deals`,
`User Manuals`, `Hub Settings`, `Choose File...`) nhúng trực tiếp trong binary.
Các chuỗi này không nằm trong `translation.xml` chính; khi chạy tiếng Việt nếu
chưa patch bảng XML trong DLL thì các nhãn riêng của Hub sẽ tự động fallback về
tiếng Anh `<us>`. Chi tiết kỹ thuật và danh sách chuỗi xem tại `docs/HUBSERVICE.md`.
