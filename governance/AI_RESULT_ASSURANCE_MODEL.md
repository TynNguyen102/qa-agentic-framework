# AI Result Assurance Model

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> **Câu hỏi tài liệu này trả lời:** "Kết quả agent sinh ra đáng tin tới đâu?" — và trả lời **không**
> bằng một con số "AI đúng X%".

## 1. Vì sao không dùng một con số phần trăm

Muốn nói "AI đúng 95%" thì phải có **evaluation dataset có ground truth** đủ lớn và đại diện.
Repo này hiện có `evals/qa-agent/eval-suite.yaml` với 33 case (11 zero-tolerance + 22 P0) —
đủ để làm **regression gate cho hành vi**, **không đủ** để tuyên bố một tỉ lệ chính xác.

Ngoài ra `eval-suite.yaml` tự ghi trong `known_limitations`: đây là *behavioral eval*, không phải
black-box eval, vì subagent vẫn đọc được source/config thật (chỉ giấu `expected_behavior`).

⚠️ **Baseline hiện đang stale:** lần chạy duy nhất là `2026-07-19`. Router và config đã đổi nhiều lần
kể từ đó mà chưa chạy lại — chính file eval khuyến nghị chạy lại mỗi khi router/config đổi lớn.
Đây là gap #35 và là việc P0.

## 2. Thay vào đó, đo 18 chỉ số

Chia làm 4 nhóm. Chỉ số nào **chưa đo được** thì ghi `NOT_MEASURED`, không ước lượng.

### 2.1 Chất lượng thiết kế test
| Chỉ số | Định nghĩa | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|
| Requirement traceability | % testcase dẫn được AC/rule id | `canonical-testcase-schema.yaml` | ĐO ĐƯỢC |
| Coverage completeness | Coverage unit đã cover / denominator | `professional-coverage-model.yaml` | ĐO ĐƯỢC |
| Test case validity | % case qua `09-review-testcases` không phải sửa | skill 09 output | ĐO ĐƯỢC |
| Expected-result correctness | % expected dẫn nguồn APPROVED (không phải suy diễn) | `requirement-intake` + rule id | ĐO ĐƯỢC |
| Duplicate rate | % case trùng phát hiện khi merge | `execution-plan` `merge_rules` | `NOT_MEASURED` |

### 2.2 Chất lượng phát hiện lỗi
| Chỉ số | Định nghĩa | Nguồn | Trạng thái |
|---|---|---|---|
| Defect precision | Bug được dev confirm / tổng bug đã log | Jira status (Closed-Fixed vs Rejected/Duplicate) | ĐO ĐƯỢC |
| False-positive rate | Bug bị Rejected + "not a bug" / tổng đã log | Jira | ĐO ĐƯỢC |
| False-negative sample | Lỗi lọt phát hiện sau release, lấy mẫu | `Defects/INDEX.md` + production defect | `NOT_MEASURED` |
| Conflict detection precision | Conflict được owner xác nhận là conflict thật | `Conflicts/INDEX.md` | `NOT_MEASURED` (skill 42 mới) |

### 2.3 Độ tin cậy thực thi
| Chỉ số | Định nghĩa | Nguồn | Trạng thái |
|---|---|---|---|
| Automation pass reliability | % run PASS ổn định qua nhiều build | `test-result.schema.yaml` `run_id` | ĐO ĐƯỢC |
| Flaky rate | % TC có `flaky_suspected=true` | `test-result` | ĐO ĐƯỢC |
| Reproducibility | % FAIL tái hiện lại được | `test-result` `retry_count` | ĐO ĐƯỢC |
| Evidence completeness | % result có evidence đủ theo `evidence_record` | `test-result` | ĐO ĐƯỢC |

### 2.4 Chất lượng điều phối & tuân thủ
| Chỉ số | Định nghĩa | Nguồn | Trạng thái |
|---|---|---|---|
| Routing accuracy | % execution plan không bị người sửa lại | `execution-plan` + feedback | `NOT_MEASURED` |
| Skill selection precision/recall | So với ground truth do Lead gán nhãn | cần dataset | `NOT_MEASURED` — **cần ground truth** |
| Human acceptance rate | % output được reviewer accept không sửa | `LEARNING_FEEDBACK_POLICY.md` | `NOT_MEASURED` |
| Standards compliance | % output có mục bắt buộc theo schema | lint schema | ĐO ĐƯỢC |
| Token/time efficiency | token + tool-call + thời gian mỗi task | `TOKEN_COST_OPTIMIZATION.md` | `NOT_MEASURED` |

**Trung thực:** 9/18 chỉ số hiện `NOT_MEASURED`. Đừng trình bày như thể đã đo đủ.

## 3. Confidence Score có giải thích

Xem `Config/QA-Agent/schemas/confidence-report.schema.yaml`. Tám thành phần, mỗi thành phần 0–3:
source quality, requirement completeness, traceability, coverage, execution evidence,
reproducibility, review status, conflict status.

**Luôn báo cáo:** band + `limiting_factors` + `required_actions`. **Không bao giờ** chỉ hiện con số,
và **không bao giờ** gọi nó là "độ chính xác của AI".

## 4. Đánh giá output AI của SẢN PHẨM (khác với mục trên)

Mục 1–3 nói về chất lượng của *agent QA*. Khi **sản phẩm** có AI/LLM (Copilot, Investigator,
alert triage, risk scoring), việc test nó thuộc `40-ai-output-testing`:

- Không đánh giá output AI bằng boolean đơn giản — dùng rubric + evidence + reviewer khi cần.
- Nêu rõ **oracle class**: `INVARIANT` / `DISTRIBUTIONAL` / `GROUNDED`.
- Một mẫu duy nhất **không** chứng minh consistency — phải nêu số lần lặp N và variance.
- Đổi model/prompt/provider là **sự kiện regression** ⇒ chạy lại baseline `40` rồi `32`.
- Chuẩn áp dụng (29119-11, 25059, ISTQB CT-AI) hiện còn `PROPOSED_2026-09-07` trong
  `standards-profile.yaml` ⇒ **NEED_CONFIG**, chưa được dùng ngôn ngữ pass/fail chuẩn tắc.

## 5. Cổng promotion

Từ `learning-profile.yaml` (giữ nguyên, nhắc lại vì hay bị quên):

- Agent **không tự nâng** knowledge state, competency level hay execution readiness.
- Chỉ knowledge `APPROVED` được dùng làm oracle PASS/FAIL.
- `L3` hoặc `EVIDENCE_PROVEN` cần evidence thực thi **và** audit entry đã review.
- **Toàn bộ** case zero-tolerance phải PASS trước khi công bố một phiên bản agent mạnh hơn.

## 6. Việc P0 còn lại của mục này

1. ~~Chạy lại `eval-suite.yaml` (baseline stale từ 2026-07-19).~~ **ĐÃ XONG 2026-09-16:** chạy 53/53 case, 14/14 zero-tolerance PASS, 0 FAIL; baseline `CURRENT_20260916`.
2. Thêm golden case cho capability mới: conflict detection, risk/impact, test advisor, orchestration.
3. Nối eval vào CI hoặc vào checklist khi sửa router/config (hiện **không** chạy tự động).
