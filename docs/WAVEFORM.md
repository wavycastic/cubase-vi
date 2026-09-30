# Nghiên cứu: Cubase 15 dựng và vẽ waveform (dải sóng âm thanh) thế nào

Ghi lại những gì đã dò được từ `Cubase15.exe`, để không phải RE lại từ đầu.

Đối tượng: `E:\Steinberg\Cubase 15\Cubase15.exe` — 135.492.480 byte, PE32+,
ImageBase `0x140000000`, 401.328 hàm trong `.pdata`.

Tài liệu này là **phần nghiên cứu** của repo dịch `translation.xml`. Mục §10 nói
riêng ra hệ quả với bản dịch tiếng Việt.

---

## Tóm tắt

1. Cubase 15 **không** vẽ waveform bằng cách đọc thẳng số mẫu mỗi lần vẽ. Nó dựng
   một **ảnh**: với mỗi **cột pixel**, tính một cặp `(min, max)` rồi tô thành dải.
2. Việc dựng ảnh diễn ra **ngoài luồng vẽ**, theo yêu cầu
   `(startPixel, numPixels, framesPerPixel)`, và có log riêng
   `startPixel:%12d numPixels:%12d framesPerPixel:%8.2f`.
3. Có **hai thuật toán**, chọn theo mức phóng:
   - `framesPerPixel < 1` (phóng sâu hơn 1 mẫu/pixel): vẽ thẳng bằng số mẫu thật,
     nối bằng đường thẳng giữa hai mẫu → đây là chỗ **nội suy** (interpolation).
   - `framesPerPixel >= 1`: gom **min/max theo từng cột pixel**.
4. Nguồn số liệu cũng có hai: **đọc thẳng từ file âm thanh** (phóng to) và
   **Audio Image đã dựng sẵn** (thu nhỏ). Ranh giới là `framesPerPixel` so với
   một ngưỡng lấy từ accessor, mặc định **8192**.
5. Audio Image được cache trong file riêng đuôi **`.peak`**, tên hiển thị
   **"Audio Image File"**, chữ ký 4 byte đầu là `PEAK`. Đây là lý do các chuỗi
   dịch nói `Audio Image` chứ không nói `peak file`.
6. `WaveFileHandler` của Cubase 15 **không biết chunk `PEAK`** của WAV — không có
   peak data nào nằm trong file WAV. Danh sách chunk nó biết: `riff `, `wave`,
   `fmt `, `data`, `junk`, `bext`, `iXML`.

---

## 0. Thuật ngữ: `Waveform` trong Cubase 15 có bốn nghĩa khác nhau

| Nghĩa | Ví dụ trong `keys/all_strings.tsv` | Offset ASCII trong exe |
|---|---|---|
| **Dải sóng hiển thị của audio event** | `Show Waveforms`, `Waveform Brightness`, `Waveform Outline Intensity`, `Interpolate Audio Waveforms`, `Zoom In/Out On Waveform Vertically` | `0x05FA4200`, `0x05FA4220`, `0x05FA4230` |
| **Ảnh cache của dải sóng** (không phải thứ hiển thị) | `Create Audio Images During Record`, `Update Image`, `Image under construction...` | `0x05FBB8F0`, `0x05FF8D50` |
| **Dạng sóng LFO** (hình học của LFO, không liên quan tới âm thanh) | `Waveform`, `Wavelength`, `Length as PPQ` (Retro Volume / MIDI Echo) | `0x05F2C350`, `0x05F2C370` |
| **Định dạng file WAV / BWF** | `Wave File`, `Broadcast Wave`, `Wave 64 File`, `RF64 Broadcast Wave File` | `0x05FFE8D8`, `0x05FFED70` |

Còn `Peak` thì gần như **luôn** nghĩa là *đỉnh tín hiệu* (True Peak, Meter Peak,
`Filter Hitpoints by Peak Level`) — không phải dải sóng. Riêng chỗ này
`Hitpoint` + `Peak` là hai khái niệm độc lập: `Peak Level` là biên độ, không liên
quan tới việc có hiện hitpoint hay không.

---

## 1. Chuỗi và khoá cấu hình liên quan

Cùng một khối `.rdata` (vùng lớp `PAudioImage`), toạ độ **file offset**:

