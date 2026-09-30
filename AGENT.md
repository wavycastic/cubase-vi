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
- **TUYỆT ĐỐI KHÔNG**: ngoặc chú thích ở cuối (`Thêm track (Add Audio Tracks)` — SAI,
  nhãn tràn chữ). Chỉ giữ ngoặc khi **key gốc đã có**, và khi đó dịch trong ngoặc.
  Cũng không dịch thuần Việt: `Automation`, `Bounce`, `Track`, `Clip`, `Freeze`, `Quantize`.

## 2. Thuật ngữ bắt buộc

**DAW — giữ tiếng Anh (160 từ).**

70 từ cốt lõi: Track · Channel · Bus · FX · Group · VCA · Insert · Send · Slot · Fader · Pan · Solo · Mute · Meter · Metronome · Click · Marker · Locator · Automation · Clip · Event · Part · Pool · Quantize · Snap · Grid · Bounce · Render · Freeze · Warp · Velocity · Pitch · Note · Chord · Tempo · Timecode · Bar · Beat · Fade · Punch · Buffer · Latency · Sample Rate · ASIO · VST · Plug-in · Preset · MixConsole · Inspector · Zone · Export · Import · Arranger · Chain · Step · Lane · Pattern · Expression · Voicing · Tension · Articulation · Layout · Map · Mapping · Script · Machine Control · Talkback · Cue

90 từ mở rộng: Project · Audio · Controller · Cycle · Bypass · Remote · Effect · Monitor · Video · Routing · Bank · Loop · Transpose · Loudness · Assistant · Media · Strip · Focus · VariAudio · SyncStation · Player · Score · Logical · Listen · Region · Band · Crossfade · Clock · Panner · Workspace · Snapshot · Room · Hitpoint · Gain · Surface · Sampler · Transport · Retrospective · Learn · Shuttle · Pitchbend · Extension · Wave · Modulation · Frame · Dynamics · Modulator · Factory · ASIO-Guard · MediaBay · Mixdown · Layer · Ruler · SysEx · High-Cut · Side-Chain · Profile · Macro · Pre-roll · Phase · Tuning · Trim · Patch · Multi-Channel · Low-Cut · Word · Folding · Post-Fader · Dynamic · Pedal · Permission · Pre-Fader · Subsection · Post-roll · Downmix · Module · Count-In · CCMode · NoteExp · Latch · Thru · Z-Axis · Remote-Control · AudioWarp · Transformer · Scripting · Cache · Studio · Offline · Mixer

> `Time Signature` và `Chord Symbols` đã gỡ khỏi danh sách vì §3 bắt dùng tiếng Việt;
> map theo §3 (49 chuỗi) — quyết định chốt. 90 từ "mở rộng" đo trên 10.737 chuỗi:
> nguồn ≥5 lần, bản dịch dịch ≤2 lần (`terms_do_not_translate.json`).
>
> **Cách tìm từ nên cấm** — đừng hỏi "thuật ngữ nào đã bị dịch" (16 ứng viên, **không
> cái nào sai**). Hỏi: **thuật ngữ nào có MỘT chuỗi lệch khỏi gia đình?** — 18 lỗi.

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
| `Duration` → **thời lượng** | *trường độ* = ngành/khoa | `New` → **mới** | không phải *Tạo* |
| `Word Clock` → giữ `Word` | *Word Spacing* → *Khoảng cách từ* đúng | `Deactivate` → **Tắt** | *Hủy* = *cancel* |
| `External` → giữ `External` | *outside* = nghĩa **đối lập** | `Doubles` → **Note trùng** | ghi trùng, không dài gấp đôi |
| `Material` → **chất liệu** | không phải *tư liệu* | `Notehead` → **đầu nốt** | không phải *đầu nối* |
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
- File Cubase đang chạy: **chỉ `us` + `vi`** (1.449.424 byte). `install.ps1` ghi `.bak`
  cạnh mọi file; `keys/translation_original.xml` là nguồn của cả hai bản. PowerShell
  báo `String: 0` là **sai** (`.String` trùng `System.String`) — kiểm bằng Python.

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
  `--status` báo đội gấp đôi số bè mỗi chuỗi tiết kiệm được. Nay khử trùng
  theo entity.