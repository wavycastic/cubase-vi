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
> `Wave Brightness`). Cơ chế đọc giá trị lúc vẽ đã được làm sáng tỏ hoàn toàn ở §1.1
> và §16: các pref này được lưu thành biến toàn cục và đối tượng `Binding::Value`,
> sau đó được lớp `PSeqEventImageScheme` nạp để dựng struct `WaveStyle` cho bộ vẽ.

---

### 1.1 Cơ chế lưu trữ và truyền giá trị Preference xuống bộ vẽ

Mỗi tuỳ chọn được quản lý qua biến toàn cục hoặc đối tượng `Binding::Value`:

| Tuỳ chọn UI | Biến nội bộ / Cơ chế | Địa chỉ VA | Nơi đọc / Sử dụng lúc vẽ |
|---|---|---|---|
| `Show Waveforms` | `byte` cờ toàn cục | `0x1475C15B9` | Khi đổi, gọi `0x1437C6100` phát sự kiện `"timeEditorInvalid"` buộc Project Window vẽ lại |
| `Interpolate Audio Waveforms` | `byte` cờ toàn cục | `0x1475C1590` | Đọc trực tiếp tại `0x141E9AD3D` (lệnh tô `0x141E9AD10`) và `0x141E9D5AE` (phóng sâu `0x141E9D4C0`) |
| `Show Hitpoints` | `byte` cờ toàn cục | `0x1475C15B8` | Dùng trong `PAudioEventImage::draw` kiểm tra cờ hiển thị hitpoint |
| `Background Color Modulation` | `byte` cờ toàn cục | `0x1476FC64D` | Đọc trong bộ scheme để điều chế màu nền |
| `Use Mouse Wheel for Event Volume` | `byte` cờ toàn cục | `0x1476FC64E` | Xử lý sự kiện chuột trên event |
| `Show Filename` | `byte` cờ toàn cục | `0x1476FA350` | Getter `0x141E2E1C0`, quyết định vẽ tên file |
| `Wave Brightness` | Đối tượng `Binding::Value` | `[0x1476E01A0 + 0x18]` | Nạp trong `PSeqEventImageScheme::buildScheme` (`0x14393CA90`) |
| `Wave Outline Intensity` | Đối tượng `Binding::Value` | `[0x1476E01A0 + 0x20]` | Nạp trong `PSeqEventImageScheme::buildScheme` (`0x14393CEB4`) |

Khi `Wave Brightness` hoặc `Wave Outline Intensity` thay đổi:
1. Setter (`0x1437A8A30` / `0x1437A8A80`) gọi `Binding::Value::setValue` (`0x14455BB40`), ghi giá trị mới vào `[obj + 0x40]` và gọi `[rax + 0x50]` để thông báo cho các observer.
2. `PSeqEventImageScheme` (vtable `0x1462F6F08`) gọi `buildScheme` (`0x14393BCC0`), đọc các màu skin (`eventBackDefault`, `eventWaveMuted`, `eventWaveAutomFill`, `eventWaveAutomLine`, `eventFrame`, v.v.), áp dụng hệ số từ `Wave Brightness` và `Wave Outline Intensity`, sau đó dựng struct `WaveStyle` (`0xB8` = 184 byte, ctor `0x141EA23D0`).
3. Trong `WaveStyle`:
   - `+0x40..+0x57`: màu/brush dải sóng chính (`+0x50` là con trỏ/giá trị 8 byte truyền vào `device->vfunc+0x80`).
   - `+0x58..+0x6F`: màu/brush dải sóng phụ (cho các chế độ hiển thị thay thế).
   - `+0x78..+0x8F`: màu/brush đường viền dải sóng (outline).
   - `+0x90`, `+0x98`: giá trị `double` tỉ lệ hiển thị.
   - `+0xB0`: cờ bitfield (`bit 0` = tô màu, `bit 3` = vẽ chấm mẫu khi phóng sâu, `bit 7` = chọn giữa kiểu vẽ 1 và 2).

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
| `[rsp+0x130]` | `framesPerPixel` — `double`. **Đơn vị của nó là "frame" của Audio Image, tức một cột peak, không phải một mẫu âm thanh** — xem §3.5 |
| `[rsp+0x140]` | con trỏ chuyển đổi miền thời gian (warp), có thể `null` |

Ngay đầu hàm log:

```
0x141E9C3B2  lea  rax, [rip+…]   ; "startPixel:%12d numPixels:%12d framesPerPixel:%8.2f"
```

Đây là chỗ **duy nhất** trong exe in ra ba đại lượng này — nếu muốn xác minh hành
vi thực tế thì đây là chỗ cài log.

### 3.2 Chuẩn bị

```
xmm10 = (double)framesPerPixel                   ; đọc từ [rsp+0x130]
xmm6 = (float)framesPerPixel                     ; cvtpd2ps rồi cvtps2pd 0x141E9C38D
xmm7 = (startPixel+numPixels) * framesPerPixel  ; vị trí cuối
nếu có converter (warp):
    nếu converter->mode() == 0x0A (VT_R8):
        bỏ qua
    ngược lại:
        dựng Variant kiểu 10 (double) rồi converter->vfunc+0x28(&variant)
    rồi gọi converter->vfunc+0x20(start) và vfunc+0x20(end)
r15d = nguồn->vfunc+0x38()                      ; SỐ KÊNH
iterator = 0x1421F3650(rcx, xmm1=start, xmm2=end, r9d=channels, fpp)
n       = iterator->vfunc+0x18()                ; SỐ BẢN GHI, uint64
xmm8    = framesPerPixel / n                    ; 0x141E9C4FC
```

`xmm7` ở `0x141E9C501` nạp hằng `1.0` (`0x145ED62F0`), ở `0x141E9C666` nạp
`0.5` (`0x145ECCF38`). Cả hai nằm trong một bảng ngưỡng dùng chung ở `0x145ED62D0`:
`1e-5`, `0.010001`, `0.050001`, `1.0`, `FLT_MAX`, `-FLT_MAX`, `0.0`.

### 3.3 Nhánh A — thu nhỏ (nội suy)

Nhánh A xảy ra khi `1.0 > framesPerPixel / n`, tức **một pixel che được nhiều hơn
một bản ghi**. Với file `.peak` (256 mẫu/cột) điều này tức mức phóng dưới
**256 mẫu mỗi pixel** — chi tiết ở §3.5.

> Tên "phóng to" ở đây dễ gây nhầm: nhánh A phục vụ **thu nhỏ** (một pixel che nhiều
> bản ghi) và nội suy để vẽ mượt. Tôi đổi tên để tránh hiểu ngược.

Với mỗi cột:

```
t = (pixel * framesPerPixel) / n                 ; 0x141E9C542
i = (int)t                                       ; cvttsd2si 0x141E9C54E
f = t - i                                        ; subsd     0x141E9C560
v0 = iterator->vfunc+0x20(i * channels, &out)     ; 0x141E9C597 -> (a0, b0)
v1 = iterator->vfunc+0x20((i+1)*channels, &out)   ; 0x141E9C5B1 -> (a1, b1)
nếu lần hai trả false → dùng luôn (a0, b0)         ; 0x141E9C5C2
kết quả = lerp:  a = a0*(1-f) + a1*f ,  b = b0*(1-f) + b1*f   ; 0x141E9C5E4
ghi 8 byte ra con trỏ ra; con trỏ += 8              ; 0x141E9C629 / 0x141E9C62D
```

Chính là **nội suy tuyến tính riêng cho min và max**, theo phần thập phân của vị
trí bản ghi. Đây là cơ chế phía sau tuỳ chọn *Interpolate Audio Waveforms*.

Hai chi tiết đáng ghi:

- Vế phải của phép lerp là `1.0 - f`, và `1.0` nạp từ `0x145ED62F0` (`0x141E9C5E4`).
  Nên khi `f` hơi âm do sai số `double` thì `1.0 - f > 1` vẫn đúng — nhánh này an
  toàn với `f` âm.
