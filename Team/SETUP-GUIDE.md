# Setup Guide — chạy được QA workflow trên máy cá nhân

**Cho:** QC mới join team Example-Project, tự chạy bộ skill trên máy mình.
**Thời gian:** ~45 phút (chưa tính thời gian chờ cấp token).
**Cập nhật:** 2026-08-27

> **Máy chưa có Node.js / Python?** Xem `Team/IT-REQUEST.md` — danh sách công cụ cần nhờ IT helpdesk
> cài, soạn sẵn dạng ticket paste được, kèm phần cert nội bộ và allowlist kho gói (phần hay bị quên
> nhất). Lưu ý: cài extension "Playwright Test for VSCode" **không phải** là đã cài Playwright.

---

## Bước 0 — Lấy workspace về máy

Repo chính thức (private, group `<QC-GROUP>`):

```powershell
cd C:\Users\<user>
git clone https://gitlab.example.local/<GROUP>/<QC-GROUP>/qa-workflow-agentskill-main.git qa-workflow
cd qa-workflow
```

Cần quyền Developer trở lên trên repo — xin Lead thêm nếu clone bị 403.

### ⚠️ Nhánh — `main` là protected, KHÔNG push trực tiếp

Đây là **rule công ty**, không phải quy ước nội bộ của team. Đừng xin bỏ, và đừng mất thời gian thử —
GitLab sẽ trả `You are not allowed to push code to protected branches`.

**Luồng bắt buộc:**

```powershell
git checkout main
git pull

# Tên nhánh và commit message BẮT BUỘC có mã Jira
git checkout -b feat/<JIRA-KEY>-mo-ta-ngan
git add <đường-dẫn-đã-sửa>
git commit -m "feat(<JIRA-KEY>) mô tả ngắn gọn việc đã làm"
git push -u origin feat/<JIRA-KEY>-mo-ta-ngan
```

Sau đó mở **Merge Request** vào `main` trên GitLab — GitLab in sẵn link ngay sau khi push. **Chờ
người khác approve rồi mới merge.** Không tự approve MR của mình.

⚠️ **Một số path bắt buộc code owner duyệt** — `.agents/`, `.claude/`, `SKILL.md`, `CLAUDE.md`,
`governance/`, `evals/`, `tools/`. MR đụng vào đó sẽ **không merge được** cho tới khi owner approve
(cấu hình qua [`CODEOWNERS`](../CODEOWNERS)). Các path còn lại (`Projects/`, `Team/`, `Outputs/`,
`Config/`, `Templates/`) thì member tự merge được sau khi có approve thường.

Chi tiết đầy đủ: [`CONTRIBUTING.md`](../CONTRIBUTING.md) mục 4 và 5.

⚠️ **Không commit secret.** `.gitignore` đã loại `.env`, `Projects/*/qa-config.local.yaml`,
`Projects/*/session-state.local.yaml`. Trước khi commit lần đầu, tự kiểm tra:

```powershell
git check-ignore -v .env Projects\Example-Project\qa-config.local.yaml
```

Cả 2 phải hiện ra là đã bị ignore. Nếu không → **dừng lại, báo Lead**, đừng commit.

**Đặt workspace ở đâu trên máy:**
- ✅ Ổ local. Workspace chính thức của Lead: `C:\Users\<user>\qa-workflow-agentskill-main`
  — chốt 2026-09-03: trước đó workspace nằm trên ổ mạng `T:`, nay đã chuyển hẳn sang `C:` và **mọi
  thao tác git đi từ `C:` lên GitLab**. Bản cũ trên `T:` không còn được dùng.
- ❌ **Không** đặt trên network drive (ổ `T:`, ổ mạng chung). Chính sách path-based của máy công ty
  chặn ghi file thực thi (`.js`, `.ps1`) trên network drive — mọi việc dùng `npm`/`node` sẽ fail.
  Đây là lỗi đã gặp thật, không phải giả định.

---

## Bước 1 — Cài Claude Code

1. Cài theo hướng dẫn chính thức: https://claude.com/claude-code
2. Mở workspace: `cd C:\Users\<user>\qa-workflow` rồi `claude` (hoặc dùng VS Code extension).
3. Kiểm tra skill đã load: gõ `/` → phải thấy danh sách skill `01-review-requirements` …
   `39-issue-triage` + `qa-router`, `daily-check`, `master-test-plan`.

Nếu không thấy skill: kiểm tra thư mục `.claude/skills/` có tồn tại trong workspace không.

---

## Bước 2 — Cert nội bộ YOUR-ORG (bắt buộc nếu dùng npm/node)

Cert SSL nội bộ (`<INTERNAL-ROOT-CA>`) chặn Node tải file qua HTTPS. Cần export cert và trỏ
biến môi trường:

```powershell
# Sau khi export cert ra file .pem
$env:NODE_EXTRA_CA_CERTS = "C:\Users\<user>\certs\YOUR-ORG-ca.pem"
```

Áp dụng cho **mọi** việc dùng npm/node trong workspace này (Playwright, tool script…), không chỉ
Playwright. Nên set vào biến môi trường user cho vĩnh viễn.

