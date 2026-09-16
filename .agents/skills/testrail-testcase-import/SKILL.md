---
name: testrail-testcase-import
description: Discover the exact TestRail case schema (project/suite/section structure, custom fields, type/priority IDs), map canonical testcases, validate and dry-run, and—with explicit approval—push cases via the TestRail API and read back results. Use when suite/section mapping, custom field format, or import to TestRail is requested.
---

# TestRail Testcase Import

Read `Config/QA-Agent/canonical-testcase-schema.yaml`, `Projects/<ACTIVE_PROJECT>/Config/testrail-profile.yaml`, and `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml` first.

## How The Case Schema Is Known

Never guess TestRail fields, type IDs, or priority IDs. Derive them from one of these authoritative sources, in priority order:

1. live TestRail API metadata for the target project (`get_case_fields`, `get_case_types`, `get_priorities`, `get_suites`/`get_sections` for the target project/suite);
2. a current exported case/field reference from the target TestRail instance;
3. a versioned project mapping explicitly confirmed by the user.

Record `project_id`, `suite_mode` (single suite / multiple suites / suites + baselines), section strategy, case template (Text vs Steps), custom field names/types, `type_id`/`priority_id` mappings, and the reference field used for requirement/Jira traceability (commonly `refs`). Update `testrail-profile.yaml` only after confirmation.

## Procedure

1. Validate the testcase title profile and every required canonical field.
2. Resolve suite/section placement — TestRail organizes cases under Suites → Sections, not folders/cycles like QMetry; create or confirm the target section path before mapping cases into it.
3. Map canonical fields to TestRail case fields without losing traceability:
   - `title` → case title
   - `steps` / `steps.expected_result` → `custom_steps_separated` (preferred, one row per step) or `custom_steps` + `custom_expected` (plain text), whichever template is confirmed for this project
   - `priority` → `priority_id` via the confirmed mapping — do not assume TestRail's default 1–4 scale matches this project's priority names
   - `scenario_type` / `technique` → the project's confirmed custom field, if one exists; otherwise keep in the local canonical record only
   - `linked_requirements` → the confirmed reference field (commonly `refs`, a comma-separated Jira/requirement key list)
   Keep unmapped internal fields (test_level, coverage_type, oracle_layers, etc.) in the local source artifact — TestRail cannot store everything the canonical schema tracks.
4. Check case template compatibility, required custom fields, `priority_id`/`type_id` validity, duplicate titles within the target section, and precondition/step/expected formatting.
   - Read `sprint.current`; return `NEED_CONFIG: CURRENT_SPRINT` when it is blank or `TBD`.
   - Keep execution-only fields (actual result, elapsed, defects, `status_id`) out of case-creation payloads — those belong to a Run/Result push (see `13-execute-approved-testcases`), not case authoring.
5. Produce a preview and dry run first (a labelled request-payload preview, or a non-mutating validation call if the connector supports one). If no API connector is configured, report `TOOL_NOT_CONFIGURED`; do not pretend the import command exists.
6. Require explicit approval immediately before any live `add_case` / `add_section` / `add_suite` call.
7. TestRail's API creates cases one at a time (`POST add_case/{section_id}`) — there is no native bulk case-creation endpoint (bulk endpoints exist for results: `add_results`/`add_results_for_cases`, not for cases). An import of N cases means N sequential `add_case` calls; read back each created case ID, section/suite placement, title, steps, custom fields, and traceability refs, and reconcile partial failures across that loop individually — do not assume one call covers a batch.

## Output Contract

Return `NEED_CONFIG`, discovered schema with evidence, validation report, dry-run/preview, or created TestRail case IDs with readback and rollback/recovery notes.

## Pre-DONE check

- Distinguish `CANDIDATE_MAPPING` (not yet verified against the live instance) from `VERIFIED_TESTRAIL_SCHEMA`.
- Preserve all canonical fields that TestRail cannot store in the local artifact.
- Never mark an execution PASS merely because a case or run entry was created.
- Require title selection, target suite/section, duplicate policy, field mapping, dry-run, approval and readback before live import.
