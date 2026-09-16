---
name: 11-generate-automation-script
description: Generate traceable automation code from approved testcases using the repository's established Robot Framework, Playwright, API, k6, or mobile conventions. Use after testcase review when automation code is requested.
---

# Generate Automation Script

> Token note: for 1-3 approved testcases with an already-confirmed framework/target, generate directly from the testcase content without re-reading this whole file. Read it fully when scripting for a whole module, adding a new keyword/fixture pattern, or when the framework/target isn't yet confirmed.

Generate code only from an approved testcase or an explicitly approved scenario. Preserve the testcase ID, requirement ID, business rule, expected outcome, and evidence needs.

Read `Projects/<ACTIVE_PROJECT>/qa-config.yaml`, the gitignored `Projects/<ACTIVE_PROJECT>/qa-config.local.yaml` when present, `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml`, and `Projects/<ACTIVE_PROJECT>/Config/automation-structure.yaml` before selecting Robot paths. The user requires one folder per Jira User Story within the official framework.

## Selecting which testcases to automate

1. If anh specifies an exact scope (testcase IDs, a module, a file, or any explicit range), follow it exactly — do not add or drop testcases outside that scope, and skip the priority rule below.
2. If no scope is given, prioritize testcases whose canonical record has `automation_candidate: Yes` or `Partial` (per `Config/QA-Agent/canonical-testcase-schema.yaml`) — skip `No` unless anh explicitly asks to script it anyway (and flag that as an override, since `No` means a real exclusion criterion applied).
3. If no testcase has `automation_candidate` set at all (legacy record predating schema v3), stop and ask whether to automate the full set before proceeding — do not assume `Yes`.
4. For a `Partial` case, automate only the steps/assertions its `automation_reason` says are scriptable; keep the rest as a manual step or a `NEED_INPUT` note in the mapping matrix — do not silently automate the whole case or silently drop the non-scriptable part.
5. Use each case's `automation_layers` to choose which layer(s) this script must actually assert (not just the one the tool defaults to): `UI` → Playwright/Robot Browser assertion, `API` → response assertion via Robot/RequestsLibrary/Postman, `DB` → DB reconciliation query. A case listing more than one layer needs an assertion for each listed layer in the generated script, not only the first one reached.
6. If an explicitly-scoped testcase has no `automation_candidate`/`automation_layers` value, still automate it, but note the gap in the mapping matrix and derive the layers from the case's `oracle_layers` instead.

## Procedure

1. Read the target testcase and its review result. Stop with `NEED_INPUT` when the expected business result is ambiguous.
2. Inspect the official automation repository and existing style before choosing a tool:
   - Robot Framework for keyword-driven functional, API, integration, regression, and DB suites.
   - Playwright for browser UI and frontend E2E.
   - API libraries or Postman for service checks when that is the established project stack.
   - k6 for approved performance workloads.
   - Appium only for native or hybrid mobile applications — check `Projects/<ACTIVE_PROJECT>/Config/tooling-plan.yaml` for whether the active project has a confirmed Appium convention yet. Treat any Appium output as a proposal pending the same real-repo confirmation Robot Framework already received, not an established convention.
3. Reuse fixtures, resources, page objects, variables, data builders, and reporting hooks. Do not create a competing framework.
   - Resolve the active project's own folder inside the connected Robot repo from `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml` (its project mapping section) — target `<project_root>/<JIRA_KEY>/` and place type-specific suites directly in that story folder using `test_<jira_key_compact>_<feature_slug>_<type>.robot`. Do not assume a literal folder name from another project.
   - Keep reusable keywords in that project's `KeywordLibraries/<PROJECT>` or `<PROJECT>-API`, data in `DataTest/<PROJECT>`, and environment values in `Variables`; do not clone them for each story.
   - Never write one project's suites under another project's root in the Robot repo, or reuse another project's business truth as this one's. If the resolved project root is absent or the worktree is dirty, return the planned mapping and request approval for the exact safe target before creating files.
4. Produce a mapping matrix before coding with exactly these columns: source testcase ID, type, test level, precondition, business step, expected result, target suite file, high-level keyword, low-level keyword, data used, environment.
5. Add stable tags for requirement, testcase, layer, risk, and suite type.
6. Assert the business outcome and required API, DB, event, audit, or UI readback. A successful HTTP status alone is not a pass.
7. Keep credentials, URLs and environment values outside source control. Make data setup and cleanup deterministic; avoid fixed sleeps and prefer condition-based/explicit waits (e.g. `Wait Until Element Is Visible`/`Wait For Elements State`, never `Sleep`).
8. For layered Robot code, keep low-level actions small (one action per keyword, no branching/looping inside), compose business flows above them in a high-level layer, and centralize business verification in a verification layer that only asserts state — never let a test case call a low-level keyword directly. Follow the official repository rather than hardcoding RESTinstance, RequestsLibrary, Browser, locator attributes or a four-layer layout from another project.
9. Run lint, dry run, or the smallest safe targeted test available. If dependencies or environments are absent, report the exact verification command without claiming execution or CI readiness.
10. For an approved sprint-close request, build a cross-US journey map from completed story sources and generate/update Robot suites under `<project_root>/BusinessJourneys/<SPRINT_ID>/` (same `<project_root>` resolved above). Do not generate a journey merely because individual US suites exist; require the business sequence, shared state/data and expected end result.

