---
name: 36-log-jira-defect
description: Soạn nháp, kiểm tra trùng lặp, xác thực và—khi được phê duyệt rõ ràng—tạo defect trên Jira theo format tiếng Việt, bằng chứng và liên kết truy vết đã cấu hình. Dùng khi một lỗi đã vượt qua cơ sở xác nhận bug.
---

# Ghi nhận defect trên Jira

> **Tóm tắt (VI):** Ghi bug lên Jira đúng chuẩn (title 4 phần, đủ mục, assignee/sprint/due, link Story) sau khi qua 6 cổng. Dùng khi có lỗi ĐÃ xác minh cần raise.

Đọc `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml` và `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml` trước. Luôn tạo phần mô tả bằng tiếng Việt; chỉ giữ nguyên tên kỹ thuật, endpoint, mã lỗi và giá trị enum khi việc dịch làm sai nghĩa.

## Cổng cấu hình

Có thể dùng ngay cấu trúc mô tả khi profile ở trạng thái `PARTIAL_CONFIG`. Dùng đúng `title_format` đã xác nhận trong `defect-profile.yaml`, không tự đổi sang style khác (kể cả style quan sát từ `reference_issues` trong profile đó). Severity/priority/component/label/custom field vẫn chưa có mapping — không tự đặt, trả `NEED_CONFIG: SEVERITY_PRIORITY_SCALE` khi cần.

## Format mô tả — hai bản khác nhau, KHÔNG dùng chung

**Bản local (đầy đủ 9 phần)** — lưu ở `Projects/<ACTIVE_PROJECT>/Defects/<local_id>/manifest.yaml` + `description.md`, dùng đúng thứ tự heading trong `defect-profile.yaml`:

1. Môi trường
2. Điều kiện tiên quyết
3. Các bước tái hiện
4. Kết quả thực tế
5. Kết quả mong đợi
6. Bằng chứng
7. Ảnh hưởng
8. Khả năng tái hiện và phạm vi ảnh hưởng
9. Liên kết truy vết

Không để heading rỗng. Nếu chưa có dữ liệu, ghi `CHƯA CÓ` hoặc `NEED_CONFIRM` kèm lý do.

**Bản Jira live (chỉ 5 phần, xem `jira_live_body` trong `defect-profile.yaml`)** — Môi trường, Các bước tái hiện, Kết quả thực tế, Kết quả mong muốn, Bằng chứng. Mỗi mục 1-3 dòng. KHÔNG đưa Điều kiện tiên quyết, Ảnh hưởng, Khả năng tái hiện và phạm vi ảnh hưởng, Liên kết truy vết, residual risk, duplicate-triage reasoning hay bất kỳ phân tích dài nào lên Jira — những phần đó chỉ ở lại bản local. Nếu profile có ghi lại phản hồi trước đây của anh về việc log quá dài dòng, tuân theo đúng mức độ ngắn gọn đó.

**Style bắt buộc cho bản Jira live** (đối chiếu `reference_issues` thật trong `defect-profile.yaml` khi có): gạch đầu dòng lồng nhau kiểu `* **Label:** value`, KHÔNG dùng markdown table, KHÔNG viết đoạn văn dài. Case/dataset/field liệt kê từng bullet riêng (có thể lồng dưới bước liên quan), không gộp bảng. Chỉ bước tái hiện đánh số; mọi thứ khác dùng bullet. Dùng đúng `template_example` trong `defect-profile.yaml`.

## Quy trình

