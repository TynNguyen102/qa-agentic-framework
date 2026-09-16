# QA Agentic Workflow — Gap Analysis

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Phạm vi:** toàn bộ repo control-plane (Core + `Projects/Example-Project/` làm project tham chiếu)
> **Phương pháp:** đọc file thật trong repo; mỗi kết luận đều dẫn file chứng minh.
> **Không tuyên bố coverage 100%** — đây là đánh giá theo 38 capability trong brief, không phải audit chứng nhận.

## 0. Cách đọc bảng

| Status | Nghĩa |
|---|---|
| `ĐÃ CÓ` | Có artifact thật, đã nối router, dùng được ngay |
| `MỘT PHẦN` | Có nhưng thiếu mảng con quan trọng |
| `CHƯA CÓ` | Không tìm thấy artifact nào trong repo |
| `CHƯA NỐI ROUTER` | Artifact tồn tại nhưng `qa-router/SKILL.md` không route tới |
| `STALE` | Có artifact nhưng đã lỗi thời so với thứ nó bảo vệ |

Risk = thiệt hại nếu gap gây lỗi lọt. Priority: P0 (chặn dùng rộng) / P1 (hiệu quả) / P2 (tối ưu).

## 1. Ma trận capability

| # | Capability | Existing Skill/File | Status | Gap | Risk | Prio | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | Requirement analysis | `.agents/skills/01-review-requirements/SKILL.md` + `REFERENCE.md` | ĐÃ CÓ | Output chưa chuẩn hoá theo schema máy đọc | Trung bình | P0 | Thêm `schemas/requirement-intake.schema.yaml`, giữ nguyên skill 01 |
| 2 | Document ingestion | `Knowledge-Base/{Confluence,GitLab}-Mirror/`, `API-Specs/`, `knowledge-policy.yaml` | MỘT PHẦN | Chưa có intake chuẩn cho MR / source diff / release note / DB schema | Cao | P0 | Bổ sung `intake_types` vào schema intake |
| 3 | Conflict detection | rải rác: `qa-router` gates, `knowledge-policy.yaml` `conflict_policy`, skill `06`/`09`/`14`/`30` | MỘT PHẦN — CHƯA CÓ SKILL RIÊNG | Không có skill chuyên trách; không có Conflict ID / severity / blocking schema | **Cao** | **P0** | Skill `42-document-conflict-analysis` + `conflict-report.schema.yaml` |
| 4 | Domain knowledge | `Knowledge-Base/Domain-Rules/<module>/{_overview,_db-reference}.md` + `knowledge-policy.yaml` | ĐÃ CÓ | — metadata đã đủ theo brief §IV | Thấp | — | Giữ nguyên |
| 5 | Risk analysis | skill `01`/`04` có mục risk; `professional-coverage-model.yaml` | MỘT PHẦN — CHƯA CÓ SKILL RIÊNG | Không có change-impact map (component → dependency → consumer → DB → event → role); risk score không có công thức | **Cao** | **P0** | Skill `43-risk-and-change-impact` |
| 6 | Test-type recommendation | `qa-router/SKILL.md` mục "Typical chains" | MỘT PHẦN | Router tự chọn nhưng không trả checklist cho người dùng tick; người mới không thấy lựa chọn | Trung bình | **P0** | Skill `44-test-advisor` |
| 7 | Test planning | `02-sprint-test-plan`, `03-feature-test-plan`, `master-test-plan` | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 8 | Test-case generation | `05`,`06`,`07`,`08` + `Config/QA-Agent/canonical-testcase-schema.yaml` | ĐÃ CÓ | Schema thiếu `risk_id`, `execution_mode` (brief §XI, §XXV) | Trung bình | P1 | Thêm 2 trường optional (backward-compatible) |
| 9 | Coverage analysis | `24-test-coverage-audit` + `professional-coverage-model.yaml` + `api-coverage-profile.yaml` | ĐÃ CÓ | Thiếu enum trạng thái `NOT_APPLICABLE` / `BLOCKED` chuẩn hoá | Thấp | P1 | Bổ sung enum |
| 10 | Test-data generation | `10-generate-test-data` + `Projects/<P>/Config/test-data-readiness.yaml` | ĐÃ CÓ | Chưa có seed tái lập cho regression (brief §XVIII) | Trung bình | P1 | Bổ sung mục seed/cleanup |
| 11 | UI testing | `21-ui-ux-testing`, `28-frontend-e2e-testing`, `Config/QA-Agent/ui-pattern-checklists/` | ĐÃ CÓ | Visual regression chưa tách rõ khỏi functional UI | Trung bình | P1 | Tách 4 chế độ trong skill 21 |
| 12 | UX review | `16-usability-testing` | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 13 | API testing | `08`,`14`,`22` + `api-coverage-profile.yaml` | ĐÃ CÓ | — bao phủ OWASP API + contract | Thấp | — | Giữ nguyên |
| 14 | Database testing | `34-database-testing`, `38-query-data-by-assurance-level` + `_db-reference.md` | ĐÃ CÓ | — `assurance-levels.yaml` đã chặn write | Thấp | — | Giữ nguyên |
| 15 | Security testing | `23-security-testing` + `standards-profile.yaml` (ASVS 5.0 L2, API Top10 2023, WSTG 4.2) | ĐÃ CÓ | Prompt-injection / data-leakage nằm ở skill `40`, chưa cross-link từ `23` | Trung bình | P1 | Cross-link `23` ↔ `40` |
| 16 | Performance & reliability | `25`,`17`,`20`,`27` | ĐÃ CÓ | — `assurance-levels.yaml` L4 yêu cầu môi trường riêng + approval | Thấp | — | Giữ nguyên |
| 17 | Accessibility | `07`, `19` (WCAG 2.2 AA) | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 18 | AI/LLM testing | `40-ai-output-testing` + `standards-profile.yaml` mục `ai_testing` | ĐÃ CÓ — **STANDARD CHƯA CHỐT** | 3 standard (29119-11, 25059, ISTQB CT-AI) còn `PROPOSED_2026-09-07` | Trung bình | P1 | `NEED_CONFIG`, xin Lead chốt edition |
| 19 | Integration testing | rải trong `14`,`22`,`35` | MỘT PHẦN | Không có mục riêng cho consumer-provider boundary ngoài `22` | Trung bình | P1 | Ghi rõ trong Target Architecture, chưa cần skill mới |
| 20 | End-to-end testing | `28-frontend-e2e-testing`, `15-functional-happy-path-testing` | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 21 | Deep testing | `26-deep-coverage-testing` | ĐÃ CÓ | Chưa có luật khi nào chạy song song vs sau baseline (brief §XIX) | Trung bình | P1 | Đưa vào `router-policy.yaml` mục `parallelization` |
| 22 | Exploratory testing | `18-exploratory-testing` | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 23 | Bug hunting | `30-business-logic-bug-hunt` + `Projects/<P>/Config/bug-basis-profile.yaml` | ĐÃ CÓ | — đã có 12 `bug_hunting_dimensions` | Thấp | — | Giữ nguyên |
| 24 | Test execution | `13-execute-approved-testcases` | MỘT PHẦN | Chưa chuẩn hoá 8 trạng thái brief §XX (thiếu `INCONCLUSIVE`, `ENVIRONMENT_ERROR`, `AUTOMATION_ERROR` dạng enum); chưa có luật phân biệt product / script / env failure ở tầng schema | **Cao** | **P0** | `test-result.schema.yaml` |
| 25 | Evidence management | `Modules/<m>/Sprint-N/Evidence/`, redaction rule ở `knowledge-policy.yaml` | MỘT PHẦN | Không có schema evidence (loại, path, redaction status, checksum) | **Cao** | **P0** | `evidence.schema.yaml` |
| 26 | Defect validation | `39-issue-triage` + `bug-basis-profile.yaml` + `.claude/hooks/pre_jira_write_gate.py` | ĐÃ CÓ — THIẾU NGƯỠNG | Có 7 confirmation gate + hook cưỡng chế, nhưng không có defect confidence threshold để quyết log hay chờ human | **Cao** | **P0** | `DEFECT_VERIFICATION_POLICY.md` |
| 27 | Jira logging | `36-log-jira-defect` + `Projects/<P>/Config/defect-profile.yaml` | ĐÃ CÓ | — có `jira_rich_format_2026_09_15`, Relates→Story rule, hook gate | Thấp | — | Giữ nguyên |
| 28 | Automation generation | `11`, `12`, `Config/robot-framework-profile.yaml`, `automation-structure.yaml` | ĐÃ CÓ — **GẮN CỨNG TOOL** | Chỉ `06` nhắc chữ "adapter"; Robot/Playwright/k6 gắn cứng theo profile, chưa có adapter contract chung | **Cao** | P1 | `Config/QA-Agent/tool-adapters.yaml` |
| 29 | Regression selection | `32-smoke-regression-testing` | ĐÃ CÓ | Tiêu chí smoke/regression chưa ở dạng máy đọc | Trung bình | P1 | Bổ sung vào `router-policy.yaml` |
| 30 | CI/CD integration | `.gitlab-ci.yml`, `.github/workflows/qa-workspace-validation.yml`, `Automation/Robot-Framework/.gitlab-ci.yml` | MỘT PHẦN | GitLab CI chỉ chạy Robot **dryrun** với `allow_failure: true`; chưa có stage smoke/regression theo impact; chưa publish result về Jira/TestRail | Trung bình | P1 | Mở rộng theo roadmap; giữ `allow_failure` tới khi runner sẵn sàng |
| 31 | Multi-agent orchestration | — | **CHƯA CÓ** | Không có orchestrator, shared-context contract, merge/dedup output. `.agents/skills/*/agents/openai.yaml` chỉ là interface metadata, **không phải** multi-agent | **Cao** | **P0** | `execution-plan.schema.yaml` + mục orchestration trong `router-policy.yaml`, bắt buộc fallback sequential |
| 32 | Token/cost optimization | — | **CHƯA CÓ** | Không có progressive-disclosure rule; không đo token/tool-call theo task | Trung bình | P1 | `TOKEN_COST_OPTIMIZATION.md` |
| 33 | Beginner guidance | `README.md`, `.claude/hooks/prompt_skill_nudge.py` | MỘT PHẦN | Hook chỉ gợi ý tên skill; không có wizard/checklist chọn phạm vi test | Trung bình | **P0** | Skill `44-test-advisor` |
| 34 | Human review gates | rải trong `qa-router` "Mandatory gates" + từng skill + hook | MỘT PHẦN — CHƯA GOM | Gate đúng và đang chạy nhưng nằm rải rác; không có nguồn liệt kê đủ 8 gate brief §XXVII | **Cao** | **P0** | `HUMAN_APPROVAL_GATES.md` (tổng hợp, không phát minh gate mới) |
| 35 | Quality evaluation | `evals/qa-agent/eval-suite.yaml` (11 ZT + 22 P0, baseline `2026-07-19`) | **STALE** | Baseline chạy 2026-07-19; router/config đã đổi nhiều lần mà chưa chạy lại — chính file tự ghi "nên chạy lại mỗi khi router/config đổi lớn". Chưa có case cho conflict / risk / advisor / orchestration | **Cao** | **P0** | ✅ **ĐÃ ĐÓNG 2026-09-16** — thêm 20 case mới (CF/RK/TA/OR/EX), chạy 53/53, baseline `CURRENT_20260916` |
| 36 | Learning & feedback loop | `Config/QA-Agent/learning-profile.yaml` | MỘT PHẦN | Có **nguyên tắc** ("không tự học từ mọi output") nhưng **không có cơ chế**: không có feedback record schema, không có đường feedback → eval case | Trung bình | P1 | `LEARNING_FEEDBACK_POLICY.md` |
| 37 | Git governance | `Config/QA-Agent/git-collaboration.yaml`, `CODEOWNERS`, `CONTRIBUTING.md` | ĐÃ CÓ | — | Thấp | — | Giữ nguyên |
| 38 | Traceability & audit | `governance/audit-policy.yaml`, `Projects/<P>/governance/audit-events/`, `Knowledge-Base/Traceability/` | ĐÃ CÓ — **POLICY LỆCH THỰC TẾ** | `audit-policy.yaml` `required_fields` yêu cầu `event_id` + `skill` nhưng event tháng 09/2026 **không có 2 trường này** | Trung bình | **P0** | Chốt lại policy hoặc bổ sung trường; không im lặng bỏ qua |

