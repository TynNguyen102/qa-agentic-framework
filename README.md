# Example AI Quality Platform — Enterprise QA Control Plane

> **Tài liệu kiến trúc nền tảng (platform architecture), không phải hướng dẫn sử dụng.** Chi tiết vận hành nằm ở **Appendix** cuối tài liệu.

---

## 1. Executive Summary

**Example AI Quality Platform** là một **QA Control Plane cấp tổ chức**: một nền tảng thống nhất để con người (QC) và AI cùng vận hành đảm bảo chất lượng trên **một chuẩn chung, một nguồn sự thật, một bộ governance** — có khả năng phục vụ **nhiều dự án** từ chính kiến trúc, không phải một bộ công cụ QA rời rạc.

Nền tảng đang chạy thật trên sản phẩm **Example-Project** (SOC/security — "Cyber Digital Brain"): **51 workflow chuẩn hoá**, kiến trúc **5-plane**, governance **evidence-first / APPROVED-oracle**, và một **Quality Execution Engine** (Robot Framework + CI) đưa test vào release gate. Mục tiêu chiến lược: từ *workflow được tạo ra* → *được dùng rộng* → *trở thành chuẩn QA của tổ chức, tái dùng cho nhiều sản phẩm*.

---

## 2. Business Challenges

| Thách thức | Hệ quả nếu không giải |
|---|---|
| QC làm **rải rác theo squad**, mỗi người một kiểu | Chất lượng không đồng đều, khó review/handover, khó mở rộng |
| **AI được dùng nhưng thiếu governance** | Nguy cơ kết luận sai / báo PASS giả, không truy vết được → rủi ro release |
| **Coverage & traceability thiếu** | Không chứng minh được chất lượng bằng số cho lãnh đạo |
| **KPI không đo được** (DRE, MTTR, leakage) do lỗ hổng nguồn dữ liệu | Không định lượng được hiệu quả, không thuyết phục được đầu tư |
| Regression **thủ công**, nhân lực mỏng (3 QC / ~30 module) | Không theo kịp nhịp phát triển, tải dồn cuối sprint |

---

## 3. Platform Vision

Chuyển QA từ **hoạt động thủ công, phân mảnh** sang **một nền tảng chất lượng có kiểm soát, AI-augmented, đa dự án**:

- **Chuẩn hoá** — một canonical schema + coverage model cho mọi loại test, mọi dự án.
- **AI có governance** — AI tăng năng suất nhưng mọi kết luận phải có bằng chứng + được kiểm soát.
- **Đo được** — adoption, compliance, coverage, chất lượng AI hiển thị bằng số.
- **Mở rộng** — thêm sản phẩm mới = cấu hình, không xây lại nền tảng.

---

## 4. Platform Capabilities

| Năng lực | Đã cung cấp (bằng chứng) |
|---|---|
| **Standardization** | Canonical testcase schema, 44 skill đánh số (01–44) + 7 hỗ trợ, `professional-coverage-model.yaml` (denominator `DESIGNED→REVIEWED→AUTOMATED→EXECUTED→PROVEN`), testcase/defect title profile |
| **AI Governance** | Chỉ knowledge `APPROVED` là oracle · **reporting-integrity gate** (từ chối báo PASS không bằng chứng) · **recall-gate** (bắt buộc dùng lại tri thức cũ) · audit-events bất biến |
| **Quality Execution** | **Quality Execution Engine = Robot Framework + CI** (regression gate) · Playwright (UI/E2E, chạy DEV qua mint-cookie) · AI-output & benchmark testing (skill 40/20/27) |
| **AI Quality Assurance** | AI-model map (<LLM-PROVIDER>/<RAG-ENGINE>) · ground-truth Q&A framework · chống hallucination (no-verdict-without-runtime) |
| **Scalability / Portability** | Core dùng chung + `Projects/<name>/` tách biệt + `Project-Scaffold` → thêm dự án bằng cấu hình |
| **Observability** | Metrics & Adoption Dashboard (Confluence <QC-SPACE>) + audit-events làm nguồn adoption |

