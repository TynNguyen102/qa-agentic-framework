# Export (CSV / Excel / PDF) — Common Testcase Checklist

## Meta
- prefix: `CHK-EXP`
- coverage_type: `business_side_effects_and_readback`
- applies_when: feature has an Export/Download action
- status: DRAFT — adapt control names to the real mockup/UI before use; see `INDEX.md`
- **Mandatory cross-reference**: this checklist is not sufficient by itself — route to
  `41-generated-file-testing` for the full file-testing protocol (encoding/BOM/delimiter, opening in
  the real consuming application, formula injection, export authorization). Do not close a file
  defect on a byte-level check alone.

---

## 1. Giao diện

- **CHK-EXP-001 · Medium** — Nút Export đúng label, đúng trạng thái enable/disable theo có/không có dữ liệu để xuất.
- **CHK-EXP-002 · Medium** — Trong lúc export (nếu xử lý async/mất thời gian) → loading indicator rõ, không cho bấm export lần 2 chồng lên.

## 2. Chức năng

- **CHK-EXP-020 · High** — File xuất ra chứa **đúng tập record đang hiển thị theo filter/search/sort hiện tại** — xác nhận rõ export theo "đang xem" hay "toàn bộ dữ liệu" trước khi coi là bug, hai hành vi này khác nhau hoàn toàn.
- **CHK-EXP-021 · High** — Số cột, tên cột, thứ tự cột trong file khớp với cấu trúc đã xác nhận (có thể khác thứ tự UI nếu export có mapping riêng — xác nhận với BRD).
- **CHK-EXP-022 · High** — Giá trị từng ô trong file khớp với dữ liệu nguồn (không bị làm tròn/cắt/đổi định dạng ngày ngoài ý muốn).
- **CHK-EXP-023 · Medium** — Export tập dữ liệu rỗng (0 record sau filter) → xử lý rõ ràng (file có header nhưng 0 dòng data, hoặc chặn export với thông báo) — không phải file lỗi/crash.
- **CHK-EXP-024 · Medium** — Bulk export (kết hợp với row-selection) chỉ chứa đúng record đã chọn.

## 3. Phi chức năng

- **CHK-EXP-040 · High** — Dữ liệu chứa ký tự đặc biệt có thể bị Excel diễn giải thành công thức (`=`, `+`, `-`, `@` ở đầu ô) → không được thực thi như công thức khi mở file (formula injection) — route sang `41-generated-file-testing` để đánh giá đầy đủ.
- **CHK-EXP-041 · Medium** — Export tập dữ liệu lớn → không timeout, có giới hạn hợp lý hoặc xử lý bất đồng bộ (job + link tải sau), không block UI.
