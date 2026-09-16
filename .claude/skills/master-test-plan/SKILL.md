---
name: master-test-plan
description: Produce a Master Test Plan & Strategy for a project/milestone (MVP, launch, major release) spanning multiple sprints — strategy, entry/exit criteria, NFT breakdown, KPIs, and approval. Use for project/milestone kickoff, not for a single sprint (`02-sprint-test-plan`) or a single US/feature (`03-feature-test-plan`).
---

# Master Test Plan

> Token note: for a small milestone or a quick strategy question, generate directly without reading every section below. Read fully when producing the complete document or when the boundary against sprint/feature plans is unclear.

Scope: the active project only (`project/active-project.yaml`). Reference framework: `Config/QA-Agent/standards-profile.yaml` (ISTQB/ISO 29119-style process, ISO 25010 quality model) — cite only the edition recorded there, and note if it's still `PROPOSED_PENDING_QA_LEAD_APPROVAL`.

## Boundary — Master Test Plan vs Sprint/Feature Plan

This skill owns the **strategic, cross-sprint** layer. Do not duplicate tactical detail owned elsewhere:

| Master Test Plan (this skill) | Sprint/Feature Plan (`02`/`03`) |
|---|---|
| Strategy matrix by risk group (4-5 rows) | Per-feature automation % detail |
| Entry/Exit criteria for the whole milestone | Per-sprint entry/exit gates |
| NFT types + approach + owner | Concrete NFT scenario execution |
| Phase-level schedule, reverse-planned from go-live | Task-by-task sprint schedule |
| One consolidated AI-usage governance reference | — |

If asked for sprint- or feature-level detail, redirect to `02-sprint-test-plan` / `03-feature-test-plan` instead of inflating this document.

## Read first

1. Read `Projects/<ACTIVE_PROJECT>/qa-config.yaml` for project identity, sprint template, and automation profile pointers.
2. Read `Config/QA-Agent/assurance-levels.yaml` and `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml` for what this session is actually authorized to execute vs. only plan.
3. Read `governance/knowledge-policy.yaml` for which knowledge sources are `APPROVED` oracles — do not use another project's rules or unapproved sources as this project's expected behavior.
4. If an AI-usage/data-handling governance section exists (e.g. a PII/secrets policy in `governance/`), cite it in the AI Policy section below rather than inventing rules inline. If none exists yet, mark that row `NEED_CONFIG` — do not silently omit it.
5. **Mandatory diagram check**: when reading a Jira issue or Confluence page as a requirement source, check for attached/embedded images (flowcharts, sequence diagrams, wireframes) and read them before analyzing — they often carry constraints the text doesn't state.

## Inputs

| Info | Required |
|---|---|
| Epic/US list in scope for this milestone (Jira keys, summaries, status) | ✅ |
| Milestone timeline (start–end) | ✅ |
| QA team and roles (`Team/Members/` if configured, otherwise ask) | ✅ |
| Environments and tools in scope | ✅ |
| Project/milestone/version name | ✅ |

Missing info → write `[Cần bổ sung]` and ask. Do not guess.

## Procedure

1. Pull the epic/US list for the milestone via Jira (Atlassian MCP); for each, read linked Confluence FRS and check for diagrams per the mandatory check above.
2. If `01-review-requirements` has already run on these US, reuse its requirement/AC matrix and risk findings instead of re-deriving them.
3. Draft the 11 sections below. Use `[Cần bổ sung]` / `NEED_CONFIRM` for anything not sourced from an approved reference — never invent a number, threshold, or name.
4. Cross-check against `Config/QA-Agent/assurance-levels.yaml` before writing any Entry/Exit criterion that implies test execution — do not promise an execution level the current session isn't authorized for.
5. Save as a new, non-overwriting file at `Outputs/cross-sprint/MasterTestPlan/MasterTestPlan_<project_key>_<milestone>_v<n>_<yyyy-mm-dd>.md` — this spans sprints, so it does not belong under a single `Projects/<Sprint>/Outputs/` folder (same reasoning as `Projects/<ACTIVE_PROJECT>/Defects/` living at the root, not per-sprint).
6. Draft only by default. Publishing to Confluence or linking from Jira requires anh's explicit approval this session.

