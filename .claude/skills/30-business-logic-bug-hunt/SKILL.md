---
name: 30-business-logic-bug-hunt
description: Hunt for business-logic defects by challenging authoritative invariants across state, permission, data, integration, timing, retries, concurrency, and tenant boundaries. Use for targeted risk-based bug discovery.
---

# Business-Logic Bug Hunt

A suspicious behavior is not a confirmed defect until the expected rule, reproducible deviation, and evidence are established.

Read `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml` before designing a hunt or classifying a finding.
Read the depth triggers and business/data/integration dimensions in `Config/QA-Agent/professional-coverage-model.yaml`; use uncovered/high-risk coverage units as hunt hypotheses.
For boundary/date/calculation/concurrency/race edge hypotheses, mine `Projects/<ACTIVE_PROJECT>/Knowledge-Base/QA-Checklists/edge-cases.draft.md` for hunt ideas — it is `status: DRAFT` borrowed cross-project (cross-project) reference (see `governance/knowledge-policy.yaml`), a hypothesis source only, never a PASS/FAIL oracle; a suspicious behavior still needs an authoritative expected rule before it is a confirmed defect.

## Procedure

1. Identify invariants from the profile's oracle priority. Record source version and timestamp.
2. Target high-risk combinations of state, role, tenant, historical data, boundary, sequence, and integration response.
3. Challenge duplicates, retries, out-of-order events, concurrent edits, stale data, partial failure, session changes, cache, and recovery.
4. Verify both visible behavior and authoritative readback. Repeat from a clean state and narrow the minimum reproduction.
5. Apply every confirmation gate and use one configured classification. When product sources conflict, use `NEED_CONFIRM` and show the conflict rather than choosing silently.
6. Create or update a sanitized cross-sprint record at `Projects/<ACTIVE_PROJECT>/Defects/<local_id>/manifest.yaml` for a persistent finding, using `Templates/defect-record.yaml`. Record `found_in_sprint`, fingerprint, traceability, evidence references and regression impact; do not embed raw secrets/logs.
7. Route confirmed defects to workflow 36; feed newly discovered conditions back into the coverage denominator/regression mapping and preserve questions separately.

## Output Contract

Return coverage-unit/invariant and source, hypothesis, state/data/role, minimal steps, expected, actual, readback, evidence, reproducibility, classification, impact, regression/coverage update and proposed next workflow.
