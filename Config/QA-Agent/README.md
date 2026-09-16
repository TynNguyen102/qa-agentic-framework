# QA Agent Configuration (Core)

This folder holds the profiles genuinely shared across every project: canonical testcase schema,
professional/API coverage models, standards profile, assurance levels, defect register schema,
Git collaboration conventions, the workflow catalog, and `ui-pattern-checklists/` — a starter
reference library of concrete, pre-vetted testcase checklists per common UI pattern (table/list,
form, permission, concurrency, browser/device, per-field-type validation), each mapped to a
`coverage_type` value in the canonical schema. See `ui-pattern-checklists/INDEX.md` for how
`06-generate-functional-testcases` and related skills use it, and its `DRAFT` governance status.

Project-specific decisions — confirmed testcase title format, defect title/severity/priority
mapping, test management tool layout (QMetry columns or TestRail suite/section/field mapping —
whichever the project's `qa-config.yaml` names), Jira subtask titles, automation structure, agent
competency/readiness — live in each project's own `Projects/<name>/Config/`, not here. Once a
project has real confirmed decisions to record, add a `Projects/<name>/Config/README.md`
documenting them.
