# Compact Reference: 01-review-requirements

> Compact reference for `01-review-requirements` — quick lookup of the core checklist/format; see `SKILL.md` for the complete workflow and rationale.

## 3 Personas (quick prompts)

| Persona | Core question |
|---|---|
| QC Expert | Can I write a testcase from this? (expected output, pass/fail condition, precondition, actor, failure/edge cases all defined?) |
| End User | Does this flow feel natural? Are errors/status communicated clearly? Are real-world use cases covered? |
| BA / Senior Dev | Is the business rule/priority/limit implementable? Are integrations, dependencies, data model, state machine fully specified? |

## TSV Output Header (requirement issues list)

```
ID	Vai trò	Loại vấn đề	Vị trí	Vấn đề	Tại sao quan trọng	Câu hỏi / đề xuất	Mức độ	Trạng thái
```

- `Vai trò`: `QC` / `END_USER` / `BA_DEV`
- `Loại vấn đề`: Ambiguous AC / Missing rule / Missing data / Missing state / Missing permission / Non-testable / Contradiction
- `Mức độ`: `Blocker` / `Major` / `Minor` (Blocker = phải clarify trước khi dev bắt đầu)
- `Trạng thái`: mặc định `Open`

## ⚑ Kiểm tra trước khi báo DONE

- [ ] Review đủ 3 góc nhìn: QC Expert, End User, BA/Dev
- [ ] TSV issues list đủ cột, không còn dòng trống không giải thích
- [ ] Mọi rule/expected chưa xác nhận nguồn của dự án đang active đã đánh dấu `NEED_CONFIRM` — không dùng rule dự án khác làm mặc định
- [ ] Completion Status rõ ràng: `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`
- [ ] Cập nhật `Projects/<ACTIVE_PROJECT>/session-state.local.yaml` (gitignored, per-member) → `last_execution.skill`, `last_execution.status`, `notes`
- [ ] Ghi 1 event file vào `Projects/<ACTIVE_PROJECT>/governance/audit-events/YYYY/MM/` theo `governance/audit-policy.yaml`
