# Test Coverage Model

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Đây là trang chỉ đường, không phải mô hình mới.** Mô hình coverage thật đã tồn tại và đang được
> dùng — tài liệu này gom đầu mối lại và bổ sung đúng phần enum còn thiếu (gap #9).
> Không tạo mô hình song song để tránh hai nguồn sự thật.

## 1. Nguồn chuẩn (giữ nguyên, không thay thế)

| File | Vai trò |
|---|---|
| `Config/QA-Agent/professional-coverage-model.yaml` | **Mẫu số dùng chung** — coverage unit theo các dimension BE/API/data, FE/UI/UX, flow/business, security, non-functional |
| `Config/QA-Agent/api-coverage-profile.yaml` | Phạm vi API/event |
| `Config/QA-Agent/canonical-testcase-schema.yaml` | Hình dạng testcase + trường traceability |
| `.agents/skills/24-test-coverage-audit/SKILL.md` | Skill thực hiện audit coverage |

## 2. Luật bất di bất dịch

1. **Không có mẫu số thì không có phần trăm.** Mọi con số coverage phải kèm denominator thật.
2. **Không tuyên bố** "đã cover tất cả" / "100%" / "zero bug".
3. Thiếu execution **không** được quy đổi thành 100% (eval case P0-012).
4. Có file testcase/automation **không** đồng nghĩa đã EXECUTED (eval case ZT-010).
5. Mọi báo cáo coverage phải kèm **residual risk**.

## 3. Trạng thái coverage chuẩn hoá (phần BỔ SUNG)

Trước đây các skill dùng chữ tự do. Từ nay dùng đúng 5 giá trị:

| Trạng thái | Nghĩa | Được tính vào tử số? |
|---|---|---|
| `COVERED` | Có testcase **và** đã execute có evidence | Có |
| `PARTIALLY_COVERED` | Có testcase nhưng chưa execute đủ, hoặc execute thiếu readback | Không — đếm riêng |
| `NOT_COVERED` | Chưa có testcase | Không |
| `NOT_APPLICABLE` | Không áp dụng cho unit này — **bắt buộc ghi lý do** | Loại khỏi mẫu số |
| `BLOCKED` | Không test được do quyền/môi trường/data/conflict — **bắt buộc ghi blocker** | Không — đếm riêng |

`NOT_APPLICABLE` không có lý do ⇒ coi như `NOT_COVERED`. Đây là chỗ dễ bị lạm dụng để làm đẹp số.

## 4. Chiều coverage phải cân nhắc

Từ `professional-coverage-model.yaml` + brief §XI. Chiều nào không áp dụng thì ghi
`NOT_APPLICABLE` kèm lý do, **không** im lặng bỏ:

requirement · acceptance criteria · risk · business rule · positive/negative · boundary ·
state transition · role & permission · data variation · API operation & status code · UI action ·
integration · security · regression impact · historical defect · traceability completeness

## 5. Output bắt buộc của một coverage audit

```
- denominator: <tổng coverage unit áp dụng>
- counts: {COVERED, PARTIALLY_COVERED, NOT_COVERED, NOT_APPLICABLE, BLOCKED}
- untested_units: [danh sách cụ thể, không gom chung]
- blocked_units: [đơn vị + blocker + ai gỡ được]
- residual_risk: [mô tả rủi ro còn lại + mức]
- suggested_additional_tests: [...]
- evidence_state: CONFIRMED | INFERRED | ASSUMED | NOT_CHECKED
```

## 6. Liên kết

- Ngưỡng chấp nhận residual risk → cổng **G2** trong `HUMAN_APPROVAL_GATES.md`
- Kết quả từng testcase → `Config/QA-Agent/schemas/test-result.schema.yaml`
- Độ tin cậy của chính bản audit → `Config/QA-Agent/schemas/confidence-report.schema.yaml`
