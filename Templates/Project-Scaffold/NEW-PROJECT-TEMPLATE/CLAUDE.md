# CLAUDE.md - QA Workspace Context (NEW-PROJECT placeholder)

> Rename this folder (`Projects/NEW-PROJECT/`) and this file's content once the real project
> name/domain is known, and update `active_project` in `project/active-project.yaml` to switch
> the workspace default to it. Everything below is a scaffold — no real fact yet.

This workspace is dedicated to **<PROJECT NAME — NEED_CONFIRM>** QA work.

## Must Follow

- Read `README.md`, `SKILL.md`, `Projects/NEW-PROJECT/CURRENT_STATE.md`, this file, `qa-config.yaml`
  in this folder and the gitignored `qa-config.local.yaml` overlay when present,
  `Config/agent-profile.yaml` (this folder), and `governance/knowledge-policy.yaml` before acting.
- Do not use another project's business rules, permission matrix, Jira state, QMetry folders, or
  test data as this project's expected behavior unless explicitly approved.
- Use live Jira/Confluence/API specs when available; local files are cached references.
- Only `APPROVED` knowledge may be used as a PASS/FAIL oracle. Do not self-promote knowledge
  state, competency level, or execution readiness.
- Live updates require explicit user approval in the current session.
- Use `Config/QA-Agent/professional-coverage-model.yaml` for the shared coverage denominator and
  `Config/QA-Agent/api-coverage-profile.yaml` for API/event scope; report evidence states and
  residual risk instead of claiming zero defects.

## Daily Workflow

1. Check current sprint config.
2. Check Jira for US/defects needing QA.
3. Check Confluence/API spec changes.
4. Update local state/report under `Projects/NEW-PROJECT/`.
5. Execute only approved or requested work.
