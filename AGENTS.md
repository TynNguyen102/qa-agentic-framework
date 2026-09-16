# Repository Guidelines

## Project Structure & Module Organization

This repository is a **multi-project QA workspace** — currently one active project,
`Example-Project`. Core navigation starts in `README.md`, with agent notes
in `CLAUDE.md`, `CODEX.md`, and `SKILL.md`. Resolve the active project from
`project/active-project.yaml` first. Domain references live under
`Projects/<ACTIVE_PROJECT>/Knowledge-Base/`: API specs, Confluence mirrors, DB schemas, domain
rules, test data, and traceability notes. That project's sprint/cross-sprint deliverables are in
`Projects/<ACTIVE_PROJECT>/Outputs/`; cross-project artifacts (e.g. the combined defect index) sit
in root `Outputs/`. Automation assets are split by tool: `Automation/Robot-Framework/`,
`Automation/Postman-Collections/`, `Automation/Playwright/`, and `Automation/k6/`.

## Build, Test, and Development Commands

There is no single application build. Use task-specific commands and prefer dry runs before live integrations.

```bash
python3 tools/qa_workspace.py validate
python3 tools/qa_workspace.py skills-check
python3 tools/qa_workspace.py defects-validate
k6 run --out json=Automation/k6/results/<run>.json Automation/k6/<script>.js
robot --dryrun --variablefile <robot-repo>/Variables/ENV_<PROJECT>_SIT.yaml <robot-repo>/Projects/<PROJECT>/<JIRA-KEY>/
```

## Coding Style & Naming Conventions

Keep Markdown outputs short, traceable, and evidence-based. Name sprint artifacts with sprint, module/story, and date, for example `Sprint1_ACC01_TC_20260713.tsv`. Python scripts should be snake_case and focused on one integration or report job. Do not hardcode credentials, tokens, passwords, or SIT/UAT secrets; use environment variables or ignored local config.

## Testing Guidelines

For US testing, start from Jira/Confluence/business rule, then API/UI behavior, then evidence/readback. Read `Projects/<ACTIVE_PROJECT>/qa-config.yaml`, then overlay the gitignored `Projects/<ACTIVE_PROJECT>/qa-config.local.yaml` when it exists. New Robot suites for the active project must use `Projects/<PROJECT>/<JIRA_KEY>/` in the resolved official repository (resolve `<PROJECT>` from `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml`'s project mapping). Keep shared keywords/data/variables outside story folders. Cross-US flows belong in `Projects/<PROJECT>/BusinessJourneys/<SPRINT_ID>/` after sprint journey review. Never write one project's automation code into another project's folder in that repo.

Use `Config/QA-Agent/professional-coverage-model.yaml` as the common BE/FE/UI-UX/flow/data/non-functional denominator and `Config/QA-Agent/api-coverage-profile.yaml` for API/event scope. Distinguish designed, reviewed, automated, executed, and proven coverage; never claim zero bugs or 100% without an explicit denominator and residual risk.

## Agent Role & Knowledge Governance

Read `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml` before selecting a role mode or claiming execution capability. Apply `governance/knowledge-policy.yaml`: only `APPROVED` knowledge for the active project may be used as a PASS/FAIL oracle. Competency levels and readiness cannot be self-promoted; promotion requires eval and reviewed evidence.

## Commit & Pull Request Guidelines

Use traceable commit messages:

```text
[SPRINT-ID] [Action]: [module] [description] - [US/BUG-ID]
S1 Add: access control regression robot suite - DEMO-123
```

Pull requests should include linked Jira issue, changed test assets, evidence/report paths, screenshots for UI-facing changes, and QMetry cycle/folder IDs touched.

## Security & Configuration Tips

Never commit `.env`, API tokens, generated logs, `results/`, or `__pycache__/`. Prefer live OpenAPI specs for new test generation when required by the workflow, and treat local specs as cached references unless confirmed current.
