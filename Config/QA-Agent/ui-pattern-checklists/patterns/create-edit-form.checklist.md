# Create / Edit Form — Common Testcase Checklist

## Meta
- prefix: `CHK-FRM`
- coverage_type: `form_validation_timing_messages_and_recovery`, `decision_tables_and_cross_field_rules`, `persistence_events_cache_and_downstream_consistency`, `partial_failure_rollback_and_cleanup` (Edit)
- applies_when: feature has a create form/modal and/or an edit flow
- status: DRAFT — adapt field/button names to the real mockup/UI before use; see `INDEX.md`
- **Also read**: `patterns/field-validation.checklist.md` for the field-type-specific items (text,
  dropdown, multi-select, date, rich text, attachment) — this file covers the form as a whole.

---

## Quy trình 9 điểm — dùng để không bỏ sót khi viết case cho bất kỳ action Create/Edit/Delete nào

Với mỗi action (Create, Edit, hoặc bước tương đương trong Delete), rà đủ 9 điểm sau theo thứ tự —
mỗi điểm ít nhất 1 case hoặc ghi rõ N/A + lý do:

1. **Mở chức năng** — đúng tên button/trigger, đúng vị trí, đúng visibility theo role.
2. **Nhập/chỉnh sửa dữ liệu** — từng field theo đúng thứ tự trên mockup; field nào ảnh hưởng field khác (cross-field dependency) phải có case riêng.
3. **Lưu (happy path)** — dữ liệu hợp lệ → thành công, đúng dữ liệu được lưu.
4. **Huỷ** — có xác nhận "discard changes?" nếu đã nhập dữ liệu; huỷ thì không lưu gì.
5. **Validation** — required field, format rule, business constraint, cross-field rule.
6. **Kết quả sau khi lưu** — redirect đi đâu, màn hình đổi gì, toast/message thành công đúng nội dung.
7. **Ảnh hưởng tới dữ liệu trong danh sách** — record mới/đã sửa xuất hiện đúng vị trí, count cập nhật, **và đúng từng field theo Field Propagation Map** (xem mục riêng bên dưới) — không phải "record hiện đúng" chung chung.
8. **Ảnh hưởng tới hệ thống/màn hình liên quan** — theo Field Propagation Map (Detail, màn khác) và cross-screen effect đã biết của module (xem `Knowledge-Base/Domain-Rules/<module>/_overview.md` nếu có).
9. **Activity Log/Audit** — nếu tính năng có ghi log: entry đúng nội dung, đúng actor, đúng timestamp.

---

## Field Propagation Map — dựng TRƯỚC khi viết Expected của điểm 6-8

Đây là bước hay bị bỏ qua nhất và là lý do phổ biến nhất khiến Expected Result quá chung chung
("record xuất hiện đúng trong list") khiến `13-execute-approved-testcases` không có gì cụ thể để
đối chiếu. **Không suy đoán field nào hiện ở đâu — tra bằng nguồn thật của chính màn Listing/Detail
đó** (mockup/BRD riêng của Listing/Detail, hoặc `Knowledge-Base/Domain-Rules/<module>/_overview.md`
nếu đã có, hoặc UI thật nếu quan sát được) trước khi viết case.

**Cách dựng — 1 bảng cho mỗi feature Create/Edit, dùng lại cho cả case Edit:**

| Field trên form Create/Edit | Xuất hiện ở Listing? | Tên cột/label thật ở Listing | Xuất hiện ở Detail? | Tên field/label thật ở Detail | Transform/format khi hiển thị | Nguồn xác nhận |
|---|---|---|---|---|---|---|
| `Entity Name` | Có | cột "Entity Name" | Có | field "Name" (label khác form!) | verbatim | Listing mockup + Detail mockup |
| `Type` | Có | cột "Type" | Có | field "Type" | verbatim | Listing mockup |
| `Tags` | Có | cột "Tags" (chip, overflow "+N" nếu >3) | Có | section "Tags" (hiện đủ, không overflow) | khác cách hiển thị giữa 2 màn — test riêng từng màn | Listing + Detail mockup |
| `Description` | **Không** | — | Có | field "Description" | — | Detail mockup — Listing không có cột này |
| *(không có field nguồn)* | Có | cột "Risk Score" | Có | field "Risk Score" | **computed, không phải pass-through** — case riêng cho công thức tính, không thuộc case "field hiển thị đúng sau tạo" | domain overview/BRD công thức |

