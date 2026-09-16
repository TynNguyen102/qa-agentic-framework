---
name: 28-frontend-e2e-testing
description: Design, generate, or execute frontend end-to-end tests with Playwright using stable locators, isolated data, role fixtures, business readback, cross-browser coverage, and diagnostic artifacts. Use for browser E2E journeys.
---

# Frontend E2E Testing

Follow the existing Playwright framework in `Automation/Playwright/` or the official application test repository.

Read the Playwright section of `Projects/<ACTIVE_PROJECT>/Config/automation-structure.yaml`. Do not claim artifact capture when no config/run artifact exists.
Read `Config/QA-Agent/professional-coverage-model.yaml`; select approved critical business-flow coverage units, not only convenient UI paths.

## Procedure

1. Select critical user journeys by business outcome, role/tenant, state, risk, change, integration and supported browser/device matrix. Include interruption/reentry, error/recovery and cross-feature handoffs when applicable.
   - Archetype journeys to weigh when selecting: saga / circuit-breaker (multi-service transaction with compensation on partial failure), offline-sync (reconnect + conflict resolution), eventual-consistency (read-after-write lag across services), and cross-feature handoff (one feature's output becomes another feature's input).
2. Set up state through approved APIs or fixtures when that improves speed and reliability; validate the actual journey through the UI.
3. Prefer accessible role, label, and test-contract locators. Avoid brittle CSS chains and fixed sleeps.
4. Isolate accounts and data, clean up deterministically, and avoid order-dependent tests.
5. Assert user-visible outcomes and every required API, DB, event, audit or downstream readback. Do not mark a journey `PROVEN` from the final page alone.
6. Wrap each meaningful business step/checkpoint in `test.step`; keep low-level clicks inside the relevant business step so traces remain readable.
7. Apply the configured evidence mode:
   - `standard`: retain trace on failure/first retry, screenshot on failure, video on failure, and failure diagnostics.
   - `audit`: retain trace/video and take screenshots at each business checkpoint plus failure.
8. Redact secrets/PII and send large traces, screenshots and video to approved artifact storage; keep sanitized references in reports.
9. If Playwright or the target app is unavailable, generate reviewed code and exact commands but do not claim execution.

## Resolve unresolved selectors on a live browser (`test.fixme` → real test)

When a generated spec/POM carries `NOT_FOUND` stubs or `test.fixme` (selector unconfirmed), mature them against a live browser on **DEV only (never PROD)** — this operationalizes no-verdict-without-runtime:

- List every `NOT_FOUND` stub in the POM and every `test.fixme` in the spec; if none, the script is clean — stop.
- Navigate to the feature (URL from config/`BASE_URL`, DEV host). If it redirects to login, refresh the session (mint-cookie / `save-session`) — do not proceed against an unauthenticated page.
- Discover each selector by priority: `data-testid` → role+text → `aria-label` → structural → text. Drive the UI to the state that renders the element (open modal / hover / conditional) before snapshotting; never invent a selector.
- Classify: **found** → replace the stub with a real `readonly Locator` and resolve `test.fixme` to a real `test(...)`; **exists-but-timing** → add a condition-based `waitFor` (never `waitForTimeout`), note why; **absent** → keep `test.fixme` and record the reason (BUSINESS / DATA / UI-version). Never convert an unverified case into a passing `test` — an unresolved case stays `test.fixme`.
- Smoke the resolved flow on the open browser against the testcase's expected result, then report resolved vs still-fixme and the exact re-run command. Editing the generated spec/POM is fine here; running against a live environment still follows the approval and PROD rules above.

## Output Contract

Return coverage-unit/journey-to-test mapping, files, projects, roles/states/data, tags, assertions/readback, denominator state changes, verification result, commands, evidence paths, flaky risks, untested browsers/flows and residual risk.

At sprint close, generate/update cross-feature journeys only from an approved business-journey map across completed User Stories. This requires an explicit user/CI/Jira/Workspace Agent trigger; local files alone do not make the process automatic.

## Bổ sung 2026-09-07 — Cross-module blast radius (bắt buộc trước khi test)

Trước khi thiết kế/chạy E2E hoặc UI/UX, đọc `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/_cross-module-map.md`:

- Xác định module đang test **là consumer của shared component/logic nào** (pagination · filter-chip/search-box/table-display · BasePage/NavPage · ProtectPage route-guard · RBAC · SLA/breach counter · verdict model · whitelist→alert · node error classifier · CMDB asset data…).
- US **chỉ DÙNG** shared đó → test thêm invariant của shared ngay trên màn này.
- US **SỬA chính shared** đó → regression **TOÀN BỘ module ở cột "Blast radius"** của map, nêu rõ trong scope — không chỉ test màn đang làm. Đây là câu trả lời cho "module khác làm giống thì logic bên này có ảnh hưởng không".
- Hit **INFERRED** phải soi live (mở đúng component/struct/collection) xác minh trước khi tính là ảnh hưởng — không tự tin liệt kê chung với CONFIRMED.

Cùng recall `Defects/INDEX.md` + `Domain-Rules/<module>/_overview.md` (như recall-gate skill 01). Phát hiện shared MỚI → ghi vào `_cross-module-map.md` (kỷ luật chưng cất, skill 13/33).

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
