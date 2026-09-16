---
name: qa-router
description: Route QA requests to the numbered professional testing skills for the active project. Use for new User Stories, sprint planning, testcase generation or review, execution, automation, non-functional testing, bug hunting, reporting, Jira defects, retest, or data-query validation when the correct workflow must be selected and sequenced.
---

# QA Router

## Route

1. Read `project/active-project.yaml` to resolve `<ACTIVE_PROJECT>` (ask if it lists more than one and the user hasn't said which). Then read `README.md`, `AGENTS.md`, `SKILL.md`, `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md`, `Projects/<ACTIVE_PROJECT>/qa-config.yaml`, `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml`, and `Config/QA-Agent/professional-coverage-model.yaml`. Read `Config/QA-Agent/api-coverage-profile.yaml` when API/backend/event scope exists.
2. Select one primary role mode from the agent profile and the narrowest numbered skill (01-44) matching the request. Route unscreened issues through `39-issue-triage`; use multiple skills only for dependent phases. Check the `applies_when` clause of the `ai_and_model_output` and `generated_files_and_exports` dimensions — both cut across modules and are easy to miss when routing by feature name alone. Routing signals, fan-out limits, next-skill rules and suite classification are specified in `Config/QA-Agent/router-policy.yaml` — read it before building a plan; never route on keyword match alone.
3. Keep scope limited to `<ACTIVE_PROJECT>` — do not borrow another project's business rules, data, or environment as truth for this one. Apply `governance/knowledge-policy.yaml`; only `APPROVED` knowledge may serve as a PASS/FAIL oracle.
4. Start with requirement sources and business invariants. Build an explicit coverage denominator across applicable BE/API/data, FE/UI/UX, flow/business, security and non-functional dimensions before design, data, execution, evidence and reporting.
5. Check the selected competency's readiness. `DESIGN_ONLY` must not claim execution; `EVIDENCE_PROVEN` requires eval and audit evidence.
6. Treat Jira, Confluence, QMetry, API, DB, browser, mobile, CI, and Git capabilities as unavailable unless the current runtime exposes them.

## Mandatory pre-chain (new US / ticket / change request)

Before any test design (`05`/`06`/`07`/`08`), run and record: `01-review-requirements` ->
`42-document-conflict-analysis` -> `43-risk-and-change-impact` -> `44-test-advisor` (user confirms
scope). A `BLOCKER` conflict from `42` stops design in the affected components until gate **G1** is
cleared. Skip conditions and the full rule set are in `Config/QA-Agent/router-policy.yaml`
(`mandatory_prechain`). Retest (`37`) and sanity/smoke (`31`/`32`) may reuse the most recent risk
record instead of re-running `43`.

## Artifacts this router must read but historically forgot

- `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml` — confirmation gates + bug dimensions, for any defect/bug-hunt flow.
- `Config/QA-Agent/assurance-levels.yaml` — L0-L4; required for any flow touching data or an environment.
- `Config/QA-Agent/tool-adapters.yaml` — pick a tool by capability, not by name. Any tool named in a skill is the current default, not a constraint; check `Projects/<ACTIVE_PROJECT>/Config/tool-inventory.yaml` first and treat `NOT_INSTALLED`/`NOT_CONFIGURED` as absent. No usable adapter => `NEED_CONFIG: <capability>_ADAPTER_UNAVAILABLE`, never a claim that it ran.
- `Config/QA-Agent/skill-registry.yaml` — skill versions; record the version used in any durable output.
- `Config/QA-Agent/ui-pattern-checklists/` — UI/UX work.
- `.claude/hooks/pre_jira_write_gate.py` — enforces the pre-bug gates; its Relates→Story check only warns, so confirm the Story link yourself.
- `evals/qa-agent/eval-suite.yaml` — rerun after any large router/config change (baseline is stale since 2026-07-19).

## Mandatory gates

- Human approval gates G1-G9 are listed in `governance/HUMAN_APPROVAL_GATES.md`. A gate blocks — stop and ask; do not self-approve.
- Resolve the active project's test management tool from `Projects/<ACTIVE_PROJECT>/qa-config.yaml`'s `integration.test_management.tool` (e.g. `QMetry` or `TestRail`) and read that tool's profile (`qmetry-profile.yaml` or `testrail-profile.yaml`) before producing import-ready output. Allow a labelled candidate preview either way, but return `NEED_CONFIG: TEST_MANAGEMENT_TARGET_VERIFICATION` before import-ready output while `validation.live_import_allowed` is false.
- Validate testcase titles against `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml`; return `NEED_CONFIG: TESTCASE_TITLE_FORMAT_SELECTION` only when its status/selection is not `CONFIRMED`.
- If `Projects/<ACTIVE_PROJECT>/Config/jira-subtask-profile.yaml` lacks title formats, return `NEED_CONFIG: JIRA_SUBTASK_TITLES` before creating live subtasks.
- If `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml` has no `title_format`, allow a Vietnamese description draft but return `NEED_CONFIG: DEFECT_TITLE_FORMAT` before logging a live defect.
- Never claim PASS from HTTP status alone; require business result plus applicable UI/API/DB/audit readback.
- **Reporting integrity (áp cho MỌI trạng thái báo ra, không chỉ verdict).** Trước khi nói `done`/`fixed`/`created`/`updated`/`clean`/`no issues`/một con số/`exists`/`render OK`: nêu bằng chứng vừa quan sát TRONG PHIÊN (tool output · đọc-lại file/byte/DB · grep/diff · nguồn live) và gắn nhãn `CONFIRMED` (đã đo) / `INFERRED` (suy 1 lớp) / `ASSUMED` / `NOT_CHECKED`. Đọc code/spec/MR KHÔNG phải bằng chứng runtime; MR merged/closed ≠ đã fix; kết quả rỗng/skip ≠ pass; fixture cũ ≠ trạng thái hiện tại; ghi file/Jira/Confluence xong phải readback trước khi báo "đã xong"; số liệu phải từ đếm/query thật (có denominator). Không xác minh được thì nói thẳng "chưa xác minh, cần X" — KHÔNG lấp bằng phỏng đoán trình bày như sự thật.
- Never accept an empty list, an empty result set or a skipped test as PASS evidence when the interface or runner cannot distinguish it from failure; record `BLOCKED` or `NEED_DATA` instead.
- Route to `40-ai-output-testing` before claiming any AI-backed output passes, and state the oracle class plus repeat count; a single sample never proves a consistency claim.
- Route to `41-generated-file-testing` whenever the feature produces a downloadable file; a byte-level or parser check alone is not sufficient evidence.
- Never claim complete/100%/zero-bug coverage without the coverage-unit denominator, state counts and residual risk required by `professional-coverage-model.yaml`.
- Draft locally by default. Live Jira, QMetry, Confluence, Git, environment, or data mutations require explicit approval in the current session.
- **QC chuyển trạng thái story/task sang go-live khi đã đảm bảo chất lượng.** Khi mọi sub-task QC của story/task đó (`Create Testcase` + `Execute test`) đã `Closed`/`Done`, và không còn bug nào đang mở thực sự chặn go-live (một bug `Open` mà BA/PO đã comment chấp nhận fix sau — accept-known-issue — thì KHÔNG tính là chặn; phải đọc `comment` để xác nhận có đúng câu chấp nhận đó, không tự suy đoán) — QC (không phải BA/Dev) là người chuyển trạng thái Story/Task cha sang `Closed` hoặc `Ready to deploy`, dùng đúng transition đang thật sự khả dụng trên workflow của issue đó (gọi API lấy transitions trước, không đoán tên/ID transition). Ngay sau khi chuyển, **post 1 comment trên chính story/task đó, @mention Dev phụ trách** (accountId lấy thật từ `assignee` của issue, xem [[project-jira-role-convention]] cách @mention đúng) xác nhận tính năng đã được QC đảm bảo, sẵn sàng go-live/deploy. Việc chuyển trạng thái + comment vẫn là live Jira write — chỉ thực hiện khi đã có approve rõ trong phiên hiện tại (đủ điều kiện + user đồng ý), sau đó readback lại status/comment để xác nhận đã ghi thành công trước khi báo "đã xong".

## Router output

State the selected role mode, workflow(s), competency readiness, authoritative sources/rule IDs used, coverage denominator/gaps, unresolved conflicts, action authorization, expected evidence and residual risk. Do not expose internal chain-of-thought.

## Typical chains

- Start of day/session: `daily-check` first — Jira/Confluence status diffed against the last snapshot in `Projects/<ACTIVE_PROJECT>/Outputs/daily/`.
- Project/milestone kickoff (MVP, launch): `master-test-plan` once, then `02` per sprint inherits its version instead of restating strategy.
- New US: `01` -> `42` -> `43` -> `44` (scope confirmed) -> `03`/`04` -> `06`/`08` plus applicable specialists -> `09` -> `10` -> `24` -> `13` -> `33`. Skill `01` chạy **recall local bắt buộc** (`Defects/INDEX.md` + `Modules/<module>/TC` + `Domain-Rules/<module>`) trước khi design — không test US mà bỏ qua finding/quyết định cũ của module.
- **Sprint start** (sprint mới vừa bắt đầu, hoặc cần xác nhận sprint hiện tại): (1) xác nhận sprint
  active thật qua Jira Agile API (`GET board/{boardId}/sprint?state=active`, KHÔNG suy đoán từ ngày
  tháng) → cập nhật `qa-config.yaml` `sprint.current/start_date/end_date/goal` nếu lệch; (2) pull toàn
  bộ item sprint qua JQL (`project=<key> AND sprint=<id>`, phân trang bằng `nextPageToken` nếu dùng
  `/search/jql`), nhóm theo squad thật qua field `Team` (`customfield_10001`, KHÔNG suy đoán tên squad
  từ text sprint goal — goal có thể dùng tên khác Team field thật), loại `Sub-task` khỏi bảng scope
  chính → ghi `Sprints/Sprint-<N>/scope-<squad>.md` (mẫu: nhóm 🔴 Ready to test / 🟡 Developing / ⚪
  Chưa bắt đầu / 🔵 Pending khác / ✅ Done-Closed, không bỏ sót bucket nào); (3) `02` cho sprint test
  plan — kế thừa Master Test Plan cũ (ghi version, chỉ viết phần delta, không lặp lại chiến lược không
  đổi); (4) **với mỗi story ưu tiên (risk Rất cao/Cao)**: kiểm tra đã có đủ 2 subtask QC chưa
  (`Create Testcase` + `Execute test` — field `subtasks` của story, đối chiếu tên thật đang tồn tại
  trên Jira thay vì chỉ tin `jira-subtask-profile.yaml` nếu nghi ngờ lệch) và đọc `comment` của story
  xem có câu hỏi BA/Dev nào còn treo chưa trả lời; nếu thiếu subtask hoặc chưa có testcase thật, pull
  spec (link trong `description`, hoặc `SPEC-REPO`/`PRODUCT-REPO/specs/` nếu không có link) TRƯỚC khi
  soạn nội dung AC/DoD thật cho subtask mới (không tạo bằng placeholder); nếu spec có Open
  Questions/câu hỏi chưa trả lời, subtask phải flag rõ phần đó `NEED_CONFIRM` **và post thêm 1 comment
  trên story cha @mention đúng BA (accountId thật qua `reporter`) liệt kê rõ từng câu hỏi còn mở —
  không chỉ ghi trong nội dung subtask, xem rule chi tiết trong `jira-subtask-profile.yaml`**, không
  tự chọn 1 phương án rồi coi là final; xác nhận danh sách dự kiến tạo với anh trước khi tạo live (số
  lượng, nội dung
  tóm tắt) — sau khi tạo, set `assignee` ngay trong request (xem rule trong
  `jira-subtask-profile.yaml`, đừng để trống rồi sửa sau); khi cần @mention BA/Dev trong comment, lấy
  `accountId` thật qua `reporter`/`assignee`/`customfield_10283` (Multiple assignees) của story đó,
  không đoán tên. Sau đó mới sang `24` -> execution skills -> `33`.
- Sprint (đã có test plan, tiếp tục theo dõi giữa sprint): `02` -> `24` -> execution skills -> `33`.
- Sprint-close business journey: `24` cross-US audit -> approved journey map -> `11` Robot or `28` Playwright -> `32` impacted regression -> `33`.
- Automation with an established framework: approved testcase -> `11` -> dry-run -> `32`; if framework foundations are missing: `12` -> `11`.
- Defect: observation/report -> `39` -> `30` when investigation is needed -> `36`; fix delivered -> `37` -> `32` -> `33`.
- API: `01` -> API operation/coverage inventory -> `08` -> `10` -> `09`/`24` -> `14` -> `22`/`23`/`25`/`34`/`35`/`38` as risk requires.
- AI/LLM-backed feature (Copilot, Investigator, triage, scoring): `01` -> `04` -> `40` before any functional pass is claimed; `23` for injection depth, `20`/`27` when comparing model or provider versions. A model, prompt-version or provider change is a regression event -> `40` baseline rerun -> `32`.
- Any feature that hands the user a file (export, template, error file, report): `41` alongside the functional skill, never instead of it. `41` requires opening the file in the real consuming application and locale; a byte-level check alone may not close a file defect.
- Jira QA subtasks: `jira-test-subtasks` after the parent story and title profiles are available.
- Test management import: `06` or `08` -> `09` -> candidate preview; live import only after target-project schema/field/folder-or-section/allowed-values verification in `qmetry-testcase-import` (QMetry) or `testrail-testcase-import` (TestRail) — whichever `integration.test_management.tool` the active project's `qa-config.yaml` names.
- Unscreened incoming issue (Jira/support/monitoring): `39` -> `30`, `36`, `01`, `37`, or `NO_QA_ACTION` depending on triage verdict.
