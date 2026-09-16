# Concurrency & Race Condition — Common Testcase Checklist

## Meta
- prefix: `CHK-CON`
- coverage_type: `duplicate_idempotency_retry_and_concurrency`, `state_sequence_time_and_expiry`
- applies_when: any Create/Edit/Delete action on data shared across users/sessions
- status: DRAFT — adapt to the real concurrency-control mechanism (optimistic lock, pessimistic
  lock, last-write-wins, none) before use; see `INDEX.md`. **Confirm which mechanism the feature
  actually uses before writing expected results** — the three behave very differently and guessing
  produces a wrong oracle.

---

## 1. Giao diện

- **CHK-CON-001 · High** — Record đang được user khác chỉnh sửa → hiển thị cảnh báo rõ ("đang được [user] chỉnh sửa") hoặc lock không cho edit, tuỳ cơ chế đã xác nhận.
- **CHK-CON-002 · High** — Record đã bị thay đổi bởi người khác trước khi save (optimistic lock) → user hiện tại thấy thông báo rõ ("dữ liệu đã bị thay đổi, vui lòng tải lại"), **không âm thầm ghi đè** thay đổi của người kia.
- **CHK-CON-003 · Medium** — Button Submit chuyển sang loading/disabled ngay khi click — ngăn double-submit trước khi có response.

## 2. Chức năng

### 2.1 Double submit / rapid click

- **CHK-CON-020 · High** — Double-click nhanh nút Submit trên kết nối chậm → chỉ tạo đúng 1 record, không duplicate.
- **CHK-CON-021 · High** — Double-click nhanh nút Delete/Confirm → chỉ xoá đúng 1 lần, không lỗi ở lần thao tác thứ 2.
- **CHK-CON-022 · Medium** — Submit liên tiếp nhanh (trước khi response đầu về) → chỉ 1 record tạo thành công, hoặc lần 2 bị block với message rõ ràng.

### 2.2 Nhiều user thao tác đồng thời

- **CHK-CON-030 · High** — 2 user cùng edit 1 record, sửa field khác nhau, cùng save → theo đúng cơ chế đã xác nhận: 1 bên bị reject rõ ràng (optimistic lock), hoặc merge đúng nếu field độc lập (nếu thiết kế hỗ trợ) — không có trường hợp nào mất thầm lặng thay đổi của 1 bên.
- **CHK-CON-031 · High** — User A đang xem detail record X, User B xoá record X → User A thao tác tiếp (edit/save) nhận thông báo "record không còn tồn tại", không crash, redirect hợp lý.
- **CHK-CON-032 · Medium** — 2 user cùng tạo record với giá trị field unique trùng nhau (VD cùng Name) → chỉ 1 bên tạo thành công, bên còn lại nhận lỗi unique constraint rõ ràng (không phải lỗi kỹ thuật chung chung).
- **CHK-CON-033 · Medium** — 2 user cùng đổi trạng thái 1 record theo 2 hướng khác nhau gần như đồng thời → chỉ 1 thay đổi thắng, người còn lại nhận conflict rõ, trạng thái cuối cùng nhất quán (không có trạng thái trung gian sai).

### 2.3 Browser / Tab

- **CHK-CON-040 · High** — Mở cùng 1 form edit ở 2 tab, sửa và save ở tab 1, quay lại tab 2 và save → tab 2 nhận conflict warning hoặc dữ liệu tab 2 được refresh trước khi cho save tiếp — không ghi đè thầm lặng.
- **CHK-CON-041 · Medium** — F5 giữa lúc đang submit → không tạo duplicate; nếu browser hỏi "gửi lại dữ liệu form?" và user đồng ý, xử lý idempotent (không tạo thêm bản ghi thứ 2).
- **CHK-CON-042 · Medium** — Bấm Back sau khi submit thành công rồi Submit lại → không tạo duplicate; hệ thống báo lỗi hoặc điều hướng về record đã tạo.

## 3. Phi chức năng

- **CHK-CON-050 · High** — API hỗ trợ idempotency key: gọi cùng request 2 lần với cùng key → chỉ thực hiện 1 lần, lần 2 trả kết quả của lần 1.
- **CHK-CON-051 · Medium** — Nhiều user thao tác đồng thời trên cùng module (10+ tuỳ ngưỡng dự án) không làm response time tăng đột biến hay gây data corruption — đo thật, không suy đoán.
