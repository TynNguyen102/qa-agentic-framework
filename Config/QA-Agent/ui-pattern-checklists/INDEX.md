# UI Pattern Checklists — Index

## Purpose

`coverage_type` in `Config/QA-Agent/canonical-testcase-schema.yaml` names *categories* of coverage
(e.g. `loading_empty_error_success_partial_and_stale_states`) but does not say what a concrete
testcase for that category looks like. Every time `06-generate-functional-testcases` (or `07`, `21`,
`28`) generated a case for one of these categories, the model re-derived the concrete steps from
scratch — which produces inconsistent depth run to run and lets non-obvious tester knowledge (the
"0" vs "—" vs empty distinction, optimistic-lock messaging, sensitive data must not exist in the DOM
at all, etc.) get silently dropped.

This folder is a **starter reference library** of concrete, pre-vetted checklist items per common UI
pattern, each explicitly mapped to the `coverage_type` value(s) it evidences. It captures reusable
tester knowledge — things true across almost any web feature, independent of any single BRD.

## Status — read before treating this as authoritative

`status: DRAFT` on every file in this folder. These were adapted from a manual tester's accumulated
checklist on a different project (see `Projects/*/CURRENT_STATE.md` if you need the provenance), not
yet reviewed against any specific project's actual UI conventions, design system, or component
library. Per `governance/knowledge-policy.yaml`, `DRAFT` knowledge is a **reference to adapt**, not a
PASS/FAIL oracle — do not cite a checklist item alone as the expected result; always resolve the
concrete expected value against the project's own confirmed source (BRD/AC/mockup/design system).
Promote a file's `status` to `REVIEWED`/`APPROVED` only after a QA lead has confirmed it fits this
workspace's projects, the same way `Projects/<name>/Knowledge-Base/Domain-Rules/*` gets reviewed.

## How `06-generate-functional-testcases` (and other design/execution skills) use this

1. From the reconciled feature description (BRD + mockup/design when available), identify which UI
   components are actually present: a data table, a create/edit form, delete action, filters,
   permission-gated elements, concurrent-write data, etc.
2. Load **only** the checklist file(s) matching components actually present — do not load unrelated
   ones (keeps the read focused and avoids inventing coverage for something that doesn't exist in
   this feature).
3. Use each loaded checklist as a *reference to not miss a pattern*, not a template to copy verbatim:
   translate item names/labels/values to this feature's real field/column/button names, drop items
   that don't apply (record why), and still run the case through the same self-review the skill
   already requires (concrete expected result, real coverage-unit trace, etc.).
4. Every checklist item that applies must end up as a testcase or an explicit `N/A_WITH_REASON` —
   same rule the skill already applies to the coverage matrix.
5. Map each generated case's `coverage_type` field to the value(s) listed in the checklist's own
   `coverage_type:` line — do not invent a new category name (same rule as the schema itself).

## Map: UI component present → checklist file(s)

| Component in the feature | Checklist file | Primary `coverage_type` |
|---|---|---|
| Data table / list screen | `patterns/table-list.checklist.md` | `loading_empty_error_success_partial_and_stale_states`, `business_side_effects_and_readback` |
| Filter, search box, sort | `patterns/filter-search-sort.checklist.md` | `happy_and_alternate_paths`, `equivalence_and_boundary_classes`, `state_preservation_refresh_back_forward_and_multi_tab` |
| Pagination | `patterns/pagination.checklist.md` | `equivalence_and_boundary_classes`, `state_preservation_refresh_back_forward_and_multi_tab` |
| Row checkbox / bulk action bar | `patterns/row-selection-and-bulk-actions.checklist.md` | `duplicate_idempotency_retry_and_concurrency`, `state_sequence_time_and_expiry` |
| Export (CSV/Excel/PDF) | `patterns/export.checklist.md` | `business_side_effects_and_readback` — also route to `41-generated-file-testing`, this checklist is not a substitute |
| Create form / modal | `patterns/create-edit-form.checklist.md` | `form_validation_timing_messages_and_recovery`, `decision_tables_and_cross_field_rules`, `persistence_events_cache_and_downstream_consistency` |
| Edit / inline edit | `patterns/create-edit-form.checklist.md` (Edit section) | same as Create, plus `partial_failure_rollback_and_cleanup` |
| Delete (single/bulk) | `patterns/delete.checklist.md` | `partial_failure_rollback_and_cleanup`, `business_side_effects_and_readback` |
| Detail / view screen | `patterns/detail-view.checklist.md` | `loading_empty_error_success_partial_and_stale_states`, `route_guards_navigation_and_deep_links` |
| Stat card / metric widget, Activity/Audit log tab | `patterns/stat-card-and-activity-log.checklist.md` | `business_side_effects_and_readback`, `observability_logs_metrics_traces_alerts_and_correlation` |
| Any input field (text, dropdown, multi-select, date, rich text, attachment) | `patterns/field-validation.checklist.md` | `form_validation_timing_messages_and_recovery`, `equivalence_and_boundary_classes` |
| Role-based access anywhere in the feature | `cross-cutting/permission.checklist.md` | `actors_roles_permissions_and_tenants`, `authentication_authorization_and_abuse`, `role_tenant_and_cross_entity_isolation` |
| Create/Edit/Delete on shared data | `cross-cutting/concurrency.checklist.md` | `duplicate_idempotency_retry_and_concurrency`, `state_sequence_time_and_expiry` |
| Any screen (always applicable) | `cross-cutting/browser-device.checklist.md` | `state_preservation_refresh_back_forward_and_multi_tab`, `responsive_browser_device_locale_theme_and_zoom`, `accessibility_semantics_keyboard_focus_reflow_and_assistive_technology` |

## Files in this folder

```
Config/QA-Agent/ui-pattern-checklists/
├── INDEX.md                              (this file)
├── patterns/
│   ├── table-list.checklist.md
│   ├── filter-search-sort.checklist.md
│   ├── pagination.checklist.md
│   ├── row-selection-and-bulk-actions.checklist.md
│   ├── export.checklist.md
│   ├── create-edit-form.checklist.md
│   ├── delete.checklist.md
│   ├── detail-view.checklist.md
│   ├── stat-card-and-activity-log.checklist.md
│   └── field-validation.checklist.md
└── cross-cutting/
    ├── permission.checklist.md
    ├── concurrency.checklist.md
    └── browser-device.checklist.md
```

## Extending this library

Adding a pattern not covered here (e.g. a kanban board, a timeline/gantt view, a chat/streaming
panel) follows the same shape: `coverage_type` mapping line, `status: DRAFT`, sections `Giao diện /
Chức năng / Phi chức năng`, stable ID prefix `CHK-<code>`. Add the new file's row to the map table
above in the same commit — an unlisted checklist file will not get loaded by the skill.
