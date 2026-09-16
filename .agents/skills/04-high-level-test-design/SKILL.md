---
name: 04-high-level-test-design
description: Convert approved requirements and risks into high-level test conditions, coverage models, techniques, layers, and priorities without writing detailed step-by-step cases. Use before functional/API testcase generation or specialist test design.
---

# High-level Test Design

Read `Config/QA-Agent/professional-coverage-model.yaml`. Start from the approved applicability matrix/denominator when one exists; otherwise create a draft denominator and mark it `NEED_CONFIRM` for review.

## Workflow

1. Build actor, permission, state, data-flow, integration, and business-invariant models.
2. Derive test conditions using equivalence partitioning, boundary analysis, decision tables, state transitions, use cases, pairwise combinations, and risk-based exploration.
3. Cover positive, alternate, negative, boundary, invalid transition, retry, duplicate, concurrency, partial failure, cross-role, cross-tenant, and readback paths as applicable.
4. Assign each condition a test layer, priority, evidence oracle, data need, and automation suitability.
5. Assign stable `COV-*` IDs and trace conditions to requirements, rules and risks. Set each unit to `DESIGNED`, `NEED_CONFIRM`, `BLOCKED` or `N/A_WITH_REASON`; do not equate design with review, automation or execution. Before setting `NEED_CONFIRM`, search the entire source document (edge-case tables, changelog, appendices too — see `01-review-requirements`), not just the section that looks relevant — carrying forward an already-answered question as `NEED_CONFIRM` wastes a stakeholder's time and erodes trust in the flag.
6. Route complex state, role/tenant, asynchronous, cross-service, historical-data, security or concurrency depth triggers to workflow 26.

## Output

Return a high-level condition catalog and coverage matrix: coverage-unit ID, linked source/risk, intent, applicability, technique, layer, priority, owner, data/role, oracle, automation candidate, status and residual risk. Include denominator state counts. Do not invent detailed expected results.

---

## Bổ sung 2026-09-03 — Đánh giá module ảnh hưởng (bắt buộc)

Từ 2026-09-03, QA workspace tổ chức theo **module sản phẩm**, không theo squad. Mỗi lần phân tích một US, phải trả lời được: **US này chạm những module nào?**

### Vì sao bắt buộc

Một US thường được viết trong phạm vi một module, nhưng hệ quả lan sang module khác. Bỏ bước này thì testcase chỉ phủ module chính, còn lỗi hồi quy nằm ở module bị ảnh hưởng gián tiếp — chỗ không ai kiểm.

Ví dụ thật từ DEMO-5967: ticket ghi *"[Pentest] Vào thẳng link request sau khi đăng nhập lại"*, nhìn như chỉ chạm module `pentest`. Thực tế cơ chế nằm ở `ProtectPage` bọc **toàn bộ 138 route** — tức chạm **mọi module**. Nếu chỉ test màn Pentest thì bỏ sót 137 route còn lại, và bỏ sót luôn lỗ hổng ở `/ingestion-jobs`.

### Cách làm

1. **Xác định module chính** — module mà US được viết cho. Lấy `id` từ `Projects/<ACTIVE_PROJECT>/Config/modules.yaml`, không tự đặt tên.

2. **Truy tìm module bị ảnh hưởng gián tiếp** theo bốn hướng:

   | Hướng | Câu hỏi | Cách tìm |
   |---|---|---|
   | **Dùng chung code** | Component/hook/util nào bị sửa, còn ai dùng nó? | GitLab group search theo tên component |
   | **Dùng chung dữ liệu** | Bảng/collection/enum nào đổi, module nào đọc nó? | Tìm theo tên field trong spec và code |
   | **Dùng chung API** | Endpoint nào đổi contract, ai gọi nó? | Tìm theo đường dẫn endpoint |
   | **Dùng chung luồng nền** | Auth, phân quyền, notification, i18n, layout | Kiểm nếu US chạm bất kỳ thứ nào trong nhóm này |

3. **Ghi thành bảng** trong file review/design, mức ảnh hưởng nêu rõ:

   | Module | Vai trò | Mức ảnh hưởng | Cần test gì |
   |---|---|---|---|
   | `<id>` | chính | trực tiếp | testcase đầy đủ |
   | `<id>` | phụ | gián tiếp qua `<lý do>` | regression tối thiểu |

4. **Nếu US chạm luồng nền** (auth, phân quyền, layout, i18n) → nêu rõ đây là **ảnh hưởng toàn hệ thống**, và đề xuất phạm vi regression tương ứng thay vì chỉ test module chính.

### Testcase bám module, không bám US

| | Cũ | Mới |
|---|---|---|
| Nơi đặt | `Squads/<squad>/Sprint-N/TC/` | **`Modules/<module>/TC/`** |
| Đặt tên | theo US | **theo chức năng của module** |
| Dùng lại | mỗi sprint viết lại | **dùng lại xuyên sprint** |

Testcase là **tài sản của module**, sống lâu hơn US sinh ra nó. Một US mới chạm module cũ thì **bổ sung/sửa testcase sẵn có**, không tạo file mới theo mã US.

Evidence và báo cáo vẫn theo sprint: `Modules/<module>/Sprint-N/Evidence/`.

### Không map được module

**Không tự tạo module mới.** Ghi `NEED_CONFIRM` và hỏi Lead. Module chỉ được thêm vào `modules.yaml` khi có **route thật trên DEV** hoặc **spec đã Released**.
