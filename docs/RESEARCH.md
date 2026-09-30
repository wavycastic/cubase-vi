# Nghiên cứu: Cubase lưu chuỗi giao diện ở đâu và cách ghi đè

Ghi lại những gì đã dò được, để không phải RE lại từ đầu.

> Chủ đề riêng: cách Cubase 15 dựng và vẽ dải sóng âm thanh nằm ở
> [`WAVEFORM.md`](WAVEFORM.md) — gồm cả file cache `.peak`, thuật toán min/max
> theo cột pixel, và hệ quả với bản dịch tiếng Việt.

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
| `pe_info.py` | header, section, data directory, resource, `.pdata` function count |
| `res_names.py` | liệt kê resource leaf kèm offset/size |
| `scan_xml.py` | quét `<?xml`, `<String Key=`, thống kê thẻ con theo ngôn ngữ |
| `binfind.py` | tìm chuỗi theo ASCII/UTF-8/UTF-16LE/UTF-16BE kèm context |
| `strings_at.py` | dump chuỗi ASCII + UTF-16 trong dải offset (file offset, không phải length) |
| `xref.py` | xref đã verify qua `.pdata` + capstone; `--callers` để tìm hàm gọi |
| `disasm.py` | disassemble theo biên hàm `.pdata`, `--func` để decode trọn một hàm |
| `readpath.py` | launch Cubase rồi đọc `std::wstring` trong bộ nhớ tiến trình |
| `qm_dump.py` | đọc catalogue Qt `.qm` của Score Editor |
| `skin_srf.py` | giải nén `Skins/skin.srf`: template, màu, icon |
| `scoring_l10n.py` | so sánh bộ dịch tên nhạc cục giữa các ngôn ngữ |
| `strgrep.py` | quét chuỗi theo regex trong toàn bộ exe (ASCII/UTF-16), in offset |
| `ptr.py` | đọc con trỏ tại một VA, ghi chú nó trỏ vào hàm nào / chuỗi nào |
| `deobf_str.py` | giải mã chuỗi Steinberg bị obfuscate bằng LCG |

Tất cả dùng chung `tools/cubelib/`. Dùng lại:
```powershell
python tools\research\pe_info.py "E:\Steinberg\Cubase 15\Cubase15.exe" --find TRANSLATION.XML
python tools\research\disasm.py "E:\Steinberg\Cubase 15\Cubase15.exe" --func 0x1445B9960
python tools\research\xref.py "E:\Steinberg\Cubase 15\Components\ScoringEngine\ScoringEngine.dll" 0x4FAEBF0
```

### Bài học về công cụ

Hai lỗi cũ đáng ghi lại vì rất dễ lặp lại:

1. **Quét byte thô cho xref là sai.** RIP-relative displacement xuất hiện bên
   trong immediate và operand bytes, nên quét thô báo nhiều false positive.
   Ngược lại, quét chỉ nhận REX prefix (bản cũ) thì **bỏ sót hẳn** — đã thử
   trên `ScoringEngine.dll` và nhận 0 hit trong khi có 1 thật. Cách đúng: lấy
   biên hàm từ `.pdata` (exception directory — thứ mà loader dùng để unwind),
   lọc thô, rồi để capstone xác nhận từng hit.

2. **Đừng decode từ offset tùy ý.** Bản `disasm.py` cũ decode tuyến tính từ địa
   chỉ cho trước, nên lệch vài byte là sinh ra `sti` / `sahf` trông rất thuyết
   phục. Nay nó tự snap về đầu hàm theo `.pdata` và **nói rõ** khi nào không có
   `.pdata` phủ.

Ngoài ra: `.qm` dùng **độ dài block big-endian** (đọc little-endian ra số vô
lý nhưng trông hợp lý), và có bản ghi với `len = 0xFFFFFFFF` làm sentinel —
parser phải clamp chứ không tin độ dài, nếu không mất sạch mọi message phía sau.

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
3. ~~Mở rộng `translations/batches/`~~ — xong, 10.737/10.737

---

## Phát hiện sau (2026-09-30)

### `PSEUDO_LOCALIZATION` — cờ dev còn sót trong bản ship

`Cubase15.exe` file offset `0x659E520`, UTF-16, là **chuỗi duy nhất** khớp
pattern `[A-Z][A-Z0-9_]{4,}` mà trông như tên biến môi trường (quét hết file:
38 hit, 37 cái còn lại là tên tháng/ngày/thư viện Windows).

Chuỗi đó đi vào một hàm one-shot cache cờ:

```
0x1445BAEE0  dựng wstring L"PSEUDO_LOCALIZATION"
0x1445BAF70  call [rax+0xE8]        ; vtable của một singleton Steinberg
0x1445BAF76  mov [flag], al         ; cache vào global 0x1477BB324
```

