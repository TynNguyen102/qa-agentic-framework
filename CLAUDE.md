# CLAUDE.md - QA Workspace Context

This workspace is a **multi-project QA control plane** (Core framework: 51 skills, coverage
model, governance mechanism) shared across projects, each living in its own `Projects/<name>/`
folder with its own knowledge, config, defects, and state.

## Must Follow

- Read `project/active-project.yaml` first to resolve `<ACTIVE_PROJECT>` — do not assume a
  project when the file lists more than one, or when the user names a different one explicitly.
- Then read `SKILL.md`, `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md`,
  `Projects/<ACTIVE_PROJECT>/CLAUDE.md` (project-specific must-follow rules and scope), the
  project's `qa-config.yaml` and gitignored `qa-config.local.yaml` overlay when present,
  `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml`, and `governance/knowledge-policy.yaml`
  before acting. (`README.md` is human onboarding — read it on demand, not every session; the
  operating contract for the agent lives in this file + `SKILL.md` + skill descriptions.
  `CURRENT_STATE.md` is kept lean — its historical log is in `CURRENT_STATE-archive.md`, load only
  when you need past-session history.)
- Do not borrow another project's business rules, permission matrix, Jira state, QMetry folders,
  or test data as this project's expected behavior unless explicitly approved.
- Use live Jira/Confluence/API specs when available; local files are cached references.
- Only `APPROVED` knowledge (per that project's governance state) may be used as a PASS/FAIL
  oracle. Do not self-promote knowledge state, competency level, or execution readiness.
- Live updates require explicit user approval in the current session.
- **Định dạng câu trả lời (ghim 2026-09-16, Lead chốt — cổng G6).** Mọi mã Jira nhắc trong câu trả
  lời phải là link bấm được `[DEMO-1234](https://YOUR-SITE.atlassian.net/browse/DEMO-1234)`, kể cả khi
  nhắc lại ticket cũ. Mọi file trong workspace phải là link tương đối bấm được `[tên](đường/dẫn.md)`,
  không viết path trần trong backtick. Kết quả trả về bằng BẢNG, không phải văn xuôi. Luật đầy đủ ở
  `Projects/<ACTIVE_PROJECT>/CLAUDE.md` — ghim ở đây vì luật nằm trong file project dễ bị bỏ sót khi
  phiên không mở file đó (đã xảy ra 2026-09-16).
- Use `Config/QA-Agent/professional-coverage-model.yaml` for the shared coverage denominator and
  `Config/QA-Agent/api-coverage-profile.yaml` for API/event scope; report evidence states and
  residual risk instead of claiming zero defects.

## Daily Workflow

1. Resolve the active project (`project/active-project.yaml`, or ask if ambiguous).
2. Check that project's current sprint config.
3. Check Jira for US/defects needing QA.
4. Check Confluence/API spec changes.
5. Update that project's local state/report under `Projects/<ACTIVE_PROJECT>/`.
6. Execute only approved or requested work.
