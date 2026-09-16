# Contributing — QA Workflow AgentSkill

> Repo chính thức (private): `https://gitlab.example.local/<GROUP>/<QC-GROUP>/qa-workflow-agentskill-main`
> — group `<QC-GROUP>`, nhánh mặc định `main`. Khởi tạo 2026-08-27.
> **`main` là protected branch — KHÔNG push trực tiếp.** Đây là **rule công ty**, không phải quy ước
> nội bộ của team, nên không xin bỏ. Mọi thay đổi đi qua: **nhánh riêng → Merge Request → người khác
> approve → merge**. Xem mục 4 và 5. *(Ghi nhận 2026-09-03: dòng cũ ở đây từng ghi "commit trực tiếp
> lên main" — đã lạc hậu và trái với mục 4 ngay bên dưới.)*

Project song song (Robot Framework automation repo, nếu có): `NEED_CONFIRM` — xác nhận với DevOps/
automation owner của dự án đang active (`project/active-project.yaml`) trước khi dùng URL nào.

## 1. Clone về máy

```bash
git clone <remote-url-của-repo-này>   # NEED_CONFIRM — chưa có remote chính thức, hỏi DevOps
cd qa-workflow-agentskill
```

## 2. Setup lần đầu sau khi clone

```bash
cp .env.example .env   # điền giá trị thật theo đúng .env.example hiện tại (Jira/Confluence/GitLab/
                        # TestRail/Platform DEV-PROD của dự án đang active — xem
                        # Projects/<ACTIVE_PROJECT>/qa-config.yaml để biết dự án nào đang active)
```
Đây chủ yếu là skill/agent definition (markdown + config), không cần build gì thêm.
Mở workspace bằng Claude Code/Claude Desktop sẽ tự nhận `.claude/skills/` và `.agents/`.

## 3. Mở bằng VSCode

```bash
code .
```
Extension gợi ý: **Python** (Microsoft).

## 4. Quy trình làm việc (branch → commit → push → merge)

```bash
git checkout main
git pull

# Commit message BẮT BUỘC gắn mã Jira ticket (server từ chối push nếu thiếu)
git checkout -b feat/<JIRA-KEY>-mo-ta-ngan

git add <đường-dẫn-đã-sửa>
git commit -m "feat(<JIRA-KEY>) mô tả ngắn gọn việc đã làm"
git push -u origin feat/<JIRA-KEY>-mo-ta-ngan
# → mở Merge Request vào main trên GitLab, chờ review/approve rồi merge.
```

## 5. Quyền merge — path bị khoá (core skill)

Các path sau là phần định nghĩa "lõi" của AI agent skill — mọi MR đụng tới
các path này **bắt buộc phải được code owner duyệt (approve)** trước khi
merge được vào `main` (cấu hình qua [`CODEOWNERS`](CODEOWNERS)):

```
.agents/
.claude/
SKILL.md
AGENTS.md
CLAUDE.md
CODEX.md
governance/
evals/
tools/
```

Member vẫn push/tạo MR bình thường vào các path trên, chỉ là MR sẽ **không
merge được vào main** cho tới khi owner approve. Các phần còn lại
(`Outputs/`, `Projects/<name>/` tức Defects/Knowledge-Base/Outputs theo từng dự án, `Team/`,
`Templates/`, `Config/`, `testing-output/`...) member tự do merge, không
cần duyệt riêng.

## 6. NOTED — việc còn thiếu

- [x] Git remote chính thức: `<QC-GROUP>/qa-workflow-agentskill-main`, nhánh `main` (2026-08-27).
- [x] **Quy ước branch/MR — CHỐT 2026-09-03.** `main` là protected branch theo rule công ty. Không
      push trực tiếp được (GitLab trả `You are not allowed to push code to protected branches`). Mọi
      thay đổi qua nhánh riêng + MR + approve của người khác. Xem mục 4 và 5.
- [ ] Điền giá trị thật vào `.env` cho dự án đang active — xem `Projects/<ACTIVE_PROJECT>/qa-config.yaml`
      để biết credential/nguồn nào còn `PENDING`/`NEED_CONFIRM`.