## 2. Tổng hợp theo trạng thái

| Status | Số | Capability |
|---|---:|---|
| ĐÃ CÓ | 20 | 1, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 27, 37 + 26 (thiếu ngưỡng) |
| MỘT PHẦN | 12 | 2, 3, 5, 6, 19, 24, 25, 29, 30, 33, 34, 36 |
| ĐÃ CÓ nhưng rủi ro | 3 | 18 (standard chưa chốt), 28 (gắn cứng tool), 38 (policy lệch) |
| **CHƯA CÓ** | **2** | **31 multi-agent orchestration**, **32 token optimization** |
| **STALE** | **0** | ~~35 eval-suite~~ — đã chạy lại 16/09, baseline `CURRENT_20260916` |

## 3. Capability ĐÃ CÓ nhưng CHƯA ĐƯỢC NỐI

Nhóm brief hỏi riêng — thứ đã tồn tại nhưng router hoặc người dùng không thấy:

| Artifact | Nằm ở | Vì sao bị bỏ sót |
|---|---|---|
| `bug-basis-profile.yaml` (7 confirmation gate + 12 bug dimension) | `Projects/<P>/Config/` | `qa-router/SKILL.md` **không nhắc tên file này**; chỉ skill 30/39 dùng |
| `assurance-levels.yaml` (L0–L4 chặn write/destructive) | `Config/QA-Agent/` | Router không liệt kê trong mandatory gates; chỉ skill 38 dùng |
| `.claude/hooks/pre_jira_write_gate.py` | `.claude/hooks/` | Cưỡng chế 6 cổng trước khi raise bug nhưng **không được tài liệu hoá** ở `governance/` |
| `evals/qa-agent/eval-suite.yaml` | `evals/` | Không skill nào trỏ tới; **không chạy trong CI** |
| `ui-pattern-checklists/` | `Config/QA-Agent/` | Chỉ skill 21 biết |
| `learning-profile.yaml` | `Config/QA-Agent/` | Được `knowledge-policy` nhắc nhưng không workflow nào tiêu thụ |

