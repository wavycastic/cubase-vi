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
| **Đã dịch sang `vi`** | **707** |
| Còn lại | tự động rơi về tiếng Anh — không hiện chữ trống |

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

Bảng dịch khoá theo **chuỗi tiếng Anh** (`"File": "Tệp"`) vì 97% `String Key`
trùng bản gốc. Tra chuỗi cần dịch trong `keys/all_strings.tsv`;
`tools/suggest_keys.py` giúp khi bạn đoán sai tên.

> JSON không cho key trùng (cái sau ghi đè cái trước, không cảnh báo).
> Chạy `python tools\merge_maps.py --check` trước khi commit.

## Yêu cầu

- Python 3.10+ (chỉ dùng thư viện chuẩn)
- `tools/research/disasm.py` cần `pip install capstone` — chỉ dùng khi nghiên cứu lại
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
