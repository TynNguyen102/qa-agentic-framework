---
name: 01-review-requirements
description: Review Jira, Confluence, FRS, API, domain-rule, permission, and data requirements for completeness and testability. Use when a User Story, Epic, feature, change request, or requirement set must be understood before planning or testcase design.
---

# Review Requirements

> **Tóm tắt (VI):** Soi kỹ yêu cầu (US/AC/spec) TRƯỚC khi thiết kế test — recall defect cũ + domain rule, tìm mâu thuẫn/thiếu, chốt oracle. Dùng khi bắt đầu một US mới.

## Inputs

Require the issue/page identifier or supplied requirement text. Read live sources for the active project when available and record source/version.

## Workflow

0. **Tìm và đọc commit/MR thật đã implement story này, nếu đã có** — trước khi phân tích thuần từ Jira/BRD. Với story ở status `Testing`/`In Progress`/`To Review` (đã có code), tra theo thứ tự: (a) branch/MR trùng đúng Jira key (`feat/<KEY>`, hoặc GitLab MR search `search=<KEY>`), (b) nếu không ra, search MR theo từ khoá nghiệp vụ của feature (tên field/hành động — branch/MR không phải lúc nào cũng đặt tên theo Jira key). Đọc **toàn bộ mô tả MR**, không chỉ tên file đổi — mô tả MR thường ghi rõ quyết định kỹ thuật, edge case đã né, và lý do chọn cách làm này thay vì cách khác mà Jira/BRD không bao giờ ghi (ví dụ thật, DEMO-7037 "cho Pentester sửa due date của vuln": Jira chỉ ghi "role Pentester", MR ghi rõ quyền thực tế hẹp hơn — `isPICPentester || hasAppSecAuditPerm`, cố tình KHÔNG dùng hàm rộng hơn "vì hàm đó cũng cho phép người tạo vuln" — chi tiết này quyết định hẳn 1 testcase negative permission mà không nguồn nào khác tiết lộ). Test file dev đã viết kèm MR (`*_test.go`, `*.test.tsx`) cũng đáng đọc lướt — biết dev đã cover gì để không trùng, và tìm khoảng trống dev-test thường bỏ qua (E2E, bypass quyền qua API, cross-screen). Không tìm được MR/commit nào thì ghi rõ đã tìm và không thấy, tiếp tục phân tích thuần từ Jira/BRD như bình thường — đừng chờ hoặc coi là blocker.
1. Extract objectives, actors, triggers, preconditions, rules, states, data, integrations, errors, audit needs, and non-functional expectations.
2. Map each Acceptance Criterion to confirmed business rules and identify contradictions or missing decisions.
3. Check testability: observable result, controllable precondition, obtainable data, environment, role, and measurable threshold.
4. Separate confirmed fact, inference, assumption, and question.
5. Mark missing authority for the active project as `NEED_CONFIRM`; never borrow another project's expected behavior. **Before marking anything `NEED_CONFIRM`, search the ENTIRE source document(s)** — not just the AC/section that seems most relevant — including edge-case tables, changelog/revision history, appendices and footnotes. A real BRD case (2026-08-27, DEMO-4609): a testcase author checked only the AC number they assumed was relevant, missed that the same fact was answered in the Edge Case table a few sections over, and escalated a non-question to BA. Grep the full document for the specific term/behavior in question before escalating.
6. Identify initial risk, impacted modules, regression surface, and required specialist skills.
7. Read `Config/QA-Agent/professional-coverage-model.yaml` and classify each dimension `REQUIRED`, `OPTIONAL_BY_RISK`, `N/A_WITH_REASON`, or `NEED_CONFIRM`. Do not create testcase quotas here.

## Output

Return source register, requirement/AC matrix, business invariants, state/permission/data gaps, testability findings, initial coverage-applicability matrix, risks, blockers, owners, and clarification questions. Do not create detailed testcases in this skill.

## Testability tick-list (per requirement/AC)