## 4. Capability đang có nhưng CHƯA ĐỦ AN TOÀN

| Vấn đề | Bằng chứng | Rủi ro |
|---|---|---|
| Eval baseline stale ~2 tháng | `eval-suite.yaml` `known_limitations` tự ghi "nên chạy lại mỗi khi router/config đổi lớn" | Gate zero-tolerance có thể đã regress mà không ai biết |
| `audit-policy` lệch thực tế | policy yêu cầu `event_id` + `skill`; event 09/2026 không có | Audit không parse được bằng automation |
| Standard AI chưa chốt | `standards-profile.yaml` `ai_testing` = `PROPOSED_2026-09-07` | Skill 40 đang test AI mà chuẩn chưa được duyệt |
| Standard xác nhận cho project đã không còn | chính file ghi "confirmed for a project that no longer exists in this workspace" | Toàn bộ standard đang áp cho Example **chưa được re-confirm** |
| CI `allow_failure: true` | `.gitlab-ci.yml` | Pipeline xanh **không** chứng minh test pass |

## 5. Xác nhận âm tính

Đã grep toàn repo (trừ `node_modules`, `.git`): **không tìm thấy** `advisor`, `orchestrat*`, `change impact`, `token budget`, `progressive disclosure`, `execution_plan`, `router-policy`. Chỉ `06-generate-functional-testcases` có chữ "adapter".

