# cubase-vi — Giao diện tiếng Việt cho Cubase 15

**English: see [README.md](README.md).**

![Cubase 15 với giao diện tiếng Việt](demo.png)

## Vì sao nên dùng?

Cubase rất mạnh nhưng nổi tiếng khó học — mà học bằng tiếng Anh thì dốc
gấp đôi. Những menu như `Direct Offline Processing`,
`Retrospective Record` hay `VCA Faders` chặn người mới từ trước khi đụng
tới nhạc.

Bản dịch này phá rào cản ngôn ngữ mà không làm mất chất chuyên nghiệp:

- Giao diện thường ngày đọc tiếng Việt: nút bấm, hộp thoại, cảnh báo.
- Thuật ngữ giữ tiếng Anh (`Cycle`, `Quantize`, `Side-Chain`) nên mọi
  tutorial trên YouTube vẫn khớp từng chữ trên màn hình.
- Phủ kín: cả 10.737 chuỗi kể cả Score Editor — không đang làm dở chừng
  rớt về tiếng Anh.
- Không crack, không vá: một file XML thuần mà chính Cubase ưu tiên đọc.
  Gỡ là về nguyên bản bằng một lệnh.

Cubase không có bản tiếng Việt. Chuỗi giao diện của nó không nằm trong
binary mã hoá — mà là **XML văn bản thuần** (`TRANSLATION.XML`), và Cubase
đọc `translation.xml` từ đĩa **trước khi** dùng bản nhúng trong
`Cubase15.exe`. Repo này khai thác đúng cơ chế đó: chép file vào là chạy,
**không cần vá file thực thi.**

Kiểu dịch **lai Anh–Việt**: từ thường dịch tiếng Việt, thuật ngữ DAW giữ
nguyên tiếng Anh để tra được video hướng dẫn (`Bật Cycle`,
`Chế độ Absolute`, `Triads`). Quy tắc bắt buộc — xem [`AGENT.md`](AGENT.md).

| | |
|---|---|
| Chuỗi | 10.737 |
| Ngôn ngữ gốc để đối chiếu | 9 (`us de fr es it pt jp zh ru`) |
| Đã dịch | **10.737 (100%)** |
| Test | full suite, pass hết |

## Dùng nhanh

```powershell
# dịch: sửa batch, rồi gộp -> kiểm tra -> build -> test
notepad translations\batches\round_NNN.json
python tools\merge_maps.py
python tools\build.py style
python tools\build.py punct
python tools\tests\run.py

# cài (tự backup file cũ)
powershell -ExecutionPolicy Bypass -File scripts\install.ps1 -Variant full

# trong Cubase: Edit > Preferences > General > Language > Vietnamese > restart
```

## Bố cục

```
translations/vi.json            bản dịch hợp nhất — nguồn sự thật duy nhất
translations/batches/*.json     mỗi vòng sửa là một file batch (số tiếp theo)
keys/all_strings.tsv            10.737 key kèm tiếng Anh gốc (tham chiếu)
tools/read.py                   đọc bảng dịch: page / long / short / inspect
tools/merge_maps.py             gộp batch vào vi.json (--check cho CI)
tools/build.py                  kiểm tra style + dấu câu, đóng gói XML
tools/audit.py                  20+ bộ dò lỗi
tools/dupes.py                  trùng giá trị, trôi số nhiều
tools/family.py                 một thuật ngữ qua mọi anh em
tools/group_by_offset.py        nhóm chuỗi theo vị trí .rdata (63% có nhóm)
tools/clarity.py                chuỗi dài + khó đọc
tools/review_all.xlsx           toàn bảng chuỗi, Anh/Đức/Pháp/Việt song song
tools/tests/run.py              full test, không cần Cubase
scripts/install.ps1             cài / gỡ (-Variant full)
docs/RESEARCH.md                cơ chế loader tìm ra bằng cách nào
docs/OPEN_QUESTIONS.md          thuật ngữ đã chốt
COMMIT_CONVENTION.md            quy định commit: tiếng Anh, theo vòng
AGENT.md                        luật bắt buộc khi dịch
```

## Thêm bản sửa

1. Tìm lỗi: đọc theo thứ tự (`python tools\read.py page 1 100`),
   hoặc tra cứu chuỗi nghi ngờ (`python tools\read.py inspect <key>`).
2. Chốt thuật ngữ theo 9 ngôn ngữ gốc, rồi cả họ thuật ngữ
   (`family.py`), rồi đa số toàn bảng — không bao giờ theo một
   chuỗi đơn lẻ.
3. Ghi `translations/batches/round_NNN.json` (số tiếp theo),
   chạy pipeline trên. Style, punct và full test phải pass hết.
4. Commit theo [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md), push.

Tên trong ngoặc kép phải khớp đúng nhãn của nó (`audit.py quotes`);
`'Stop'` trích dẫn phải viết `'Dừng'` vì nhãn `Stop` là `Dừng`.

## Yêu cầu

- Python 3.10+, chỉ cần thư viện chuẩn, không cài gì thêm.
- Cần Cubase 15 trên máy (build đọc từ bản của bạn).
- Đóng hẳn Cubase trước khi cài.

## Pháp lý

Đây là **bổ sung giao diện cho máy của bạn**, không đụng tới bản quyền
hay cơ chế bảo vệ của Cubase.

`keys/all_strings.tsv` là **nội dung của Steinberg** (trích từ
`Cubase15.exe`), commit có chủ đích làm bảng tham chiếu — xem
[`NOTICE.md`](NOTICE.md). File XML gốc 4,65 MB chứa 9 bản dịch thì
**không** commit — `tools/build.py` tái tạo từ Cubase trên máy bạn.

Nếu Steinberg ra bản tiếng Việt chính thức, hãy dùng bản đó.
