---
name: 33-test-reporting
description: Produce an evidence-based test report from approved plans, testcase execution, automation results, coverage, defects, blockers, and residual risks. Use for sprint, feature, cycle, or release reporting.
---

# Test Reporting

Do not fabricate counts or infer pass status from missing evidence.
Read `Config/QA-Agent/professional-coverage-model.yaml`; report its state funnel against an explicit denominator.

## Procedure

1. Define reporting period, scope, build, environments, sources, and snapshot time.
2. Reconcile planned, designed, approved, executed, passed, failed, blocked, not executed, and unclear cases using explicit source records.
   - Define snapshot grain such as testcase + cycle + build + environment and retain execution history.
   - Label `passed/(passed+failed)` as executed pass rate; report execution, blocked and not-run rates with explicit denominators.
3. Summarize coverage units by NOT_ASSESSED/NEED_CONFIRM/DESIGNED/REVIEWED/AUTOMATED/EXECUTED/PROVEN and exceptions, then requirement/risk coverage, defects, retest, blockers and environment issues.
4. Evaluate entry/exit criteria and explain deviations, exclusions, and data freshness.
   - Use `N/A`, `NOT_TESTED` or `OUT_OF_SCOPE` for untested categories; never convert missing testing into 100%.
   - Calculate a health score only when its formula, weights, baseline and owner are configured.
   - Optional supplementary tables to present (presentation only, not new metrics): a layer breakdown (UI / API / DB / E2E case + automation counts), automation-progress by test type, and a bug severity × status matrix; and three report depths — Level 1 (~1 page: exec summary + coverage + risks + next steps), Level 2 (~3–5 pages: + layer breakdown, automation, bug metrics, action items), Level 3 (~10 pages: + per-feature detail, full risk register, historical trends). These are layout aids only — do NOT introduce a hard weighted Readiness formula; a health score is still computed only when its formula/weights/baseline/owner are configured (per the line above).
5. State residual business risk and a recommendation with supporting evidence.
6. Create a local draft by default. Publish to Jira, Confluence, or the configured test management tool (QMetry/TestRail) only with explicit approval and read back the result.

## Output Contract

Return executive summary, scope/build/environment, source timestamp, denominator and state counts, execution metrics with formulas, false-coverage warnings, defects, blockers/exclusions, residual risks, exit-criteria result, recommendation basis and evidence links.

## Bổ sung 2026-09-07 — Chưng cất kiến thức bền vững (bắt buộc khi đóng US/sprint)

Sau khi execute/đóng một US, các fact BỀN VỮNG phải được cất vào nơi có cấu trúc để US sau recall được — KHÔNG để trôi trong log/Jira comment:

- **Invariant nghiệp vụ đã xác nhận / quyết định expected đã chốt** (vd "chỉ áp file mới, không backfill"; quyền thực hẹp hơn tên role) → ghi vào `Knowledge-Base/Domain-Rules/<module>/_overview.md` (tạo nếu chưa có), kèm nguồn + trạng thái APPROVED/DRAFT.
- **Cross-screen / cross-module effect mới phát hiện** → bảng cross-screen trong `_overview.md` của module.
- **Defect mới / đổi trạng thái** → cập nhật `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md` (module → finding) NGAY, song song với `manifest.yaml`.

Ghi rõ trong report là đã chưng cất (hoặc "không có fact bền vững mới"). Đây là mặt còn lại của recall-gate ở skill `01`: có chưng cất thì lần sau mới recall được.
