# Câu hỏi mở — những cụm đang lệch mà bảng **không đủ** để quyết

Mỗi vòng đọc tuần tự tôi lại điều tra lại những cụm dưới đây, tốn lượt mà không
tiến. Ở đây là chỗ ghi lại **bằng chứng một lần**, để lần sau đọc thẳng vào
mục này thay vì đo lại.

Quy tắc để một mục được xoá khỏi đây: phải có **một trong hai** —
(a) chứng minh được nhóm anh em buộc phải theo một hướng, hoặc
(b) một quyết định của người dùng.
Số đo 51/49 **không** phải (bằng chứng cho thấy sai).

---

## 1. Cụm `Filter` — 32 giữ "Filter" / 17 dùng "bộ lọc"
**Đợt 96, để nguyên.**
- Giữ: `Filter` -> `Filter`, `Activate Filter` -> `Bật Filter`,
  `Deactivate Filter` -> `Tắt Filter`, `Filter Channel Types` -> `Loại Filter Channel`
- Dịch: `Add filter` -> `Thêm bộ lọc`, `Remove Filter` -> `Gỡ bỏ bộ lọc`,
  `Input Filter` -> `Bộ lọc đầu vào`, `Rating Filter` -> `Bộ lọc đánh giá`,
  `Event Target Filters`, `Limit Number of Attribute Filters`,
  `Reset Filter`, `Reset Result Filters`, `Append Filter`, `Show/Hide Attribute
  Filters`, `Sync Track/Channel Type Filters`, `List Editor: Show/Hide Filters`
- **Bằng chứng quan trọng:** `Remove Filter` -> `Gỡ bỏ bộ lọc` và `Remove filter`
  -> `Gỡ bỏ bộ lọc` **giống nhau**, tức bản dịch **không** phân biệt hoa/thường
  như tiếng Anh. Nên "bộ lọc" không phải hệ quả của viết hoa.
- Có thể là quy ước có chủ đích (thuật ngữ có tên giữ tiếng Anh, danh từ thường
  thì dịch) — giống `String`/`dây`.
- **Cần:** biết `Input Filter` và `Activate Filter` có phải cùng một tính năng
  không. Nếu có thì phải chọn một hướng cho cả hai.

## 2. Cụm `Template` — 11 dùng "mẫu" / 2 giữ tiếng Anh
**Đợt 98, để nguyên.**
- Dịch: `Templates` -> `Mẫu`, `Install Template` -> `Cài đặt mẫu`,
  `Select Template` -> `Chọn mẫu`, `Save as Template` -> `Lưu thành mẫu`,
  `Template Category` -> `Danh mục mẫu`, `Test Template` -> `Mẫu kiểm tra`,
  `Track Templates` -> `Mẫu Track`, `All Templates` -> `Tất cả mẫu`, ...
- Giữ: `Project Templates` -> `Project Template`, `Load SyncStation Template` -> giữ
- AGENT.md §1 lại liệt kê `Template` trong **90 từ giữ nguyên** → theo luật phải
  giữ cả 13.
- Hai cái giữ có thể cố ý: `SyncStation` là **tên sản phẩm**.
- **Cần:** người dùng quyết luật §1 với đa số trong bản dịch.

## 3. Cụm `Audio Performance` — 3 dịch / 2 giữ
**Đợt 102, để nguyên.**
- Dịch: `Audio Performance` -> `Hiệu năng Audio`, `VST Performance` -> `VST Hiệu năng`,
  `...Click to Show Audio Performance...` -> `...Bảng Hiệu năng Audio`
- Giữ: `Audio Performance Meter`, `Audio Performance Monitor`
- Hai cái giữ là **tên bảng cửa sổ có tên** trong Cubase → có lý do riêng.
- 3/2 không phải bằng chứng.

## 4. Tên nhạc cụ trong bảng chính vs `instrumentnames_vi.xml`
**Đợt 105, để nguyên.** Đây là mục có bằng chứng mạnh nhất, nên ghi kỹ.

Bảng chính (`translations/vi.json`):
- `Bass Drum` -> `Trống Bass`, `Hand Drum` -> `Trống tay`,
  `Marching Bass Drum (1 line)` -> `Trống Bass diễu hành (1 dòng)`,
  `Marching Snare Drum (1 line)` -> `Trống Snare diễu hành (1 dòng)`,
  `Marching Tenor Drum (1 line)` -> `Trống Tenor diễu hành (1 dòng)`
