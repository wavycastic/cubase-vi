# Nghiên cứu: làm dải sóng Cubase giống FL Studio

Mục tiêu: dải sóng audio event trong Project Window của Cubase 15 trông giống dải
sóng trong Playlist của FL Studio 2026 — khối đặc, viền sáng, không có lớp volume
curve đè lên.

Hai bên đã dò được (`docs/WAVEFORM.md` là phần Cubase, tài liệu này là phần FL
Studio + kế hoạch dựng skin).

> **Kết quả chính**: công thức tần số → màu của FL Studio **đã tìm ra** — nằm ở
> `Shared\ildsp_x64.dll` (lớp C++ `WaveformColouring`), không phải `FLEngine_x64.dll`.
> Xem **§8**. Chuỗi lời gọi dẫn tới nó ở **§9**. Cái còn thiếu để dựng bản Cubase
> 1:1 nằm ở **§8.7**.
>
> **Tóm tắt công thức**: chế độ *Multiband* **không** dùng FFT và **không** dùng
> bảng màu. Nó tách dải sóng thành **3 băng bằng hai bộ lọc một cực nối tiếp**
> (góc ~1000 Hz, `k = tan(π·1000/SR)/(1+tan(π·1000/SR))`), rồi lấy
> `R = băng thấp`, `G = băng giữa`, `B = băng cao`, chuẩn hoá theo tổng. Công thức
> đầy đủ ở **§8.8**, kết luận ở **§8.10**, thứ còn thiếu ở **§8.11**.

---

## 1. Cài đặt đã dò

| | |
|---|---|
| FL Studio | `E:\Image-Line\FL Studio 2026` |
| `FL64.exe` | 594 KB, PE32+, chỉ **1.116** hàm — loader mỏng, không phải nơi vẽ |
| `FLMManaged.dll` | 9,3 MB, PE32 **.NET** (`CLR` directory), không liên quan giao diện |
| `FLEngine_x64.dll` | **26,6 MB — toàn bộ GUI nằm ở đây** |
| `Artwork/Skins/Default/` | chỉ có ảnh (`BigFruit.png`, `Title.png`, `ScopeGradient.bmp`, …), **không** có file màu |
| `Artwork/Themes/*.flstheme` | **văn bản thuần**, INI kiểu `key=value`, 33 dòng |
| Gói ngôn ngữ | `E:\Image-Line\Shared data\Downloads\Languages\<ver>\*.moe` — `vi.moe` đã có sẵn (không đụng) |

### 1.1 `FLEngine_x64.dll` là binary Delphi — rất thuận cho RE

```
.pdata có 58.608 hàm          → xref.py / disasm.py dùng được nguyên vẹn
RTTI đầy đủ                  → il.WaveformCacheProcessor.TWaveformCacheComputeJobImpl
import: gdi32.dll, opengl32.dll, D3D$  → vẽ bằng GDI và OpenGL
```

> **Bẫy**: `pe.resolve()` ưu tiên giải số đưa vào là **file offset**. Với file 26 MB
> này, RVA của `.text` trùng vùng với offset hợp lệ của `.data`, nên truyền RVA
> vào `disasm.py` sẽ ra sai. Phải tính offset trước: `off = rva - 0x1000 + 0x400`
> cho `.text`.

---

## 2. Màu dải sóng của FL Studio nằm ở theme, không nằm ở skin

Đây là phát hiện quan trọng nhất: **FL Studio không tải màu từ skin, mà từ file
theme dạng văn bản thuần.**

Nút vẽ theme: `Options ▸ … ▸ Theme`, file `__current.flstheme`
(`FLEngine_x64.dll` file `0xD1E1CC`, xref tại RVA `0xD1DB40..0xD1ED54`).

Danh sách khoá đọc trong hàm đó (`lea r8/rdx, [rip+…]` lần lượt):

```
Hue  Saturation  Lightness  Contrast  Text  Selected  Highlight  Mute  Option
StepEven  StepOdd  TextColor  LightMode  OverrideClips  Meter  WaveClr  WaveSpc
NoteColor  EEGridFilename  PLGridCustom  PLGridBack  "\PLForm"  "Grid Color"
"Grid color"  PRGridCustom  PRGridBack  …
```

### 2.1 `WaveClr` — màu dải sóng, là một **bảng 6 màu**

```
0x111E10C  lea  rcx, [rbp+0x100]
0x111E113  lea  rdx, [rip+0xea6]        ; L"WaveClr"
0x111E11A  mov  r8,  [rbp+0xF8]         ; tên khoá đã sinh (kèm chỉ số)
0x111E121  call <đọc giá trị>
0x111E137  mov  rax, [rbp+0x138]        ; bảng màu mặc định
0x111E13E  mov  r9d, [rax]
0x111E141  call <ghi vào biến màu>
0x111E14D  or   eax, 0xFF000000         ; ép alpha = 255
0x111E16D  lea  rdx, [rip+0xe68]        ; L"WaveSpc"
```

Biến màu nằm ở `VA 0x15E6C98` (file `0x11E5C98`) — **mảng 6 phần tử**, không
phải một màu đơn: `0x112FEB7` cho thấy vòng lặp `r11d = 6` copy song song ba
bảng:

| bảng (VA) | file | bước nhảy | ghi chú |
|---|---|---|---|
| `0x15E5A08` → `0x15E6C98` | `0x11E4A08` → `0x11E5C98` | +4 | dword, màu |
| `0x15E3780` → `0x15E4A78` | `0x11E2780` → `0x11E3A78` | +8 | qword |
| `0x15E5D28` → `0x15E1A98` | `0x11E4D28` → `0x11E0A98` | +4 | dword |

Sáu màu = sáu **nhóm kênh** của mixer FL Studio (Insert 1-6 …), tức **dải sóng
trong Playlist được tô theo nhóm kênh của track**, không phải một màu chung.
Giá trị mặc định nằm sẵn trong `.data`:

```
bảng mặc định @0x11E4A08 : 0x01400900 0x00000000 0x015F57C0 0x00000000
                           0x015C411E 0x00000000 0x01940C18 …
```

> **Chưa xác minh**: byte-thứ-tự màu. Delphi `TColor` là `0x00BBGGRR`; các số
> trên đọc ra rất tối, nhiều khả năng còn phải qua bộ lọc
> `Hue/Saturation/Lightness/Contrast` của theme mới thành màu hiển thị
> (`Dark.flstheme` đặt `Lightness=-153`, `Contrast=-8`).

### 2.2 `WaveSpc` — độ dày / khoảng cách nét sóng

Đọc ngay sau `WaveClr` (`0x111E16D`). Tên gợi ý đây là tham số **khoảng cách
(độ dày) nét dải sóng** — một trong ba thứ ta muốn chỉnh.

### 2.3 Sửa theme được, FL Studio nạp lại tức thì

```
0x112958F  lea  rdx, [rip+…]   L"Theme has changed|The current theme has changed."
0x112959F  lea  rdx, [rip+…]   L"Keep"
0x11295B7  lea  rdx, [rip+…]   L"Discard"
0x11295CF  lea  rdx, [rip+…]   L"Cancel"
```

Nghĩa là FL Studio **theo dõi file theme** và hỏi người dùng khi file đổi. Nên
để chỉnh màu dải sóng FL Studio chỉ cần sửa `__current.flstheme` (thêm
`WaveClr0…5`), không cần vá exe.

---

## 3. Cache đỉnh của FL Studio

```
il.WaveformCacheProcessor                     (unit)
  TWaveformCacheProcessorIntf
  TWaveformCacheComputeJob / …ComputeJobImpl
  TPair<JJobKey, TWaveformCacheComputeJobImpl> trong TDictionary
```

Cùng kiểu kiến trúc với Audio Image của Cubase (`.peak`), cũng là job +
dictionary + chạy nền. Phía vẽ chưa truy được (xem *Chưa làm*).

---

## 4. Phía Cubase: ba cái cần đổi và mức độ can thiệp

| Cần đổi | Chỗ ở Cubase | Mức độ |
|---|---|---|
| Màu dải sóng, độ sáng | skin `eventBackDefault`, `eventWaveMuted` + pref **Waveform Brightness** | **chỉ skin + pref** |
| Độ đậm viền | pref **Waveform Outline Intensity** | **chỉ pref** |
| Bỏ lớp volume curve đè | pref **Show Event Volume Curves Always** (tắt) + skin `eventWaveAutomFill/Line` | **chỉ pref + skin** |
| Khối đặc thay vì rỗng | nằm trong **code** `0x141E9E140` | **phải vá exe** |

Vì có pref *Waveform Brightness* (điều chỉnh độ sáng **phần tô**) và pref
*Waveform Outline Intensity* (điều chỉnh viền), nhiều khả năng Cubase vốn đã tô
đặc rồi — ba dòng đầu nằm gọn trong skin + pref. Chỉ dòng cuối là vá code.

Vị trí cần nếu vá code:

| ý nghĩa | VA | `.pdata` |
|---|---|---|
| vẽ dải min/max thành hình (sang đường, -0.0f = cột rỗng) | `0x141E9E140` | RVA `0x1E9E140..0x1E9E825` (1.765 byte) |
| dựng mảng (min,max) theo cột pixel | `0x141E9C340` | RVA `0x1E9C340..0x1E9C85F` |
| vẽ bằng số mẫu thật khi phóng sâu (nội suy) | `0x141E9D4C0` | RVA `0x1E9D4C0..0x1E9E138` |
| điều phối, cấp phát buffer, +1 pixel mỗi bên | `0x141E9B6F0` | RVA `0x1E9B6F0..0x1E9BA17` |

---

## 5. Đường đi: sửa `Skins/skin.srf` — **đã có công cụ, đã kiểm chứng**

Định dạng container (đã đọc được, `tools/cubelib/srf.py`):

```
"Steinberg Resource File"   23 byte
"\r\n"                       2 byte
("/Thumbs.db\r\n" + member) × 842
bảng tra cứu                49.865 byte tại 0x134DF87
```

- **842 member**: 486 PNG, 293 XML, 22 skin, 11 BMP, 5 SVG, 25 khác.
- Member nén zlib (`78 da` / `78 9c`) hoặc để thô (PNG).
- Dấu `/Thumbs.db\r\n` **không** đứng trước mọi member — file gốc có ít hơn
  10.104 byte separator (tức ~24 byte), nên khi dựng lại phải **chép nguyên** đoạn
  giữa các member chứ không tự sinh lại.
- **Bảng tra cứu cuối file** là *manifest git nội bộ của Steinberg*, không phải
  index runtime: nó liệt kê cả `.gitignore`, `audio`, `..` (892 mục > 842
  member) theo thứ tự chữ cái, mỗi mục có offset / stored / decoded / tên, mục
  cuối có một chuỗi 32 ký tự hex trông như MD5 (chưa khớp MD5 của tên lẫn của
  payload → **chưa xác minh**).

### 5.1 `tools/skin_edit.py`

