# Kiến trúc Localization của Cubase Hub (`hubservice.dll`)

## 1. Hiện tượng
Trên giao diện khởi động **Cubase Pro Hub**, một số thành phần hiển thị tiếng Việt (`Các Project`, `Mẫu`, `Mở`, `Không có Driver`, `Chưa kết nối`), nhưng nhiều nút và mục quan trọng vẫn hiện **tiếng Anh**:
- Nút tạo: `Create Empty Project...`
- Cột bên trái: `Tutorials`, `Deals`, `User Manuals`, `Hub Settings`
- Khung danh sách: `Recent`
- Nút chọn: `Choose File...`

## 2. Nguyên nhân kỹ thuật
Các chuỗi này **không nằm trong file bản dịch chính** `translation.xml` (10.737 chuỗi của Cubase core trong `translations/vi.json`).

Hub được phát triển như một Component độc lập:
- Đường dẫn: `Components\hubservice.dll` (kích thước ~3.080.192 bytes).
- Cơ chế dịch: Component này sử dụng module `\lib.frame-base\source\language\translator.cpp`.
- Bảng chuỗi: Nhúng trực tiếp một bảng XML gồm **89 chuỗi riêng** trong section data của binary từ offset `0x25D192` đến `0x266180`.
- Ngôn ngữ hỗ trợ gốc: Chỉ có 9 ngôn ngữ chuẩn của Steinberg (`<us>`, `<de>`, `<fr>`, `<es>`, `<it>`, `<pt>`, `<jp>`, `<zh>`, `<ru>`).
- Khi Cubase chạy với ngôn ngữ Tiếng Việt, các chuỗi trùng Key với core sẽ được nạp bản dịch, còn các chuỗi chỉ có trong bảng 89 chuỗi của Hub do thiếu thẻ `<vi>` nên tự động fallback về tiếng Anh `<us>`.

## 3. Danh sách 89 chuỗi riêng của Hub trong `hubservice.dll`

| Key gốc | Ý nghĩa / Vị trí | Đề xuất tiếng Việt |
|---|---|---|
| `Create Empty Project...` | Nút tạo dự án mới | Tạo Project rỗng... |
| `Create Empty Project` | Nhãn hành động | Tạo Project rỗng |
| `Recent` | Tab / Tiêu đề danh sách gần đây | Gần đây |
| `Tutorials` | Menu bên trái | Hướng dẫn |
| `Deals` | Menu bên trái | Ưu đãi |
| `User Manuals` | Menu bên trái | Hướng dẫn sử dụng |
| `Hub Settings` | Menu bên trái | Cài đặt Hub |
| `Choose File...` | Nút duyệt mở file | Chọn file... |
| `Projects` | Tab danh mục | Các Project |
| `Templates` | Tab danh mục mẫu | Mẫu |
| `Factory Templates` | Danh mục mẫu cài sẵn | Mẫu mặc định |
| `User Templates` | Danh mục mẫu người dùng | Mẫu người dùng |
| `Start a New Project` | Tiêu đề hướng dẫn | Bắt đầu Project mới |
| `Click 'Create Empty' to start with a blank project.` | Chú thích | Nhấn 'Tạo rỗng' để bắt đầu với một Project trống. |
| `Click 'Tutorials' to access official video tutorials, walkthroughs, and tips.` | Chú thích | Nhấn 'Hướng dẫn' để xem video hướng dẫn, thủ thuật chính thức. |
| `Open Hub When Closing Projects` | Cài đặt | Mở Hub khi đóng Project |
| `Display File Paths and Template Descriptions` | Cài đặt | Hiện đường dẫn file và mô tả mẫu |
| `Clear 'Recent'` | Menu chuột phải | Xóa danh sách 'Gần đây' |
| `Remove from 'Recent'` | Menu chuột phải | Gỡ khỏi 'Gần đây' |
| `Add User Location` | Nút thêm thư mục | Thêm vị trí người dùng |
| `Remove User Location` | Nút gỡ thư mục | Gỡ vị trí người dùng |

## 4. Hướng xử lý
1. **Lưu trữ từ điển chuỗi của Hub**: Lưu trữ 89 chuỗi này trong một file riêng `translations/hub_strings.json` để quản lý chuẩn hóa ngôn ngữ.
2. **Quy trình Patch / Inject**:
   - Tương tự như `patch_translation.py` cho `Cubase15.exe`, có thể xây dựng công cụ `patch_hub.py` để chèn hoặc thay thế chuỗi ngôn ngữ trong `hubservice.dll`.
   - Vì bảng XML nhúng trong DLL có giới hạn kích thước vùng nhớ, giải pháp an toàn là:
     a) Chèn thẻ `<vi>` nếu còn khoảng trống (padding).
     b) Hoặc ghi đè trực tiếp vào thẻ ngôn ngữ ít dùng (như `<ru>`) hoặc thay thế chuỗi trực tiếp.
