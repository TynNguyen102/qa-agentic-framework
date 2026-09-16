# Khung QA — bản sạch, chưa gắn project nào

Bản này tách ra từ một control plane QA đã chạy thật, **đã bóc hết dữ liệu của dự án cũ**.
Giữ nguyên toàn bộ phương pháp và cơ chế; bỏ toàn bộ số liệu, tên, địa chỉ, ticket của dự án đó.

## Bắt đầu dùng

| # | Việc | Lệnh / file |
|---|---|---|
| 1 | Tạo project đầu tiên | copy `Templates/Project-Scaffold/NEW-PROJECT-TEMPLATE/` → `Projects/<tên>/` |
| 2 | Khai project đang active | sửa `project/active-project.yaml` (hiện đang `null`) |
| 3 | Điền cấu hình project | `Projects/<tên>/qa-config.yaml` — Jira key, môi trường, repo |
| 4 | Điền secret ở máy mình | copy `.env.example` → `.env` (đã gitignore) |
| 5 | Kiểm khung còn sạch không | `python tools/sanitize-check.py` |

Khi `active_project` còn `null`, **không được tuyên bố PASS/FAIL cho bất kỳ việc gì** — chưa có
oracle. Đây là luật cố ý, không phải thiếu sót.

## Có gì trong này

| Phần | Vai trò |
|---|---|
| `SKILL.md` + `.claude/skills/`, `.agents/skills/` | Router `qa-router` + 51 skill đánh số 01–44 và support. Phương pháp luận QA, không gắn sản phẩm |
| `Config/QA-Agent/` | Canonical testcase schema, coverage model, standards profile, router policy, skill registry, tool adapters, 6 schema I/O |
| `governance/` | 10 tài liệu: knowledge policy (DRAFT→NEED_CONFIRM→APPROVED), 9 cổng phê duyệt G1–G9, defect verification, AI result assurance, coverage model, standards traceability, learning feedback, token cost |
| `tools/*.py` | `tc-status.py` (đọc khối `case:` máy đọc được), `defects-index.py`, `tc-migrate.py`, `gen-baseline-coverage.py`, `qa_schema_check.py`, `qa_workspace.py`, `sanitize-check.py` |
| `.claude/hooks/` | 4 hook: session start, skill nudge, reply format gate, pre-Jira-write gate |
| `Templates/` | Project scaffold + template defect/report/checklist |
| `Automation/` | Chỗ đặt Playwright / Postman / k6 / Robot-Framework — **để trống**, bộ test là tài sản của từng project |
| `Team/` | Playbook cho Lead, hướng dẫn setup máy, mẫu ticket xin IT cài môi trường |
| `evals/` | Cơ chế eval zero-tolerance cho chính agent QA |

## Đã bóc đi những gì

| Bỏ | Lý do |
|---|---|
| Toàn bộ `Projects/<dự-án-cũ>/` | Knowledge base, defect, testcase, output, sprint state — dữ liệu thật |
| 690+ script `.mjs` dò theo từng ticket | Là sản phẩm công việc của dự án cũ, không phải khung. Giữ lại 5 file harness dùng chung |
| Bộ test Robot-Framework | Test suite là tài sản của project |
| Mọi secret | `.env`, `qa-config.local.yaml`, 12 file `state_*.json` (cookie phiên) — **không file nào được copy sang** |
| `node_modules/`, `.venv/`, binary trình duyệt | Cài lại bằng `npm install` |

## Đã thay bằng placeholder

Chạy `python tools/sanitize-check.py --apply` với bảng luật trong chính file đó. Các lớp đã thay:

| Lớp | Thay bằng |
|---|---|
| Tên sản phẩm, tên tổ chức | `Example-Project`, `YOUR-ORG` |
| Host DEV/PROD, Keycloak, GitLab, Jira site | `*.example.local`, `YOUR-SITE.atlassian.net` |
| Mã ticket thật | `DEMO-####` |
| Tài khoản test | `qauser01`…`qauser12` |
| Tên người thật | `<QA Lead>`, `<QC EM>`, `<dev>`, `<QC member>` |
| Email công ty | `qa-lead@example.com` |
| Repo nội bộ, group GitLab | `<QC-GROUP>`, `<PENTEST-REPO>`, `<AUTOTEST-REPO>` |
| ID trang Confluence, tên máy, IP nội bộ, UNC share | `<page-id>`, `<MACHINE-NAME>`, `<internal-ip>`, `<file-server>` |
| Squad, sprint, số liệu thật | `<squad-N>`, `Sprint N`, `<N>` |

## Kiểm chứng

`tools/sanitize-check.py` chạy **không có** `--apply` thì chỉ quét và báo cáo, không sửa gì.
Nó kiểm 16 lớp rò rỉ: tên sản phẩm, tên tổ chức, tên công ty mẹ, Jira site, mã ticket, repo sản
phẩm, tài khoản test, ID Confluence, IP nội bộ, token, tên máy, repo nội bộ, tên người Việt có dấu,
email thật, UNC share.

Lần chạy cuối trước khi bàn giao: **SẠCH, 0 chỗ**.

> ⚠️ Máy quét bắt theo mẫu, không hiểu ngữ nghĩa. Nó bắt được mọi thứ nó *biết cách* tìm — không
> chứng minh được là không còn gì khác. Trước khi chia sẻ bản này ra ngoài, **đọc mắt** ít nhất
> `README.md`, `Team/` và `.env.example`. Ba lớp rò rỉ cuối trong danh sách trên chỉ được thêm vào
> *sau khi* đợt quét đầu báo "sạch" mà đọc tay vẫn thấy sót — nên đừng tin tuyệt đối vào một lượt quét.

## Muốn dùng lại bộ lọc cho lần sau

Sửa `RULES` trong `tools/sanitize-check.py` theo tên/địa chỉ của nơi mới, rồi chạy `--apply`.
Thứ tự trong bảng luật quan trọng: mẫu dài và cụ thể phải đứng trước mẫu chung, nếu không
mẫu chung sẽ nuốt mất phần đuôi.