- Giữ: `BassDrum` -> `BassDrum`, `Brake Drum` -> `Brake Drum`,
  `Kick Drum (Low)` -> `Kick Drum (Trầm)`

File tên nhạc cụ (`instrumentnames_vi.xml`, dựng ở đợt 86 từ 9 catalogue):
- giữ **387/624** `uiName` y hệt tiếng Anh (`zh` giữ 601, `de` 177, `ja` 0)
- giữ `Bass Drum`, `Kick Drum`, `Hand Drum`, `Brake Drum`, `Snare Drum`
- `de` cũng giữ `Bass Drum` và `Snare Drum`; `it` giữ `Brake Drum`; `ru` giữ
  `Brake Drum` và `Tom`

**Hai điều đã chứng minh được:**
1. `BassDrum` (không có khoảng trắng) **không xuất hiện trong bất kỳ
   catalogue nào của Steinberg** (10 file, 0 lần). Nó là chuỗi riêng của
   bảng chính, không phải tên nhạc cụ. Giữ nguyên là đúng.
2. `Brake Drum`, `Kick Drum` giữ tiếng Anh trong cả hai nơi → **đã thống nhất**,
   không phải lỗi.

**Còn lại, chưa quyết:** `Bass Drum` / `Hand Drum` / `Marching ... Drum` được
dịch trong bảng chính nhưng giữ tiếng Anh trong file tên nhạc cụ. Có thể là
đúng — nhãn giao diện dịch được, còn tên nhạc cụ trong danh sách phải khớp
tên file. Có thể là lệch. Bảng không cho biết `Bass Drum` trong bảng chính hiện
ở đâu.
**Cần:** biết `Bass Drum` trong bảng chính là nhãn hay mục chọn nhạc cụ.

## 5. Cụm `Auto X` — giữ "Auto X" hay "X tự động"?
**Đợt 103, để nguyên.** Cả hai kiểu cùng tồn tại:
- Giữ trọn: `Auto Fade In`, `Auto Fade Out`, `Auto Join`, `Auto Punch`,
  `Auto Fades Settings`, `Auto-Scroll with Project Cursor`, `Auto-Zoom to Event`
- Dịch: `Auto Fades` -> `Fade tự động`, `Auto Zoom` -> `Zoom tự động`,
  `Auto LFO` -> `LFO tự động`, `Auto Join Time` -> `Thời gian Auto Join`
- Còn `Auto Crossfades` -> `Crossfade tự động` (đợt 103 đã bỏ số nhiều)
- Đây là nhãn menu ở các hộp thoại khác nhau; bảng không nói cái nào ở đâu.
**Cần:** người dùng chỉ hộp thoại nào hay thấy nhất.

---

## 6. `key` ≠ `<us>` — dịch theo cột nào? **Đợt 189, để nguyên, cần người dùng quyết**

`keys/translation_original.xml` có **283 chuỗi mà `<us>` khác `Key`**, không chỉ khác
ở dấu `[...]`. Ví dụ `Key='Autoscroll'` nhưng `<us>='Auto-Scroll On/Off'`. Đây là
điều AGENT.md §6 chỉ nói vừa một câu ("theo key") nhưng **chưa ai đo xem hệ quả**.

**Điều Cubase hiện lên màn hình là `<us>` của ngôn ngữ đang chọn, không phải `Key`.**
Nếu vậy thì 3 chuỗi dưới đang hiện **thiếu chữ** so với bản gốc:

| Key | `<us>` | VI hiện tại | de | ja | zh | ru |
|---|---|---|---|---|---|---|
| `MIDI Step Input` | **`MIDI Input`** | `MIDI Step Input` | `MIDI-Eingabe` | `MIDI ステップ入力` | `MIDI 步进输入` | — |
| `Slip Event` | **`Slip Event Content`** | `Slip Event` | `Event-Inhalt verschieben` | `イベントの内容をずらす` | `滑动事件` | — |
| `Pre/Post Fader` | **`Pre-/Post-Fader`** | `Pre/Post Fader` | `Pre/Post Fader` | `プリ/ポストフェーダー` | `推子 前/后` | — |

