# Lead Playbook — vận hành team QC Example-Project

**Cho:** QA Lead (vai **Test Lead T5/T6** theo "QA Career Path" — vận hành dự án, **không phải**
QA Manager quy hoạch phòng ban).
**Bối cảnh:** 4 QC / 4 Squad / 1 sprint chung 2-2.5 tuần / release liên tục không lịch trình.
**Cập nhật:** 2026-08-27 · Trạng thái: DRAFT — chưa chạy thật lần nào, số calibration cần validate
sau 1 sprint.

Playbook này giải quyết đúng 6 gap của vai Test Lead: nhịp review, báo cáo PM, ước lượng effort,
phân việc theo năng lực, review người-review-người, go/no-go, coaching.

---

## 1. Nhịp review định kỳ

Nguyên tắc thiết kế: **4 người thì không họp nhiều.** Async là mặc định, họp chỉ khi cần quyết định.

| Nhịp | Khi nào | Ai | Thời lượng | Làm gì |
|---|---|---|---|---|
| **Daily async** | Trước 10h hằng ngày | Mỗi QC | 5 phút | Cập nhật `scope.md` + 3 dòng lên channel: hôm qua xong gì / hôm nay làm gì / blocker gì. **Không họp** |
| **Daily Lead scan** | Sau 10h | Lead | 10 phút | Mở dashboard 10330, soát 4 thứ (checklist dưới) |
| **Mid-sprint checkpoint** | Giữa sprint | Cả team | 30 phút | Soát tiến độ vs còn lại, quyết cắt scope nếu cần |
| **Weekly PM report** | Chiều thứ 6 | Lead | 30 phút | Gửi theo `Templates/pm-report-weekly.md` |
| **1-1 coaching** | 2 tuần/lần/người | Lead + 1 QC | 30 phút | Xem mục 7 |
| **Sprint close** | Ngày cuối sprint | Cả team | 60 phút | Report cuối sprint (skill `33`) + retro 3 câu |

### Daily Lead scan — soát đúng 4 thứ, 10 phút

1. **Item 🔴 nào chưa có testcase?** → người phụ trách bị chặn hay đang chậm?
2. **Item nào chờ BA > 1 ngày?** → Lead vào nhắc trực tiếp, không để QC tự chờ.
3. **Bug nào `Resolved` mà chưa `Closed`?** → nhắc dev. Ở project này `Resolved` KHÔNG phải đã đóng.
4. **Widget "Sprint hiện tại — chưa gán Squad"** → có item mới rơi vào vùng không ai sở hữu không?

### Mid-sprint checkpoint — 4 câu hỏi, quyết ngay tại chỗ

1. Còn bao nhiêu item 🔴 chưa test? Với capacity còn lại có kịp không? (tính theo mục 3)
2. Item nào phải **cắt khỏi scope sprint này** — quyết ngay, báo PM trong report thứ 6.
3. Ai đang quá tải, ai còn dư → có đảo việc không?
4. Blocker nào Lead phải escalate lên QC Engineering Manager / PO / tech lead?

### Retro 3 câu (sprint close, 15 phút)

1. Cái gì tuần này làm chậm mình nhất? Chọn đúng **1** cái, sửa ở sprint sau.
2. Có bug nào lọt ra `Ready to deploy` / PROD mà lẽ ra mình bắt được không? Vì sao lọt?
3. Có kết luận nào của mình sai trong sprint này? **Không phạt** — ghi lại thành bài học
   (xem `WORKING-AGREEMENTS.md` mục 5: sửa mà không xoá lịch sử).

---

## 2. Báo cáo PM

Dùng `Templates/pm-report-weekly.md` — 1 trang, PM đọc trong 2 phút.

**Ba nguyên tắc bắt buộc:**

1. **Mở đầu bằng 1 trạng thái duy nhất:** `ON TRACK` / `AT RISK` / `BLOCKED`. PM cần biết ngay dòng đầu.
2. **Mọi con số coverage phải có denominator**, phân biệt `DESIGNED` / `REVIEWED` / `AUTOMATED` /
   `EXECUTED` / `PROVEN`. Không gộp thành "% coverage".
3. **Không claim zero-bug** — chỉ nói "không phát hiện thêm lỗi trong phạm vi đã test".

**Phần PM quan tâm nhất, đặt lên trên:** rủi ro cần PM **quyết**, tối đa 3 mục, mỗi mục kèm đề xuất
sẵn của QC. Đừng đưa vấn đề mà không đưa đề xuất.

