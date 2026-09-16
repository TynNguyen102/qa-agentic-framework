# Stat Card / Metric Widget & Activity Log — Common Testcase Checklist

## Meta
- prefix: `CHK-WID`
- coverage_type: `business_side_effects_and_readback`, `observability_logs_metrics_traces_alerts_and_correlation`
- applies_when: feature has a stat/metric card, dashboard widget, and/or an Activity/Audit log tab
- status: DRAFT — adapt widget/column names to the real mockup/UI before use; see `INDEX.md`

---

## A. Stat card / metric widget

### Giao diện & Chức năng

- **CHK-WID-001 · High** — Con số trên card khớp với phép tính thật từ dữ liệu nguồn — tự tính lại độc lập (không chỉ tin UI), đối chiếu công thức đã xác nhận (VD tổng, trung bình, % thay đổi so với kỳ trước).
- **CHK-WID-002 · Medium** — Card cập nhật đúng khi dữ liệu nguồn thay đổi (realtime hoặc theo chu kỳ refresh đã xác nhận).
- **CHK-WID-003 · Medium** — Card ở trạng thái 0 data thật sự (chưa có gì để tính) hiển thị khác với lỗi tải dữ liệu — không gộp làm một, dùng cùng quy tắc "0 vs — vs trống".
- **CHK-WID-004 · Medium** — Khoảng thời gian/bộ lọc áp dụng cho toàn dashboard (nếu có) phản ánh đúng vào từng card — không có card nào "quên" áp filter.
- **CHK-WID-005 · Low** — Click vào card (nếu có drill-down) điều hướng đúng tới danh sách/màn chi tiết tương ứng với đúng filter ngầm định của card đó.

## B. Activity / Audit Log

### Giao diện & Chức năng

- **CHK-WID-020 · High** — Mỗi hành động ghi log (create/update/delete/trạng thái đổi...) tạo đúng 1 entry, đúng nội dung mô tả hành động, đúng actor thực hiện, đúng timestamp.
- **CHK-WID-021 · High** — Log hiển thị **giá trị cũ → giá trị mới** nếu thiết kế yêu cầu (không chỉ "đã sửa field X" chung chung khi BRD cần chi tiết before/after).
- **CHK-WID-022 · Medium** — Log entry vẫn tồn tại sau khi record liên quan bị xoá (log không biến mất theo record, trừ khi thiết kế xác nhận ngược lại).
- **CHK-WID-023 · Medium** — Log không thể chỉnh sửa/xoá bởi user thường (tính bất biến của audit trail) — chỉ role có thẩm quyền mới thấy tuỳ chọn liên quan, nếu có.
- **CHK-WID-024 · Medium** — Log của action bị từ chối do thiếu quyền (xem `cross-cutting/permission.checklist.md` CHK-PRM-052) vẫn được ghi lại nếu thiết kế yêu cầu audit cả attempt thất bại.
- **CHK-WID-025 · Low** — Log hỗ trợ filter/search/pagination (nếu có) — áp dụng lại checklist tương ứng (`filter-search-sort`, `pagination`) cho chính bảng log này.
