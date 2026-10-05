# cubase-vi — Vietnamese UI for Cubase 15 / Giao diện tiếng Việt cho Cubase 15

Cubase ships no Vietnamese localization. Its UI strings are not compiled
or encrypted — they live in a plain-text XML resource (`TRANSLATION.XML`),
and Cubase reads `translation.xml` from disk **before** falling back to the
copy embedded in `Cubase15.exe`. This repo uses exactly that mechanism:
drop in a file, no executable patching.

Cubase không có bản tiếng Việt. Chuỗi giao diện của nó không nằm trong
binary mã hoá — mà là **XML văn bản thuần** (`TRANSLATION.XML`), và Cubase
đọc `translation.xml` từ đĩa **trước khi** dùng bản nhúng trong
`Cubase15.exe`. Repo này khai thác đúng cơ chế đó: chép file vào là chạy,
**không cần vá file thực thi.**

Translation style is **hybrid English–Vietnamese**: everyday words in
Vietnamese, DAW terms in English so tutorials stay searchable
(`Bật Cycle`, `Chế độ Absolute`, `Triads`). Rules are enforced, not
suggested — see [`AGENT.md`](AGENT.md).

Kiểu dịch **lai Anh–Việt**: từ thường dịch tiếng Việt, thuật ngữ DAW giữ
nguyên tiếng Anh để tra được video hướng dẫn. Quy tắc bắt buộc —
xem [`AGENT.md`](AGENT.md).

| | EN | VI |
|---|---|---|
| Strings | 10,737 | 10.737 chuỗi |
| Source languages | 9 (`us de fr es it pt jp zh ru`) | 9 ngôn ngữ gốc để đối chiếu |
| Translated | **10,737 (100%)** | **10.737 (100%)** |
| Tests | **174 passing** | **174 test, pass hết** |

## Quick start / Dùng nhanh

```powershell
# translate / dịch: edit a batch, then merge -> check -> build -> test
notepad translations\batches\round_222.json
python tools\merge_maps.py
python tools\build.py style
python tools\build.py punct
python tools\tests\run.py

# deploy / cài (backs up the old files automatically / tự backup file cũ)
powershell -ExecutionPolicy Bypass -File scripts\install.ps1 -Variant full

# in Cubase / trong Cubase:
# Edit > Preferences > General > Language > Vietnamese > restart
```

## Layout / Bố cục

```
translations/vi.json            the merged map — the single source of truth
                                bản dịch hợp nhất — nguồn sự thật duy nhất
translations/batches/*.json     one fix batch per round (round_001 ... round_222)
                                mỗi vòng sửa là một file batch
keys/all_strings.tsv            10,737 keys with English source (reference)
                                10.737 key kèm tiếng Anh gốc (tham chiếu)
tools/read.py                   read the map: page / long / short / inspect
                                đọc bảng dịch theo trang / câu dài / nhãn / tra cứu
tools/merge_maps.py             merge batches into vi.json (--check for CI)
                                gộp batch vào vi.json
tools/build.py                  style + punct checks, XML build
                                kiểm tra style + dấu câu, đóng gói XML
tools/audit.py                  20+ defect detectors / 20+ bộ dò lỗi
tools/dupes.py                  duplicate values, plural drift / trùng giá trị, trôi số nhiều
tools/family.py                 one term across all its siblings / một thuật ngữ qua mọi anh em
tools/group_by_offset.py        group strings by .rdata offset (63% covered)
                                nhóm chuỗi theo vị trí .rdata (63% có nhóm)
tools/clarity.py                long + hard-to-read strings / chuỗi dài + khó đọc
tools/review_all.xlsx           all 10,737 strings, EN/DE/FR/VI side by side
                                toàn bảng 10.737 chuỗi, Anh/Đức/Pháp/Việt song song
tools/tests/run.py              174 tests — no Cubase needed / 174 test, không cần Cubase
scripts/install.ps1             install / uninstall (-Variant full) / cài / gỡ
docs/RESEARCH.md                how the loader mechanism was found / cơ chế loader
docs/OPEN_QUESTIONS.md          frozen terminology decisions / thuật ngữ đã chốt
COMMIT_CONVENTION.md            commit messages: English-only, round format
                                quy định commit: tiếng Anh, theo vòng
AGENT.md                        mandatory rules for translation work / luật bắt buộc
```

## Adding a fix / Thêm bản sửa

1. Find the defect: read in order (`python tools\read.py page 1 100`),
   or inspect a suspect (`python tools\read.py inspect <key>`).
   Tìm lỗi: đọc theo thứ tự, hoặc tra cứu chuỗi nghi ngờ.
2. Settle terminology against all 9 source languages, then the term's
   family (`family.py`), then the map majority — never one sibling alone.
   Chốt thuật ngữ theo 9 ngôn ngữ gốc, rồi cả họ thuật ngữ, rồi đa số
   toàn bảng — không bao giờ theo một chuỗi đơn lẻ.
3. Write `translations/batches/round_NNN.json` (next free number),
   run the pipeline above. Style, punct, and all 174 tests must pass.
   Ghi batch mới, chạy pipeline. Style, punct và 174 test phải pass hết.
4. Commit per [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md), push.
   Commit theo quy định, push.

Quoted names must match the label they quote (`audit.py quotes`);
a quoted `'Stop'` reads `'Dừng'` because the `Stop` label is `Dừng`.
Tên trong ngoặc kép phải khớp đúng nhãn của nó; `'Stop'` trích dẫn
phải viết `'Dừng'` vì nhãn `Stop` là `Dừng`.

## Requirements / Yêu cầu

- Python 3.10+, standard library only. No dependencies to install.
  Chỉ cần thư viện chuẩn, không cài gì thêm.
- Cubase 15 installed (the build reads your own copy).
  Cần Cubase 15 trên máy (build đọc từ bản của bạn).
- Close Cubase fully before deploying. Đóng hẳn Cubase trước khi cài.

## Legal / Pháp lý

This is a **UI supplement for your own machine**. It does not touch
Cubase licensing or copy protection.
Đây là **bổ sung giao diện cho máy của bạn**, không đụng tới bản quyền
hay cơ chế bảo vệ của Cubase.

`keys/all_strings.tsv` is **Steinberg's content** (extracted from
`Cubase15.exe`), committed deliberately as a reference table — see
[`NOTICE.md`](NOTICE.md). The 4.65 MB original XML with all 9 vendor
translations is **not** committed; `tools/build.py` rebuilds from the
Cubase on your machine.
`keys/all_strings.tsv` là **nội dung của Steinberg** (trích từ
`Cubase15.exe`), commit có chủ đích làm bảng tham chiếu — xem
[`NOTICE.md`](NOTICE.md). File XML gốc 4,65 MB chứa 9 bản dịch thì
**không** commit — `tools/build.py` tái tạo từ Cubase trên máy bạn.

If Steinberg ever ships official Vietnamese, use theirs.
Nếu Steinberg ra bản tiếng Việt chính thức, hãy dùng bản đó.
