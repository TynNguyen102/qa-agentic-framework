# Detail / View Screen — Common Testcase Checklist

## Meta
- prefix: `CHK-DTL`
- coverage_type: `loading_empty_error_success_partial_and_stale_states`, `route_guards_navigation_and_deep_links`
- applies_when: feature has a detail/view screen for a single record (page or panel)
- status: DRAFT — adapt section/field names to the real mockup/UI before use; see `INDEX.md`

---

## 1. Giao diện

- **CHK-DTL-001 · Medium** — Layout tổng quan đúng theo mockup: section/tab đúng thứ tự, đúng heading.
- **CHK-DTL-002 · Medium** — Từng field/data point: đúng label, đúng format hiển thị (ngày, số, badge màu...), empty state riêng cho field không có giá trị (áp dụng cùng quy tắc "0 vs — vs trống" của `table-list.checklist.md`).
- **CHK-DTL-003 · Medium** — Loading state khi đang tải chi tiết; error state nếu load thất bại (không phải trang trắng im lặng).

## 2. Chức năng

- **CHK-DTL-020 · High** — Dữ liệu hiển thị khớp đúng với nguồn (API/DB) cho đúng record đang xem — đặc biệt xác nhận không bị lệch record khi vào từ danh sách đang có filter/sort.
- **CHK-DTL-021 · High** — Truy cập trực tiếp bằng URL/deep link tới ID record không tồn tại → xử lý rõ ràng (404/thông báo hợp lệ), không crash trang trắng.
- **CHK-DTL-022 · Medium** — Navigation trong trang chi tiết (tab con, link sang record liên quan) đi đúng đích.
- **CHK-DTL-023 · Medium** — Nút Back (trong app, không phải nút Back browser) quay về đúng danh sách gốc, giữ đúng trạng thái filter/sort/trang đã có trước khi vào detail.
- **CHK-DTL-024 · Medium** — Action có trên màn (nếu có nút Edit/Delete/... ngay trong detail) hoạt động đúng, đồng bộ với hành vi đã test ở checklist tương ứng (`create-edit-form`, `delete`).

## 3. Phi chức năng

- **CHK-DTL-040 · Low** — Accessibility: heading/section đọc được đúng thứ tự bằng screen reader.
