# AGENT.md — Quy tắc bắt buộc khi dịch Cubase

Áp dụng cho **mọi** thay đổi trong `translations/**`. Không có ngoại lệ.

---

## 1. Kiểu dịch: LAI TIẾNG ANH – TIẾNG VIỆT

**KHÔNG dịch sang tiếng Việt hoàn toàn.** Cubase là công cụ chuyên nghiệp:
hàng triệu video hướng dẫn, tài liệu, forum đều dùng **từ tiếng Anh**. Người dùng
phải nhìn thấy đúng chữ đó để tìm được nút cần bấm.

Mỗi chuỗi dịch phải thuộc đúng **một** trong hai mẫu:

### Mẫu A — GIỮ NGUYÊN TIẾNG ANH

Dùng khi là **tên riêng, tên thương hiệu, định dạng file, chuẩn**, hoặc **thuật
ngữ chuyên môn mà cộng đồng âm nhạc Việt vẫn gọi bằng tiếng Anh** và tiếng Việt
không có từ tương đương chính xác.

```
Track            →  Track
Automation       →  Automation
Bounce           →  Bounce
Warp             →  Warp
MIDI             →  MIDI
VST Connections  →  VST Connections
Key Editor       →  Key Editor
```

> Giá trị **bằng đúng** key gốc. Không thêm gì.

### Mẫu B — LAI: `Tiếng Việt (English)`

Dùng cho **chữ trên giao diện** (menu, nút, nhãn) khi tiếng Việt có từ tương
đương tự nhiên và dễ hiểu.

```
Devices         →  Thiết bị (Devices)
Window          →  Cửa sổ (Window)
File            →  Tệp (File)
Save            →  Lưu (Save)
Cancel          →  Hủy (Cancel)
Add Audio Tracks...  →  Thêm track âm thanh (Add Audio Tracks...)
```

> Phần trong ngoặc **bắt buộc**, và phải là **nguyên văn chuỗi gốc**.

### Quy tắc máy kiểm tra

Giá trị dịch phải khớp **một trong hai** mẫu sau (so sánh không phân biệt
hoa thường, bỏ khoảng trắng thừa):

```
giá trị == key                                  → Mẫu A
giá trị kết thúc bằng  " (<key>)"               → Mẫu B
```

Kiểm tra tự động: `python tools/check_style.py` (chạy trong CI, exit code khác 0
khi vi phạm).

---

## 2. Những gì KHÔNG BAO GIỜ dịch

Áp dụng cho cả hai mẫu — những thứ này giữ nguyên tiếng Anh **ở giữa câu**:

- **Tên thương hiệu / sản phẩm:** Cubase, Steinberg, HALion, VST, VST3, ASIO,
  Groove, Pro Tools, MediaBay, Control Room
- **Chuẩn / định dạng:** MIDI, AAF, AIFF, AIFC, WAV, MP3, MusicXML, AVI, SysEx,
  NRPN, CC, Timecode
- **Tên track, bus, preset, plugin, effect** nếu là giá trị do người dùng đặt
- **Phần mở rộng tệp** (`.cpr`, `.npr`, `.mpr`)

```
Bounce Selection      →  Bounce vùng chọn (Bounce Selection)
Add Expression Map    →  Thêm Expression Map (Add Expression Map)
VST Connections       →  Kết nối VST (VST Connections)
```

---

## 3. Placeholder — bất di bất dịch

Chuỗi gốc có `%s`, `%d`, `%i`, `%.3f`, `%l`… thì giá trị dịch phải giữ **nguyên
văn, đúng số lượng, đúng thứ tự**. Không thêm bớt.

```
%d file(s) found       →  Tìm thấy %d tệp (found %d file(s))
```

Nếu không chắm chắn cách diễn đạt → **dùng Mẫu A**, giữ nguyên chuỗi gốc.

---

## 4. Bảng thuật ngữ — bắt buộc nhất quán

Cùng một tiếng Anh **luôn** dịch thành cùng một tiếng Việt, xuyên suốt repo.

