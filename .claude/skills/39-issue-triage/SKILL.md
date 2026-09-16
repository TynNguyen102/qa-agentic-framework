---
name: 39-issue-triage
description: Triage incoming bug reports, Jira issues, support reports, errors, and monitoring alerts by validating context, redacting secrets, searching for duplicates and regressions, reviewing fix history, assessing impact, and routing the issue to investigation, defect logging, requirement clarification, or no action. Use before creating or updating a Jira defect when an issue has not yet been professionally screened.
---

# Issue Triage

Đọc trước:

- `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml`
- `governance/knowledge-policy.yaml`
- `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml`
- `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml`

Chọn role mode `defect_retest_manager`. Chỉ dùng rule `APPROVED` làm expected. Triage là bước sàng lọc, không tự xác nhận bug và không tự ghi Jira.

## Input gate

Thu thập dữ liệu hiện có, không bịa phần thiếu:

- nguồn báo cáo hoặc Jira key;
- môi trường, build/version, thời điểm, role/tenant;
- hành động người dùng, trạng thái và dữ liệu đầu vào;
- expected cùng Rule ID/nguồn của dự án đang active;
- actual, error signature, component, API operation/journey;
- bằng chứng và ảnh hưởng quan sát được.

Thiếu dữ liệu trọng yếu thì dùng `INSUFFICIENT_CONTEXT` hoặc `NEED_CONFIRM`; không suy đoán.

## Quy trình

1. **Làm sạch trước khi xử lý.** Xóa hoặc thay thế password, token, cookie, API key, private key, curl chứa credential và PII không cần thiết bằng placeholder. Không đưa secret vào từ khóa tìm kiếm, output, comment hoặc file.
2. **Tạo issue fingerprint.** Tách business invariant, component, operation/journey, symptom/error signature, precondition/state/role/data, environment/build và readback impact. Giữ observation tách biệt với interpretation.
3. **Kiểm tra validity.** Áp dụng các confirmation gate trong `bug-basis-profile.yaml`; triage chỉ đưa ra candidate classification. Không nâng thẳng thành `CONFIRMED_DEFECT` nếu chưa qua workflow xác minh phù hợp.
4. **Tìm Jira theo nhiều lát cắt khi connector khả dụng.** Tìm cả issue đang mở và đã giải quyết trong project cấu hình, tối thiểu theo: exact error signature; component + operation; business invariant + symptom; hành động người dùng + readback impact. Không coi một truy vấn đơn lẻ là đủ.
5. **Đọc candidate mạnh.** Mở description, comments, links, fix version/build, resolution và evidence của candidate liên quan; không chỉ so summary.
6. **So sánh có trọng số.** Chấm tối đa 100: business invariant 25; component 10; operation/journey 15; symptom/error 15; precondition/state/role/data 15; readback impact 10; root cause/fix history 10. Ghi rõ điểm giống và khác. Cùng triệu chứng không đồng nghĩa cùng root cause.
7. **Phân loại duplicate dimension** bằng đúng một verdict:
   - `HIGH_CONFIDENCE_DUPLICATE`: 90–100 và không có khác biệt trọng yếu;
   - `LIKELY_DUPLICATE`: 70–89, cần người phụ trách xác nhận;
   - `RELATED`: 40–69 hoặc cùng khu vực nhưng khác invariant/root cause;
   - `POSSIBLE_REGRESSION`: hành vi tương đương issue đã resolved/fixed xuất hiện lại trên build mới;
   - `NEW_ISSUE`: dưới 40 sau khi đã tìm kiếm đủ phạm vi;
   - `INSUFFICIENT_CONTEXT`: thiếu fingerprint hoặc evidence để so sánh;
   - `SEARCH_BLOCKED`: connector/quyền/truy vấn không cho phép kiểm tra.
8. **Đánh giá impact.** Mô tả ảnh hưởng business/user/data/security/operation và phạm vi. Chỉ gán severity/priority khi mapping trong `defect-profile.yaml` đã được cấu hình; nếu chưa, trả `NEED_CONFIG: SEVERITY_PRIORITY_SCALE` và không tự sáng tạo thang điểm.
9. **Đề xuất route.** Dùng `30-business-logic-bug-hunt` khi cần xác minh invariant/reproduction; `36-log-jira-defect` khi đủ cơ sở và là new/regression; `01-review-requirements` khi expected mơ hồ/xung đột; `37-retest-jira-defect` khi cần kiểm chứng fix đã giao; hoặc `NO_QA_ACTION` khi có bằng chứng đây là expected/environment/automation issue.
10. **Lưu finding cần theo dõi.** Tạo/cập nhật manifest đã làm sạch tại `Projects/<ACTIVE_PROJECT>/Defects/<local_id>/manifest.yaml`, ghi `found_in_sprint`, fingerprint, triage verdict, Jira candidate keys và traceability. Dùng `DRAFT`/`TRIAGED`; không gọi manifest là Jira defect.
11. **Dừng tại approval gate.** Mặc định chỉ trả kết quả và draft. Comment, link, create, edit hoặc transition Jira đều cần anh phê duyệt rõ ràng trong phiên hiện tại. Sau thao tác được duyệt, đọc lại Jira để xác nhận kết quả và báo partial failure.

Nếu Jira search bị lỗi hoặc thiếu quyền, phải dùng `SEARCH_BLOCKED`; tuyệt đối không kết luận “không có duplicate”.

## Hành động sau phê duyệt

- Duplicate: soạn comment đã làm sạch, dẫn issue nguồn và nêu bằng chứng tương đồng; chỉ ghi lên candidate được chọn sau phê duyệt.
- Regression: tạo defect mới qua workflow 36 và liên kết issue cũ/fix history; không âm thầm reopen issue cũ.
- New issue: chuyển workflow 36; format tiêu đề chưa cấu hình vẫn chặn live create.
- Related/insufficient context: thu thập thêm evidence hoặc điều tra bằng workflow 30 trước khi log.

## Output contract

Trả: nguồn; fingerprint đã làm sạch; phạm vi/câu truy vấn đã dùng; bảng candidate; điểm tương đồng và khác biệt; validity candidate; duplicate verdict và confidence; fix history; impact; severity/priority hoặc `NEED_CONFIG`; route đề xuất; hành động cần phê duyệt. Tách rõ `fact`, `inference` và `unknown`.

## Confidence report (bổ sung 2026-09-16)

Output của skill này phải kèm một confidence report theo
`Config/QA-Agent/schemas/confidence-report.schema.yaml` — 8 thành phần, mỗi thành phần 0–3, kèm
**một dòng lý do cho từng thành phần**: source quality · requirement completeness · traceability ·
coverage · execution evidence · reproducibility · review status · conflict status.

**Cách báo cáo:** luôn hiện `band` + `limiting_factors` + `required_actions`. **Không bao giờ** chỉ
hiện con số tổng, và không gọi nó là "độ chính xác của AI".

**Luật cứng:**

| Điều kiện | Hệ quả |
|---|---|
| Bất kỳ thành phần nào = 0 | band tối đa là `LOW`, bất kể tổng điểm |
| `conflict_status` = 0 (có conflict `BLOCKER` mở) | band `UNUSABLE` — không publish ra ngoài |
| `execution_evidence` ≤ 1 | **Không** được phát biểu verdict PASS/FAIL, chỉ được nói `INFERRED` |
| Muốn nâng band | Phải có **bằng chứng mới**, không phải đánh giá lại. Agent không tự nâng band |

Xem thêm `governance/AI_RESULT_ASSURANCE_MODEL.md`.
