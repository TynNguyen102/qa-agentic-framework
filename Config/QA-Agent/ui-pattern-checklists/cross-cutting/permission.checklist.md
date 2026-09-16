# Permission / Role-Based Access Control — Common Testcase Checklist

## Meta
- prefix: `CHK-PRM`
- coverage_type: `actors_roles_permissions_and_tenants`, `authentication_authorization_and_abuse`, `role_tenant_and_cross_entity_isolation`, `sensitive_data_secrets_logging_and_error_exposure`
- applies_when: any screen/feature with role-based access control
- status: DRAFT — adapt role names to the real permission matrix before use; see `INDEX.md`. Never
  use another project's permission matrix as truth for this one — this checklist names the *shape*
  of what to test, the actual role/permission values must come from this project's confirmed source.

---

## 1. Giao diện

- **CHK-PRM-001 · High** — Button/menu/section không thuộc quyền của role hiện tại phải **ẩn hoàn toàn** hoặc **disabled rõ ràng** — không hiển thị như bình thường nhưng âm thầm không hoạt động khi click.
- **CHK-PRM-002 · High** — Menu item của module/tính năng không được phép không xuất hiện trong sidebar/navigation.
- **CHK-PRM-003 · Medium** — Cột dữ liệu nhạy cảm ẩn hoặc masked (`***`) đúng theo role không có quyền xem.
- **CHK-PRM-004 · High** — Role có đầy đủ quyền (Admin/tương đương) thấy đầy đủ mọi button/menu/cột/action ở trạng thái active.

## 2. Chức năng

### 2.1 Truy cập trực tiếp (bypass UI)

- **CHK-PRM-020 · High** — Nhập trực tiếp URL của module không có quyền → redirect 403/trang chủ, không hiển thị nội dung dù chỉ trong khoảnh khắc trước redirect.
- **CHK-PRM-021 · High** — Nhập trực tiếp URL chi tiết 1 record không có quyền xem → 403/redirect, không lộ dữ liệu record qua bất kỳ đường nào (kể cả preview/cache).
- **CHK-PRM-022 · High** — Gọi thẳng API (không qua UI) với token hợp lệ nhưng thiếu quyền cho action đó → API trả 403, action không được thực hiện dù request hợp lệ về mặt kỹ thuật.

### 2.2 Hành động theo role

- **CHK-PRM-030 · High** — Role không có quyền Create/Edit/Delete/Export: thử thực hiện qua mọi đường (UI ẩn nhưng thử URL/API trực tiếp) → bị từ chối nhất quán ở mọi đường, không chỉ chặn ở UI.
- **CHK-PRM-031 · High** — Role không có quyền vào Settings/cấu hình hệ thống → menu ẩn và truy cập trực tiếp cũng bị chặn.

### 2.3 Session & thay đổi quyền khi đang dùng

- **CHK-PRM-040 · High** — Session hết hạn giữa lúc đang thao tác (đang điền form dài) → submit sau khi hết hạn bị chặn, redirect login rõ ràng, dữ liệu không bị submit một phần.
- **CHK-PRM-041 · High** — **Quyền bị thu hồi trong khi user đang đăng nhập** (Admin đổi role ngay lúc đó) → hành động tiếp theo bị từ chối **ngay, không cần logout/login lại mới có hiệu lực**.
- **CHK-PRM-042 · Medium** — User có nhiều role/nhóm quyền đồng thời → được phép thực hiện theo union của các quyền (quyền cao nhất áp dụng), không bị quyền thấp hơn ghi đè nhầm.
- **CHK-PRM-043 · High** — Sau logout, bấm Back trên browser quay lại trang cũ → redirect login, không hiển thị dữ liệu cache cũ.

## 3. Phi chức năng

- **CHK-PRM-050 · High** — Dữ liệu field không có quyền xem **không tồn tại trong DOM/response** — không chỉ bị ẩn bằng CSS hoặc lọc ở phía client. Kiểm bằng cách xem thẳng response API/HTML source, không chỉ nhìn UI đã render.
- **CHK-PRM-051 · High** — Token/session key không xuất hiện trong URL query string ở bất kỳ thao tác nào.
- **CHK-PRM-052 · Medium** — Hành động bị từ chối do thiếu quyền được ghi log (attempt unauthorized) nếu tính năng audit yêu cầu — role có thẩm quyền xem được log này.
