# <Module Name> — Domain Overview

> Copy this file to `Knowledge-Base/Domain-Rules/<module>/_overview.md` (one per module) and fill it
> in from real, confirmed sources (BRD/PRD, Confluence, live code) before treating it as anything
> more than a DRAFT. Read it — and keep it updated — before designing or reviewing ANY feature in
> this module, even one no atomic rule has been extracted for yet. It does not replace the atomic
> rule files in this same folder (`<module>-*.yaml`) — those still carry the specific, sourced
> business rule; this file only prevents missing a cross-screen effect that no single story's rule
> extraction would surface. See `governance/knowledge-policy.yaml`'s `module_overview_artifact`
> section for the governance rules this file follows.

## Meta
- module: "<module name — match the name used in Jira Team/Component and Config/modules.yaml if this project has one>"
- status: DRAFT
- sources: ["<BRD/PRD/Confluence page(s) this was built from>"]
- verified_at: "<date this was last checked against a real source>"
- owner: NEED_CONFIRM

---

## Tổng quan module

<2-4 câu: module này giải quyết bài toán nghiệp vụ gì, ai dùng (persona/role), tại sao nó tồn tại.>

**Menu/màn chính:**
- **<Menu 1>** — <1 dòng mục đích>
- **<Menu 2>** — <1 dòng mục đích>
- **<Menu 3>** — <1 dòng mục đích>

---

## Menu 1: <Tên menu>

### Mục đích nghiệp vụ
<Ai vào đây làm gì, để giải quyết bài toán gì.>

### Các khái niệm chính
- **<Khái niệm A>**: <định nghĩa ngắn>
- **<Khái niệm B>**: <định nghĩa ngắn>

### Logic nghiệp vụ cần nhớ
- <Quy tắc ngầm hay bị hiểu sai — điều mà một US/BRD đơn lẻ thường không nhắc lại vì coi là "hiển nhiên với người trong module".>
- <Ví dụ dạng: "X tăng khi Y xảy ra, giảm khi Z xảy ra". "Tắt A không xoá dữ liệu cũ, chỉ ngừng tạo mới". "Sửa ngưỡng chỉ áp dụng từ thời điểm lưu, không hồi tố".>

### Liên kết sang màn khác
- <Hành động ở đây ảnh hưởng gì ở menu khác — 1 dòng mỗi liên kết.>

---

## Menu 2: <Tên menu>

<Lặp lại cấu trúc Menu 1.>

---

## Liên kết logic giữa các menu (Cross-Screen Logic)

Bảng này là phần giá trị nhất của file — dùng để tự hỏi "feature tôi đang test có động vào cái gì
ở màn khác không" mà không phải nhớ hết bằng trí nhớ.

| Hành động | Xảy ra ở | Kiểm tra thêm ở |
|---|---|---|
| <Hành động 1> | <Menu nguồn> | <Menu bị ảnh hưởng> — <ảnh hưởng cụ thể là gì> |
| <Hành động 2> | <Menu nguồn> | <Menu bị ảnh hưởng> — <ảnh hưởng cụ thể là gì> |

---

## Khi viết/review testcase cho feature trong module này — checklist tự hỏi

1. Feature này tạo/thay đổi **<thực thể chính của module>** nào? → Kiểm hiệu ứng ở <menu tương ứng>.
2. Feature này liên quan tới **<khái niệm/rule engine chính, nếu có>** nào? → Kiểm khi nó bật/tắt/đổi.
3. Feature này đọc **dữ liệu từ Settings/cấu hình** không? → Kiểm khi cấu hình đó thay đổi.
4. Feature này thay đổi **trạng thái** của một thực thể → Kiểm trạng thái phản ánh đúng ở mọi màn liên quan, không chỉ màn đang sửa.
5. <Câu hỏi đặc thù thêm cho module này, nếu có.>
