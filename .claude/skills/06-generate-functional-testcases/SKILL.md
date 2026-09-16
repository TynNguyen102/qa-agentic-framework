---
name: 06-generate-functional-testcases
description: Generate functional testcases from approved requirements and high-level design using the canonical testcase schema, including happy, alternate, negative, boundary, state, permission, integration, and readback coverage. Use when detailed functional cases are requested.
---

# Generate Functional Testcases

> **Tóm tắt (VI):** Sinh testcase chức năng từ yêu cầu đã chốt — happy/negative/boundary, truy vết tới AC/rule, đúng title format. Dùng sau khi review requirement.

## Mandatory configuration

Read `Config/QA-Agent/canonical-testcase-schema.yaml`, `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml`, and `Config/QA-Agent/professional-coverage-model.yaml`.

- **UI pattern checklists**: read `Config/QA-Agent/ui-pattern-checklists/INDEX.md` and, from it, load only the checklist file(s) matching UI components actually present in this feature (a data table, a create/edit form, delete, filters, permission-gated elements, concurrent-write data, etc.) — do not load unrelated ones. Treat each loaded checklist as reference to avoid missing a known pattern, not a template to copy verbatim: translate item names/labels to this feature's real field/column/button names (from the mockup/design when available), drop items that don't apply with a reason, and still pass every generated case through the Self-review section below. These files are `status: DRAFT` (adapted cross-project tester knowledge, not yet project-reviewed) — resolve the concrete expected value against this project's own confirmed source, never cite a checklist item alone as the oracle.
- **Field Propagation Map (mandatory for any Create/Edit feature)**: before writing the post-save expected results, build the field-by-field map described in `ui-pattern-checklists/patterns/create-edit-form.checklist.md` — for every field on the create/edit form, trace whether and where it reappears (Listing column, Detail field, other screens), using that OTHER screen's own mockup/BRD/spec for the real column/label name (never assume it matches the form's field name — it often doesn't). A field with no confirmed downstream appearance and no confirmed "internal-only" source is `NEED_CONFIRM`, not silently dropped. A Listing/Detail field that is computed/derived rather than a pass-through of a create-form field gets its own case for the computation, not folded into the "created record displays correctly" case. Post-save expected results must enumerate the mapped fields concretely (exact column/label = exact value, including any display transform) — a generic "record appears correctly in the list" is not sufficient for `13-execute-approved-testcases` to validate against.
- **Module domain overview**: if `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/<module>/_overview.md` exists for this feature's module, read it before drafting — its cross-screen effect table and self-check questions catch impact on other menus/screens that this single US's rules never state. It is `DRAFT` reference (see `governance/knowledge-policy.yaml`'s `module_overview_artifact`), not a substitute for tracing the actual confirmed rule for this feature.
- **Module baseline coverage**: if `Projects/<ACTIVE_PROJECT>/Modules/<module>/TC/_baseline-coverage.md` exists for this feature's module, read it before drafting — it maps which pages/features in the module already have testcases (file, case count, NEED_CONFIRM/BLOCKED items, gaps with zero coverage). Without it, this skill only sees the current US's own requirement source and has no way to know what the module already covers, so it risks silently duplicating cases or missing that a related page has no baseline at all. Treat its NEED_CONFIRM/BLOCKED entries as snapshots, not current fact — verify against live Jira/DEV before relying on them, and update the file's page-map/gap list afterward when this run adds a new testcase file or resolves a listed gap.
- **Module DB reference**: if `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/<module>/_db-reference.md` exists for this feature's module, read it before drafting any case that needs field-mapping, join-key, or record-count verification beyond what the API/UI already exposes (see `governance/knowledge-policy.yaml`'s `db_reference_artifact`) — it is the source-of-truth-vs-app-DB mapping this skill otherwise has no way to know. A case that needs DB-level verification should route the query design to skill `34-database-testing`, but the mapping/join-key knowledge itself is read here at design time so the coverage matrix can mark the right unit `REQUIRED` instead of `NEED_CONFIRM` for lack of a known mapping.
- **Mockup/design reconciliation**: when a mockup, screenshot, or Figma design is available alongside the requirement source, reconcile it against the BRD/AC before drafting: the requirement source wins on business rules; for field/column/button names and UI structure, prefer the **freshest observable source** — an actual live/staged UI screenshot first if one exists, then the current mockup/design, then requirement-doc prose last (a mockup can be stale — see the DEMO-4609 lesson in Self-review below, where an old mockup's "Score"/"Entity" had already been superseded by the real AC/UI's "Anomaly Score"/"Entity Type"). Flag with `NEED_CONFIRM` any element present in one source but not another, or any naming mismatch between them — still generate a case for it, just mark the gap; never silently pick one source without recording the conflict. Use generic placeholders like "field X" or "column A" only while a name is still `NEED_CONFIRM` — never in a final case.
- **Edge/BVA reference (optional)**: for boundary, date/time/DST, calculation (div-zero/NaN/overflow), string/i18n/RTL, file-upload, network, and concurrency edge conditions, scan `Projects/<ACTIVE_PROJECT>/Knowledge-Base/QA-Checklists/edge-cases.draft.md` — a grouped checklist so a known edge group isn't silently missed. It is `status: DRAFT` borrowed cross-project (cross-project) knowledge (see `governance/knowledge-policy.yaml`), a design aid only — never the PASS/FAIL oracle; resolve each concrete expected value against this project's confirmed source and translate item names to this feature's real field/column names.

