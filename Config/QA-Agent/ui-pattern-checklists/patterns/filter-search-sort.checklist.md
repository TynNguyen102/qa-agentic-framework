# Filter / Search / Sort — Common Testcase Checklist

## Meta
- prefix: `CHK-LST`
- coverage_type: `happy_and_alternate_paths`, `equivalence_and_boundary_classes`, `state_preservation_refresh_back_forward_and_multi_tab`
- applies_when: list/table screen has a filter bar, search box, and/or sortable columns
- status: DRAFT — adapt control names to the real mockup/UI before use; see `INDEX.md`

---

## 1. Filter

- **CHK-LST-001 · High** — Áp 1 filter → kết quả chỉ chứa record thoả điều kiện, tổng số cập nhật đúng.
- **CHK-LST-002 · High** — Áp nhiều filter cùng lúc (combination) → kết quả là **AND** đúng nghĩa của tất cả điều kiện (xác nhận rõ AND hay OR với BRD nếu không chắc — đừng đoán).
- **CHK-LST-003 · Medium** — Filter không có kết quả → empty state đúng (khác empty state "chưa filter gì"), có gợi ý "xoá filter"/"reset" nếu thiết kế có.
- **CHK-LST-004 · Medium** — Clear/reset filter → quay về danh sách đầy đủ, control filter trả về trạng thái mặc định.
- **CHK-LST-005 · Medium** — Filter theo khoảng (range: ngày, số) — biên: giá trị đúng biên dưới/trên có được tính vào không (inclusive/exclusive) — xác nhận với BRD, đừng suy đoán.
- **CHK-LST-006 · Medium** — Badge/hiển thị số filter đang active (nếu thiết kế có) đúng số lượng, click badge xoá đúng filter đó.

## 2. Search

- **CHK-LST-020 · High** — Search với từ khoá khớp chính xác → trả đúng record.
- **CHK-LST-021 · Medium** — Search không phân biệt hoa/thường, không phân biệt dấu (tuỳ ngôn ngữ hệ thống) — xác nhận hành vi mong đợi thật với BRD trước khi coi là bug.
- **CHK-LST-022 · Medium** — Search một phần chuỗi (substring) nếu thiết kế hỗ trợ — xác nhận search theo prefix hay full substring.
- **CHK-LST-023 · Medium** — Search ký tự đặc biệt (`%`, `_`, `'`, khoảng trắng thừa, emoji) không làm crash hoặc trả kết quả sai lệch bất thường.
- **CHK-LST-024 · Medium** — Debounce/độ trễ search: gõ nhanh liên tục không gửi N request thừa, không hiển thị kết quả của request cũ đè lên request mới (race condition giữa các lần gõ).
- **CHK-LST-025 · Low** — Xoá hết search box → quay về danh sách đầy đủ (hoặc theo filter đang áp, không mất filter khác).

## 3. Sort

- **CHK-LST-040 · High** — Click header cột sortable → sort tăng dần đúng theo kiểu dữ liệu (số/chữ/ngày) — chữ có dấu thì đúng theo locale, không sort như ASCII thô nếu hệ thống không có ý đó.
- **CHK-LST-041 · High** — Click lần 2 → đảo chiều giảm dần; click lần 3 (nếu có trạng thái "không sort") → quay về sort mặc định hoặc theo đúng hành vi thiết kế.
- **CHK-LST-042 · Medium** — Sort đồng thời với filter/search đang áp → kết quả vẫn đúng điều kiện filter/search, chỉ đổi thứ tự.
- **CHK-LST-043 · Medium** — Cột có giá trị null/trống khi sort: nằm đầu hay cuối danh sách theo đúng quy ước đã xác nhận, không random.
- **CHK-LST-044 · Low** — Icon sort hiển thị đúng chiều đang active, chỉ 1 cột active tại một thời điểm (trừ khi thiết kế hỗ trợ multi-sort).

## 4. Duy trì trạng thái (cross-cutting với browser-device)

- **CHK-LST-060 · High** — Filter/search/sort/trang hiện tại **giữ nguyên** khi: F5 refresh (nếu thiết kế encode vào URL query), quay lại bằng nút Back của browser sau khi vào detail rồi quay ra, hoặc chuyển tab rồi quay lại — xác nhận đúng hành vi mong đợi của thiết kế (persist qua URL vs reset về mặc định) trước khi kết luận PASS/FAIL.
- **CHK-LST-061 · Medium** — Chia sẻ URL đã có filter/sort (nếu encode trong URL) cho người khác/tab khác → mở ra đúng trạng thái filter đó.
