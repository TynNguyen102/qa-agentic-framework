---
name: 38-query-data-by-assurance-level
description: Select and perform the least-invasive data query or readback needed for the project's configured assurance level while protecting production, privacy, and database stability. Use when test conclusions require data verification.
---

# Query Data by Assurance Level

Read `Config/QA-Agent/assurance-levels.yaml` and the authoritative schema before querying. Choose the lowest level that can prove the expected business result.

## Levels

- `L0`: document and contract analysis only; no connected query.
- `L1`: connected read from approved UI/API/log sources.
- `L2`: allowlisted read-only DB query and cross-layer reconciliation.
- `L3`: controlled non-production test-data mutation with explicit approval and cleanup.
- `L4`: dedicated high-impact data, performance, resilience, or recovery activity with formal approval.

## Procedure

1. State the business question, required proof, environment, data classification, source, and selected level.
2. Use parameterized queries, least privilege, row/time limits, narrow columns, and indexed predicates. Avoid unrestricted `SELECT *` and expensive scans.
3. Redact or aggregate personal and sensitive data. Never expose secrets in output.
4. At L2 or above, reconcile results with the triggering API, event, UI, audit, or downstream state.
5. Require explicit approval for mutation, DDL, production access, full scans, locks, or load. Include cleanup and rollback for controlled changes.

## Output Contract

Return question, assurance level and rationale, assumptions, query scope, controlled query, summarized result, reconciliation, privacy handling, evidence, and remaining uncertainty.
