# AGENT.md — Quy tắc bắt buộc khi dịch Cubase 15

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ.
Chuẩn hoá theo `keys/all_strings.tsv` (10.737 cặp key ⇄ English).
Bản rút gọn từ 2.442 dòng — lịch sử 80 đợt đọc tay ở
`…\Temp\opencode\AGENT.md.bak`, đọc khi cần biết *vì sao* một luật tồn tại.

## 1. Kiểu dịch

- **Động từ / thao tác / trạng thái / giao diện** → Việt hoá ngắn gọn: `Thêm`,
  `Xóa`, `Gỡ bỏ`, `Nhân bản`, `Sửa`, `Mở`, `Lưu`, `Bật`, `Tắt`, `Ẩn`, `Hiện`,
  `Chọn`, `Tới`, `Đảo ngược`.
- **Thuật ngữ âm thanh & DAW** → **giữ tiếng Anh**, ghép vào ngữ pháp tiếng Việt.
- **TUYỆT ĐỐI KHÔNG**: ngoặc chú thích ở cuối (`Thêm track (Add Audio Tracks)` — SAI,
  nhãn tràn chữ). Chỉ giữ ngoặc khi **key gốc đã có**, và khi đó dịch trong ngoặc.
  Cũng không dịch thuần Việt: `Automation`, `Bounce`, `Track`, `Clip`, `Freeze`, `Quantize`.

## 2. Thuật ngữ bắt buộc

**DAW — giữ tiếng Anh (160 từ).**

70 từ cốt lõi: Track · Channel · Bus · FX · Group · VCA · Insert · Send · Slot · Fader · Pan · Solo · Mute · Meter · Metronome · Click · Marker · Locator · Automation · Clip · Event · Part · Pool · Quantize · Snap · Grid · Bounce · Render · Freeze · Warp · Velocity · Pitch · Note · Chord · Tempo · Timecode · Bar · Beat · Fade · Punch · Buffer · Latency · Sample Rate · ASIO · VST · Plug-in · Preset · MixConsole · Inspector · Zone · Export · Import · Arranger · Chain · Step · Lane · Pattern · Expression · Voicing · Tension · Articulation · Layout · Map · Mapping · Script · Machine Control · Talkback · Cue

90 từ mở rộng: Project · Audio · Controller · Cycle · Bypass · Remote · Effect · Monitor · Video · Routing · Bank · Loop · Transpose · Loudness · Assistant · Media · Strip · Focus · VariAudio · SyncStation · Player · Score · Logical · Listen · Region · Band · Crossfade · Clock · Panner · Workspace · Snapshot · Room · Hitpoint · Gain · Surface · Sampler · Transport · Retrospective · Learn · Shuttle · Pitchbend · Extension · Wave · Modulation · Frame · Dynamics · Modulator · Factory · ASIO-Guard · MediaBay · Mixdown · Layer · Ruler · SysEx · High-Cut · Side-Chain · Profile · Macro · Pre-roll · Phase · Tuning · Trim · Patch · Multi-Channel · Low-Cut · Word · Folding · Post-Fader · Dynamic · Pedal · Permission · Pre-Fader · Subsection · Post-roll · Downmix · Module · Count-In · CCMode · NoteExp · Latch · Thru · Z-Axis · Remote-Control · AudioWarp · Transformer · Scripting · Cache · Studio · Offline · Mixer

> `Time Signature` và `Chord Symbols` đã gỡ khỏi danh sách vì §3 bắt dùng tiếng
> Việt; map theo §3 (49 chuỗi) — đây là quyết định chốt. 90 từ "mở rộng" đo trên
> 10.737 chuỗi: nguồn có ≥5 lần, bản dịch dịch ≤2 lần (chi tiết ở
> `terms_do_not_translate.json`; sinh lại bằng `tools/audit_protected.py`).

