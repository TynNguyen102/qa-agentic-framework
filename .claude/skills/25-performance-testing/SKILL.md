---
name: 25-performance-testing
description: Design or execute authorized load, stress, spike, soak, volume, and capacity testing with realistic workloads, service objectives, observability, and bottleneck analysis. Use for system performance assurance.
---

# Performance Testing

Run resource-intensive tests only in an approved environment with capacity owners, monitoring, stop thresholds, and rollback.

## Procedure

1. Derive workload from business volumes, arrival rates, concurrency, journey mix, data distribution, think time, peaks, and growth.
   - For data-pipeline flows, consider file/data size, rows per second, connector count, concurrent jobs, queue depth and end-to-end ingestion latency when applicable.
2. Record build, infrastructure, topology, dependencies, client location, cache state, dataset, and service objectives.
3. Select the required type: baseline, load, stress, spike, soak, volume, or capacity. Do not combine purposes without clear phases.
   - Derive ramp, duration, load multiplier and soak length from the approved workload/SLO; do not import fixed JMeter or legacy-project values.
4. Measure percentiles such as p50, p95, and p99, throughput, errors, saturation, queueing, resource use, database behavior, and downstream latency.
5. Correlate client results with infrastructure, application, database, queue, and dependency telemetry. Reconcile functional correctness under load.
6. Separate transport errors, timeouts, business rejections and HTTP-success/business-failure responses. Treat bottleneck mappings as hypotheses until telemetry supports them.

## Output Contract

Return workload, environment fingerprint, approvals, thresholds, run record, latency distribution, throughput, errors, resource evidence, bottleneck hypothesis, capacity conclusion, and residual risk.

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