| Nhãn UI (UTF-16, hiện cho người dùng) | offset | Pref id nội bộ (ASCII) | offset |
|---|---|---|---|
| `Interpolate Audio Waveforms` | `0x05FA2C08` | `Interpolate Audio Images` | `0x05FA2F58` |
| `Show Waveforms` | `0x05FA3780` | `Show Waveforms` | `0x05FA4200` |
| `Waveform Brightness` | `0x05FA3848` | `Wave Brightness` | `0x05FA4220` |
| `Waveform Outline Intensity` | `0x05FA3870` | `Wave Outline Intensity` | `0x05FA4230` |
| `Background Color Modulation` | `0x05FA38A8` | `Background Color Modulation` | `0x05FA4248` |
| `Show Hitpoints on Selected Events` | `0x05FA3800` | `Show Hitpoints` | `0x05FA4210` |
| `Show Event Volume Curves Always` | `0x05FA3740` | — | — |
| `Use Mouse Wheel for Event Volume and Fades` | `0x05FA3960` | `Use Mouse Wheel for Event Volume` | `0x05FA4268` |
| — | — | `Show Filename` | `0x05FA41F0` |

**Phạm vi (scope) của nhóm tuỳ chọn là chuỗi `PAudioImage`** (`0x05F946A8`), nhóm
giao diện là `Audio` (`0x05EDD050`). Cả hai đều là chuỗi ASCII và được đọc ở
`0x141EB9900` (dựng trang Preferences) và `0x141E9ED00` (đọc giá trị).

```
0x141EB9A3A  lea  r8, [rip+…]        ; "Show Waveforms"
0x141EB9A41  lea  rdx, [rip+…]       ; "PAudioImage"
0x141EB9A4B  call [rax+0x120]        ; đăng ký pref id trong scope PAudioImage
0x141EB9A54  lea  rdx, [rip+…]       ; "Audio"
0x141EB9A5E  call [rax+0x110]        ; gắn nhóm giao diện
```

> Nhãn UI và pref id **không giống nhau** (`Waveform Brightness` vs
> `Wave Brightness`). Kết quả: xref `Show Waveforms` chỉ có **1** hit (trang
> Preferences) — phần vẽ không tra chuỗi này nữa, nhiều khả năng đọc giá trị đã
> đẩy qua observer. **Chưa truy được** chỗ đọc trong lúc vẽ.

---

## 2. Pipeline: từ file âm thanh tới pixel

```
0x141E9B6F0   điều phối: so số kênh của 2 nguồn, cấp phát 2 buffer
 ├─ framesPerPixel <  1.0 ──► 0x141E9D4C0   vẽ bằng số mẫu thật (3.192 byte)
 └─ framesPerPixel >= 1.0 ──► 0x141E9A540 ──► 0x141E9C340
                                  │             dựng mảng (min,max) theo cột pixel
                                  │              ├─ 0x1421F3650  tạo đối tượng đọc lát
                                  │              │     ├─ 0x28 byte: qua Audio Image cache
                                  │              │     └─ 0x70 byte: đọc thẳng file (ctor 0x1421F4EE0)
                                  │              └─ vtable: +0x18 số frame, +0x20 đọc 1 cặp,
                                  │                          +0x28 đọc cả khoảng
                                  └─ nếu thiếu dữ liệu → trả false
                                       │
0x141E9E140   vẽ: nối các (min,max) thành dải;  -0.0f = cột không có dữ liệu → bỏ qua
```

Các tên lớp xuất hiện trong chính exe (không phải RTTI, mà là chuỗi tên dùng cho
đăng ký lớp `CmObject`):

| Chuỗi | offset | Vai trò |
|---|---|---|
| `PAudioImage` | `0x05F946A8` | lớp nền, giữ scope của nhóm pref |
| `PAudioImage::ConstructorThread` | `0x05FA30C8` | lớp **thread** dựng ảnh ngoài luồng vẽ |
| `Steinberg::Warp::PAudioEventImage` | `0x05FA39D8` | đối tượng vẽ audio event trong Project Window |
| `PAudioEventInCollapsedFolderImageCreator` | `0x05FA3A00` | ảnh event khi track bị thu gọn |
| `PAudioClipViewer` | `0x05FA36D8` | khung xem audio clip |
| `MAudioCollector::FlatSliceIterator` | `0x05FA2AD8` | duyệt lát âm thanh phẳng |
| `AudioImageCache` | `0x05FF9020` | cache ảnh trong RAM |
| `AudioImageCacheAccessor` | `0x05FF90D0` | cổng truy cập cache |
| `AudioImageFile` | `0x05FF91B0` | ảnh trên đĩa (file `.peak`) |
| `AudioImageAccessor` | `0x05FF9260` | cổng truy cập ảnh trên đĩa |
| `PSeqEventImageScheme` | `0x062F52E8` | skin scheme cho ảnh event |
| `StMedia::AudioImageColumnHandler` | `0x062F6B80` | phía StMedia đọc/ghi cột của `.peak` |
| `MWaveInterpolator` | `0x060A81B0` | bộ nội suy (cùng nhóm `MSineInterpolator`, `MParabolaInterpolator`) |

