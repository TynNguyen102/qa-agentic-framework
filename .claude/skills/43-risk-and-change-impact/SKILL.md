---
name: 43-risk-and-change-impact
description: Phân tích rủi ro và bản đồ ảnh hưởng của một thay đổi — component trực tiếp, component phụ thuộc, API consumer/provider, DB/schema, UI flow, role/permission, event/queue, batch, integration, migration, security, performance, regression, backward compatibility, observability, và AI model/prompt/RAG nếu có. Dùng sau khi requirement đã rõ và conflict đã được quét, trước khi chọn phạm vi test.
---

# Risk & Change Impact Analysis

> **Tóm tắt:** Trả lời "thay đổi này chạm tới đâu, và chỗ nào đáng lo nhất" — bằng bản đồ ảnh hưởng có nguồn, không phải cảm tính.

Đây là đầu vào chính cho `44-test-advisor` (chọn loại test) và cho `qa-router` (chọn skill, quyết định fan-out).

## Input gate

- Output `01-review-requirements` (`requirement-intake.schema.yaml`)
- Output `42-document-conflict-analysis` — conflict `BLOCKER` làm risk tăng, không được bỏ qua
- `Projects/<ACTIVE_PROJECT>/Config/modules.yaml` — danh mục module
- `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md` — lịch sử lỗi của module (tín hiệu risk mạnh nhất)
- Khi có: MR/commit diff qua GitLab REST, OpenAPI hiện hành, `_db-reference.md` của module

Không có nguồn nào cho biết thay đổi chạm gì (không MR, không spec, không mô tả kỹ thuật)
⇒ trả `NEED_CONFIG: CHANGE_SCOPE_UNKNOWN` và nêu cần gì. **Không đoán impact.**

## 17 chiều ảnh hưởng phải quét

Mỗi chiều trả một trong: `IMPACTED` / `NOT_IMPACTED` / `UNKNOWN`. `UNKNOWN` **không** được coi là không ảnh hưởng.

| # | Chiều | Câu hỏi |
|---|---|---|
| 1 | Component trực tiếp | File/service/màn hình nào thực sự đổi? |
| 2 | Component phụ thuộc | Ai gọi/đọc component đó? |
| 3 | API consumer / provider | Contract có đổi? Ai đang dùng bản cũ? |
| 4 | Database / table / schema | Cột, ràng buộc, index, view nào chạm? |
| 5 | UI flow | Luồng màn hình nào bị chèn/bỏ/đổi thứ tự? |
| 6 | Role & permission | Ai được/không được làm gì sau thay đổi? |
| 7 | Authentication / authorization | Token, scope, guard, route guard? |
| 8 | Event / message / queue | Producer/consumer, schema event, thứ tự, retry? |
| 9 | Batch / schedule | DAG, cron, job nào đọc dữ liệu này? |
| 10 | Integration | Hệ thống ngoài nào nhận ảnh hưởng? |
| 11 | Data migration | Có backfill/migration? Dữ liệu cũ xử lý ra sao? |
| 12 | Security | Bề mặt tấn công mới? Dữ liệu nhạy cảm mới lộ ra? |
| 13 | Performance | Query mới, N+1, payload lớn, vòng lặp gọi API? |
| 14 | Regression | Hành vi cũ nào có thể vỡ? |
| 15 | Backward compatibility | Client/phiên bản cũ còn chạy được? |
| 16 | Observability / logging | Có log/metric/audit cho hành vi mới? Mất log cũ không? |
| 17 | AI model / prompt / RAG | Đổi model, prompt, retrieval source, tool-use? |

Chiều 17 là **sự kiện regression** riêng — đổi model/prompt/provider luôn kéo theo `40-ai-output-testing` baseline rerun.

## Chấm risk

Risk của mỗi vùng ảnh hưởng = **Khả năng xảy ra × Mức thiệt hại**, có giải thích, không chỉ con số.

**Khả năng xảy ra** tăng khi: module có lịch sử defect trong `Defects/INDEX.md`; thay đổi nhiều file;
logic phức tạp (state machine, đồng thời, tính toán); requirement còn `NEED_CONFIRM`;
có conflict `MAJOR`/`BLOCKER`; code mới chưa từng có test.

**Bắt buộc đọc trước khi chấm khả năng xảy ra:**
`Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/_defect-patterns.md` — bảng lớp lỗi lặp lại
rút từ toàn bộ lịch sử finding của project, kèm hệ số cộng vào khả năng xảy ra. Đây là thống kê lịch
sử, **không phải oracle**; dùng để xếp ưu tiên, không dùng làm căn cứ PASS/FAIL và không trích ra
báo cáo ngoài. Không có file đó thì ghi `ASSUMED` cho phần khả năng xảy ra, đừng đoán.