**Vì sao để nguyên chứ không sửa:** bằng chứng **chia làm đôi** —
`MIDI Step Input` thì **ja + zh** dịch theo *key*, còn **de** theo `<us>`;
`Pre/Post Fader` thì **de** lại theo *key*. Không ngôn ngữ nào nhất quán, nên
51/49 ở đây lại là số đo, không phải quyết định. Riêng `MIDI Step Input` đợt 184 đã
sửa *từ* `MIDI Input` **thành** `MIDI Step Input` dựa trên giả định của tôi rằng
key là thứ hiển thị — **giả định đó chưa được kiểm chứng, đợt 189 mới phát hiện ra là
có 2 phe.**

**Cần:** người dùng xác nhận **Cubase 15 hiện `<us>` hay hiện `Key`** trên UI. Chỉ
cần câu trả lời này là 3 chuỗi này (và toàn bộ 283 chuỗi còn lại) được quyết ngay.
Trong lúc đó **đừng đo lại cụm này nữa** — đo 5 lần rồi.

**Trạng thái (đợt 191): người dùng trả lời "chưa check"** — chưa mở Cubase để đối chiếu
nên **3 chuỗi này giữ nguyên, đã đóng băng cho tới khi có câu trả lời.** Đừng hỏi lại
và đừng sửa. Ba chuỗi đó là:
`MIDI Step Input` → `MIDI Step Input` · `Slip Event` → `Slip Event` ·
`Pre/Post Fader` → `Pre/Post Fader`.

**Cách người dùng tự kiểm tra trong 30 giây:** mở Cubase → *Edit ▸ Preferences ▸
General ▸ Language* → đổi sang **English**, bật chế độ đọc (View ▸ Read Mode ▸ On),
tìm nút **Step Input** trên thanh công cụ Key Editor (hoặc menu *MIDI ▸ Step Input*)
→ xem nó ghi `MIDI Input` hay `MIDI Step Input`. Trả lời một câu là xong cụm này.

---

## Đã quyết rồi (không cần hỏi lại)

| Quy ước | Nguồn của bằng chứng |
|---|---|
| Bảng màu (Color Setup / Palette) -> giữ nguyên tiếng Anh | Người dùng yêu cầu trực tiếp (32 chuỗi: White, Black, Red, Blue, Dark/Light..., Black 50/70, Gray 5..90) |
| Score Editor -> giữ nguyên thuật ngữ chuyên ngành ký âm | Người dùng yêu cầu trực tiếp (Staff, Clef, Barline, Stem, Beam, Accidental, Rest, Notehead, Arpeggio, Tuplet...) |
| `Equal Power` (Stereo Pan Law) -> giữ nguyên `Equal Power` | Người dùng yêu cầu trực tiếp qua ảnh chụp màn hình (đồng bộ với `Equal Gain`) |
| `X Presets` (số nhiều, tập hợp) -> `Preset X`; `X Preset` (thuật ngữ) -> giữ | `Mixer Presets` -> `Preset của Mixer` vs `Logical Preset` -> `Logical Preset` |
| khoá `"X - Y"` -> giữ dấu ` - ` | 93 chuỗi, 91 giữ (đợt 102) |
| bỏ số nhiều tiếng Anh trong thuật ngữ giữ nguyên | `Articulations` 22/25, `Voicing` 35/38, `Crossfade` 26/27 (đợt 101, 103) |
| `Arm` -> "sẵn sàng ghi", `Record Enable` -> **giữ EN** | đợt 171 (người dùng: "bật ghi nghe chán quá" + "record là từ chuyên ngành mà lại dịch à"). Luật AGENT.md dòng 95 đã yêu cầu giữ EN vì là **chữ in trên nút** — bản dịch trái luật mới là lỗi. Đã ghi đè dòng này. |
| ~~`Time Signature` -> "số chỉ nhịp"~~ **giữ EN thay thế** | đợt 146–171: 49 chuỗi `số chỉ nhịp` → `Time Signature`, hết trong round 160. Dòng này viết từ trạng thái cũ. |
| `Barline` -> giữ `Barline` | rounds 148–149 sửa `vạch nhịp` → `Barline`, giống Score Editor. Nguồn cũ ghi "vạch nhịp" — đã lệch. |
| nhãn/đơn vị `Beat` -> `Beat`; văn xuôi về nhịp -> "nhịp" | `Beats` -> `Beat` cạnh `Beats in Original Length` -> `Số nhịp...` |