**Bàn nhạc (Score Editor) — dùng tiếng Việt:** Staff/Stave = khuông nhạc ·
Clef = khóa nhạc · Rest = dấu lặng · Beam = đuôi nốt · **Stem = thân nốt** ·
Barline = vạch nhịp · **Key Signature = hóa âm** · Time Signature = số chỉ nhịp ·
**Chord Symbols = hóa biểu** · Voice = bè · Ledger Line = dòng kẻ ·
Accidental = dấu hóa · Note (trường độ) = giữ `Note` → `Note 1/8` ·
Rhythm Dot = dấu chấm dôi · Slash = gạch chéo · Scale (data) = co giãn

`System` và `Bar` theo ngữ cảnh: Score Editor → `dòng nhạc` / `Bar`; ngoài đó →
`hệ thống` / `thanh`. Từ HLV cũng giữ bên HLV: `con trỏ`, `bè`, `phát lại`, `hợp âm`.

## 3. Bẫy thuật ngữ — đọc sai ở đây là hỏng

| Sai → Đúng | Vì sao | Sai → Đúng | Vì sao |
|---|---|---|---|
| `Duration` → **thời lượng** | *trường độ* = ngành/khoa | `No.` → **số** | viết tắt *Number* |
| `Word Clock` → giữ `Word` | *Word Spacing* → *Khoảng cách từ* thì đúng | `New` → **mới** | không phải *Tạo* |
| `External` → giữ `External` | *outside* = nghĩa **đối lập** | `Deactivate` → **Tắt** | *Hủy* = *cancel* |
| `Search ... String` → **chuỗi** | chỉ `String`+`Tuning`/`From` mới là dây | `Doubles` → **Note trùng** | ghi trùng, không phải dài gấp đôi |
| `Material` → **chất liệu** | không phải *tư liệu* | `Notehead` → **đầu nốt** | không phải *đầu nối* |
| `Retrospective Record` → giữ Anh | đợt 72 đảo lại; *ghi hồi tố* = 0 chuỗi | `Group` (danh từ) → **nhóm** | `Gộp` là động từ |
| `Factory` → giữ `Factory` | đã có 4 kiểu | `Command` → **lệnh** | `Key Command` → **phím tắt** |
| `Pick-up` → giữ **`Pick-up`** | không phải *Lấy đà* | `Scaling` → **co giãn** | *thu phóng* = `Zoom` |
| `Mouse Wheel` → **con lăn chuột** | không phải *cuộn chuột* | `Write Protection` → **bảo vệ ghi** | kể cả ở nhãn |
| `Flat` → **giảm** | nửa tông, không phải *phẳng* | `Multi` → **bội** | *đa kênh* = *multichannel* |
| `Symbol` / `Sign` | cùng **một** giá trị | `Version` (nhãn) → giữ | trong câu `phiên bản` đúng |
| `Octave` | `quãng tám` trong câu, `Octave` ở nhãn | chord **with a** 7 → **với nốt** 7 | `cấp 7` = Cmaj7 |

**`Set up X`** (20 nhãn): dịch `Set up` thành `Thiết lập` rồi **bỏ mặc danh từ** —
`Thiết lập Attribute Columns`. Kiểm "câu có tiếng Việt" sẽ bỏ sót; phải đọc phần sau
tiền tố. Cùng kiểu, `Replace / Restore / Reload / Resolve / Reveal / Resulting` — bảy
giá trị **tháo câu ra ghép ngược**: `Restore Default Setup` → `Thiết lập Restore Default`.

**Luật phụ thuộc nguồn** (mục `src` trong `terms_do_not_translate.json`): `Bypass`
cấm `bỏ qua`, `Cycle` cấm `lặp` — cùng một từ Việt đúng ở nguồn này, sai ở nguồn
kia. 13 `Bypass` đã sửa ở đợt 72, nhưng 23 chuỗi `Ignore` **phải** giữ `bỏ qua`;
luật không có vế `src` sẽ chặn cả 36.

## 4. Thứ tự từ và câu