---

## 3. Ước lượng effort khi không có story point

Jira project `SP` không có story point/effort estimate. **Không chờ có** — dùng thang riêng của QC,
tính theo **số testcase và độ rõ của AC**, đơn vị **ngày-QC**.

| Size | Điều kiện | Effort QC |
|---|---|---|
| **S** | ≤ 5 TC · AC rõ · 1 màn hình · không cần data đặc biệt | **0.5 ngày** |
| **M** | 6-15 TC · AC rõ · nhiều màn hình hoặc có API | **1-2 ngày** |
| **L** | 16-30 TC · hoặc có state machine / permission matrix | **3-4 ngày** |
| **XL** | > 30 TC · hoặc feature AI · hoặc migration/breaking change | **5+ ngày — phải chia nhỏ** |

**Hệ số nhân, cộng dồn:**

| Điều kiện | Nhân |
|---|---|
| Chưa có AC — phải tìm 3 kênh + hỏi BA | **×1.5** |
| Feature AI (Copilot / Investigator / Triage / UEBA) | **×1.5** |
| Migration / breaking change — phải test cả regression "mất quyền" và dữ liệu cũ | **×1.5** |
| Chưa có tài khoản/quyền để tạo tình huống | **×1.3** + ghi `NEED_CONFIRM` ngay từ đầu |

**Calibration từ dữ liệu thật của chính team** (không phải số bịa):

| Item thật | Số TC | Size tính ra | Thực tế đã xảy ra |
|---|---|---|---|
| DEMO-6065 (Whitelist v2) | 18 TC | **L** × 1.5 migration ≈ 5 ngày | Khớp — chạy `01→04→06→09` đã mất phần lớn 1 ngày chỉ để **thiết kế**, chưa execute |
| DEMO-6091 (AI tóm tắt lỗi playbook) | 33 TC | **XL** × 1.5 AI ≈ 7 ngày | Khớp — deep-dive tay mất trọn 1 ngày, vẫn còn 14 case `NEED_CONFIRM` |

**Capacity chuẩn: 1 QC / sprint 2 tuần = 8 ngày test thật** (10 ngày làm việc − 2 ngày họp, support,
regression, việc phát sinh). Không tính 10.

### Phép tính capacity Sprint N — con số phải đưa cho PM

```
Item đang active (đã gán Team):   14 🔴 cần test ngay  +  37 🟡 đang dev  =  51 item
Nhân lực:                          4 QC × 8 ngày                          =  32 ngày-QC

Giả định trung bình size M (1.5 ngày):  51 × 1.5 = 76.5 ngày-QC cần
                                         → thiếu khoảng 2.4× capacity
```

> ⚠️ **Phép tính sơ bộ, phải validate 1 sprint trước khi dùng làm cam kết.** Ba điểm chưa chắc:
> (1) không phải mọi item đều cần test đầy đủ — item rủi ro Thấp rút gọn được; (2) 51 item chỉ là
> item **đã gán Team**, còn ~53% item sprint chưa gán nên số thật có thể cao hơn; (3) chưa có dữ
> liệu thời gian thật của 4 người.
>
> Nhưng ngay cả với sai số lớn, **kết luận "capacity không đủ" là chắc chắn** — và đó là thứ PM cần
> biết sớm, không phải cuối sprint.

---

## 4. Phân việc theo đúng năng lực

### Bước 1 — Biết level của 4 người (1-1 30 phút/người, làm tuần này)

Dùng đúng 5 competency đã có trong `Templates/member-profile.yaml`:

| Competency | Câu hỏi xác định level |
|---|---|
| `requirements_and_business_analysis` | Tự tìm được BRD qua 3 kênh chưa? Phát hiện được AC thiếu/mâu thuẫn chưa? |
| `functional_test_design` | Viết được case có cả negative / boundary / permission chưa, hay chỉ happy path? |
| `api_testing` | Đọc response JSON và readback dữ liệu chưa, hay chỉ xem HTTP status? |
| `bug_hunting_defect_and_retest` | Tự tìm được occurrence thứ 2 của 1 bug chưa? Phân biệt bug vs AC chưa rõ chưa? |
| `ui_e2e_and_automation` | Đọc/sửa được Playwright script chưa? Chạy được suite chưa? |

Chấm L0-L5 theo mô tả trong **"QA Career Path"** (trang <QC-SPACE>, người phụ trách career path) — **không tự nghĩ thang mới**.