Ba lớp lỗi dưới đây chiếm tỷ trọng lớn nhất trong lịch sử và **thường bị bỏ sót**, nên luôn kiểm
xem thay đổi có chạm không, kể cả khi chúng không nằm trong mô tả yêu cầu:

| Lớp | Dấu hiệu cần soi |
|---|---|
| Phân quyền trên **bề mặt mới** | Thêm scope, thêm endpoint phụ (`sse`, `audit_logs`, `*-metrics`), thêm route — hàm kiểm quyền có, nhưng **quên gọi** |
| FE hiển thị **số giả** khi API lỗi | Màn có thẻ chỉ số/KPI đọc từ API riêng — API lỗi mà FE hiện `0` thay vì trạng thái lỗi |
| **Lệch số** giữa nhiều nguồn | Cùng một con số hiển thị ở thẻ tổng quan, bảng và API — phải đối chiếu cả ba |

**Mức thiệt hại** tăng khi: chạm tiền/quyền/dữ liệu khách hàng; ảnh hưởng nhiều tenant;
không thể rollback; lỗi âm thầm (không có cảnh báo); chạm security/privacy/compliance;
là luồng nghiệp vụ tới hạn.

| Mức | Nghĩa | Hệ quả bắt buộc |
|---|---|---|
| `VERY_HIGH` | Có thể gây mất/lộ dữ liệu, sai quyền, hỏng luồng tới hạn | Test sâu bắt buộc; không được bỏ; cần security pass |
| `HIGH` | Ảnh hưởng nghiệp vụ rõ, khó phát hiện bằng mắt | Baseline + deep test; ưu tiên automation |
| `MEDIUM` | Ảnh hưởng cục bộ, phát hiện được | Baseline đủ |
| `LOW` | Thay đổi hiển thị/nội dung, không đổi dữ liệu | Smoke |
| `NEED_CONFIRM` | Chưa đủ dữ kiện để chấm | **Không** được mặc định coi là LOW |

**Luật cứng:** không hạ risk để giảm khối lượng test. Muốn giảm phạm vi test thì đi qua cổng **G2**
(chấp nhận residual risk), không phải bằng cách chấm risk thấp hơn.

## Output contract

Theo `skill-io.schema.yaml` `universal_output_envelope`, kèm:

```
risk_id: RISK-YYYYMMDD-NNN
change_summary: <thay đổi là gì, dẫn nguồn: MR/spec/ticket>
impact_map:
  - dimension: <1 trong 17>
    verdict: IMPACTED | NOT_IMPACTED | UNKNOWN
    detail: <cụ thể: tên endpoint/bảng/màn hình/role>
    source: <MR id / spec / schema / suy luận — ghi rõ>
    evidence_state: CONFIRMED | INFERRED | ASSUMED
risk_items:
  - area, likelihood, impact, level, explanation, historical_defect_refs
overall_risk_level: <mức cao nhất trong risk_items>
required_test_depth: MINIMUM | RECOMMENDED | DEEP
suggested_skills: [...]
suggested_test_suite: [smoke | impacted regression | full regression]
parallelizable_tasks: [...]      # theo router-policy.yaml fanout_rules
blocking_dependencies: [...]     # gì phải xong trước
unknowns: [...]                  # chiều nào còn UNKNOWN và cần ai trả lời
```

## Safety gate

- `UNKNOWN` ≠ `NOT_IMPACTED`. Mỗi `UNKNOWN` phải có một câu hỏi và một người nhận câu hỏi.
- Không suy impact từ **tên** file/endpoint — phải đọc được diff, spec hoặc schema thật.
  Suy từ tên ⇒ `evidence_state: INFERRED`, ghi rõ.
- Không dùng impact map của project khác.
- Không tự chạy query/probe lên môi trường để "kiểm tra impact" nếu vượt assurance level cho phép
  (`Config/QA-Agent/assurance-levels.yaml`).

## Next recommended

- Luôn → `44-test-advisor` (biến risk thành checklist loại test)
- `overall_risk_level` ∈ {`HIGH`, `VERY_HIGH`} → cân nhắc song song theo `router-policy.yaml` `fanout_rules`
- Chiều 17 `IMPACTED` → `40-ai-output-testing` baseline rerun
- Chiều 12 `IMPACTED` → `23-security-testing` (cần cổng **G3** nếu là test xâm nhập)
- Chiều 11/4 `IMPACTED` → `34-database-testing`
- Chiều 3/15 `IMPACTED` → `22-contract-compatibility-testing`
