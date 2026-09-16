---
name: 41-generated-file-testing
description: Test files the product generates or exports — CSV, Excel, PDF, JSON, templates and error files — across encoding, delimiter and locale, content contract against the source of truth, scale and special characters, formula injection and authorization, and the download/job lifecycle. Use whenever a feature hands the user a file.
---

# Generated File and Export Testing

A file is an interface with a consumer the product does not control. It passes only when it opens correctly in the tool the user actually uses, with values that reconcile against the source of truth.

Read the `data_and_integration`, `security_and_privacy` and `ux_and_usability` dimensions in `Config/QA-Agent/professional-coverage-model.yaml`, and `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml`.

**A byte-level check is a necessary condition, never a sufficient one.** Confirming an encoding marker is present does not prove the file opens correctly; passing the byte check and closing the defect is how an encoding bug survives a retest. Open the file in the real target tool at the real target locale before calling it PASS.

## Procedure

1. Inventory every generation point for the feature, not just the obvious button: main export, downloadable template, error/rejection file, report, and any file produced by a background job. Record for each whether it is generated server-side or client-side (for example a browser `Blob`) — they fail differently and are usually fixed in different places.
2. Encoding and structure at byte level: byte-order mark, character encoding, line endings, quoting, and the field delimiter against the target locale's expectation. Record the actual leading bytes rather than trusting the generator's intent.
3. Open each file in the real target application at the target locale and version — the spreadsheet program most users have, not only a parser or a text editor. Test the default path the user takes (double-click), not just the import wizard. Record application name, version and locale; a pass on one locale is not a pass on another.
4. Content contract against the source of truth: column set, header naming and order versus the screen, data types, empty and null representation, number precision and thousands/decimal separators, dates and time zones, enum labels versus stored codes, and truncation of long values. Reconcile the values themselves through `38-query-data-by-assurance-level` — matching column headers proves nothing about the data underneath.
5. Scale and hostile content: empty result set, single row, the documented maximum, oversized fields, and values embedding the delimiter, quote characters, newlines, right-to-left marks and the active language's diacritics.
6. Security. Check formula injection — a cell whose value begins with `=`, `+`, `-`, `@`, tab or carriage return can execute when the file is opened, so the generator must neutralize it. Check that the export honours exactly the same authorization, scope and tenant filter as the screen it came from; an export route that returns more than the UI is a privilege defect. Check filename construction for path traversal and injected separators, and check that no column leaks data the caller may not see.
7. Download and job lifecycle: pending or queued jobs, timeout, expiry of a generated link, re-download, concurrent exports, partial or interrupted export, and whether a failed generation reports an error or silently yields an empty file.
8. Recurrence check — mandatory. Search the defect history for the same failure class in other modules before closing out. When the same class already exists elsewhere, report it as systemic (a missing shared generation utility) rather than as an isolated module bug, and say so in the finding.
9. Classify with `bug-basis-profile.yaml`, keeping the generator defect separate from a consuming application's own configuration.

## Hard rules

- Never close a file defect on a byte-level or parser check alone when the reported symptom was observed in an end-user application.
- Never state PASS without recording the consuming application, its version and its locale.
- Never attach a generated file containing real personal data, credentials or production records to a defect or report; use a redacted or synthetic equivalent that still reproduces the failure.
- Treat "the data is currently all ASCII so the problem does not show" as a latent defect, not a pass.

## Output Contract

Return coverage-unit ID, the generation-point inventory with server-side/client-side for each, byte-level findings (encoding, marker, delimiter, line endings), the consuming application/version/locale used and what it showed, the content reconciliation and the readback layer used, scale and special-character results, security results covering formula injection and export authorization, lifecycle results, the recurrence check with the keys searched, classification, and residual risk.
