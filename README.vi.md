# cubase-vi — Giao diện tiếng Việt cho Cubase 15

**English: see [README.md](README.md).**

![Cubase 15 với giao diện tiếng Việt](demo.png)

## Vì sao nên dùng?

Học Cubase đã khó, học bằng tiếng Anh càng khó. Mấy menu kiểu
`Direct Offline Processing` hay `Retrospective Record` đủ làm người mới
nản trước khi bấm được nốt nào.

Bản dịch này giải quyết đúng chuyện đó:

- Nút bấm, hộp thoại, cảnh báo: tiếng Việt.
- Thuật ngữ nghề: tiếng Anh (`Cycle`, `Quantize`, `Side-Chain`) để xem
  tutorial YouTube vẫn khớp từng chữ trên màn hình.
- Dịch hết 10.737 chuỗi, cả Score Editor. Không có chỗ nào đang dùng
  rớt về tiếng Anh giữa chừng.
- Một file XML Cubase tự đọc. Gỡ ra là mọi thứ về như cũ.

Cubase không có bản tiếng Việt. Chuỗi giao diện của nó không nằm trong
binary mã hoá. Nó là file XML văn bản thuần (`TRANSLATION.XML`), và Cubase
đọc `translation.xml` trên đĩa trước rồi mới tới bản nhúng trong
`Cubase15.exe`. Repo này chỉ làm một việc: đặt đúng file vào đúng chỗ.
Không vá víu gì cả.

Cách dịch cũng cố tình pha hai thứ tiếng. Từ thường ngày viết tiếng Việt,
thuật ngữ nghề giữ tiếng Anh để còn tra được hướng dẫn
(`Bật Cycle`, `Chế độ Absolute`, `Triads`). Mỗi chỗ chọn một kiểu đều có
luật ghi trong [`AGENT.md`](AGENT.md), máy kiểm tra chứ không nói miệng.

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
