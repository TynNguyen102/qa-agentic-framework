---
name: 26-deep-coverage-testing
description: Discover hidden test conditions by combining decision, state, combinatorial, temporal, adversarial, concurrency, data-lineage, and failure-model techniques. Use when ordinary requirement-based cases are insufficient.
---

# Deep Coverage Testing

Use this workflow to expose blind spots, then route executable cases to the appropriate design or execution workflow.
Read `Config/QA-Agent/professional-coverage-model.yaml`; prioritize its `depth_triggers` and create/link coverage units for every distinct hidden risk retained.

Use coverage-layer labels `C0`-`C5` to avoid confusion with agent maturity `L0`-`L5`: `C0 requirement/rule`, `C1 happy`, `C2 role/state`, `C3 boundary/negative`, `C4 cross-service/entity`, `C5 adversarial/concurrency/failure`.

## Procedure

1. Identify high-risk rules, irreversible effects, complex state, multiple actors, asynchronous behavior, and integration boundaries.
2. Model decisions and exclusions, state transitions, pairwise or selected higher-order combinations, sequences, time, retries, races, duplicates, partial failure, and recovery.
3. Challenge permissions, tenant boundaries, data lineage, historical data, migration state, cache state, and inconsistent downstream responses.
4. Add adversarial but authorized inputs and operational scenarios.
   - Require rules of engagement for injection, chaos, fuzz, runaway-query or intrusive concurrency work. Save deterministic fuzz seeds and minimum reproduction.
5. Use the canonical coverage states. Design is not review/automation/execution/proof; `N/A_WITH_REASON` requires a source, reason and owner.
6. Remove equivalent cases, retain distinct risk coverage, and state why every proposed case matters. Do not assume all 5xx responses are defects or all eventual-consistency delays violate an SLA.

## Output Contract

Return coverage-unit ID, hidden condition, source and assumptions, technique, risk, proposed case, required data/environment, oracle layers, evidence needed, owner, priority, status, residual risk and target downstream workflow.
