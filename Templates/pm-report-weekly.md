# Template — Báo cáo QC tuần cho PM

**Cách dùng:** copy phần "TEMPLATE" xuống dưới, điền, gửi PM chiều thứ 6. Mục tiêu: PM đọc trong
**2 phút** và biết ngay 3 điều — có kịp không, rủi ro gì, cần PM quyết gì.

**Quy tắc bắt buộc** (xem `Team/LEAD-PLAYBOOK.md` mục 2):
- Dòng đầu là **1 trạng thái duy nhất**: `ON TRACK` / `AT RISK` / `BLOCKED`.
- Mọi con số coverage phải có **denominator** và phân biệt `DESIGNED` / `REVIEWED` / `AUTOMATED` /
  `EXECUTED` / `PROVEN`. Không gộp thành "% coverage".
- **Không claim zero-bug** — chỉ nói "không phát hiện thêm lỗi trong phạm vi đã test".
- Mục "cần PM quyết": tối đa 3, **mỗi mục phải có đề xuất sẵn của QC**. Đừng đưa vấn đề trống.

---

# TEMPLATE

## Báo cáo QC — Sprint <N> — tuần <YYYY-MM-DD>

**Trạng thái:** `ON TRACK` | `AT RISK` | `BLOCKED`
**Một dòng lý do:** <vì sao ở trạng thái đó — 1 câu, không giải thích dài>
**Sprint:** <N> (<ngày bắt đầu> → <ngày kết thúc>) · còn <X> ngày làm việc
**Người báo cáo:** <Lead>

### 1. Cần PM quyết (tối đa 3)

| # | Việc cần quyết | Ảnh hưởng nếu không quyết | Đề xuất của QC |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 2. Tiến độ theo Squad

| Squad | Item cần test | Đã test | PASS | FAIL | Chưa test được | Bug đang mở |
|---|---:|---:|---:|---:|---:|---:|
| Alpha | | | | | | |
| Squad-B | | | | | | |
| Sigma | | | | | | |
| Squad-D | | | | | | |
| **Tổng** | | | | | | |

> "Chưa test được" tách riêng khỏi FAIL — đó là giới hạn dữ liệu/quyền, không phải lỗi sản phẩm.

### 3. Coverage — nói đúng trạng thái, không gộp thành %

| Trạng thái | Số coverage unit | Ghi chú |
|---|---:|---|
| `DESIGNED` | | đã thiết kế testcase |
| `REVIEWED` | | đã qua review |
| `EXECUTED` | | đã chạy thật |
| `PROVEN` | | đã chạy + có evidence + business readback |
| `NEED_CONFIRM` | | chưa test được — nêu lý do ở mục 5 |
| **Denominator** | | tổng coverage unit theo coverage model |

### 4. Blocker đang chờ ai

| Blocker | Ai bị chặn | Từ ngày | Đang chờ ai | Cần PM hỗ trợ? |
|---|---|---|---|---|
| | | | | |

### 5. Rủi ro còn lại (residual risk)

- <vùng nào chưa được test và vì sao — dữ liệu thật chưa có / thiếu quyền / thiếu AC>

### 6. Khuyến nghị release cho item ở `Ready to deploy`

| Item | Khuyến nghị | Điều kiện thiếu | Ai chấp nhận rủi ro |
|---|---|---|---|
| | `GO` / `GO WITH RISK` / `NO GO` | | |

### 7. Tuần tới làm gì

- <3-5 dòng, cụ thể>

---

# VÍ DỤ ĐIỀN SẴN — tuần 2026-08-27 (Sprint N)

> Số liệu lấy từ 4 file `scope.md` và các output thật đã tạo 26-27/08. Các ô ghi `[cần điền]` là
> chỗ Lead phải bổ sung sau khi có roster và sau khi execute thật.

## Báo cáo QC — Sprint N — tuần 2026-08-27

**Trạng thái:** `AT RISK`
**Một dòng lý do:** Capacity QC thiếu khoảng 2.4× so với khối lượng item đang active, và toàn bộ
automation đang bị chặn vì chưa có tài khoản QC test trên DEV.
**Sprint:** 18 (2026-08-19 → 2026-09-04) · còn 6 ngày làm việc
**Người báo cáo:** QA Lead

### 1. Cần PM quyết

| # | Việc cần quyết | Ảnh hưởng nếu không quyết | Đề xuất của QC |
|---|---|---|---|
| 1 | **Capacity không đủ**: 51 item đang active / 4 QC × 8 ngày = 32 ngày-QC, nhu cầu sơ bộ ~76 ngày-QC | Sẽ có item vào `Ready to deploy` mà chưa được test đủ, rủi ro dồn về cuối sprint | Cắt scope theo rủi ro: chỉ cam kết test đầy đủ nhóm **Rất cao/Cao**; nhóm Thấp rút gọn còn happy path + hiển thị. PM xác nhận danh sách được rút gọn |
| 2 | **~53% item của sprint chưa gán Team field** → không thuộc squad nào, không ai sở hữu | Item bị bỏ sót hoàn toàn khỏi mọi con số và khỏi kế hoạch test | PM/PO gán Team cho các item trong widget "Sprint hiện tại — chưa gán Squad" trên dashboard 10330. QC không tự gán |
| 3 | **Tài khoản QC test riêng trên DEV** — hiện phải dùng tài khoản AD cá nhân, bị MFA + Cloudflare chặn | Automation đứng ở 0%, không thể tiến tới target 70% APP / 100% API đã chốt | PM hỗ trợ đẩy nhanh với team dev. Đây đã là action item chính thức trong "[Enhance] QC workflow" |

