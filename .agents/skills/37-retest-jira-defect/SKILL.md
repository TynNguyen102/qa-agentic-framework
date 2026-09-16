---
name: 37-retest-jira-defect
description: Retest a Jira defect by reading the full defect and comments, identifying the fix build and change delta, rerunning the original failure and related regression, and producing a controlled verdict. Use after a fix is delivered.
---

# Retest Jira Defect

Do not retest from the summary alone.

## Procedure

1. Read the defect, comments, attachments, linked requirement/testcase/execution, fix version, changed build, deployment notes, and prior evidence.
2. Read the cross-sprint manifest at `Projects/<ACTIVE_PROJECT>/Defects/<local_id>/manifest.yaml` if one exists — reuse its fingerprint, `traceability`, and `regression.testcase_ids`/`automation_paths` instead of rediscovering them. Confirm the trigger against `Config/QA-Agent/defect-register-schema.yaml`'s `ready_for_retest_trigger` (fix build/version, deployment environment, change delta must come from a read Jira status/comment/field, never assumed from elapsed time).
3. Reconstruct the original environment, role, data, state, and minimum reproduction. Identify the fix delta and nearby regression risk.
4. Use fresh sessions and controlled data. Re-run the original failing path, important boundaries, and directly affected scenarios.
5. Verify the visible behavior and authoritative API, DB, event, audit, or downstream readback.
6. Assign exactly one verdict:
   - `PASS_FIXED`
   - `FAIL_REPRO`
   - `BLOCKED`
   - `NEED_CLARIFY`
   - `PARTIAL_PASS_WITH_GAP`
7. Update the manifest: `fixed_in_sprint`, append the current sprint once to `retested_in_sprints`, update `retest.fix_build/executed_at/verdict/evidence/residual_risk`, and set `lifecycle_status` per the verdict (`PASS_FIXED` with regression still owed → `REGRESSION_PENDING`; `FAIL_REPRO` → `REOPEN_RECOMMENDED`; `BLOCKED`/`NEED_CLARIFY` → `RETEST_BLOCKED`). Do not set `VERIFIED` here — that requires the regression result too (see `32-smoke-regression-testing`).
8. Create a local retest draft by default. Add Jira comments, transition status, or close/reopen only with explicit approval, then read back the result.

## Output Contract

Return defect/build/environment, source material reviewed, original-path result, related regression result, evidence, verdict, residual risk, manifest path updated, and proposed Jira update.
