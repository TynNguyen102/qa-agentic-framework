# Testcase Template

Renders `Config/QA-Agent/canonical-testcase-schema.yaml` — the single internal testcase model. All tools (QMetry, TestRail, Jira, Robot, Playwright, report) map **from** this schema; don't invent a different field set per tool.

| Field | Notes |
|---|---|
| `external_id` | Stable local ID, independent of the test management tool's own ID |
| `title` | Format per `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml` — do not invent one if that profile isn't confirmed yet for this project |
| `objective` | One line, business intent |
| `linked_requirements` | US/AC key(s) |
| `linked_rules` | Domain-Rules reference(s), if any |
| `linked_coverage_units` | Applicable `COV-*`/`API-COV-*` IDs from the approved coverage denominator |
| `risk` | `critical` / `high` / `medium` / `low` |
| `priority` | |
| `test_type` | e.g. functional, negative, boundary, state, security |
| `preconditions` | |
| `roles` | |
| `environment` | |
| `protocol` | UI, REST_HTTP, GRAPHQL, GRPC, WEBSOCKET, ASYNC_EVENT, DB, MOBILE or another approved value |
| `oracle_layers` | Required UI/API/DB/EVENT/AUDIT/CACHE/QUEUE/DOWNSTREAM/LOG_TRACE evidence |
| `steps` | Each: `step_no`, `action`, `test_data`, `expected_result`, `readback_oracle` |
| `automation_candidate` | |
| `tags` | |
| `need_confirm` | List anything the expected result depends on that isn't confirmed yet |
| `residual_risk` | Applicable behavior/risk not proven by this case |
| `source_evidence` | Where the expected result traces to |

## Hard rules (from the schema)

- Expected results must cite a confirmed source for the active project — HTTP status alone is never a business expected result.
- Map to the active project's test management tool only through its confirmed profile (`qmetry-profile.yaml` or `testrail-profile.yaml`, per `qa-config.yaml`'s `integration.test_management.tool`) — do not invent a layout while that profile is `NOT_CONFIGURED`/`NEED_CONFIG`.
- Do not treat a title as validated until `Projects/<ACTIVE_PROJECT>/Config/testcase-title-profile.yaml` is `CONFIRMED` for this project.
