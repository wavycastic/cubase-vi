# Nghiên cứu: Cubase lưu chuỗi giao diện ở đâu và cách ghi đè

Ghi lại những gì đã dò được, để không phải RE lại từ đầu.

## Kết luận

Chuỗi giao diện của Cubase 15 nằm ở **XML văn bản thuần (UTF-8, không nén)**
nhúng trong PE resource `TRANSLATION.XML`. Bộ nạo **thử mở
`<thư mục>\translation.xml` từ đĩa trước**, chỉ fallback sang bản nhúng khi
thất bại. → chỉ cần đặt file ở đúng thư mục là ghi đè được.

## Vị trí trong file

`Cubase15.exe` — PE32+ (x86-64), ImageBase `0x140000000`, 135.492.480 byte.

| | |
|---|---|
| Section chứa resource | `.rsrc` — RawPtr `0x07B78400`, RawSize `0x5BEA00` |
| Offset của XML | `0x07B79180` (3.456 byte vào `.rsrc`) |
| Kích thước | 4.874.598 byte |
| Data directory `Resource` | rva `0x07C8D000`, size 6.023.232 |
| Tên resource | `TRANSLATION.XML` (RT_RCDATA, lang 1031) |

Có **56 resource leaf** trong `.rsrc`; XML là cái đầu tiên, nằm ngay đầu section
(slack 2 byte sau nó). Đây là lý do phải biết đường dẫn mới ghi được.

## Định dạng

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Generated: 2026-03-02 15:46:18.29910159 +0100 -->
<Translation>
  <LanguageTable>
    <language key="us">English</language>
    <language key="de">German</language>
    ...
    <language key="ru">Russian</language>
  </LanguageTable>
  <StringTable>
    <String Key="File">
      <us>File</us><de>Datei</de><fr>Fichier</fr>...
    </String>
    <String Key="%d file(s) found">
      <us>%d file(s) found</us>
      <de>%d Datei(en) gefunden</de>
      ...
    </String>
  </StringTable>