## Playwright / TypeScript concrete patterns (browser UI, frontend E2E)

When the chosen tool is Playwright, generate against this project's own framework at `Projects/<ACTIVE_PROJECT>/Automation/ui/` (`pages/BasePage.ts`, `fixtures/persistent-context.ts`, `helpers/`, `playwright.config.ts`) — extend it, never fork a parallel one. Layer as **Page → Action → Spec**:

- **Page Object** (`pages/<MODULE>/<Feature>Page.ts`): `export default class <Feature>Page extends BasePage`; expose locators as public `readonly <name>: Locator` grouped by feature area with comment headers (the spec reads them directly to `expect()`). `navigateTo()` builds the URL from `process.env.BASE_URL` (via config), then awaits the framework's ready signal — never `waitForTimeout`. **Never emit a live host as a URL or fallback; if `BASE_URL` is unset, fail loudly — never default to a real host, and never target PROD** (per `Projects/<ACTIVE_PROJECT>/CLAUDE.md`). A selector unresolved during exploration → a stub getter that throws `NOT_FOUND … re-explore to discover selector`; never invent one. Append new locators under a dated `// ── New: <date> ──` header and keep existing ones.
- **Action layer** (`actions/<MODULE>/<Module>Actions.ts`, only when a flow spans ≥2 page objects): one method = one complete business flow; the spec calls Actions, not Page, for multi-page flows. Register the network listener BEFORE the UI action — `const [res] = await Promise.all([page.waitForResponse(pred), pageX.action()])`; never `await click()` then a separate `await waitForResponse()` (the response is missed). Make the predicate body-aware (`r.request().postData()` + method + endpoint) so a preflight or unrelated call to the same endpoint is skipped; reference endpoints via a committable `constants/<MODULE>/<module>-api.ts` map (URL segments, SCREAMING_SNAKE, no secrets), not hardcoded strings in the predicate. Return a **typed result** interface (e.g. `QueryResult { code; items; reqBody }`, `PatchResult { code; newValue? }`) so the spec asserts business state without knowing internals; capture dynamic expected values (e.g. an option's text) BEFORE the mutating click and return them, so the spec asserts observed state instead of a hardcoded literal. Guard assertions (response parsed, id present) may live in the action; the **business assertion belongs in the spec** — a parsed 2xx is a guard, not a pass (see Procedure step 6).
- **Spec** (`*.spec.ts`): AAA structure; choose `beforeAll` vs `beforeEach` by whether state must be isolated per test; mark an unresolved selector `test.fixme` rather than a fake pass; assert each layer the testcase's `automation_layers` requires.

These patterns augment Procedure steps 2–8; they do not bypass any gate — script only APPROVED testcases, keep the mapping matrix and tags, emit the review request before merge, and never run against a live environment (never PROD) or push without approval.

## CI/CD integration guidance

The connected Robot Framework repo's CI state is recorded in `Projects/<ACTIVE_PROJECT>/Config/robot-framework-profile.yaml: ci_observed` — check it for which project(s) currently have a working pipeline before assuming the active project does. When asked to wire the active project into CI:
1. Confirm the exact `.gitlab-ci.yml` job/stage pattern already used for whichever project has one working before proposing an equivalent for the active project — do not invent a different CI structure.
2. Install/cache dependencies, inject secrets via the CI secret store (never inline), run the confirmed test command, and publish the artifact report (Allure/Robot HTML per `ci_observed.capabilities`).
3. Treat this as a live-execution capability change — draft the proposed job only; do not edit or push `.gitlab-ci.yml` without explicit approval, and never touch it while the worktree has unrelated uncommitted changes (see `robot-framework-profile.yaml: risks_and_gaps`).

## Requesting review before merge

Automation code is not ready to merge or run in CI on its own say-so. When code is ready, emit a review request instead of assuming approval:

```
--- REVIEW REQUEST — 11-generate-automation-script ---
Testcase(s): <IDs>
Files: <paths>
Reviewer: <Team/Members/<alias>.yaml owner if configured, otherwise ask anh who should review>
Checklist: business assertion present (not status-code-only), no hardcoded secret/URL, layered keyword compliance, dry-run/lint result attached
Action requested: reply "Approved" or "Cần fix: <detail>"
---
```

Log the request and its outcome as a `Projects/<ACTIVE_PROJECT>/governance/audit-events/` entry once resolved. Do not merge, run in CI, or mark automation "ready" before an explicit "Approved".

## Output Contract

Return changed files, testcase-to-script mapping (using the columns above), tags, verification performed, commands, evidence path, assumptions, blockers, and the review request block when applicable. Do not push Git or run against a live environment without explicit approval.

Return `DONE` only when the requested code and mapping exist and local verification passes; use `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED` when verification, framework or authoritative expected behavior is incomplete.

This skill does not monitor sprint completion automatically. A user, CI job, Jira automation or Workspace Agent trigger must invoke the sprint-close journey workflow.

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
