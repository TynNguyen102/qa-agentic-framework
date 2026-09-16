---
name: 02-sprint-test-plan
description: Create or update a sprint-level QA plan covering stories, risk, environments, data, resources, execution waves, automation, non-functional testing, entry and exit gates. Use during sprint planning, QA kickoff, scope change, or sprint readiness review.
---

# Sprint Test Plan

## Workflow

1. Read sprint scope, story status, dependencies, release goal, team capacity, environments, and prior regression risk.
   - If an approved Master Test Plan exists, record its version and write sprint-specific deltas instead of duplicating unchanged strategy, metrics, suspension rules and governance.
   - If it does not exist, keep the sprint plan self-contained and mark missing strategic decisions `NEED_CONFIRM`.
2. Classify each story by business impact, change surface, data sensitivity, integration depth, and automation readiness.
3. Define test levels, ownership, environments, fixtures, execution order, regression pack, and specialist testing needs.
4. Plan requirement review, testcase review, automation, execution, defect/retest, reporting, and contingency windows.
   - Include a sprint-close business-journey review: map completed US flows into critical cross-feature journeys, decide Robot/Playwright ownership, generate/update suites, then run impacted regression.
5. Define measurable entry, suspension, resumption, and exit criteria with source, formula, owner and verification method. Do not invent pass-rate, health-score, severity or open-defect thresholds.
6. Surface missing Jira filter, test management cycle/folder/run (QMetry or TestRail), environment, account, data, or specification as blockers.

## Output

Write sprint objectives, in/out scope, risk matrix, story-to-test-type matrix, schedule/waves, resources, environments, data, automation plan, defect flow, reporting cadence, entry/exit gates, dependencies, and open decisions. Do not claim committed dates or capacity without sources.

Before `DONE`, verify scope snapshot, capacity gap, inherited Master Plan version, environment/data readiness, regression and linked-defect impact, and all unresolved decisions. Use role/alias or `NEED_CONFIRM` for unconfirmed people.

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