---

## 5. Domain Coverage

> **Mục này để trống có chủ đích — điền theo sản phẩm của bạn.**
> Khung không đi kèm domain của bất kỳ sản phẩm nào; danh sách module là dữ liệu của project,
> khai trong `Projects/<tên-project>/Config/modules.yaml`.

Cách điền: gom module thành **4–6 nhóm domain** theo nghiệp vụ, mỗi nhóm một dòng. Nhóm nào có
feature do **model sinh output** (AI/LLM) thì tách riêng — nhóm đó không test bằng assert tất định
được, phải đi qua lớp AI-output (`40-ai-output-testing`).

```
- <Nhóm domain 1> — <module a>, <module b>, <module c>.
- <Nhóm domain 2> — <module d>, <module e>.
- <Nhóm AI-native> — <feature LLM> — output không tất định, dùng lớp AI-output riêng.
```

Sau khi điền, mô hình hoá **ảnh hưởng chéo giữa các module** (blast-radius) ở
`Projects/<tên-project>/Knowledge-Base/Domain-Rules/_cross-module-map.md`. Đây là thứ quyết định
phạm vi regression khi một module đổi — không có nó thì mọi ước lượng "sửa chỗ này ảnh hưởng chỗ
nào" đều là đoán.

---

## 6. Standards Alignment

| Nhóm | Chuẩn tham chiếu |
|---|---|
| Test process / design | ISO/IEC/IEEE **29119**, **ISTQB** |
| Quality & data model | ISO/IEC **25010**, **25012** |
| Accessibility | **WCAG 2.2 AA** |
| Security | **OWASP ASVS**, **OWASP API Security Top 10**, MASVS |
| API contract | **OpenAPI** từ live spec |
| **AI/ML quality** | **ISO/IEC 29119-11**, **ISO/IEC 25059**, **ISTQB CT-AI** (PROPOSED — thực hành đã có ở skill 40) |

Chuẩn giúp chọn risk/technique/evidence; **không thay thế** Jira/Confluence/business rule làm expected của sản phẩm. Edition/version chờ QA Lead/PO duyệt.

---

## 7. Enterprise Architecture — mô hình 5 Plane

```text
┌──────────────────────────────────────────────────────────────┐
│  CONTROL PLANE      Router (qa-router) + router-policy.yaml +  │
│                     51 skill + active-project → chọn đúng      │
│                     workflow cho đúng dự án                    │
│                     project → chọn đúng workflow cho đúng dự án│
├──────────────────────────────────────────────────────────────┤
│  KNOWLEDGE PLANE    Domain-Rules · Defects/INDEX · cross-      │
│                     module map · AI-model map · ground-truth   │
│                     → recall-gate BẮT BUỘC dùng lại            │
├──────────────────────────────────────────────────────────────┤
│  QUALITY EXECUTION  ★ Quality Execution Engine = Robot + CI    │
│  PLANE              (regression gate) · Playwright (UI/E2E)    │
│                     · AI-output/benchmark · mint-cookie auth   │
├──────────────────────────────────────────────────────────────┤
│  GOVERNANCE PLANE   APPROVED-oracle · reporting-integrity ·    │
│                     evidence-first · audit-events · CẤM PROD   │
├──────────────────────────────────────────────────────────────┤
│  MULTI-PROJECT      Core dùng chung + Projects/<name>/ tách    │
│  (PORTABILITY)      biệt + Project-Scaffold → thêm dự án       │
└──────────────────────────────────────────────────────────────┘
        Data plane thực thi: DEV (dev-app/dev-api.example.local)
                    PROD (app.example.com) — CẤM test
```

**Quality Execution Engine (Robot Framework + CI)** là *xương sống thực thi xác định* của platform: keyword-driven 4 lớp (LowLevel `*_API`/`*_UI`/`*_DB` → HighLevel → Verification), tổ chức theo module + mã Jira, regression điều khiển bằng TAG, và **đưa test vào release gate** qua GitLab CI + Jenkins (repo riêng `AUTOMATION-REPO`). Playwright đảm nhận UI/E2E; lớp AI-output đảm nhận chất lượng model.