## 5b. Trạng thái các gap sau phiên 2026-09-16 (cập nhật, đọc mục này trước mục 1)

Bảng ở mục 1 là ảnh chụp **lúc audit**. Sau phiên 16/09, các gap sau đã được xử lý:

| Gap # | Nội dung | Trạng thái mới | Bằng chứng |
|---|---|---|---|
| 3 | Conflict detection | ✅ Có skill `42` + schema + đã chạy thật ra 3 conflict | [Conflicts/](../Projects/Example-Project/Knowledge-Base/Conflicts/) |
| 5 | Risk & change impact | ✅ Có skill `43`, đã nối `_defect-patterns.md` | [_defect-patterns.md](../Projects/Example-Project/Knowledge-Base/Domain-Rules/_defect-patterns.md) |
| 6 · 33 | Test advisor / beginner guidance | ✅ Có skill `44` | — |
| 10 | Seed tái lập test data | ✅ Đã bổ sung vào skill `10` | — |
| 24 · 25 | Trạng thái execution + evidence schema | ✅ `test-result.schema.yaml` | — |
| 26 | Ngưỡng confidence cho defect | ✅ `DEFECT_VERIFICATION_POLICY.md` + đã nối skill `39`/`36`/`24` | — |
| 28 | Automation gắn cứng tool | ⚠️ Có `tool-adapters.yaml` + bộ dò; **8 skill vẫn còn gắn cứng** | `tools/qa_schema_check.py` |
| 30 | CI/CD | ⚠️ Đã thêm `skills-check` + `qa_schema_check`; **chưa có stage smoke/regression theo impact** | — |
| 31 | Multi-agent orchestration | ⚠️ Có contract; đã chạy 6 agent song song cho **eval**, **chưa chạy cho một US thật** | — |
| 32 | Token optimization | ⚠️ Có tài liệu + **1 điểm đo thật**; còn 4/5 chỉ số `NOT_MEASURED` | [metrics/](../Projects/Example-Project/governance/metrics/) |
| 34 | Human approval gates | ✅ `HUMAN_APPROVAL_GATES.md` G1–G9, eval chứng minh gate chặn thật | — |
| 35 | Eval stale | ⚠️ Đã thêm 18 case + chạy 6; **45 case còn lại chưa chạy** | — |
| 36 | Learning feedback loop | ⚠️ Có chính sách + thư mục; **chưa có feedback record nào** | [feedback/](../Projects/Example-Project/governance/feedback/) |
| 38 | Audit policy lệch thực tế | ✅ **Đã chốt phương án A**, cưỡng chế từ 2026-09-17, đã kiểm chứng bằng negative test | `governance/audit-policy.yaml` `resolved_divergence` |
| P0 #10 | Skill versioning | ✅ `skill-registry.yaml`, 51 skill có version | — |

