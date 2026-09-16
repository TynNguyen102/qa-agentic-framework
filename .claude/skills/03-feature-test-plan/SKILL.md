---
name: 03-feature-test-plan
description: Produce a detailed feature or User Story test plan from approved requirements and risk. Use after requirement review when one feature, Epic, module, or release slice needs a concrete QA approach and execution scope.
---

# Feature Test Plan

Read `Config/QA-Agent/professional-coverage-model.yaml`; use it as the coverage denominator contract, not as a reason to force irrelevant test types.

## Workflow

1. Confirm source requirements, version/build target, actors, states, integrations, data, and business invariants.
2. Define objectives, in/out scope, test levels, types, techniques, environments, roles, fixtures, and dependencies.
3. Map risks to planned coverage and evidence oracles.
4. Select functional, API, UI, DB, contract, security, accessibility, reliability, usability, performance, and mobile coverage only when applicable.
5. Define execution sequence, retest/regression impact, automation candidates, and quality gates.
6. Mark unknown thresholds or expected behavior `NEED_CONFIRM`.
7. Create coverage units for applicable dimensions with source/risk, owner, priority, target state and evidence oracle. Record every exclusion as `N/A_WITH_REASON` or `OUT_OF_SCOPE_WITH_OWNER`.

## Output

Create a traceable plan containing scope, sources, risks, approach, coverage-unit denominator and state targets, environments, data, roles, deliverables, execution order, evidence, defect/retest process, entry/exit criteria, blockers, exclusions and residual-risk ownership.

Keep Test Completion separate from any Go-Live recommendation. Record who owns each decision and how it is verified; do not assume legacy QA Lead/PM approval, fixed SLA, arbitrary risk counts or numeric KPI targets.
