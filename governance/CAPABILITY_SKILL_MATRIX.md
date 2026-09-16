# Capability → Skill → Schema → Eval Matrix

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> Trả lời một câu hỏi: *"Capability này do skill nào làm, ra output theo schema nào, và eval nào bảo vệ nó?"*
> Cột **Eval** là chỗ dễ trống nhất — trống nghĩa là capability đó **không có gì bảo vệ khi regress**.

## Ký hiệu

`✅` có · `⚠️` một phần · `❌` chưa có · `🕐` có nhưng stale

## Ma trận

| Capability | Skill | Output schema | Eval case | Gate |
|---|---|---|---|---|
| Requirement analysis | `01` | `schemas/requirement-intake.schema.yaml` ✅ | P0-001 ✅ | — |
| Document ingestion | `01` | `requirement-intake` `intake_types` ✅ | ❌ | — |
| **Conflict detection** | **`42`** ✅ | `schemas/conflict-report.schema.yaml` ✅ | CF-001/002/003 ✅ *(chưa chạy)* | **G1** |
| Domain knowledge | `knowledge-policy.yaml` | `required_rule_fields` ✅ | ZT-002, ZT-011 ✅ | G8 |
| **Risk & change impact** | **`43`** ✅ | trong SKILL.md `output_contract` ⚠️ | RK-001..004 ✅ *(chưa chạy)* | — |
| **Test-type recommendation** | **`44`** ✅ | checklist trong SKILL.md ⚠️ | TA-001/002/003 ✅ *(chưa chạy)* | **G2** |
| Test planning | `02`,`03`,`master-test-plan` | — ❌ | ❌ | — |
| Test-case generation | `05`,`06`,`07`,`08` | `canonical-testcase-schema.yaml` ✅ | P0-002, P0-003, P0-018 ✅ | — |
| Coverage analysis | `24` | `professional-coverage-model.yaml` + `TEST_COVERAGE_MODEL.md` ✅ | ZT-009, ZT-010, P0-012, P0-017 ✅ | **G2** |
| Test-data generation | `10` | `test-data-readiness.yaml` ⚠️ | ❌ | **G4** |
| UI testing | `21`,`28` | `ui-pattern-checklists/` ⚠️ | P0-014, P0-020 ✅ | — |
| UX review | `16` | — ❌ | ❌ | — |
| API testing | `08`,`14`,`22` | `api-coverage-profile.yaml` ✅ | P0-003, P0-018, P0-019, P0-022 ✅ | — |
| Database testing | `34`,`38` | `assurance-levels.yaml` ✅ | ❌ | **G4** |
| Security testing | `23` | `standards-profile.yaml` ✅ | P0-022 ✅ | **G3** |
| Performance & reliability | `25`,`17`,`20`,`27` | `assurance-levels.yaml` L4 ✅ | ❌ | **G3** |
| Accessibility | `07`,`19` | WCAG 2.2 AA ✅ | ❌ | — |
| AI/LLM testing | `40` | `standards-profile.yaml` `ai_testing` ⚠️ *PROPOSED* | RK-004 ✅ *(chưa chạy)* | — |
| Integration testing | `14`,`22`,`35` | — ⚠️ | P0-021 ✅ | — |
| End-to-end testing | `28`,`15` | — ❌ | P0-015 ✅ | — |
| Deep testing | `26` | `router-policy.yaml` `deep_test_scheduling` ✅ | ❌ | — |
| Exploratory testing | `18` | — ❌ | ❌ | — |
| Bug hunting | `30` | `bug-basis-profile.yaml` ✅ | ❌ | — |
| **Test execution** | `13` | `schemas/test-result.schema.yaml` ✅ | ZT-003, ZT-004, EX-001/002 ✅ *(EX chưa chạy)* | — |
| **Evidence management** | `13` và mọi execution skill | `test-result.schema.yaml` `evidence_record` ✅ | ZT-006 ✅ | — |
| Defect validation | `39` | `bug-basis-profile.yaml` + `DEFECT_VERIFICATION_POLICY.md` ✅ | ZT-007, P0-008, P0-009, EX-003/004 ✅ *(EX chưa chạy)* | **G5** |
| Jira logging | `36` | `defect-profile.yaml` ✅ | ZT-005, P0-005 ✅ | **G9** |
| Automation generation | `11`,`12` | `robot-framework-profile.yaml` ⚠️ *(chưa vendor-neutral)* | P0-013, P0-016 ✅ | — |
| Regression selection | `32` | `router-policy.yaml` `suite_classification` ✅ | ❌ | **G7** |
| CI/CD integration | `.gitlab-ci.yml`, `.github/workflows/` | — ⚠️ | ❌ | **G7** |
| **Multi-agent orchestration** | `qa-router` | `schemas/execution-plan.schema.yaml` ✅ | OR-001..004 ✅ *(chưa chạy)* | — |
| Token/cost optimization | — ❌ | — ❌ | ❌ | — |
| Beginner guidance | `44` ✅ | checklist ⚠️ | TA-001 ✅ *(chưa chạy)* | — |
| Human review gates | tất cả | `HUMAN_APPROVAL_GATES.md` ✅ | ZT-005, ZT-008 ✅ | G1–G9 |
| Quality evaluation | `evals/qa-agent/eval-suite.yaml` | `schemas/confidence-report.schema.yaml` ✅ | ✅ **baseline `CURRENT_20260916`** — chạy 53/53 case ngày 16/09 | — |
| Learning & feedback | `learning-profile.yaml` ⚠️ | — ❌ | ❌ | G6 |
| Git governance | `git-collaboration.yaml`, `CODEOWNERS` | — ✅ | ❌ | G6 |
| Traceability & audit | `audit-policy.yaml` | ⚠️ *lệch thực tế, xem `known_divergence`* | ❌ | — |

## Đọc ra được gì từ bảng này

**Capability không có eval bảo vệ (14):** document ingestion, test planning, test-data generation,
UX review, database testing, performance, accessibility, exploratory, bug hunting, regression
selection, CI/CD, token optimization, learning loop, git governance, traceability.
→ Những chỗ này nếu regress sẽ **không ai biết** cho tới khi lọt lỗi thật.

**Capability chưa có output schema (9):** test planning, UX review, E2E, exploratory,
integration (một phần), CI/CD, token optimization, learning loop.
→ Output đang là văn xuôi tự do, máy không kiểm được.

**18 eval case mới (CF/RK/TA/OR/EX) chưa từng chạy** — chúng mô tả hành vi mong muốn, chưa phải
bằng chứng hành vi thật.

## Việc kế tiếp theo thứ tự ưu tiên

1. Chạy lại toàn bộ eval-suite (baseline stale + 18 case mới) — **P0**
2. Chốt `known_divergence` của `audit-policy.yaml` (phương án A hay B) — **P0**
3. Lead confirm 3 chuẩn AI đang `PROPOSED` trong `standards-profile.yaml` — **P1**
4. `tool-adapters.yaml` để gỡ gắn cứng Robot/Playwright — **P1**
5. Eval case cho nhóm 14 capability đang trống — **P1/P2**
