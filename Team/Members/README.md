# Team/Members — profile từng người

Mỗi QC có 1 file `<alias>.yaml`, copy từ `Templates/member-profile.yaml`.

**Mục đích:** ghi rõ phạm vi quyền (được write vào tool nào, môi trường nào) và mức năng lực có
evidence — để phân task đúng người và không ai vô tình làm quá quyền.

## Tạo profile

```powershell
Copy-Item Templates\member-profile.yaml Team\Members\<alias>.yaml
```

## Quy tắc

- `member_alias`: alias không chứa thông tin cá nhân nhạy cảm (không email, không số điện thoại).
- `project_scopes`: `["Example-Project"]`.
- `role_modes`: chọn từ `Projects/Example-Project/Config/agent-profile.yaml` → `role_modes`
  (`requirement_analyst`, `test_designer`, `test_executor`, `defect_retest_manager`…).
- **Không tự nâng `current_level` / `readiness`** — Lead quyết định dựa trên evidence thật
  (audit event + output đã review). Quy tắc: `promotion_policy` trong `agent-profile.yaml`.
- `authorization.tools_write`: chỉ ghi tool mà người đó **thật sự** được duyệt write (Jira comment,
  Jira issue, TestRail import…), không ghi sẵn cho tương lai.

## Mức năng lực

| Level | Nghĩa |
|---|---|
| L0 | Chưa cấu hình / chưa có nguồn |
| L1 | Hiểu khái niệm, nguồn và giới hạn |
| L2 | Thiết kế được output đúng cấu trúc và truy vết |
| L3 | Thực thi được và có evidence/readback |
| L4 | Chẩn đoán, đánh giá rủi ro, tối ưu strategy |
| L5 | Định nghĩa standards, quality gate, hướng dẫn người khác |

| Readiness | Nghĩa |
|---|---|
| `DESIGN_ONLY` | Chỉ phân tích/thiết kế, chưa được tuyên bố đã chạy |
| `READY_FOR_DRY_RUN` | Có framework tối thiểu để validate/dry-run local |
| `READY_FOR_EXECUTION` | Có tool, environment, account/data và approval cần thiết |
| `EVIDENCE_PROVEN` | Đã vượt eval và có execution evidence trong audit |
