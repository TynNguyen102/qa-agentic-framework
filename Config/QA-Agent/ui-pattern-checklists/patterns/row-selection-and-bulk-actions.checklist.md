# Row Selection & Bulk Actions — Common Testcase Checklist

## Meta
- prefix: `CHK-SEL`
- coverage_type: `duplicate_idempotency_retry_and_concurrency`, `state_sequence_time_and_expiry`
- applies_when: table/list has row checkboxes and a bulk action bar
- status: DRAFT — adapt control names to the real mockup/UI before use; see `INDEX.md`

---

## 1. Giao diện

- **CHK-SEL-001 · Medium** — Chọn 1 row → checkbox check đúng, action bar/toolbar bulk xuất hiện với đúng số lượng đã chọn.
- **CHK-SEL-002 · Medium** — Chọn tất cả (header checkbox) → toàn bộ row trên trang hiện tại được chọn. Xác nhận rõ: có chọn cả record ở trang khác không, hay chỉ trang đang xem — hành vi này khác nhau nhiều giữa các hệ thống, đừng suy đoán.
- **CHK-SEL-003 · Medium** — Bỏ chọn tất cả → toolbar bulk biến mất, checkbox header về trạng thái chưa check.
- **CHK-SEL-004 · Low** — Chọn một phần (không phải tất cả, không phải không có gì) → header checkbox ở trạng thái indeterminate (dấu gạch ngang), không hiện sai thành checked hoàn toàn.

## 2. Chức năng

- **CHK-SEL-020 · High** — Bulk action (VD xoá/export/đổi trạng thái hàng loạt) áp dụng đúng và chỉ đúng tập record đã chọn — không sót, không dính thêm record khác.
- **CHK-SEL-021 · High** — Bulk action trên tập record có 1 record không đủ điều kiện thực hiện (VD đã bị xoá bởi người khác, hoặc thiếu quyền trên riêng record đó) → hệ thống báo rõ record nào fail, record hợp lệ vẫn xử lý xong (partial success có thông báo rõ) — không âm thầm rollback toàn bộ mà không giải thích, và không báo "thành công" mù mờ khi thực ra có phần fail.
- **CHK-SEL-022 · Medium** — Chọn record ở trang 1, chuyển sang trang 2 rồi quay lại trang 1 → trạng thái chọn có giữ nguyên theo đúng thiết kế (một số hệ thống giữ selection xuyên trang, một số reset theo trang) — xác nhận hành vi mong đợi, không tự suy đoán rồi báo bug sai.
- **CHK-SEL-023 · Medium** — Bulk action trên tập rỗng (0 record được chọn) → nút bulk action phải disabled, không cho thực hiện.

## 3. Phi chức năng

- **CHK-SEL-040 · Medium** — Bulk action trên số lượng lớn record (ngưỡng cụ thể theo dự án) → có loading/progress rõ ràng, không block UI vô thời hạn, không timeout im lặng khiến user tưởng đã xong.