---

## Bước 3 — Kết nối Jira / Confluence (Atlassian MCP)

Không cần token. Auth qua **OAuth trong session**:

1. Trong Claude Code, chạy `/mcp` → chọn connector Atlassian → đăng nhập bằng tài khoản
   `@example.com` của bạn.
2. Kiểm tra: hỏi Claude "list các Jira project tôi thấy được" → phải ra project `SP`.

Quyền cần có: `read:jira-work`, `write:jira-work` (để comment/tạo subtask khi được duyệt).
Nếu không thấy project `SP` → xin Lead cấp quyền Jira project trước.

---

## Bước 4 — File `.env`

```powershell
Copy-Item .env.example .env
```

Rồi điền các giá trị sau. **Không commit `.env`, không paste token vào chat.**

| Biến | Lấy ở đâu | Bắt buộc? |
|---|---|---|
| `GITLAB_TOKEN` | GitLab → Settings → Access Tokens, scope `read_api` + `read_repository` | ✅ Bắt buộc — dùng để tìm BRD/spec/code |
| `TESTRAIL_USERNAME` | Email công ty của bạn | ✅ |
| `TESTRAIL_API_KEY` | https://your-org.testrail.io/index.php?/mysettings → tab API Keys. **Không dùng password login** | ✅ |
| `PLATFORM_DEV_USERNAME` / `PLATFORM_DEV_PASSWORD` | Tài khoản AD cá nhân, hoặc tài khoản QC test khi có | ⚠️ Xem Bước 6 |
| Các biến URL còn lại | Đã điền sẵn trong `.env.example`, không cần đổi | — |

---

## Bước 5 — Tạo profile của bạn

```powershell
Copy-Item Templates\member-profile.yaml Team\Members\<alias>.yaml
```

Điền `member_alias` (alias không chứa thông tin cá nhân nhạy cảm), `project_scopes: ["Example-Project"]`,
`role_modes` (xem `Projects/Example-Project/Config/agent-profile.yaml` để biết các role mode có sẵn).

**Không tự nâng `current_level` / `readiness` của mình** — việc này Lead quyết định dựa trên evidence
(quy tắc `promotion_policy`).

---

## Bước 6 — Môi trường test DEV (hiện đang có blocker)

| | |
|---|---|
| DEV | `https://dev-app.example.local` — nơi QC test |
| PROD | `https://app.example.com` — **chỉ smoke sau go-live**, không test intrusive/destructive |

**Trạng thái thật:** chưa có tài khoản QC test riêng. Login DEV đi qua YOUR-ORG AD SSO + MFA +
Cloudflare bot-check.

**Test tay:** đăng nhập bình thường bằng trình duyệt của bạn — không vấn đề gì.

**Test tự động:** đã thử và **thất bại** nhiều hướng (đừng thử lại từ đầu, mất thời gian):
- ❌ Playwright tự login (headless/headed): MFA number-matching hết hạn quá nhanh, Cloudflare chặn
  Chromium mới.
- ❌ Playwright điều khiển profile Edge/Chrome mặc định: trình duyệt chủ động từ chối
  ("DevTools remote debugging requires a non-default data directory").
- ✅ **Cách đang dùng được:** Playwright `connectOverCDP` vào browser bạn **đã đăng nhập sẵn**.
  Bắt buộc dùng lại `context.pages()[0]` (tab đã login) — **tuyệt đối không mở tab mới** trong
  context đó (tab mới bị logout).
- ⏳ Hướng đúng về lâu dài: tài khoản QC service riêng → login tay 1 lần → lưu `storageState` → tái
  sử dụng. Đang chờ (`Team/README.md` việc #3).

Chi tiết: `Automation/Playwright/README.md`.

---

## Bước 7 — Chạy thử lần đầu (smoke test)

Làm đúng thứ tự này để biết setup đã ổn:

1. `/daily-check` → phải đọc được Jira live, ra danh sách item đổi trạng thái.
2. Chọn 1 item trong `Sprints/Sprint-18/scope-*.md` thuộc squad bạn, chạy
   `/01-review-requirements <JIRA-KEY>` → phải ra file review trong `Modules/<module>/TC/`.
3. Nếu cả 2 bước chạy được → setup xong.

Không chắc dùng skill nào: chạy `/qa-router` và mô tả việc cần làm, router sẽ chọn skill.

---

## Checklist hoàn thành

- [ ] Workspace nằm trên ổ local (không phải network drive)
- [ ] Claude Code thấy đủ skill `01`–`39`
- [ ] `NODE_EXTRA_CA_CERTS` đã set (nếu cần npm/node)
- [ ] Atlassian MCP đã OAuth, thấy project `SP`
- [ ] `.env` đã điền `GITLAB_TOKEN`, `TESTRAIL_*`
- [ ] `Team/Members/<alias>.yaml` đã tạo
- [ ] `/daily-check` chạy được
- [ ] Đã đọc `Team/WORKING-AGREEMENTS.md`