Hai chuỗi `Image under construction...` (`0x05FA2C40`) và `Image construction error`
(`0x05FA2C78`) là **trạng thái lúc dựng ảnh** — dấu hiệu rõ rằng việc dựng ảnh là
bất đồng bộ: UI có lúc chỉ, có lúc báo lỗi.

---

## 3. Thuật toán min/max theo cột pixel — `0x141E9C340`

`.pdata` cho hàm: RVA `0x1E9C340..0x1E9C85F` (1.311 byte).

### 3.1 Tham số

| Vị trí | Ý nghĩa |
|---|---|
| `rcx` | đối tượng Audio Image (giữ `[rcx+0x18]` = nguồn lát) |
| `rdx` | con trỏ ra: **mảng kết quả**, mỗi phần tử **8 byte = 2 × float32** |
| `r8d` | `startPixel` |
| `r9d` | `numPixels` |
| `[rsp+0x130]` | `framesPerPixel` — `double` |
| `[rsp+0x140]` | con trỏ chuyển đổi miền thời gian (warp), có thể `null` |

Ngay đầu hàm log:

```
0x141E9C3B2  lea  rax, [rip+…]   ; "startPixel:%12d numPixels:%12d framesPerPixel:%8.2f"
```

Đây là chỗ **duy nhất** trong exe in ra ba đại lượng này — nếu muốn xác minh hành
vi thực tế thì đây là chỗ cài log.

### 3.2 Chuẩn bị

```
xmm6 = startPixel * framesPerPixel              ; vị trí frame đầu
xmm7 = (startPixel+numPixels) * framesPerPixel  ; vị trí frame cuối
nếu có converter (warp):
    nếu converter->mode() == 0x0A (VT_R8):
        bỏ qua
    ngược lại:
        dựng Variant kiểu 10 (double) rồi converter->vfunc+0x28(&variant)
    rồi gọi converter->vfunc+0x20(start) và vfunc+0x20(end)
r15d = nguồn->vfunc+0x38()                      ; SỐ KÊNH
iterator = 0x1421F3650(rcx, xmm1=start, xmm2=end, r9d=channels, fpp)
frames  = iterator->vfunc+0x18()                ; số frame trong lát
```

`xmm7` ở `0x141E9C501` nạp hằng `1.0` (`0x145ED62F0`), `xmm7` ở `0x141E9C666`
nạp hằng `0.5` (`0x145ECCF38`).

### 3.3 Nhánh A — phóng to (nội suy)

Điều kiện: `1.0 <= framesPerPixel / frames` thì sang **nhánh B**. Tức nhánh A xảy
ra khi **một pixel nhỏ hơn lát dữ liệu**.

Với mỗi cột:

```
t = (pixel * framesPerPixel) / frames           ; 0..1 trong lát
i = (int)t                                     ; cắt phần nguyên
f = t - i                                      ; phần thập phân
v0 = iterator->getPair(i * channels)            ; 8 byte: (a0, b0)
v1 = iterator->getPair((i+1) * channels)        ; 8 byte: (a1, b1)
nếu getPair thứ hai trả false → dùng luôn (a0, b0)
kết quả = lerp:  a = a0*(1-f) + a1*f ,  b = b0*(1-f) + b1*f
ghi 8 byte ra con trỏ ra; con trỏ += 8
```

Chính là **nội suy tuyến tính riêng cho min và max**, theo phần thập phân của vị
trí mẫu. Đây là cơ chế phía sau tuỳ chọn *Interpolate Audio Waveforms*.

Chỗ `f < 0` thì `1.0 - f` vẫn đúng, nên nhánh này không cần `min/max` thủ công.

### 3.4 Nhánh B — thu nhỏ (gom min/max)

Điều kiện ngược: `framesPerPixel >= frames` → mỗi pixel **bao trọn** cả lát.

```
y0 = round_half_away((pixel * fpp) / frames)    ; "cắt ±0.5 rồi cắt phần nguyên"
last = (int)(obj[0x30]/channels * obj[0x38] / frames) * channels - 1
với mỗi cột:
    y1 = round_half_away(((pixel+1) * fpp) / frames)
    rows = max(y1 - y0, 1)
    với mỗi kênh:
        nếu chỉ số < 0 hoặc > last → ghi 8 byte 0 (cột rỗng)
        ngược lại:
            end = min(last, (rows-1)*channels + kênh + y0*channels)
            iterator->vfunc+0x28(start = y0*channels + kênh, end, channels, &out)
            ghi 8 byte
```

`vfunc+0x28` là **truy vấn cả khoảng** → trả về `(min, max)` của khoảng frame đó,
một lần cho tất cả kênh. Đây là đường đi khi dữ liệu nằm trong Audio Image hoặc
khi phải đọc file.