- **Danh từ chính giữ vị trí.** Anh đặt ở cuối → `Output Bus`, `Analyzer Track`.
  Việt đặt trước → `Tên Channel`, `Số Note`, `Chế độ Value`. Cả hai dạng **đúng**.
  HLV + tiếng Anh: `Tên Channel`. HLV + HLV: `Volume của Channel`.
- Số đứng **trước**: `100 Events` → `100 Event`; `%d Channels` → `%d Channel`.
- `to` khi **chuyển đổi** là `sang` (không phải `vào`, không phải mũi tên):
  `Mono to Multi-Channel` → `Mono **sang** Multi-Channel`. `vào` thừa khi câu đã có
  động từ (`Go vào Input` → `Tới đầu vào`), nhưng `Thêm ... vào ...` là **đúng**.
- **Viết lại cả câu**, không thay từ rời — kể cả khi mọi từ đều là thuật ngữ DAW.
- **Câu phải có chủ thể.** `Đạt giới hạn ...` thiếu chủ ngữ → `Đã đạt giới hạn ...`.
  Giữ dấu kết câu và dấu ba chấm của key.
- **Đừng cắt mất câu.** Tiếng Anh **nói luật trước, ngoại lệ sau** nên vế sau trông
  như chú thích và là vế **bị bỏ** — mất đúng thứ nói *cái giá* của tính năng.
  Khi đọc câu dài, **đếm vế**.
- **Tên trong ngoặc kép phải khớp bản dịch của nhãn** — vì menu hiện tên đã Việt
  hoá. `'Part Editing Mode'` → trích `'Chế độ sửa Part'`. Ngoại lệ: tên nút / giá
  trị dropdown giữ tiếng Anh (`Record Enable`, `Monitor`, `Solo`, `Read`, `Write`,
  `Any`) vì đó là chữ **in trên nút**. `Save` thì không — Cubase hiện `Lưu`. Tên
  không có nhãn tương ứng thì giữ tiếng Anh.
- **Không dịch nửa vế**: dịch thì dịch trọn, giữ thì giữ trọn, không để nửa.

## 5. Văn phong — bỏ bị động, rút gọn

Phải là **tiếng Việt đời thường**, không phải tiếng Việt do máy dịch. Đợt
75/77/79 sửa 358 chuỗi vì đúng mấy nguyên tắc này.

- **Bỏ bị động `... được`** — dấu hiệu rõ nhất của câu dịch máy: `đã được` → `đã` ·
  `sẽ được` → `sẽ` · `đang được` → `đang` · `đã bị loại bỏ` → `đã bỏ` · `Không thể
  chỉnh sửa VariAudio` → `Không sửa được VariAudio` · `không thể được Modulation`
  → `không nhận Modulation`.
- **Bỏ giọng ra lệnh và từ thừa.** `Bạn phải khởi động lại ứng dụng` → `Cần khởi
  động lại ứng dụng` · `Thực hiện Audio Export` → `Export Audio` · `Vui lòng nhập
  tên` → `Nhập tên` · `các hành động` → `Action`. Bỏ lặp: `gồm cài đặt Channel,
  Group Channel, Send Effect và Master Bus` → bỏ `cài đặt` ở cuối.
- **Rút từ dư.** `đã chứa` → `có` · `sẽ bị gỡ bỏ` → `sẽ mất` · `đang có hiệu lực`
  → `đang dùng` · `Có thể do vấn đề về quyền ghi` → `Có thể do không có quyền ghi` ·
  `Đã xảy ra sự cố khi truy cập` → `Không mở được` · `Thư mục Project chỉ cho phép
  đọc` → `Thư mục Project chỉ đọc`. Giữ **mạo từ** khi làm chủ thể, bỏ khi thừa.
- **`inactive` đổi nghĩa theo ngữ cảnh.** Bốn nghĩa: không dùng / chưa bật
  (Version, Project) · đang tắt (Cycle) → `tắt` · tính năng bị hỏng → `chưa chọn`
  (đối chiếu bản Đức) · đĩa hỏng → `đang chạy không bình thường`. `đang không hoạt
  động bình thường` là cách dịch máy cho "not working normally".
