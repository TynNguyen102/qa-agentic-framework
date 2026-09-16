# Learning & Feedback Policy

> **Trạng thái:** APPROVED · **Duyệt bởi:** QA Lead (qa-lead@example.com) · **Duyệt lúc:** 2026-09-16 · **Ưu tiên: P1**
> **Soạn bởi:** claude-code (agent) · nội dung kỹ thuật chưa được chứng minh bằng eval — xem mục trạng thái cuối mỗi tài liệu
> `Config/QA-Agent/learning-profile.yaml` đã có **nguyên tắc** ("agent growth is grounded retrieval
> plus evaluated workflows, not automatic model training"). Tài liệu này bổ sung **cơ chế** — gap #36.

## 1. Luật nền

**Workflow chỉ thông minh hơn từ dữ liệu ĐÃ ĐƯỢC REVIEW VÀ PHÊ DUYỆT.**
Không tự học từ mọi output của chính nó. Output của agent **không phải** là dữ liệu huấn luyện.

## 2. Nguồn feedback hợp lệ (chỉ 9 nguồn này)

| Nguồn | Tín hiệu | Thu từ đâu |
|---|---|---|
| Testcase được reviewer accept/reject | chất lượng thiết kế | skill `09` |
| Bug được confirmed / rejected / duplicate | defect precision | Jira status |
| Automation script được merge | chất lượng code test | GitLab MR |
| Routing decision bị người sửa | routing accuracy | `execution-plan` bị chỉnh |
| Test còn thiếu, phát hiện sau release | false negative | `Defects/INDEX.md` |
| Production defect escaped | lỗ hổng nghiêm trọng nhất | incident |
| Lịch sử flaky test | độ tin cậy automation | `test-result` `flaky_suspected` |
| Root-cause analysis | lỗi hệ thống hay lỗi ngẫu nhiên | RCA doc |
| Domain rule được owner approve | oracle mới | `Knowledge-Base/Domain-Rules/` |

**Không hợp lệ:** agent tự đánh giá output của mình; chat history; ý kiến chưa có người chịu trách nhiệm.

## 3. Feedback record

Lưu tại `Projects/<ACTIVE_PROJECT>/governance/feedback/FB-<YYYYMMDD>-<NNN>.yaml`:

```yaml
feedback_id: FB-20260916-001
version: 1
source: testcase_review | defect_outcome | automation_merge | routing_correction |
        missed_test | escaped_defect | flaky_history | rca | rule_approval
subject_ref: <TC id / Jira key / MR iid / plan_id>
reviewer: <người, có email>
reviewed_at: <ISO>
signal: ACCEPTED | REJECTED | CORRECTED
what_was_wrong: <cụ thể, không chung chung>
what_should_have_happened: <hành vi đúng>
root_cause_hypothesis: <vì sao agent làm sai: thiếu rule? router sai? prompt thiếu context?>
proposed_change: <đề xuất sửa gì — skill nào / config nào>
converted_to_eval_case: <eval id hoặc PENDING>
applied: false
rollback_ref: <commit/MR để hoàn tác>
```

## 4. Đường đi bắt buộc: feedback → eval → skill

```
feedback record  →  eval case (golden)  →  chạy eval  →  sửa skill qua MR  →  chạy lại eval
```

**Không được rút ngắn.** Cụ thể:

1. Một feedback **không** trực tiếp sửa skill. Nó phải được chuyển thành **eval case** trước.
2. Eval case mới phải **FAIL** trên bản hiện tại (chứng minh nó bắt được vấn đề thật).
3. Sửa skill qua Merge Request — cần cổng **G6**.
4. Sau khi sửa: eval case mới PASS **và** toàn bộ case zero-tolerance vẫn PASS.
5. Ghi audit event.

Lý do: nếu sửa skill thẳng từ feedback, lần sau regress sẽ không ai biết.

## 5. Điều tuyệt đối không được làm

- **Không tự sửa Core skill/policy/schema.** Cần G6.
- Không gộp nhiều feedback thành một thay đổi lớn không rollback được.
- Không coi feedback là rule nghiệp vụ mới — rule cần owner approve (cổng **G8**).
- Không xoá feedback record cũ; sai thì tạo bản mới có `supersedes`.
- Không dùng feedback để **nới lỏng** một gate an toàn. Gate chỉ nới bởi người, qua G6, có lý do ghi lại.

## 6. Hiện trạng

| Thành phần | Trạng thái |
|---|---|
| Nguyên tắc | ✅ `learning-profile.yaml` |
| Feedback record schema | ✅ tài liệu này (chưa có thư mục thật) |
| Thư mục `governance/feedback/` | ❌ **chưa tạo** — tạo khi có feedback đầu tiên |
| Đường feedback → eval | ⚠️ đã định nghĩa, **chưa chạy lần nào** |
| Đo human acceptance rate | ❌ `NOT_MEASURED` |

**Bước đầu tiên đề xuất:** khi Lead review bộ tài liệu này và sửa chỗ nào, chính lần sửa đó là
feedback record `FB-*` đầu tiên.
