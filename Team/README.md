# Team QC — Example-Project

**Cập nhật:** 2026-08-27
**Lead:** Nguyen Thi Thanh Tuyen (`qa-lead@example.com`)
**Dự án:** Example-Project (YOUR-ORG AI) — Jira project `SP`, 4 Squad, sprint hiện tại **SP Sprint N**
(2026-08-19 → 2026-09-04)
**Bản publish cho cả team:** Confluence <QC-SPACE> › QC › **Example-Project — QC Way of Working**
(page id `<page-id>`) — https://YOUR-SITE.atlassian.net/wiki/spaces/<QC-SPACE>/pages/<page-id>
Publish 2026-08-27, trạng thái DRAFT. **File local là nguồn chính** — sửa ở đây rồi đồng bộ lại
Confluence bằng `updateConfluencePage`, không có auto-sync.

---

## 1. Tài liệu nào đọc trước

Đọc theo đúng thứ tự này, đừng nhảy cóc:

| # | File | Để biết |
|---|---|---|
| 1 | `Team/SETUP-GUIDE.md` | Cài máy cá nhân, chạy được workflow lần đầu |
| 2 | `Team/WORKING-AGREEMENTS.md` | Cái gì được tự làm, cái gì phải xin duyệt |
| 3 | `Projects/Example-Project/QC-TESTING-PROCESS.md` | Quy trình test thật theo status Jira |
| 4 | `Projects/Example-Project/ONBOARDING.md` | Cách tìm BRD/AC cho 1 item (bắt buộc, 4 bước) |
| 5 | `Projects/Example-Project/Team/Squads-2026-08/<Squad>.md` | Domain + dependency của squad mình |
| 6 | `Projects/Example-Project/Sprints/Sprint-18/scope-*.md` | Danh sách việc thật của squad, phân theo mức sẵn sàng test |
| 7 | `Projects/Example-Project/CURRENT_STATE.md` | Nhật ký duy nhất: quyết định đã chốt, blocker hiện tại |

Nguyên tắc: **nếu `CURRENT_STATE.md` không nói, coi là chưa biết** — không suy đoán trạng thái dự án.

### Riêng cho Lead

| File | Để làm gì |
|---|---|
| `Team/LEAD-PLAYBOOK.md` | Nhịp review · thang ước lượng effort · phân việc theo level · review chéo · go/no-go · coaching + blocker |
| `Templates/pm-report-weekly.md` | Báo cáo PM chiều thứ 6 — có ví dụ điền sẵn số thật Sprint N |
| `Templates/artifact-review-checklist.md` | Checklist review chéo testcase/bug (người review người) |
| `Templates/go-no-go-record.md` | Mẫu comment Jira khuyến nghị release cho item ở `Ready to deploy` |

Phạm vi: vai **Test Lead (T5/T6)** theo trang Confluence **"QA Career Path"** — vận hành dự án.
Phần quy hoạch phòng ban, tuyển dụng, ngân sách, career framework thuộc vai **QA Manager**, đã có
sẵn org-wide, **không làm lại**.

### Bản Confluence tương ứng (cho người không dùng workspace)

```
Confluence <QC-SPACE> › QC
│
├── ★ Example-Project — QC Way of Working              <page-id>   ◄── hub
│   ├── 01. Quy trình test theo status Jira           <page-id>
│   ├── 02. Chuẩn testcase và log bug                 <page-id>
│   ├── 03. Phân công QC theo Squad, cách nhận việc   <page-id>   ⚠ chờ Lead điền
│   ├── 04. Onboarding QC mới, cách tìm BRD/AC        <page-id>
│   ├── 05. Kế hoạch Automation                       <page-id>
│   ├── 06. Test feature AI (Copilot/Investigator/    <page-id>
│   │        Triage/UEBA)
│   ├── 07. AI QA Workflow — cách team dùng skill     <page-id>
│   ├── 08. Report cuối sprint và Dashboard           <page-id>
│   │   ── cho Lead ──
│   ├── 09. Nhịp quản lý, review chéo, Go/No-Go       <page-id>
│   └── 10. Template báo cáo QC tuần cho PM           <page-id>
│
├── Master Test Plan & Strategy (SP Sprint N)        <page-id>
├── Template/  ── chuẩn org-wide, KHÔNG copy lại
│   ├── Test Case Template for Integration
│   ├── Ticket Bug Template for Integration
│   ├── System Test Report (Web Portal/API)
│   └── AI Model Test Report (Lite Suite)
├── QA Career Path                                   63311948   ← thang level L0-L5
├── Test Strategy for SOC and AI Security
├── Evaluation Strategy for AI/ML Systems/  (+4 trang con)
├── AI Testing Agent/
│   └── [Vibe-Testing] AI Testing Framework — Antigravity + Playwright
└── [Enhance] QC workflow
```