- **Từ hay dịch sai nghĩa:** `làm mất hiệu lực` → `làm hỏng` · `Ngưỡng cho phép đo`
  → `Ngưỡng đo` (*threshold* ≠ *allowed threshold*) · `dấu bình hủy bỏ` → `dấu bình
  khử` · `Tái sử dụng` → `Dùng lại` · `phần mở rộng File` → `đuôi File` · `hộp thoại
  file` → `cửa sổ duyệt file` · `audio stream` → `Audio Stream`.

## 6. Bất biến kỹ thuật — giữ nguyên 100%

Placeholder `%s %d %i %.3f` · dấu hai chấm · `?` `!` `.` · dấu ba chấm ·
**số dòng mới** · **khoảng trắng đầu/cuối**. Xuống dòng bằng **`\n` hai ký tự**,
không phải newline thật. Bộ dò placeholder phải khớp cả `%1.0f` và `%02d` —
`r'%(?:\.\d+)?[a-zA-Z%]'` bỏ sót cả hai; dùng `cubelib.placeholders.PLACEHOLDER`.

- **`[RM]` thuộc về KEY, tuyệt đối không được nằm trong giá trị** — nó sẽ **hiện
  lên màn hình** cạnh nhãn ở chế độ read-mode. Cả tám nhà cung cấp đều dịch cặp đó
  giống nhau và không ai đặt nhãn vào giá trị. Marker `[RM] [Score View Option]
  [Key] [vocal]` là marker riêng của Cubase, nằm trong key — giữ nguyên.
- **Key ≠ English.** Cột 1 và cột 2 của TSV khác nhau: `AppKey[Key]`→`Menu`,
  `Delete Tool`→`Erase Tool`, `Check Files`→`Find Missing Files` — theo **key**.
- File Cubase đang chạy: **chỉ `us` + `vi`** (1.449.424 byte). `install.ps1` ghi
  `.bak` cạnh mọi file; `keys/translation_original.xml` là nguồn của cả hai bản.
  PowerShell báo `String: 0` là **sai** (`.String` trùng `System.String`) — kiểm bằng Python.

## 7. Bẫy công cụ

- **`[Ā-ỿ]` là SAI** — tiếng Việt nằm ở `U+00C0…U+00FF`, dưới đầu khoảng đó. 9
  công cụ đã âm thầm chỉ xem một phần bản dịch. Đúng: `[\u00c0-\u024f\u1e00-\u1eff]`.
- **"bộ dò báo 0" và "bộ dò hỏng" trông giống nhau.** Thử một giá trị biết đúng
  vào bộ dò trước khi tin kết quả. Mọi ký tự đại diện phải kiểm bằng giá trị mẫu.
- Bộ dò đếm CÂU bỏ sót vế mất **ở giữa** câu (số dấu chấm vẫn khớp) — phải so
  **số dòng**; `check_punctuation.py` đã nối vào `build.py`.
- `all_strings.tsv` có thể **cắt cụt key dài**; hai dòng có thể trùng tiền tố 60
  ký tự. Khi tra bằng key, yêu cầu **đúng một** ứng viên.
- Bốn báo động giả đã biết: (1) `Tên Channel`/`Số Note` trông đảo nhưng đúng;
  (2) `gán vào`/`chuyển vào` cần `vào`; (3) `lặng` nằm trong `dấu lặng`, `Over`
  trong `Cross-Over` khớp `\b` sau gạch nối; (4) `check_style` cấm ngoặc `(ms)` ở
  cuối dù là đơn vị — sửa **giá trị**, đừng sửa luật. Bộ dò báo động giả nhiều lần
  còn tệ hơn không có bộ dò: nó dạy người đọc bỏ qua báo cáo.

## 8. Bài học về cách sửa

1. **Tra bằng TỪ, không tra bằng key.** Thấy thuật ngữ trong chuỗi mới thì `grep`
   **từ đó** trong `vi.json` và sửa **mọi** chỗ khớp. Sửa 1/5 rồi dừng là thêm một
   biến thể.
