# Template — Checklist review chéo testcase / bug (người review người)

**Khi nào dùng:** theo trigger, không theo lịch — xem `Team/LEAD-PLAYBOOK.md` mục 5.
**Ai review:** người backup của squad đó (vòng tròn Alpha → Squad-B → Sigma → Squad-D → Alpha).
**SLA:** trong 1 ngày làm việc, tối đa **30 phút**. Quá 30 phút chưa xong → trả lại người viết,
**không tự sửa hộ**.

---

## Khi nào BẮT BUỘC review chéo

| Bắt buộc | Không cần |
|---|---|
| Item rủi ro **Rất cao / Cao** | Item rủi ro Thấp (UI polish, đổi nhãn) |
| **Feature AI** (Copilot / Investigator / Triage / UEBA) | Retest bug đã có testcase sẵn |
| **Migration / breaking change** | Sanity check sau build |
| Người viết đang ở **L1** — 100% trong 2 sprint đầu | |
| Trước khi **import TestRail live** | |
| Bug severity **Critical / High** sắp log Jira | |

---

## Checklist 7 điểm — testcase

Rút từ skill `09-review-testcases` + 4 finding thật của DEMO-6065. Đọc lần lượt, không nhảy.

| # | Kiểm tra | Nếu thiếu |
|---|---|---|
| 1 | **Trace về Jira key** — có trong tên file và trong case? | `REWORK` — không trace được thì không tính là coverage |
| 2 | **`EXPECTED_RESULT` có cả tầng UI và tầng logic/dữ liệu?** Không chỉ "hiển thị đúng" | `REWORK` — feature platform này phần lớn là số liệu/state |
| 3 | **Có bước cleanup?** Hoặc ghi rõ "không cần cleanup" và tại sao | `PASS_WITH_COMMENTS` — bài học DEMO-6065: 18/18 case thiếu cleanup |
| 4 | **Có case negative và boundary?** Không chỉ happy path | `REWORK` nếu item rủi ro Cao |
| 5 | **Có case permission/role?** Cả "role nào ĐƯỢC" và **"role nào KHÔNG được xem"** | `REWORK` — gap này bị bỏ sót ở DEMO-6065, chỉ có case "ai được sửa", thiếu "ai không được xem" |
| 6 | **`NEED_CONFIRM` có lý do cụ thể?** Phân biệt rõ *real-data gap* vs *thiếu quyền/config* | `PASS_WITH_COMMENTS` — để trống lý do thì người đọc report không biết đó là giới hạn gì |
| 7 | **Có dùng rule `DRAFT` làm oracle PASS/FAIL không?** | `REWORK` — chỉ `APPROVED` được làm oracle |

### 3 câu hỏi thêm khi item là migration / breaking change

| # | Kiểm tra |
|---|---|
| 8 | Có case cho **dữ liệu cũ** (thế hệ trước) sau khi migrate? |
| 9 | Có case **regression "mất quyền"** — role trước đây làm được, giờ không còn? |
| 10 | Có case **rollback** nếu migration fail? |

> Bài học DEMO-6065: US mô tả whitelist v2 nhưng code tìm thấy là v1 — hai data model khác hẳn. Người
> review phải hỏi "cái này là feature cộng thêm hay là thay thế cái đang chạy?" trước khi review nội
> dung case.

---

## Checklist 5 điểm — bug trước khi log Jira

| # | Kiểm tra | Nếu thiếu |
|---|---|---|
| 1 | Đây là **bug thật**, hay là AC chưa rõ? | AC chưa rõ → hỏi BA, **không log bug** |
| 2 | Đã **tìm duplicate** chưa? Project `SP` rất lớn, dùng chung nhiều team | Tìm trước khi log |
| 3 | Có **evidence** chưa? (screenshot / response JSON / query readback) | Chưa đủ để log |
| 4 | **Expected Result có nguồn** chưa? (AC nào / rule nào) — không phải cảm nhận | `REWORK` |
| 5 | Đã tìm **occurrence thứ 2** ở chỗ khác chưa? | Nếu có → lỗi ở tầng chung. Phải ghi vào bug để dev không fix cục bộ. Bài học DEMO-6925 |

---

## Ghi kết quả review

Thêm **1 dòng** vào cuối file testcase — không tạo file mới:

```
---
REVIEW: PASS_WITH_COMMENTS · reviewer: <alias> · 2026-08-27
- Điểm 3: thiếu cleanup ở TC-05..TC-09 → đã bổ sung quy ước cleanup chung ở đầu file
- Điểm 6: TC-11 NEED_CONFIRM chưa nói rõ là thiếu dữ liệu hay thiếu quyền → người viết bổ sung
```

**Ba giá trị kết quả, không có giá trị thứ tư:**

| Kết quả | Nghĩa | Có review lại? |
|---|---|---|
| `PASS` | Đi luôn | Không |
| `PASS_WITH_COMMENTS` | Sửa rồi đi luôn | **Không** |
| `REWORK` | Phải sửa và review lại | Có |

**Nguyên tắc cho người review:** nêu **vấn đề**, không viết hộ giải pháp. Người viết là người sở hữu
artifact và sở hữu cả việc sửa.