Làm tròn kiểu *round half away from zero*: `x < 0 ? x - 0.5 : x + 0.5` rồi `cvttsd2si`.

### 3.5 Vì sao lúc dựng phải dư 1 pixel mỗi bên

Hàm điều phối `0x141E9B6F0`:

```
ebx = numPixels + 3                            ; kích thước buffer tính bằng CỘT
r8d = startPixel - 1                           ; startPixel thật
r9d = numPixels + 2                            ; numPixels thật
buffer = channels * (numPixels+3) * 8 byte
```

Tức hình ảnh luôn được dựng **rộng hơn 2 pixel** và lệch 1 pixel, để khi vẽ chồng
nhiều event cạnh nhau thì mép nối không bị hở. Kích thước buffer được kiểm tra
lại ngay trước khi vẽ ở `0x141E9E140`.

---

## 4. Phóng sâu: `0x141E9D4C0`

RVA `0x1E9D4C0..0x1E9E138` (3.192 byte) — nhánh dùng khi `framesPerPixel < 1.0`,
tức mỗi pixel chỉ che dưới 1 số mẫu.

Đây là chỗ **không dựng ảnh trung gian**: đọc số mẫu thật rồi vẽ các đoạn thẳng
nối giữa hai mẫu liền kề. Trong hàm thấy rõ bộ toán học pixel→mẫu:

```
xmm6 = 1.0 / (số frame)                        ; 0x141E9D5CA, hằng tại 0x145ED62F0
(cột) → mẫu:  cvttsd2si(mẫu), trừ phần nguyên để lấy floor
              và cộng/trừ để lấy ceil, rồi vẽ đoạn [floor, ceil]
xmm9 = min(x, 3.0)                             ; 0x141E9DA97, hằng tại 0x145EDDF60
```

Hằng `3.0` ở `0x145EDDF60` là **giới hạn trên** của một đại lượng đo bằng pixel ở
đây (nhiều khả năng chiều cao băng vẽ tính bằng số dòng). Chưa xác minh được nó
chặn cái gì.

---

## 5. Nguồn dữ liệu: cache hay file — `0x1421F3650`

Hàm này chọn một trong hai loại đối tượng đọc dữ liệu:

```
if (nguồn->cacheAccessor == null)  limit = 8192 (0x2000)      ; 0x1421F369F
else                               limit = cacheAccessor->vfunc+0x18()
if (framesPerPixel <  limit)  → tạo đối tượng 0x70 byte (ctor 0x1421F4EE0)  ; đọc thẳng
else                          → tạo đối tượng 0x28 byte                     ; qua cache
```

- **0x28 byte** = bọc `AudioImageCacheAccessor`: `+0x00` vptr vào khối vtable
  `0x145FFAC20`, `+0x10` vptr `AudioImageCacheAccessor` (`0x145FFACA0`),
  `+0x18`/`+0x20` giữ con trỏ lấy từ nguồn.
- **0x70 byte** = đọc lát thẳng; nhiều khả năng là
  `MAudioCollector::FlatSliceIterator` của StMedia (**chưa xác minh** — tên lớp nằm
  ở khối `.rdata` khác nên chỉ suy từ vị trí và hành vi).

Nghĩa là: **thu nhỏ thì đọc ảnh đã dựng sẵn; phóng to thì đọc file**. Ngưỡng mặc
định 8192 nghĩa là một cột pixel ở mức thu nhỏ còn tối đa 8192 frame — nếu
Audio Image có độ phân giải cao hơn thì ngưỡng do accessor báo.

---

## 6. File `.peak` — "Audio Image File"

Đăng ký loại file tại `0x14161AF40`:

| Trường | Giá trị | offset |
|---|---|---|
| id | `com.steinberg.peakfile` | `0x05FF8D80` (UTF-16) |
| đuôi file | `peak` | `0x05FF8DF8` (UTF-16) |
| mime | `application/x-vnd.Steinberg-Peak` | `0x05FF8DB0` (UTF-16) |
| tên hiển thị | `Audio Image File` | `0x05FF8E08` (UTF-16) |
| chữ ký 4 byte | `PEAK` | hằng `0x5045414B` nạp vào `r8d` |

```
0x14161AF4B  mov  r8d, 0x5045414B     ; 'PEAK'  <- chữ ký đầu file
0x14161AF56  lea  r9,  [rip+…]        ; L"peak"
0x14161AF5D  lea  rax, [rip+…]        ; L"application/x-vnd.Steinberg-Peak"
0x14161AF69  lea  rdx, [rip+…]        ; L"Audio Image File"
```

Còn lại:

- `Updating Image on "%s"` (`0x05FF8D50`) — log khi cập nhật, nằm trong
  `0x14161B090`.
- `Trying to match image files...` — lúc MediaBay/Pool khớp file ảnh với file
  audio.
- `Create Audio Images During Record` — tuỳ chọn tạo ảnh ngay khi thu âm.

### 6.1 Đường dẫn nguồn nội bộ: giải mã xong mới thấy

Hàm `0x14161B090` (log `Updating Image on "%s"`) gọi `0x1421F5FC0`, và hàm đó
**không** chứa chuỗi nào dạng rõ — nó dựng chuỗi bằng cách tự giải mã lúc chạy:

```
mov  ecx, 0xDC1BE0D5                 ; seed
mov  dword [rbp-0x45], 0xC869C191    ; key (immediate, little endian)
mov  dword [rbp-0x41], 0xD462F014
mov  dword [rbp-0x3D], 0xB8198004
movdqa xmm, [0x145FFAF50] / [0x145FFAF70] / [0x145FFAF40]   ; key còn lại
mov  byte [rbp-9], 0x55
mov  r9d, 0x3D                       ; 61 byte
lặp: out[i] = (state & 0xFF) ^ key[i]
     state = (state * 0xBC8F) % 0x7FFFFFFF
```

Giải mã ra:

```
D:\T1\work\40ff4699062de924\lego\source\audiofile\aimage.cpp
```

Tức **mã Audio Image nằm ở `audiofile/aimage.cpp`** trong cây nguồn Steinberg
(tên dự án nội bộ là `lego`). Có **3.965** chỗ dùng đúng thuật toán này trong
`Cubase15.exe`, nên nếu cần tên đường dẫn nguồn hay tên biến nội bộ thì giải mã
tiếp được — xem `tools/research/deobf_str.py`.

Trong vùng code Audio Image có tới **6** bản giải mã, và cả hai bản đầu đều ra
cùng một chuỗi (một bản cho assert, một bản cho log).

---

## 7. Bằng chứng: WAV của Cubase 15 không có chunk `PEAK`

Bảng id chunk mà `WaveFileHandler` / `Wave64FileHandler` biết (vùng
`0x05FFE8C8`–`0x05FFEDF0`, chuỗi ASCII 4 byte):

```
riff   wave   fmt   data   junk   bext   iXML
```

Quét toàn exe không có chuỗi `PEAK` nào (chỉ có `BEXT/BWF_MAX_TRUE_PEAK_LEVEL`).
Kết luận: **không có peak data trong file WAV**; Cubase 15 giữ nó ở file `.peak`
riêng và trong RAM. Đây là khác biệt so với các phiên bản ghi peak vào chính WAV.

---

## 8. Skin: màu dùng để vẽ dải sóng

`Skins/skin.srf` (20.292.176 byte, nén zlib) — giải ra được nhờ
`tools/research/skin_srf.py`. Các id trong `<color>`:

| id | giá trị trong skin |
|---|---|
| `eventBackDefault` | `$210,020,070` |
| `eventBackMuted` | `$210,010,095` |
| `eventWaveMuted` | `$210,005,090` |
| `eventWaveAutomFill` | `$210,015,090` |
| `eventWaveAutomLine` | `$210,015,075` |
| `eventFrame` | `$000,100,100` |
| `eventFrameActive` | `gray10` |

Điểm mấu chốt, đã kiểm lại bằng thực nghiệm: **skin không hề có id cho dải sóng
bình thường.** Liệt kê toàn bộ id chứa `wave` trong `skin.srf` chỉ ra đúng ba màu
— `eventWaveMuted`, `eventWaveAutomFill`, `eventWaveAutomLine` — và cả ba đều gắn
với trạng thái *mute* hoặc lớp phủ đường volume. Không tồn tại `eventWave` /
`eventWaveNormal` tương đương.

Hệ quả: **dải sóng bình thường lấy màu từ màu track**, không phải từ skin. Đó là
lý do sửa `eventBackDefault` không làm dải sóng đổi màu — track colour ghi đè mọi
thứ skin đặt. `eventBackDefault` chỉ là *mặc định* cho track chưa gán màu.

Vì vậy muốn dải sóng nhiều màu như FL Studio thì **sửa skin là ngõ cụt**, phải
can thiệp bằng DLL. Xem §13.

Khi event bị **mute** thì dải sóng đổi sang `eventWaveMuted`;
`eventWaveAutomFill` + `eventWaveAutomLine` là lớp phủ cho **đường volume của
event** vẽ đè lên dải sóng (fill + đường). Đây là cặp màu mà *Waveform
Brightness* và *Waveform Outline Intensity* điều chỉnh.