Before marking an AC ready for design, confirm each AC is:

- **Observable** — the result is visible on screen or in data/logs, not an internal-only side effect.
- **Measurable** — success/failure is decidable objectively (a value, a state, a threshold), not a subjective feel.
- **Reproducible** — any QA can recreate the precondition and repeat the check deterministically.
- **Independent** — the AC can be verified without silently depending on another AC passing first, or that dependency is stated explicitly.

Example — **not testable:** "the application should be fast". **Testable:** "list page loads in < 2s with 1,000 records on DEV".

NFR mini-checklist (look for an explicit, measurable target; if absent, mark `NEED_CONFIRM`, do not invent one): performance (response-time / throughput target), scalability (concurrent users / data volume), security (authn/authz, encryption, audit expectation), accessibility (conformance target, e.g. WCAG 2.1 AA), browser/device support matrix.

---

## Bổ sung 2026-09-03 — Đánh giá module ảnh hưởng (bắt buộc)

Từ 2026-09-03, QA workspace tổ chức theo **module sản phẩm**, không theo squad. Mỗi lần phân tích một US, phải trả lời được: **US này chạm những module nào?**

### Vì sao bắt buộc

Một US thường được viết trong phạm vi một module, nhưng hệ quả lan sang module khác. Bỏ bước này thì testcase chỉ phủ module chính, còn lỗi hồi quy nằm ở module bị ảnh hưởng gián tiếp — chỗ không ai kiểm.

Ví dụ thật từ DEMO-5967: ticket ghi *"[Pentest] Vào thẳng link request sau khi đăng nhập lại"*, nhìn như chỉ chạm module `pentest`. Thực tế cơ chế nằm ở `ProtectPage` bọc **toàn bộ 138 route** — tức chạm **mọi module**. Nếu chỉ test màn Pentest thì bỏ sót 137 route còn lại, và bỏ sót luôn lỗ hổng ở `/ingestion-jobs`.

### Cách làm

