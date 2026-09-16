# Standards Traceability Matrix

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Cảnh báo bắt buộc đọc:** repo này **không tuyên bố chứng nhận hay tuân thủ đầy đủ** bất kỳ chuẩn
> nào dưới đây. Đây là bản map "chuẩn này được dùng làm khung ở đâu", không phải bằng chứng conformance.
> Chuẩn là **khung rủi ro và bằng chứng**; nguồn expected behavior của sản phẩm vẫn là Jira/Confluence/
> domain rule đã APPROVED (`standards-profile.yaml` `rules`).

## Tình trạng xác nhận (quan trọng)

`Config/QA-Agent/standards-profile.yaml` tự ghi: toàn bộ mục `CONFIRMED` được chốt ngày **2026-07-19**
cho **một project không còn tồn tại trong workspace này**. Nghĩa là:

| | |
|---|---|
| ✅ Editions đã được chốt một lần | bởi QA Lead, 2026-07-19 |
| ⚠️ **Chưa re-confirm cho Example-Project** | đây là điều kiện file đó tự đặt ra |
| ⚠️ 3 chuẩn AI còn `PROPOSED_2026-09-07` | chưa được dùng ngôn ngữ pass/fail chuẩn tắc |

**⇒ `NEED_CONFIG: STANDARDS_RECONFIRM_FOR_ACTIVE_PROJECT`.**

## Ma trận

| Chuẩn / thực hành | Edition | Xác nhận | Workflow stage | Skill | Output | Evidence | Evaluation | Owner |
|---|---|---|---|---|---|---|---|---|
| ISO/IEC/IEEE 29119-1/2/3 | ~2021–2022 | CONFIRMED *(dự án cũ)* | Toàn bộ quy trình test | `02`,`03`,`04`,`13`,`33` | test plan, design, report | plan/report có trong `Outputs/` | ❌ | QA Lead |
| ISTQB CTFL | v4.0 (2023) | CONFIRMED *(dự án cũ)* | Thuật ngữ, kỹ thuật thiết kế, risk-based, review | `04`,`06`,`09`,`26` | testcase + lý do kỹ thuật | testcase có ghi kỹ thuật áp dụng | P0-002 | QA Lead |
| ISO/IEC 25010:2023 | 2023 | CONFIRMED *(dự án cũ)* | Chọn đặc tính chất lượng cần test | `44`,`24` | checklist + coverage dimension | `professional-coverage-model.yaml` | P0-017 | QA Lead |
| ISO/IEC 25012:2008 | 2008 | CONFIRMED *(dự án cũ)* | Chất lượng dữ liệu | `34`,`38`,`10` | data quality checks | DB readback | ❌ | Data owner |
| OWASP ASVS | 5.0.0 L2 *(candidate)* | CONFIRMED *(level cần owner duyệt)* | Security test design | `23` | security findings | evidence đã redact | ❌ | Security owner |
| OWASP API Security Top 10 | 2023 | CONFIRMED *(dự án cũ)* | API security | `08`,`14`,`23` | map API1–API10 / operation | `N/A_WITH_REASON` khi không áp dụng | **P0-022** ✅ | Security owner |
| OWASP WSTG | v4.2 | CONFIRMED *(dự án cũ)* | Recon, authn, authz, session, input | `23` | test steps | — | ❌ | Security owner |
| OWASP MASVS | 2.x L1 | CONFIRMED *(chỉ khi có app mobile — chưa xác nhận có)* | Mobile security | `29` | — | — | ❌ | Security owner |
| WCAG | 2.2 Level AA | CONFIRMED *(dự án cũ)* | Accessibility | `07`,`19` | a11y findings | scan + manual + AT evidence | ❌ | QA Lead |
| OpenAPI Specification | theo live spec | CONFIRMED | API contract | `08`,`14`,`22` | contract test | so sánh response ↔ contract | P0-018, P0-019 | Dev Lead |
| **ISO/IEC/IEEE 29119-11** | 2020 (AI systems) | ⚠️ **PROPOSED_2026-09-07** | Test hệ thống AI, oracle problem | `40` | invariant/distributional/grounded | variance theo N | RK-004 *(chưa chạy)* | **chờ Lead** |
| **ISO/IEC 25059** | 2023 (AI quality) | ⚠️ **PROPOSED_2026-09-07** | Đặc tính chất lượng AI | `40` | — | — | ❌ | **chờ Lead** |
| **ISTQB CT-AI** | v1.0 (2021) | ⚠️ **PROPOSED_2026-09-07** | Metric ML, metamorphic, data quality | `40`,`20`,`27` | benchmark precision/recall | so ground truth | ❌ | **chờ Lead** |
| IEEE-style test documentation | — | thực hành | Traceability | `24`, `Knowledge-Base/Traceability/` | ma trận truy vết | — | ❌ | QA Lead |
| Internal domain policy | — | theo project | Mọi stage | `knowledge-policy.yaml` | rule APPROVED | audit event | ZT-002, ZT-011 | BA/PO |

## Khoảng trống rõ nhất

- **9/15 chuẩn không có eval case nào** ⇒ nếu skill regress khỏi chuẩn, không cơ chế nào phát hiện.
- 3 chuẩn AI chưa chốt trong khi `40-ai-output-testing` **đang được dùng thật** cho Copilot/Investigator.
- ASVS level (L2) mới là *candidate*, chưa có owner duyệt phạm vi requirement cho Example.
- MASVS đang liệt kê dù **chưa xác nhận** project có app mobile native hay không.

## Không được làm

- Không viết "tuân thủ OWASP/ISO/WCAG" trong bất kỳ báo cáo nào gửi ra ngoài.
- Không dùng ngôn ngữ pass/fail chuẩn tắc cho chuẩn còn `PROPOSED`.
- Không coi chuẩn là nguồn expected behavior thay cho AC/business rule.
- Không tự nâng `PROPOSED` lên `CONFIRMED` — cần cổng **G6**.
