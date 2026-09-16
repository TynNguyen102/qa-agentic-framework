# Thêm một project mới vào QA-Workflow-AgentSkill

Workspace này là **control plane QA đa dự án**: một **Framework Core** dùng chung (skill đánh số
01–44 + support, coverage model, governance, canonical schema, router) chạy cho bất kỳ project nào
đang active, cộng với dữ liệu riêng của từng project trong `Projects/<name>/`.

Hiện tại project active là **Example-Project** (`project/active-project.yaml`). File này hướng dẫn
cách thêm project thứ 2 mà không phá phần dùng chung — **không chứa dữ liệu công ty/dự án cũ** (đã
lột sạch); mọi tham chiếu cụ thể ở dưới là ví dụ minh hoạ theo project active.

## Nguyên tắc

Khi có project thứ 2 thật, **đừng sửa trực tiếp** các file project-specific của project đang có cho
project mới — hãy **copy scaffold sang một bản riêng** (`Templates/Project-Scaffold/` →
`Projects/<tên-mới>/`), giữ nguyên phần Framework Core dùng chung, rồi khai báo project mới trong
`project/active-project.yaml`. Sau khi có 2 bản project thật để so sánh, MỚI quyết định có cần tách
cấu trúc `Core/` + `Projects/<A>/` + `Projects/<B>/` triệt để hay không (lúc đó ranh giới rõ ràng,
không phải đoán).

## Framework Core — dùng chung, KHÔNG sửa riêng cho từng project

| Thư mục/file | Vai trò |
|---|---|
| `SKILL.md` (router) | Router `qa-router` — trung lập; scope resolve từ `project/active-project.yaml`, không hardcode tên project |
| `.agents/skills/`, `.claude/skills/` | Skill đánh số — phần lớn là phương pháp luận QA chung (ISTQB/coverage model/bug hunting); vài skill có ví dụ/biến đặc thù project → review từng skill khi dùng cho project khác, đừng giả định 100% generic |
| `Config/QA-Agent/canonical-testcase-schema.yaml` | Generic — schema TC không phụ thuộc project |
| `Config/QA-Agent/professional-coverage-model.yaml` | Generic — coverage dimension/denominator model |
| `Config/QA-Agent/standards-profile.yaml` | Generic (ISTQB/ISO/OWASP/WCAG); `confirmation: CONFIRMED` gắn với approval của QA lead project active → project mới cần re-confirm nếu team/QA lead khác |
| `governance/knowledge-policy.yaml`, `governance/audit-policy.yaml` | Generic — state machine DRAFT/NEED_CONFIRM/APPROVED |
| `Projects/<ACTIVE_PROJECT>/governance/audit-events/` (cơ chế) | Cơ chế append-only event dùng chung; nội dung từng event là lịch sử riêng của project tạo ra nó |
| `evals/qa-agent/eval-suite.yaml` (cơ chế) | Cơ chế zero-tolerance/P0 dùng chung; **nội dung case cụ thể** (contract_ref trỏ tới rule của project) cần viết lại cho project mới |
| `.claude/hooks/session_start.py`, `prompt_skill_nudge.py` | Cơ chế dùng chung (đã dùng `$CLAUDE_PROJECT_DIR`, portable); `SKILL_TRIGGERS` keyword table + nội dung nhắc có thể có ví dụ đặc thù → review khi thêm project |
| `.claude/workflows/` | Cơ chế Workflow dùng chung; nội dung từng workflow file tham chiếu field đặc thù project → viết bản riêng cho project mới |
| `Config/TAG-EXTRACTION-RULES.md`, `SKILLS-INDEX.md` (nếu có) | Kiểm tra generic hay có ví dụ hardcode |

## Project-Specific — KHÔNG copy nguyên sang project khác

| Thư mục/file | Lý do project-specific |
|---|---|
| `Projects/<ACTIVE_PROJECT>/CLAUDE.md` (dòng tuyên bố scope) | Tuyên bố phạm vi project — project mới cần bản riêng |
| `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md` | Toàn bộ là trạng thái sprint/nguồn live của project đó |
| `Projects/<ACTIVE_PROJECT>/<PROJECT>_OPERATING_CONTRACT.md` | Source-of-truth priority, defect contract... trỏ tới nguồn thật (Jira key, Confluence page id) của project đó |
| `Projects/<ACTIVE_PROJECT>/Knowledge-Base/` (toàn bộ) | Domain rule, API spec, DB schema đều của project đó |
| `Projects/<ACTIVE_PROJECT>/qa-config.yaml`, `qa-config.local.yaml.example` | Cấu hình project — cần bản mới cho project khác |
| `Projects/<ACTIVE_PROJECT>/Defects/`, `Outputs/`, `Modules/` (nội dung, không phải cấu trúc thư mục) | Dữ liệu thật đã tích luỹ của project đó |
| `Projects/<ACTIVE_PROJECT>/Config/agent-profile.yaml` (phần `competencies` đã promote) | Competency L2/L3 gắn với evidence thật của project → project mới bắt đầu lại từ `DESIGN_ONLY` |
| `Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml` (severity/priority mapping đã CONFIRMED) | Mapping viết riêng cho ngữ cảnh project → không copy nguyên cho project khác loại (vd fintech) |

## Khi nào thực sự tách `Core/` + `Projects/<name>/`

Chỉ làm khi có project thứ 2 THẬT (không phải giả định) đã dùng workspace này đủ lâu để biết rõ phần
nào thực sự dùng chung nguyên vẹn. Tới lúc đó:
1. So sánh 2 bản project thật đã chạy, liệt kê chính xác cái gì giống 100%, cái gì na ná nhưng khác.
2. Tách phần giống 100% vào `Core/`, mỗi project giữ bản riêng trong `Projects/<name>/`.
3. Ghi quyết định thành 1 audit event, đổi `agent-profile.yaml` mục multi-project restructure từ
   `NOT_NEEDED_YET` sang trạng thái thật đã làm.
