# Mẫu defect

Mặc định tạo bản nháp local. Chỉ tạo hoặc cập nhật Jira live sau khi anh phê duyệt rõ trong phiên hiện tại.

## Tiêu đề

Xác nhận 2026-07-19: `[<US_ID>/<Tên US ngắn>][<Type>] Verify <observable behavior>`

Ví dụ: `[US-123/Ingestion][Functional] Verify user can create ingestion source with valid SAP HANA connection`

Lưu ý: dùng phong cách "Verify <behavior>" giống title testcase/AC, khác phong cách "nêu vấn đề" quan sát từ DEMO-976 (`[Module][Sub-component] Unable to ... - <error>`). Đây là lựa chọn tường minh của anh (2026-07-19) — không tự đổi lại theo style DEMO-976.

## Mô tả tiếng Việt

```markdown
### Môi trường
- Build/Version:
- Môi trường và URL:
- Vai trò/Tenant:
- Component/Connector:
- Điều kiện dữ liệu đã làm sạch:

### Điều kiện tiên quyết
- Trạng thái ban đầu:
- Quyền/Feature flag/Dependency:
- Test data:

### Các bước tái hiện
1.
2.
3.

### Kết quả thực tế
- Hành vi quan sát được:
- Mã/thông báo lỗi:
- UI/API/DB/Event/Audit readback:

### Kết quả mong đợi
- Kết quả nghiệp vụ:
- Nguồn xác nhận:

### Bằng chứng
- Screenshot/Video:
- Log/Trace/Request ID:
- Request/Response đã che dữ liệu nhạy cảm:

### Ảnh hưởng
- Người dùng/luồng nghiệp vụ bị ảnh hưởng:
- Hậu quả dữ liệu/bảo mật/vận hành:
- Severity rationale:
- Workaround:

### Khả năng tái hiện và phạm vi ảnh hưởng
- Tần suất:
- Trường hợp bị ảnh hưởng:
- Trường hợp đối chứng không bị ảnh hưởng:

### Liên kết truy vết
- Requirement/User Story:
- Testcase/Execution:
- API operation/Business rule:
- Build/Issue liên quan:
```

Không để heading rỗng. Nếu chưa có dữ liệu, dùng `CHƯA CÓ` hoặc `NEED_CONFIRM` và ghi lý do.

## Cơ sở bắt bug

1. Xác định business invariant và nguồn expected chính thức.
2. Lập ma trận option UI với constraint API/schema/backend.
3. Kiểm tra state, role, tenant, data, boundary và mọi combination rủi ro.
4. Kiểm tra validation xảy ra ở đâu và thông báo có giúp người dùng sửa lỗi hay chỉ lộ raw backend error.
5. Kiểm tra retry, duplicate, concurrency, ordering, partial failure, session/cache và recovery.
6. Đối chiếu UI, API, DB, event, audit và downstream state.
7. Chỉ dùng `CONFIRMED_DEFECT` khi có nguồn, reproduce, evidence, impact và đã loại trừ environment/test-data/automation issue.

## Quy tắc bảo mật

- Không lưu bearer token, password, cookie, API key, private key hoặc credential thật.
- Thay secret bằng `<đã-che>` và chỉ giữ phần request/response cần chẩn đoán.
- Không đính kèm `.json` hoặc `.md` lên Jira nếu anh chưa yêu cầu rõ.
