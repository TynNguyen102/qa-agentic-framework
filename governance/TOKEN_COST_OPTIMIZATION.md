# Token, Time & Cost Optimization

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16 · **Ưu tiên: P2**
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> Gap #32 — trước đây repo **không có** tài liệu nào về việc này.

## 1. Nguyên tắc: rẻ nhất mà vẫn đủ bằng chứng

Tối ưu token **không bao giờ** được đổi bằng việc bỏ bằng chứng. Thứ tự ưu tiên khi xung đột:
**an toàn > bằng chứng > chi phí**.

## 2. Progressive disclosure

| Giai đoạn | Chỉ nạp | Không nạp |
|---|---|---|
| Routing | `name` + `description` của skill; `router-policy.yaml` | Toàn bộ SKILL.md của mọi skill |
| Skill đã chọn | SKILL.md của **skill đó** | SKILL.md của skill khác |
| Oracle | rule theo `rule_id` cần dùng | Cả thư mục `Domain-Rules/` |
| Tài liệu | đoạn liên quan | Nguyên trang Confluence/spec |
| Lịch sử | `CURRENT_STATE.md` | `CURRENT_STATE-archive.md` (chỉ khi cần) |

Đây là lý do `skill-io.schema.yaml` bắt skill khai `inputs` — để orchestrator cắt đúng phần cần.

## 3. Mười ba luật cụ thể

1. **Không dán nguyên tài liệu** vào prompt. Trích đoạn + dẫn nguồn.
2. **Cache tài liệu đã parse** (`Knowledge-Base/*-Mirror/` có `pulled_at`) — không pull lại trong cùng phiên.
3. **Cache OpenAPI/schema** — không fetch lại cho mỗi endpoint.
4. **Tái dùng** testcase / test data / automation script đã có trước khi sinh mới.
5. **Incremental impact analysis** — chỉ phân tích phần đổi, không quét lại cả module.
6. **Change-based execution** — chạy regression theo impact map, không chạy full mặc định.
7. **Song song có giới hạn** — `max_parallel` mặc định 3 (`router-policy.yaml`).
8. **Chỉ fan-out khi risk đủ cao** — risk LOW/MEDIUM chạy tuần tự.
9. **Dừng agent khi đạt exit criteria** — không chạy tiếp "cho chắc".
10. **Không gọi LLM cho assertion tất định.** So sánh số, so schema, đếm bản ghi, diff file → dùng code/tool.
11. **Rule engine trước, AI sau.** Việc nào checklist/regex/schema làm được thì đừng để model suy luận.
12. **Không lặp lại nội dung** giữa các output trong cùng phiên — tham chiếu thay vì chép lại.
13. **Đọc file lớn theo đoạn** (`sed -n`, `head`, grep có ngữ cảnh) thay vì đọc cả file.

## 4. Chỗ KHÔNG được tiết kiệm

| Không cắt | Vì sao |
|---|---|
| Readback đa lớp trước khi kết luận PASS | Cắt là mất tính đúng đắn của verdict |
| Capture evidence | Không có evidence thì kết quả vô giá trị |
| Lặp lại N lần cho output AI | Một mẫu không chứng minh consistency |
| Đọc `Defects/INDEX.md` khi test module cũ | Bỏ là lặp lại lỗi cũ |
| Đọc rule APPROVED làm oracle | Bỏ là tự suy diễn expected |
| Các cổng G1–G9 | Cổng không phải chi phí, là điều kiện |

## 5. Chỉ số cần theo dõi (chưa đo được)

| Chỉ số | Trạng thái |
|---|---|
| Token / task | `NOT_MEASURED` |
| Số tool-call / task | `NOT_MEASURED` |
| Thời gian / task | `NOT_MEASURED` |
| Tỉ lệ tái dùng artifact | `NOT_MEASURED` |
| Số lần fetch lại tài liệu đã cache | `NOT_MEASURED` |

`execution-plan.schema.yaml` đã có trường `budget` (`token_budget_hint`, `time_budget_hint`,
`max_parallel`) để chứa các số này khi có cơ chế đo. Hiện **chưa có** — đừng báo cáo số ước lượng
như số đo thật.

## 6. Dấu hiệu đang lãng phí

- Đọc cùng một file nhiều lần trong một phiên.
- Fan-out 5 agent cho một US risk LOW.
- Sinh lại testcase cho thứ `Modules/<m>/TC/` đã có.
- Dùng model để so hai con số.
- Nạp cả `Domain-Rules/` khi chỉ cần một rule.
- Chạy full regression khi impact map chỉ chạm một endpoint.
