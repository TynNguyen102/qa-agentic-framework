# Field Validation (by input type) — Common Testcase Checklist

## Meta
- prefix: `CHK-FLD`
- coverage_type: `form_validation_timing_messages_and_recovery`, `equivalence_and_boundary_classes`
- applies_when: any form field of the types below — load only the sub-section matching field types
  actually present in this feature's mockup, not every section
- status: DRAFT — adapt to the real field name/constraints before use; see `INDEX.md`

---

## A. Text input (single/multi-line) — `CHK-FLD-TXT`

- **001 · High** — Giá trị hợp lệ ở giữa khoảng độ dài cho phép → lưu đúng.
- **002 · High** — Biên độ dài: đúng min length (nếu có), đúng max length (chặn nhập thêm hoặc validate khi submit — xác nhận cơ chế nào), 1 ký tự dưới min, 1 ký tự trên max.
- **003 · Medium** — Chuỗi toàn khoảng trắng → coi như rỗng nếu field required (không được pass validate required).
- **004 · Medium** — Khoảng trắng đầu/cuối chuỗi hợp lệ → tự động trim hay giữ nguyên theo đúng thiết kế.
- **005 · Medium** — Ký tự đặc biệt/Unicode (emoji, tiếng Việt có dấu, ký tự RTL) → lưu và hiển thị lại đúng, không vỡ encoding.
- **006 · High** — Chuỗi HTML/script (`<script>`) → không được thực thi khi hiển thị lại (xem thêm `23-security-testing` nếu nghi ngờ XSS thật).
- **007 · Medium** — Format-specific (email/phone/URL nếu field ràng buộc format riêng) → đúng/sai theo regex đã xác nhận, không đoán quy tắc.

## B. Dropdown (single-select) — `CHK-FLD-DDL`

- **001 · High** — Danh sách option đúng, đúng thứ tự theo BRD/mockup (alphabet, theo priority nghiệp vụ, hay theo thứ tự tạo — xác nhận rõ).
- **002 · Medium** — Option mặc định đúng khi mở form Create (nếu có default) và khi mở form Edit (giá trị hiện tại của record, không phải default).
- **003 · Medium** — Option bị vô hiệu hoá có điều kiện (phụ thuộc field khác) → đúng theo cross-field rule.
- **004 · Medium** — Danh sách option rỗng (chưa có data nguồn) → hiển thị placeholder rõ ràng, không phải dropdown trống câm lặng.
- **005 · Low** — Search/filter trong dropdown (nếu là searchable-select) hoạt động đúng, không phân biệt hoa/thường theo đúng thiết kế.

## C. Multi-select / tag chip — `CHK-FLD-MSEL`

- **001 · High** — Chọn nhiều giá trị → lưu đúng, hiển thị lại đủ tất cả (không rơi mất giá trị khi re-render).
- **002 · Medium** — Bỏ chọn 1 tag giữa danh sách nhiều tag → chỉ mất đúng tag đó.
- **003 · Medium** — Giới hạn số lượng chọn tối đa (nếu có) → chặn đúng khi đạt ngưỡng, thông báo rõ.
- **004 · Medium** — Tạo tag mới tại chỗ (nếu hỗ trợ "create new") → tag mới được lưu đúng vào nguồn dữ liệu chung, không chỉ tồn tại cục bộ trong form này.
- **005 · Low** — Nhiều tag vượt quá độ rộng field → overflow indicator ("+N") hoặc wrap dòng đúng thiết kế.

## D. Date / datetime picker — `CHK-FLD-DATE`

- **001 · High** — Chọn ngày hợp lệ → lưu và hiển thị lại đúng định dạng, đúng timezone đã xác nhận (đây là nguồn lỗi rất phổ biến — xác nhận rõ giờ hiển thị theo timezone nào).
- **002 · High** — Biên: ngày min/max cho phép (nếu có giới hạn, VD không được chọn ngày quá khứ cho 1 field, hoặc không quá X ngày trong tương lai) — test đúng biên và 1 ngày ngoài biên.
- **003 · Medium** — Range picker (từ ngày - đến ngày): "đến" phải ≥ "từ" — chọn ngược thứ tự phải bị chặn hoặc tự đảo lại theo đúng thiết kế.
- **004 · Medium** — Nhập tay (nếu cho phép gõ trực tiếp thay vì chỉ chọn từ lịch) với format sai → validate đúng, không parse sai thành ngày khác không báo lỗi.
- **005 · Low** — Time picker riêng (nếu tách date và time) → kết hợp đúng thành 1 giá trị datetime khi lưu.

## E. Rich text editor — `CHK-FLD-RTE`

- **001 · Medium** — Format cơ bản (bold/italic/list/link) lưu và hiển thị lại đúng.
- **002 · High** — Nội dung dán từ nguồn ngoài (Word, web) không mang theo style/script rác phá layout hoặc gây XSS khi hiển thị lại.
- **003 · Medium** — Giới hạn độ dài nội dung (nếu có) tính đúng trên nội dung thật (text), không tính lẫn các thẻ HTML ẩn của editor.
- **004 · Low** — Rỗng thật sự (chỉ có thẻ `<p></p>` rỗng do editor tự sinh) phải được coi là rỗng nếu field required, không pass validate nhầm.

## F. File attachment / upload — `CHK-FLD-ATT`

- **001 · High** — Upload đúng định dạng, đúng dung lượng cho phép → thành công, file lưu đúng và tải lại được nguyên vẹn.
- **002 · High** — Vượt quá dung lượng tối đa → chặn với thông báo rõ dung lượng giới hạn.
- **003 · High** — Sai định dạng file không được chấp nhận (kể cả đổi đuôi file giả mạo — kiểm tra bằng nội dung thật/MIME, không chỉ đuôi file) → bị chặn.
- **004 · High** — Tên file chứa ký tự đặc biệt/path traversal (`../`, `<script>` trong tên) → xử lý an toàn, không gây lỗi hệ thống lưu trữ.
- **005 · Medium** — Upload nhiều file cùng lúc (nếu hỗ trợ) → đúng số lượng, đúng thứ tự hiển thị, xoá từng file riêng lẻ không ảnh hưởng file khác.
- **006 · Medium** — Xoá file đã upload trước khi submit form → không còn gửi kèm khi submit.