**Còn lại thật sự chưa động tới:** historical defect intelligence đã làm (gap P2) — nhưng routing
metrics, human acceptance rate và skill-selection precision/recall vẫn `NOT_MEASURED` vì **cần
ground truth do Lead gán nhãn**, không tạo ra được bằng cách viết tài liệu.

## 6. Roadmap

| Phase | Nội dung | Deliverable chính |
|---|---|---|
| **P0** | Contract & an toàn trước khi dùng rộng | 5 schema, `router-policy.yaml`, 3 skill mới (42/43/44), `HUMAN_APPROVAL_GATES.md`, `DEFECT_VERIFICATION_POLICY.md`, `AI_RESULT_ASSURANCE_MODEL.md`, golden eval case, sửa lệch `audit-policy` |
| **P1** | Hiệu quả thực thi | `tool-adapters.yaml`, mở rộng CI, `LEARNING_FEEDBACK_POLICY.md`, cross-link 23↔40, seed/cleanup test data, tách 4 chế độ UI |
| **P2** | Tối ưu & học | `TOKEN_COST_OPTIMIZATION.md`, routing metrics, historical defect intelligence, confidence score vận hành |

## 7. Audit này KHÔNG khẳng định

- Không khẳng định coverage repo là 100% hay đầy đủ theo bất kỳ chứng nhận nào.
- 20 capability "ĐÃ CÓ" mới xác nhận **artifact tồn tại và được router trỏ tới** — **không** xác nhận chúng chạy đúng.
- Chỉ `python tools/qa_workspace.py validate` được chạy thật trong audit này (kết quả `OK (Example-Project)`).
- Chất lượng nội dung từng skill chưa được đánh giá lại theo eval — xem gap #35.

## 8. Tài liệu liên quan

- `governance/QA_AGENTIC_TARGET_ARCHITECTURE.md` — kiến trúc đích
- `governance/CAPABILITY_SKILL_MATRIX.md` — capability ↔ skill ↔ schema ↔ eval
- `governance/HUMAN_APPROVAL_GATES.md` — cổng phê duyệt người
- `governance/DEFECT_VERIFICATION_POLICY.md` — ngưỡng log bug
- `governance/AI_RESULT_ASSURANCE_MODEL.md` — đo chất lượng output AI
- `governance/STANDARDS_TRACEABILITY_MATRIX.md` — map chuẩn ↔ stage ↔ evidence
