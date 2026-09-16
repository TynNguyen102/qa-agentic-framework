# Defect Verification Policy

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Quan hệ với cái đã có:** `Projects/<ACTIVE_PROJECT>/Config/bug-basis-profile.yaml` đã định nghĩa
> 7 confirmation gate + 6 classification và **đang hoạt động**. Tài liệu này **không thay thế** file đó —
> nó bổ sung đúng thứ còn thiếu (gap #26): **ngưỡng confidence** để quyết định log Jira hay chờ người.

## 1. Luật gốc

**Test FAIL ≠ bug.** Không tạo Jira issue ngay khi có FAIL. Mọi FAIL đi qua `39-issue-triage` trước.

## 2. Bảy cổng xác nhận (đã có, giữ nguyên)

Nguồn: `bug-basis-profile.yaml` → `confirmation_gates`. Tóm tắt:

1. Expected behavior có nguồn có thẩm quyền của **đúng project này**, hoặc đánh dấu `NEED_CONFIRM`.
2. Actual behavior tái hiện được từ state có kiểm soát (ghi build, env, role, data).
3. Khác biệt expected↔actual **quan sát được** và có evidence.
4. Có readback ở lớp có thẩm quyền (UI/API/DB/event/audit/downstream).
5. Đã **loại trừ** lỗi môi trường, lỗi test data, lỗi automation.
6. Đã nêu impact (business/user/security/data/operational) và phạm vi.
7. Đã kiểm tra duplicate trên Jira khi có quyền truy cập.

## 3. Ngưỡng confidence (phần MỚI)

Dùng `Config/QA-Agent/schemas/confidence-report.schema.yaml`, `subject_type: DEFECT_DRAFT`.

| Band | Điều kiện | Hành động |
|---|---|---|
| **HIGH** (21–24) | 7/7 cổng đạt, `evidence_state: CONFIRMED`, không conflict mở | Được phép log Jira sau khi qua **G9 (live write)** |
| **MEDIUM** (15–20) | 7/7 cổng đạt nhưng có `limiting_factors` (vd chưa readback đủ lớp, chưa check duplicate do mất quyền) | Log được, **bắt buộc** ghi `limiting_factors` vào mô tả bug |
| **LOW** (8–14) | Có cổng chưa đạt, hoặc `failure_classification: UNKNOWN` | **KHÔNG log Jira.** Tạo *suspected defect* local + **G5** |
| **UNUSABLE** (0–7) | Không có nguồn expected, hoặc có conflict `BLOCKER` mở | Không log, không publish. Route ngược về `42` hoặc `01` |

**Luật cứng:**
- `execution_evidence ≤ 1` (INFERRED/ASSUMED) ⇒ **không bao giờ** log Jira. Đọc code/spec/MR không phải bằng chứng runtime.
- `conflict_status = 0` (có BLOCKER) ⇒ band `UNUSABLE`, bất kể các thành phần khác.
- `SEARCH_BLOCKED` khi tìm duplicate ⇒ **không được** kết luận "không có duplicate"; hạ band xuống `MEDIUM` và ghi rõ.
- Agent **không được tự nâng band**. Nâng band cần bằng chứng mới, không phải đánh giá lại.

## 4. Suspected defect (band LOW)

Khi chưa đủ để log Jira, vẫn phải lưu lại — không được im lặng bỏ qua:

- Tạo `Projects/<ACTIVE_PROJECT>/Defects/FINDING-<YYYYMMDD>-<NNN>/manifest.yaml`
- Thêm một dòng vào `Projects/<ACTIVE_PROJECT>/Defects/INDEX.md`
- Trạng thái: `SUSPECTED_AWAIT_REVIEW`
- Ghi rõ **thiếu gì** để lên được band cao hơn

Đây chính là quy tắc "log hai nơi" mà repo đang dùng — giữ nguyên.

## 5. Phân loại trước khi gán cho sản phẩm

Từ `test-result.schema.yaml` → `failure_classification`. Chỉ `PRODUCT_DEFECT` mới được route sang `36-log-jira-defect`:

| Classification | Route tới |
|---|---|
| `PRODUCT_DEFECT` | `36-log-jira-defect` (sau ngưỡng ở §3) |
| `ENVIRONMENT_ISSUE` | Báo owner môi trường, **không** tạo bug sản phẩm |
| `TEST_DATA_ISSUE` | `10-generate-test-data` |
| `AUTOMATION_ISSUE` | `11-generate-automation-script` sửa script; không đổ cho sản phẩm |
| `REQUIREMENT_CONFLICT` | `42-document-conflict-analysis` → G1 |
| `UNKNOWN` | Điều tra thêm hoặc **G5**. **Không** được coi là `PRODUCT_DEFECT` |

## 6. Nội dung bug bắt buộc

Nguồn format: `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml`
(hiện hành: `jira_rich_format_2026_09_15`, canonical ví dụ DEMO-7516).

Bắt buộc có: summary theo `title_format`, description đủ 9 mục, precondition, steps, test data,
expected + **nguồn**, actual, environment, build/version, evidence (đã redact), severity,
priority đề xuất, component, labels, requirement/testcase liên quan, kết quả check duplicate,
cờ regression.

**Liên kết bắt buộc:** mọi Bug phải có `Relates → Story`.
⚠️ Hook `.claude/hooks/pre_jira_write_gate.py` hiện **chỉ cảnh báo**, không chặn luật này — nên nó
dễ bị quên. Khi chưa rõ Story nào, **hỏi Lead trước khi log**, không log rồi sửa sau.

## 7. Điều tuyệt đối không làm

- Không log Jira từ suy luận code/spec/MR mà không có bằng chứng runtime.
- Không dùng retry để làm biến mất một FAIL thật.
- Không gộp hai issue chỉ vì trùng thông báo lỗi — phải so business invariant, state, root cause.
- Không tự transition/assign/close issue của người khác khi chưa được yêu cầu.
- Không đính evidence còn `PENDING_REDACTION`.