</Translation>
```

- **10.737** mục `<String>`, mỗi mục có đúng **9** phần tử con (một cho mỗi ngôn ngữ)
- `String Key` trùng giá trị `<us>` ở **10.454 / 10.737 = 97%** → dịch khoá theo
  chuỗi tiếng Anh cho tiện tra cứu và kiểm tra
- Chuỗi trong file **không XML-escape** được áp dụng cho key (`&gt;` v.v. có mặt
  vì chính parser escape khi ghi ra)

### Bảng ngôn ngữ

Chỉ 9 ngôn ngữ, mỗi ngôn ngữ một khóa 2 ký tự. Thêm `<language key="vi">` là
đủ để ngôn ngữ xuất hiện (giả định: danh sách trong Preferences dựng từ
`LanguageTable` — **chưa xác minh được** vì lý do ở mục *Giới hạn*).

## Bộ nạp

Nguồn: `lib.frame-base\source\language\translator.cpp` (đường dẫn build còn sót
tại `0x06595570`).

Hàm nạp (VA `0x14455FF90`, entry trước đó tại file offset `0x455F3C0`):

```asm
0x14455FFCD  call     0x144305E80          ; -> &global  (getter 1 lệnh: lea rax,[rip+...]; ret)
0x14455FFD2  lea      rdx, [rax + 0x40]     ; &global.path  (std::wstring)
0x14455FFDB  call     0x1445caf70          ; copy ctor -> rsp+0x60
0x14455FFE4  lea      rdx, [rip + 0x203711D] ; L"translation.xml"   (UTF-16)
0x14455FFF0  call     0x1445bd130          ; nối -> <dir>\translation.xml
0x14455FFFD  mov      rcx, rsi
0x144560000  call     0x1445603e0          ; thử mở file; trả bool
0x144560005  test     al, al
0x144560007  jne      0x1445600c2          ; thành công -> BỎ QUA resource
0x14456000D  call     0x14450ade0          ; lấy app instance
0x14456001C  lea      rdx, [rip + 0x2037105] ; "translation.xml"   (ASCII)
0x14456003E  call     rbx                 ; -> nạp từ PE resource
```

Hàm mở file `0x1445603e0`:
- `call [rax+0x138]` lấy nhà cung cấp filesystem
- `call [r10]` (vtable `+0xD0`) mở file theo path → trả handle
- `call 0x1439df6e0` đọc nội dung
- `call 0x1445622b0` parse → trả bool

Có **hai** bản sao của hàm nạp (một ở `0x14455FF90`, một ở `0x144560200`) với
logic giống hệt nhau.

### Còn chỗ nào để dò

`global + 0x40` là `std::wstring` chứa thư mục. Getter trỏ tới biến toàn cục tại
file offset `0x77AE990` (RVA `0x78C1790`) — nằm trong section tên `.pdata`, nhưng
section này bị đặt tên lại trong binary (cùng nhóm `IPPCODE` / `IPPDATA` /
`.itt_not`), và nội dung runtime ở đó **không phải** một `std::wstring` (đọc được
con trỏ kiểu dữ liệu unwind table). Nên **chưa xác định được chính xác thư mục
mà loader tìm** bằng phân tích tĩnh.

## Giới hạn của việc xác minh

Máy đang chạy agent nằm ở **session 2 (disconnected)**, console là session 5 nhưng
đang kẹt ở màn LogonUI. Hệ quả:

- **input chuột/bàn phím giả không tới được app** — `GetForegroundWindow()` trả 0,
  `SetCursorPos` + `mouse_event` không được app nhận
- `PostMessage` **có** hiệu lực (đã dùng đóng hộp thoại Safe Mode bằng ENTER)
- `PrintWindow` **có** hiệu lực với cửa sổ chính của Cubase (đã chụp được Hub)
  nhưng **không** được với menu popup (DWM → ảnh đen)

Vậy nên **chưa xác minh được** danh sách Language có hiện "Vietnamese" hay không —
bước đó cần click trong hộp Preferences, mà click giả không tới app.

Cũng đã thử và **không** dùng được:
- `fsutil behavior query disablelastaccess` → `2` (tắt), bật lại thì NTFS vẫn
  debounce cập nhật → không đáng tin
- `icacls /setaudit` → tham số không tồn tại trên hệ thống này (exit 87)
- đặt SACL bằng `SetNamedSecurityInfo` qua PowerShell → lỗi API dễ dàng
  (`RawAcl` overload, `Marshal.Copy` ambiguity)

Cách chắc chắn còn lại: đọc event log 4663 sau khi bật audit thành công
(`auditpol /set /subcategory:"File System" /success:enable` chạy được), hoặc
chạy script tự động hoá trong một session có input desktop thật.

## Công cụ đã viết (`tools/research/`)

| | |
|---|---|
| `pe_info.py` | parse PE: section, data directory, liệt kê resource leaf kèm offset/size |
| `res_names.py` | đọc tên resource (UTF-16) trong cây `.rsrc` |
| `scan_xml.py` | quét nhịp `<?xml`, `<String Key=` và thống kê thẻ con theo ngôn ngữ |
| `binfind.py` | tìm chuỗi trong binary theo ASCII/UTF-16LE/UTF-16BE kèm context |
| `strings_at.py` | dump chuỗi ASCII + UTF-16 trong một dải offset |
| `xref.py` | quét `.text` tìm `lea/mov` RIP-relative trỏ tới một offset đích |
| `disasm.py` | disassemble (capstone), tự chú thích tham chiếu RIP bằng string literal |
| `readpath.py` | launch Cubase rồi đọc `std::wstring` trong bộ nhớ tiến trình |

Dùng lại:
```powershell
python tools\research\pe_info.py "E:\Steinberg\Cubase 15\Cubase15.exe"
python tools\research\disasm.py "E:\Steinberg\Cubase 15\Cubase15.exe" 0x14455FF90 0x300
```

## Bản vá ghi đè

`tools/build_translation.py` chèn ngay trước `</String>`:

```xml
<language key="vi">Vietnamese</language>   <!-- trước </LanguageTable> -->
...
<vi>Tệp</vi>                                <!-- cuối mỗi <String> -->
```

Mọi chuỗi **không** có `<vi>` sẽ rơi về `<us>` (tiếng Anh) — an toàn, không sinh
chuỗi rỗng. File tăng ~11 KB cho 438 mục.

## Hướng tiếp

1. Xác minh thư mục loader tìm (xem *Giới hạn*)
2. Nếu file override không ăn, chuyển sang vá PE: dựng lại `.rsrc` với XML mới
   ở đầu section, cập nhật `OffsetToData` của 56 resource leaf, kích thước
   section, và xoá entry Certificate (Authenticode chắc chắn hỏng khi sửa file)
3. Mở rộng `translations/batches/` — còn ~10.300 chuỗi
