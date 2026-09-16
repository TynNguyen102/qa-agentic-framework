---
name: 13-execute-approved-testcases
description: Execute approved testcases professionally with environment checks, risk-based ordering, business readback, evidence capture, and controlled status reporting. Use when the user asks to perform an approved test run.
---

# Execute Approved Testcases

Execute only the explicitly approved scope. Do not silently expand a run or mutate an environment beyond the configured assurance level.
Read `Config/QA-Agent/professional-coverage-model.yaml`; preserve linked coverage-unit IDs and never promote an unexecuted unit from design/automation to execution.

## Procedure

1. Record testcase version, build, environment, service health, accounts and roles, test data, dependencies, entry criteria, and known incidents.
2. Order execution by business risk and dependency: build viability, critical journeys, changed areas, integration paths, then broader coverage.
3. Use the appropriate method: guided manual test, browser automation, API test, DB reconciliation, exploratory session, or approved non-functional tool.
4. Capture actual results and timestamped evidence. Verify every required oracle layer; set a coverage unit `PROVEN` only when all scoped business/readback assertions pass for the stated build/environment.
5. Assign only these statuses:
   - `PASS`: all expected business and readback results are proven.
   - `FAIL`: a reproducible deviation is evidenced.
   - `BLOCKED`: a named dependency prevents execution.
   - `NOT_EXECUTED`: outside the completed run.
   - `NEED_CLARIFY`: expected behavior cannot be determined from an authoritative source.
6. Preserve failed state where useful, collect diagnostics safely, and route confirmed defects to workflow 36. Do not update Jira or the test management tool live without explicit approval.
7. If a test management update is approved, map only evidence-backed testcase results from this ledger and read them back (QMetry execution update, or a TestRail run/result push per `testrail-profile.yaml`'s `run_and_results.status_id_mapping`). Never create an execution/result entry and mark it PASS without the corresponding completed assertions and evidence.

## Output Contract

Return an execution ledger with testcase and coverage-unit IDs, build, environment, status, actual result, oracle-layer evidence, defect link or draft, denominator state changes, blockers, unexecuted units and residual risk.

## Bổ sung 2026-09-07 — Chưng cất kiến thức bền vững (bắt buộc khi đóng US/sprint)

Sau khi execute/đóng một US, các fact BỀN VỮNG phải được cất vào nơi có cấu trúc để US sau recall được — KHÔNG để trôi trong log/Jira comment:

- **Invariant nghiệp vụ đã xác nhận / quyết định expected đã chốt** (vd "chỉ áp file mới, không backfill"; quyền thực hẹp hơn tên role) → ghi vào `Knowledge-Base/Domain-Rules/<module>/_overview.md` (tạo nếu chưa có), kèm nguồn + trạng thái APPROVED/DRAFT.
- **Cross-screen / cross-module effect mới phát hiện** → bảng cross-screen trong `_overview.md` của module.
- **Defect mới / đổi trạng thái** → cập nhật `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md` (module → finding) NGAY, song song với `manifest.yaml`.

Ghi rõ trong report là đã chưng cất (hoặc "không có fact bền vững mới"). Đây là mặt còn lại của recall-gate ở skill `01`: có chưng cất thì lần sau mới recall được.
