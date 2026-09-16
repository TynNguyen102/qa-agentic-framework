---
name: 15-functional-happy-path-testing
description: Validate the project's critical functional happy paths end to end with realistic roles, valid data, business outcomes, and cross-layer readback. Use for focused positive-path confidence, not as a substitute for full testing.
---

# Functional Happy-Path Testing

Identify the smallest set of representative journeys that prove the primary user value.

## Procedure

1. Derive journeys from approved requirements, business rules, roles, and acceptance criteria.
2. State prerequisites, valid representative data, source state, user action, expected state transition, and downstream outcome.
3. Execute through the real entry point and verify the result across every required layer.
4. Capture evidence for the user-visible outcome and the authoritative readback.
5. Report negative, permission, recovery, and boundary risks that remain uncovered. Never use a happy-path pass as evidence of full release quality.

## Output Contract

Return journey, role, data, build/environment, expected outcome, actual outcome, readback, evidence, status, and uncovered risk.
