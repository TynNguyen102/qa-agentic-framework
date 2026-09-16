---
name: 24-test-coverage-audit
description: Audit requirement, risk, business rule, state, role, data, integration, non-functional, automation, execution, and defect traceability. Use to identify false confidence and prioritized coverage gaps.
---

# Test Coverage Audit

> **Tóm tắt (VI):** Rà coverage theo denominator + rủi ro (không đếm testcase), lộ chỗ thiếu/trùng/blocked, báo residual risk. Dùng khi cần đánh giá "đã phủ đủ chưa".

Coverage is evidence of mapped behavior and risk, not merely a testcase count.
Read `Config/QA-Agent/professional-coverage-model.yaml` and use its coverage-unit/state/denominator rules. For API scope also read `api-coverage-profile.yaml`.

## Procedure

1. Audit breadth first: enumerate coverage units from the approved feature/module profile. If none exists, create a draft denominator from the canonical model and report `NEED_CONFIRM: COVERAGE_DENOMINATOR` rather than calculating a percentage.
2. Build the chain: requirement or rule -> risk -> condition -> testcase -> automation -> execution -> evidence -> defect.
3. Audit roles and permissions, state transitions, decisions, data classes, boundaries, integrations, failure modes, platforms, environments, config parity and applicable non-functional qualities.
4. Detect missing, duplicate, stale, ambiguous, permanently blocked, and untraceable cases.
5. Distinguish NOT_ASSESSED, NEED_CONFIRM, DESIGNED, REVIEWED, AUTOMATED, EXECUTED and PROVEN plus terminal exceptions. Do not infer state from file presence, filename suffix, green dashboard or HTTP status.
6. Route depth gaps to workflow 26 after breadth gaps are visible; rank gaps by business impact, likelihood, change exposure, detectability, and release timing.

## Quick automation-coverage sub-check (TC ↔ spec)

A fast, read-only reconcile of one module/feature's testcases against its automation spec — complements, does not replace, the breadth audit above:

- Extract testcase IDs from the canonical testcase records and the `test(...)` / `test.fixme(...)` / `test.skip(...)` IDs from the spec file(s).
- Classify each: **Automated** (in both, active test) · **Fixme** (`test.fixme` — selector unresolved) · **Skipped** (`test.skip` — data-dependent) · **Missing** (testcase with `automation_candidate` `Yes`/`Partial` but absent from spec) · **Manual-only** (`automation_candidate: No` — excluded from the denominator, listed separately, never counted as Missing) · **Orphaned** (spec test whose ID is in no testcase — likely typo or a removed case).
- Coverage % = Automated ÷ automatable (denominator excludes Manual-only, per this project's `canonical-testcase-schema.yaml`). Report the lists, not just the number.
- Mechanical index only: "Automated" here means a spec exists, NOT that it passed — keep the state labels of Procedure step 5 (a green or merely-present test is not `PROVEN`). Read-only — propose gaps, never edit spec/testcases here.

## Output Contract

Return a coverage-unit matrix, denominator/state counts and calculation rules, gaps, false-coverage warnings, obsolete assets, risk priority, owner, residual risk and recommended workflow to close each gap. Never return 100% while required units are NEED_CONFIRM, BLOCKED, NOT_ASSESSED or OUT_OF_SCOPE.

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