2. **Bảng thuật ngữ viết sai không tự báo lỗi.** Sửa **cả bản dịch lẫn dòng luật** —
   `Key Signature | hóa biểu` đã sinh 8 chuỗi sai vì luật sai.
3. **Mỗi đợt một file `fix_reading<N>.py`, không chép bảng của đợt trước.** Bảng cũ
   **là** một lệnh ghi đè: `glossary_readthrough.py` chạy cuối đã xoá `Lệnh` của
   `fix_reading4.py` mỗi lần chạy.
4. **Sau khi ghi, đếm lại từ mình vừa xoá** — không thì bản sửa tạo ra chính lỗi nó
   đi sửa. Kiểm `NOT IN CUBASE` **trước** khi `--write`.
5. Trong bảng cài đặt, **hai từ tiếng Anh đứng cạnh nhau thì nguy hiểm gấp đôi** —
   dịch từng từ một (`Duration` cạnh `Field` → `trường độ`).
6. **Luật và bản dịch lệch nhau ở quy mô lớn thì luật có thể sai, không phải map.**
   §3 chốt `Time Signature = số chỉ nhịp`; §2 lại bắt giữ tiếng Anh. 49 chuỗi theo
   §3 là bằng chứng §3 đúng. Đo trước, sửa luật, đừng sửa 49 chuỗi.
7. **Một bộ dò đúng vẫn tạo báo động giả nếu thiếu ngữ cảnh.** `audit_split.py` xếp
   `Latency → độ trễ` lên đầu, nhưng lịch sử cho thấy *Độ trễ Channel* là ví dụ
   **được duyệt**. `grep` chỉ ra chỗ cần nhìn, không quyết định đúng sai.
8. **Tên hai bộ dò gần giống nhau, đừng lẫn.** `audit_terms.py` liệt kê mọi cách
   diễn đạt của một thuật ngữ; `audit_split.py` hỏi thuật ngữ §2 nào đang bị dịch.
9. Lỗi đảo trong câu dài, cách diễn đạt khó đọc, mất câu, sai nghĩa chỉ lộ ra khi
   **đọc thật**. Đọc tay là bước cuối: `read_long.py` / `read_short.py` /
   `sample_domain.py <miền> <bắt đầu> <số>`.

## 9. Quy trình kiểm tra

Dừng ngay khi một bước báo lỗi.

```powershell
python tools\merge_maps.py --check      # gộp batch -> vi.json, bắt key trùng
python tools\check_style.py             # 5 luật cứng (xem dưới)
python tools\audit_quality.py           # thuật ngữ xung đột + trật tự từ
python tools\audit_leak.py              # bộ dò chữ: Anh lọt câu / lọt lẻ, câu chưa
python tools\find_leftover_english.py   # dịch, mất vế, khung Anh, ngoặc kép lệch
python tools\audit_fragments.py         # nhãn, key trùng, U+FFFD
python tools\find_dropped_sentences.py  # audit_split / audit_protected: xem §2
python tools\find_english_frame.py
python tools\find_quoted_names.py
python tools\check_duplicate_keys.py
python tools\fix_mojibake.py
python tools\audit_clarity.py           # [A] dài  [B] khó đọc
python tools\tests\run.py               # 90 test: bất biến + bộ dò
python tools\build.py                   # sinh build/translation_vi.xml + validate
pwsh -File scripts\install.ps1 -Action install
```

**5 luật cứng của `check_style.py`**: (1) cấm ngoặc chú thích cuối trừ khi key
gốc có; (2) cấm dịch thuần Việt thuật ngữ §1 (nay 49 mẫu, xem
`terms_do_not_translate.json`); (3) placeholder phải khớp; (4) giá trị không rỗng;
(5) cấm `[RM]`. Luật 5 **duy nhất không mang tính thẩm mỹ** — nó ngăn chữ lên màn hình.