```
python tools\skin_edit.py list skin.srf --grep wave
python tools\skin_edit.py get  skin.srf eventWaveMuted
python tools\skin_edit.py set  skin.srf -o fl-wave.srf eventWaveMuted="$210,005,200" --check-index
```

Nguyên tắc an toàn khi ghi lại:

1. Member **không** đụng tới thì chép **nguyên byte**, kể cả separator → chỉ member
   sửa mới làm dịch offset.
2. Sau khi ghi, **tự parse lại** file vừa ghi bằng đúng bộ đọc của mình và so
   từng payload: sai thì báo `FAIL` và dừng.
3. `--check-index` in ra vị trí kết thúc phần member và độ lệch của bảng tra cứu.

**Đã kiểm chứng** trên `skin.srf` gốc, sửa `eventWaveMuted` `$210,005,090` →
`$210,005,200`:

```
wrote ... : 20,292,176 bytes (was 20,292,176)
  member #82: eventWaveMuted  stored 12,943 -> 12,943 (+0)
  self-check ok: 842 members, payloads intact
  members now occupy 0x0..0x134DF87 (was 0x134DF87); trailing table copied
  verbatim (49,865 bytes), so its recorded offsets are +0 bytes out of date
```

Đối chiếu byte thô: **9.420 byte khác, tất cả nằm trong member #82**, bắt đầu tại
`0x382DAC`; trước và sau đó **giống hệt**. Nghĩa là bản vá chỉ đúng chỗ cần sửa,
và bảng tra cứu cuối file vẫn còn đúng.

### 5.2 Vì sao làm bộ skin riêng được

Cubase nạp skin theo tên: đặt file `<tên>.srf` vào `Skins/` và chọn trong
Preferences. Nên kế hoạch là:

```
Skins/skin.srf                     (gốc, không đụng)
Skins/fl-wave.srf                  (bản mới, sinh từ bản gốc)
```

### 5.3 Màu nào liên quan tới dải sóng