**Quy tắc chống lạm phát level:** self-assessment chỉ là điểm khởi đầu. Lead chỉ xác nhận 1 level
khi thấy **1 artifact thật** chứng minh (testcase đã review, bug đã log đúng chuẩn, script đã chạy).
Ghi vào `Team/Members/<alias>.yaml` → `competencies.*.evidence`. Đúng theo `promotion_policy`:
người tự chấm không tự nâng.

### Bước 2 — Luật phân việc

| Loại item | Giao cho |
|---|---|
| Rủi ro **Rất cao / Cao** (permission, ASM Phase 1, AI Triage, bug `[BE][Pentest]`) | Người **L3+** ở competency tương ứng |
| **Feature AI** | Người **L2+** VÀ đã đọc 2 trang methodology AI |
| Size **L / XL** | Không giao cho người L1. Nếu buộc phải giao → **review chéo 100%** (mục 5) |
| **Migration / breaking change** | Người **L3+** — phải nghĩ ra được testcase regression "mất quyền", thứ không có trong AC |
| Size **S / M**, rủi ro Thấp | Ai cũng được — đây là vùng để người L1 lên L2 |

### Bước 3 — Cấu trúc phủ squad với 4 người

**Mỗi người: 1 squad chính + 1 squad backup**, xếp vòng tròn:

```
QC-1   chính: Alpha       backup: Squad-B
QC-2   chính: Squad-B     backup: Sigma
QC-3   chính: Sigma       backup: Squad-D        ← Sigma 49 item, nặng nhất
QC-4   chính: Squad-D     backup: Alpha
```

Lý do chọn vòng tròn (không phải cặp đôi): **backup cũng chính là người review chéo** (mục 5) — một
cấu trúc giải hai việc, và mỗi người dần biết domain của 2 squad thay vì 1.

⚠️ Sigma nặng gấp ~4.5× Squad-B (49 vs 11 item). Không chia 1-1 phẳng được — Lead phải chủ động đảo
việc ở mid-sprint checkpoint, hoặc đưa vào báo cáo PM như một rủi ro capacity.

---

## 5. Review người-review-người

Skill `09` review output của AI. **Không thay được người review người** — vì `09` không biết domain
squad, không biết cái gì PO vừa đổi ý hôm qua.

### Review theo TRIGGER, không theo lịch

4 người không đủ thời gian review tất cả. Chỉ review khi:

| Bắt buộc review chéo | Không cần review |
|---|---|
| Item rủi ro **Rất cao / Cao** | Item rủi ro Thấp (UI polish, đổi nhãn) |
| **Feature AI** | Retest bug đã có testcase sẵn |
| **Migration / breaking change** | Sanity check sau build |
| Người viết đang ở **L1** — review 100% trong 2 sprint đầu | |
| **Trước khi import TestRail live** | |
| Bug severity **Critical / High** sắp log Jira | |

**Ai review ai:** người backup của squad đó (vòng tròn ở mục 4 bước 3).

**SLA:** review trong **1 ngày làm việc**, tối đa **30 phút/lần**. Quá 30 phút mà chưa xong nghĩa là
artifact có vấn đề cấu trúc — **trả lại người viết, không tự sửa hộ**.

**Checklist:** `Templates/artifact-review-checklist.md` — 7 điểm, rút từ skill `09` + 4 finding thật
của DEMO-6065.

**Kết quả review** chỉ có 3 giá trị:

| Kết quả | Nghĩa |
|---|---|
| `PASS` | Đi luôn |
| `PASS_WITH_COMMENTS` | Sửa rồi đi luôn, **không** review lại |
| `REWORK` | Phải sửa và review lại |

Ghi 1 dòng vào cuối file testcase, không tạo file mới.

---

## 6. Go/no-go khi release liên tục không lịch trình

**Vấn đề thật:** release liên tục, không có mốc release cố định → **không thể có 1 gate cho cả
release**. Đừng cố dựng lịch release — đó không phải quyền của QC.

**Cách giải: gắn gate vào từng item khi vào `Ready to deploy`.** Mỗi item là 1 quyết định nhỏ, không
cần thêm cuộc họp nào.

### Điều kiện tối thiểu để QC nói "được deploy" (per item)

| # | Điều kiện |
|---|---|
| 1 | Toàn bộ TC priority **High** đã `EXECUTED`, không còn FAIL chưa xử lý |
| 2 | Bug severity **Critical / High** của item đã **`Closed`** — không phải `Resolved` |
| 3 | Smoke vùng liên quan **PASS** |
| 4 | Mỗi kết luận có **evidence path** |
| 5 | Nếu là migration → đã test **dữ liệu cũ** và **rollback** |