### 2. Tiến độ theo Squad

| Squad | Item cần test | Đã test | PASS | FAIL | Chưa test được | Bug đang mở |
|---|---:|---:|---:|---:|---:|---:|
| Alpha | 19 | 0 | 0 | 0 | — | [cần điền] |
| Squad-B | 11 | 0 | 0 | 0 | — | [cần điền] |
| Sigma | 49 | 5 US đã thiết kế TC, 1 US execute thật | — | — | 14 case | 1 (DEMO-6925) |
| Squad-D | 29 | 0 (2 US chờ BA trả lời) | 0 | 0 | — | [cần điền] |
| **Tổng** | **110** (đã gán Team) | **1 US execute thật** | — | — | **14 case** | **1 mới log** |

> Ghi chú: 110 là item **đã gán Team**, không phải toàn bộ sprint — xem mục 1 việc số 2.
> Squad-D có 2 US (DEMO-6377, DEMO-6241) đang `WAITING_BA_RESPONSE`, không tính là chậm do QC.

### 3. Coverage — DEMO-6091 (US duy nhất đã execute thật tuần này)

| Trạng thái | Số coverage unit | Ghi chú |
|---|---:|---|
| `DESIGNED` | 33 | 33 testcase, đã qua review `09` |
| `EXECUTED` | 19 | chạy thật trên DEV qua UI + API |
| `PROVEN` | 11 | có evidence + business readback (D01, P01, B01, B02/B03, B10, B12, B18, F01…) |
| `NEED_CONFIRM` | 14 | 6 case do dữ liệu thật chưa có tình huống · 8 case do QC không có quyền/config |
| `OUT_OF_SCOPE_WITH_OWNER: Dev` | 5 | guardrail/truncate thuộc tầng unit test của dev |
| **Denominator** | **33** | theo `professional-coverage-model.yaml` |

**Automation:** `0%` trên tổng 33 case — không phải chọn lựa, mà do blocker ở mục 1 việc số 3.

### 4. Blocker đang chờ ai

| Blocker | Ai bị chặn | Từ ngày | Đang chờ ai | Cần PM hỗ trợ? |
|---|---|---|---|---|
| Tài khoản QC test riêng trên DEV | Cả team | 2026-08-26 | Team dev | **Có** |
| Swagger / API doc từ DEV | Cả team | 2026-08-26 | Dev team | **Có** |
| 2 US Squad-D chờ BA trả lời công thức metric | Squad-D | 2026-08-26 | BA | **Có** — đã comment Jira 2 lần |
| Security Owner ký Ground Truth cho model AI | QC làm feature AI | 2026-08-26 | Chưa xác định người | **Có** — cần PM chỉ định |
| Ranh giới Red Team/Pentest Squad-B ↔ Squad-D | Lead phân task | 2026-08-26 | PO | Có |

### 5. Rủi ro còn lại

- **14/33 case của DEMO-6091 chưa test được** — 6 case vì tình huống chưa từng xảy ra trong dữ liệu
  thật trên DEV (authentication, retry thành công, batch partial), 8 case vì QC không có quyền/config
  để tạo tình huống. Đây là giới hạn dữ liệu và quyền, không phải QC làm thiếu.
- **Data-model gap chưa xác nhận được:** `error_summary` chỉ tồn tại ở cấp execution, không lặp theo
  từng node — hành vi khi 1 execution có nhiều node fail đồng thời chưa kiểm chứng được vì mọi mẫu
  dữ liệu thật quét được đều chỉ có 1 node fail.
- **Automation 0%** → mọi regression hiện tại là manual. Sprint càng nhiều item, rủi ro regression
  lọt càng cao.
- **Chưa có cơ chế review người-review-người** đang được áp dụng (vừa thiết kế, chưa chạy) → hiện
  chất lượng artifact phụ thuộc từng cá nhân.

### 6. Khuyến nghị release cho item ở `Ready to deploy`

| Item | Khuyến nghị | Điều kiện thiếu | Ai chấp nhận rủi ro |
|---|---|---|---|
| DEMO-6091 | `GO WITH RISK` | 14/33 case chưa verify được (thiếu dữ liệu thật + thiếu quyền). Bug DEMO-6925 đã log, chưa `Closed` | [cần PM/PO xác nhận] |
| 13 item 🔴 còn lại | [cần điền sau khi execute] | | |

### 7. Tuần tới làm gì

- Execute 13 item 🔴 còn lại, ưu tiên nhóm rủi ro Rất cao/Cao trước (cụm bug `[BE][Pentest]` phân quyền).
- 1-1 với 4 QC để chấm level và chốt roster → phân việc theo năng lực từ sprint sau.
- Theo dõi DEMO-6925 (bug đã log) tới khi `Closed`, không dừng ở `Resolved`.
- Nhắc BA trả lời 2 US Squad-D; nếu tới thứ 3 chưa có → escalate lên PO.
- Áp nhịp daily async + daily Lead scan cho cả team.