Cùng vùng đó còn có `bmEventWarped`, `bmEventMusical` — icon đánh dấu event đã warp
và event ở chế độ musical, cũng nằm trên nền dải sóng.

Phần vẽ (`0x141E9E140`) đọc cờ ở bitfield `[r13+0xB0]`, bit 4 và bit 5
(`shr eax,4` / `shr eax,5` rồi `test al,1`), và so sánh mỗi phần tử với hằng
`-0.0f` (`0x145FA4E40`) để bỏ qua cột không có dữ liệu.

---

## 9. Waveform ở những màn khác

| Màn | Bộ phận (chuỗi / offset) |
|---|---|
| Sample Editor | `PSampleEditorWaveController` `0x05F85E30`, `PSampleEditWaveLayer` `0x05F86E98`, `WWaveZoom` `0x06136710`, `WaveFrame` `0x061BF9E8`, `wave::verticalZoom` `0x05F88958`, `wave::verticalScroll` `0x05F88980` |
| MixConsole | `MIXER_WAVEFORMS` `0x060E7580`, `mixerWaveforms` `0x0628E830`, `VstWaveMeter` `0x062775B0`, `VstPlaybackWaveView` `0x061EE1B0` |
| MediaBay | `AudioImage` `0x05FBB8F0`, `MediaAudioPreview` `0x05FBB898`, `MediaFrameCount` `0x05FBB790`, `mbAudioPreviewZoneColor` `0x05FBB918` — MediaBay có **bộ Audio Image riêng**, không dùng chung với Project Window |
| Meter | `MPeak1L`…`MPeak12R` `0x06136D88`…, `MPeak%dL/R` `0x06137F18` — đây là **đỉnh meter**, không liên quan dải sóng |

---

## 10. Hệ quả với bản dịch tiếng Việt

### 10.1 Chỗ đang lệch nhau (đã kiểm tra trong `translations/vi.json`)

| key | bản dịch hiện tại | vấn đề |
|---|---|---|
| `Show Waveforms` | `Hiện Waveforms` | giữ tiếng Anh |
| `Waveform Brightness` | `Dạng sóng Độ sáng` | dịch NLV + hoa chữ sai (`Dạng` đầu câu) |
| `Waveform Outline Intensity` | `Cường độ đường viền dạng sóng` | dịch NLV, còn key kia giữ tiếng Anh → **cùng một trang Pref mà hai kiểu** |
| `Zoom In/Out On Waveform Vertically` | `Phóng vào dạng sóng theo chiều dọc` / `Thu nhỏ dạng sóng…` | dịch NLV |
| `Image under construction...` | `Image dưới construction...` | **nửa Anh nửa Việt** |
| `Trying to match image files...` | `Trying vào match image files...` | **nửa Anh nửa Việt** |
| `Updating Image on "%s"` | `Updating Image trên "%s"` | nửa dịch |
| `Show Event Volume Curves Always` | `Hiện Event Volume Curves Always` | bỏ sót `Always` |
| `Use Mouse Wheel for Event Volume and Fades` | `Use Mouse Wheel cho Event Volume and Fades` | trộn |
| `Filter Hitpoints by Intensity` | `Filter Hitpoints theo Intensity` | trộn |

Toàn bộ 10.737 chuỗi chỉ có **6** chuỗi chứa `Waveform`; trong đó 5 dùng
`dạng sóng`, 1 giữ `Waveforms`.

### 10.2 Đề xuất chốt thuật ngữ

- **`Waveform` giữ tiếng Anh**, cùng hạng với `Track`, `Event`, `Hitpoint`,
  `Automation` trong AGENT.md §3 — không có lý do dịch `dạng sóng` khi Cubase đã
  dùng `Waveform` cho cả nhãn Pref lẫn nhãn Zoom. `sóng` còn dễ lẫn với
  *audio waveform* và *LFO waveform* (§0) — giữ `Waveform` tránh được chỗ này.
- **`Audio Image` giữ nguyên**, vì đó là tên Cubase đặt cho **file `.peak`**;
  dịch `hình ảnh âm thanh` sẽ làm mất liên hệ với việc xoá/nhân bản file đó.
- **`Peak` = đỉnh tín hiệu**, không bao giờ dịch thành `đỉnh sóng`.
  `Filter Hitpoints by Peak Level` → giữ `Peak Level`.
- Chuỗi nửa Anh nửa Việt ở §10.1 là lỗi thật, không phải lựa chọn thuật ngữ —
  nên sửa.

Chưa sửa gì trong `translations/` — nghiên cứu này chỉ để dùng sau.

---

## 11. Công cụ mới trong `tools/research/`

