---
name: 10-generate-test-data
description: Design and generate safe test data for functional, API, UI, DB, mobile, security, performance, and stateful testing. Use when valid, invalid, boundary, combinatorial, lifecycle, tenant, role, volume, or cleanup-ready fixtures are needed.
---

# Generate Test Data

## Workflow

1. Read field schemas, business constraints, referential relationships, state machines, tenant/role rules, privacy policy, and environment limits.
2. Partition data into valid, alternate, invalid, boundary, null/missing, wrong type/format, duplicate, expired/future, stateful, cross-field, cross-role, and cross-tenant sets.
3. Use min-1/min/min+1 and max-1/max/max+1 boundaries; pairwise for interactions; separate deterministic cases from fuzzing.
4. Generate synthetic data only. Mask PII and never copy production secrets.
5. Define setup, ownership, uniqueness, reset, cleanup, retention, and parallel-run collision handling.
6. Do not create or mutate live data unless assurance level and approval allow it.
7. When producing an actual DB/API seed script (not just a data catalog), it must ship with three things at minimum, modeled on a real working example (DEMO-4609, reviewed 2026-08-27): a **QC marker** on every inserted/created record (e.g. a distinctive ID prefix or tag like `QC-TEST-%`) so seeded rows are trivially identifiable and never mistaken for real data; an **idempotent guard** so re-running the script is safe (skip/upsert on an existing marker, don't duplicate); and an explicit, ready-to-run **cleanup command** (e.g. `DELETE ... WHERE marker LIKE 'QC-TEST-%'`) documented alongside the script, not left as an exercise for whoever runs it later.

## Output

Store or return a data catalog mapping dataset ID to linked cases, values/generator rules, intended validity, state/role/tenant, expected validation, setup, cleanup, sensitivity, environment, and expiry.


## Seed tái lập & cleanup (bổ sung 2026-09-16)

Trước đây thiếu phần này nên mỗi lần regression lại sinh data mới, không so được kết quả giữa các lần chạy.

### Seed

Mọi bộ data sinh ra phải khai **seed** để lần sau tái lập đúng bộ đó:

```yaml
dataset_id: DS-<module>-<YYYYMMDD>-<NNN>
seed: <số nguyên>            # dùng lại seed này thì ra đúng bộ data cũ
generator: <script/skill đã sinh>
generated_at: <ISO>
scope: <module + US + môi trường>
record_count: <số bản ghi thật đã tạo, đếm lại sau khi tạo — không phải số dự định>
prefix: <tiền tố nhận dạng, vd uiA1- / apiA2->
```

- **Prefix bắt buộc** khi có nhiều phiên/nhánh chạy song song — để không giẫm chân nhau và để cleanup
  đúng phần của mình. Xem `Config/QA-Agent/schemas/execution-plan.schema.yaml` mục `parallelization`.
- Regression chạy lại **phải dùng lại seed cũ**, nếu không thì khác biệt kết quả có thể do data chứ
  không phải do sản phẩm — và khi đó verdict là `INCONCLUSIVE`, không phải `FAIL`.
- Seed không áp dụng được (data lấy từ hệ thống thật, không sinh được) thì ghi rõ
  `seed: NOT_APPLICABLE` + lý do, đừng bịa một con số.

### Cleanup

| Loại data | Cleanup |
|---|---|
| Fixture do test tạo (có prefix) | **Xoá sau khi chạy** — ghi lại đã xoá bao nhiêu bản ghi |
| Data làm hỏng trạng thái dùng chung | Khôi phục trạng thái gốc ngay trong cùng testcase |
| Data không xoá được (không có API xoá) | Ghi vào mục **nợ dọn dẹp** của báo cáo + hỏi Lead, **không** im lặng bỏ lại |
| Data trên môi trường dùng chung | Cleanup là **bắt buộc** — môi trường DEV dùng chung với dev và các squad khác |

**Không bao giờ:** chạy lệnh xoá hàng loạt không có điều kiện lọc theo prefix của chính mình.

### NEED_CONFIRM còn mở

- Chưa chốt với Lead nơi lưu registry seed dùng chung giữa các sprint.
  Tạm thời ghi seed vào chính file testcase và ledger execution; khi có registry thì trỏ về đó.