- `a0, b0` được đọc vào `xmm1, xmm2` dạng **float32** (`movss` rồi `cvtps2pd`),
  nhưng phép lerp làm ở **double** rồi mới `cvtpd2ps` ghi lại. Vậy bản ghi `.peak`
  là float32, phép nội suy là double — khớp với §15.2.

### 3.4 Nhánh B — phóng to (gom min/max nhiều bản ghi)

Điều kiện ngược: `1.0 <= framesPerPixel / n` → **một bản ghi che được nhiều hơn
một pixel**, nên phải gom min/max của cả khoảng bản ghi cho từng pixel.

```
y0 = floor((pixel * fpp) / n)                         ; 0x141E9C65D..0x141E9C67F
last = (int)(obj[0x30]/channels * obj[0x38] / n) * channels - 1
với mỗi cột:
    y1 = floor(((pixel+1) * fpp) / n)                 ; 0x141E9C6E1..0x141E9C6FD
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

**Đính chính (đọc lại mã, lượt trước sai):** tôi đã ghi làm tròn kiểu *round half
away from zero*. Mã thật ở `0x141E9C66E` là:

```
0x141E9C66E  comisd  xmm8(0.0), xmm6
0x141E9C673  jbe    +   ->  addsd xmm6, 0.5     ; x <= 0
0x141E9C675  subsd  xmm6, 0.5                  ; x >  0   <-- dấu bị đảo so với doc cũ
0x141E9C67F  cvttsd2si edx, xmm6
```

Với `x >= 0` (chỉ số cột luôn không âm) thì `trunc(x - 0.5)` **chính là `floor(x)`**.
Nên phép ánh xạ là **floor**, không phải làm tròn. Hệ quả thực tế: cột pixel thứ
`p` lấy bản ghi `floor(p·fpp/n)`, lệch về bên trái, không lệch về gần giữa.

Về `last`: công thức đọc từ mã cho ra `n - 1` **với điều kiện `obj[0x30]·obj[0x38]
= n²`** — tức nó là chỉ số bản ghi hợp lệ cuối cùng, dùng để chặn đọc quá độ dài
mảng. Tôi chưa xác định được `+0x30` và `+0x38` là gì, nhưng tích của chúng bằng `n²`
thì công thức cho kết quả đúng; đây là điều kiện cần giữ khi đọc tiếp.

### 3.5 `framesPerPixel` tính bằng **cột peak**, không phải bằng mẫu âm thanh

Đọc lại `0x141E9C4C9`–`0x141E9C4FC` làm rõ đơn vị. Ở đây tôi đã hiểu sai từ trước:

```
0x141E9C4C9  mov  rax, [rax]              ; vtable của đối tượng Audio Image
0x141E9C4CF  call [rax + 0x18]            ; -> n, trả về trong RAX
0x141E9C4D5  xorps xmm9, xmm9
0x141E9C4D9  test rax, rax
0x141E9C4DC  js   0x141e9c4e5             ; âm -> nhánh chuyển đổi
0x141E9C4DE  cvtsi2sd xmm9, rax           ; không âm
0x141E9C4E5  shr  rax, 1                  ; idiom chuyển uint64 ->
0x141E9C4E8  and  ecx, 1                  ;   double của MSVC, không
0x141E9C4EB  or   rax, rcx                ;   mất chính xác
0x141E9C4F3  addsd xmm9, xmm9
0x141E9C4F8  movaps xmm8, xmm10           ; xmm10 = framesPerPixel
0x141E9C4FC  divsd  xmm8, xmm9            ; xmm8 = fpp / n
```

Ba điều, tất cả từ mã:

**1. `n` là SỐ BẢN GHI, không phải "số frame trong lát"** như tôi đã ghi ở §3.2.
Cơ sở: `vfunc+0x18` (`0x1421F4C00`, §3.6) đọc `[rcx+0x30]->+0x38` và so sánh với
chỉ số bản ghi trong `vfunc+0x20` (`0x1421F4C49  cmp rdx, r12`). Cùng một đại lượng
ở cả hai hàm. Tôi cũng đoán "uint64" từ idiom `shr/and/or/addsd`; điều đó **không
đủ căn cứ** vì hàm trả về `dword` — xem §3.6.

**2. Mẫu số của mọi phép ánh xạ pixel→bản ghi là `n`, tức số bản ghi.** Nên
`framesPerPixel` mà hàm nhận cũng tính bằng **cột peak**. Nếu nó là mẫu âm thanh
thì `(pixel·fpp)/n` không ra chỉ số bản ghi.

**3. Hệ quả trực tiếp với `.peak`:** một cột peak đại diện **256 mẫu âm thanh**
(§15.4). Khi phóng vào mức **1 pixel < 256 mẫu**, hàm này vẽ dữ liệu đã lấy mẫu
theo 256 rồi nội suy tuyến tính — **không phải dạng sóng thật**. Dạng sóng thật
chỉ xuất hiện ở `fpp < 1.0` (§4, `0x141E9D4C0`).

Nói cách khác: **điểm bão hòa thị giác của Cubase là 256 mẫu mỗi pixel.** Muốn vẽ
đẹp hơn ở mức phóng lớn thì phải tự đọc file âm thanh, không dựa vào `.peak`.

### 3.6 Ba hàm vfunc của AudioImage đã đọc được — và `0x100` hardcode

Vtable **interface** 6 slot của `AudioImageFile` là `0x145FFAE30`
(`AudioImageCache` là `0x145FFACA0`). `0x1421F3650` chính là hàm chọn: nó gán
`0x145FFAC30` rồi `0x145FFACA0` vào `[rdi]` (`0x1421F36FF` / `0x1421F3709`) khi
trả về cache, và các hằng tương ứng khi trả về file — khớp với sơ đồ vtable ở §14.

Lưu ý: 6 slot này nằm ở vtable thứ ba (`0x145FFAE30`), **không** phải vtable chính
`0x145FFADC0`. Vtable chính 14 slot có `+0x18 = 0x141973B50` và
`+0x28 = 0x1421F67C0` — hàm dtor, không phải đọc dữ liệu. Đó là lý do §3.3/§3.4 gọi
`[rax+0x18]` trên con trỏ trả về từ `0x1421F3650` mà vẫn đúng: nó là con trỏ
**interface**, không phải con trỏ đối tượng.

Ba slot mà `0x141E9C340` dùng, đọc trực tiếp từ mã:

| slot | hàm | việc |
|---|---|---|
| `+0x18` | `0x1421F4C00` | **số bản ghi** |
| `+0x20` | `0x1421F4C20` | đọc **một** bản ghi `(a, b)` |
| `+0x28` | `0x1421F4E30` | đọc **một khoảng** → `(min, max)` |

`+0x18` chỉ dài 5 lệnh và **chứa hằng `0x100` = 256**:

```
0x1421F4C00  mov  rax, qword ptr [rcx + 0x30]   ; con trỏ tới lớp nền
0x1421F4C04  test rax, rax
0x1421F4C07  je   0x1421F4C0D                    ; chưa nạp -> dùng hằng
0x1421F4C09  mov  eax, dword ptr [rax + 0x38]    ; số bản ghi thật
0x1421F4C0C  ret
0x1421F4C0D  mov  eax, 0x100                     ; <-- 256
0x1421F4C12  ret
```

### 3.7 Đã tìm thấy mã **ghi** header `.peak` — mọi trường đã đặt tên được

Hàm `0x1421F1600` ghi header, và nó **xác nhận từng trường** bằng nguồn ghi, không
phải bằng suy luận:

```
0x1421F16C8  ; vong copy ten file nguon vao [rdi + 0x20] byte tuong byte,
             ;   dung den byte 0  -> chuoi NUL ket thuc
