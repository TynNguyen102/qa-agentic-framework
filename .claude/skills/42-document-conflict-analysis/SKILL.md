---
name: 42-document-conflict-analysis
description: Phát hiện mâu thuẫn và quan hệ giữa các nguồn yêu cầu — AC vs API contract, UI design vs business rule, requirement mới vs hành vi regression cũ, tài liệu thay thế nhau, policy vs project rule, ticket phụ thuộc ticket. Dùng SAU khi review requirement và TRƯỚC khi thiết kế testcase, hoặc khi hai nguồn cùng nói về một hành vi mà expected khác nhau.
---

# Document Conflict & Relationship Analysis

> **Tóm tắt:** Tìm chỗ hai nguồn có thẩm quyền nói khác nhau, ghi thành record máy đọc được, **để người quyết** — agent không tự chọn bên nào.

Thực thi nguyên tắc đã có ở `governance/knowledge-policy.yaml` mục `conflict_policy`
("không âm thầm chọn một source khi hai nguồn có thẩm quyền xung đột") bằng một quy trình và một schema.

## Input gate

Cần có trước khi chạy:

- Output của `01-review-requirements` theo `Config/QA-Agent/schemas/requirement-intake.schema.yaml`
  (tối thiểu: `source_refs`, `expected_behavior`, `acceptance_criteria`).
- `governance/knowledge-policy.yaml` — thứ tự thẩm quyền nguồn.
- `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/<module>/` — rule đã APPROVED của module.
- `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md` — hành vi cũ đã được xác nhận qua defect.

Thiếu `source_refs` ⇒ trả `NEED_CONFIG: SOURCE_REFS_MISSING`, không đoán.

## Mười loại conflict phải quét

Với mỗi cặp nguồn liên quan, kiểm tra theo `Config/QA-Agent/schemas/conflict-report.schema.yaml`:

| Loại | Câu hỏi kiểm tra |
|---|---|
| `EXPECTED_RESULT_MISMATCH` | Hai tài liệu quy định kết quả khác nhau cho cùng hành vi? |
| `AC_VS_API_CONTRACT` | AC nói gì, OpenAPI/live contract nói gì — có lệch required/enum/status/field? |
| `UI_VS_BUSINESS_RULE` | UI design cho phép/hiển thị thứ business rule cấm, hoặc ngược lại? |
| `NEW_VS_REGRESSION` | Requirement mới có phá hành vi cũ đang PASS trong regression? |
| `SUPERSESSION` | Có tài liệu mới thay tài liệu cũ mà bản cũ vẫn đang được trích dẫn? |
| `EFFECTIVE_DATE_OVERLAP` | Hai bản hiệu lực chồng nhau / khác ngày hiệu lực? |
| `POLICY_VS_PROJECT_RULE` | Domain policy (security, data retention) xung đột rule project? |
| `CROSS_TICKET_DEPENDENCY` | Ticket này phụ thuộc/mâu thuẫn ticket khác (Relates, Blocks, parent Epic)? |
| `MULTI_COMPONENT_IMPACT` | Một thay đổi chạm nhiều component với kỳ vọng khác nhau? |
| `STALE_RULE_IN_TESTCASE` | Testcase hiện có đang dùng rule đã `SUPERSEDED`/`REJECTED`? |

## Quy trình

1. **Dựng bảng nguồn.** Mỗi nguồn: loại, id, url, version/updated_at, effective_date, thứ hạng thẩm quyền
   (theo `knowledge-policy.yaml` `authoritative_source_priority`), pulled_at.
2. **Trích phát biểu.** Với mỗi hành vi đang xét, trích **nguyên văn câu** từ từng nguồn — không diễn giải lại.
   Không trích được câu cụ thể thì chưa đủ cơ sở gọi là conflict.
3. **So từng cặp.** Chỉ so các cặp cùng nói về một hành vi. Khác phạm vi ≠ conflict.
4. **Phân loại + chấm severity** (`BLOCKER` / `MAJOR` / `MINOR`).
5. **Truy vết ảnh hưởng.** Conflict này chạm testcase nào, component nào, AC/rule nào.
6. **Đề xuất, không quyết.** Viết `proposed_resolution` kèm lý do, và `required_owner_decision`
   (ai là người có thẩm quyền quyết: BA/PO / Dev Lead / Security owner).
7. **Ghi record.** `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Conflicts/CONF-YYYYMMDD-NNN.yaml`
   + một dòng trong `Conflicts/INDEX.md`.
8. **Chặn đúng chỗ.** `BLOCKER` ⇒ kích hoạt cổng **G1** (`governance/HUMAN_APPROVAL_GATES.md`);
   không route sang `05`/`06`/`07`/`08` trong vùng ảnh hưởng.

## Phân biệt conflict thật và khác biệt vô hại

Không phải khác chữ là conflict. **Chỉ ghi conflict khi hai phát biểu loại trừ nhau** — tức là
làm theo A thì vi phạm B.

| Không phải conflict | Vì sao |
|---|---|
| Hai tài liệu mô tả cùng hành vi bằng từ khác nhau | Khác diễn đạt |
| Một tài liệu chi tiết hơn tài liệu kia | Bổ sung, không loại trừ |
| Tài liệu cũ đã `SUPERSEDED` và không ai còn trích | Đã đóng |
| AC nói về UI, contract nói về API — hai trách nhiệm khác lớp | Xem `knowledge-policy.yaml`: "API validation contract không tự động chứng minh UI/business expected" |

Ngược lại, **đừng bỏ qua** conflict chỉ vì nó bất tiện hoặc vì một bên "có vẻ đúng hơn".

## Safety gate

- **Không** tự chọn `statement_a` hay `statement_b` làm expected, kể cả khi một bên rõ ràng mới hơn.
  Live source mới hơn thắng local cache **sau khi** xác minh đúng project + scope — đó là xác minh, không phải phán đoán.
- **Không** sửa/xoá conflict cũ. Đóng bằng `decision_record`, hoặc tạo conflict mới có `supersedes`.
- **Không** tự mở khoá một `BLOCKER`.
- Không lộ secret/token khi trích nguồn.
- Chỉ đọc — skill này không ghi Jira/Confluence. Muốn hỏi BA/Dev trên Jira thì đó là live write ⇒ cổng **G9**.

## Output contract

Theo `Config/QA-Agent/schemas/skill-io.schema.yaml` `universal_output_envelope`, kèm:

- Bảng nguồn đã so (có version + thứ hạng thẩm quyền)
- Danh sách conflict: `conflict_id`, loại, severity, blocking, hai phát biểu + nguồn, vùng ảnh hưởng
- Danh sách cặp **đã kiểm tra và không có conflict** (để lần sau không kiểm lại)
- Conflict `BLOCKER` đang chặn những skill nào
- Câu hỏi cụ thể cần hỏi ai (dạng hỏi được ngay, không chung chung)
- `evidence_state`: `CONFIRMED` nếu đã đọc bản live; `INFERRED` nếu chỉ đọc cache

## Next recommended

- Có `BLOCKER` → **G1**, dừng design trong vùng ảnh hưởng
- Không có `BLOCKER` → `43-risk-and-change-impact`
- Conflict thuộc loại `STALE_RULE_IN_TESTCASE` → `09-review-testcases` để sửa testcase cũ
- Conflict đã `DECIDED` → cập nhật rule trong `Knowledge-Base/Domain-Rules/` (cần cổng **G8** nếu ghi đè rule APPROVED)
