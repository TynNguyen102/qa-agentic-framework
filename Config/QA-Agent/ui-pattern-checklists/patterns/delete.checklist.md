# Delete — Common Testcase Checklist

## Meta
- prefix: `CHK-DEL`
- coverage_type: `partial_failure_rollback_and_cleanup`, `business_side_effects_and_readback`
- applies_when: feature has a delete action (single or bulk)
- status: DRAFT — adapt control names to the real mockup/UI before use; see `INDEX.md`
- **Also read**: `patterns/create-edit-form.checklist.md`'s 9-point action procedure, and
  `cross-cutting/concurrency.checklist.md` for concurrent-delete scenarios.

---

## 1. Giao diện

- **CHK-DEL-001 · High** — Nút Delete chỉ hiển thị/enable theo đúng role và đúng điều kiện trạng thái record (nếu có ràng buộc, VD không xoá được record đang ở trạng thái đang xử lý).
- **CHK-DEL-002 · High** — Confirm dialog xuất hiện trước khi xoá thật — không xoá ngay khi click 1 lần. Nội dung confirm nêu rõ đối tượng sắp xoá (tên/ID record, hoặc số lượng nếu bulk).

## 2. Chức năng

- **CHK-DEL-020 · High** — Xác nhận xoá → record biến mất khỏi danh sách, tổng số bản ghi giảm đúng.
- **CHK-DEL-021 · High** — **Request**: bấm Confirm xoá thực sự gửi đúng request (endpoint/method DELETE hoặc tương đương, đúng ID record) — mở DevTools Network hoặc bắt request tại tầng automation, không suy đoán từ việc UI đã ẩn record. **Response + DB**: status code đúng, và đối chiếu tầng lưu trữ (API GET lại hoặc DB) xác nhận record thực sự đã bị xoá (hoặc soft-delete/archive đúng theo thiết kế) — 3 lớp (request/response/DB) độc lập, không suy ra lẫn nhau: UI ẩn record có thể chỉ là optimistic update trong khi request thực tế chưa gửi hoặc đã fail.
- **CHK-DEL-022 · Medium** — Huỷ ở confirm dialog → record không bị xoá, không có side-effect nào xảy ra.
- **CHK-DEL-023 · High** — Xoá record đang được tham chiếu bởi dữ liệu khác (foreign key/liên kết cross-feature) → xử lý đúng theo thiết kế: chặn xoá kèm lý do rõ, hoặc cascade đúng phạm vi đã xác nhận — không để lại orphan record hay lỗi ngầm.
- **CHK-DEL-024 · Medium** — Xoá hàng loạt (bulk) với 1 phần record không đủ điều kiện xoá → báo rõ record nào fail/lý do, record hợp lệ vẫn xoá xong đúng (partial success có thông báo).
- **CHK-DEL-025 · Medium** — Nếu tính năng có Activity Log: entry xoá ghi đúng actor, đúng record, đúng thời gian, tồn tại **sau khi** record đã bị xoá (log không bị xoá theo record).

## 3. Phi chức năng

- **CHK-DEL-040 · High** — Double-click nút Delete/Confirm không gây lỗi "record not found" ở lần thao tác thứ 2 và không xoá nhầm record khác nếu list đã re-render.
- **CHK-DEL-041 · Medium** — Xoá record trong khi user khác đang xem/edit record đó — xem `cross-cutting/concurrency.checklist.md` mục Concurrent Delete.