0x1421F16DF  mov dword ptr [rdi + 0x1C], 0        ; +0x1C = 0 luc GHI
0x1421F17C2  mov rax, [rsi + 0x10]
0x1421F17CA  call [rax + 0x48]                   ; so luong mau
0x1421F17CD  mov edx, 0x7FFFFFFF
0x1421F17D2  cmp rax, rdx                         ; clam o 2^31-1
0x1421F17D5  cmovl edx, eax
0x1421F17D8  mov [rdi + 0x10], edx                ; +0x10 = TONG SO FRAME
0x1421F17E3  call [rax + 0x38]                   ; so kenh
0x1421F17E6  mov [rdi + 0x0C], eax                ; +0x0C = SO KENH
0x1421F17E9  mov dword ptr [rdi + 0x14], 0x100    ; +0x14 = 256, HARDCODE
```

Bốn kết luận, tất cả từ mã ghi:

**1. `+0x10` là tổng số frame** — lấy từ `vfunc+0x48` của đối tượng nguồn, có
clamp ở `0x7FFFFFFF`. Đúng như tôi đo từ header 19 file (§15.4), nay đã xác nhận
từ phía ghi.

**2. `+0x0C` là số kênh** — từ `vfunc+0x38`. Đúng với giá trị `2` mọi file.

**3. `+0x14` = 256 là hằng ghi cứng**, không phải số đo. Đây là câu trả lời dứt
điểm cho mục "chưa đặt tên được" ở §15.7: **`0x100` là frames-per-column do phía
ghi quyết định**, và nó trùng với giá trị mọi file thật.

**4. `+0x1C` là HASH của một chuỗi đường dẫn, không phải checksum dữ liệu.** Trong
toàn bộ vùng mã `aimage` chỉ có **hai** chỗ ghi vào `+0x1C`, và cả hai đều không
liên quan tới dữ liệu:

```
0x1421F16DF  mov dword ptr [rdi + 0x1C], 0            ; nhanh: chua co gi
...
0x1421F17AD  mov rcx, rax
0x1421F17B0  call 0x1421F66E0                          ; ham hash
0x1421F17B6  mov dword ptr [rdi + 0x1C], eax           ; luu ket qua hash
```

`0x1421F66E0` là hàm hash chuỗi rỗng-kết-thúc trên **ký tự 16-bit** (kiểu
`wchar_t`/UTF-16), dạng djb2 biến thể, và nó **cộng dồn theo từng thành phần** ngăn
cách bởi ký tự phân cách:

```
0x1421F66EF  movzx eax, word ptr [rcx]        ; ky tu 16-bit hien tai
0x1421F66FE  movzx ecx, word ptr [rip + …]     ; KY TU PHAN CACH
0x1421F6705  cmp  ax, cx
0x1421F6708  jne  -> xu ly ky tu thuoc
0x1421F670A  add  esi, ebx                     ; gap: cong don vao tong
0x1421F670C  xor  ebx, ebx                     ;   bat dau don moi
0x1421F6713  call 0x1439CBF60                  ; bien doi ky tu (hoa thuong?)
0x1421F6722  lea  ebx, [rax + rbx*2]           ; don = kyTu + don*2
0x1421F6732  lea  eax, [rbx + esi]             ; ket qua
```

Nên `+0x1C` **không** phụ thuộc nội dung dữ liệu âm thanh, và cũng không phải hằng
định dạng. Việc 18/19 file trùng nhau có nghĩa là **18 file đó cùng dùng một chuỗi
đầu vào** — nhiều khả năng là đường dẫn thư mục, vì cả 19 file đều nằm trong
`Images\`. File `01 - Show Me` khác, nên nó nhiều khả năng được dựng từ nguồn khác
(đường dẫn audio khác, hoặc phiên Cubase khác).

Đã xác minh chuỗi băm của `+0x1C`: `0x1421F1659` gọi `vfunc+0x170` của đối tượng
đường dẫn nguồn để lấy chuỗi đường dẫn thư mục chứa file âm thanh, sau đó băm
bằng `0x1421F66E0`. Điều này giải thích hoàn hảo vì sao **18 file cùng nằm trong
thư mục `Audio\` của dự án có chung mã hash `0x8DAFEE63`**, còn file `01 - Show Me`
được import từ một thư mục khác nên mang giá trị hash khác.

Về `+0x04` và `+0x06`: đây chính là **Major Version** (`uint16_t` = 1) và
**Minor Version** (`uint16_t` = 200, tức format version 1.200). Hàm kiểm tra
tính hợp lệ của header `.peak` tại `0x1421F15B0..0x1421F15EC` kiểm tra trực tiếp:

```asm
0x1421F15BA  cmp dword ptr [rdi], 0x46464950   ; 'PIFF' magic
0x1421F15C0  jne -> tu choi
0x1421F15C2  mov eax, 0xC8                     ; 200
0x1421F15C7  cmp word ptr [rdi + 6], ax        ; minor_version <= 200
0x1421F15CB  jg  -> tu choi
0x1421F15CD  cmp dword ptr [rdi + 0x0C], 0     ; channels > 0
0x1421F15D1  jle -> tu choi
0x1421F15D3  cmp dword ptr [rdi + 0x14], 0     ; frames_per_column > 0
0x1421F15D7  jle -> tu choi
0x1421F15D9  cmp word ptr [rdi + 4], 1         ; major_version == 1
0x1421F15DE  jne -> tu choi
```

Nếu một trong các điều kiện này sai, Cubase từ chối file cache và tự động tính toán,
ghi đè lại file `.peak` mới.

### 3.8 Vì sao header là big-endian: hàm `0x1421F0EF0`

Header trong RAM là little-endian; trước khi ghi, Cubase gọi `0x1421F0EF0` để đảo
byte. Hàm này **không** dùng `bswap` — nó hoán đổi từng cặp byte:

```
0x1421F0EF3  movzx edx, byte ptr [rcx + 4]
0x1421F0EF7  movzx eax, byte ptr [rcx + 5]
0x1421F0EFB  mov byte ptr [rcx + 4], al
0x1421F0F02  mov byte ptr [rcx + 5], dl
0x1421F0F05  movzx edx, byte ptr [rcx + 6]
0x1421F0F09  mov byte ptr [rcx + 6], al   ; al = byte[7]
0x1421F0F11  mov byte ptr [rcx + 7], dl
```

Nó lặp lại cho các cặp `+8/+9`, `+0xA/+0xB`, … `+0xE/+0xF`, rồi `+0x10..+0x1F`,
và **dừng ở `+0x1F`** — không đụng `+0x20` trở đi (tên file) và không đụng phần dữ
liệu. Đây chính là lý do phần dữ liệu float32 ở `+0x60` vẫn là **little-endian**
trong khi header là big-endian: hai vùng dùng hai đường ghi khác nhau.

Kiểm chéo bằng số: giá trị trong RAM `0x00C80001` (LE → byte `01 00 C8 00`), hoán
đổi từng cặp cho ra `00 01 00 C8` — **khớp đúng** 4 byte `+0x04` trong file thật.
Vậy `+0x04` là **hai số 16-bit big-endian**: `major = 0x0001` rồi `minor = 0x00C8` (= 200).

`+0x20` xác nhận bố cục xen kẽ của file `.peak` — nó chặn trên
`[rcx+0x30]->+0x30`, rồi tính địa chỉ byte:

```
0x1421F4C45  mov  rax, [rcx + 0x30]
0x1421F4C49  mov  r12d, [rax + 0x30]        ; tổng số bản ghi
0x1421F4C4D  cmp  rdx, r12                  ; index >= n -> false
0x1421F4C50  jae  -> tra false
0x1421F4C56  mov  r14d, [rcx + 0x20]
0x1421F4C5A  shr  r14d, 3                   ; <-- CHIA 8: kích thước 1 bản ghi
```

`shr 3` trên `[rcx+0x20]` là **8 byte mỗi bản ghi** — khớp §15.2. Và ở `0x1421F4CC8`
: `lea rdi, [rcx + r15*8]` với `r15` là chỉ số bản ghi — xác nhận bản ghi tính bằng
**chỉ số phẳng**, kênh xen kẽ, không có bảng tra. Tức `index*channels + kênh` là
cách duy nhất, và nó là lý do §3.3/§3.4 nhân `channels` vào mọi chỉ số.

`+0x28` nhận **5 tham số** (`rcx, rdx, r8, r9, [rsp+0x50]`), trong đó tham số đầu ra
lấy từ `[rsp+0x50]` — nên lời gọi ở §3.4 truyền 4 tham số thật (`this, start, end,
channels`) cộng con trỏ ra làm tham số thứ 5 trên xếp chồng. Nó ghi
`*(qword*)rbx = 0` trước khi quét (`0x1421F4E5F`), tức **luôn khởi tạo kết quả bằng
0** rồi mới gom min/max — đó là lý do các cột ngoài phạm vi trả về 8 byte số 0 chứ
không phải giá trị rác.

Và 3 hàm này của `AudioImageCache` (`0x1421F12F0`, `0x1421F1310`, `0x1421F1330`) đều
chỉ là **3 lệnh chuyển tiếp** — không có logic riêng:

```
0x1421F12F0  mov  rcx, [rcx + 0x10]   ; xuống lớp dưới
0x1421F12F4  add  rcx, 0x30          ; lấy vtable con
0x1421F12F8  mov  rax, [rcx]
0x1421F12FB  jmp  [rax + 0x18]       ; gọi tiếp cùng slot
```

Nghĩa là cache **không có định nghĩa riêng** cho ba thao tác này — nó ủy quyền. Đây
là cơ sở vững để chọn `AudioImageFile` làm điểm can thiệp: sửa logic thật, thay vì
sửa một lớp chuyển tiếp.

### 3.9 Vì sao có hai vòng lặp lồng nhau

Nhánh A quét `rbp` trong khoảng `1..r15d` bên trong `r12` chạy **ngược** từ
`numPixels` về 1 (`0x141E9C520` vòng trong, `0x141E9C652` vòng ngoài), con trỏ ra
tăng 8 byte mỗi lần (`0x141E9C62D`). Thứ tự ghi là **pixel tăng dần, kênh tăng
dần** — đúng thứ tự một bộ đệm `(numPixels × channels)` cần, và giải thích vì sao
§3.10 phải cấp phát `channels * (numPixels+3)` phần tử.

### 3.10 Vì sao lúc dựng phải dư 1 pixel mỗi bên

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

### 3.11 Thuật toán tính toán đỉnh (peak) từ số mẫu âm thanh thô — `0x1421F5150`

Toàn bộ quy trình sinh file `.peak` từ file âm thanh thô nằm ở `0x1421F4100` và `0x1421F5150`:

1. **Đọc số mẫu**: `0x1421F4100` cấp phát bộ đệm đọc tối đa **16.384 mẫu** mỗi lần (`0x1421F4360  mov r12d, 0x4000`), sau đó gọi reader đọc lát âm thanh.
2. **Quét tìm đỉnh 2 nửa chu kỳ**: trong `0x1421F5150`:
   ```asm
   0x1421F52E0  movss   xmm0, dword ptr [r12]       ; mẫu âm thanh (float32)
   0x1421F52F2  comiss  xmm0, xmm7                  ; so sánh với 0.0f
   0x1421F52F5  jbe     -> nhánh âm
   ; Nhánh dương:
   0x1421F52F7  comiss  xmm0, dword ptr [rcx + rax*8] ; so với max dương hiện tại
   0x1421F52FD  movss   dword ptr [rcx + rax*8], xmm0 ; pos_max = max(pos_max, sample)
   ...
   ; Nhánh âm:
   0x1421F5313  mulss   xmm0, xmm6                  ; xmm6 = -1.0f (lấy độ lớn tuyệt đối)
   0x1421F5317  comiss  xmm0, dword ptr [rcx + rax*8 + 4] ; so với max âm hiện tại
   0x1421F531E  movss   dword ptr [rcx + rax*8 + 4], xmm0 ; neg_max = max(neg_max, -sample)
   ```
3. **Ghi theo cột 256 mẫu**:
   - Cứ sau đúng 256 mẫu (`0x100`) trên mỗi kênh, hàm gọi `0x1421F53B1` ghi 8 byte `(pos_max, neg_max)` vào file `.peak` tại toạ độ `0x60 + index * 8`.
   - Sau đó reset cặp giá trị về 0 (`0x1421F53C1  mov qword ptr [rax + r14*8], 0`).
4. **Kiểm tra độ dài cuối file**:
   Tại `0x1421F5710..0x1421F5726`, Cubase tính công thức:
   ```asm
   total_records = channels * ceil(total_frames / 256)
   ```
   Nếu kích thước file trên đĩa khớp đúng số bản ghi này thì quá trình tạo peak hoàn tất thành công.

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
xmm9 = min(pixels_per_sample * 0.5, 3.0)        ; 0x141E9DA97, hằng tại 0x145EDFB60
```

