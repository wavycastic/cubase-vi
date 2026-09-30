# Cubase Vietnamese (`cubase-vi`)

Giao diện tiếng Việt cho Cubase 15.

Steinberg không phát hành bản dịch tiếng Việt. Nhưng chuỗi giao diện của
Cubase **không nằm trong binary đã mã hoá** — nó là **XML văn bản thuần**,
và chương trình chủ động đọc file `translation.xml` từ đĩa *trước khi* dùng bản
nhúng trong `Cubase15.exe`. Repo này khai thác đúng cơ chế đó: **không cần vá
file thực thi.**

Kiểu dịch: **lai tiếng Anh – tiếng Việt** (`Thiết bị (Devices)`), thuật ngữ
kỹ thuật giữ nguyên tiếng Anh để tra được video hướng dẫn. Quy tắc bắt buộc ở
[`AGENT.md`](AGENT.md).

Chi tiết kỹ thuật: [`docs/RESEARCH.md`](docs/RESEARCH.md)

---

## Dùng nhanh

```powershell
# 1. build (trích chuỗi từ exe -> dịch -> đóng gói)
python tools\build.py "E:\Steinberg\Cubase 15\Cubase15.exe"

# 2. cài (tự backup file cũ)
powershell -File scripts\install.ps1 -Action install

# 3. mở Cubase -> Edit > Preferences > General > Language -> Vietnamese -> restart
```

Gỡ lại: `powershell -File scripts\install.ps1 -Action uninstall`

## Trạng thái

| | |
|---|---|
| Chuỗi trong bảng gốc | 10.737 |
| Ngôn ngữ gốc | 9 (`us de fr es it pt jp zh ru`) |
| **Đã dịch sang `vi`** | **10.737 (100% Hoàn tất toàn bộ Cubase 15)** |
| Còn lại | **0 chuỗi** — Đạt độ phủ 100% toàn bộ phần mềm |

## Bố cục

```
translations/vi.json          bản dịch hợp nhất - nguồn sự thật duy nhất
translations/batches/*.json   các lô dịch, gộp bằng tools/merge_maps.py
translations/unmatched.json   các key đoán sai, đã tách ra (tools/prune_map.py)
AGENT.md                      quy tắc bắt buộc: dịch LAI Anh-Việt, không dịch thuần Việt
keys/all_strings.tsv          10.737 chuỗi: key <-> tiếng Anh (tham chiếu, đã commit)
build/                        output (gitignored)
tools/build.py                pipeline: extract -> list -> merge -> build -> validate
tools/extract_translation.py  lấy TRANSLATION.XML ra khỏi Cubase15.exe
tools/list_strings.py         xuất key <-> tiếng Anh ra TSV
tools/build_translation.py    chèn <language key="vi"> + <vi> vào từng chuỗi
tools/validate_translation.py kiểm tra XML + đếm số chuỗi đã dịch
tools/merge_maps.py           gộp các lô dịch (--check để CI)
tools/prune_map.py            tách key đoán sai khỏi vi.json và khỏi các lô dịch
tools/worklist.py             danh sách chuỗi chưa dịch, ưu tiên theo nhóm
tools/suggest_keys.py         gợi ý key thật khi tên bạn đoán không khớp
tools/check_dups.py           phát hiện key trùng trong JSON
tools/check_style.py          cưỡng chế AGENT.md: mỗi giá trị phải là "<Vi> (<key>)" hoặc đúng key
tools/audit_clarity.py        tìm chỗ DÀI và chỗ KHÓ ĐỌC (vòng 81 trở đi)
tools/audit_bloat.py          tìm chỗ tiếng Việt dài hơn tiếng Anh không cần thiết
tools/cubelib/                thư viện dùng chung cho toàn bộ công cụ
tools/tests/                  test cho cubelib (chạy được, không cần Cubase)
tools/research/               công cụ RE dùng để tìm ra cơ chế (xem RESEARCH.md)
scripts/install.ps1           install / uninstall / status
```

## Thêm bản dịch

```powershell
# xem những gì còn thiếu, ưu tiên nhãn ngắn
python tools\worklist.py A 200

# sửa translations/batches/<ten>.json rồi:
python tools\merge_maps.py                # gộp -> vi.json
python tools\build.py                     # build lại
powershell -File scripts\install.ps1 -Action install
```

