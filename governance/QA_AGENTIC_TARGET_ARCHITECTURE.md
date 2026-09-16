# QA Agentic Workflow — Target Architecture

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> Mô tả kiến trúc đích. Phần **đã có** ghi rõ là đã có; phần **chưa có** ghi rõ là chưa — tài liệu
> này không mô tả một hệ thống tưởng tượng.

## 1. Bốn tầng

```
┌─ TẦNG 1: INTAKE ────────────────────────────────────────────────┐
│ Jira · Confluence · OpenAPI · GitLab MR/diff · DB schema ·      │
│ UI design · business rule · policy · release note               │
│        ↓ chuẩn hoá thành requirement-intake.schema.yaml         │
└─────────────────────────────────────────────────────────────────┘
┌─ TẦNG 2: ANALYSIS (pre-chain bắt buộc) ─────────────────────────┐
│ 01 review → 42 conflict → 43 risk/impact → 44 test advisor      │
│        ↓ execution-plan.schema.yaml + người dùng chốt phạm vi   │
└─────────────────────────────────────────────────────────────────┘
┌─ TẦNG 3: EXECUTION ─────────────────────────────────────────────┐
│ design (04-08) → review (09/24) → data (10) → run (13,14,19,    │
│ 21,23,25,28,32,34,40,41) → evidence                             │
│        ↓ test-result.schema.yaml                                │
└─────────────────────────────────────────────────────────────────┘
┌─ TẦNG 4: VERIFY & LEARN ────────────────────────────────────────┐
│ 39 triage → 36 log Jira → 37 retest → 33 report                 │
│ → confidence-report → audit event → feedback (đã review) → eval │
└─────────────────────────────────────────────────────────────────┘
```

**Xuyên suốt 4 tầng:** `governance/knowledge-policy.yaml` (cái gì được làm oracle),
`HUMAN_APPROVAL_GATES.md` (G1–G9), `audit-policy.yaml` (ghi lại mọi thứ).

## 2. Knowledge Center

Đã có, nằm ở `Projects/<ACTIVE_PROJECT>/Knowledge-Base/`:

| Thư mục | Nội dung |
|---|---|
| `Domain-Rules/<module>/` | rule nguyên tử + `_overview.md` (cross-screen) + `_db-reference.md` (data layer) |
| `API-Specs/` | OpenAPI đã cache, có `pulled_at` |
| `Confluence-Mirror/`, `GitLab-Mirror/` | tài liệu BA/spec đã mirror |
| `DB/` | schema, lineage |
| `TestData/` | catalog dữ liệu test |
| `Traceability/` | map requirement ↔ testcase ↔ defect |
| `QA-Checklists/`, `QC-Framework-Ref/` | checklist tái dùng |
| **`Conflicts/`** *(mới)* | conflict record từ skill `42` |

**Metadata mỗi knowledge item** (đã định nghĩa ở `knowledge-policy.yaml` `required_rule_fields`):
id, title, statement, module, status, scope, sources, source version/updated_at, verified_at,
owner, applies_to, supersedes, keywords. Vòng đời: `DRAFT → NEED_CONFIRM → APPROVED → SUPERSEDED/REJECTED`.
**Chỉ `APPROVED` được dùng làm oracle PASS/FAIL.**

**Truy xuất tiết kiệm token:** chỉ nạp rule liên quan module/role/layer/task hiện tại
(`knowledge-policy.yaml` `retrieve`). Không dán nguyên tài liệu vào prompt.

## 3. Điều phối

`qa-router` + `Config/QA-Agent/router-policy.yaml` sinh ra một **Execution Plan**
(`schemas/execution-plan.schema.yaml`) trước khi chạy bất cứ gì.

**Mặc định là SEQUENTIAL.** Song song chỉ khi: risk HIGH/VERY_HIGH, các dimension độc lập, build đã
qua smoke, và runtime thực sự hỗ trợ multi-agent. Runtime không hỗ trợ ⇒ tự hạ về tuần tự và ghi lý do.

