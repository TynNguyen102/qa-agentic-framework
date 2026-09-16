# CODEX.md - Using Codex With This QA Workspace

Start each Codex session with:

```text
Đây là multi-project QA workspace. Trước khi làm task, đọc README.md, AGENTS.md, SKILL.md,
project/active-project.yaml để biết project đang active, rồi đọc Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md,
Projects/<ACTIVE_PROJECT>/qa-config.yaml và overlay Projects/<ACTIVE_PROJECT>/qa-config.local.yaml
nếu file tồn tại. Không dùng rule của project khác trừ khi anh nói rõ là reuse template.
```

## Operating Rules

- Scope mặc định là project trong `active_project` (`project/active-project.yaml`) — hỏi nếu không chắc.
- Không hardcode credentials.
- Không live update Jira/QMetry/Confluence nếu chưa được approve rõ.
- Khi thiếu tài liệu của project đang làm, hỏi hoặc mark `NEED_CONFIRM`; không mượn expected từ project khác.
- Đọc `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml` để chọn role mode/readiness và `governance/knowledge-policy.yaml` trước khi dùng business rule.
- Chỉ knowledge `APPROVED` được dùng làm PASS/FAIL oracle; không tự nâng competency/readiness.
- Ưu tiên `rg` khi tìm file/text.
- Dùng `Config/QA-Agent/professional-coverage-model.yaml` làm denominator chung; API/event đọc thêm `Config/QA-Agent/api-coverage-profile.yaml`. Không gộp designed/automated/executed/proven hoặc hứa zero bug.

## Good Prompts

```text
Check Jira Sprint hiện tại của project đang active, đọc comment mới, cho anh list US cần test.
```

```text
Chuẩn bị test US <JIRA-KEY> (nêu rõ project): đọc Jira/Confluence, gen testcase, robot skeleton, QMetry draft.
```

```text
Retest defect DEMO-456, chỉ draft comment trước, chưa update Jira.
```
