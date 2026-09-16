# QA Agent Workflow Catalog

Router: `.agents/skills/qa-router/`. Mỗi workflow là một repo-native skill độc lập, có input gate, procedure, safety gate và output contract.

| # | Workflow | Kết quả chính |
|---:|---|---|
| 01 | Review requirements | Requirement/rule/risk matrix và câu hỏi cần xác nhận |
| 02 | Sprint test plan | Scope, strategy, entry/exit, schedule và risk của sprint |
| 03 | Feature test plan | Test plan chi tiết cho US/feature |
| 04 | High-level test design | Models, conditions và coverage ở mức cao |
| 05 | Generate test specification | Scenario/spec thủ công từ business rule |
| 06 | Generate functional testcases | Testcase functional theo canonical schema |
| 07 | Design accessibility testcases | Cases theo target accessibility đã duyệt |
| 08 | Generate API testcases | Cases contract/business/negative/integration |
| 09 | Review testcases | Review quality, traceability và gaps |
| 10 | Generate test data | Data classes, builders, privacy và cleanup |
| 11 | Generate automation script | Robot/Playwright/API/k6/Appium code từ TC duyệt |
| 12 | Set up test automation | Framework, structure, CI, reporting và secrets |
| 13 | Execute approved testcases | Execution ledger, evidence, defects và residual risk |
| 14 | Professional API testing | API assurance đầy đủ và business readback |
| 15 | Functional happy-path testing | Critical positive E2E journeys |
| 16 | Usability testing | Findings theo persona/task/observable criteria |
| 17 | Reliability/resilience testing | Failure, recovery, consistency, RTO/RPO evidence |
| 18 | Exploratory testing | Charter, session notes, findings và follow-up |
| 19 | Execute accessibility testing | Automated + manual + assistive-technology evidence |
| 20 | Design benchmark testing | Reproducible benchmark protocol |
| 21 | UI/UX testing | Design/behavior/responsive/state findings |
| 22 | Contract compatibility testing | Backward/forward compatibility matrix |
| 23 | Security testing | Authorized risk findings theo rules of engagement |
| 24 | Test coverage audit | Requirement-risk-TC-automation-execution traceability |
| 25 | Performance testing | Load/stress/spike/soak/volume/capacity results |
| 26 | Deep coverage testing | Hidden cases từ state/decision/race/failure/data lineage |
| 27 | Execute benchmark testing | Controlled baseline comparison and variance |
| 28 | Frontend E2E testing | Playwright journeys, readback và failure artifacts |
| 29 | Mobile feature testing | Device/OS/lifecycle/network/permission coverage |
| 30 | Business-logic bug hunt | Confirmed invariant violations hoặc NEED_CONFIRM |
| 31 | Sanity testing | Focused confidence cho change/hotfix |
| 32 | Smoke/regression testing | Build gate hoặc impacted/full regression |
| 33 | Test reporting | Evidence-backed metrics, risk và recommendation |
| 34 | Database testing | Integrity/transaction/migration/query/reconciliation |
| 35 | Infrastructure/session testing | Routing/TLS/cache/token/cookie/failover behavior |
| 36 | Log Jira defect | Draft/deduplicate/create/readback theo format của anh |
| 37 | Retest Jira defect | Retest defect+comments+fix delta và controlled verdict |
| 38 | Query data by assurance level | Least-invasive query/readback L0–L4 |
| 39 | Issue triage | Validity, duplicate, severity/priority và routing cho issue chưa qua sàng lọc |
| 40 | AI output testing | Invariant/consistency/grounding/leakage cho output do model sinh |
| 41 | Generated file testing | CSV/Excel/PDF/JSON export: encoding, contract, scale, authorization, lifecycle |
| 42 | Document conflict analysis | Conflict record có severity/blocking + câu hỏi cho người quyết |
| 43 | Risk & change impact | Impact map 17 chiều, risk score có giải thích, độ sâu test cần thiết |
| 44 | Test advisor | Checklist loại test tick được (MINIMUM/RECOMMENDED/DEEP) kèm lý do và effort |

Cập nhật 2026-09-16: bảng trước đây dừng ở 39 và thiếu `40`/`41` đã tồn tại — đã bổ sung cùng ba skill mới `42`–`44`.

Bảy skill hỗ trợ ngoài dãy số:

- `qa-router`: chọn và sắp xếp skill; chính sách ở `Config/QA-Agent/router-policy.yaml`.
- `jira-test-subtasks`: tạo draft hoặc tạo live đúng hai QA subtasks.
- `qmetry-testcase-import`: discover schema, validate, dry run, import và readback.
- `testrail-testcase-import`: tương đương cho TestRail, chọn theo `integration.test_management.tool`.
- `master-test-plan`: chiến lược test cho cả project/milestone (MVP, launch), xuyên nhiều sprint — tầng trên `02`, không thay thế nó.
- `daily-check`: check Jira/Confluence đầu ngày, diff với snapshot hôm trước để chỉ ra chỗ mới/đổi.
- `end-of-day`: chốt cuối ngày, ghi CURRENT_STATE + audit event — cặp đối xứng của `daily-check`.

Các số trùng mục đích đã được tách rõ: 07 thiết kế accessibility, 19 thực thi; 20 thiết kế benchmark, 27 thực thi; 05 tạo test specification, 11 tạo automation code.
