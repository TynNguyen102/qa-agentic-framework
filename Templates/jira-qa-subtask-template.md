# QA Subtask Templates (Jira)

Renders `Projects/<ACTIVE_PROJECT>/Config/jira-subtask-profile.yaml` — the canonical source for these two subtasks. Project key: `NX`. Status: `PARTIAL_CONFIG` — both title formats are `NEED_CONFIG: JIRA_SUBTASK_TITLES` until anh provides them; description sections below are ready to use.

Draft locally first. Live creation requires: Jira create metadata fetched, both title formats set, and explicit approval this session. After live creation, read back key/title/fields/links.

## Subtask 1 — "Create Testcase"

Title: pending.

Description sections (in order):
1. Objective
2. Test Basis
3. Scope
4. Coverage Dimensions
5. Test Data And Roles
6. Deliverables
7. Dependencies And Blockers
8. Definition Of Done

## Subtask 2 — "Testing"

Title: pending.

Description sections (in order):
1. Objective
2. Build And Environment
3. Preconditions
4. Execution Scope
5. Evidence Paths
6. Result And Defect Links
7. Regression Impact
8. Definition Of Done

See skill `jira-test-subtasks` (`.claude/skills/jira-test-subtasks/`) for the full procedure.