Rồi ngay trong hàm nạp `translation.xml`:

```
0x1445600C2  call 0x1445B9950       ; hỏi cờ trên
0x1445600C9  je   skip
0x1445600CB  lea  r8, [L"Pseudolocalization"]   @0x6595538
0x1445600D2  lea  rdx, [@0x6595560]              ; = L"xx"
0x1445600DC  call 0x144561570       ; setLanguage("xx", "Pseudolocalization")
```

Tức bật cờ → Cubase tự chèn một ngôn ngữ giả có key `xx`, tên hiển thị
`Pseudolocalization`, để test layout với chữ bị accent + giãn dài. Có cổng
thứ hai ở `0x1445B9979`: so global với `"xx"` (cmp `'x'`, `'x'`, `0`).

**Chưa xác minh** giá trị biến nào bật được (`1`? chuỗi bất kỳ?).

### Score Editor có hệ l10n riêng

`Components/ScoringEngine/ScoringEngine.dll` (107 MB) là engine Dorico nhúng.
Nó **không** dùng `translation.xml`:

```
l10n/instrumentnames_{9 ngôn ngữ}.xml   624 entity mỗi file, ~360 KB
l10n/strings_{9 ngôn ngữ}.qm            catalogue Qt, 1,9–3,1 MB
l10n/strings_pseudo.qm, strings_mirror.qm, strings_chef.qm
l10n/qtbase_*.qm, icudt77l.dat
```

Cơ chế nạp là **glob**, không hardcode danh sách:

```
ScoringEngine.dll @0x4FAEBF2   .*instrumentnames_(\w+)\.xml
ScoringEngine.dll @0x4E672C2   *strings.*_(\w+)\.qm
ScoringEngine.dll @0x4E67114   %app  Steinberg::Steam::DoricoStringTranslator  l10n
```

`instrumentnames_en.xml` là **fallback hardcode** (xref tại `0x181931ACE`,
trong `DefaultAndUserLibrarySerialiser::loadAllPartsOfDefaultLibrary`).

Bảng ngôn ngữ trong engine — mảng tĩnh `{u32 id, u32 code}` 184 phần tử ở
file `0x4F12FD0` (id 0..183, code 936..1119), tên ở blob `0x4F13590`:

```
9 ngôn ngữ Steinberg trước: kEnglish kFrench kGerman kItalian kSpanish
                            kJapanese kChinese kPortuguese kRussian
rồi ~175 tên ICU, trong đó có kVietnamese @0x4F13E18
```

Hàm dùng bảng (`0x1805AEED0`) quét tuyến tính, sentinel = **địa chỉ chuỗi
`kEnglish`** ⇒ 1472/8 = 184 phần tử.

**Chưa xác minh:** không tìm thấy mảng `const char*[184]` song song, nên chưa
chắc vị trí thứ 170 trong blob tên ứng với id nào. Tra tên→enum đi qua bảng
băm quanh `0x4F12CF0`, chưa phân tích tiếp.

**Câu hỏi quyết định:** liệu app language `vi` có được truyền xuống thành
`kVietnamese` không. Trả lời bằng cách chạy Cubase, không phải bằng RE thêm.

### `strings_pseudo.qm` — chứa sẵn bộ chữ giả

Parse ra (1.784 message, 100% khớp bảng hash):

```
Register Now. Bork Bork Bork!
Rehearsel Merks
Remofe-a Ill Flows from this Leyooot
Remofing this instrooment will ilso remofe-a ill its moosic.
        Bork Bork Bork! Do yooo woont to continooe-a?
Solid/deshed continooeshoon line-a zeeeckness
```

Quy tắc (đoán từ mẫu): `b`→`oo`, `s`→`oo`, `v`→`f`, `d`→`ee`/`dd`, `m`→`mm`,
rồi nối `" Bork Bork Bork!"`. Đây là bộ **chuỗi mẫu biết trước sẽ tràn** —
dùng làm bài test layout cho bản dịch tiếng Việt.

### `Skins/skin.srf` — toàn bộ theme Cubase, giải nén được

20.292.176 byte, format: `/Thumbs.db\r\n` lặp trước mỗi member, rồi zlib
hoặc PNG raw. Giải hết **99,8%**:

| | |
|---|---|
| member | 842 |
| XML | 315 (22 khối `<skin>` + 293 khác) = 4,48 MB, **2.328 `<template>`** |
| ảnh | 486 PNG + 11 BMP + 5 SVG |
| bảng tên | `0x134DF87`, có `.gitignore` → export từ repo git nội bộ |