Hằng `3.0` ở `0x145EDFB60` là **bán kính tối đa (pixel) của các chấm điểm mẫu**
(sample points / sample dots) hiển thị trên dải sóng:
- Khi phóng to cực sâu (`framesPerPixel < 1.0` hay `pixels_per_sample > 1.0`), Cubase
  vẽ các chấm tròn nhỏ tại mỗi toạ độ điểm mẫu bằng hàm biến đổi `0x141EA5E00`.
- Bán kính chấm tỉ lệ thuận với mức phóng: `pixels_per_sample * 0.5`, nhưng bị chặn trần
  ở **3.0 pixel** (tương đương đường kính hạt tối đa 6.0 pixel).
- Nếu `bit 3` của cờ style tắt (`style->0xB0 & 8 == 0`), bán kính được ép về `0.0`
  (chỉ vẽ đường nối giữa các mẫu, không vẽ chấm).

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

> **Đã sửa ở §14** (vòng RE thứ hai): đối tượng 0x70 byte **không phải**
> `MAudioCollector::FlatSliceIterator` mà là **`AudioImageFile`** — tức là chính
> **file `.peak`**, không phải file âm thanh. Vtable `0x145FFADC0` có
> `isKindOf("AudioImageAccessor")`; xem §14.1 và §14.3.

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
| `ptr.py` | đọc con trỏ tại một VA và ghi chú từng con trỏ trỏ vào đâu: nằm trong `.pdata` không, chuỗi gì, hay header PE. Đây là công cụ đi từ "tên lớp" tới "danh sách hàm". Cần `--va` khi đưa vào một file offset đã ghi trong tài liệu này (bẫy 6) |
| `deobf_str.py` | giải mã chuỗi Steinberg bị obfuscate bằng LCG (`state * 0xBC8F`) |
| `deobf_scan.py` | dò theo **hình dạng** để giải mã hàng loạt chuỗi obfuscate, không cần gõ seed/key. Quét cả `.text` ra 281 chuỗi ở 36 file nguồn — xem §14.7. Lọc theo "chữ in được" nên con số là **cận dưới**: chuỗi quá ngắn hoặc không phải ASCII đều bị bỏ |
| `tools\peak_read.py` | đọc file `.peak` thật: in header, kiểm tra công thức `records == channels × ceil(frames/256)`, và vẽ lại dải sóng ra PNG/ASCII. `--check` quét cả thư mục. Xem §15 |

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
6. **Vị trí chuỗi trong tài liệu này là *file offset*, không phải VA.** Vtable thì
   phải tra bằng VA. `PE.resolve` ưu tiên file offset nên đưa VA vào là đọc
   nhầm byte tại offset đó — `ptr.py` đã có `--va` (giống `disasm2.py`).