- If the title profile is not configured, draft testcase bodies but set title to `NEED_CONFIG: TESTCASE_TITLE_FORMAT`; do not call the output final.
- Check `Projects/<ACTIVE_PROJECT>/qa-config.yaml`'s `integration.test_management.tool` when test-management-ready output is requested, and read that tool's profile (`qmetry-profile.yaml` or `testrail-profile.yaml`) only then. Block import-ready output while that profile is not configured. For QMetry, the candidate adapter is exactly the profile's confirmed column count and order — never drop or reorder a column; a missing column shifts every field after it and breaks upload. For TestRail, map fields per the profile's `mapping_from_canonical` and case template (Text vs Steps) instead of a fixed column count.
- **Mandatory diagram check**: when reading a Jira issue or Confluence page as a requirement source, check for attached/embedded images (flowcharts, sequence diagrams, wireframes) and read them before analyzing — they often carry constraints the text doesn't state.
- If `04-high-level-test-design` has run for this scope, only treat its output as authoritative once anh has recorded it as reviewed/approved (not just present earlier in the conversation) — otherwise generate testcases directly from AC/BR/US and note the missing high-level-design approval as a gap, don't block on it.

## Workflow

1. Build a Rule Inventory from real US/AC/BR IDs, plus these additional categories when triggered:
   - `CHANGE-xx` — a PO/BA/DEV comment indicates the requirement changed (e.g. "updated FRS", "clarified", "scope moved", "superseded"). Verify whether the old expected result is still valid before reusing it.
   - `DECISION-xx` — a business decision, default behavior, precedence rule, or state-machine choice.
   - `XENTITY-xx` — cross-entity/cross-tenant behavior, consent/purpose mapping, or a runtime join across entities.
   - `BYPASS-xx` — the UI hides or doesn't surface an option/value that the API can still be called with directly.
   Mark derived observations `DRAFT` or `NEED_CONFIRM`; do not invent approved rules.
2. Trace each case to confirmed rules, risks and stable coverage-unit IDs. Give every applicable rule/coverage unit a case or `N/A_WITH_REASON`/`NEED_CONFIRM`/`BLOCKED` entry in the coverage matrix. Every applicable item in a loaded UI pattern checklist (see Mandatory configuration) gets the same treatment — a case or an explicit `N/A_WITH_REASON` — before the set is considered final.
3. Cover the applicable groups below — do not silently skip one that applies:

   | Group | Risk-based selection rule |
   |---|---|
   | AC-based | Prove each material AC and add a disconfirming/negative condition when the AC can be violated; otherwise record why not applicable |
   | BR-based | Prove each authoritative material rule and its highest-risk violation |
   | Basic/happy flow | Cover each critical business outcome, not merely each screen or endpoint |
   | Equivalence partitioning | Select representative valid/invalid classes for constrained or behaviorally distinct inputs |
   | Boundary value analysis | Use on explicit/derived limits; include just-inside/on/outside values where safe and meaningful |
   | Decision table / combinatorial | Model multi-condition rules; cover rule outcomes and use pairwise/risk-based higher-order combinations rather than exhaustive claims |
   | State transition | Cover reachable critical states, valid/invalid transitions and recovery; add auth/session lifecycle only when in scope |
   | Corner cases / error guessing | idempotency, race conditions, timeout, malformed input |
   | Impact (cross-feature) | sync/retry/rollback and effect on other modules, per any `XENTITY-xx`/cascading state |
   | Regression | existing flows unaffected by the change, per any `CHANGE-xx` |
   | Non-functional | Select applicable security, performance, reliability, accessibility, usability and compatibility risks; route specialist execution separately |
   | Checklist-based | only if anh supplied a checklist; otherwise `N/A` |
   | Exploratory | Create risk-based charters when uncertainty, novelty or defect history warrants; do not add arbitrary testcase rows |
   | Source-of-truth verify | When a static/seeded data source (spreadsheet export, DB seed, upstream system) exists in parallel with the UI/API under test, add a small set of cases that read the source directly and diff it against what the UI/API shows — count parity, per-record field parity, and status/category counts. Don't rely on UI-only checks when an independent source of truth is available; a real case (DEMO-4609, reviewed 2026-08-27) found a real data-import gap (7 missing records) exactly this way. |