### QC không quyết định release — QC ra 1 trong 3 khuyến nghị

| Khuyến nghị | Khi nào | Bắt buộc kèm |
|---|---|---|
| **GO** | Đủ 5 điều kiện | — |
| **GO WITH RISK** | Thiếu điều kiện nhưng business cần ra | Thiếu gì · rủi ro cụ thể · **tên người chấp nhận rủi ro** |
| **NO GO** | Có FAIL ở TC High, hoặc bug Critical chưa đóng | Lý do cụ thể + cần gì để chuyển thành GO |

Khớp với 3 phương án PA1/PA2/PA3 của template report org-wide. **Người quyết cuối cùng là PM/PO,
không phải QC** — QC đưa dữ liệu và khuyến nghị.

**Ghi ở đâu:** 1 comment trên chính item Jira, theo `Templates/go-no-go-record.md`. Không tạo tài
liệu riêng, không cần họp.

---

## 7. Coaching và tháo gỡ blocker

### 1-1 30 phút / 2 tuần / người

4 người = 4 buổi = 2 tiếng/sprint. Khả thi, đừng bỏ.

**Cấu trúc cố định 4 phần** — đừng để thành buổi báo cáo tiến độ, tiến độ đã có ở daily async:

1. **1 artifact người đó làm 2 tuần qua** — đọc cùng nhau, hỏi "vì sao chọn cách này".
2. **1 điều làm tốt** — cụ thể, không chung chung.
3. **1 điều cần sửa** — chỉ 1, kèm cách sửa cụ thể.
4. **Level đang ở đâu so với target** — theo "QA Career Path", và cần artifact gì để lên level tiếp.

### Blocker — cơ chế "không tự ngồi mò"

| Quy tắc | Chi tiết |
|---|---|
| **Chặn > 4 tiếng phải báo** | Không tự mò tiếp. Báo lên channel, không chờ tới daily |
| **Lead sở hữu blocker** | Blocker vào bảng theo dõi dưới đây, **Lead** là người đi gỡ, không phải QC |
| **Blocker > 2 ngày → escalate** | Lên QC Engineering Manager / PO / tech lead tuỳ loại |
| **Blocker lặp lại lần 2** | Không gỡ lẻ nữa — phải sửa quy trình hoặc tài liệu, ghi vào `CURRENT_STATE.md` |

### Bảng theo dõi blocker (Lead cập nhật, đưa vào báo cáo PM thứ 6)

| Blocker | Ai bị chặn | Từ ngày | Đang chờ ai | Lead đã làm gì |
|---|---|---|---|---|
| Chưa có tài khoản QC test trên DEV — chặn toàn bộ automation | Cả team | 2026-08-26 | Team dev (PIC: Lead) | Là action item chính thức trong "[Enhance] QC workflow" |
| Chưa có swagger/API doc — chặn target API 100% | Cả team | 2026-08-26 | Dev team | Chưa trao đổi |
| Chưa có Security Owner ký Ground Truth — chặn đánh giá accuracy model AI | QC làm feature AI | 2026-08-26 | Chưa có người | Chưa escalate |

---

## 8. Việc Lead phải làm, xếp theo thứ tự

| # | Việc | Khi nào | Chặn cái gì nếu không làm |
|---|---|---|---|
| 1 | 1-1 với 4 QC → chấm level → điền roster (mục 4 bước 1) | **Tuần này** | Chặn toàn bộ mục 4 và 5 — không phân việc và không xếp cặp review được |
| 2 | Đóng blocker **tài khoản QC test DEV** | **Tuần này** | Chặn automation, chặn target 70/30, chặn lộ trình ở trang Confluence 05 |
| 3 | Chạy báo cáo PM đầu tiên | **Thứ 6 này** | PM chưa biết vấn đề capacity ~2.4× |
| 4 | Áp nhịp daily async + daily Lead scan | Ngay | Không phát hiện sớm item chậm |
| 5 | ~~Chốt repo GitLab, push workspace~~ — **XONG 2026-08-27**, repo `<QC-GROUP>/qa-workflow-agentskill-main` | — | — |
| 6 | Validate thang effort mục 3 sau 1 sprint | Sau 2026-09-04 | Con số ước lượng vẫn là giả định |
