# Table / List Screen — Common Testcase Checklist

## Meta
- prefix: `CHK-TBL`
- coverage_type: `loading_empty_error_success_partial_and_stale_states`, `business_side_effects_and_readback`, `persistence_events_cache_and_downstream_consistency`
- applies_when: feature has a data table or list view of any kind
- status: DRAFT — adapt column/label names to the real mockup/UI before use; see `INDEX.md`

---

## 1. Giao diện

- **CHK-TBL-001 · High** — Header đủ đúng số cột, đúng thứ tự, đúng tên theo mockup/design thật.
- **CHK-TBL-002 · Medium** — Alignment nhất quán: ID/text căn trái, ngày căn giữa, trạng thái căn giữa/phải; không lệch padding giữa các dòng.
- **CHK-TBL-003 · High** — **Ba trạng thái ô dữ liệu, không được gộp làm một**: số liệu bằng 0 thật (có data, giá trị = 0), không áp dụng (hiển thị `—` hoặc ký hiệu quy ước), và không có data (ô trống). Viết 1 TC riêng cho mỗi trạng thái trên cùng 1 cột.
- **CHK-TBL-004 · Medium** — Giá trị dài: cột có kích thước cố định, giá trị dài bị ellipsis/truncate hoặc xuống dòng theo đúng quy ước thiết kế — không vỡ layout, không đẩy cột khác.
- **CHK-TBL-005 · Medium** — Nếu có ngưỡng "xem thêm" (hiện N ký tự/item rồi link "Xem thêm"/"+N"): 1 TC cho nội dung ≤ ngưỡng (hiện đủ, không có link), 1 TC cho > ngưỡng (chỉ hiện N + link), 1 TC cho click mở rộng, 1 TC cho thu gọn lại.
- **CHK-TBL-006 · Medium** — Cột có thể chứa nhiều giá trị (tag, nhãn, multi-value): kiểm overflow indicator ("+N") hoặc tooltip hiển thị đủ khi hover.
- **CHK-TBL-007 · High** — Empty state: không có dữ liệu → hiển thị message rõ ràng ở giữa bảng, không phải khoảng trắng.
- **CHK-TBL-008 · Medium** — Loading state: đang tải → skeleton/spinner, không hiển thị bảng rỗng gây hiểu nhầm là "không có data".
- **CHK-TBL-009 · Medium** — Error state: load thất bại → thông báo lỗi + hành động thử lại, không phải bảng trắng im lặng.
- **CHK-TBL-010 · Medium** — Cột/hàng cố định (sticky header, sticky column) nếu thiết kế có: giữ nguyên khi scroll ngang/dọc, dữ liệu không lệch hàng.

## 2. Chức năng

- **CHK-TBL-020 · High** — Đối chiếu giá trị từng ô với nguồn dữ liệu thật (API response hoặc DB) cho ít nhất 1 record đầy đủ — không chỉ nhìn UI "có vẻ đúng". Không nhầm cột (swap).
- **CHK-TBL-021 · High** — Tổng số bản ghi hiển thị (footer/pagination) khớp với tổng thật từ nguồn dữ liệu.
- **CHK-TBL-022 · Medium** — Dữ liệu cập nhật khi có thay đổi từ nguồn khác (record mới/sửa/xoá ở màn khác hoặc do hệ thống khác ghi) — sau F5 hoặc theo cơ chế refresh của app, danh sách phản ánh đúng, tổng số cập nhật theo.
- **CHK-TBL-023 · Medium** — Click vào row: điều hướng đúng tới detail của đúng record đó (không lệch record khi danh sách đang có filter/sort/pagination áp dụng).
- **CHK-TBL-024 · Low** — Hover row có highlight; không ảnh hưởng khả năng click các control khác trong hàng.

## 3. Phi chức năng

- **CHK-TBL-040 · High** — Dữ liệu chứa chuỗi giống HTML/script (`<script>...</script>`, thẻ `<img onerror=...>`): hiển thị dưới dạng text an toàn, không thực thi (route thêm vào `23-security-testing` nếu phát hiện thực thi được — đây không phải bằng chứng đầy đủ đã hết XSS).
- **CHK-TBL-041 · Medium** — Bảng lớn (hàng trăm/nghìn bản ghi tuỳ ngưỡng thực tế của tính năng): thời gian render nằm trong ngưỡng chấp nhận được của dự án — lấy ngưỡng cụ thể từ SLO/NFR đã duyệt, không tự đặt số nếu chưa có.
- **CHK-TBL-042 · Low** — Accessibility: header/data đọc được tuần tự bằng screen reader, có ARIA label phù hợp cho bảng và các control tương tác trong hàng.
