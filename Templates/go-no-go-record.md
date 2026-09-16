# Template — Khuyến nghị Go/No-Go cho 1 item

**Khi nào dùng:** item chuyển vào `Ready to deploy`. Mỗi item 1 quyết định nhỏ — **không** chờ mốc
release, vì project này release liên tục không lịch trình.

**Ghi ở đâu:** 1 comment trên chính item Jira. Không tạo tài liệu riêng, không cần họp.

**QC không quyết định release.** QC đưa dữ liệu và khuyến nghị; PM/PO quyết.

---

## 5 điều kiện tối thiểu để khuyến nghị `GO`

| # | Điều kiện | Đạt? |
|---|---|---|
| 1 | Toàn bộ TC priority **High** đã `EXECUTED`, không còn FAIL chưa xử lý | ☐ |
| 2 | Bug severity **Critical/High** của item đã **`Closed`** — không phải `Resolved` | ☐ |
| 3 | Smoke vùng liên quan **PASS** | ☐ |
| 4 | Mỗi kết luận có **evidence path** | ☐ |
| 5 | Nếu là migration → đã test **dữ liệu cũ** và **rollback** | ☐ / N/A |

> Điều kiện 2 là chỗ dễ sai nhất ở project `SP`: `Resolved` **không** tính là đã đóng.

---

## TEMPLATE comment Jira

```
[QC] Khuyến nghị release: GO / GO WITH RISK / NO GO

Phạm vi đã test
- Testcase: <đã execute>/<tổng>  (High: <x>/<y>)
- Môi trường: DEV
- Evidence: <đường dẫn hoặc mô tả ngắn>

Kết quả
- PASS: <n>
- FAIL: <n>  <nếu có: nêu ngắn cái nào>
- Chưa verify được: <n>  <lý do: thiếu dữ liệu thật / thiếu quyền-config>

Bug liên quan
- <KEY>: <severity> — <status hiện tại>

Rủi ro còn lại
- <vùng nào chưa được kiểm chứng và vì sao>

Khuyến nghị: <GO / GO WITH RISK / NO GO>
<nếu GO WITH RISK: thiếu điều kiện nào, rủi ro cụ thể là gì, và cần ai chấp nhận rủi ro>
<nếu NO GO: cần gì để chuyển thành GO>
```

**Viết như QA viết tay** — ngắn gọn, chỉ nói việc. Không nhắc tên file nội bộ, rule ID nội bộ, tên
skill. Xưng hô "mình/bạn" nếu cần.

---

## Ba khuyến nghị — chọn đúng 1

| Khuyến nghị | Khi nào | Bắt buộc kèm |
|---|---|---|
| **GO** | Đủ 5 điều kiện | — |
| **GO WITH RISK** | Thiếu điều kiện nhưng business cần ra | Thiếu gì · rủi ro cụ thể · **tên người chấp nhận rủi ro** |
| **NO GO** | Có FAIL ở TC High, hoặc bug Critical chưa `Closed` | Lý do cụ thể + cần gì để chuyển thành GO |

Khớp 3 phương án PA1/PA2/PA3 của template report org-wide ("System Test Report (Web Portal/API)").

**`GO WITH RISK` bắt buộc có tên người chấp nhận rủi ro.** Không có tên thì không phải là quyết định
— chỉ là QC tự gánh rủi ro thay người khác.

---

## VÍ DỤ THẬT — DEMO-6091

```
[QC] Khuyến nghị release: GO WITH RISK

Phạm vi đã test
- Testcase: 19/33 đã execute (High: đã chạy hết)
- Môi trường: DEV, qua UI + API, dữ liệu production-like
- Evidence: ledger execution ngày 27/08, quét ~89% (7313/8183) execution failed thật hiện có

Kết quả
- PASS: 11 case có evidence + đối chiếu dữ liệu (gồm 72 mẫu khớp 100% bảng category↔fault_domain)
- FAIL: 0
- Chưa verify được: 14 — 6 case do tình huống chưa từng xảy ra trong dữ liệu thật
  (authentication, retry thành công, batch partial); 8 case do cần quyền/config QC không có
- 5 case thuộc tầng unit test của dev, không nằm trong phạm vi QC

Bug liên quan
- DEMO-6925: Minor — user_message lộ nguyên văn HTTPStatusError khi category không khớp pattern.
  Đã xác nhận xảy ra ở 2 playbook khác nhau nên là lỗi tầng classifier chung, không riêng 1 playbook.
  Status: chưa Closed.

Rủi ro còn lại
- Hành vi khi 1 execution có nhiều node fail đồng thời chưa kiểm chứng được: mọi mẫu dữ liệu thật
  quét được đều chỉ có 1 node fail.
- 2 badge UI chưa có tên chính thức, đang chờ xác nhận.

Khuyến nghị: GO WITH RISK
- Thiếu điều kiện: 14/33 case chưa verify được, và DEMO-6925 chưa Closed.
- Rủi ro: người dùng có thể thấy thông báo lỗi kỹ thuật thô ở nhánh category không khớp pattern.
  Không mất dữ liệu, không chặn luồng chính.
- Cần PM/PO xác nhận chấp nhận rủi ro này để deploy trước khi DEMO-6925 được fix.
```