**Quy ước màu trạng thái** dùng thống nhất trên 11 trang Confluence — khi sửa file local nhớ giữ
đúng nghĩa này:

| Nhãn | Màu | Nghĩa |
|---|---|---|
| `ĐÃ CHỐT` / `APPROVED` | 🟢 xanh | Đã xác nhận bởi nguồn có thẩm quyền — dùng được ngay |
| `ĐANG LÀM` / `CHUẨN BỊ` | 🔵 xanh dương | Đang tiến hành, có người phụ trách rõ |
| `DRAFT` / `NEED_CONFIRM` | 🟡 vàng | Chưa duyệt — **không** dùng làm oracle PASS/FAIL |
| `BLOCKED` / `LÀM NGAY` | 🔴 đỏ | Chặn, hoặc cần xử lý ngay |
| `CHỜ PO` / `CHỜ DEV` | 🟣 tím | Phụ thuộc người ngoài team QC |
| `KHÔNG ÁP DỤNG` / `OUT_OF_SCOPE` | ⚪ xám | Ngoài phạm vi QC, hoặc thuộc owner khác |

---

## 2. Cấu trúc thư mục — việc của mình nằm ở đâu

```
Team/
  README.md               ← file này: charter, ai làm gì
  SETUP-GUIDE.md          ← cài đặt máy cá nhân
  WORKING-AGREEMENTS.md   ← guardrail: được/không được làm gì
  LEAD-PLAYBOOK.md        ← riêng Lead: nhịp, effort, review chéo, go/no-go
  Members/<alias>.yaml    ← profile + phạm vi quyền của từng người

Templates/
  pm-report-weekly.md          ← báo cáo PM thứ 6
  artifact-review-checklist.md ← checklist review chéo
  go-no-go-record.md           ← mẫu comment Jira khuyến nghị release
  member-profile.yaml          ← mẫu profile

Projects/Example-Project/
  QC-TESTING-PROCESS.md   ← quy trình chính (nguồn của trang Confluence)
  ONBOARDING.md           ← cách tìm tài liệu BRD/AC
  Config/modules.yaml     ← danh mục 31 module (quét thật từ platform)
  Modules/
    README.md             ← vì sao chia theo module, quy tắc
    <module>/
      TC/                 ← testcase, DÙNG LẠI xuyên sprint
      Sprint-18/
        Evidence/<KEY>/   ← screenshot, response JSON, ledger
        Reports/          ← report của module
  Sprints/Sprint-18/
    scope-<squad>.md      ← việc thật trong sprint, theo mức sẵn sàng test
  Knowledge-Base/
    Domain-Rules/*.yaml   ← business rule đã trích từ BRD (DRAFT / APPROVED)
    Confluence-Mirror/    ← bản mirror BRD nguồn Confluence
    GitLab-Mirror/        ← bản mirror spec/code nguồn GitLab
  Defects/<FINDING-ID>/   ← defect trước khi log Jira
  Outputs/                ← report cross-sprint, daily-check, QC report
  governance/audit-events/← lịch sử chạy skill, BẤT BIẾN (không sửa/xoá)
```

**Quy ước đặt tên bắt buộc** (để trace được về Jira):
- Testcase: `Modules/<module>/TC/<chức-năng>.md`
- Evidence: `Modules/<module>/Sprint-<N>/Evidence/<JIRA-KEY>/<ngày>_<mô-tả>.md`
- Defect nội bộ trước khi log Jira: `Defects/FINDING-<YYYYMMDD>-<NNN>/`

---

## 3. Ai làm squad nào