`skin_edit.py list --grep wave` trong `skin.srf` (member #82 chứa toàn bộ):

| id | giá trị gốc |
|---|---|
| `eventBackDefault` | `$210,020,070` |
| `eventBackMuted` | `$210,010,095` |
| `eventWaveMuted` | `$210,005,090` |
| `eventWaveAutomFill` | `$210,015,090` |
| `eventWaveAutomLine` | `$210,015,075` |
| `eventFrame` | `$000,100,100` |
| `eventFrameActive` | `gray10` |
| `mbAudioPreviewWaveColor` | `$110,65,100` (member #299 — dải sóng preview trong MediaBay) |

Ba id cuối không có trong `Cubase15.exe` (`exe` chỉ giữ
`eventWaveMuted`, `eventWaveAutomFill/Line`, `eventFrame*`), nghĩa là exe phân
giải chúng qua scheme chứ không tra chuỗi lúc vẽ.

---

## 6. "Màu theo tần số" của FL Studio — có, nhưng **không phải skin**

### 6.1 Tên đúng của tính năng: `Colorful waveforms` → `Multiband`

FL Studio có đúng cái tên bạn nói. Nằm ở
**Options → General → Display → [✓] Colorful waveforms**, một combo box bên cạnh.

DFM, file offset `0x017D8EC8`:

```
TQuickCombo  ColorfulWavesCombo   Style=FS_SoberCombo  ThemeID=ColorfulWaves
Hint              "|Waveforms are shown in color"
Items.Strings     <0> Color map
                  <1> Multiband
Hints.Strings     "Don't show wave content as colors"
                  "Use colors from the theme to show average frequency content"
                  "Calculate colors after a multiband frequency analysis"
DefaultValue / OnChange -> ColorfulWavesBoxClick
```

| tên | file offset |
|---|---|
| `ColorfulWavesCombo` | `0x017D8EC8` |
| `"Colorful waveforms"` (nhãn) | `0x017D9364` |
| `forms.options.generalpage.disppanel.colorfulwavesbox` | `0x017D8F3C`, `0x017D941D` |
| `ColorfulWavesBoxClick` | `0x00F58F25` (RTTI), `0x017D922B` (DFM) |

Đúng **2 chế độ**:

- **Color map** — dùng màu của theme để thể hiện **nội dung tần số trung bình**
- **Multiband** — tính màu sau **phân tích tần số nhiều băng**

### 6.2 Setting `ColorfulWaves` — đã biết byte biến nằm ở đâu

| | |
|---|---|
| khoá (UTF-16) | `ColorfulWaves` @ `0x00DAF16C` |
| bảng đăng ký setting | hàm RVA `0xDA6F10..0xDAF0F8` (32.744 byte) |
| con trỏ tới biến | `.data` VA `0x15E5958` → trỏ tới `0x13AEAA8` |
| **biến thật** | **VA `0x13AEAA8`**, kiểu **byte** (0..255) |
| nơi đọc | chỉ **2** chỗ tham chiếu trực tiếp: đăng ký setting + widget xem trước trong Options (dispatch theo chiều cao 36/30/18 px) |

Mỗi khoá setting trong khối này có đuôi cố định 12 byte sau tên
(`b0 04 02 00 ff ff ff ff <n> 00 00 00`) — cùng dạng với `WaveClr`.

### 6.3 Setting của FL Studio nằm ở registry

```
0x00DAF7C8   Software\Image-Line\FL Studio 26\Favorite dirs
```

Tức toàn bộ setting của FL Studio 2026 nằm trong
`HKCU\Software\Image-Line\FL Studio 26`.

**Đã xác minh**: khoá này **có thật** (7 subkey: `Devices`, `Favorite dirs`,
`General`, `MRU`, `Plugin version specific`, `RMC`, `Windows`), và
`General\MIDIForm\ColorfulWaves = 2` tức đang bật **Multiband**. Nhưng **không có
khoá màu nào** cho colourful waveform: `General\Theme` chỉ có `ThemeFilename`,
`FruityLoopsMainForm` chỉ có `ColorfulChannelControls` và `MRUColor0..9` (lịch sử
màu người dùng tự chọn). Dải màu không phải setting — nó nằm trong code (xem §8 và §9).

### 6.4 Phía Cubase: không có tính năng tương đương

`keys/all_strings.tsv` của Cubase 15 chỉ có **một** chuỗi liên quan:
`Spectrum Analyzer` — đó là **plug-in**, mở cửa sổ riêng, không phải cách Cubase tô
dải sóng trong Project Window. Trong `Cubase15.exe` cũng chỉ có
`Spectrum Analyzer` / `Spectrum Display View` / `SpectrumDisplay` /
`Eq:EnableSpectrum` — toàn bộ thuộc plug-in.

Tức là muốn có "colourful waveform: multiband" trong dải sóng của Cubase thì
**phải tự tính phổ**: mỗi cột pixel chạy FFT, ánh xạ sang gradient, rồi tô dải
`(min,max)` bằng màu tính được.

### 6.5 Đã tìm được hàm vẽ Playlist của FL Studio

Nhờ RTTI kiểu Delphi (bảng *published method* của form), đã giải được địa chỉ thật:

| | |
|---|---|
| form | `TLEventPanel` — tên lớp RTTI `0x00A348FC` |
| DFM | `forms.eventeditform.tleventpanel` (`0x0174D905`), `OnPaint = TLEventPanelPaint` (`0x0174D927`) |
| tên method | `TLEventPanelPaint` `0x00A359BC`, `…MouseDown` `0x00A358C1`, `…MouseUp` `0x00A358E1`, `…DblClick` `0x00A3599D` |
| **code** | **RVA `0xE74E40..0xE79C1C` — 19.932 byte**, `TLEventPanelPaint` nằm ở `RVA 0xE76390` |

> **Bẫy mới**: trường địa chỉ trong bảng published method của Delphi **là RVA, không
> phải VA**. Bố cục mục là `Word size` + `8 byte address` + `ShortString name`
> (`size = 2 + 8 + 1 + len(tên)` — kiểm tra được với `TLEventPanelPaint`:
> 28 = 2+8+1+17). Nếu cộng ImageBase vào sẽ trỏ nhầm vào vùng `.reloc`.

FL Studio có sẵn cả framework FFT: `DSP_FFT` (`TFFT`, `TFFTBank`, `TFFTBankFFT`) và
`DSP_FFTFilter` (`TFFTFilter`) — `0x0027F6C7` trở đi.

### 6.7 Vì sao bản vá Cubase không giải quyết được, và cách thật sự khả thi

`TLEventPanel.Paint` dài 19.932 byte và có bảng nhảy nội tuyến, nên
`disasm.py` (giải mã tuyến tính) **mất đồng bộ** chỗ và sinh call giả — đọc
tay để tìm công thức tần số → màu sẽ rất chậm và dễ sai.

Quan trọng hơn: phía Cubase, thêm "màu theo tần số" **không phải vá byte được**.
Một bản vá nhỏ không thể chèn thêm cả FFT + gradient vào hàm vẽ. Ba hướng thật:

| hướng | thực tế |
|---|---|
| skin + pref | không đủ — đã loại |
| vá byte trong `Cubase15.exe` | không đủ — thiếu chỗ cho FFT + code mới |
| **DLL tiêm vào hook `0x141E9E140`** | khả thi: đã có sẵn địa chỉ hàm vẽ, đã biết mảng `(min,max)` theo cột pixel do `0x141E9C340` sinh ra. DLL tự tính FFT từ dữ liệu đó rồi vẽ đè lên cùng vùng |

Hướng khả thi là hướng cuối, và nó **không cần sửa file exe** — chỉ cần một
injector + một DLL, tự nạp khi Cubase chạy.


### 6.8 Phát hiện phụ: chuỗi giao diện của FL Studio là gettext

```
0x010A3CB0  Project-Id-Version: FL Studio
0x010A3CEE  POT-Creation-Date: 2022-08-17 11:41
0x010A3CF2  Language: zh-Hans
0x010A3D16  Content-Type: text/plain; charset=UTF-8
0x010A3D5E  X-Generator: POEditor.com
```

Bảng chuỗi tiếng Anh (và các bản dịch) nằm ngay trong `FLEngine_x64.dll` dạng
**gettext PO**, biên dịch bằng POEditor. File `.moe` ở
`Shared data\Downloads\Languages\<ver>\` rất có thể là `.mo` đã bọc lại — nhưng
định dạng nén của nó chưa xác minh (không phải zlib/LZMA/LZ4/zstd thuần).

## 7. Việc cần làm tiếp

### 7.1 Đã xong: đọc được setting của FL Studio

FL Studio đã chạy trên máy này và đã ghi
`HKCU\Software\Image-Line\FL Studio 26\General\MIDIForm\ColorfulWaves = 2`.
Không có khoá `WaveClr` nào trong registry, và theme cũng không lưu nó (§9.5) —
nên phần còn lại của §7.1 **không** lấy được từ file/registry, chỉ lấy được từ
code.

### 7.2 Nếu làm phần Cubase

1. **Chắc chắn được, nhìn thấy được**: skin + pref — sáng, đậm viền, bỏ lớp
   volume curve. `tools/skin_edit.py` đã xong và đã kiểm chứng round-trip.
2. **Colourful multiband**: phải là DLL hook `0x141E9E140` (§6.7). Mỗi cột pixel
   cần FFT; vì `0x141E9C340` chỉ cho mảng `(min,max)` nên phải tự đọc audio —
   khả năng dùng `ffmpeg.exe` của FL Studio (`Shared\ffmpeg`) để giải mã rồi tính
   trước ra một file sidecar cạnh file `.peak`, DLL chỉ đọc file sidecar đó.

## 8. Tìm ra công thức: `ildsp_x64.dll`, không phải `FLEngine_x64.dll`

### 8.1 FL Studio có hai lớp: Delphi (vỏ) và MSVC (nghệ thuật)

Công thức màu **không** nằm trong `FLEngine_x64.dll`. Nó nằm trong
`Shared\ildsp_x64.dll` (4,2 MB, **MSVC**, có section `IPPCODE` dùng Intel IPP và
2.622 hàm trong `.pdata`).

Bằng chứng — hai dấu vết trong `ildsp_x64.dll`:

```
0x003F2842  WaveformColouring_CreateInstance      (tên export)
0x003F5398  .?AVWaveformColouring@@                (RTTI type descriptor MSVC)
```

Trong 223 DLL/EXE của FL, đây là **file duy nhất** chứa `WaveformColouring`.

Cơ chế nối: `FLEngine_x64.dll` không gọi trực tiếp mà tra qua bảng *"tên → hàm"*:

```
; FLEngine RVA 0x26EAF0
lea rdx, [L"WaveformColouring_CreateInstance"]
call RVA 0x26EA70            ; tra bảng
call qword [0x13EDEF0]       ; ← CreateInstance
```

### 8.2 Từ export tới vftable

`WaveformColouring_CreateInstance` (RVA `0x1AC470`, 48 byte) chỉ là bọc:

```c
p = alloc(0x228);            // 552 byte
memset(p, 0, 0x228);
return ctor_tail(p);         // ← RVA 0x1AC4A0
```

Ctor `RVA 0x1AC4A0` viết vftable và **hard-code bộ hằng tần số**:

```c
*(void**)self = 0x1803E01B0;                    // vftable
self->f08 = 48000.0f;      self->f0C = 1.0f/48000.0f;
self->f10 = 24000.0f;      self->f14 = 3.14159265f/48000.0f;
self->f18 = 6.28318531f/48000.0f;              // 2π
self->f28 = 0.01f;          self->f2C = 1.0f;
```

Tức lớp lưu **mốc tần số chuẩn 48 kHz / Nyquist 24 kHz / góc pha tính theo
radian**. Không phải Hz — đó là dấu hiệu nó làm việc trên **trục góc pha**.

### 8.3 Bảng vftable

`VA 0x1803E01B0`:

| slot | RVA | byte | |
|---|---|---|---|
| 0 | `0x1A9CF0` | 235 | dtor |
| 1 | `0x1A9F10` | 404 | biến thể **2** bộ lọc — đường *Color map* |
| 2 | `0x1A9E10` | 247 | `SetSampleRate(SR)` |
| 3 | `0x1A9DE0` | — | `Reset()` — xoá `self+0x20`, lặp 2 vòng |
| **4** | **`0x1AA0B0`** | **475** | **`vmt[0x20]` = hàm màu — đường *Multiband*** |
| 5 | `0x1AC460` | — | `operator delete(0x228)` |

`FLEngine` gọi đúng `call [rbx+0x20]` ⇒ khớp slot 4. Xác nhận chuỗi đóng.

**Không có bộ tách băng, không có FFT trong lớp này.** Sáu slot đã hết và không
slot nào đọc audio. Lớp chỉ: nhớ sample rate, giữ 5 tần số mỗi kênh, làm mượt
một mảng số rồi trả về màu. **Mảng đầu vào do bên gọi đưa vào** — mà bên Delphi
chỉ có sẵn min/max theo cột pixel cùng dải mẫu. Suy ra: dải màu của FL **không
mô tả phổ tần số của audio**, mà mô tả **động lực** của cột pixel đó. Điều này
khớp quan sát thị giác: màu chạy dọc theo trục thời gian, không phải một dải cầu
vồng cố định từ trái sang phải.

`FLEngine` gọi đúng `call [rbx+0x20]` ⇒ khớp slot 4. Xác nhận chuỗi đóng.

### 8.4 Hàm màu, `RVA 0x1AA0B0..0x1AA28B` — công thức đầy đủ

> **Đính chính lần trước.** Tôi từng nói "màu của *một băng*". Sai. Đọc kỹ vòng lặp:
> vòng **ngoài** đi theo **kênh** (`rbx`, `rcx += 0xEC` mỗi vòng), vòng **trong** duyệt
> **mảng năng lượng băng** của kênh đó (bước `4 × sốKênh`). Đầu ra là **một RGB
> mỗi kênh** (`r8 += 0xC`). Tức hàm này biến **một vector phổ** thành **một màu**.

`rcx = self + 0x8C` là khối trạng thái của kênh đang xét: **5 cặp `(hệ số, trạng
thái)`**, mỗi cặp cách nhau `0x28` byte.

```c
// v = input[i]  (năng lượng băng thứ i, đã kèm sẵn theo kênh)
float d0 = (v - s0) * k0;   s0 += d0;  float e  = v - s0;   st0 = s0 + d0;
float d1 = (e - s1) * k1;   s1 += d1;  float e2 = e  - s1;  st1 = s1 + d1;
m5 = sqrt( (s0*s0 - s2) * k2 + s2 );
m4 = sqrt( (s1*s1 - s3) * k3 + s3 );
m3 = sqrt( (e2     - s4) * k4 + s4 );

float sum = m3 + m4 + m5;
float inv = 1.0f / max(sum, 1.19e-07f);        // hằng 0x1803E0230
out.R = inv * m5;    // [rcx+0xA4]
out.G = inv * m4;    // [rcx+0xA8]
out.B = inv * m3;    // [rcx+0xAC]
```

| phần tử | offset từ `rcx` |
|---|---|
| `k0` / `st0` | `-0x04` / `+0x00` |
| `k1` / `st1` | `+0x24` / `+0x28` |
| `k2` | `+0x4C` |
| `k3` | `+0x74` |
| `k4` | `+0x9C` |
| kết quả R,G,B | `+0xA4`, `+0xA8`, `+0xAC` |

**Nói gọn**: màu **không** lấy từ bảng màu nào cả, mà là

```
R : G : B  =  m5 : m4 : m3
```

— ba mức năng lượng đo bằng ba bộ lọc một cực có **hằng thời gian khác nhau**, quy
thành ba kênh màu. Nhiều năng lượng ở bộ lọc nhanh hơn ⇒ ngả về xanh; chậm hơn ⇒
ngả về đỏ. Nhờ đó màu **biến đổi theo thời gian** trên dải sóng, đúng như bạn thấy.

### 8.5 Bảng hệ số: 5 tần số, mặc định 1000 Hz

`slot 2` (`RVA 0x1A9E10`) là **`SetSampleRate(SR)`**. Nó gọi `RVA 0x1A99A0` hai
lần, với `self+0x50` và `self+0x13C` (chênh `0xEC`) — **hai khối, mỗi khối một
kênh**. `0x1A99A0` viết mẫu `0x28` byte:

```c
p[+0x00] = SR ;  p[+0x04] = 1/SR ;  p[+0x08] = SR*0.5 ;
p[+0x0C] = (1/SR)*π ;  p[+0x10] = (1/SR)*2π ;  p[+0x14] = 0 ;
p[+0x18] = SR ;  p[+0x1C] = 1/SR ;  p[+0x20] = SR*0.5 ;
p[+0x24] = (1/SR)*π ;  p[+0x28] = (1/SR)*2π ;
p[+0x30] = f ;                                  // ← tần số của bộ lọc này
p[+0x34] = F( (1/SR)*π * f ) ;                 // F = hàm Ở RVA 0x1C9EF0
p[+0x38] = p[+0x34] / ( p[+0x34] + 1.0f ) ;     // ← đây chính là k
p[+0x3C] = 0 ;
```

Ghép đúng với §8.4: `k_i` của hàm màu nằm ở `self+0x88`, `+0xB0`, `+0xD8`,
`+0x100`, `+0x128` — tức `+0x38` của **5 mẫu kế tiếp** (bước `0x28`).

**Bảng tần số nằm ngay trong ctor dưới dạng hằng số.** Trích 81 lệnh
`mov [rbx+disp], imm` cho ra mẫu lặp với bước `0x28`, và **cả 5 tần số đều bằng
1000.0 Hz**:

```
self+0x80 = 1000.0    self+0xA8 = 1000.0    self+0xD0 = 1000.0
self+0xF8 = 1000.0    self+0x120 = 1000.0
self+0x16C = 1000.0   self+0x194 = 1000.0   self+0x1BC = 1000.0
self+0x1E4 = 1000.0   self+0x20C = 1000.0        (kênh 1, base self+0x13C)
```

Kèm theo mỗi tần số là `π/SR` và `2π/SR` cùng giá trị `SR`, `1/SR`, `SR/2`.

**Nghĩa là**: 1000 Hz chỉ là **mặc định khởi tạo**; 5 giá trị này được ghi đè lúc
chạy (nhiều khả năng theo vùng tần số đang hiển thị), và **hệ số `k` suy ra từ
tần số qua `F(π·f/SR)/(1+F(π·f/SR))`**. Đó là lý do dải sóng đổi màu khi zoom.

### 8.6 Hệ số `k`: đã biết chính xác — `k = tan(π·f/SR) / (1 + tan(π·f/SR))`

`F` ở `RVA 0x1C9EF0` **là `tan`**, không phải `exp` cũng không phải logistic. Ba
ngưỡng rẽ nhánh là `π/4`, `2⁻¹³`, `2⁻²⁷` — biên vùng đa thức của `tan`, kèm giảm
đoạn bằng cách tròn tới bội chẳn của π (`cvttpd2dq` trên `x·1/π + 0.5`).

| vùng `\|x\|` | công thức |
|---|---|
| `< 2⁻²⁷` | `x` |
| `2⁻²⁷ … 2⁻¹³` | `x + x³·c`, với **`c = 0.3333333333333333` = 1/3** |
| `2⁻¹³ … π/4` | `x + x³(Ax²+B) / ((Cx²+D)x²+E)` |
| `> π/4` | giảm đoạn theo π rồi trên đó |

`c = 1/3` là số hạng khai triển Taylor đầu của **tan** (`tan x = x + x³/3 + …`; của
`sin` thì phải là `−1/6`).

**Kiểm chứng bằng hằng của ctor** — hằng trùng khớp tới 7 chữ số:

```
tan(π · 1000 / 48000) = tan(0.06544985) = 0.0655435   ← hằng 0x3D863BA7
  ÷ (1 + 0.0655435)                             0.0615118   ← hằng 0x3D7BF3C6
```

Vậy mỗi mẫu `0x28` giữ:

```
k = tan( (1/SR)·π·f ) / ( 1 + tan( (1/SR)·π·f ) )
```

Mặc định cả 5 tần số bằng 1000 Hz và `SR = 48000` ⇒ **cả 5 hệ số đều bằng 0.0615118**.
Nghĩa là 5 bộ lọc **cùng hằng thời gian**; chúng khác nhau ở chỗ được **bơm vào
tín hiệu khác nhau** (`v`, `v−s0`, `s0²`, `s1²`, `e2`). Đó là mấu chốt của thiết kế.

### 8.7 Các hằng số đã giải

| hằng | giá trị | nghĩa |
|---|---|---|
| `0x1803E0570` | `0.5` (float) | dùng cho `SR*0.5` = Nyquist |
| `0x1803E0718` | `π` (double) | radian/mẫu |
| `0x1803E0738` | `2π` (double) | radian/mẫu (chu kỳ) |
| `0x1803E0230` | `1.19e-07` (float) | epsilon `max(sum, ε)` |
| `0x1803E0820` | `100.0` (float) | tần số tham chiếu #1 (`1.0/0.01`) |
| `0x1803E0870` | `640.0` (float) | tần số tham chiếu #2 |
| `0x1803E3118` | `1/3` (double) | hệ số `x³` của `tan` |
| ctor | `48000` / `1/48000` / `24000` | mốc tần số chuẩn |

Ctor tính sẵn `f30 = tan(100·π/SR)`, `f34 = f30/(1+f30)`, và tương tự với `640`.

Phía Delphi, `FLEngine RVA 0x29B390` dùng bảng hệ số cửa sổ ở
`VA 0x13F0824` (`[0]=0`, `[1]=0.01`, `[2]=0.1`) — xem §9.7 bước 4.

### 8.8 Công thức cuối cùng, đủ để dựng lại

```c
// SR   : sample rate, đặt qua SetSampleRate
// f[5] : 5 tần số, mặc định cả 5 = 1000 Hz
// in[] : mảng năng lượng theo cột pixel (bên Delphi đưa vào)
// out  : 1 RGB float3 mỗi kênh

for (ch = 0; ch < nch; ++ch) {
    for (i = 0; i < n; ++i) {
        float k0 = K(f[0]), k1 = K(f[1]), k2 = K(f[2]), k3 = K(f[3]), k4 = K(f[4]);
        float v  = in[ch][i];
        float d0 = (v - s0) * k0;  s0 += d0;   float e  = v - s0;
        float d1 = (e - s1) * k1;  s1 += d1;   float e2 = e  - s1;
        float m5 = sqrt(s2 + (s0*s0 - s2) * k2);
        float m4 = sqrt(s1*s1 + (s1*s1 - s3) * k3);
        float m3 = sqrt(s4 + (e2 - s4) * k4);
    }
    float inv = 1.0f / max(m3 + m4 + m5, 1.19e-07f);
    out[ch] = (inv*m5, inv*m4, inv*m3);
}
K(f) = tan(M_PI * f / SR) / (1.0f + tan(M_PI * f / SR));
```

Trạng thái `s0..s4` **giữ giữa các lần gọi** (mỗi kênh một bộ riêng), nên đây là
một bộ lọc **thời gian** dọc theo trục thời gian của dải sóng — cũng là lý do phải
tính lại mỗi khi zoom.

### 8.9 Đã đóng: 5 tần số là hằng biên dịch, không ai ghi đè

Quét toàn bộ `ildsp_x64.dll` tìm mọi dấu vết của `1000.0f`: **13 lần, toàn bộ trong
`.text`**, trong đó 11 nằm ngay trong ctor (`file 0x1AB8BF–0x1ABD79` = RVA
`0x1AC4BF–0x1AC979`). Hai chỗ còn lại vô can:

| RVA | nội dung |
|---|---|
| `0x16A630..0x16AB5A` | bảng hằng chung, có cả `100.0f` bên cạnh — không liên quan |
| `0x19617A` | một `comiss` so với `1000.0f`, không có `.pdata` |

Không có bảng thang tần số nào trong `.rdata` (đã dò cả 5 float liên tiếp tăng đơn
điệu, gần như cấp số nhân). Vậy **cả 5 tần số là hằng biên dịch, đều 1000 Hz**, và
**cả 5 hệ số bằng nhau**:

```
k = tan(π·1000/SR) / (1 + tan(π·1000/SR))
SR=48000 → 0.0615118      SR=44100 → 0.0665735      SR=96000 → 0.0316982
```

Hệ số tỉ lệ nghịch với sample rate — đúng nghĩa của một tần số cố định 1000 Hz.

### 8.10 Vì sao gọi là "Multiband": tách băng bằng bộ lọc một cực, không phải FFT

Đọc lại 5 bộ lọc với tên gọi đúng, chúng thành **một bộ tách 3 băng bằng bộ lọc
một cực nối tiếp**:

```c
s0 = LPF(v)          e  = v - s0          // băng thấp, rồi phần dư
s1 = LPF(e)          e2 = e - s1          // băng giữa, rồi phần dư

R = sqrt( LPF(s0²) )     ← băng THẤP
G = sqrt( LPF(s1²) )     ← băng GIỮA
B = sqrt( LPF(e2 ) )     ← băng CAO

out = (R, G, B) / max(R+G+B, 1.19e-07)
```

Đó là toàn bộ ý nghĩa của chế độ *Multiband*, và nó khớp đúng thứ bạn quan sát:
vùng nhiều bass đỏ, vùng nhiều treble xanh/tím. Không có FFT, không có bảng màu,
không bảng tần số — chỉ ba bộ lọc một cực có góc quanh 1000 Hz rồi chuẩn hoá.

Vì bộ lọc là **trạng thái lưu giữa các lần gọi** và hàm được gọi **một lần cho mỗi
cột pixel** (xác nhận ở `FLEngine RVA 0x8C8500`: `cmp eax, esi` so bộ đếm cột với
tổng số cột, lời gọi nằm trong vòng lặp đó), nên:

- đầu vào là **chuỗi giá trị theo cột pixel** của vùng đang xem,
- màu mỗi cột phụ thuộc **cả giá trị của nó lẫn lịch sử phía trước**,
- phải tính lại mỗi khi zoom, vì chuỗi cột thay đổi.

### 8.11 Còn thiếu: đúng một thành phần vô danh

Truy tiếp phía Delphi để biết `in[]` là gì:

`FLEngine RVA 0x29B390` (1.840 byte) là bước *chuẩn bị + cache*, gọi trước hàm màu với
`(obj, mode, sốCột, conTrỏNgoài, &bool, &ptr)`. Nó lộ ra hai điều kiện bắt buộc:

```c
obj->f40 = 1;
window = Round( bảngHệSố[mode] * obj->f54 );      // 0.1 × sample rate
if (sốCột < 0x20)            return 0;             // cần >= 32
if (obj->f6C < window)       return 0;             // audio >= 0,1 giây
```

Rồi tới cache, khoá theo **cặp `(độ dài, mode)`**:

```c
bảng = obj->f44;                                  // một interface
if (bảng[8*mode + 8] == obj->f6C && bảng[0x20] == mode)
     kếtQuả = obj->f8;                            // ← TRÚT CACHE = in[]
else
     bảng->slot0();                               // dựng lại
```

Nên `in[]` **không** được tính trong hàm này: nó do một thành phần khác sinh ra rồi
cache lại, và thành phần đó nằm sau interface ở `obj+0x44`. Tham dòng
`RVA 0x29B390` không có chuỗi nào để đặt tên, nên phải đi tiếp qua RTTI của Delphi
để tìm lớp hiện thực — đó là một cuộc săn riêng, và tôi đánh giá giá trị thấp.

**Xác nhận chắc (không suy đoán):** hàm màu được gọi **một lần cho mỗi cột pixel** —
vòng lặp cột ở `FLEngine RVA 0x8C8500` so bộ đếm cột với tổng số cột
(`cmp eax, esi`) và gọi `0x373720` bên trong. Vì trạng thái bộ lọc giữa các lần gọi,
`in[]` là **chuỗi giá trị dọc theo trục thời gian của vùng đang xem**, và màu mỗi cột
phụ thuộc cả giá trị của nó lẫn lịch sử phía trước.

**Còn thiếu duy nhất**: giá trị mà mỗi cột đóng góp — biên độ thô, hay đã lấy log,
đã chuẩn hoá theo `(min,max)` của cột. Đây là **giả định duy nhất** khi dựng bản
Cubase, và nó chỉ ảnh hưởng *độ tương phản* của dải màu, không ảnh hưởng cấu trúc
thuật toán.

Ngoài ra:
- Chưa biết `WaveSpc` là độ dày nét hay khoảng cách giữa các cột.
- Chưa xác minh đối chiếu với ảnh chụp thật (§10).

---

## 9. Vòng RE thứ hai: đã mở được đồ thị lời gọi

### 9.1 Bảng stub 6 byte của Delphi — nguyên nhân gốc của "call vô nghĩa"

`FLEngine_x64.dll` có **đúng một** bảng nhảy, nằm trong section *tên là*
`.pdata` — và section đó **không** phải exception directory (thật là RVA
`0x19A8980`). `find_runs()` trong `tools/research/thunk.py` (chỉ chấp nhận
**run liên tục** ≥ 16 mục `E9 rel32` nhảy vào vùng code) ra:

```
stub run >= 16 muc: 1
  VA 0x1AB1400 .. 0x1C18998   245.316 stub
      target RVA 0x7080 .. 0x11EF0
```

Mỗi mục = `E9 rel32` (5 byte) + 1 byte đệm. **340/340 lời gọi trực tiếp trong
`TLEventPanel.Paint` đều trỏ vào stub** — không có ngoại lệ. Đó chính là lý do
đọc tay hàm 19.932 byte trước đây không ăn: mọi đích lời gọi đều nằm ở
`0x1AB5xxx`, ngoài mọi thứ đọc được.

Đi qua stub, `TLEventPanel.Paint` (RVA `0xE74E40..0xE79C1C`) gọi **340 hàm khác
nhau, mỗi hàm đúng 1 lần** — đúng mẫu của một unit chứa 340 hàm vẽ nhỏ sinh ra
cùng lúc. Callee đáng chú ý:

| RVA | byte | nhiều khả năng là |
|---|---|---|
| `0x4E63E0..0x4E6995` | 1.461 | hàm tô lớn nhất trong painter |
| `0x4E6AA0..0x4E6BFB` | 347 | hàm tô kèm |
| `0x4E62D0..0x4E63B2` | 226 | |
| `0x4E5B00..0x4E5BBA` | 186 | |
| `0x50560..0x50611` | 177 | |
| `0x4CFA30..0x4CFADA` | 170 | |
| `0x133F0..0x13477` | 135 | |
| `0xF9E0..0xFA5B` | 123 | |
| `0x1A7B0..0x1A7F5` | 69 | gọi ~20 lần |
| `0x12D60..0x12DA2` | 66 | gọi ~14 lần |
| `0x14E70..0x14EB9` | 73 | **đọc setting** (`rcx`=owner, `rdx`=`&var`) |
| `0x1A770..0x1A7A8` | 56 | gọi ~10 lần |

### 9.2 `ColorfulWaves` có **11** chỗ đọc (bản đầu của tôi ghi 2 — sai)

> **Đính chính.** Lần đầu tôi dò nhầm địa chỉ (lệch `0x1000`) nên xref vào **con trỏ**
> `0x15E5958` chứ không phải biến, và kết luận "painter không đọc biến này". Sai.
> Biến thật ở **VA `0x15E4958`** (RVA `0x11E4958`, `.data`), và nó có **11** xref:

| VA đọc | hàm (RVA) | vai trò |
|---|---|---|
| `0xDE7651` | `0x9E6EA0..0x9E7B4F` | |
| `0xF6DD76` | `0xB6D9A0..0xB6E3D2` | |
| `0xF70868` | `0xB70790..0xB708AD` | **copy chế độ vào field `+0x156D`** |
| `0x111F615` | `0xD1F5C0..0xD2059E` | vùng bảng đăng ký setting |
| `0x1198CC1` | `0xD98350..0xD9F969` | |
| `0x11A8E61`, `0x11A8E71` | `0xDA6F10..0xDAF0F8` | đăng ký setting |
| `0x11B1A45` | `0xDB0F30..0xDB2790` | |
| `0x12DB138` | `0xEDAC80..0xEDB44A` | chỉ đọc khi cờ `bit 0x20` ở `[+0x13]` bằng 0 |
| `0x1367993`, `0x13679A9` | `0xF67980..0xF67A4D` | handler `ColorfulWavesBoxClick` |

Cả ba chỗ ở `0x7319D0` / `0x731AE0` / `0x731C20` (setter generic) đọc **con trỏ**
tới biến, không phải biến — nên chúng không nằm trong bảng trên.

> **Sửa `xref.py`**: có `XrefFinder.find_va()` nhưng CLI không expose, mà biến
> setting nằm ngoài vùng có byte thô thì `PE.resolve` không sinh được offset.
> Nay đã có `xref.py <exe> --va <VA>`.

### 9.3 **Không** có bảng màu nào để tra — FL tính màu bằng công thức

Quét mọi section dữ liệu, hai cách:

| cách | kết quả |
|---|---|
| dword colour table, khớp **chính xác** byte đã đo trên màn hình (`0x16 0x7D 0xA2 0xBF 0xD6 0xEB 0xFA`) | **0** run |
| bảng byte đơn điệu ≥ 64 byte (dạng hue sweep) | chỉ có bảng xám |

Ba bảng byte đơn điệu đáng kể nằm cạnh nhau, mỗi bảng 256 mục:

```
VA 0x13E06DA   0x00 00 00 00 01 02 03 04 04 05 ...   (giá trị tối đa ~0x1D)
VA 0x13E07E2   0x10 11 12 12 13 13 14 ...
VA 0x13E08E0   0x00 01 02 03 04 05 06 07 ...
```

Đây là **gamma LUT theo từng kênh R/G/B** của bộ lọc theme, không phải dải màu
tần số. Không có bảng nào quét hue.

### 9.4 Multiband **không** lấy màu từ theme

Giả thuyết cũ (§2.1: 6 màu `WaveClr` của theme là màu dải sóng) **sai với
Multiband**. Field `0x184C` — nơi palette `WaveClr` 6 sắc được copy vào — chỉ
được **7 hàm** chạm tới, và cả 7 đều nằm trong vùng theme `RVA 0xD2C000..0xD32000`:

```
RVA 0xD31920 (1.898 B, 18 hit)   RVA 0xD2CE00 (3.109 B, 12 hit)
RVA 0xD32290 (497 B, 9 hit)      RVA 0xD2DB50 (314 B, 6 hit)
RVA 0xD2DF80 (182 B, 6 hit)      RVA 0xD2E430 (2.476 B, 4 hit)
```

Còn `TLEventPanel.Paint` chỉ đọc **một** biến màu trong khối đó —
`VA 0x15E6CC0` (mục thứ 5 của bảng con trỏ bắt đầu ở `0x15E6C98`), đúng 6 lần —
và không đụng 5 mục còn lại. Tức `Color map` và `Multiband` là **hai đường màu
độc lập**.

### 9.5 Theme không lưu `WaveClr`

Lần chạy FL Studio **không** sinh `__current.flstheme` (đã tìm toàn bộ ổ `C:\Users\Administrator` và `E:\`),
và trong **42** file `.flstheme` ship kèm **không file nào** có khoá `WaveClr` /
`WaveSpc`. Nên giá trị mặc định của palette nằm thẳng trong `.data`.

### 9.6 Còn mắc ở đâu (sau khi dò bảng stub)

Không còn mắc ở chỗ này nữa. Trước khi có bảng stub, tôi tưởng công thức nằm sau
chuỗi lời gọi ảo mà `TLEventPanel.Paint` gọi — hoá ra `Paint` **không phải** hàm vẽ
dải sóng. Sau khi giải được stub, đường đi đúng nằm ở field `+0x156D`; xem §9.7.

### 9.7 Chuỗi lời gọi từ setting tới màu — đã dò tận nơi

Đây là kết quả của việc đi theo VMT mà bạn chọn. Toàn bộ chuỗi đã đóng, chỉ còn
một bước vớt (xem 9.8.7).

**Bước 0 — handler đổi chế độ.** `ColorfulWavesBoxClick`, RVA `0xF67980..0xF67A4D`
(205 byte):

```
mov rcx, [rcx+0x1078] ; call đọc-giá-trị-combo      ; 0/1/2
mov rcx, [0x15E4958]  ; mov byte [rcx], al          ; ghi vào setting
mov rcx, [0x15E61C0]  ; [rax] vtable call [rbx+0x2B0]  ; SetSetting
mov rax, [0x15E5370]  ; [rax] call [rbx+0x178]         ; Invalidate
; lặp trên mảng global [0x15E6A30], lọc theo kiểu ở 0xF5B550,
; gọi [vmt+0x178] trên từng thực thể
```

**Bước 1 — chép chế độ vào field của đối tượng vẽ.** RVA `0xB70790..0xB708AD`:

```
mov rax, [rbp+0x50] ; mov rax, [rax+0x820]
mov dword [rax+0x15AC], -1              ; đánh dấu cache cũ
mov rcx, [0x15E4958] ; movzx ecx, byte [rcx]
mov byte [rax+0x156D], cl               ; ← field chế độ
```

Field `+0x156D` bị **6 hàm** chạm tới; hàm vẽ là `RVA 0x8C8500..0x8C9AF7`
(5.623 byte) — đọc nó **4** lần. (Đây mới là hàm vẽ dải sóng thật, **không** phải
`TLEventPanel.Paint`: hàm đó chỉ tham chiếu 4 chuỗi, trong đó có `"Record %s to"`.)

**Bước 2 — truyền chế độ xuống hàm màu theo cột pixel.** Trong hàm vẽ, mỗi lần
dựng cột:

```
movsd  xmm3, [r9+0x11FC]
cvtsi2sd xmm0, rax
movsd  [rsp+0x20], xmm0
divss  xmm0, [0xCC9B60] ; movsd [rsp+0x28], xmm0
mov    eax, [rbp+0x9C]  ; mov dword [rsp+0x30], eax
mov    dword [rsp+0x38], 0xFF            ; ← 255, có vẻ là alpha
mov    eax, [rbp+0xA4]  ; mov dword [rsp+0x40], eax
movzx  rax, byte [rax+0x156D]
mov    byte [rsp+0x48], al               ; ← đối số ngăn xếp thứ 10 = chế độ
mov    dword [rsp+0x50], -1
call   <stub>  →  RVA 0x373720..0x373F16 (2.038 byte)
```

**Bước 3 — rẽ nhánh theo chế độ** (trong `0x373720`):

```
cmp byte [rbp+0x198], 0     ; chế độ (đối số ngăn xếp + 0x48 của caller)
jbe <màu mặc định>
; chế độ >= 1: xin handle từ cache
;   mode 1 → call RVA 0x29BC10  → trả số nguyên đã chuẩn hoá
;            colour = table[ Round(n × HằNG × (count-1)) ]
;            table ở VA 0x15F79F0, xây lúc chạy trong .bss
;   mode 2 → call RVA 0x29BC10  → trả thẳng TColor, dùng làm màu
; rồi:  word[+0xC4] = 0x7FFF ; word[+0xC6] = 0x8000   (kẹp min/max ±32767/-32768)
;       call RVA 0x29A090  → lấy (min,max) của cột pixel
#       call RVA 0x2BE630  → vẽ cột
```

**Bước 4 — `RVA 0x29BC10..0x29C06D` (1.117 byte)**, hàm trung tâm. Nhánn đầu:

```
mov eax, ebx ; sub al,1 ; test al,al ; jne <mode 2>      ; mode-1
```

| | mode 1 (Color map) | mode 2 (Multiband) |
|---|---|---|
| cửa sổ | `Round(0.01 × [obj+0x54])` | `Round(0.1 × [obj+0x54])` |
| `[obj+0x54]` là | sample rate (double) | sample rate (double) |
| trả về | **2 byte**: `Round([obj+0x18]×255)`, `Round([obj+0x24]×255)` | **2 TColor** |
| cách dùng | tra `table[n]` ở `0x15F79F0` | dùng thẳng làm màu |

Bảng hệ số cửa sổ nằm ở **`VA 0x13F0824`**: `[0]=0.0`, `[1]=0.01`, `[2]=0.1`
(kèm `0x01080402` ở `[3]`, không phải float). Ở 48 kHz: **480 mẫu** cho Color map,
**4.800 mẫu** cho Multiband. Hằng `0x69C070 = 255.0`.

Nhánh có cache (`[cache] != nil`) — đường nhanh, và là đường thật khi đang zoom:

```
xmm6  = (float)pixelPos / [obj+0x6C]
count = (dài mảng [rdi+0x2C]) - 1
idx   = Round(xmm6 × count)                       ; ← chọn băng
[out] = (idx < [rdi + 8×mode + 0x34])             ; cờ hợp lệ
; nếu idx == count-1  → lấy thẳng phần tử cuối
; ngược lại           → nội suy giữa phần tử idx và idx+1 theo t= xmm6
;   colour : RVA 0x29BB50 (172 byte)
;   kênh   : RVA 0xAE30  (50 byte)
```

Bảng băng `[rdi+0x2C]` là mảng bản ghi **8 byte** (2 dword). `[rdi+0x34+8×mode]` là
**số băng của từng chế độ**. Bảng này dựng ở `RVA 0x3769C0..0x376AC3`:

```
lea  rcx, [0x15F79F0] ; mov rdx, [type 0x771520] ; mov r8d, 1
mov  r9,  [obj+0x80]              ; ← SỐ BĂNG
call SetLength                     ; dword, độ dài = số băng
; lặp i = 0 .. số băng-1:
;   lea rax, [obj+0x108] ; mov rcx, [rax+8]
;   call [rax]                    ; ← gọi ảo, trả 1 dword
;   mov [0x15F79F0 + 4*i], eax
```

**Bước 5 — worker phân tích.** `RVA 0x29B090..0x29B382` (754 byte):

```
nếu [obj+0x10] == nil → tạo analyser qua factory (lazy)
xmm1 = [obj+0x54] ; call [vmt+0x10]              ; analyser.SetSampleRate(SR)
window = Round(bảng[chế độ] × [obj+0x54])
nếu [obj+0x4D] != 1:
    call RVA 0x17FC0(obj+0x38, <class 0x68FE30>, 1, window×2×[obj+0x4C])
; mode 2:
    rcx = [obj+0x10] ; rbx = [rcx]              ; vtable của analyser
    [rsp+0x20] = obj + 0x20                      ; ← tham số ra
    call [rbx + 0x20]                           ; ← PHÉP TÍNH MÀU MULTIBAND
```

**Bước 6 — chuyển float ra `TColor`.** `RVA 0x2612C0` (139 byte), dùng cho cả 2
màu của mode 2:

```
; xmm0, xmm1, xmm2 = r, g, b  (float 0..1)
mulss  xmm0, [0x661350]        ; 255.0
cvtss2sd ; addsd [0x661358]    ; + 0.5
call   <Round>                 ; × 3 lần
shl rbx,16 ; shl rsi,8 ; add ; add     → 0x00BBGGRR (Delphi TColor)
```

**Bước 7 — chỗ còn lại: `vmt[0x20]` của analyser.** Đây là bước duy nhất chưa
mở được. Analyser được lấy **theo tên**, không phải theo lớp:

```
; RVA 0x26EAF0..0x26EB2A
cmp qword [0x13EDEF0], 0 ; jne <có sẵn>
lea rcx, [0x13EDEF0] ; lea rdx, [0x66EB38]        ; L"WaveformColouring_CreateInstance"
call RVA 0x26EA70                                 ; tra bảng "tên → hàm"
call qword [0x13EDEF0]                            ; ← CreateInstance
```

Bảng tra được dựng từ một *class reference nhúng trong code* (`lea rcx, [0x66EA34]`
— không phải VMT nên không đọc được tên lớp), tra bằng id (`RVA 0x235F0`). Chuỗi
`WaveformColouring_CreateInstance` **chỉ xuất hiện 1 lần** trong cả DLL (UTF-16,
file `0x0026DF38`), nên bảng khoá theo id/hash chứ không theo tên. Đây là bước
RE còn lại.

### 9.8 Những gì đã loại trừ (để không dò lại)

| giả thuyết | kết luận |
|---|---|
| `TLEventPanel.Paint` vẽ dải sóng | **Sai** — nó chỉ tham chiếu 4 chuỗi, có `"Record %s to"`; hàm vẽ thật là `RVA 0x8C8500` |
| palette theme `WaveClr` sinh màu Multiband | **Sai** — Multiband dùng bảng ở `0x15F79F0` và 6 float từ analyser |
| có bảng màu tĩnh trong `.data` | **Sai** — bảng nằm trong `.bss`, dựng lúc chạy bởi `RVA 0x3769C0` |

### 9.9 Bảng địa chỉ thu gọn

| ý nghĩa | RVA |
|---|---|
| hàm vẽ thật của Playlist | `0x8C8500..0x8C9AF7` (5.623 byte) — **không** phải `TLEventPanel.Paint` |
| hàm màu theo cột pixel | `0x373720..0x373F16` (2.038 byte) |
| hàm phân tích băng | `0x29BC10..0x29C06D` (1.117 byte) |
| worker FFT | `0x29B090..0x29B382` (754 byte) |
| lấy (min,max) cột pixel | `0x29A090..0x29A2B3` (547 byte) |
| vẽ cột | `0x2BE630..0x2BE76E` (318 byte) |
| chuyển float→`TColor` | `0x2612C0` (139 byte) |
| nội suy màu giữa 2 băng | `0x29BB50` (172 byte); một kênh: `0xAE30` (50 byte) |
| dựng bảng màu theo băng | `0x3769C0..0x376AC3`: `SetLength(table, [obj+0x80])` rồi `table[i] = iface108.GetColour(i)` |
| `Round` | `0xC660` |
| chép chế độ vào field `+0x156D` | `0xB70790..0xB708AD` |
| handler `ColorfulWavesBoxClick` | `0xF67980..0xF67A4D` (205 byte) |
| bảng hệ số cửa sổ theo chế độ | `VA 0x13F0824` — `[1]=0.01`, `[2]=0.1` |
| hằng `255.0` | `VA 0x69C070` |
| bảng màu runtime (`.bss`) | `VA 0x15F79F0` |
| biến setting `ColorfulWaves` | `VA 0x15E4958` |
| tên thành phần tô màu | `L"WaveformColouring_CreateInstance"`, file `0x0026DF38` |

### 9.10 Công cụ mới trong vòng này

| file | làm gì |
|---|---|
| `tools/research/disasm2.py` | giải mã tuyến tính **có tự đồng bộ lại**: kiểm tra đích `call`/`jmp` phải nằm trong section, gặp lỗi thì báo `??` và dịch tiếp từ byte kế — dùng được với hàm có bảng nhảy nội tuyến. Cờ `--va` vì `PE.resolve` ưu tiên offset và đọc sai VA trùng vùng offset hợp lệ. |
| `tools/research/thunk.py` | `find` (dò bảng stub), `resolve` (1 stub → đích thật), `calls` (đồ thị lời gọi của 1 hàm, đã giải qua stub). Phát hiện bảng bằng **tính liên tục**, không phải quét `E9` ở mọi byte — quét thô ra 279.734 kết quả sai. |
| `tools/research/xref.py --va` | dò xref tới địa chỉ **không có byte thô** (biến setting). Chính cờ này lộ ra sai sót lệch `0x1000` ở §9.2. |

> **Công cụ quan trọng nhất không phải của repo**: `llvm-objdump` đã có sẵn ở
> `C:\Program Files\LLVM\bin`. Nó giải mã sạch hơn capstone và in comment đích
> RIP-relative. **Nhưng `--start-address` là VA, không phải RVA** — suýt đọc nhầm
> một lần. Và trong `llvm-objdump` nhãn `<__dbk_fcall_wrapper+...>` là vùng nhãn
> tượng trưng của LLVM, **không phải** tên hàm.

### 9.11 Cái chưa mở được

`in[]` — giá trị mỗi cột pixel đóng góp — do một thành phần Delphi vô danh sinh ra
(xem §8.11). Đây là **giả định duy nhất** còn lại khi dựng bản Cubase, và nó chỉ
ảnh hưởng độ tương phản chứ không ảnh hưởng cấu trúc thuật toán.

## 11. Đã dựng: bộ skin + pref (phần làm được ngay, không cần hook)

Công thức màu Multiband (§8) cần DLL. Nhưng ba thứ *hình dạng* thì chỉ skin + pref
là xong, và đã dựng xong trên máy này.

### 11.1 Định dạng màu của skin Steinberg: `$h,s,l`

| thành phần | ý nghĩa |
|---|---|
| `h` | **độ** của hue, 0-360 |
| `s` | saturation, 0-255 |
| `l` | lightness, 0-255 |

`h` là **độ**, không phải thang 0-255: trong `skin.srf` có 6 giá trị vượt 255
(`h = 275, 339, 340, 345, 350, 355`), điều mà thang 0-255 không cho phép. Còn lại
đội màu chủ đạo của Cubase là `h = 210` (214/337 màu), tức xanh lam.

**Cách lách động đối**: mọi màu sửa đều **giữ nguyên `h = 210`** và chỉ đổi `s`/`l`.
Nhờ vậy kết quả nằm đúng trong sắc xanh lam sẵn có của Cubase, không phụ thuộc vào
việc mình hiểu đúng thang chia hay không.

### 11.2 Năm id đã đổi

Màu sóng trong Project Window lấy chính là màu nền event — `eventBackDefault`
(vì vậy sáng màu này thì cả event sáng theo).

| id | gốc | mới | RGB gốc → mới |
|---|---|---|---|
| `eventBackDefault` | `$210,020,070` | `$210,080,100` | `(65,70,75)` → `(69,100,131)` |
| `eventBackMuted` | `$210,010,095` | `$210,016,125` | `(91,95,99)` → `(117,125,133)` |
| `eventWaveMuted` | `$210,005,090` | `$210,010,120` | `(88,90,92)` → `(115,120,125)` |
| `eventWaveAutomFill` | `$210,015,090` | `$210,080,100` | `(85,90,95)` → `(69,100,131)` |
| `eventWaveAutomLine` | `$210,015,075` | `$210,080,100` | `(71,75,79)` → `(69,100,131)` |

Hai dòng cuối **đặt bằng `eventBackDefault`**: đó là lớp phủ đường volume, đặt
cùng màu nền thì nó **biến mất bất kể pref nào đang bật** — không phụ thuộc
*Show Event Volume Curves Always*. Chênh lệch `l` của hai trạng thái muted được
giữ đúng như skin gốc (`backMuted = backDefault + 25`, `waveMuted = backDefault + 20`)
nên event bị mute vẫn nhạt hơn event thường như thiết kế.

`tools/make_fl_skin.py` sinh ra bộ này, có 3 mức:

```powershell
python tools\make_fl_skin.py --level nhe               # ghi ra file rieng
python tools\make_fl_skin.py --level vua               # mac dinh
python tools\make_fl_skin.py --level manh              # mau dam, gan look FL
python tools\make_fl_skin.py --level vua --install     # sao luu roi ghi de skin.srf
```

**Đã ghi đè `skin.srf`** — Cubase 15 không hiện skin tách riêng trong danh sách
nên phải thay thẳng. `--install` làm đúng thứ tự an toàn:

1. từ chối chạy nếu `Cubase15.exe` đang mở (Cubase ghi đè skin lúc thoát),
2. `shutil.copy2` ra `skin.srf.bak-<giờ>` — giữ nguyên mtime của bản gốc,
3. đọc ngược từ **bản sao lưu** và so với bản gốc; lệch thì dừng trước khi sửa,
4. mới ghi đè, rồi đọc ngược 5 giá trị từ chính `skin.srf`; sai thì tự khôi phục.

Trạng thái sau khi ghi đè:

```
skin.srf                    20,292,172   md5 c6207cdcc75fd2c3adff69ccbb854b23
skin.srf.bak-20260930-105046 20,292,176  md5 7c0433c59aebbb905f6543b24f0d318d
```

Kiểm chứng độc lập:

- đọc lại cả 5 giá trị từ `skin.srf` — đều khớp,
- bảng tra cứu **49.865 byte cuối file giống hệt** bản gốc,
- **842 member** ở cả hai, chỉ member #82 khác payload.

**Cách trả lại bản gốc**:

```powershell
Copy-Item "E:\Steinberg\Cubase 15\Skins\skin.srf.bak-20260930-105046" `
          "E:\Steinberg\Cubase 15\Skins\skin.srf" -Force
```

### 11.3 Ba pref đã đổi

Nằm trong `%APPDATA%\Steinberg\Cubase 15_64\UserPreferences.xml`, nhóm `PAudioImage`
(16 giá trị). Trên máy này:

| pref id | gốc | mới | ý nghĩa |
|---|---|---|---|
| `Show Volume Curves Always` | `1` | **`0`** | tắt lớp đường volume bị ép hiện |
| `Wave Brightness` | `-25` | **`0`** | bỏ độ tối mặc định, để skin lo độ sáng |
| `Wave Outline Intensity` | `15` | **`45`** | viền sáng hơn gấp 3 |

Đổi bằng `tools/set_prefs.py`, có sao lưu đóng dấu thời gian và tự kiểm:

```powershell
python tools\set_prefs.py --list PAudioImage
python tools\set_prefs.py --group PAudioImage --set "Show Volume Curves Always=0"
```

Hai bẫy đã vấp, đã xử lý trong công cụ:

1. **Cubase ghi đè toàn bộ file khi thoát** — sửa lúc nó đang chạy là vô nghĩa.
   Script kiểm tra tiến trình và từ chối nếu Cubase đang mở.
2. **File không có `DOCTYPE` nhưng vẫn dùng entity HTML** (`&aacute;`), nên
   `xml.etree` báo `undefined entity` **trên chính file gốc**. Script vì thế không
   parse XML mà so sánh **theo dòng**: chỉ những dòng `<int .../>` đã định sửa được
   phép khác, sai là tự khôi phục bản gốc.

Ngoài ra: tên khoá trong file **không nhất quán** — cùng nhóm vừa có khoá tiếng Anh
(`Wave Brightness`) vừa có khoá đã dịch (`Hiển Fade`, `Hiển Fades`). Tức tên khoá
phụ thuộc bản dịch đang nạp, và đổi bản dịch có thể làm một pref rơi về mặc định.

### 11.4 Việc còn lại

- Khởi động lại Cubase để nạp skin mới (skin được đọc lúc khởi động).
- Hai giá trị pref ở §11.3 là **con trượt trong GUI** — nếu thấy chưa đúng thì kéo
  lại chứ không cần sửa file.
- Muốn mạnh hơn hoặc dịu hơn: `python tools\make_fl_skin.py --level manh --install`
  (lần sau nó sẽ tự tạo thêm một bản sao lưu nữa).
- Chưa đối chiếu bằng ảnh thật, vì Cubase không chạy được tự động trên máy này
  (xem `docs/RESEARCH.md`). Phần còn lại của tính năng — **màu theo băng** — cần
  DLL hook, và **§12** ghi lại chỗ hook đúng (không phải `0x141E9E140` như dòng
  này từng nói).

Ghi chú về phía FL: `WaveformColouring.vmt[0x20](rcx=analyser, rdx=range, r8,
r9=bool, &obj[0x20])` ghi ra 6 float = **2 màu, mỗi màu RGB** — đây là công thức
băng→màu thật của FL. Nó được gọi qua vtable nên không tra được bằng xref tĩnh; phải
đi qua bảng tra "tên → hàm" (`RVA 0x26EA70`), mà bảng đó khoá theo id/hash chứ
không theo tên.

`WaveformColouring.vmt[0x20](rcx=analyser, rdx=range, r8, r9=bool, &obj[0x20])` —
ghi ra 6 float = **2 màu, mỗi màu RGB**. Đây là công thức băng→màu thật. Nó được
gọi qua vtable nên không tra được bằng xref tĩnh; phải đi qua bảng tra "tên → hàm"
(`RVA 0x26EA70`), mà bảng đó khoá theo id/hash chứ không theo tên.

---

## 12. Chuỗi tô dải sóng của Cubase — và chỗ hook đúng

§11.4 từng nói còn cần hook `0x141E9E140`. **Chỗ đó sai**: đó là *hàm vẽ*, hook vào
đó thì chỉ đếm được lời gọi, không sửa được gì. Vòng này dò lại từ đầu và tìm
được lệnh tô thật.

### 12.1 Chuỗi đầy đủ

```
0x141E9B6F0  điều phối            chọn thuật toán theo framesPerPixel   (§3 WAVEFORM.md)
0x141E9C340  gom min/max          ra mảng 8 byte / cột
0x141E9E140  hàm vẽ event         quy đổi sang toạ độ màn hình, rồi gọi lệnh tô 4 lần
0x141E9AD10  LỆNH TÔ             dựng path rồi rasterise 2 lần          <-- chỗ hook
0x141EA8150  hỏi pen + style     lấy trục, số điểm, biên
0x141EA58C0  dựng path           đọc mảng điểm, tạo đa giác
0x141EA7840  RASTERISER           1.844 byte, khung stack 0x3328         <-- nơi ghi pixel
0x141EA7F80  cắt / kiểm tra      đọc [style + 0x90] so 0
```

Điểm mấu chốt ở `0x141EA7840`: khung stack **0x3328 byte (13 KB)** và thân hàm
1.844 byte. Đó **không** phải lời gọi GDI/Direct2D — **Cubase tự rasterise** dải
sóng trong phần mềm. Nghĩa là màu cuối cùng được ghi bên trong hàm này, không đi
qua hệ đồ hoạ.

### 12.2 Chữ ký của `0x141E9AD10` — đã đặt tên được cả 6 tham số

Frame của `0x141E9E140` **không** dùng frame pointer chuẩn:

```
mov  rax, rsp
mov  [rax+8], rcx      ; arg1
mov  [rax+0x10], rdx   ; arg2
mov  [rax+0x18], r8    ; arg3
mov  [rax+0x20], r9    ; arg4
push rbp,rbx,rsi,rdi,r12,r13,r14,r15          ; 8 lần
lea  rbp, [rax - 0x138]
sub  rsp, 0x1f8
```

Nên tham số của chính nó nằm ở `rbp + 0x140` trở đi — 8 tham số:

| rbp | tham số | tên tìm được | bằng chứng |
|---|---|---|---|
| `+0x140` | arg1 | thiết bị vẽ | hàm tự deref `[rcx+0x18]` rồi gọi `vfunc+0x38` |
| `+0x148` | arg2 | — | truyền làm `this` cho `0x141EA3DC0` |
| `+0x150` | arg3 | bút / ngữ cảnh vẽ | `0x141EA8150(pen, style, …)` |
| `+0x158` | arg4 | **đối tượng style** | có bitfield ở `+0xB0` |
| `+0x160` | arg5 | **mảng đích** (y toạ độ màn hình) | vòng lặp ghi `[rbx]`, `[rbx+4]`, `rbx += 8` |
| `+0x168` | arg6 | **mảng nguồn** (min/max thô) | vòng lặp đọc `[rdi]`, `[rdi+4]`, `rdi += 8` |

Và `0x141E9AD10` nhận:

| tham số | nội dung |
|---|---|
| `rcx` | thiết bị vẽ |
| `rdx` | ngữ cảnh nét |
| `r8` | bút / ngữ cảnh |
| `r9` | **mảng điểm** — chỗ sửa được hình dạng |
| `[rsp+0x20]` (arg5) | **cờ, luôn = 1** |
| `[rsp+0x28]` (arg6) | **đối tượng style** — chỗ sửa được màu |

Đối tượng style đọc được ở: `+0x90` (double), `+0x98` (double, truyền vào
`0x141EA58C0`), `+0xA8` (con trỏ, so với null), `+0xB0` (bitfield).

### 12.3 Bốn lần gọi — phân biệt bằng gì

Cả bốn đều truyền `arg5 = 1`, cùng `arg1/arg2/arg3`. Chúng khác ở **arg4** và
**arg6**:

| chỗ gọi | arg4 (mảng điểm) | arg6 (style) |
|---|---|---|
| `0x141E9E44C` | `rbx` = mảng đích (arg5) | `[rbp+0x158]` — **style gốc, chưa sửa** |
| `0x141E9E4BC` | `[rsp+0x38]` = mảng đích | `&[rbp-0x10]` — bản sao đã sửa |
| `0x141E9E649` | `[rbp+0x160]` = mảng đích | `&[rbp-0x10]` |
| `0x141E9E75A` | `[rbp+0x168]` = **mảng nguồn** | `&[rbp-0x10]` |

Bản sao ở `[rbp-0x10]` do `0x141EA23D0(&local, [rbp+0x158])` dựng ra, gọi trước
chỗ 2, 3, 4. Bit 7 của `style->0xB0` chọn giữa chỗ 1 và chỗ 2
(`shr eax,7; test al,1` ở `0x141E9E41A`).

**Cách lọc đáng tin cậy:** chỗ 1 là chỗ dùng **đúng con trỏ style mà hàm vẽ nhận
vào**. Nên:

> Ghi lại `arg4` (r9) của `0x141E9E140` khi vào hàm — thứ đã hook sẵn — rồi trong
> hook của `0x141E9AD10` so `arg6` với giá trị đó. Khớp ⇒ đây là lớt dải sóng
> chính. Không cần đoán theo địa chỉ stack.

### 12.4 Đính chính: `arg5` **không** phải số cột

Tôi đoán `arg5` là số cột. Sai. Cả bốn chỗ gọi đều truyền `1`, và hàm dùng nó
để tính kích thước buffer nội bộ:

```
esi = arg5
eax = esi + 0xA          ; +10
lea rsi, [rax*8]         ; (arg5 + 10) * 8 byte
memset(buf, 0, rsi)      ; 0x144CF0872
```

Tức nó là **số phần / cờ**, và 1 nghĩa là "một path". Số điểm thật lấy từ
`0x141EA8150(pen, style, &out)` — hỏi pen ra, rồi đưa vào `0x141EA58C0` qua
`r8d`/`r9d`. Nếu hook muốn biết có bao nhiêu điểm thì phải đọc kết quả của
`0x141EA8150`, không phải đếm mảng.

### 12.5 Vì sao hook `0x141E9AD10` thay vì `0x141E9E140`

1. `0x141E9E140` tự tính rồi tự tô — muốn đổi kết quả thì phải làm lại 1.765 byte.
2. `0x141E9AD10` **nhận thẳng mảng điểm** (hình dạng) và **đối tượng style**
   (màu). Sửa trước khi tô thì xong.
3. Nó có 7 caller, còn 3 caller kia (`0x1E9A790`, `0x1E9AAA0`, `0x1E9B100`) là các
   lớp tô khác dùng lại đúng lệnh này — nên **phải lọc theo §12.3**. Hook chỗ
   gọi thì chính xác hơn nhưng phải làm 4 hook.

### 12.6 Đi tận chỗ ghi pixel — và tại sao không có lệnh đó

Câu hỏi tự nhiên: chỗ ghi pixel nằm ở đâu. Câu trả lời: **không tồn tại trong
`Cubase15.exe`** — và đây là kết quả, không phải chỗ chưa dò.

Đo bằng cách liệt kê **mọi** lệnh ghi bộ nhớ có đích không phải `rbp`/`rsp`, trong
cả hai hàm:

| hàm | kích thước | lệnh ghi ra ngoài stack |
|---|---|---|
| `0x141EA7840` rasteriser | 1.844 byte, khung `0x3328` | **đúng một**: `0x141EA7A87` `mov [rcx],eax` + `0x141EA7A89` `movss [rcx+4],xmm0` |
| `0x141E9D010` flush | 756 byte | **không có** |

Lệnh duy nhất kia ghi 8 byte — một đỉnh (x nguyên, y thực) — vào bảng cạnh. Tức
`0x141EA7840` **không** tô, nó chỉ dựng bảng cạnh trong 13 KB stack của chính nó.

Lời gọi cuối cùng là **gọi ảo**:

```
0x141E9D04F  test byte ptr [r8 + 0xB0], 1        ; style, bit 0
0x141E9D066  lea  rdx, [r8 + 0x50]               ; &style->paint
0x141E9D074  call 0x144A958D0                    ; dựng paint 13 byte từ đó
0x141E9D05C  mov  rax, [rcx]                     ; vtable của thiết bị
0x141E9D05F  mov  rbx, [rax + 0x80]
0x141E9D081  call rbx                            ; <-- chạm framebuffer
```

`0x144A958D0` chỉ 59 byte: chép 8 byte đầu của `style+0x50` vào `local+0`, ghi
`1` vào `local+8`, ghi cờ vào `local+0xC`. Rồi đưa `&local` cho
`device->vfunc+0x80`.

Nên chuỗi thật là:

```
0x141E9AD10   lệnh tô
 ├─ 0x141EA58C0  dựng path từ mảng điểm
 ├─ 0x141EA7840  dựng bảng cạnh (stack 13 KB)      <- không tô
 ├─ 0x141E9D010  dựng paint từ style+0x50
 │    └─ device->vfunc+0x80(device, &paint)        <- LỜI GỌI CUỐI
 └─ 0x141EA7F80  cắt / kiểm tra
```

**Hệ quả thực tế:** đừng tìm lệnh ghi pixel nữa — không có. Muốn biết chỗ ghi thật
thì phải biết lớp thiết bị nào cài `vfunc+0x80`, và cái đó **chỉ biết lúc chạy**.
Đúng công cụ cho việc đó là bộ dò đã có sẵn: `hook/waveprobe.c` (phần đầu file ghi
rõ: gắn hook vào mọi hàm có prologue 15 byte an toàn rồi xem cái nào chạy khi
Cubase vẽ dải sóng). Đó là cách duy nhất đóng được nốt câu hỏi này.

**Chỗ hook thực dụng** do đó là hai chỗ tra tĩnh được:

| chỗ | sửa được gì |
|---|---|
| `0x141E9AD10` vào hàm | mảng điểm (hình dạng) + các trường của style |
| `0x141E9D010` vào hàm | `style+0x50` — thứ sắp được đưa cho thiết bị |

Với màu, `style+0x50` là ứng viên đầu tiên: nó là thứ duy nhất đi thẳng tay vào
lời gọi cuối.

### 12.7 Bẫy phần cứng: kiểm tra xong, và nó **không** thành hiện thực

Cần cảnh báo trước khi đặt kỳ vọng vào `uint32_t* pixels`. Đã kiểm, và kết
luận ngược với dự đoán: **dải sóng của Cubase 15 vẽ trên CPU, qua GDI**, không
phải texture GPU.

Bằng chứng, từ bảng import của `Cubase15.exe` (79 DLL):

| DLL | số hàm | ý nghĩa |
|---|---|---|
| `GDI32.dll` | 20 | `CreateCompatibleDC`, `CreateCompatibleBitmap`, `BitBlt`, `SelectObject`, `CreateSolidBrush`, `GetDeviceCaps`, `DeleteDC`… |
| `dxgi.dll` | 1 | chỉ `CreateDXGIFactory1` — dò độ phân giải, không phải vẽ |
| `dwmapi.dll` | 4 | `DwmFlush`, `DwmSetWindowAttribute` — hiệu ứng cửa sổ |
| `d2d1.dll` | **0** | — |
| `d3d11.dll` | **0** | — |
| `dwrite.dll` | **0** | — |
| `gdiplus.dll` | **0** | — |

`CreateCompatibleDC` + `CreateCompatibleBitmap` + `BitBlt` là mẫu kinh điển: dựng
trong DC ảo, rồi chép sang cửa sổ. Không có `StretchDIBits` / `CreateDIBSection`
cũng nghĩa là không có đường nào để lấy con trỏ pixel tĩnh — **GDI giữ bitmap
trong bộ nhớ hệ thống**, không phải heap của tiến trình.

Ngoài ra, trong toàn bộ `Cubase15.exe` **không có chuỗi nào** chứa `d2d1.dll`,
`D3D11`, `ID2D1DeviceContext`, `D2D1CreateDeviceContext`, `opengl32`, `vulkan`. Vậy
không phải chuyện gọi `LoadLibrary` động.

Có một DLL tên đáng ngờ: `graphics2d.dll` (2.5 MB) **có** import cả `d2d1.dll`
`d3d11.dll` `DWrite.dll` `gdiplus.dll`. Nhưng nó không export gì liên quan
(2 export), và không hề có chuỗi `ID2D1RenderTarget` / `CreateRenderTarget`. Đường
dẫn nguồn PDB cho thấy nó thuộc `lib.graphics2d\win\x64` — lớp vẽ 2D dùng chung,
**không phải** đường đi của dải sóng. Đường tôi đã lần theo (§12.1) nằm trọn
trong `Cubase15.exe` và kết thúc ở GDI.

**Hệ quả cho "Mức 3":** không có `uint32_t* pixels` để `memcpy`, nhưng cũng không
bị chặn. Nếu vẽ bằng GDI thì đường tự nhiên là `GetDC` cửa sổ → vẽ đè bằng
primitive của GDI (`Rectangle`, `MoveToEx`/`LineTo`, `Polyline`) → `ReleaseDC`.
Đó là đường ngắn nhất, và nó cho anti-aliasing/clipping của chính hệ thống.

### 12.8 Đã dựng xong: bộ probe đọc vtable của device

`0x141E9D010` lấy vtable bằng **gọi ảo trả về**, không phải hằng số trong `.rdata`:

```
0x141EAD690  mov  rax, [rbx]              ; vtable cua mot doi tuong khac
0x141EAD698  call [rax + 0x2B8]          ; -> tra ve vtable cua device
0x141EAD69E  mov  [rbp - 0x30], rax
   ...
0x141EAE165  mov  [rbp + 0x110], rax     ; gan vao dau struct device
```

Nên **không** dò được bằng cách quét `.rdata`: phải chạy. Đã dựng bộ probe:

| việc | ở đâu |
|---|---|
| nhận `dev` (đã có sẵn trong stub ASM, truyền `rcx` vào `WaveDrawHook_C`) | `hook/wavehook.h`, `hook/wavehook.c` |
| xuất 24 slot đầu + 8 trường đầu, kèm **tên module chứa con trỏ** | `probe_device()` |
| tự ghi ra `%TEMP%\waveprobe.txt` | `probe_flush_file()` |
| lệnh đọc | `python tools\inject_wavehook.py devdump` |
| build | `hook\build.bat release wavehook4.dll` (đã build, 142.848 byte) |

Hai điều cố ý trong cách làm:

- **Mọi phép đọc bọc `__try`.** Con trỏ màu có thể chưa khởi tạo, và một lỗi đọc
  sẽ làm Cubase crash — đúng cái giá đã trả ở §13.1. Ở đây bảo vệ là bắt buộc,
  không phải phòng tránh.
- **Chỉ ghi một lần.** Ham vẽ chạy trên luồng Cubase, mỗi phép I/O đều làm luồng
  đó nghẽn. Một lần thì không đáng kể.

Điều kiện để chạy thật: **Cubase phải vẽ một dải sóng**. Dự án `demo1.cpr` trên máy
này (`D:\01_Music_Projects\Cubase\`) **có** audio — 19 file `.peak` trong `Images\`
nên chắc chắn nó sẽ vẽ dải sóng khi mở. Thiếu duy nhất là một phiên desktop có
input thật: session agent hiện tại gửi input không tới app (xem
`docs/RESEARCH.md`), nên không tự mở dự án được.

Nên khi có phiên desktop:

```powershell
# 1. mo Cubase, File > Open Project... > D:\01_Music_Projects\Cubase\demo1.cpr
# 2. dam bao Project Window hien mot event audio (keo track cao mot chút)
python tools\inject_wavehook.py load --dll hook\wavehook4.dll
python tools\inject_wavehook.py devdump
```

`devdump` in ra 24 slot vtable kèm **tên module** của từng con trỏ, nên nhìn là biết
slot `+0x80` rơi vào `Cubase15.exe` hay DLL khác — tức là trả lời ngay câu hỏi
"CPU hay GPU" ở §12.7 bằng dữ kiện chứ không phải suy luận.

`tools\inject_wavehook.py status` kiểm tra hook đã vào chưa (đọc 15 byte đầu hàm
và tìm mẫu `49 BB ... 41 FF E3`), `calls` xem `g_callCount` đã đếm được bao nhiêu
lần vẽ.

### 12.9 Trình tự nên làm

1. Mở một dự án có audio, rồi chạy
   `python tools\inject_wavehook.py devdump`. Phần đang chờ nằm ở §12.8.
2. Từ vtable thu được, xác định slot nào là `QueryInterface` / `AddRef` /
   `Release`, và slot `+0x80` rơi vào module nào — trong `Cubase15.exe` hay
   `graphics2d.dll`. Kết quả này quyết định Mức 3 đi đường GDI hay cần thêm bước.
3. Chuyển hook sang `0x141E9AD10`, chỉ sửa **màu**: in ra `style+0x50` cùng `+0x90`,
   `+0x98`, `+0xA8`, `+0xB0` cho vài event khác nhau, xem cái nào đổi theo màu
   track. Đó là ứng viên màu.
4. Xác nhận bằng cách đếm số lần tô trên một event.
5. Mới động tới hình dạng — sửa mảng điểm.

Bỏ qua bước 1–2 thì mọi thứ vẽ sau đó đều sai, mà lỗi loại này Cubase không báo
gì — chỉ vẽ ra sai màu, rất khó phát hiện là do hook.
