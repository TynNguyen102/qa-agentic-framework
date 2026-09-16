# Human Approval Gates

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Bản chất:** tài liệu này **tổng hợp** các cổng phê duyệt đã tồn tại rải rác trong repo — nó
> **không phát minh cổng mới**. Mỗi cổng dưới đây đều dẫn nơi nó đang được thực thi.
> Gap #34 trong `QA_AGENTIC_WORKFLOW_GAP_ANALYSIS.md`: gate đúng và đang chạy, nhưng không có
> một nguồn nào liệt kê đủ — đây là nguồn đó.

## Nguyên tắc

1. Gate là **chặn**, không phải cảnh báo. Agent gặp gate thì **dừng và hỏi**, không tự quyết.
2. Phê duyệt có **phạm vi và thời hạn**: duyệt cho việc này không tự động duyệt cho việc sau.
3. Mọi lần vượt gate phải sinh một audit event (`governance/audit-policy.yaml`).
4. Agent **không được tự duyệt** thứ do chính agent đề xuất.

## Bảng cổng

| ID | Cổng | Chặn điều gì | Ai duyệt | Đang được thực thi ở đâu |
|---|---|---|---|---|
| **G1** | Conflict resolution | Test design + mọi verdict PASS/FAIL trong vùng ảnh hưởng, khi có conflict `BLOCKER` | BA/PO (business), Dev Lead (contract), Security owner (security) | `knowledge-policy.yaml` `conflict_policy`; `schemas/conflict-report.schema.yaml`; skill `42` |
| **G2** | Residual risk acceptance | Đóng sprint/feature khi còn coverage unit chưa test | QA Lead + PO | `professional-coverage-model.yaml`; skill `24`, `33` |
| **G3** | Destructive test | Security/performance/resilience/failover ở assurance L3–L4 | QA Lead + owner môi trường | `assurance-levels.yaml` (`approval_required`, `dedicated_environment_required`); skill `23`, `25`, `17` |
| **G4** | Sensitive data use | Dùng dữ liệu thật/PII/production-like | Data owner + QA Lead | `knowledge-policy.yaml` `security_and_retention`; skill `10`, `38` |
| **G5** | Low-confidence defect | Log Jira khi confidence band = `LOW`/`UNUSABLE` | QA Lead | `DEFECT_VERIFICATION_POLICY.md`; `schemas/confidence-report.schema.yaml`; skill `39` |
| **G6** | Core skill / policy change | Sửa Core skill, `Config/QA-Agent/*`, `governance/*`, schema | QA Lead (+ CODEOWNERS) | `CODEOWNERS`, `CONTRIBUTING.md`, `git-collaboration.yaml` |
| **G7** | Release gate inclusion | Đưa một test vào cổng release/CI blocking | QA Lead + Release owner | `router-policy.yaml` `suite_classification` |
| **G8** | Business rule override | Ghi đè/diễn giải khác business hoặc domain rule đã APPROVED | Rule owner (BA/PO) | `knowledge-policy.yaml` `promote` ("agent không tự approve rule do chính agent phát hiện") |
| **G9** | Live write | Mọi ghi live: Jira, QMetry/TestRail, Confluence, Git push/merge, mutation môi trường/dữ liệu | Người yêu cầu trong phiên hiện tại | `CLAUDE.md` Must Follow; `qa-router` Mandatory gates; `.claude/hooks/pre_jira_write_gate.py` |

## Chi tiết từng cổng

### G1 — Conflict resolution
**Kích hoạt khi:** skill `42` sinh conflict với `severity: BLOCKER`.
**Agent được làm:** trình bày cả hai statement + nguồn + version, đề xuất `proposed_resolution`.
**Agent KHÔNG được làm:** chọn một bên rồi tiếp tục design/verdict.
**Mở cổng bằng:** `decision_record` có `decided_by`, `decided_at`, `chosen_source`, `rationale`.

### G3 — Destructive test
**Kích hoạt khi:** `assurance_level` ≥ L3.
**Bắt buộc có trước khi chạy:** scope, rules of engagement, môi trường được phép, rate limit, stop condition, kế hoạch redact evidence.
**Không bao giờ:** chạy trên PROD. `Projects/Example-Project/qa-config.yaml` đặt `TEST_POLICY: FORBIDDEN` cho PROD.

### G5 — Low-confidence defect
**Kích hoạt khi:** confidence band `LOW`/`UNUSABLE`, hoặc `failure_classification = UNKNOWN`.
**Agent được làm:** tạo *suspected defect* local (`Defects/FINDING-*`), không tạo Jira issue.
**Mở cổng bằng:** Lead xác nhận, hoặc bổ sung bằng chứng để nâng band.

### G9 — Live write
Cổng gặp thường xuyên nhất. Đã có hook cưỡng chế: `.claude/hooks/pre_jira_write_gate.py`.
**Lưu ý đã biết:** hook chỉ **cảnh báo** với luật "bug phải Relates→Story" chứ không chặn — nên luật này
dễ bị quên. Xem `DEFECT_VERIFICATION_POLICY.md`.

## Cổng KHÔNG tồn tại (đừng bịa)

Agent không được tự tạo cổng mới để trì hoãn việc. Nếu một việc thấy rủi ro nhưng không khớp G1–G9:
nêu rủi ro trong output, **vẫn làm tiếp**, và đề xuất bổ sung cổng qua G6.

## Ghi nhận phê duyệt

Mỗi lần vượt gate, audit event phải có:

```yaml
gate_id: G9
approved_by: "<người> (<email>) — <trích nguyên văn câu duyệt>"
approval_scope: "<đúng phạm vi đã duyệt>"
approved_at: "<ISO timestamp>"
```

Không ghi "user approved" chung chung — phải trích được câu duyệt thật.