> ⚠️ **Bảng mẫu — điền theo tổ chức thật của bạn.** Đây là khung, không phải dữ liệu thật.
> Trước khi dùng để phân task, Lead phải điền và xác nhận từng dòng.

| Squad | Domain | PO | QC phụ trách | Backup |
|---|---|---|---|---|
| `<squad-1>` | `<domain của squad 1>` | `<PO>` | _NEED_CONFIRM_ | _NEED_CONFIRM_ |
| `<squad-2>` | `<domain của squad 2>` | `<PO>` | _NEED_CONFIRM_ | _NEED_CONFIRM_ |
| `<squad-3>` | `<domain của squad 3>` | `<PO>` | _NEED_CONFIRM_ | _NEED_CONFIRM_ |
| `<squad-4>` | `<domain của squad 4>` | `<PO>` | _NEED_CONFIRM_ | _NEED_CONFIRM_ |

**Ràng buộc capacity — ghi con số THẬT, đừng bỏ trống.** Mẫu cách viết: *"N QC / M squad, chỉ 1
sprint chung cho cả M squad — không squad nào có nhân lực độc lập. Squad `<X>` nhiều việc nhất sprint
này (`<số>` item."* Khi phân task phải tính việc dùng chung người, **không** giả định mỗi squad có 1
QC toàn thời gian.

**Ranh giới giáp ranh giữa các squad — liệt kê và bắt PO xác nhận trước khi phân task.** Chỗ hai
squad cùng đụng một domain là chỗ hay rơi task nhất; viết ra thành câu hỏi cụ thể thay vì để ngầm.

---

## 4. Nhịp làm việc

| Khi nào | Ai | Làm gì |
|---|---|---|
| Đầu ngày | Mỗi QC | Chạy `daily-check` (hoặc mở Jira dashboard) → xem item nào đổi status vào vùng mình |
| Item vào `Developing`/`To Dev` | QC phụ trách | Viết testcase draft + test data, chưa execute |
| Item vào `To Test`/`Testing` | QC phụ trách | Execute trên DEV, ghi PASS/FAIL, log bug |
| Item vào `Ready to deploy` | QC phụ trách | Smoke/regression vùng liên quan |
| Cuối sprint | Lead | Tổng hợp report (skill `33`), cập nhật `CURRENT_STATE.md` |
| Sang sprint mới | Lead | Tạo `Sprint-<N+1>/` cho cả 4 squad + `scope.md` mới (xem `ONBOARDING.md`) |

**Dashboard theo dõi:** https://YOUR-SITE.atlassian.net/jira/dashboards/10330 ("Example-Project QC Report")

---

## 5. Ai duyệt cái gì

| Hành động | Ai duyệt |
|---|---|
| Tạo/sửa testcase local, viết test data, phân tích requirement | Tự làm |
| Comment Jira hỏi BA/PO | Tự làm (nội dung theo chuẩn — xem `WORKING-AGREEMENTS.md`) |
| Tạo Jira defect | Lead duyệt nội dung trước khi tạo |
| Tạo Jira subtask QA | Lead |
| Import TestRail live | Lead (hiện `live_import_allowed: false` — chưa mở) |
| Publish/sửa Confluence | Lead |
| Promote business rule `DRAFT` → `APPROVED` | Lead + nguồn có thẩm quyền (PO/BA) |
| Test intrusive/destructive trên PROD | **Không làm.** Cần duyệt cấp trên Lead |

---

## 6. Việc còn mở của cả team

| # | Việc | Chờ ai |
|---|---|---|
| 1 | Điền bảng phân công mục 3 | Lead |
| 2 | ~~Chọn repo GitLab để team clone~~ — **XONG 2026-08-27**: `<QC-GROUP>/qa-workflow-agentskill-main`, nhánh `main` | — |
| 3 | Tài khoản QC test riêng trên DEV (không dùng AD cá nhân) | Lead — action item org-wide |
| 4 | DEV cung cấp swagger/API doc để automate API | Dev team |
| 5 | Quyết định TestRail suite/section + template trước khi import live | Lead |
| 6 | Ranh giới Red Team/Pentest Squad-B ↔ Squad-D | PO |
| 7 | AI Copilot có phải nền tảng dùng chung không | PO |
| 8 | Security Owner ký Ground Truth cho model AI | Chưa có người |