Tên trong bảng: `addtrackdialog.xml`, `audioconnections.xml`,
`channelsettings.xml`, `chordtrack.xml`, `cubase_pro.png`…

74 chuỗi `title=` trong skin XML **đều có** trong `translation.xml` → chúng là
key tra bảng, không phải bản dịch thứ hai. Phần mở được là **toàn bộ theme**.

### `instrumentnames_XX.xml` — làm được, và bốn lỗi trong đó

9 file, 624 entity, đều cùng 624 `entityID`. `parentEntityID` và
`inheritanceMask` **giống nhau từng byte** ở cả 9 ngôn ngữ, `<name>` ở cấp
entity cũng vậy, `gender` là `kNeutral` ở 624/624. Nên **file tiếng Anh là một
bản mẫu đầy đủ** — không cần ghép từ nhiều file.

Chỉ 5 ô trong `<data>` là được dịch:

```
uiName  singularFullName  singularShortName  pluralFullName  pluralShortName
```

`instrumentnames_en.xml` có **1.126 chuỗi phân biệt** trong 3.115 ô. Khối lượng
thật sự nhỏ hơn con số ô: 396 chuỗi xuất hiện đúng một lần, 463 chuỗi hai lần,
số còn lại 3–26 lần — nên dịch một chuỗi là được dùng ở nhiều entity.

#### Vì sao phải cắt chuỗi chứ không re-serialise

```
<?xml version="1.0" ?>          <- có khoảng trắng trước ?>

                            <- CRLF toàn bộ
				<parentEntityID/>        <- không có khoảng trắng trước />
```

Và entity `aluphone` xếp `<name>` **trước** `<entityID>`, còn 623 entity kia
xếp sau; nó còn mang thêm `<customVariantString/>` nằm giữa `<uiName>` và
`<singularFullName>`. Một vòng `ElementTree` sẽ viết lại cả những thứ đó.
Nên `cubelib/score.py` giữ nguyên văn bản, cắt trong từng khối entity, rồi
**parse lại bằng parser thật** để tự kiểm.

Bằng chứng cho cách làm này: dựng lại từng trong 9 file gốc với map rỗng, kết quả
**giống hệt file nguồn** ngoại trừ 625 marker `<language>`. 9/9 byte-exact.

#### Lỗi thật trong file của Steinberg

```
en : kEnglish = 625
de : kEnglish = 2     kGerman = 623
es : kEnglish = 1     kSpanish = 624
fr : kEnglish = 1     kFrench = 624
it : kEnglish = 1     kItalian = 624
ja : kEnglish = 1     kJapanese = 624
pt : kEnglish = 1     kPortuguese = 624
ru : kEnglish = 1     kRussian = 624
zh : kChinese = 624   kEnglish = 1
```

**Cả 8 file không-Anh đều còn sót `instrumentname.pitchedpercussion.aluphone` ở
`kEnglish`**; file Đức còn thêm `instrumentname.band.unpitched.marching.snare.drum.rim`.
Đó chính là entity Steinberg thêm tay vào bản tiếng Anh (nó có
`<customVariantString/>`) rồi copy nguyên xi sang các bản dịch mà quên dán nhãn
lại. `build` vì thế ghi đồng nhất cả 625 marker và báo `mis_tagged`.

Ngoài ra 5 ô tên **rỗng ngay trong file gốc**: `cajon.low` mất
`singularShortName`, `pluralFullName`, `pluralShortName`;
`clarinet.contra.alto.eflat` mất hai ô plural. Không phải lỗi dịch — đã kiểm
lại rằng bản dịch không làm rỗng thêm ô nào.

#### `import` từ bảng chính: 146/1.126 chuỗi đã có sẵn

`translations/vi.json` của chính repo này đã dịch **88** chuỗi tên nhạc cụ trùng
khớp, và còn **58** chuỗi nữa có mặt với giá trị giống hệt bản gốc
(`Conga`→`Conga`, `Guitar`→`Guitar`, `Sampler`→`Sampler`). `import` ghi cả hai
loại vào batch, vì map giống hệt **là một câu trả lời**, không phải một lỗ hổng.

Nó cũng **định nghĩa** khuôn dịch, thay vì để tôi tự nghĩ ra:

```
Tenor Drum (High)  →  Trống Tenor (Cao)
Tabla baya (larger) →  Tabla baya (Lớn hơn)
Bongo Bell         →  Chuông Bongo
Sleigh Bells       →  Chuông xe trượt tuyết
Large Gong         →  Cồng lớn
Brass              →  Bộ đồng
Marching Bass Drum (1 line) → Trống Bass diễu hành (1 dòng)
```

