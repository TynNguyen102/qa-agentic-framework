# Pagination — Common Testcase Checklist

## Meta
- prefix: `CHK-PAG`
- coverage_type: `equivalence_and_boundary_classes`, `state_preservation_refresh_back_forward_and_multi_tab`
- applies_when: list/table has more records than fit on one page
- status: DRAFT — adapt control names to the real mockup/UI before use; see `INDEX.md`

---

## 1. Giao diện

- **CHK-PAG-001 · Medium** — Footer hiển thị đúng: trang hiện tại, tổng số trang, tổng số bản ghi, tuỳ chọn số item/trang nếu thiết kế có.
- **CHK-PAG-002 · Low** — Nút Previous disabled ở trang đầu, nút Next disabled ở trang cuối.

## 2. Chức năng — biên số

- **CHK-PAG-020 · High** — Trang 1: đúng số item cấu hình (VD 20/trang), đúng thứ tự.
- **CHK-PAG-021 · High** — Trang cuối: chỉ hiện số item còn lại (không tràn, không lặp record của trang trước).
- **CHK-PAG-022 · Medium** — Tổng bản ghi là bội số chẵn của số item/trang (VD đúng 40 record, 20/trang) — trang cuối vẫn hiện đúng 20, không phát sinh trang rỗng thừa.
- **CHK-PAG-023 · Medium** — Đổi số item/trang (10/20/50...) → tính lại đúng số trang, giữ nguyên (hoặc reset về trang 1 theo đúng thiết kế) vị trí record đang xem nếu có thể.
- **CHK-PAG-024 · Medium** — Nhảy trực tiếp tới số trang bất kỳ (nếu có input số trang) — nhập số vượt quá tổng số trang → không crash, xử lý hợp lý (kẹp về trang cuối hoặc báo lỗi).
- **CHK-PAG-025 · Medium** — Đang ở trang N > 1, dữ liệu bị xoá bớt từ nơi khác khiến trang N không còn tồn tại → không hiển thị trang trắng lỗi, tự điều chỉnh về trang hợp lệ gần nhất.
- **CHK-PAG-026 · High** — Kết hợp pagination với filter/sort: đổi filter → reset về trang 1 (không giữ số trang cũ có thể vượt quá tổng trang mới, gây trang trắng).

## 3. Phi chức năng

- **CHK-PAG-040 · Low** — Chuyển trang không load lại toàn bộ trang (nếu là SPA) — chỉ phần bảng cập nhật, giữ nguyên filter/search UI state.
