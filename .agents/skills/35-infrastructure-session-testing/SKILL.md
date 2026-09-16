---
name: 35-infrastructure-session-testing
description: Test infrastructure-facing behavior and session lifecycle across routing, TLS, caching, authentication tokens, cookies, expiry, revocation, concurrency, failover, deployment, observability, and data-pipeline infrastructure (Kafka, CDC, ETL, catalog). Use for environment, session, and data-pipeline assurance.
---

# Infrastructure and Session Testing

Do not disrupt infrastructure, rotate secrets, invalidate shared sessions, inject failures, or purge/replay data-pipeline state without explicit approval — this applies equally to the web-facing infra below and the data-pipeline infra section.
Read `Config/QA-Agent/professional-coverage-model.yaml`. Treat topology and pipeline maps as versioned knowledge inputs, not permanent truth embedded in this skill.

## Procedure — web/session infrastructure

1. Map environment topology, routing and load balancing, TLS termination, proxy/CDN/cache, identity provider, session store, token types, cookie policy, and observability.
2. Cover login, expiry, refresh, logout, revocation, password or role change, concurrent sessions, device/session limits, idle and absolute timeout, replay, clock skew, and cookie attributes.
3. Cover sticky and non-sticky routing, failover, instance restart, rolling deployment, cache invalidation, configuration consistency, headers, and error handling as applicable.
4. Verify user behavior, server state, logs, traces, alerts, security controls, and data consistency.
5. Separate application, identity, network, configuration, and environment failures.

## Procedure — data-pipeline infrastructure (Kafka / CDC / ETL / catalog)

This section is worked from a real Ingestion architecture example (originally observed on a project no longer in this workspace) to show how to test a data pipeline; skip it (and test the active project's own pipeline stages using the same verify-real-effect-not-just-configured principle) if the active project has no comparable Kafka/CDC/ETL/catalog stack.

The cached topology candidate in `Projects/<ACTIVE_PROJECT>/Knowledge-Base/API-Specs/ingestion-service.md` currently describes source (JDBC batch or Debezium CDC) -> Kafka -> SeaTunnel -> Bronze -> catalog/lineage -> serving, with schema registry and DLQ/quarantine. Re-fetch the live contract and inspect the knowledge record's status/owner before each scoped design. Use confirmed contract facts for topology discovery; use only `APPROVED` rules as PASS/FAIL business oracles. Keep unresolved behavior `NEED_CONFIRM`. When the stages apply, test each explicitly:

1. **Kafka health and lag** — topic/partition existence, broker reachability, consumer group lag (is the pipeline falling behind, not just "is the broker up"), retention window vs actual consumption speed (are messages expiring unread).
2. **CDC connector health** (Debezium) — connector actually running and capturing insert/update/delete, not just configured; verify via the `connector/restart` and diagnostics endpoints and by confirming a real source-side change produces the expected downstream event.
3. **ETL job integrity** (SeaTunnel) — job completion status via `runs` history, partial-failure behavior (does a failed job leave Bronze in a half-written state or roll back cleanly), retry behavior.
4. **Catalog registration** (Gravitino / OpenMetadata) — a newly-ingested Bronze table is actually registered and discoverable, and lineage correctly shows source -> Bronze -> downstream; a table that exists but isn't cataloged is a real, silent defect class.
5. **Schema drift and DLQ** — a source-side schema change is detected (`schema-drift` endpoint) rather than silently corrupting downstream data; records that fail validation land in DLQ/quarantine (not dropped), and quarantine resolve/discard/replay behaves per `Projects/<ACTIVE_PROJECT>/Knowledge-Base/API-Specs/ingestion-service.md`.
6. **Offset recovery** — after a simulated failure, `recover` restores from the correct Kafka offset without duplicating or losing events (verify via a controlled, approved test, not in a shared environment without approval).

### Tooling note

Read-only broker/topic observability can reuse the pattern already used for another project (`_probe_kafka_broker.robot` in the connected Robot Framework repo): browser automation against the Kafka UI's own REST API (`/api/clusters`, `.../brokers`, `.../topics`) rather than a raw Kafka client. The active project's equivalent Kafka UI URL/cluster ID is not yet confirmed — `NEED_CONFIRM` before reusing this pattern here. Deeper testing (produce/consume, schema/DLQ behavior, offset recovery) needs a direct Kafka client (e.g. `confluent-kafka`/`kafka-python`) or CLI (`kcat`), which is not yet installed — confirm which one anh wants before installing (see `Projects/<ACTIVE_PROJECT>/Config/tooling-plan.yaml`).

## Output Contract

Return topology/session assumptions (and, when data-pipeline scope applies, the pipeline stage map above), build/environment, scenario matrix, expected/actual, telemetry/readback, evidence, classification, severity, and operational risk. For data-pipeline findings, state which stage failed (Kafka/CDC/ETL/catalog/schema) — do not report a generic "ingestion failed" without isolating the stage.

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