0. **Nếu `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/<module>/_overview.md` đã tồn tại** cho module chính, đọc trước bước 1 — dùng bảng cross-screen effect và checklist tự hỏi có sẵn trong đó để không phải suy luận lại từ đầu cho những liên kết đã biết. File này (`status: DRAFT` cho tới khi được review — xem `governance/knowledge-policy.yaml`'s `module_overview_artifact`) không thay thế bước 2-4 bên dưới: vẫn phải truy tìm live cho shared code/data/API/luồng nền, vì đó là cách duy nhất bắt được ảnh hưởng MỚI mà overview chưa từng ghi (đúng như case DEMO-5967 — không nguồn tĩnh nào biết trước `ProtectPage` bọc 138 route nếu chưa từng có ai ghi lại).
1. **Xác định module chính** — module mà US được viết cho. Lấy `id` từ `Projects/<ACTIVE_PROJECT>/Config/modules.yaml`, không tự đặt tên.

2. **Truy tìm module bị ảnh hưởng gián tiếp** theo năm hướng:

   | Hướng | Câu hỏi | Cách tìm |
   |---|---|---|
   | **Dùng chung code** | Component/hook/util nào bị sửa, còn ai dùng nó? | GitLab group search theo tên component |
   | **Dùng chung dữ liệu** | Bảng/collection/enum nào đổi, module nào đọc nó? | Tìm theo tên field trong spec và code |
   | **Dùng chung API** | Endpoint nào đổi contract, ai gọi nó? | Tìm theo đường dẫn endpoint |
   | **Field/column cụ thể đang sửa** | Field này còn bị ghi/đọc ở luồng ngầm nào (reminder/scheduler worker, notification template, KPI/scoring service, export/report converter, event/queue payload) mà một US đơn lẻ không bao giờ nhắc? | GitLab group search theo đúng tên field/column (không phải tên tính năng) — xem quy trình xác minh bắt buộc ngay dưới |
   | **Lịch sử bug/test report cũ** | Field/tính năng này từng gây bug hay spec-gap nào chưa fix không? | Grep đúng tên field trong thư mục test-report/bug của repo spec (`stories/**/test_report/**/bugs/`, `stories/**/test_case/`) — nguồn này thường bị bỏ qua vì không phải BRD/code |

   **Bắt buộc xác minh trước khi tính là ảnh hưởng thật (áp dụng cho 2 hướng "Field/column cụ thể" và "Lịch sử bug"):** một hit từ grep theo tên field **chỉ là giả thuyết**, không phải bằng chứng — cùng tên `due_date`/`status`/`id`... hoàn toàn có thể là 2 field độc lập trên 2 entity khác nhau, trùng tên ngẫu nhiên. Phải **mở đúng struct/model/schema** chứa field đó ra đọc, xác nhận nó thuộc cùng bảng/collection (hoặc có đường ghi/đọc thật nối 2 phía — event payload, foreign key, service gọi chéo) trước khi liệt kê là ảnh hưởng chéo module. Đây là bản mở rộng của bài học DEMO-6065 ("tìm thấy code khớp từ khoá không có nghĩa code đó implement ĐÚNG feature đang hỏi") áp dụng cho field thay vì cho cả feature. Hit chưa xác minh được thì ghi `NEED_CONFIRM` kèm lý do, không tự tin liệt kê chung với hit đã xác minh.
   **"Cùng thư mục/package" KHÔNG phải bằng chứng đủ** — case thật (DEMO-7037, 2026-09-06, lặp lại 2 lần trong cùng phiên): 1 file nằm chung thư mục `services/vulns-management/` với model đang sửa bị tưởng nhầm là cùng domain, đọc kỹ mới thấy nó dùng `CmdbRepository` và truy vấn collection `cmdb.vuln_metrics_daily` — một entity hoàn toàn khác, chỉ tình cờ tổ chức code chung thư mục. Dấu hiệu xác nhận đúng phải là: **tên struct/repository triển khai** và **tên collection/table/index nó thực sự truy vấn trong câu query** — không phải tên file, tên thư mục, hay tên package.
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

## Bổ sung 2026-09-07 — Recall kiến thức local về module/US (bắt buộc, TRƯỚC khi design)

Trước khi thiết kế testcase cho một US, PHẢI kéo lại kiến thức đã tích luỹ ở workspace local — nếu bỏ, sẽ lặp lại lỗi cũ hoặc dùng expected SAI với hành vi mà phiên/US trước đã chốt. Đọc theo thứ tự:

1. **Defect đã có của module/US** — mở `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md`, lọc theo module chính + US gốc. Với finding khớp: đọc `manifest.yaml` các phần `fingerprint`, `expected`, `regression`, `retest`. Bug OPEN/chưa retest trên cùng behavior → thiết kế testcase để né/relate, KHÔNG báo PASS đè lên.
2. **Testcase sẵn có của module** — `Modules/<module>/TC/*`. US mới chạm module cũ thì SỬA/BỔ SUNG file sẵn có (testcase là tài sản module), không tạo file mới theo mã US.
3. **Domain-Rules của module** — `Knowledge-Base/Domain-Rules/<module>/_overview.md` (invariant, cross-screen effect, **quyết định expected đã chốt**) + file rule `.yaml` liên quan. Chỉ dùng `APPROVED` làm oracle PASS/FAIL (`governance/knowledge-policy.yaml`); DRAFT chỉ để thiết kế.
4. **Quyết định ràng buộc expected từ US/phiên trước** — nếu behavior này từng được chốt khác BRD (vd "chỉ áp file mới, không backfill"; quyền thực hẹp hơn tên role) → dùng quyết định đã chốt, ghi rõ nguồn.

**Output thêm:** một "Recall summary" ngắn — invariant đã biết · defect liên quan (trạng thái) · quyết định ràng buộc expected · US regression-linked. Không có thì ghi rõ "đã tra INDEX/Domain-Rules, không có", đừng bỏ qua im lặng.
