---
name: 34-database-testing
description: Design or execute controlled database testing for integrity, transactions, migrations, reconciliation, performance, audit, security, and data lineage. Use when database behavior is part of the expected result.
---

# Database Testing

Use authoritative schemas and a read-only account by default. DML, DDL, lock, migration, destructive, or high-cost operations require explicit approval and rollback controls.
Read `Config/QA-Agent/professional-coverage-model.yaml` and link DB checks to the originating functional/API/data-flow coverage units.
If `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/<module>/_db-reference.md` exists for the module under test, read it before designing queries — it carries the upstream-source-to-app-schema field mapping, join keys, known gaps/assumptions, and existing reconciliation validator scripts (see `governance/knowledge-policy.yaml`'s `db_reference_artifact`). Treat it as `DRAFT` reference, not an oracle by itself: a mapping marked "verified" there may have been verified in a different project/session — re-confirm against this project's live schema/data before relying on it, and flag any mismatch as a new gap rather than silently trusting either source.

## Procedure

1. Confirm database, schema/version, environment, access scope, data classification, and expected business rule.
2. Cover constraints, types, nullability, uniqueness, referential integrity, CRUD side effects, transaction atomicity, rollback, concurrency, locking, audit fields, and reconciliation as applicable.
3. Assess migrations, backward compatibility, historical data, indexes, query plans, partitioning, retention, encryption, masking, and lineage where in scope.
4. Parameterize queries, bound time and rows, avoid unrestricted `SELECT *`, and redact sensitive values.
5. Reconcile DB state with API, event, UI, or downstream state instead of treating a row in isolation as proof.

## Output Contract

Return linked coverage units, rule and source, database/schema version, query intent, controlled query or script, expected/actual result, cross-layer reconciliation, evidence, privacy handling, status, blocked readbacks and residual risk.
