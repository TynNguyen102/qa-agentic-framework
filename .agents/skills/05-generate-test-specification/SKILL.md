---
name: 05-generate-test-specification
description: Turn approved high-level test design into structured executable test scenarios or manual test scripts before tool-specific testcase formatting. Use when QA needs scenario-level steps, Given/When/Then flows, execution order, or evidence requirements.
---

# Generate Test Specification

## Workflow

1. Read approved conditions, sources, roles, states, data, and risk.
2. Write scenarios at business-action level with explicit preconditions, actions, results, and readback oracles.
3. Keep one primary intent per scenario and isolate invalid dimensions for diagnostic clarity.
4. Include cleanup/rollback and evidence requirements.
5. Preserve traceability to coverage-unit ID, condition, AC/rule, and risk.
6. Mark unresolved expected results `NEED_CONFIRM`.

## Output

Produce scenario ID, linked coverage units, intent, source links, preconditions, role/state/data, steps or Given/When/Then, expected business result, oracle layers, cleanup, priority, residual risk, and automation candidate. This is not a test-management-import format (QMetry or TestRail) and does not replace skill 11 automation code generation.
