---
name: 09-review-testcases
description: Review functional, API, UI, data, mobile, or non-functional testcases for correctness, coverage, traceability, maintainability, execution readiness, and test management tool compatibility (QMetry, TestRail). Use before testcase approval, import, automation, or regression inclusion.
---

# Review Testcases

Read `Config/QA-Agent/professional-coverage-model.yaml`; read `api-coverage-profile.yaml` for API/backend/event cases. Review against the approved denominator, not testcase count.

## Review gates

1. Validate title using the configured title profile; otherwise report `NEED_CONFIG: TESTCASE_TITLE_FORMAT`.
2. Build or validate the Rule Inventory and expected-result traceability. Require source/version for derived `CHANGE`, `DECISION`, cross-entity, bypass, diagram or flow rules; keep unapproved items `NEED_CONFIRM`.
3. Check atomic intent, prerequisites, roles, state, test data, deterministic steps, business expected result, readback oracle, cleanup, and evidence. Spot-check that field/column/label names quoted in expected results match the confirmed requirement doc verbatim, not a mockup shorthand — a suite-wide label mismatch (e.g. "Score" vs the AC's "Anomaly Score") is a REWORK finding, not a nitpick, since it breaks search/mapping for anyone reusing the suite later.
4. Audit all applicable coverage dimensions and depth triggers. For each coverage unit, verify source/risk, case linkage, oracle layers, owner and state; score `COVERED`, `PARTIAL`, `GAP`, `N/A_WITH_REASON`, `BLOCKED` or `NEED_CONFIRM`. Do not use arbitrary group-count thresholds.
5. Detect duplicates, contradictions, untestable expectations, excessive coupling, flaky setup, and automation hazards.
6. If test-management output is in scope, validate the candidate mapping (QMetry column layout or TestRail field mapping, per whichever tool `qa-config.yaml` names) separately from target-project import readiness. Do not treat an execution/results table as the same schema as the case-creation schema.
7. Propose supplemental cases as a patch/draft. Do not modify the approved source merely to make a gate pass.

## Drift re-review (when the story/AC changed after testcases existed)

When a story or its acceptance criteria change mid-sprint, run a conservative drift pass over the existing testcases — read-only, propose only (per gate 7):

- Compare each current AC against the existing testcase coverage (and the test-design coverage matrix if present).
- Produce four lists: **New ACs needing coverage** (AC with no case) · **TCs to review** (a step/expected now conflicts with the changed AC) · **Stale TCs** (reference an AC that was removed/renamed) · **Scripts to review** (automation whose underlying case changed).
- Be conservative — flag anything that MIGHT be affected, not only obvious breaks. An additive-only change → focus on missing coverage; a removal/rename → surface stale cases and their script references.
- Never auto-delete or auto-edit a case; deletions need explicit QC-Lead confirmation. End with a Next-actions checklist (add / review / delete-after-confirm / regenerate).

### Common drift scenarios

| Story/AC change | Typical drift level | Action |
|---|---|---|
| AC wording clarified, meaning unchanged | 0 (none) | No change; note only |
| AC scope expanded (e.g. "edit name" → "edit name, description, owner") | 1 (minor) | Update affected TCs; add cases for the new scope |
| AC deleted / feature removed | 1 (minor) | Flag covering TCs stale; delete-after-confirm or move to regression |
| AC renamed / re-numbered | 1 (minor) | Re-point traceability; flag scripts referencing the old ID |
| ≥3 ACs added/removed/significantly rewritten, or feature scope changed | 2 (major) | Treat as re-design; re-run test-design/generation for the affected area |

Drift-level thresholds (quantified): **0 = none** (wording only, meaning unchanged) · **1 = minor** (1–2 ACs added/changed, none removed, existing cases mostly valid) · **2 = major** (≥3 ACs added/removed/rewritten, or scope changed). Level only sizes the effort; deletions still need explicit QC-Lead confirmation (never auto-delete).

## Output

Return recommendation per case: `RECOMMEND_APPROVAL`, `APPROVE_WITH_EDITS_CANDIDATE`, `REWORK`, `BLOCKED`, or `NEEDS_CONTEXT`; include denominator/state counts, findings by risk, missing/untraceable units, false-coverage warnings, proposed corrections, residual risk, and readiness summary. Never claim human/QA Lead approval or enforce legacy SLA/sign-off rules that are not configured.
