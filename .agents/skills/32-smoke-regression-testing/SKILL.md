---
name: 32-smoke-regression-testing
description: Select and execute smoke or regression suites using build viability, change impact, business risk, traceability, and diagnostic evidence. Use for release gates and post-change confidence.
---

# Smoke and Regression Testing

Read `Config/QA-Agent/professional-coverage-model.yaml`; select from approved coverage units and preserve their evidence states.

Classify the requested run before selecting tests:

- Smoke proves the build and its critical integrations are testable.
- Retest reruns the original defect failure and belongs to workflow 37; it is not automatically a sanity or smoke result.
- Sanity checks the changed area and immediate dependencies and belongs to workflow 31.
- Impacted regression covers affected behavior and dependencies.
- Full regression covers the agreed release baseline.

## Procedure

1. Record build, environment, deployment changes, feature flags, migrations, affected services, and known incidents.
2. Select tests from coverage units, traceability, changed code/components, defect history, risk, dependency graph and critical journeys. Discover open defect manifests (`Projects/<ACTIVE_PROJECT>/Defects/*/manifest.yaml` with `lifecycle_status: REGRESSION_PENDING`) and include each one's `regression.testcase_ids`/`automation_paths` in scope — a defect is not release-safe until its own regression has run.
   - At sprint close, inspect `Projects/<PROJECT>/BusinessJourneys/<SPRINT_ID>/` (resolve `<PROJECT>` from the active project's `robot-framework-profile.yaml` mapping) in the resolved official Robot repository and the cross-US journey map. Report missing journey automation as a coverage gap rather than silently claiming it was generated.
3. Execute stable tags or approved manual cases with isolated data and evidence.
4. Triage failures into product defect, automation defect, environment issue, data issue, or known issue; never report only a green/red dashboard.
5. For each defect manifest covered in this run, update `regression.last_result/last_run_at/evidence`. If `last_result: PASS` and the manifest's `retest.verdict` is already `PASS_FIXED`, set `lifecycle_status: VERIFIED`; otherwise leave it `REGRESSION_PENDING` and state why.
6. Reconcile critical business effects and state release limitations explicitly. Do not call a run “full regression” unless its approved denominator and all exclusions are reported.

## Output Contract

Return run type, selection rationale, coverage-unit/suite/case IDs, build/environment, pass/fail/block counts with source data, denominator state changes, failure triage, evidence, coverage limits/exclusions, defect manifests updated, residual risk and release recommendation.