0. **Không bao giờ tham chiếu một Bug ID trong run-log/test report trước khi bug đó thật sự được tạo với đúng ID đó.** Nếu automation/execution phát hiện lỗi nhưng chưa kịp log defect chính thức ngay lúc đó, dùng placeholder tường minh (vd `PENDING-BUG`, hoặc mô tả ngắn) trong run-log rồi cập nhật lại ID thật sau khi log xong — không đoán/tái dùng số ID kế tiếp. Case thật đã gặp (DEMO-4609, review 2026-08-27): run-log ghi "BUG-001/002/003" cho 3 lỗi automation tìm thấy, nhưng bug report thật lại dùng đúng 3 ID đó cho 3 lỗi hoàn toàn khác (đã log từ một vòng test riêng) — gãy truy vết, ai tra theo ID sẽ ra nhầm bug.
1. Vượt qua các cổng xác nhận trong `bug-basis-profile.yaml`: có nguồn expected, tái hiện được, chứng minh actual, readback, impact và loại trừ lỗi môi trường/test data/automation.
2. Tìm defect trùng khi connector Jira khả dụng. So sánh business invariant, triệu chứng, component, API operation, error signature, build và điều kiện tái hiện.
3. Soạn đủ chín phần bằng tiếng Việt cho bản LOCAL, liên kết requirement/testcase/execution và giữ bước tái hiện tối thiểu, xác định. Khi tạo/sửa nội dung trên Jira, chỉ dùng bản rút gọn 5 phần + style bullet ở trên — không copy nguyên bản local 9 phần lên Jira.
4. Xóa password, token, cookie, API key, PII không cần thiết và curl chứa credential trước khi ghi hoặc đính kèm bằng chứng.
5. Tạo hoặc cập nhật manifest xuyên sprint tại `Projects/<ACTIVE_PROJECT>/Defects/<local_id>/manifest.yaml` (khởi tạo từ `Templates/defect-record.yaml`, theo đúng schema/enum trong `Config/QA-Agent/defect-register-schema.yaml`): điền `found_in_sprint`, `fingerprint`, `duplicate_triage`, `traceability.requirements/testcases`, `security.redaction_status`. Đặt `lifecycle_status` theo tiến trình thật (`DRAFT` → `TRIAGED` → `CONFIRMED`), không nhảy cóc.
6. Mặc định lưu `DRAFT`. Chỉ tạo Jira live sau khi anh phê duyệt rõ ràng trong phiên hiện tại.
7. Ảnh/screenshot: kiểm tra lại mỗi lần xem bộ tool hiện có API đính kèm file nhị phân vào Jira không (tính tới 2026-07-19: KHÔNG có). Nếu không có, phải báo rõ giới hạn này với anh (không âm thầm bỏ qua) và ghi tên file + đường dẫn local vào phần Bằng chứng để anh tự đính kèm, thay vì giả vờ đã đính kèm.
8. Sau khi tạo, đọc lại key, tiêu đề, issue type, trạng thái, fields, links và attachments; báo rõ partial failure. Cập nhật manifest: `jira.key/status/snapshot_at`, `lifecycle_status: LOGGED` (yêu cầu `security.redaction_status: VERIFIED` trước khi chuyển).

## Đầu ra

Trả một trong các kết quả: `NEED_CONFIG`, bản nháp defect tiếng Việt đã validate, quyết định duplicate candidate, hoặc Jira key đã tạo kèm readback — kèm đường dẫn manifest đã tạo/cập nhật. Không gọi một observation chưa đủ cơ sở là bug.

---

## Bổ sung 2026-09-03 — chuẩn Example-Project đã được Lead chốt

`defect-profile.yaml` của Example-Project giờ ở trạng thái `CONFIGURED`. Đọc nó và tuân theo, không tự suy diễn format nữa.

### Tiêu đề — bốn thành phần, thiếu một là không log

```
[<TẦNG>][<LOẠI>] <Module> / <Chức năng> - <Mô tả ngắn lỗi>
```

| Thành phần | Giá trị | Nguồn |
|---|---|---|
| **TẦNG** | `BE` · `FE` · `Model` | Xác định từ bằng chứng, chưa rõ thì `NEED_CONFIRM` |
| **LOẠI** | `Logic` · `UI/UX` | **Một ticket chỉ mang đúng một loại** |
| **Module** | theo `display` trong `Config/modules.yaml` | Không tự đặt tên |
| **Mô tả** | một câu nêu đúng hành vi sai | Không viết "bị lỗi" chung chung |

**Tách riêng bắt buộc:** bug `Logic` và bug `BE` **không được gộp** vào ticket `UI/UX`. Một màn hình có cả hai loại lỗi thì log hai ticket.

### Mô tả trên Jira — đúng bốn mục

1. **Môi trường**
2. **Steps**
3. **Kết quả thực tế (Evidence)**
4. **Expected**

Không thêm mục nào khác lên Jira. Phân tích, ảnh hưởng, truy vết, residual risk chỉ ở bản local.

### Lưu ý thao tác khi tạo/sửa trên Jira (đã gặp lỗi thật)