7. **Tên lớp dài hơn 15 byte thì vtable không còn ở `+0x10`.** Quy tắc "tên rồi
   vtable" chỉ đúng với tên ≤ 15 byte: `StMedia::AudioImageColumnHandler` dài 33
   byte, vtable lệch `+0x28`, và bản ở `+0x10` thuộc lớp cha. Phải **đếm chứng rồi
   mới cộng**, và kiểm bằng `getClassName` (hàm 7 byte trả về tên) cho khỏi phải
   đoán.
8. **Capstone xếp operand theo thứ tự nguồn, không theo operand `mov` của
   Intel.** `movdqa xmm0, [rip+X]` ra `[reg, mem]` còn `movdqa [rbp+d], xmm0` ra
   `[mem, reg]` — cùng mnemonic, hai chiều ngược nhau. Bộ lọc "operand 0 là
   memory" sẽ bỏ sót một nửa site nếu viết theo cảm tính.
9. **Chuỗi `PEAK` trong exe là của `PEAK_LEVEL`, không phải chữ ký file `.peak`.**
   Quét `PEAK` ra `0x05FF95E2`, ngay cạnh `BEXT/BWF_MAX_TRUE_PEAK_LEVEL` — đó là
   chunk BWF. Chữ ký `.peak` chỉ nằm trong lệnh đăng ký loại file, dưới dạng
   immediate `0x5045414B`.

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

## 14. Vòng RE thứ hai: hai lớp đọc dữ liệu, và `.peak` đọc thế nào

Vòng trước dừng ở "0x70 byte là gì?". Vòng này trả lời được câu đó, và đọc
được khoảng một nửa định dạng `.peak`.

### 14.1 Quy tắc "tên lớp → vtable", và bốn lớp trong khối AudioImage

Trong khối `.rdata` của AudioImage, bố cục lặp lại đúng hoàn toàn:

```
<chuỗi tên lớp + NUL> + padding tới 8 byte  →  vtable chính   (14 slot, 0x70 byte)
                                             →  vtable giao diện (6 slot, 0x30 byte)
```

Bốn lớp, toạ độ là **VA** (cột offset ở §2 là file offset — loại khác, xem bẫy 6
ở §12):

| lớp | tên (VA) | vtable chính | vtable giao diện 6 slot |
|---|---|---|---|
| `AudioImageCache` | `0x145FFAC20` | `0x145FFAC30` | `0x145FFACA0` |
| `AudioImageCacheAccessor` | `0x145FFACD0` | `0x145FFACE0` | `0x145FFAD50` |
| `AudioImageFile` | `0x145FFADB0` | `0x145FFADC0` | `0x145FFAE30` |
| `AudioImageAccessor` | `0x145FFAE60` | `0x145FFAE70` | — |

Cách kiểm chứng không phải đoán: `+0x30` của vtable chính là một hàm 7 byte
trả về **tên của vtable giao diện**, và `+0x38` là `isKindOf` với đúng tên đó.

```
0x1421F67B0  lea rax, ["AudioImageAccessor"]        ; AudioImageFile   -> +0x30
0x1421F67F0  lea rax, ["AudioImageCacheAccessor"]  ; AudioImageCache  -> +0x30
0x1421F6850  isKindOf("AudioImageAccessor")         ; AudioImageFile   -> +0x38
0x1421F6990  isKindOf("AudioImageAccessor")         ; AudioImageCache  -> +0x38
```

Hệ quả trực tiếp: **đối tượng 0x70 byte là `AudioImageFile`** — ctor `0x1421F4EE0`
gán vtable `0x145FFADC0`, và destructor `0x1421F6120` gọi `free` với đúng `0x70`.
Giả định cũ (`MAudioCollector::FlatSliceIterator`) **sai**.

### 14.2 Giao diện 6 slot — chính là "iterator" mà §3 dùng

Cả hai lớp cài cùng một bộ 6 hàm qua vtable thứ hai:

| slot | ý nghĩa | `AudioImageFile` | `AudioImageCache` |
|---|---|---|---|
| `+0x18` | số bản ghi trong lát | `0x1421F4C00` | `0x1421F12F0` (thunk) |
| `+0x20` | lấy 1 cặp, trả bool | `0x1421F4C20` | `0x1421F1310` (thunk) |
| `+0x28` | lấy cả khoảng | `0x1421F4E30` | `0x1421F1330` (thunk) |

Ba thunk của `AudioImageCache` chỉ là `mov rcx,[rcx+0x10]; add rcx,0x30;
jmp [vtable+N]` — tức **đẩy việc cho `AudioImageCacheAccessor`**, khung 0x28 byte
không tự tính gì.

> Đối tượng trả về là **con trỏ tới sub-object thứ hai** (`đối tượng + 0x10`), nên
> mọi lệnh đọc phải dùng `obj + 0x10` làm `this`. Dùng `obj` là lệch 0x10 byte:
> đọc vtable ở chỗ con trỏ buffer và hiểu nhầm mọi thứ sau đó.

### 14.3 Bố cục `AudioImageFile` (0x70 byte)

| offset | vai trò (suy từ cách dùng, tên trường là suy đoán) |
|---|---|
| `+0x00` | vptr `AudioImageFile`; `+0x08` = 1 (mã loại) |
| `+0x10` | vptr `AudioImageAccessor` — **con trỏ được trả về** |
| `+0x18` | con trỏ buffer đang giữ |
| `+0x20..+0x3F` | handle 32 byte, đăng ký vào pool `0x14770BEF0` với `r8d = 0x8000` |
| `+0x40` | ảnh: `+0x28` = offset byte đầu dữ liệu, `+0x30` = số bản ghi |
| `+0x48` | nguồn byte: sub-object `+0x10`, `vfunc+0x18` = seek, `vfunc+0x08` = đọc |
| `+0x50` | thành phần thứ ba (addRef, sub-object `+0x10`) |
| `+0x58` | byte cờ: cửa sổ trong bộ nhớ có hợp lệ không |
| `+0x60`, `+0x68` | chỉ số bản ghi đầu / cuối của cửa sổ đang giữ |

Ctor (`0x1421F4EE0`) nhận 3 tham chiếu và gọi `vfunc+8` (addRef) trên cả ba;
`0x1421F3650` và `0x1421F33F0` đều truyền vào từ `[ảnh + 0x48]`.

### 14.4 Bản ghi trong `.peak`: 8 byte, hai số thực **không âm**

`AudioImageFile::getPair` (`0x1421F4C20`, 516 byte) cho biết cách đọc:

```
index >= [ảnh + 0x30]                      -> trả false
seek( [ảnh + 0x28] + index * 8 )           -> vfunc+0x18 trên sub +0x10
đọc ( (len & ~15) * 8 + 0x80 ) byte        -> vfunc+0x08, vào [obj + 0x18]
```

Ba điều đáng ghi:

1. **Bản ghi = 8 byte = 2 × float32.** Chỉ số nhân với 8, đọc cả khối, không có
   bước giải mã nào — nên đây **không phải** số mẫu thô của file WAV.
2. **Có 128 byte dự phòng** và làm tròn xuống bội số **16 bản ghi**
   (`and eax, 0xFFFFFFF0` rồi `*8 + 0x80`).
3. Khi lệch khỏi cửa sổ, nó **căn chỉnh xuống**: `r15 = (index / bytesĐọcĐược) *
   bytesĐọcĐược`, rồi seek tới `offset + r15*8` — nghĩa là nó đọc theo **đơn vị
   cửa sổ**, không đọc lẻ từng bản ghi.

`getRange` (`0x1421F4E30`) gộp nhiều bản ghi, và đây là điểm sửa một hiểu lầm ở
§3.4:

```
[out] = 0
mỗi bản ghi, index += stride:
    out.f0 = max(out.f0, rec.f0)
    out.f1 = max(out.f1, rec.f1)
```