| | |
|---|---|
| `strgrep.py` | quét **hình dạng** chuỗi trong toàn bộ exe (ASCII hoặc UTF-16LE), in offset để nối tiếp vào `xref.py`. `binfind.py` chỉ tìm đúng một chuỗi; cái này dùng để liệt kê cả nhóm, ví dụ mọi tên lớp có `Wave` |
| `ptr.py` | đọc con trỏ tại một VA và ghi chú từng con trỏ trỏ vào đâu: nằm trong `.pdata` không, chuỗi gì, hay header PE. Đây là công cụ đi từ "tên lớp" tới "danh sách hàm" |
| `deobf_str.py` | giải mã chuỗi Steinberg bị obfuscate bằng LCG (`state * 0xBC8F`) |

```powershell
python tools\research\strgrep.py "E:\Steinberg\Cubase 15\Cubase15.exe" "AudioImage" 
python tools\research\ptr.py "E:\Steinberg\Cubase 15\Cubase15.exe" 0x05FF9020 --count 6
python tools\research\deobf_str.py "E:\Steinberg\Cubase 15\Cubase15.exe" 0xDC1BE0D5 `
    --key x91c169c8 --key x14f062d4 --key x048019b8 `
    --key f0x5FF9350:16 --key f0x5FF9370:16 --key f0x5FF9340:16 --key x55 --len 61
```

---

## 12. Bẫy đã vấp

1. **`.data` có `vsize` > `rsize`.** Vùng BSS không nằm trong file, nên
   `pe.rva_to_off()` trả về offset chỉ đúng *bằng tình cờ*: offset đó rơi vào
   section kế tiếp trong file và đọc ra dữ liệu `.pdata` trông rất giống code.
   Đã vấp với `0x14772F4D0` (bảng đăng ký lớp của `MWaveInterpolator`): đọc ra
   3 cặp `RUNTIME_FUNCTION`, trông như bảng con trỏ hàm.
2. **Địa chỉ BSS không xref tĩnh được.** `xref.py` khớp theo *file offset*; code
   tham chiếu BSS bằng VA nên không có byte nào trong file để khớp. Với
   `0x14770BE30` (bảng đăng ký loại file `.peak`) xref trả về 0 hit **đúng**, dù
   chắc chắn có code dùng nó.
3. **Nhiều vtable dính nhau trong `.rdata`.** Chuỗi tên lớp nằm *trước* vtable
   (`AudioImageCache` @`0x05FF9020`, vtable @`0x05FF9030`) nhưng các vtable sau
   thuộc lớp khác, và nhiều vfunc chỉ là *thunk 5 byte* (`lea rax,[rip+…]; mov
   [rdx],rax; ret`) — nhìn qua tưởng là hàm thật. Phải kiểm tra `.pdata` trước khi
   disassemble.
4. **`imul ecx, ecx, 0xBC8F` không phải `%`.** Phép chia cho `0x7FFFFFFF` được
   làm bằng `edx = high32(n*3)` rồi mới dịch chuyển, nên chỉ đúng khi state vượt
   `2^31`. Viết bằng `%` cho ra chuỗi sai.
5. **Immediate trong key phải little endian.** `mov dword [rbp-0x45], 0xC869C191`
   nghĩa là byte `91 C1 69 C8`.

---

## 13. Ba bài học sau vụ sửa skin làm Cubase crash

### 13.1 Cubase crash vì `skin.srf` bị dịch byte — và cách vá đúng

Ghi đè `skin.srf` xong thì Cubase **crash ngay** (hai lần, 10:54:02 và 10:54:30).
Cả hai dump giống hệt nhau:

| | |
|---|---|
| mã lỗi | `0xC0000005 ACCESS_VIOLATION`, **đọc** tại địa chỉ `0x0` |
| chỗ lỗi | `RIP 0x144A91782` → RVA `0x4A91782`, hàm `0x4A91760..0x4A9187B` |
| lệnh lỗi | `movss xmm6, dword ptr [rdx]` với `rdx = 0` |
| `RAX = RCX` | `0x14F870` (địa chỉ trên stack) |

Hàm đó là hàm copy một struct (`float`, `u16`, `u32`, `u64`, chuỗi) và **không
kiểm tra null** — người gọi truyền vào con trỏ null. Hai dump trùng tuyệt đối cả
RIP lẫn giá trị thanh ghi, nên đây là lỗi tất định, không phải tranh chấp bộ nhớ.

Nguyên nhân: **49.865 byte cuối `skin.srf` là bảng tra cứu, ghi offset của từng
member.** Nén lại member đã sửa làm kích thước nó nhỏ đi 4 byte, mọi member phía
sau dịch vị trí, còn bảng thì không — Cubase đọc bảng ra địa chỉ sai và nhận về
con trỏ null.