- Gọi `createJiraIssue` / `addCommentToJiraIssue` / `editJiraIssue` với `contentFormat: "markdown"`; dùng markdown thuần (`**bold**`, `` `code` ``, bảng markdown), KHÔNG trộn Jira wiki markup (`h3.`, `# item`).
- **KHÔNG bắt đầu một dòng bằng `1. ` / `2. `** trong Steps hay trong ô bảng: Jira parse `1.` đầu dòng thành ordered-list marker và **nuốt mất số đó** khi lưu (chỉ số đầu bị nuốt, các số sau giữ literal → lệch số, đã gặp thật). Dùng `Bước 1:`, `Bước 2:` mỗi bước một dòng.
- Tra assignee + sprint hiện tại của US cha trong **cùng một** lần `getJiraIssue`/JQL `key = <US>` (không hỏi anh, không gọi lẻ nhiều lần).
- Project SP có **custom field bắt buộc** khi tạo issue/subtask — `customfield_10355` (Điều kiện chấp nhận / AC-DoD) truyền dạng **ADF object** (không phải chuỗi). Nếu `createJiraIssue` báo `... is required` hoặc `not valid ADF`, bổ sung field này qua `additional_fields`.

### Assignee, due date, label

| Trường | Quy tắc |
|---|---|
| **Assignee** | Đúng người đang assignee của **US** mà bug thuộc về. Không để trống, không tự gán cho QC |
| **Due date** | `due_date_US + offset` — **Highest +1**, **High +1**, **Medium +2**. `Low` chưa quy định → hỏi Lead |
| **Label** | Theo `id` module trong `modules.yaml`. Nhiều module thì label đầu là module chính. **Không dùng label squad** |

**US không có due date** → không tự đặt due date cho bug. Ghi `NEED_CONFIRM` và báo Lead — thiếu due date US là vấn đề riêng cần xử lý.

### Bug UI/UX — gom một ticket mỗi module

Tiêu đề: `[FE][UI/UX] <Module> - Tổng hợp lỗi giao diện`

Thân bài là **bảng**, mỗi lỗi một dòng:

| # | Màn hình / Chức năng | Mô tả lỗi | Expected | Evidence |
|---|---|---|---|---|

**Số thứ tự chạy liên tục**, không đánh lại từ 1 khi bổ sung lỗi mới. Lỗi đã fix thì đánh dấu trong bảng, **không xoá dòng** — để giữ vết.

Tách thành ticket riêng khi: lỗi UI/UX **chặn luồng nghiệp vụ**; cần **assignee khác**; hoặc **due date gấp hơn hẳn** phần còn lại.

### Ghi hai nơi — không được bỏ bước nào

| Bước | Nơi |
|---|---|
| 1 | Issue trên **Jira** |
| 2 | **`Projects/<dự án>/Defects/FINDING-YYYYMMDD-NNN/`** — `manifest.yaml` + `description.md` |

Chỉ làm bước 1 là **chưa xong việc**. Lý do đầy đủ: `Knowledge-Base/Domain-Rules/quy-tac-log-bug-hai-noi.md`.

### Lý do đóng bug — phân biệt ba trường hợp

| Resolution | Nghĩa |
|---|---|
| **Fixed** | Lỗi được sửa ở tầng code, đã retest PASS |
| **Tính năng đã bị loại bỏ** | Trang/chức năng không còn tồn tại — **lỗ hổng KHÔNG được vá** |
| **Không tái hiện** | Không dựng lại được, nhưng code chưa đổi |

Đóng nhầm `Fixed` khi thực ra tính năng bị gỡ sẽ khiến người đọc sau này tưởng lỗ hổng đã vá.

## Confidence report (bổ sung 2026-09-16)

Output của skill này phải kèm một confidence report theo
`Config/QA-Agent/schemas/confidence-report.schema.yaml` — 8 thành phần, mỗi thành phần 0–3, kèm
**một dòng lý do cho từng thành phần**: source quality · requirement completeness · traceability ·
coverage · execution evidence · reproducibility · review status · conflict status.

**Cách báo cáo:** luôn hiện `band` + `limiting_factors` + `required_actions`. **Không bao giờ** chỉ
hiện con số tổng, và không gọi nó là "độ chính xác của AI".

**Luật cứng:**

| Điều kiện | Hệ quả |
|---|---|
| Bất kỳ thành phần nào = 0 | band tối đa là `LOW`, bất kể tổng điểm |
| `conflict_status` = 0 (có conflict `BLOCKER` mở) | band `UNUSABLE` — không publish ra ngoài |
| `execution_evidence` ≤ 1 | **Không** được phát biểu verdict PASS/FAIL, chỉ được nói `INFERRED` |
| Muốn nâng band | Phải có **bằng chứng mới**, không phải đánh giá lại. Agent không tự nâng band |

Xem thêm `governance/AI_RESULT_ASSURANCE_MODEL.md`.