## The 11 sections

1. **Thông tin chung** — project/milestone name, doc code, author, approvers, scope of features covered.
2. **Phạm vi kiểm thử** — In scope / Out of scope / test types applied (Functional, NFT, UAT...).
3. **Phương pháp & Chiến lược** — see subsections below.
4. **Entry Criteria** — condition, confirmed by whom, confirmed how (not just "environment ready").
5. **Exit Criteria** — split into Part A (Test Completion, QC decides) and Part B (Go-Live Decision, PM/Product decides); Part A must also list explicit **FAIL conditions**, not only pass thresholds.
6. **Suspension & Resumption Criteria** — concrete thresholds (%, hours), never vague.
7. **KPI & Metrics** — pass rate (overall + highest-risk group), Defect Removal Efficiency (DRE = bugs found in QA / (bugs QA + bugs found in UAT/Prod); target ≥95% for compliance/PII-sensitive scope, ≥85% otherwise), automation coverage (milestone-based, not flat), TC execution rate, audit/privacy compliance violations (=0, hard requirement), health score only if its formula/weights/baseline are configured (`33-test-reporting` note applies here too).
8. **Schedule** — phase-level (4-6 rows, not task-by-task), reverse-planned from the go-live date backward through UAT sign-off, SIT, functional test end. Include a capacity check (total effort / (capacity per sprint × sprint count) = utilization%).
9. **Team & Environment** — roles from `Team/Members/` if configured, environments/accounts from `Projects/<ACTIVE_PROJECT>/qa-config.yaml` / `Config/<PROJECT>_ENV.*.yaml`.
10. **Risks & Contingency** — ≥4 concrete, project-specific risks, not generic filler.
11. **Deliverables & Approval** — deliverables table + a real sign-off table (role, name, date) — QC Lead and PM at minimum; add Compliance/Legal if the milestone touches Privacy/PII/data-governance features.

### 3.1 Manual vs Automation

Table by test type: method, **milestone-based** automation target (ramp up over the project, not flat), framework (pull from `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml` / `automation-structure.yaml` — do not invent a framework name). One line for design techniques used (EP/BVA/decision table/state transition/OWASP), not a separate section.

### 3.2 AI Usage in this QA process

One consolidated table: AI-assisted activity → mandatory human review → data constraint. **Do not write the data-handling rule inline here** — cite it from the governance policy (`governance/knowledge-policy.yaml` or the dedicated data-handling policy once it exists). If that policy doesn't exist yet, this row is `NEED_CONFIG: AI_DATA_HANDLING_POLICY` — flag it, don't invent it.

### 3.3 Strategy Matrix

By risk group (Rất cao / Cao / Trung bình / Thấp), 4-5 rows — not one row per feature. Representative features, test types applied, coverage target per group.

### 3.4 NFT Breakdown

Per NFT type in scope: scope, tool, target metric, **owner** (Security testing is normally owned by the Security team with QA supporting environment/evidence — do not assume QA owns it unless confirmed). If any NFT target is `TBD` in the source requirements, generate an explicit **NFR Open Questions** table (question, why it matters, impact if unanswered, who should answer, deadline) instead of leaving a silent placeholder — an NFT result without a real SLA target has no sign-off value.

## AI Policy row status

Until the workspace has a dedicated AI/data-handling governance policy, mark section 3.2's data-constraint column `NEED_CONFIG: AI_DATA_HANDLING_POLICY` in every plan produced by this skill, and say so explicitly in the output — do not silently skip it or invent placeholder legal text.

## Output Contract

Return the file path, the 11-section document, any `NEED_CONFIRM`/`NEED_CONFIG` items (especially the AI Policy row and any NFR open questions), and a one-line pointer to `02-sprint-test-plan` for the next tactical step once the milestone's first sprint starts.

Return `DONE` only when all 11 sections are present with no unexplained placeholder; use `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED` otherwise.