Nguyên tắc cách ly: business truth của mỗi dự án đến từ nguồn đã xác nhận của chính dự án đó; chỉ **kiến trúc/method** (skill, schema, coverage model) được tái dùng.

---

## 8. Governance

Governance là **first-class** của platform, không phải phụ lục:

1. Chỉ knowledge **APPROVED** được dùng làm oracle PASS/FAIL (`governance/knowledge-policy.yaml`); `DRAFT`/`NEED_CONFIRM` chỉ để thiết kế.
2. **Reporting integrity** — mọi trạng thái báo ra phải kèm bằng chứng vừa quan sát + nhãn `CONFIRMED / INFERRED / ASSUMED / NOT_CHECKED`; đọc code/MR ≠ runtime; kết quả rỗng ≠ pass.
3. **Evidence-first** — không kết luận business PASS từ HTTP 200/toast/automation xanh; phải readback UI/API/DB/audit.
4. **Coverage denominator** — không claim complete/zero-bug nếu không có mẫu số + residual risk.
5. **Bất khả xâm phạm** — CẤM test PROD mọi hình thức; live-write cần duyệt trong phiên; che dữ liệu nhạy cảm; audit-events bất biến ghi mọi thao tác ghi.

### 8.0 Pre-chain bắt buộc và bộ tài liệu governance (bổ sung 2026-09-16)

Mọi US / ticket / change request mới đi qua **pre-chain bắt buộc** trước khi thiết kế testcase:

```
01 review-requirements → 42 conflict-analysis → 43 risk-and-change-impact → 44 test-advisor
                                    ↓                                            ↓
                         conflict BLOCKER ⇒ chặn (G1)              người dùng chốt phạm vi test
```

Chính sách định tuyến máy đọc: [`Config/QA-Agent/router-policy.yaml`](Config/QA-Agent/router-policy.yaml).
Contract input/output: [`Config/QA-Agent/schemas/`](Config/QA-Agent/schemas/) (6 schema — intake, conflict,
execution-plan, test-result, confidence, skill-io).

| Tài liệu | Trả lời câu hỏi |
|---|---|
| [`QA_AGENTIC_WORKFLOW_GAP_ANALYSIS.md`](governance/QA_AGENTIC_WORKFLOW_GAP_ANALYSIS.md) | 38 capability — cái gì đã có, thiếu, chưa nối |
| [`QA_AGENTIC_TARGET_ARCHITECTURE.md`](governance/QA_AGENTIC_TARGET_ARCHITECTURE.md) | Kiến trúc đích 4 tầng + vendor-neutral |
| [`CAPABILITY_SKILL_MATRIX.md`](governance/CAPABILITY_SKILL_MATRIX.md) | Capability → skill → schema → eval |
| [`HUMAN_APPROVAL_GATES.md`](governance/HUMAN_APPROVAL_GATES.md) | 9 cổng G1–G9, ai duyệt, chặn gì |
| [`DEFECT_VERIFICATION_POLICY.md`](governance/DEFECT_VERIFICATION_POLICY.md) | Khi nào được log Jira, khi nào phải chờ người |
| [`AI_RESULT_ASSURANCE_MODEL.md`](governance/AI_RESULT_ASSURANCE_MODEL.md) | Đo chất lượng output AI bằng 18 chỉ số, không bằng "đúng X%" |
| [`TEST_COVERAGE_MODEL.md`](governance/TEST_COVERAGE_MODEL.md) | 5 trạng thái coverage chuẩn hoá |
| [`STANDARDS_TRACEABILITY_MATRIX.md`](governance/STANDARDS_TRACEABILITY_MATRIX.md) | Chuẩn nào dùng ở stage nào |
| [`LEARNING_FEEDBACK_POLICY.md`](governance/LEARNING_FEEDBACK_POLICY.md) | Feedback → eval → skill, không đi tắt |
| [`TOKEN_COST_OPTIMIZATION.md`](governance/TOKEN_COST_OPTIMIZATION.md) | Tiết kiệm ở đâu, tuyệt đối không cắt ở đâu |

