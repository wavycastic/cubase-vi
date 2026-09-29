# AGENT.md — Quy tắc bắt buộc khi dịch Cubase

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ.

---

## 1. Kiểu dịch: LAI ANH - VIỆT TỰ NHIÊN (Vietglish chuyên ngành DAW)

Dịch theo cách giới làm nhạc, phòng thu Việt Nam giao tiếp thực tế:
- **Động từ, thao tác, trạng thái, giao diện**: Việt hoá ngắn gọn, chuẩn xác (`Thêm`, `Xóa`, `Nhân bản`, `Sửa`, `Mở`, `Lưu`, `Bật`, `Tắt`, `Ẩn`, `Hiện`, `Chọn`, `Tới`, `Đảo ngược`...).
- **Thuật ngữ chuyên môn âm thanh & DAW**: **Giữ nguyên 100% tiếng Anh**, ghép tự nhiên vào ngữ pháp tiếng Việt.

### TUYỆT ĐỐI KHÔNG:
- **KHÔNG mở ngoặc chú thích tiếng Anh ở đuôi**: `Thêm track âm thanh (Add Audio Tracks)` là **SAI**. Nút bấm và menu sẽ bị tràn chữ và trông như từ điển. Chuỗi đúng là `Thêm Audio Track`.
- **KHÔNG dịch thuần Việt các thuật ngữ chuẩn**:
  - `Automation` → `Tự động hóa` (SAI)
  - `Bounce` → `Nảy` (SAI)
  - `Track` → `Rãnh` (SAI)
  - `Clip` → `Đoạn cắt` (SAI)

---

## 2. Bảng thuật ngữ kỹ thuật (BẮT BUỘC GIỮ TIẾNG ANH)

Những từ sau đây **luôn viết bằng tiếng Anh**, xuất hiện tự nhiên trong câu:

| Thuật ngữ | Cách dùng trong câu tiếng Việt |
|---|---|
| Track | `Thêm Audio Track`, `Xóa Track đã chọn`, `Track Version mới` |
| Channel | `Màu Channel`, `Độ trễ Channel`, `Cấu hình Channel` |
| Bus / FX / Group / VCA | `Thêm Group Bus`, `FX Channel`, `VCA Fader` |
| Insert / Send | `Sửa Insert`, `Bật Send`, `Send Slot` |
| Fader / Pan / Solo / Mute | `Mute Track`, `Solo Channel`, `Fader MIDI`, `Pan tiếng nhấp` |
| Metronome / Click | `Bật Click Metronome`, `Cài đặt Metronome`, `Âm thanh Click` |
| Marker / Locator | `Thêm Cycle Marker`, `Tới Left Locator`, `Cài đặt Marker` |
| Automation | `Ẩn tất cả Automation`, `Sửa Automation`, `Automation Track` |
| Clip / Event / Part / Pool | `Chọn tất cả Event`, `File trong Pool`, `Active Clip` |
| Quantize / Snap / Grid | `Áp dụng Quantize`, `Snap tới Zero Crossing`, `Cài đặt Grid` |
| Bounce / Render / Freeze / Warp | `Bounce vùng chọn`, `Render in Place`, `Freeze Track` |
| Velocity / Pitch / Note / Chord | `Fixed Velocity`, `Sửa Pitch`, `Xóa Note trùng`, `Track hợp âm` |
| Tempo / Timecode / Bar / Beat | `Đặt Tempo`, `Tap Tempo`, `Nhịp độ (Tempo)` |
| Buffer / Latency / Sample Rate | `Kích thước Audio Buffer`, `Độ trễ Channel`, `Sample Rate` |
| ASIO / VST / Plug-in / Preset | `Thiết bị Audio ASIO`, `Quản lý Plug-in`, `Preset âm thanh` |
| MixConsole / Inspector / Zone | `Mở MixConsole`, `Kích thước Inspector`, `Lower Zone` |

---

## 3. Các thao tác giao diện c�� bản (Việt hoá tự nhiên)

| Thao tác tiếng Anh | Dịch tự nhiên | Ví dụ trong Cubase |
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

---

## 4. Placeholders (%s, %d, %i, %.3f...)

Giữ nguyên văn, không đổi thứ tự, không dịch nhầm vào tên biến.
Ví dụ: `Add %d Audio Tracks` → `Thêm %d Audio Track`.

---

## 5. Quy trình kiểm tra máy (`tools/check_style.py`)

- Cấm giá trị kết thúc bằng `(<key>)` hoặc `(<từ tiếng Anh>)`.
- Không để chuỗi rỗng.
- Kiểm tra tính toàn vẹn của placeholder.