**Hai phép lấy MAX, khởi điểm 0** — không phải min/max. Nếu bản ghi chứa
`(min, max)` như §3.4 giả định thì một tín hiệu toàn âm sẽ ra đúng 0, mất hết đỉnh
dưới. Suy ra mỗi bản ghi là **hai số không âm**: đỉnh trên và độ lớn đỉnh dưới.
Đó cũng là cách nhiều định dạng peak lưu, và giải thích vì sao phép gộp là max.

Vì `stride` = số kênh và chỉ số chạy `y0*channels + kênh` (§3.4), bố cục là:

```
mỗi cột:  lặp kênh:  8 byte = (float32 đỉnh trên, float32 |đỉnh dưới|)
```

Tức **xen kẽ theo kênh**, không phải kênh nằm cạnh nhau. Muốn chốt chắc còn cần
một file `.peak` thật — xem mục *Chưa làm*.

### 14.5 Ngưỡng 8192 nghĩa là gì, và nhánh phóng sâu đọc bằng gì

`0x1421F3650` chỉ có **một** caller: `0x141E9C4B0`, nằm trong hàm dựng cột
`0x141E9C340`. Nhánh `framesPerPixel < 1.0` gọi `0x141E9D4C0` (vẽ bằng số mẫu
thật) **không đi qua đây** — nó dùng đối tượng đọc khác, chưa định danh được.
`MAudioCollector::FlatSliceIterator` vẫn là ứng viên hợp lý cho *nhánh đó*, và
không phải cho đối tượng 0x70 byte.

Vậy ngưỡng 8192 là **giới hạn của cache RAM**, không phải độ phân giải file:

| mức phóng | đối tượng đọc | nguồn |
|---|---|---|
| `fpp < 1` | chưa rõ | số mẫu thật |
| `1 ≤ fpp < 8192` | `AudioImageFile` (0x70) | cột trong file `.peak` |
| `fpp ≥ 8192` | `AudioImageCache` (0x28) | cache trong RAM |

> **Đính chính (đo được từ file thật, §15.4):** độ phân giải của file `.peak` là
> **256 frame/cột/kênh**, không phải 8192. 8192 là ngưỡng do
> `cacheAccessor->vfunc+0x18()` báo — tức mức mà cache trong RAM phục vụ được. Nên
> khi thu nhỏ mạnh, một pixel có thể gộp **32 cột `.peak`**.

### 14.6 File `.peak` nằm ở đâu — đã rõ cơ chế, còn thiếu tên file

Chuỗi `peak` (UTF-16, `0x145FFA9F8`) và `com.steinberg.peakfile` (`0x145FFA980`)
chỉ có **một** chỗ dùng: đăng ký loại file `0x14161AF40`. Bảng đăng ký nằm ở
`.data` tại `0x14770BE30` và có đúng **hai** tham chiếu: chỗ đăng ký, và
`0x1421F1F59`.

Nơi thứ hai nằm trong hàm `0x1421F1DD0`, và cho thấy cơ chế dựng tên:

```
0x1421F1EE5  lea rdx, [L"%02d"]              ; 0x145F7EA28
0x1421F1EF0  format([rbp-0x20], L"%02d", abs(n))     ; n từ 0x1421F66E0 / 0x1421F6540
0x1421F1F03  nối chuỗi đó vào tên sẵn có ([rbp-0x50])
0x1421F1F17  new 0xE8 byte                    ; đối tượng tài liệu
0x1421F1F4E  khởi tạo(..., tên, ...)          ; 0x1445caa20
0x1421F1F63  vfunc+0xF0(0x14770BE30)          ; gắn vào bảng loại file .peak
0x1421F1F71  vfunc+0xF8(0)
0x1421F1F7F  vfunc+0x188(0)
0x1421F1F8B  vfunc+0xD0(0)
```

Nghĩa là: **tên file `.peak` không có trong exe dưới dạng chuỗi.** Nó được ghép
lúc chạy từ tên sẵn có (lấy từ đường dẫn file WAV, qua `FNPath` ở `0x1421F1E1B`)
cộng thêm một số `%02d`, rồi đuôi lấy từ bảng loại file. Chuỗi `L"%02d"` cho thấy
tên có **hậu tố đánh số 2 chữ số** — nhiều khả năng dùng để tách ảnh khi file
dài. Chưa truy được con số đó là số kênh, số phần hay số thứ tự.

Trước đây mục này bị chặn ở bẫy 2 (§12) vì bảng đăng ký nằm trong `.data`.
Không còn bị chặn: `xref.py --va` xem được, chỉ là mất hơn một phút.

### 14.7 Công cụ mới: giải mã tự động chuỗi obfuscate

`deobf_str.py` cần người dùng tự gõ seed + key + độ dài. Site giải mã trong exe
có hình dạng cố định, nên `tools/research/deobf_scan.py` dò theo hình dạng:

- chỉ `mov ecx, imm32` mới mở đầu một site (opcode `B9`, một byte) — lọc trước;
- key = mọi lệnh ghi xuống `[rbp/rsp + disp]`, **sắp theo độ lệch**; lệnh spill
  seed dùng opcode `89` nên không bao giờ lẫn vào key (key dùng `c7` / `c6` /
  `66 0f 7f`);
- độ dài = khoảng các lệnh ghi phủ, và trùng khớp `mov r9d, imm32` ở mọi site đã
  xem;
- **chỉ báo cáo khi giải mã ra chữ in được** — nên quét cả section mà không
  phải lọc tay: site thật ra chữ, site đọc lệch thì ra rác.

Quét toàn `.text` + `IPPCODE` (`0x140001000..0x145C32600`): **281 chuỗi**, ở
**36 file nguồn** khác nhau — toàn bộ là đường dẫn `__FILE__` trong macro
assert/log:

```
D:\T1\work\40ff4699062de924\lego\source\audiofile\aimage.cpp
D:\T1\work\40ff4699062de924\lego\source\project\parrange.cpp
D:\T1\work\40ff4699062de924\lib.frame-gui\source\geditor.cpp
D:\T1\work\40ff4699062de924\lib.frame-io\source\ffilesys.cpp
D:\T1\work\40ff4699062de924\skinedit\source\program\pnodeattribs.cpp
```

Hai kết quả đáng dùng:

1. **Trong toàn bộ exe không có chuỗi obfuscate nào chứa `peak` / `image` /
   `wave` / `column`** (trừ đúng hai bản `aimage.cpp`). Cùng với §14.6, điều này
   khẳng định tên file `.peak` **không** nằm trong exe dưới bất kỳ dạng nào.
2. Cây nguồn nội bộ lộ ra tên dự án `lego` và các thư viện `lib.frame-gui`,
   `lib.frame-io`, `skinedit` — hữu ích khi cần đoán tên biến.

Con số 3.965 ghi ở §6.1 là số chỗ có **thuật toán** (đếm `imul … 0xBC8F`), phần
lớn không phải chuỗi — 281 là số chuỗi thật sự giải mã được, và là **cận dưới**,
vì bộ lọc bỏ cả chuỗi quá ngắn lẫn chuỗi không phải ASCII.

### 14.8 Phụ lục: `StMedia::AudioImageColumnHandler`

Lớp phía StMedia phụ trách đọc/ghi phần cột. Chuỗi tên ở file offset `0x62F6B80`
(VA `0x1462F8780`) dài **33 byte**, nên vtable của nó không nằm ở `+0x10` như
các lớp trên — xem bẫy 6.

| | |
|---|---|
| tên (VA) | `0x1462F8780` — `StMedia::AudioImageColumnHandler` |
| vtable **của chính nó** | `0x1462F8618` |
| `getClassName` | `0x14394ADB0` (trả về đúng tên trên) |
| `isKindOf` | `0x14394B0F0` (so với `StMedia::AttributeHandler`, `CmObject`, `FObject`) |
| lớp cha | `StMedia::MarkerListAttributeHandler` — vtable `0x1462F87A8` |

