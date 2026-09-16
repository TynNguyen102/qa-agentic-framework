# SKILL.md — Workspace Router Summary

This is a **multi-project QA control plane**: one shared Core (47 numbered/support skills, coverage model,
governance mechanism, canonical schema) routed by `.agents/skills/qa-router/` against
whichever project is active. Each project's own knowledge, config, defects, and state live in
`Projects/<name>/` — currently just `Projects/Example-Project/` (the first real project, active
since 2026-08-26).

## Resolve the active project first

Read `project/active-project.yaml`. If it lists more than one project and the user hasn't said
which one this request is about, ask rather than guessing. Everywhere below, `<ACTIVE_PROJECT>` means the resolved project's folder name.

## Route

See `.agents/skills/qa-router/SKILL.md` for the full routing table, mandatory gates, and
typical skill chains (new US, sprint, defect, API, automation, etc.). In short:

1. Read `README.md`, `AGENTS.md`, this file, `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md`,
   `Projects/<ACTIVE_PROJECT>/qa-config.yaml`, `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml`,
   and `Config/QA-Agent/professional-coverage-model.yaml`.
2. Pick the narrowest numbered skill (01-44) or support skill matching the request; route
   unscreened issues through `39-issue-triage` first.
3. Keep scope limited to `<ACTIVE_PROJECT>` — never borrow another project's rules, data, or
   environment as truth for this one.
4. Apply `governance/knowledge-policy.yaml`: only `APPROVED` knowledge is a PASS/FAIL oracle.
5. Draft locally by default. Live Jira/QMetry/Confluence/Git/environment/data mutation requires
   explicit approval in the current session.

## Format gates (apply across skills)

- Testcase titles must validate against `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml`.
- Defect titles/sections must validate against `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml`.
- QMetry output must validate against `Projects/<ACTIVE_PROJECT>/Config/qmetry-profile.yaml` and
  stay blocked from live import while `validation.live_import_allowed` is false.
- Never claim PASS from HTTP status alone, or complete/zero-bug coverage without the denominator
  and residual risk `Config/QA-Agent/professional-coverage-model.yaml` requires.