**Không bao giờ song song:** bước assurance L3/L4, khi còn conflict `BLOCKER`, khi các bước ghi vào
cùng một tập dữ liệu/môi trường.

**Shared context** là bản chuẩn hoá rút gọn — mỗi bước chỉ nhận field nó khai trong `inputs`,
không nhận toàn bộ.

**Merge output:** theo schema của loại output; phát hiện trùng theo (requirement_id + điều kiện +
data class) chứ không theo title; hai bước kết luận trái nhau ⇒ sinh conflict record, không tự chọn.
Review Agent (`09` hoặc `24`) chạy sau cùng trên output đã merge.

### Vai trò agent (khi runtime hỗ trợ)

Requirement · Domain · Risk · Conflict · UI/UX · API · Database · Security · Performance ·
AI Evaluation · Test Data · Automation · Execution · Defect Verification · Coverage Review.

Mỗi vai trò ánh xạ về skill đã có, **không** phải tiến trình riêng: ví dụ "API Agent" = chạy `08`/`14`.
Đây là cách chia việc, không phải yêu cầu hạ tầng mới.

## 4. Vendor-neutral

`schemas/skill-io.schema.yaml` quy định: skill khai **capability cần có**, không hard-code tên tool.

| Adapter | Hiện trạng |
|---|---|
| Model adapter | ✅ ngầm — core không phụ thuộc vendor; fallback sequential đã định nghĩa |
| Jira adapter | ✅ MCP Atlassian hoặc REST |
| Git adapter | ✅ GitLab REST (GitHub qua cùng contract) |
| CI adapter | ✅ `.gitlab-ci.yml` + `.github/workflows/` |
| Test management adapter | ✅ QMetry / TestRail chọn theo `qa-config.yaml` |
| **Tool adapter (test runner)** | ❌ **chưa có** — Robot/Playwright/k6 còn gắn cứng. P1: `Config/QA-Agent/tool-adapters.yaml` |

## 5. Manual / Automated / Hybrid

`test-result.schema.yaml` `execution_mode` — bắt buộc ghi ở mọi kết quả:

| Mode | Nghĩa |
|---|---|
| `MANUAL` | Người thực hiện và tự đánh giá |
| `AUTOMATED` | Script/tool chạy, assertion tự động |
| `AI_ASSISTED_MANUAL` | AI phân tích/sinh test, **người** thực thi hoặc review |
| `AGENTIC_AUTOMATED` | Agent tự lập kế hoạch, chọn tool, chạy, tổng hợp — trong giới hạn governance |
| `HYBRID` | Kết hợp agent + automation + phê duyệt người |

**Luật:** AI sinh testcase **không** làm cho test đó thành `AUTOMATED`. Sinh ≠ thực thi.

## 6. Ranh giới — kiến trúc này KHÔNG làm gì

- Không tự học từ output chưa review (`learning-profile.yaml`).
- Không tự sửa Core skill/policy — cần cổng **G6**.
- Không tự ghi live Jira/Confluence/Git/môi trường — cần **G9** trong phiên hiện tại.
- Không test PROD (`TEST_POLICY: FORBIDDEN`).
- Không tuyên bố coverage 100% hay zero-bug.
- Không dùng rule/data/env của project khác làm expected cho project đang active.

## 7. Trạng thái triển khai

| Thành phần | Trạng thái |
|---|---|
| Tầng 1 Intake | ⚠️ schema đã có, parse Swagger/MR tự động **chưa có** |
| Tầng 2 Analysis | ✅ đủ `01`→`42`→`43`→`44`, đã nối router |
| Tầng 3 Execution | ✅ skill đầy đủ; schema kết quả mới thêm, **chưa được skill cũ áp dụng** |
| Tầng 4 Verify & Learn | ⚠️ triage/log/retest/report đã có; feedback→eval **chưa có cơ chế** |
| Orchestration | ⚠️ contract đã có, **chưa chạy thật lần nào** |
| Evaluation | 🕐 baseline stale, 18 case mới chưa chạy |