Cách tìm vtable đúng mà không phải đoán: `isKindOf` ghi đè của lớp con xuất hiện
trong `.rdata` **đúng một lần** (VA `0x1462F8650`), nên vtable phải bắt đầu tại
`0x1462F8650 - 0x38`. Ngược lại, `isKindOf` của lớp cha cũng chỉ xuất hiện một
lần, ở `0x1462F87E0` — tách được hai vtable mà không cần đoán.

Nghĩa là `.peak` là một file **thuộc khung attribute của StMedia** (cùng khung với
`StdAttributeHandler`, `MediaListDefaults`), và phần cột là một attribute đọc/gộp
qua các handler đó. Đó là lý do cấu trúc bên trong không giống WAV.

---

## 15. Định dạng `.peak` — đã mổ được từ file thật

Có dự án thật trên máy: `D:\01_Music_Projects\Cubase\demo1.cpr`, kèm **19 file
`.peak`**. Đọc được header, và kết quả **sửa hai điều đoán ở vòng trước**.

### 15.1 Chữ ký là `PIFF`, không phải `PEAK`

```
0000  50 49 46 46 00 01 00 C8  00 00 00 60  00 00 00 02   PIFF.......`....
0010  00 68 CE F6 00 00 01 00  FF FF FF FF  8D AF EE 63   .h.............c
0020  30 32 2E 20 42 6F 64 79  2E 66 6C 61 63 00 00 00   02. Body.flac...
```

Đối chiếu: `+0x08` bằng `96` ở **cả 19 file**, và `(len(file) - 96)` **chia hết
cho 8** ở cả 19 file. Nên `+0x08` là **kích thước header**, và dữ liệu bắt đầu ở
`0x60` — khớp với `[ảnh + 0x28] = 0x60` mà `AudioImageFile` đọc ở §14.4.

Nên chữ ký thật là **`PIFF`** (viết tắt "Packed Image File Format" của
Steinberg). Hằng `0x5045414B = 'PEAK'` ở §6.1 chỉ là tham số **signature** trong
lệnh đăng ký loại file `0x14161AF40` — dùng để Cubase nhận ra file khi duyệt, còn
4 byte đầu trên đĩa là `PIFF`. Đây là bẫy kiểu "tên hiển thị khác chữ ký thật", và
nếu không có file thật thì rất dễ đoán sai (vòng trước đã đoán sai).

### 15.2 Bản ghi dữ liệu: 2 × float32 **little-endian**, không âm

Đo trên toàn bộ 53.662 bản ghi của một file:

| kiểm tra | kết quả |
|---|---|
| big-endian float32 | ra `0.000000` mọi chỗ → **sai** |
| little-endian float32 | ra giá trị 0..1 hợp lý → **đúng** |
| tỉ lệ bản ghi có cả hai số ≥ 0 | **30000/30000 = 100%** |
| khoảng giá trị toàn file | `min = 0.0`, `max = 1.0` |

```
+60  00 40 14 3E  00 F0 37 3E     ->  0.144775  0.179626
+68  00 E0 C7 3D  00 10 FA 3D     ->  0.097595  0.122101
...
[26831]                              0.884888  0.644897
[53661] (cuoi)                      0.000153  0.000183
```

**Xác nhận dự đoán ở §14.4**: hai số **không âm**, không phải `(min, max)` có dấu.
Và việc `getRange` gộp bằng **max** (`0x141E9D010` → `0x141E9F4E30`) chỉ đúng
với dữ liệu không âm. Bản ghi là `(đỉnh trên, |đỉnh dưới|)` — hai số đo độ lớn
biên độ, chuẩn hoá 0..1.

Cũng khớp với `movss` / `comiss` trong mã: cả hai đều là **float**, không phải
int. Và không có bản ghi `(0,0)` nào trong file (0%), nên cột rỗng được đánh dấu
bằng giá trị riêng — khớp với hằng `-0.0f` (`0x145FA4E40`) mà §3.4 nêu.

### 15.3 Header 96 byte — trường nào đã biết, trường nào chưa

| offset | kiểu | đọc được | ghi chú |
|---|---|---|---|
| `+0x00` | char[4] | `PIFF` | chữ ký thật trên đĩa |
| `+0x04` | BE u16 | `1` ở cả 19 file | **major_version** = 1 (mã kiểm tra `== 1`) ✓ |
| `+0x06` | BE u16 | `200` ở cả 19 file | **minor_version** = 200 (mã kiểm tra `≤ 200`, format PIFF v1.200) ✓ |
| `+0x08` | BE u32 | `96` ở cả 19 file | **kích thước header** ✓ |
| `+0x0C` | BE u32 | `2` ở cả 19 file | **số kênh** ✓ — xác nhận từ mã ghi `vfunc+0x38` |
| `+0x10` | BE u32 | đổi ở cả 19 file | **tổng số frame** ✓ — xác nhận từ mã ghi `vfunc+0x48`, clamp `0x7FFFFFFF` |
| `+0x14` | BE u32 | `256` ở cả 19 file | **frames mỗi cột** ✓ — mã ghi **hardcode `0x100`** |
| `+0x18` | BE u32 | `0xFFFFFFFF` ở cả 19 file | sentinel −1 |
| `+0x1C` | BE u32 | hằng ở 18/19 file | **hash đường dẫn thư mục nguồn** từ `0x1421F66E0` (§3.7) ✓ |
| `+0x20` | char[] | `"02. Body.flac"` | **tên file nguồn**, đuôi `.flac` |
| `+0x60` | — | dữ liệu | `2 × ceil(frames / 256)` bản ghi |

Hệ quả: `+0x20` chứa **tên file âm thanh gốc**, và số bản ghi **không** lưu ở
dạng rõ ràng trong header — nó suy ra từ `+0x10`. Vậy công cụ đọc `.peak` bắt buộc
phải hiểu công thức ở §15.4, không chỉ đọc header.

### 15.4 Trường `+0x10` = tổng số frame; độ phân giải là **256 frame/cột**

Đo trên 19 file. Hai kết quả, một trong đó là con số quan trọng nhất của cả
nghiên cứu dải sóng:

**`+0x10` là tổng số frame của audio.** Không phải hằng — nó đổi ở **cả 19**
file (6.754.318 … 11.166.121). Vòng trước tôi chỉ kiểm một file rồi kết luận là
hằng, nên đoán sai.

**Độ phân giải `.peak` = 256 frame mỗi cột, mỗi kênh.** Kiểm bằng công thức:

```
số bản ghi  ==  2 × ceil(frames / 256)          ->  khớp 19/19 file
```

Tức `n / 2` là số cột, và mỗi cột gói **256 frame**. Lệch nhỏ giữa `frames` và
`256 × cột` là do **cột cuối không tròn** — tính được frame của cột cuối cho từng
file: 7, 21, 32, 48, 84, 96 … tới 256 (file `07. Long Way` chia hết).

Đây là câu trả lời cho câu hỏi mà §15.3 nêu là chưa giải được, và nó **sửa
đáng kể** hiểu biết cũ:

> §14.5 và §5 nói ngưỡng mặc định là **8192** frame/cột. Con số đó là
> `cacheAccessor->vfunc+0x18()` — giới hạn mà cache RAM đáp ứng, **không phải**
> độ phân giải của file `.peak`. File `.peak` ở đây là **256**. Nên khi thu nhỏ
> mạnh, Cubase gộp **32 cột `.peak`** cho mỗi pixel.

Kiểm tra nhất quán: `+0x0C` = `2` ở cả 19 file ⇒ số kênh, và `n` luôn chẵn — đúng
với bố cục xen kẽ theo kênh mà §14.4 đọc từ mã.

> **Đính chính (đọc mã ghi ở §3.7):** đoạn này ở lượt trước đã đoán `+0x1C` là
> "nhãn phiên bản/định dạng" và `+0x04` là số `65736`. **Cả hai đều sai.**
> `+0x1C` là hash chuỗi 16-bit; `+0x04` là **hai số 16-bit** (`1` và `200`), không
> phải một số 32-bit. Xem §3.7 và §3.8.

`+0x18` = `0xFFFFFFFF` là sentinel −1, hằng ở cả 19 file.

### 15.5 Đã dựng công cụ đọc `.peak`

`tools\peak_read.py` — đọc header, kiểm công thức, vẽ lại dải sóng ra PNG hoặc
ASCII (chỉ thư viện chuẩn, `zlib` để ghi PNG):

```powershell
python tools\peak_read.py "D:\01_Music_Projects\Cubase\Images" --check
python tools\peak_read.py "<mot file .peak>" --at 60 --width 96 --png wave.png
```

`--check` báo **19/19 khớp**. Ảnh vẽ ra là một dải sóng thật (một đoạn ghi âm
đã master, gần chạm 0 dB với vài đỉnh đơn) — nghĩa là toàn bộ định dạng đã đọc
được, không còn phần nào phải đoán.

Cái này cũng mở đường cho hướng "vẽ đẹp hơn": có thể dựng lại dải sóng ngoài
Cubase rồi so với ảnh Cubase chụp được, thay vì sửa bên trong tiến trình.

### 15.6 File `.peak` nằm ở đâu — đã có file thật để trả lời

```
D:\01_Music_Projects\Cubase\
  demo1.cpr
  Audio\
  Images\
    01. E851917649304.peak          <- KHÔNG cùng thư mục với WAV
    02. Body1917435672.peak
    ...