> **Trạng thái thật (cập nhật 2026-09-16 chiều):** 10 tài liệu trên đã ở `APPROVED` (Lead duyệt 2026-09-16 — xem dòng đầu mỗi file). Nhưng **nội dung kỹ thuật bên trong chưa được chứng minh bằng eval**, đó là hai việc khác nhau.
> Ba skill `42/43/44` **đã chạy trên 2 US thật** ([DEMO-6790](https://YOUR-SITE.atlassian.net/browse/DEMO-6790) ra 3 conflict, [DEMO-7067](https://YOUR-SITE.atlassian.net/browse/DEMO-7067) ra 8 gap).
> Bộ eval đã chạy **53/53 case** — 14/14 zero-tolerance PASS, 0 FAIL; baseline
> [`eval-suite.yaml`](evals/qa-agent/eval-suite.yaml) chuyển `STALE` → `CURRENT_20260916`.
> **Chưa đo được:** 9/18 metric trong `AI_RESULT_ASSURANCE_MODEL.md` còn `NOT_MEASURED` vì cần Lead
> gán nhãn ground truth. Eval case `EX-005` **chấm PASS nhưng cách đo có khiếm khuyết** — xem mục
> `eval_ex005_khiem_khuyet_thiet_ke` trong audit-event ngày 16/09.

### 8.0.1 Nhiều người cùng dùng — luật tránh giẫm chân (chốt 2026-09-16)

Workspace này được nhiều QC dùng chung trên các nhánh khác nhau. Ngày 16/09 phát hiện sự cố thật khi
thử merge lên `main`: **6 mã `FINDING` trùng nhau cho 6 lỗi hoàn toàn khác nhau**, do hai luồng QC
cùng tự đếm thư mục `Defects/` rồi cấp số tiếp theo mà không bên nào nhìn thấy bên kia.

| Luật | Nội dung |
|---|---|
| **Mã finding** | `FINDING-<YYYYMMDD>-<MÃ_NGƯỜI_LÀM>-<NNN>`, vd `FINDING-20260101-AAA-003`. Mã người làm phải **đăng ký trước** trong [`defect-profile.yaml`](Projects/Example-Project/Config/defect-profile.yaml) mục `local_finding_id`. Đã đăng ký: `AAA` (<QA Lead>) · `BBB` (<QC EM>) · `CCC` (<QC member>) |
| **Cách cấp mã** | `git fetch --all` rồi `python tools/defects-index.py --next-id <MÃ>`. Công cụ quét **cả nhánh remote** — đây là điểm khác biệt duy nhất có tác dụng |
| **Cấm** | Tự đếm thư mục `Defects/` rồi `+1`. Đó chính là cách đã gây ra sự cố |
| **Tương thích ngược** | 42 finding lịch sử không có mã người làm **vẫn hợp lệ**; không đổi số hàng loạt vì sẽ đứt liên kết với Jira và audit-event |
| **Trước khi merge** | Chạy `git merge-tree --write-tree origin/main HEAD` để xem trước conflict, **đừng merge thẳng** |

> ⚠️ **Giới hạn còn lại:** mã người làm **không** chặn được một người chạy hai phiên song song —
> đúng tình huống đã xảy ra 16/09. Và chưa có kiểm tự động chặn mã trùng ở tầng hook/CI.

### 8.0.2 Công cụ kiểm tra tại chỗ

| Công cụ | Làm gì | Ràng buộc an toàn |
|---|---|---|
| [`tools/tc-status.py`](tools/tc-status.py) | Trích số PASS/FAIL thật từ khối ```` ```yaml case:` ```` trong file TC | Bỏ qua `*.case-draft.md` và `_baseline-coverage.md` để bản nháp chưa review không bị tính vào coverage |
| [`tools/tc-migrate.py`](tools/tc-migrate.py) | Hỗ trợ chuyển file TC văn xuôi sang khối máy đọc được | **Không bao giờ** ghi đè file gốc; **không bao giờ** tự chế verdict — chỉ chép token đã có sẵn |
| [`tools/gen-baseline-coverage.py`](tools/gen-baseline-coverage.py) | Sinh `_baseline-coverage.md` cho từng module | Chỉ sinh phần đếm được; nhận định chất lượng để trống với nhãn `CẦN_NGƯỜI_BỔ_SUNG`. Không đè file người viết tay |
| [`tools/defects-index.py`](tools/defects-index.py) | Đối chiếu `Defects/` với `INDEX.md`; cấp mã finding mới | Chạy như hook `Stop`, chặn nếu lệch |
| [`tools/qa_schema_check.py`](tools/qa_schema_check.py) | Kiểm YAML, frontmatter skill, độ tươi của eval, trường bắt buộc của audit | Thiếu PyYAML thì báo `NOT_CHECKED`, **không** báo PASS |

> **Tồn đọng đo thật 16/09:** 17/124 file TC có khối `case:`. Trong 107 file còn lại, chỉ **43 là sổ
> ghi kết quả**; 55 là tài liệu hỗ trợ vốn không có case để ghi verdict. Con số "108 file tồn đọng"
> báo cáo trước đó là **thổi phồng** — đã đính chính.

### 8.1 Khác gì dùng AI ở nơi thường — và cách kiểm chứng

Cùng một model — khác ở **lớp bọc governance** quanh nó. Đó là toàn bộ giá trị:

| Khía cạnh | AI ở workspace thường (chat/IDE) | AI trong workflow QC này |
|---|---|---|
| Sự thật để đối chiếu | Trả lời từ trí nhớ training + cái bạn dán vào; tự tin kể cả khi sai | Chỉ **APPROVED knowledge** làm oracle; **không phán khi chưa có runtime thật** |
| Trí nhớ dự án | Quên sau mỗi phiên, dễ bịa lại | Nhớ bền (memory, CURRENT_STATE, Defects INDEX, fixtures) — không tự chế lại |
| Phương pháp | Lời khuyên chung chung | Skill mã hoá quy trình thật (US→testcase→execute→report), 6 cổng trước khi raise bug |
| Nguồn | Đoán | Đọc **live** Jira/GitLab/DEV; bằng chứng byte/readback/ảnh |
| Trách nhiệm | Không dấu vết | Audit event, draft mặc định, live-write cần duyệt, che dữ liệu nhạy cảm |
| Chống chính điểm yếu AI | Ảo & nịnh tự do | Recall-gate, kiểm trùng, mirror khớp |
| Phạm vi | Trộn lẫn | Không mượn rule dự án khác làm sự thật |

**Nói gọn:** workspace thường = trợ lý nhanh nhưng có thể **tự tin nói sai**; workflow này = AI bị **quấn trong kỷ luật kiểm thử**, buộc phải **chứng minh, nhớ đúng, để lại dấu vết** — biến "thực tập sinh thông minh hay chém" thành "kiểm thử viên phải đưa bằng chứng".

> ⚠️ **Thành thật (để kiểm chứng, không PR):** lớp bọc chỉ hiệu quả khi **được cưỡng chế**. AI vẫn có thể sai hoặc nịnh — cách bắt: đòi nó chỉ ra **đã kiểm ở đâu / đọc dòng spec nào / readback chưa**; **tin bằng chứng, không tin lời**. Recall-gate, 6 cổng, no-verdict-without-runtime, audit ở trên chính là để bắt đúng cái đó — và **người vẫn là bên ký PASS/FAIL cuối cùng**, AI chỉ soạn nháp.

### 8.2 Router — cách định tuyến một request (5 phần)

`qa-router` là bộ chọn skill. Hành vi hiện hành nằm ở `.claude/skills/qa-router/SKILL.md` (bản `.agents/` là mirror cho runtime OpenAI, giống hệt về nội dung). Phần "quyết định thế nào" được tách ra máy-đọc-được ở `Config/QA-Agent/router-policy.yaml` — **đang `status: DRAFT`**, tức mô tả router *nên* đi thế nào, chưa phải luật cưỡng chế cho tới khi Lead review.

**(1) Chọn skill bằng 14 tín hiệu, KHÔNG bằng keyword.** Trọng số cao: `ticket_type`, `domain_module`, `risk_level`, `impacted_components`, `technology_layer` (FE/BE/DB/AI), `required_outputs`, `user_selected_test_types`, `previous_defects` (Defects/INDEX), `change_impact` (MR/diff). Cấm: thấy chữ "API" là route 08; bỏ qua INDEX khi module có finding cũ; suy risk bằng cảm tính.

**(2) Pre-chain bắt buộc + cây next-skill.** US/ticket mới: `01` → `42` (conflict) → `43` (risk) → `44` (test-advisor, người dùng chốt scope) → design (`04`→`06/08`→`09`→`24`→`10`→`13`) → có FAIL thì `39`→`36`, hết đợt thì `33`. Còn conflict **BLOCKER** chưa xử → **cấm** route sang 05/06/07/08.

**(3) Fan-out / song song.** Mặc định tuần tự; chỉ cho song song khi risk cao + dimension độc lập (vd API vs UI-responsive vs DB) + build đã qua smoke + runtime hỗ trợ multi-agent; **cấm** song song ở L3/L4 destructive, còn BLOCKER, hoặc cùng ghi một test-data/env. Tối đa 3 agent.

**(4) 9 cổng người duyệt (G1–G9).** conflict · residual-risk · destructive · dữ liệu thật/PII · low-confidence-defect · sửa Core skill/policy · release-gate · override business-rule · **mọi live-write**. Cổng chặn thì dừng và hỏi, không tự duyệt.

**(5) File router phải đọc mà hay quên.** `bug-basis-profile.yaml`, `assurance-levels.yaml`, `tool-adapters.yaml`, `skill-registry.yaml`, `ui-pattern-checklists/`, `eval-suite.yaml`, và hook `pre_jira_write_gate.py` (cưỡng chế 6 cổng trước khi raise bug).

> Ghi chú đồng bộ: bộ skill tồn tại hai bản mirror `.claude/skills/` (Claude Code) và `.agents/skills/` (OpenAI, thêm thư mục `agents/` binding) — sửa một skill phải cập nhật cả hai để không lệch.

---

## 9. Roadmap

| Mốc | Mục tiêu | Kết quả đo được |
|---|---|---|
| **Tháng 1** | Ổn định workflow + **adoption người thật** | Cơ chế log adoption; compliance/coverage đo được |
| **Tháng 2** | **Dashboard & KPI live** | 8 KPI trên Power BI/Grafana; gỡ ≥1 data-gap |
| **Tháng 3** | **Regression pipeline vào CI** | Robot suite chạy gate tự động trên build |
| **Beyond** | Trở thành **chuẩn tổ chức đa dự án** | Nền tảng phục vụ dự án #2 (chứng minh ranh giới Core) |

Điều kiện tiên quyết cần tổ chức hỗ trợ: quyền truy cập (USE_COPILOT, DB/VPN), hạ tầng (PyPI mirror, mạng runner→DEV), và cam kết sửa nguồn KPI (PROD-Feedback, resolutiondate).

---

## 10. Business Value

| Năng lực | Giá trị tổ chức |
|---|---|
| Standardization | Chất lượng đồng đều, auditable, giảm chi phí onboard/handover, **portable** giữa dự án |
| AI Governance | Áp dụng AI **có kiểm soát**, không release trên PASS giả → giảm rủi ro, sẵn sàng compliance |
| Quality Execution Engine | Regression tự động trong gate → giảm chi phí test tay, tăng nhịp release |
| AI Quality Assurance | **Đo được** chất lượng feature AI → điều kiện release AI có trách nhiệm |
| Multi-project scalability | Chi phí biên của một dự án mới ≈ scaffold → **một nền tảng phục vụ cả tổ chức** |

---

## 11. Appendix — vận hành & tham chiếu

> Phần này giữ nguyên nội dung thực thi (không xoá) — dành cho QC/thành viên vận hành.

**A. Nhập môn (máy công ty):** clone ở **ổ C** (không ổ mạng); set `NODE_EXTRA_CA_CERTS`/`NODE_OPTIONS=--use-system-ca` (cert YOUR-ORG CA); login DEV tự động bằng **mint-cookie** (`tools/ui-automation/mint.mjs`, Keycloak — không SSO/MFA); secret chỉ trong `.env` (gitignored). Chi tiết: [`Team/SETUP-GUIDE.md`](Team/SETUP-GUIDE.md), [`Team/IT-REQUEST.md`](Team/IT-REQUEST.md).

**B. Dùng hằng ngày:** đầu ngày `/daily-check`; chọn skill theo **status Jira** (`Analyze`→`01`; `Developing`→`04/06/08/09/10`; `To Test`→`13/36`; bug fix→`37`); không rõ → `/qa-router`; cuối ngày `/end-of-day`. Bug: `Resolved` chưa đóng, chỉ `Closed` mới đóng.

**C. 51 skill:** 44 workflow đánh số (01–44) + 7 hỗ trợ/router (`qa-router`, `jira-test-subtasks`, `qmetry-testcase-import`, `testrail-testcase-import`, `master-test-plan`, `daily-check`, `end-of-day`). Danh mục: [`Config/QA-Agent/WORKFLOW-CATALOG.md`](Config/QA-Agent/WORKFLOW-CATALOG.md). Sửa skill ở `.agents/skills/`, sync sang `.claude/` bằng `python tools/qa_workspace.py skills-sync` (51/51 mirror).

> Đính chính 2026-09-16: bản trước ghi 48 skill và liệt kê một skill dự án `sprint-planning-review` — skill đó **không tồn tại** trong repo (đã grep toàn bộ). Con số đúng hiện tại là 51.

**D. Cấu trúc thư mục (không đổi):**
```text
qa-workflow-agentskill-main/        # Core (dùng chung)
├── .agents/skills/ .claude/skills/ Config/QA-Agent/ governance/ project/ Automation/ Templates/ Team/ tools/
└── Projects/Example-Project/        # data riêng dự án
    ├── CLAUDE.md CURRENT_STATE.md qa-config.yaml Config/(modules.yaml…)
    ├── Knowledge-Base/(Domain-Rules,GitLab-Mirror,Confluence-Mirror,TestData…)
    ├── Modules/<module>/{TC,Sprint-N/{Evidence,Reports}}  Defects/(INDEX.md)  Automation/ui  Outputs/
```

**E. Nguồn & môi trường (Example):** Jira `<KEY>` · Confluence `KE`/`kom` (PRD) + `<QC-SPACE>` (QC) · GitLab `soc-platform` (SPEC-REPO + PRODUCT-REPO) · DEV `dev-app`/`dev-api.example.local` (x-token, Keycloak) · **PROD `app.example.com` — CẤM test** · test management = **MD + `tc-status.py`**.

**F. Tài liệu tiếp:** [`CURRENT_STATE.md`](Projects/Example-Project/CURRENT_STATE.md) · [`AGENTS.md`](AGENTS.md) · [`SKILL.md`](SKILL.md) · Confluence <QC-SPACE> "QC Way of Working" (hub) · [`ADAPTING-TO-NEW-PROJECT.md`](ADAPTING-TO-NEW-PROJECT.md) (thêm dự án).

---

_Nền tảng mạnh nhất khi phối hợp con người có thẩm quyền + nguồn đã kiểm chứng của dự án + AI có guardrail + tool đúng phạm vi + evidence có truy vết. Mục tiêu: kết luận chất lượng đáng tin và biết rõ nó dựa trên bằng chứng nào._