4. Classify every case with exactly one `scenario_type` from this closed set — do not invent a new value: `Happy`, `Neg`, `Corner`, `Impact`, `E2E`, `Security`, `Perf`, `Reliability`, `Regression`, `Exploratory`. Distinguish `Corner` (edge condition inside the feature under test) from `Impact` (this feature's change affects another feature/service) — they are not interchangeable.
5. Record `technique` from this closed set when applicable, else `—`: `EP`, `BVA`, `DT` (decision table), `ST` (state transition), `EG` (error guessing), `Idem` (idempotency), `Race`, `DataDriven`, `Security`, `Perf`, `Reliability`.
6. Internal coverage check — do not export this as separate files, resolve gaps into the final set before returning:
   - Draft coverage map: Rule ID -> covered case IDs -> status.
   - Gap analysis: Rule ID -> missing group -> proposed case -> priority -> open question.
   - Fill every real gap with an additional case before finalizing; do not leave a gap noted without either a case or an explicit `N/A + reason`.
7. Keep test basis, scenario type, test level, technique, coverage type, smoke/regression flags, and automation candidacy as separate fields. Set `automation_candidate` (Yes/No/Partial) and, whenever it is Yes or Partial, `automation_layers` (every layer in {UI, API, DB} this case can actually assert — not only the easiest one) per `canonical-testcase-schema.yaml`; this is a real decision made now, not a placeholder for `11-generate-automation-script` to re-derive later.
8. Keep expected results business-focused and cite their source. Include roles, fixtures/data profiles, cleanup, evidence oracle, and readback. Prefer realistic test data from `Projects/<ACTIVE_PROJECT>/qa-config.local.yaml`/`Config/<PROJECT>_ENV.*.yaml` (real-shaped accounts/URLs) over placeholders like `[valid email]`. For a UI-driven Create/Edit/Delete step whose `readback_oracle` includes API, never write a bare "kiểm tra API" — state explicitly whether the expected result covers the outgoing **request** (endpoint/method/payload the UI actually sent — a DevTools Network-tab-style check; catches a UI that displays the right value but transmits the wrong one, common with dropdown IDs and multi-select arrays), the **response** (status + body field values), or both; default to both when feasible, since each catches a different bug class and neither substitutes for the other.
9. Deduplicate overlapping cases and preserve stable external IDs. Do not force testcase/exploratory counts, automation percentages, or `High -> Smoke` mappings — an honest gap or residual risk is better than fake coverage.
10. Order the final set: per AC/rule in business sequence (Happy -> Neg -> Corner), then Impact/E2E, specialist candidates, Regression, and any exploratory charters last.

## Self-review before returning (do not skip)

Scan every case and fix violations before returning — do not return a set with a known violation:

- Expected result has no vague phrase ("works correctly", "displays normally") — states the concrete business/API/UI result.
- Every `trace`/Rule ID reference resolves to a real ID in the Rule Inventory, not an invented one.
- `scenario_type` and `technique` both come from the closed sets above.
- Precondition is never blank — write `None` if genuinely none.
- Every `CHANGE-xx` has a case verifying the new contract, or an explicit `N/A + reason`.
- Every `DECISION-xx` case asserts the actual business outcome (decision/effect/state), not just status code.
- Every `XENTITY-xx` has a case with both entities seeded, asserting isolation/data integrity.
- Every `BYPASS-xx` has a direct-API negative case for the value/action the UI hides.
- Every testcase links to a real coverage unit; every applicable uncovered unit has an explicit status, owner and residual risk.
- Every field/column/label name quoted in an expected result matches the freshest observable source per the Mockup/design reconciliation rule above (live/staged UI > current mockup > requirement-doc prose) — never a stale mockup's shorthand or the tester's memory of an older version. A real case (DEMO-4609, reviewed 2026-08-27): a testcase suite consistently used "Score"/"Entity" from an old mockup while the PRD's AC and the actual staging UI both used "Anomaly Score"/"Entity Type" — the mismatch propagated through the entire suite unnoticed. Any naming conflict between sources is `NEED_CONFIRM`, not silently resolved either way.
- Every applicable item from a loaded UI pattern checklist (`Config/QA-Agent/ui-pattern-checklists/`) resulted in a case or an explicit `N/A_WITH_REASON` — not silently dropped.
- **Ground against the live feature when it exists (do not skip).** If the feature — or any slice of it — is already deployed to DEV/staging, probe the real UI/API and reconcile every testcase against the *actual* implementation, not the requirement doc alone. A requirement-accurate suite is worthless if the build silently diverges. Record what is CONFIRMED-on-DEV vs design-ahead, name the real endpoint/control observed, and raise any spec↔build deviation as a review finding (`NEED_CONFIRM` with BA/Dev) — never leave the whole suite "design-ahead" when the feature is testable now. Real case (DEMO-7065, 2026-09-10): the suite matched the BRD's rich feedback form, but DEV shipped a minimal like/dislike that records immediately with no category/description form — caught only after grounding, and only after the Lead had to ask twice.
- **Exhaust the dimensions — do not stop at happy/negative.** For each feature explicitly walk: a11y/keyboard · error & empty state (control absent) · persistence (refresh / reopen / session-switch) · permission (another role/tenant) · duplicate / rapid-repeat · network-failure / partial · cross-layer readback. Each yields a case or an explicit `N/A_WITH_REASON`. Silently missing a dimension is the failure, not the extra rows.
- For any Create/Edit feature: the Field Propagation Map exists, every create/edit field has a row in it (including `NEED_CONFIRM` rows, never a silent gap), and every post-save/post-edit expected result enumerates the mapped fields by their real downstream column/label name and value — not a generic "displays correctly" statement.
- Every Create/Edit/Delete step with API in its `readback_oracle` names request, response, or both explicitly — never an undifferentiated "kiểm tra API".
- Exploratory charters, when risk-selected, are traceable and placed last; no fixed row count is enforced.

Report a one-line self-review result (e.g. "Self-review: fixed 3 vague expected results, added 1 missing Impact case" or "Self-review: OK, no violations").

## Output

Emit canonical testcases first. When anh requests test-management-ready output, resolve the active project's tool from `qa-config.yaml`:
- **QMetry**: produce a clearly labelled candidate adapter using the exact column count/order confirmed in `qmetry-profile.yaml` (e.g. STT, Summary, Test Level, Precondition, Test Data, Step summary, Expected result, Priority, Sprint, Story Linkages, Test Type, Smoke, Auto, Dependency, Component, Trace, Technique) — never drop a column, never reorder.
- **TestRail**: produce a candidate case payload per `testrail-profile.yaml`'s `mapping_from_canonical` and confirmed case template (Text vs Steps), with `refs` carrying traceability.
Do not call either live-import ready until target-project verification passes. Never guess mandatory fields, allowed values, title selection, or folder/section.

## Pre-DONE check

- Confirm Rule Inventory and coverage denominator completeness (including any CHANGE/DECISION/XENTITY/BYPASS entries), concrete expected results, valid trace/coverage IDs, stable IDs, executable preconditions, cleanup, oracle layers and evidence/readback.
- Read `sprint.current`; block the final test-management-ready output when it is blank or `TBD`.
- Return `DONE_WITH_CONCERNS` for unresolved non-blocking gaps, `NEEDS_CONTEXT` for insufficient sources, and `BLOCKED` when authoritative expected behavior is unavailable.