Cách vá đúng là **giữ nguyên độ dài**: nén xong thêm khoảng trắng vô nghĩa trong
XML cho tới khi `len(zlib.compress(payload, 9))` trùng đúng kích thước cũ.
`tools/skin_edit.py` có cờ `--keep-size` làm việc này, và `make_fl_skin.py
--install` **mặc định bắt buộc** dùng nó (`--allow-resize` để tắt). Kết quả kiểm
chứng:

```
kich thuoc       20.292.176 -> 20.292.176   (+0)
member #82       12.943 -> 12.943          (+0)
vung member      0x0..0x134DF87            (không doi)
bang tra cuu     49.865 byte cuoi: GIONG NHAU
so member        842 vs 842, khac payload: [82]
```

Sau đó Cubase chạy 150 giây, RAM ~1 GB, **không sinh dump nào**.

Cách kiểm chứng bằng thực nghiệm: khởi chạy Cubase rồi canh
`%USERPROFILE%\Documents\Steinberg\CrashDumps`. Bản gốc → không dump; bản vá
đổi kích thước → dump ngay.

### 13.2 Khoảng giá trị của pref, lấy từ mã dựng trang Preferences

`Wave Brightness` và `Wave Outline Intensity` chỉ có **một** xref mỗi cái, đều
nằm trong cùng hàm dựng trang Preferences `0x1EB9900..0x1EB9DE2`. Ngay trước mỗi
lần gắn nhãn có một cặp `edx` / `r8d` chính là min/max:

| pref | mã | min | max | số trang |
|---|---|---|---|---|
| `Wave Brightness` | `0x141EB9B40` | `edx = 0xFFFFFF9C` → **−100** | `r8d = 0x64` → **100** | 2 |
| `Wave Outline Intensity` | `0x141EB9C07` | `edx = 0` → **0** | `r8d = 0x64` → **100** | 3 |
| `Background Color Modulation` | `0x141EB9CC8` | — | — | 4 |

Chuỗi tương ứng: `Wave Brightness` ở VA `0x145FA5E20`, `Wave Outline Intensity` ở
`0x145FA5E30`, `Background Color Modulation` ở `0x145FA5E48` (cả ba trong
`.rdata`).

Hệ quả thực tế: giá trị cài sẵn `−25` và `15` **không sai**, chỉ là thay đổi quá
nhẹ nên nhìn không ra. Đẩy hết mức (`100` / `100`) mới thấy rõ.

### 13.3 Bug tự kiểm trong `set_prefs.py` nuốt mọi lần sửa

Điều kiện kiểm diff là:

```python
if not om or not nm_ or om.group(1) not in touched \
        or om.group(1) != nm_.group(1) or om.group(2) != nm_.group(2):
```

Vế `om.group(2) != nm_.group(2)` so **giá trị cũ với giá trị mới**, tức đòi giá
trị không được đổi — trái ngược ý định. Mọi lần sửa hợp lệ đều bị coi là "dòng
đổi không mong đợi" và script tự khôi phục bản sao lưu. Đã bỏ vế đó đi.

Bài học chung: bộ tự kiểm phải kiểm **điều không được đổi**, không phải kiểm
điều được đổi. Ở đây phải đổi mới đúng.

---

## Chưa làm / hướng tiếp

1. Chưa đọc được **định dạng bên trong `.peak`** (header, số cột, cách scale).
   `StMedia::AudioImageColumnHandler` (`0x062F6B80`) và vtable của `AudioImageFile`
   (`0x145FFADC0`) là chỗ đáng vào. Trên máy này không có file `.peak` nào để đối
   chiếu — cần một project Cubase thật.
2. Chưa truy được **file `.peak` nằm ở đâu**: cùng thư mục với file WAV, hay thư
   mục project. Bị chặn ở bẫy 2 (bảng đăng ký nằm trong BSS).
3. Chưa xác minh đối tượng 0x70 byte là `MAudioCollector::FlatSliceIterator`.
4. Chưa rõ hằng `3.0` trong `0x141E9D4C0` chặn cái gì.
5. Chỗ đọc pref `Show Waveforms` / `Wave Brightness` / `Wave Outline Intensity`
   lúc vẽ — mỗi id chỉ có **một** xref, đều trong hàm dựng trang Preferences
   `0x1EB9900..0x1EB9DE2`, nên chắc đi qua observer. Khoảng min/max đã lấy được
   ở §13.2; phần còn thiếu là **công thức** biến `brightness` / `outline` thành
   hệ số màu khi vẽ.
6. `imagegenerator.dll` trong thư mục cài đặt **không** liên quan: nó là OpenCV +
   bộ lọc ảnh (`PixelSIMD@Steinberg`, `IPL_DATA_ORDER_PIXEL`), không phải dải sóng.