```

**Không nằm cạnh file âm thanh, mà nằm trong `Images\` ngay cạnh thư mục dự án**,
và tên đặt theo mẫu `<số thứ tự>.<tên track><số băm>`. Audio nằm ở `Audio\`.
Vậy mục 2 trong *Chưa làm* đã đóng bằng quan sát, không cần RE.

Còn một chi tiết lạ: thư mục `Images\Images\` có **một** bản `.bak` và **một** bản
`.peak` trùng tên với bản ở thư mục trên — dấu vết một lần dựng ảnh bị lặp. Không
ảnh hưởng kết luận.

### 15.7 Chưa giải được

**Đã đóng ở §3.7 / §3.8 / §3.11:**

- `+0x14` = 256 là **frames mỗi cột**, mã ghi **hardcode `0x100`**.
- `+0x0C` = số kênh, đọc từ nguồn `vfunc+0x38`.
- `+0x10` = tổng số frame, đọc từ nguồn `vfunc+0x48`, clamp `0x7FFFFFFF`.
- `+0x20` = tên file nguồn, chép **từng byte** tới byte 0.
- `+0x1C` = **hash chuỗi đường dẫn thư mục nguồn** (`0x1421F66E0`), giải thích vì sao 18 file trong `Audio\` chung hash `0x8DAFEE63`.
- `+0x04` = **major_version** (1) và `+0x06` = **minor_version** (200, tức format PIFF v1.200) — kiểm tra tại `0x1421F15B0..0x1421F15EC`.
- Thuật toán đọc mẫu âm thanh và tính đỉnh `pos_max / neg_max` tại `0x1421F5150`.
- Hằng `3.0` ở `0x141E9D4C0`: trần bán kính hạt điểm mẫu khi phóng sâu.
- Quan hệ Preferences -> Observer -> `PSeqEventImageScheme` -> `WaveStyle` -> rasterizer.

**Còn mở:**
- **`.cpr` là container `RIF2` của Steinberg**, không phải ZIP: magic `RIF2`, rồi
  chunk `ROOT`, các nhãn `CmObject` / `PAppVersion` / `Version` — tức chính là mô
  hình CmObject đã thấy trong exe. Trong đó có **18** tham chiếu `.flac`, và mỗi
  tham chiếu đi kèm một descriptor có chuỗi `flac` và chữ ký `FLAC Fi…`. Đọc được
  tần số sẽ phải hiểu cấu trúc descriptor đó — chưa làm, và là một dự án riêng.
  Lưu ý: không có chuỗi `48000`/`44100` nào trong `.cpr`, nên tần số được lưu dạng
  số nhị phân, không phải văn bản.
- ~~Cách ánh xạ frame → cột~~ — **đã đóng ở §3.3/§3.4/§3.5.** Phép tính là
  `floor(pixel · fpp / n)` với `n` = số bản ghi, không chia theo bảng.

---

## Chưa làm / hướng tiếp

1. ~~Chưa đọc được phần đầu file `.peak`~~ — **đã đóng hoàn toàn ở §15 + §3.7 + §3.8**.
   Header 96 byte, bản ghi 8 byte × 2 float32 LE không âm. Mọi trường header đã
   được đặt tên từ mã ghi và mã kiểm tra header: format PIFF v1.200 (`major=1, minor=200`),
   frames/cột = 256, hash thư mục nguồn ở `+0x1C`.
2. ~~Chưa xác định được số frame của audio~~ — **đã đóng ở §3.7**: `+0x10` là tổng
   số frame, đọc từ nguồn `vfunc+0x48`.
3. ~~Chưa truy được file `.peak` nằm ở đâu~~ — **đã đóng ở §15.6**: trong
   `Images\` cạnh thư mục dự án, tên `<tt>.<tên track><số băm>`. Cơ chế ghép tên
   trong mã vẫn chưa truy (hậu tố `%02d` ở §14.6), nhưng không còn quan trọng.
4. ~~Chưa xác minh đối tượng 0x70 byte là `MAudioCollector::FlatSliceIterator`~~
   — **đã đóng ở §14.1**: đối tượng đó là `AudioImageFile`, tức file `.peak`.
   `MAudioCollector::FlatSliceIterator` còn là ứng viên cho **nhánh `fpp < 1`**
   (vẽ bằng số mẫu thật), chưa truy.
5. ~~Chưa biết dải sóng được vẽ ra sao khi phóng to~~ — **đã đóng ở §3.3**: nhánh
   nội suy tuyến tính giữa hai bản ghi liền kênh, tính ở double. Ràng buộc thực
   tế: dưới **256 mẫu/pixel** thì dữ liệu đã bị lấy mẫu, không phải dạng sóng thật.
6. ~~Chưa rõ hằng 3.0 trong 0x141E9D4C0 chặn cái gì~~ — **đã đóng ở §4**: bán kính
   tối đa (pixel) của các chấm điểm mẫu (sample dots) khi zoom sâu `framesPerPixel < 1.0`.
7. ~~Chỗ đọc pref Show Waveforms / Wave Brightness / Wave Outline Intensity lúc vẽ~~
   — **đã đóng ở §1.1**:
   - `Show Waveforms`: cờ byte `0x1475C15B9`, phát sự kiện `"timeEditorInvalid"`.
   - `Interpolate Audio Images`: cờ byte `0x1475C1590`, đọc tại `0x141E9AD3D` và `0x141E9D5AE`.
   - `Wave Brightness` / `Outline`: đối tượng `Binding::Value` tại `0x1476E01A0 + 0x18/0x20`.
   - Observer `PSeqEventImageScheme` (`0x14393BCC0`) phối màu skin và pref sinh struct `WaveStyle` (`0xB8` byte), đưa vào `device->vfunc+0x80`.
8. `imagegenerator.dll` trong thư mục cài đặt **không** liên quan: nó là OpenCV +
   bộ lọc ảnh (`PixelSIMD@Steinberg`, `IPL_DATA_ORDER_PIXEL`), không phải dải sóng.
9. Chưa chạy được bộ probe vtable của device (xem `FLWAVE.md` §12.8) — cần Cubase
   đang chạy và vẽ dải sóng. `demo1.cpr` **có** audio nên điều kiện đã đủ, chỉ còn
   một phiên desktop thật.
10. **Sample rate**: không có trong `.peak`, và `.cpr` là container `RIF2` đóng
    gói (`§15.7`). Đây là mục RE riêng, chặn việc suy ra độ dài chính xác.
