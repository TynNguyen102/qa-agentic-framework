---
name: qmetry-testcase-import
description: Discover the exact QMetry testcase import schema, map canonical testcases, validate and dry-run files, and—with explicit approval—import and read back cases. Use when column count, format, folder mapping, or import is requested.
---

# QMetry Testcase Import

Read `Config/QA-Agent/canonical-testcase-schema.yaml`, `Projects/<ACTIVE_PROJECT>/Config/qmetry-profile.yaml`, and `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml` first.

## How Column Count Is Known

Never guess QMetry columns. Derive the exact ordered header and required fields from one of these authoritative sources, in priority order:

1. a current successful QMetry export or import template from the target project;
2. live QMetry project/import metadata exposed by an approved connector;
3. a versioned project mapping explicitly confirmed by the user.

Record source, project, issue type, export/import mode, delimiter, encoding, header order, required fields, field types, allowed values, and folder/cycle identifiers. Update `qmetry-profile.yaml` only after confirmation.

The current profile contains a user-provided 17-column TSV candidate. Use it for canonical-to-TSV preview and validation, but keep live import blocked while `validation.target_project_verification` is `NEED_CONFIG` or `live_import_allowed` is false. Do not confuse the separate 18-column SIT design/execution table with the testcase-import contract.

## Procedure

1. Validate the testcase title profile and every required canonical field.
2. Map canonical fields to the exact QMetry fields without losing traceability. Keep unmapped internal fields in the local source artifact when QMetry cannot store them.
3. Check column count and order, delimiter, quoting, multiline cells, encoding, required values, allowed enums, duplicate titles/external IDs, folder, cycle, labels, priority, and precondition/step/result formatting.
   - Enforce the configured 17-column order exactly for candidate TSV output.
   - Read `sprint.current`; return `NEED_CONFIG: CURRENT_SPRINT` when it is blank or `TBD`.
   - Keep actual result, execution result, bug ID, evidence and test time out of testcase-creation rows unless target-project metadata explicitly maps them.
4. Produce a preview and dry run first. If the repository lacks an importer, report `TOOL_NOT_CONFIGURED`; do not pretend the import command exists.
5. Require explicit approval immediately before a live import.
6. Read back created/updated testcase IDs, folder/cycle placement, title, steps, expected results, and traceability. Reconcile partial successes.

## Output Contract

Return `NEED_CONFIG`, discovered schema with evidence, validation report, dry-run preview, or imported QMetry IDs with readback and rollback/recovery notes.

## Pre-DONE check

- Distinguish `CANDIDATE_COLUMNS` (unverified) from `VERIFIED_IMPORT_SCHEMA` (confirmed against the active project's live QMetry instance).
- Preserve all canonical fields that QMetry cannot store in the local artifact.
- Never mark an execution PASS merely because a testcase or execution record was created.
- Require title selection, target folder, duplicate policy, allowed values, dry-run, approval and readback before live import.