| Tiếng Anh | Tiếng Việt (dùng trong phần ngoặc) |
|---|---|
| File | Tệp |
| Edit | Sửa |
| Project | Dự án |
| Window | Cửa sổ |
| Devices | Thiết bị |
| Preferences | Tùy chọn |
| Language | Ngôn ngữ |
| Help | Trợ giúp |
| Open | Mở |
| Save | Lưu |
| Close | Đóng |
| Delete | Xóa |
| Add | Thêm |
| Remove | Gỏ bỏ *(không phải "Xóa")* |
| Cancel | Hủy |
| Apply | Áp dụng |
| Reset | Đặt lại |
| Search | Tìm |
| Rename | Đổi tên |
| Duplicate | Nhân bản |
| Copy | Sao chép |
| Cut | Cắt |
| Paste | Dán |
| Undo | Hoàn tác |
| Redo | Làm lại |
| Enable | Bật |
| Disable | Tắt |
| Error | Lỗi |
| Warning | Cảnh báo |
| Transport | Transport *(giữ tiếng Anh)* |
| Marker | Marker *(giữ tiếng Anh)* |
| Track | Track *(giữ tiếng Anh)* |
| Channel | Kênh |
| Clip | Clip *(giữ tiếng Anh)* |
| Part | Part *(giữ tiếng Anh)* |
| Event | Event *(giữ tiếng Anh)* |
| Pool | Pool *(giữ tiếng Anh)* |
| Insert | Insert *(giữ tiếng Anh)* |
| Send | Send *(giữ tiếng Anh)* |
| Solo / Mute | Solo / Mute *(giữ tiếng Anh)* |
| Fader | Fader *(giữ tiếng Anh)* |
| Render | Render *(giữ tiếng Anh)* |
| Bounce | Bounce *(giữ tiếng Anh)* |
| Warp | Warp *(giữ tiếng Anh)* |
| Quantize | Quantize *(giữ tiếng Anh)* |
| Snap | Snap *(giữ tiếng Anh)* |
| Grid | Grid *(giữ tiếng Anh)* |
| Zoom | Zoom *(giữ tiếng Anh)* |
| Cursor | Cursor *(giữ tiếng Anh)* |
| Locator | Locator *(giữ tiếng Anh)* |
| Automation | Automation *(giữ tiếng Anh)* |
| Expression | Expression *(giữ tiếng Anh)* |
| Velocity | Velocity *(giữ tiếng Anh)* |
| Note | Note *(giữ tiếng Anh)* |
| Tempo | Nhịp độ |
| Bar | Cột nhịp |
| Beat | Nhịp |
| Key | Giai điệu |
| Scale | Thang điệu |
| Metronome | Métronome |
| Count-In | Đếm nhịp |
| Punch In/Out | Ghi vào/ra |
| Latency | Độ trễ |
| Sample Rate | Tần số lấy mẫu |
| Buffer | Bộ đệm |
| Bit Depth | Độ sâu bit |
| Folder | Thư mục |

Quy tắc của bảng này do người viết dịch tự rà soát. Khi thêm cặp mới, sửa
thẳng bảng ở trên — `tools/check_style.py` không kiểm tra tính nhất quán này
(nó chỉ kiểm tra đúng hai mẫu và placeholder).

---

## 5. Những điều KHÔNG làm

- **Không** dịch thuật ngữ kỹ thuật sang tiếng Việt hoàn toàn
  (`Automation` → `Tự động hóa` là **sai**)
- **Không** dịch tên file, tên plugin, tên preset
- **Không** thêm chú thích, không thêm dấu ngoặc kép thừa
- **Không** viết hoa chữ cái đầu tiên của phần tiếng Anh trong ngoặc — copy
  nguyên văn key
- **Không** để lại chuỗi rỗng
- **Không** sửa `keys/all_strings.tsv` để "hợp với bản dịch" — nó là bản tham
  chiếu từ Cubase

---

## 6. Quy trình

```powershell
# 1. xem chuỗi chưa dịch, ưu tiên nhãn ngắn
python tools\worklist.py A 100

# 2. thêm vào translations/batches/<lô>.json theo đúng quy tắc trên
# 3. kiểm tra style TRƯỚC khi build
python tools\check_style.py
# 4. gộp + build + validate
python tools\merge_maps.py
python tools\build.py
# 5. deploy
pwsh -File scripts\install.ps1 -Action install
```

Bước 3 **không được bỏ qua**. Nếu linter báo lỗi, sửa bản dịch — đừng nới lỏng
linter.
