---
name: 12-setup-test-automation
description: Plan or scaffold an automation framework after confirming the official repository, stack, package manager, versions, CI, and environment constraints. Use when automation foundations or missing framework structure must be established.
---

# Set Up Test Automation

Do not install packages or invent a new framework until the official repository, supported versions, execution environments, and CI expectations are known.

## Procedure

1. Inventory the existing framework, dependencies, test commands, reports, secrets strategy, and CI jobs.
   - Resolve shared configuration first, then `Projects/<ACTIVE_PROJECT>/qa-config.local.yaml` for member-specific repository paths. Never commit an absolute member path.
2. Select only the layers required by the project:
   - Robot Framework: follow the connected repository profile. Resolve the active project's own folder from `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml`'s project mapping — use `<project_root>/<JIRA_KEY>/` for story suites and `<project_root>/BusinessJourneys/<SPRINT_ID>/` for cross-US journeys, with shared `KeywordLibraries/<PROJECT>`, `KeywordLibraries/<PROJECT>-API`, `DataTest/<PROJECT>`, `Variables`, `ExternalSystem`, and `Libs` layers.
   - Playwright: UI/API suites, page or component models, fixtures, utilities, data builders, projects, traces, and reports.
   - k6: workloads, environment config, thresholds, and ignored results.
   - Appium: device capabilities, platform drivers, screens, fixtures, and device lab integration.
3. Add environment templates without secrets, ignored result directories, naming/tagging conventions, linting, dry-run commands, and CI stages.
4. Apply idempotent file rules: create missing scaffolds, preserve existing files, skip equivalent content, and ask before replacing materially different framework files.
   - If the official Robot repository uses a materially different structure, report the conflict and propose a migration/mapping; do not reorganize it without approval.
   - Never scaffold the active project into a dirty official worktree or into another project's root in the Robot repo; request the exact branch/target approval first.
5. Define test isolation, data lifecycle, retries policy, artifact retention, and evidence paths.
6. Validate the smallest local example. Request approval before package installation, external downloads, or live CI changes.

## Output Contract

Return the architecture decision, proposed or changed tree, dependencies, commands, CI impact, secrets handling, verification result, and unresolved prerequisites.

Before `DONE`, verify the required layers, environment templates, base resources/fixtures, ignored artifacts and dry-run command. Use `SKIPPED` when the approved structure already exists, not as an excuse to avoid validation.

## Chọn tool (bổ sung 2026-09-16)

Skill này có nhắc tên tool cụ thể ở trên. Tên tool là **mặc định hiện tại của workspace**, không phải
ràng buộc cứng — việc chọn tool đi qua `Config/QA-Agent/tool-adapters.yaml`:

1. Xác định **capability** cần dùng (vd `ui_browser_automation`, `api_testing`,
   `acceptance_suite_runner`, `load_and_performance`, `database_query`).
2. Đọc `Projects/<ACTIVE_PROJECT>/Config/tool-inventory.yaml` — tool `NOT_INSTALLED`/`NOT_CONFIGURED`
   thì coi như **không có**, dù được nhắc tên ở đây.
3. Chọn adapter `rank` thấp nhất **thực sự khả dụng**.
4. Không adapter nào khả dụng ⇒ trả `NEED_CONFIG: <capability>_ADAPTER_UNAVAILABLE`.
   **Không** claim đã chạy.

Đổi adapter **không** đổi contract: `outputs` phải giữ nguyên hình dạng để skill sau dùng được.
