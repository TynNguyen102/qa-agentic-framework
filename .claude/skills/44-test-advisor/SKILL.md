---
name: 44-test-advisor
description: Đề xuất checklist loại test cần chạy cho một ticket/US, kèm lý do, rủi ro được xử lý, ước lượng công, khả năng tự động hoá, công cụ và test data cần có — để người dùng tick chọn phạm vi. Dùng sau phân tích risk, đặc biệt khi người yêu cầu chưa biết cần test những gì, hoặc khi cần chốt phạm vi tối thiểu / khuyến nghị / sâu.
---

# Test Advisor

> **Tóm tắt:** Biến risk thành một **checklist người tick được**, kèm lý do từng mục — để tester mới không phải tự đoán cần test gì, và tester có kinh nghiệm chốt phạm vi nhanh.

Đây là bước làm cho workflow **dùng được bởi người mới** (gap #6 và #33). Router vẫn chọn skill,
nhưng advisor làm cho lựa chọn đó **nhìn thấy được và sửa được** trước khi tốn công chạy.

## Input gate

- Output `43-risk-and-change-impact` (`risk_id`, `impact_map`, `overall_risk_level`)
- Output `01-review-requirements`
- Conflict đang mở từ `42` (conflict `BLOCKER` phải hiện trong checklist như mục bị chặn)

Chưa có risk ⇒ chạy `43` trước. **Không** tự chấm risk trong skill này.

## Ba mức phạm vi

Luôn đề xuất đủ **ba** mức, để người dùng chọn có ý thức:

| Mức | Nghĩa | Khi nào hợp lý |
|---|---|---|
| `MINIMUM` | Chỉ baseline bắt buộc — bỏ bớt là mất kiểm soát | Hotfix gấp, risk LOW, đã có regression tự động mạnh |
| `RECOMMENDED` | Mặc định cho risk MEDIUM/HIGH | Phần lớn US |
| `DEEP` | Thêm deep/exploratory/bug-hunt/security | risk HIGH/VERY_HIGH, module có lịch sử defect, luồng tới hạn |

## Checklist đề xuất (28 loại)

Với mỗi loại, đánh dấu một trong: **BẮT BUỘC** (baseline) · **KHUYẾN NGHỊ** · **KHÔNG CẦN** (kèm lý do) · **BỊ CHẶN** (kèm blocker).

Functional · Positive · Negative · Boundary · Validation · UI behavior · Visual regression ·
UX heuristic · Responsive · Accessibility · API · Database · Integration · End-to-end ·
Role & permission · Security · Performance · Reliability · Compatibility · Localization ·
Recovery · Data integrity · Regression · Smoke · Exploratory · Deep test · Bug hunt ·
AI/LLM evaluation *(chỉ khi sản phẩm có AI trong luồng này)*

## Mỗi đề xuất phải trả lời đủ 7 câu

Không được chỉ liệt kê tên loại test:

1. **Vì sao cần** — dẫn tới `risk_id` hoặc AC/rule cụ thể, không nói chung chung
2. **Rủi ro được xử lý** — nếu bỏ mục này thì cái gì có thể lọt
3. **Ước lượng công** — S / M / L, kèm căn cứ (số case, số role, số endpoint)
4. **Tự động hoá được không** — `AUTOMATABLE` / `MANUAL_ONLY` / `HYBRID` + lý do
5. **Công cụ đề xuất** — theo `Config/QA-Agent/tool-adapters.yaml` khi có, không hard-code
6. **Test data cần gì** — loại data, role, khối lượng; có cần dữ liệu nhạy cảm không (⇒ cổng **G4**)
7. **Cần quyền / môi trường đặc biệt không** — assurance level, có cần cổng **G3** không

## Luật về việc bỏ test

Người dùng được bỏ tick, nhưng:

- **Baseline** (mục `BẮT BUỘC`) phải được đánh dấu rõ là baseline khi trình bày.
- **Không được bỏ im lặng** các mục thuộc nhóm zero-tolerance: security, permission/authorization,
  data integrity, và mọi mục gắn risk `VERY_HIGH`.
- Bỏ một mục quan trọng ⇒ ghi lại: **ai** chấp nhận rủi ro, **lý do**, **rủi ro còn lại** — đây là cổng **G2**.
- Agent **không được** tự bỏ mục để tiết kiệm thời gian/token, và **không được** tự tick thay người dùng.

## Output contract

Theo `skill-io.schema.yaml` `universal_output_envelope`, kèm một bảng checklist:

| Loại test | Mức | Vì sao cần | Rủi ro xử lý | Effort | Tự động? | Công cụ | Test data | Quyền/Env |
|---|---|---|---|---|---|---|---|---|

Cộng thêm:

- Ba phương án `MINIMUM` / `RECOMMENDED` / `DEEP`, mỗi phương án nêu rõ **cái gì không được test** và rủi ro còn lại
- Danh sách mục `BỊ CHẶN` + blocker + ai gỡ được
- Câu hỏi chốt gọn cho người dùng (chọn phương án nào, có bỏ mục nào không)
- `evidence_state`

## Trình bày cho người mới

- Ngôn ngữ mô tả **hành vi người dùng**, không phải tên kỹ thuật nội bộ.
- Mỗi loại test kèm **một câu** giải thích nó tìm ra lỗi kiểu gì.
- Nêu thứ tự nên chạy (cái nào chặn cái nào).
- Nói rõ cái gì agent làm được, cái gì cần người làm tay.

## Safety gate

- Không đề xuất security/performance/destructive test như thể chạy được ngay — luôn kèm điều kiện cổng **G3**.
- Không đề xuất dùng dữ liệu thật/PII mà không nêu cổng **G4**.
- Không hứa coverage 100% ở bất kỳ phương án nào, kể cả `DEEP`.
- Không đề xuất test trên PROD (`TEST_POLICY: FORBIDDEN` trong `qa-config.yaml`).
- Checklist là **đề xuất**; phạm vi cuối do người dùng chốt.

## Next recommended

- Người dùng đã chốt phạm vi → `04-high-level-test-design`
- Phạm vi chỉ có API → `08-generate-api-testcases`
- Có mục AI/LLM → `40-ai-output-testing`
- Có mục bị chặn bởi conflict → quay lại `42` / cổng **G1**
- Người dùng bỏ mục quan trọng → ghi nhận cổng **G2** trước khi đi tiếp