**Quy tắc khi dựng bảng:**
- Mỗi field trên form Create/Edit **phải** có 1 dòng — kể cả khi câu trả lời là "Không xuất hiện ở đâu khác" (field chỉ dùng nội bộ, VD phục vụ logic nhưng không hiển thị). Field không tìm được nơi xuất hiện nào và cũng không có nguồn nào xác nhận "chỉ dùng nội bộ" → `NEED_CONFIRM`, không tự kết luận là bình thường.
- Tên cột/label ở Listing/Detail phải lấy từ **mockup/BRD của chính màn đó** — thường khác tên field trên form Create (case thật ở trên: form ghi "Entity Name", Detail ghi "Name"). Đừng giả định giống tên field gốc.
- Field ở Listing/Detail nhưng **không** tới từ field nào trên form Create (computed/derived, VD Risk Score, Last Seen, Created By) → không thuộc phạm vi case "hiển thị đúng sau khi tạo" — tách thành case riêng theo đúng công thức/nguồn của nó, đừng gộp chung khiến case "tạo xong hiển thị đúng" bị mơ hồ giữa pass-through và computed.
- Đây chính là bảng cross-screen effect ở mức field — nếu module đã có `_overview.md`, đối chiếu bảng này với mục cross-screen sẵn có, đừng làm lại từ đầu nếu overview đã ghi.

## 1. Giao diện

- **CHK-FRM-001 · Medium** — Form hiển thị đúng field, đúng thứ tự, đúng label/placeholder theo mockup.
- **CHK-FRM-002 · High** — Field required có dấu hiệu rõ ràng (*, viền màu khác...) đúng theo mockup.
- **CHK-FRM-003 · Medium** — Field disabled/readonly (nếu có, VD field hệ thống tự sinh) không cho sửa, hiển thị đúng style disabled.
- **CHK-FRM-004 · Medium** (Edit only) — Form Edit mở ra pre-fill đúng giá trị hiện tại của record — không rỗng, không lẫn giá trị của record khác.

## 2. Chức năng — Save / Cancel / Validation

- **CHK-FRM-020 · High** — Lưu với dữ liệu hợp lệ đầy đủ → thành công, message đúng, redirect/đóng modal đúng thiết kế.
- **CHK-FRM-021 · High** — Bỏ trống field required → chặn submit, thông báo lỗi rõ đúng field, không submit một phần.
- **CHK-FRM-022 · High** — Nhập sai format (email, số điện thoại, số...) → validate đúng ngay khi blur field hoặc khi submit (xác nhận đúng timing validate với thiết kế), message lỗi rõ ràng theo field.
- **CHK-FRM-023 · High** — Business constraint (VD giá trị unique, giới hạn số lượng, ràng buộc theo trạng thái khác) → chặn đúng, message business-specific (không phải lỗi kỹ thuật chung chung).
- **CHK-FRM-024 · Medium** — Cross-field rule (field A ảnh hưởng field B — VD chọn Type X thì field Y bắt buộc/field Z bị disable) → đúng theo từng tổ hợp giá trị.
- **CHK-FRM-025 · Medium** — Cancel sau khi đã nhập dữ liệu → có confirm discard, chọn "Huỷ bỏ" thì không lưu, chọn "Ở lại" thì giữ nguyên dữ liệu đã nhập.
- **CHK-FRM-026 · Medium** — Submit khi có lỗi validate ở field không hiện trên viewport hiện tại (form dài, cần scroll) → tự scroll tới field lỗi đầu tiên hoặc có cách khác để user thấy ngay.

## 3. Kết quả & ảnh hưởng (điểm 6-9 của quy trình 9 điểm)

