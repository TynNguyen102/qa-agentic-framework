# NEW-PROJECT Current State

**Updated:** NEED_CONFIRM
**Project:** <PROJECT NAME — NEED_CONFIRM>
**Status:** Scaffold only. No sprint, source connection, or evidence has been created for this
project yet. This file is a placeholder from `Templates/Project-Scaffold/` so the workspace's
multi-project structure is consistent — replace every section below with real facts as they're
confirmed, do not delete the structure.

## Known Live Sources

| Source | Status | Notes |
|---|---:|---|
| Jira project/filter | PENDING | Not configured yet. |
| Confluence | PENDING | Not configured yet. |
| API Swagger/OpenAPI | PENDING | Not configured yet. |
| QMetry project/folders/cycles | PENDING | Not configured yet. |
| Environment SIT/UAT | PENDING | Not configured yet. |

## Working Rules

- Không dùng rule/data của project khác làm expected cho project này.
- Nếu tài liệu chưa có, chỉ tạo plan/checklist/template, không claim PASS/FAIL.
- Live update Jira/QMetry/Confluence cần approve rõ trong phiên hiện tại.
- Mọi claim coverage phải có denominator và phân biệt `DESIGNED`, `REVIEWED`, `AUTOMATED`,
  `EXECUTED`, `PROVEN`; luôn báo gap và residual risk.

## Next Setup Checklist

| Item | Cần gì cụ thể | Trạng thái |
|---|---|---:|
| Project identity/domain | Tên, loại hệ thống, business domain | NEED_CONFIRM |
| Jira project key | Key thật + quyền truy cập | PENDING |
| Confluence space | Root doc/space | PENDING |
| API spec | Live OpenAPI/Swagger URL | PENDING |
| Environment | SIT/UAT URL, account, role | PENDING |
| Automation stack | Robot/Playwright/API/k6/mobile — repo và convention | PENDING |
| QMetry | Project/folder/cycle, export/import template | PENDING |
