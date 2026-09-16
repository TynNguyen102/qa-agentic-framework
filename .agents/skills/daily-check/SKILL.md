---
name: daily-check
description: Run the start-of-day check — Jira/Confluence/GitLab status for the current sprint — and diff it against the most recent prior snapshot to surface what's new or changed, instead of re-listing everything as if seeing it fresh. Use at the start of a work day/session, or whenever anh asks "what's new since last time".
---

# Daily Check

> **Tóm tắt (VI):** Kiểm đầu ngày (Jira/Confluence/GitLab sprint hiện tại) + diff với hôm trước + bảng coverage theo US. Dùng đầu phiên hoặc khi anh hỏi "có gì mới".

Implements the "Daily Workflow" already documented in `CLAUDE.md` (check sprint config -> check Jira -> check Confluence/API changes -> update local state/report), plus the diff-against-yesterday step that wasn't automated before 2026-07-19, plus the GitLab check added 2026-08-27.

## Procedure

1. Read `Projects/<ACTIVE_PROJECT>/qa-config.yaml` for `sprint.current`, Jira `default_filter`/project key, Confluence space, and `repositories` (GitLab).
2. Find the most recent prior snapshot in `Outputs/daily/` (filename `YYYY-MM-DD.md`, sorted by date, excluding today's if one already exists). If none exists, this is the first run — say so explicitly, skip the diff, and just produce today's baseline.
3. Check live sources:
   - Jira (Atlassian MCP): US/defects in the current sprint/filter — key, status, summary, assignee, last-updated. Do NOT judge QC coverage from the Story/parent row alone: for each US/Task that matters, enumerate its attached **sub-tasks/child tasks** (`parent in (...)` or `getJiraIssue` subtasks) — create-testcase, execute-test, dev sub-tasks — and skim its **recent comments**. QC progress and blockers live on the sub-tasks and comments, not the parent (a Story can read `To Do`/`To Dev` while its testcase sub-task is already Closed, or vice-versa). Reporting "no testcase" or "not started" from the parent status is a known miss (corrected 2026-09-10).
   - Confluence (Atlassian MCP): pages linked from `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Confluence-Mirror/` or the configured space — flag if a page's version/last-modified changed since the prior snapshot.
   - GitLab (REST API, no MCP registered — see "GitLab access" below): for each repo in `qa-config.yaml` -> `repositories` with `access: CONFIRMED`, recent merge requests and commits on the default branch, scoped to the prior snapshot's date (or last 2 days on first run).
   - If a source is unreachable (e.g. cross-product search blocked, per `Projects/<ACTIVE_PROJECT>/Config/tooling-plan.yaml`; or GitLab token missing/expired), say so and fall back to direct-key/direct-page/direct-project reads instead of silently reporting nothing changed.
4. Build today's snapshot (see format below).
5. If a prior snapshot exists, diff Jira against it and produce three lists: **New** (not in prior snapshot), **Changed** (status/assignee/version different), **Resolved/Removed** (was open, no longer appears or is now Done/Closed). Do not infer a status change from absence alone — confirm via the live source before calling something resolved. GitLab activity is inherently append-only (commits/MRs since last check) — list it directly, no New/Changed/Resolved framing needed.
6. Save today's snapshot to `Outputs/daily/<YYYY-MM-DD>.md`. Never overwrite a different day's file.
7. Update `Projects/<ACTIVE_PROJECT>/session-state.local.yaml` (`last_execution`) and append a `Projects/<ACTIVE_PROJECT>/governance/audit-events/` entry per `governance/audit-policy.yaml`.

## GitLab access

No GitLab MCP is registered for this workspace (per `Config/tooling-plan.yaml`) — query the REST API
directly:

- Base URL, group/repo URLs, and the PAT live in the workspace-root `.env` (`GITLAB_BASE_URL`,
  `GITLAB_TOKEN`, plus one `GITLAB_*_URL` per repo/group). Never print the token value in output.
- Call via PowerShell `Invoke-RestMethod` with header `PRIVATE-TOKEN = $env:GITLAB_TOKEN` — WebFetch
  cannot attach a custom auth header, so it will not work against this private instance.
- Useful endpoints (project/group path URL-encoded):
  - Recent MRs: `GET /api/v4/projects/<id_or_path>/merge_requests?updated_after=<ISO date>&order_by=updated_at`
  - Recent commits: `GET /api/v4/projects/<id_or_path>/repository/commits?since=<ISO date>`
  - Group-wide content search (already used successfully for DEMO-6377/DEMO-6065): `GET /api/v4/groups/<group_path>/search?scope=blobs&search=<keyword>`
- Scope repos to what's realistic for a daily check: `ba_po_spec` (SPEC-REPO) and `dev_product`
  (PRODUCT-REPO) are the two most likely to have sprint-relevant activity; only widen to the full
  `soc_platform_group`/`qc_automation` sweep if the user asks for it — a full-group daily pull is
  expensive and mostly noise (45+ sub-repos).
- If the PAT is missing/expired/rejected (401/403), report GitLab as `NOT_CHECKED` with the reason —
  do not silently skip it or report "no activity".

## Snapshot format (`Outputs/daily/<YYYY-MM-DD>.md`)

```markdown
# Daily Check — <YYYY-MM-DD>

Sprint: <sprint.current> | Prior snapshot: <date or "none — first run">

## Jira — <project key> / <filter>
| Key | Status | Summary | Assignee | Updated |
|---|---|---|---|---|

## QC coverage theo US (sprint hiện tại — squad/US mà QC phụ trách)
<!-- Mục CỐT LÕI anh cần: đánh giá coverage theo TỪNG US, kéo subtask + comment, không phán từ status Story. -->
| US | Status US | Epic | Assignee (dev) | Due | Subtask QC (Create-TC / Execute) | Coverage thật | Gap / việc QC |
|---|---|---|---|---|---|---|---|
<!-- vd: DEMO-7214 | Developing | — | <dev> | 12/09 | DEMO-7322 Create-TC 🟡 / DEMO-7323 Execute ⚪ | TC đã có, execute chưa chạy | ưu tiên execute (due gấp) -->

## Confluence
| Page | Version | Last modified |
|---|---|---|

## GitLab
| Repo | Type | Ref | Title/Message | Author | Updated |
|---|---|---|---|---|---|

## Diff vs prior snapshot
### New
- ...
### Changed
- <key>: <field> <old> -> <new>
### Resolved / Removed
- ...

## Blockers / unreachable sources
- ...
```

## Output Contract

Return the snapshot file path, the three diff lists (or "first run, no diff" if applicable), the GitLab activity found (or why it's `NOT_CHECKED`), and any source that was unreachable. Do not claim "nothing changed" when a source couldn't actually be checked — distinguish `NO_CHANGE_CONFIRMED` from `NOT_CHECKED`.

Also return the **QC coverage-per-US table** (the core thing anh wants out of a daily check): for the squad/US that QC owns, one row per US showing its status, its QC sub-tasks (create-testcase / execute-test) with their real status, the true coverage, and the QC gap — resolved by reading the sub-tasks and comments, not the parent status alone. This turns the raw Jira diff into "what does QC actually need to do today", ranked by due date and blocker.

## Hard rules

- Read-only against Jira/Confluence/GitLab — this skill never comments, transitions, or edits a live issue/page, and never pushes, merges, or triggers a pipeline.
- Never print the GitLab PAT (or any token) in output, even truncated.
- Never fabricate a "prior state" if no snapshot file exists — say it's the first run.
- Never call something "resolved" from absence alone without confirming via the live source (a filter change or access issue can also make an item disappear from view).