- **CHK-FRM-040 · High** — Sau khi lưu, record xuất hiện/cập nhật đúng trong danh sách — không cần F5 thủ công nếu thiết kế là optimistic update, hoặc list tự refetch. **Expected Result phải liệt kê từng field theo Field Propagation Map ở trên**, không phải 1 dòng chung chung: mỗi cột Listing có field nguồn phải đúng giá trị vừa nhập (đúng transform nếu có, VD overflow "+N" cho Tags), và mỗi field Listing không có trong map (computed) không thuộc phạm vi case này. VD Expected thật đủ để `13-execute-approved-testcases` chạy được: *"Tại Listing, row mới có: cột 'Entity Name' = 'Test 001'; cột 'Type' = 'Server'; cột 'Tags' hiện chip 'prod', 'critical' (2 giá trị, không overflow vì <4)"* — không phải *"record hiện đúng trong list"*.
- **CHK-FRM-041 · High** — Tương tự CHK-FRM-040 nhưng cho màn Detail — Expected liệt kê từng field/section theo đúng tên label thật của Detail (có thể khác tên trên form Create, xem cột "Nguồn xác nhận" của map).
- **CHK-FRM-042 · Medium** — Sau khi lưu, đối chiếu dữ liệu thật ở tầng lưu trữ (API response hoặc DB) khớp với dữ liệu đã nhập cho **từng field** — không chỉ tin theo UI hiển thị lại giá trị vừa nhập (có thể là optimistic render sai với cái thực sự được lưu). Field UI + field API/DB trong cùng 1 case nếu `automation_layers` liệt kê cả `ui,api,db` (xem `canonical-testcase-schema.yaml`).
- **CHK-FRM-043 · Medium** — Nếu tính năng có Activity Log: sau khi tạo/sửa, log entry xuất hiện đúng nội dung, đúng actor (người thực hiện), đúng thời gian.
- **CHK-FRM-044 · Medium** (Edit) — Sau khi sửa, các màn/tính năng khác tham chiếu tới record này phản ánh đúng giá trị mới — dùng lại đúng Field Propagation Map (giá trị mới thay giá trị cũ ở đúng những nơi map đã liệt kê, không đoán thêm màn khác ngoài map).
- **CHK-FRM-045 · Medium** — Field trên form Create nhưng map ghi `NEED_CONFIRM` (không rõ có hiển thị ở đâu không) → có 1 case riêng hỏi thẳng câu này thay vì âm thầm bỏ qua, và test bằng cách quan sát trực tiếp (tạo record, tìm khắp Listing/Detail xem field đó có xuất hiện ở đâu không) để tự trả lời trước khi hỏi BA nếu quan sát đủ rõ.
- **CHK-FRM-046 · High** — **Request thật sự gửi đi đúng** — mở DevTools Network (thao tác tay) hoặc bắt request tại tầng automation khi bấm Save: đúng endpoint/method, và **payload khớp với dữ liệu đã nhập trên form theo đúng field mapping** — đặc biệt field dropdown (gửi đúng ID/value chuẩn, không phải label hiển thị), multi-select (gửi đủ mảng, không chỉ phần tử cuối), ngày giờ (đúng format/timezone BE mong đợi). Đây là case UI hiển thị đúng nhưng vẫn có thể FAIL — không suy ra tự động từ CHK-FRM-020/040.
- **CHK-FRM-047 · High** — **Response trả về đúng** — status code đúng (thành công/lỗi), body chứa đúng field cần thiết để FE dùng tiếp (VD ID mới sinh, timestamp tạo — thiếu field này có thể khiến FE không cập nhật UI đúng dù backend đã lưu thành công). Đây là case tách biệt với CHK-FRM-046 — request đúng không đảm bảo response đúng và ngược lại, cả hai đều cần assert riêng khi `automation_layers`/`oracle_layers` có `API`.

## 4. Phi chức năng

- **CHK-FRM-060 · High** — Double-click nút Submit không tạo 2 record (xem thêm `cross-cutting/concurrency.checklist.md`).
- **CHK-FRM-061 · Low** — Tab key di chuyển qua các field đúng thứ tự trên mockup (top-left → phải → xuống), không nhảy lộn xộn, không bỏ sót field.