## Rà lại độ dễ đọc

Độ phủ 100% không có nghĩa là dễ đọc. Hai loại lỗi hay gặp nhất:

```powershell
python tools\audit_clarity.py             # [A] dài, [B] khó đọc
python tools\audit_clarity.py --list A    # xem chuỗi dài nhất
python tools\audit_clarity.py --list B    # xem chỗ khó đọc nhất
python tools\audit_bloat.py               # VI dài hơn EN không cần thiết
```

- **[A] Dài** — quá ~78 ký tự thì nhãn Cubase bị xuống dòng hoặc cắt.
- **[B] Khó đọc** — tiếng Việt đúng ngữ pháp nhưng nhiều danh từ dính liền
  nhau, hoặc còn tiếng Anh trần. Hai loại lỗi này **không sai**, chỉ mệt mắt,
  nên phải đọc tay chứ audit tự động không bắt được.

Sửa xong thì ghi vào một script `fix_readingNN.py` (mẫu: `fix_reading81.py`)
để có thể chạy lại và xem trước thay đổi.

Bảng dịch khoá theo **chuỗi tiếng Anh** (`"File": "Tệp"`) vì 97% `String Key`
trùng bản gốc. Tra chuỗi cần dịch trong `keys/all_strings.tsv`;
`tools/suggest_keys.py` giúp khi bạn đoán sai tên.

> JSON không cho key trùng (cái sau ghi đè cái trước, không cảnh báo).
> Chạy `python tools\merge_maps.py --check` trước khi commit.

## Toolchain RE

Mọi công cụ nghiên cứu dùng chung `tools/cubelib/`:

| | |
|---|---|
| `cubelib/binary.py` | mmap, tìm chuỗi mọi encoding, hexdump |
| `cubelib/pe.py` | PE32/PE32+: section, RVA↔offset, resource, **`.pdata` = biên hàm thật** |
| `cubelib/x86.py` | disasm theo biên hàm + xref đã verify bằng capstone |
| `cubelib/qm.py` | đọc catalogue Qt `.qm` (Score Editor) |
| `cubelib/srf.py` | giải nén `skin.srf` (toàn bộ theme Cubase) |
| `cubelib/cubase.py` | đường dẫn Cubase, ngôn ngữ, tên resource |

```powershell
python tools\research\pe_info.py "E:\Steinberg\Cubase 15\Cubase15.exe" --find TRANSLATION.XML
python tools\research\xref.py ScoringEngine.dll 0x4FAEBF0
python tools\research\qm_dump.py "...\ScoringEngine\l10n"
python tools\research\skin_srf.py "...\Skins\skin.srf" --templates
python tools\research\scoring_l10n.py --diff en de
```

**Xref đã verify.** Bản cũ quét byte thô nên vừa bỏ sót (chỉ nhận REX prefix)
vừa báo nhầm. Bản này lấy danh sách hàm từ `.pdata`, lọc thô rồi để capstone
xác nhận từng hit — `ScoringEngine.dll` có 346.830 hàm, quét mất vài giây.

## Yêu cầu

- Python 3.10+
- **Pipeline dịch: chỉ thư viện chuẩn.** Không cần cài gì thêm.
- **Công cụ RE:** `pip install -r requirements-dev.txt` (capstone). Thiếu thì các
  script đó in hướng dẫn cài, phần còn lại vẫn chạy.
- Test: `python tools\tests\run.py` — 70 test, **không cần Cubase, không cần capstone**
- Cubase phải **đóng hẳn** trước khi deploy

## Lưu ý

Bản dịch này là **bổ sung giao diện cho máy của bạn**, không đụng tới bản quyền
hay cơ chế bảo vệ của Cubase.

`keys/all_strings.tsv` là **nội dung của Steinberg** (trích từ `Cubase15.exe`),
được commit **có chủ đích** làm bảng tham chiếu. Xem [`NOTICE.md`](NOTICE.md).
Bản XML gốc 4,65 MB chứa cả 9 bản dịch của họ thì **không** commit —
`tools/build.py` tái tạo từ bản Cubase trên máy bạn.

Steinberg đã phát hành 9 ngôn ngữ cho Cubase. Nếu họ từng bổ sung tiếng Việt
chính thức, hãy dùng bản đó.