Còn `Crash Cymbal`, `Ride Cymbal`, `Sizzle Cymbal` **giữ nguyên** trong khi
`Marching Cymbals` lại thành `Chũm chọe diễu hành` — bản gốc không nhất quán,
và quy tắc đã dùng là "tên nhạc cụ thì giữ, tính ngữ mô tả thì dịch", nên giữ là
đúng.

#### Sáu luật đặt tên, đọc ra từ 9 catalogue chứ không phải từ khẩu vị

`instrumentnames_ja.xml` và `instrumentnames_de.xml` đã phải trả lời đúng câu
hỏi "cái nào là của ngôn ngữ này, cái nào giữ tiếng Anh", và chúng **thống nhất
trên từng chuỗi**:

| tiếng Anh | Nhật | Đức |
|---|---|---|
| Acoustic Guitar | アコースティックギター | Akustische Gitarre |
| Electric Guitar | エレキギター | Elektrische Gitarre |
| Fretless Bass | フレットレスベース | Fretless-Bass |
| Banjo | バンジョー | Banjo |
| Charango | チャランゴ | Charango |
| Ac. B. Gtr | Ac. B. Gtr | Ak. B.-Git. |
| Dul. | Dul. | Dul. |

⇒ **mô tả thì dịch, tên riêng thì thành mượn ngữ, chữ viết tắt thì để yên.**
Ba bản dịch còn lại (`es fr it pt ru`) không cần đọc: chúng chỉ khác ở dấu và
hậu tố, còn ba bản trên là hai ngôn ngữ có hình thái khác hẳn tiếng Anh.

Điểm khó nhất là phân biệt *tên riêng* với *tính ngữ mô tả* khi cả hai đều là
tính từ tiếng Anh. `English Horn` là tên riêng (vì cùng thứ đó còn tên Pháp là
`Cor Anglais`) nên giữ; `Electric` là tính ngữ mô tả nên dịch. Cùng một cách,
`Marching French Horn` → `French Horn diễu hành` — giữ tên, dịch tính ngữ.

#### Kết quả

1.126/1.126 chuỗi, 3.115/3.115 ô, 624 entity, 625 marker `kVietnamese`.
**591 chuỗi (52%) giữ nguyên tiếng Anh** — đây là kết quả đúng, không phải chỗ
sót. 1.220 ô thay đổi, 1.900 ô giữ nguyên (chủ yếu là chữ viết tắt và tên
mượn ngữ). Đã kiểm bằng parser thật: không entity nào ngoài 5 ô tên và
`<language>` bị đụng tới.

#### Hai lỗi trong code của chính repo, do bộ dò mới bắt

Cả hai đúng loại lỗi mà AGENT.md §3 cảnh báo — trông đúng nhưng âm thầm không
khớp gì:

1. `score.FORBIDDEN` là `dict.fromkeys([...số...])`, còn chỗ kiểm tra là
   `c in FORBIDDEN` với `c` là **ký tự**. Tra ký tự vào dict có khoá số **luôn
   trượt**. `check_text` vì thế trả về nguyên văn một chuỗi có byte NUL:

   ```
   >>> chr(1) in FORBIDDEN      # đúng như code đang viết
   False
   >>> 1 in FORBIDDEN
   True
   >>> check_text('a\x01b', 'k')
   'a\x01b'
   ```

   Nay là `frozenset` ký tự. Bài `TestCheckText::test_rejects` là thứ bắt được.

2. `source_strings` đếm mỗi **ô** chứ không phải mỗi **entity**, nên
   `uiName` và `singularFullName` (luôn trùng nhau) thành hai "người dùng".
   `--status` vì thế báo đội gấp đôi số bè mà một chuỗi tiết kiệm được. Nay
   khử trùng theo entity, và có test khoá lại hành vi này.

#### Một cái bẫy đo sai, đáng ghi lại

`git show HEAD:docs/RESEARCH.md | python -c "…"` báo **167 CRLF**, và tôi tin
nó. Nhưng `git show` chạy qua pipeline của PowerShell sẽ đi qua đối tượng
string và được phát lại **kèm CRLF** — 167 dòng thành 167 CRLF, dù blob trong
git là LF thuần:

```
subprocess.run(['git','show','HEAD:…'], capture_output=True).stdout
    → CRLF=0  LF=167          <- git nói thật
PowerShell | python
    → CRLF=167 LF=167        <- PowerShell bịa thêm
```

Tôi đã chuẩn hoá file thành CRLF theo con số đó. Đọc blob bằng `subprocess`
mới thấy bản thân file là LF, và đã trả lại LF. **Đo một blob bằng `subprocess`,
không bao giờ qua shell pipe** — cùng loại bẫy với `FORBIDDEN` ở trên: cái đo
chạy không báo lỗi, chỉ cho kết quả sai.
