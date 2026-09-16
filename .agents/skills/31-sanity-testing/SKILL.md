---
name: 31-sanity-testing
description: Perform a focused sanity check after a build, patch, or narrow change by validating the changed behavior and its immediate critical dependencies. Use for rapid confidence before broader testing.
---

# Sanity Testing

Sanity is a narrow, risk-based check of changed functionality. It is not a substitute for smoke or regression.

## Procedure

1. Record build, change list, impacted components, dependencies, configuration, and known issues.
2. Select the primary changed journey, direct business rules, critical permission, integration, and data side effects.
3. Execute a small set of representative positive and high-risk negative checks.
4. Verify authoritative readback and collect evidence for every result.
5. Stop and recommend rejection or investigation when the core change cannot be exercised reliably.

## Output Contract

Return build/environment, change scope, selected checks and rationale, results, evidence, blockers, observed impact, and recommendation for deeper testing.
