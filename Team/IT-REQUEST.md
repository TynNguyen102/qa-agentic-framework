# Danh sách công cụ cần IT helpdesk cài — QC team Example-Project

**Cập nhật:** 2026-08-28 · **Người soạn:** QA Lead
**Máy đã khảo sát:** `<MACHINE-NAME>` (user `<user>`) — quét đệ quy ổ đĩa + registry ngày 28/08.
**Dùng khi nào:** mỗi QC mới nhận máy, hoặc khi cần mở ticket xin cài công cụ.

> **Cách dùng:** copy phần "NỘI DUNG TICKET" bên dưới, điền tên máy + tài khoản, gửi helpdesk.
> Phần A và B nên nằm **trong cùng một ticket** — cài được phần mềm mà không mở mạng thì vẫn
> không dùng được, và ngược lại.

---

## Trước khi mở ticket — đã có sẵn, đừng xin lại

Xác nhận trên máy `<MACHINE-NAME>` ngày 28/08:

| Công cụ | Đường dẫn | Ghi chú |
|---|---|---|
| Git | `C:\Program Files\Git\cmd\git.exe` | Cài bằng quyền admin — IT đã làm sẵn |
| OpenSSH client (`ssh`) | `C:\WINDOWS\System32\OpenSSH\ssh.exe` | Đủ để mở SSH tunnel tới bastion |
| `curl`, `tar` | `C:\WINDOWS\system32\` | Bản Windows dựng sẵn |
| VS Code | `%LOCALAPPDATA%\Programs\Microsoft VS Code` | **Cài user-scope, không cần admin** — xem ghi chú quan trọng bên dưới |
| Google Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` | Bắt buộc cho automation — xem mục A.1 |
| Microsoft Edge | `C:\Program Files (x86)\Microsoft\Edge\Application\` | |
| Extension *Playwright Test for VSCode* | `~/.vscode/extensions/ms-playwright.playwright-1.1.19` | **Chỉ là tích hợp editor, KHÔNG phải runtime** |

> ### Điểm hay bị nhầm nhất
> Cài extension **“Playwright Test for VSCode”** từ tab Extensions **không phải là cài Playwright**.
> Extension chỉ là bộ điều khiển: nút ▶ chạy test, xem trace, pick locator. Nó đi tìm gói
> `@playwright/test` trong project rồi gọi **Node.js** để chạy. Không có Node → nút ▶ không làm gì cả.
> Cái cần xin IT là **động cơ** (Node.js + Python), không phải cái điều khiển.

> ### Ghi chú quan trọng cho helpdesk
> Máy này **đã cài được VS Code theo user-scope** (`%LOCALAPPDATA%\Programs`), tức chính sách hiện
> tại **cho phép cài user-scope không cần quyền Administrator**. Node.js và Python đều có bản
> user-scope. Nếu chính sách không cho cài machine-wide, **bản user-scope là chấp nhận được** —
> nêu rõ điều này trong ticket để không bị từ chối oan.

---

# NỘI DUNG TICKET

**Tiêu đề:** Cài môi trường chạy kiểm thử tự động cho team QC — Example-Project

**Bối cảnh:** Team QC đang có sẵn <N> testcase tự động trong GitLab nội bộ (group
`<GROUP>/<QC-GROUP>`) nhưng **không chạy được trên máy làm việc** vì máy chưa có runtime.
Không có gì phải mua — toàn bộ là phần mềm mã nguồn mở miễn phí.

> **Phạm vi: chỉ môi trường DEV.** Mọi đề nghị trong tài liệu này đều giới hạn ở `dev-app.example.local`
> và các database DEV. **QC không xin quyền truy cập PROD** — theo quy ước của team, PROD chỉ smoke
> thủ công sau go-live, không test intrusive/destructive. Nếu một ticket nào đó xuất hiện chữ PROD,
> chỉ có thể vì hai lý do: (a) thu hồi credential PROD đang bị lộ, hoặc (b) viết sai — soát lại.

---

## A. Phần mềm cần cài

### A.1 Node.js phiên bản LTS 22.x (kèm npm)

| | |
|---|---|
| **Vì sao cần** | Chạy **<N> testcase Playwright** đang có trong repo `<QC-GROUP>/<PENTEST-REPO>` (module Ticket, UEBA, DSPM, CMDB, ESPM, User Management, Chatbot) |
| **Nguồn tải chính thức** | https://nodejs.org — bản **LTS** |
| **Lệnh winget** | `winget install OpenJS.NodeJS.LTS` (máy đã có `winget v1.29.280`) |
| **Chấp nhận user-scope?** | **Có** — nếu bản machine-wide bị chính sách chặn, cài user-scope là đủ |
| **Kiểm tra thành công** | `node --version` ra `v22.x`, `npm --version` ra `10.x` trở lên |

> Không cần cài trình duyệt riêng cho Playwright: cấu hình của repo `<PENTEST-REPO>` dùng
> `channel: 'chrome'`, tức dùng **Google Chrome đã có sẵn trên máy**.

### A.2 Python 3.12 (kèm pip)

| | |
|---|---|
| **Vì sao cần** | Chạy **<N> testcase** của repo `<QC-GROUP>/<AUTOTEST-REPO>` (UI Alert Management, API, Database) và **<N> testcase pytest** của repo `<PENTEST-REPO>` |
| **Vì sao đúng bản 3.12** | Repo đang dùng bản này: file biên dịch trong repo là `*.cpython-312.pyc`, và cấu hình CI của repo ghi `python-version: '3.12'` |
| **Nguồn tải chính thức** | https://www.python.org/downloads/ |
| **Lệnh winget** | `winget install Python.Python.3.12` |
| **Khi cài nhớ** | Tick **“Add Python to PATH”** |
| **Xử lý kèm theo** | Tắt *App Execution Alias* của `python.exe` / `python3.exe` trong **Settings → Apps → Advanced app settings → App execution aliases**. Hiện tại `python` trên PATH đang trỏ vào **stub của Microsoft Store**, chạy chỉ mở cửa hàng chứ không phải Python — stub này sẽ che mất Python thật |
| **Kiểm tra thành công** | `python --version` ra `Python 3.12.x`, `pip --version` chạy được |

### A.3 *(Chỉ xin nếu A.2 xong mà `pip install` vẫn lỗi)* Microsoft C++ Build Tools

| | |
|---|---|
| **Vì sao có thể cần** | Một repo khai báo thư viện `psycopg2` bản biên dịch từ mã nguồn, cần trình biên dịch C++ trên Windows |
| **Nguồn** | https://visualstudio.microsoft.com/visual-cpp-build-tools/ (chọn workload *Desktop development with C++*) |

> **Đừng xin mục này ngay.** Team QC sẽ thử đổi sang gói `psycopg2-binary` (bản dựng sẵn, không cần
> trình biên dịch) trước. Chỉ mở ticket bổ sung nếu cách đó không được.

---

## B. Mạng và chứng thư — phần hay bị bỏ quên

Cài xong phần mềm mà không có phần này thì **mọi lệnh `npm install` / `pip install` đều fail**.
Đây là nguyên nhân hỏng phổ biến nhất, không phải chuyện lý thuyết.

### B.1 Chứng thư CA nội bộ `<INTERNAL-CA-NAME>` dạng file `.pem`

| | |
|---|---|
| **Vì sao cần** | Proxy nội bộ chặn Node/Python tải file qua HTTPS. Không có cert, `npm install` báo lỗi `SELF_SIGNED_CERT_IN_CHAIN` / `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` |
| **Đề nghị IT** | Cung cấp trực tiếp file `.pem` (hoặc hướng dẫn export chuẩn), để QC không phải tự mò export từ certificate store |
| **QC sẽ tự cấu hình** | `NODE_EXTRA_CA_CERTS`, `npm config set cafile`, `pip config set global.cert` |

### B.2 Cho phép truy cập các kho gói chính thức

| Địa chỉ | Dùng để làm gì |
|---|---|
| `registry.npmjs.org` | `npm install` — kho gói Node chính thức |
| `pypi.org` và `files.pythonhosted.org` | `pip install` — kho gói Python chính thức |
| `cdn.playwright.dev` *(và `playwright.azureedge.net` nếu còn dùng)* | Playwright tải bản Chromium/Firefox/WebKit riêng cho kiểm thử |
| `nodejs.org`, `www.python.org` | Tải bộ cài (nếu IT không cài hộ) |

> Nếu tổ chức có **proxy nội bộ cho kho gói** (Nexus, Artifactory…), xin cho **địa chỉ proxy đó**
> thay vì mở internet — QC dùng được như nhau, và cách này thường dễ duyệt hơn.

### B.3 Xác nhận chính sách ghi file thực thi

| | |
|---|---|
| **Vấn đề đã gặp thật** | Chính sách theo đường dẫn của máy công ty **chặn ghi file thực thi (`.js`, `.ps1`) trên ổ mạng**. Workspace QC nằm trên ổ mạng (`\\<file-server>\<share>\<user>`) nên `npm install` tại đó **chắc chắn fail** |
| **Đề nghị IT xác nhận** | Thư mục `C:\Users\<user>\qa-workflow\` **được phép** ghi và chạy `.js` / `.ps1`. Nếu không, xin bổ sung ngoại lệ cho đúng thư mục đó |
| **Ghi chú** | Team QC **không** xin bỏ chính sách trên ổ mạng. Chỉ cần một thư mục làm việc trên ổ C |

---

## C. Không thuộc helpdesk — gửi đúng team khác

Đưa vào đây để khỏi lẫn vào ticket IT và bị trả về.

| Việc cần | Gửi ai | Chặn cái gì |
|---|---|---|
| **Tài khoản QC test riêng trên DEV** (`dev-app.example.local`), có quyền View/Manage Alert + User Management | Team Dev | Toàn bộ kiểm thử tự động trên giao diện. Hiện phải dùng tài khoản AD cá nhân |
| **VPN + SSH bastion** (host, user, key `.pem`) và tài khoản chỉ-đọc cho MongoDB / PostgreSQL / ClickHouse trên DEV | Team Hạ tầng | **<N> testcase Database** của `<AUTOTEST-REPO>` |
| **Tài liệu API (Swagger/OpenAPI)** của DEV | Team Dev | Mục tiêu tự động hoá 100% tầng API |
| **Thu hồi credential đang nằm trong repo GitLab của QC** — kubeconfig cluster PRODUCTION và DEV kèm token, session người dùng, 2 Slack bot token, 1 mật khẩu tài khoản thật | **DevSecOps + chủ repo — GẤP** | Rủi ro bảo mật cấp tổ chức, không phải việc cài đặt |

---

### C.1 — Bằng chứng cụ thể cho việc xin VPN / SSH bastion (chẩn đoán 2026-08-28)

QC đã cấu hình sẵn kết nối PostgreSQL trong DBeaver và **không kết nối được**. Đã chẩn đoán tận gốc,
kết luận: **không phải lỗi driver, không phải lỗi sai tài khoản** — mà là **không có đường mạng**.

| Kiểm tra | Kết quả | Nghĩa là |
|---|---|---|
| DBeaver có Java không | **Có** — `C:\Program Files\DBeaver\jre`, yêu cầu Java 21 | Không dính chuyện thiếu Java |
| Driver PostgreSQL tải được không | **Được** — 35 file trong `%APPDATA%\DBeaverData\drivers\maven\maven-central` | Maven Central thông, driver nạp bình thường |
| Lỗi thật trong log | `org.postgresql.util.PSQLException: Connection attempt timed out` | Driver chạy rồi, chỉ là **không ai trả lời** |
| DNS phân giải host | `<db-host>.rds.amazonaws.com` → **`<internal-ip>`** | DNS nội bộ đã cấu hình đúng |
| Máy QC đang ở đâu | `<internal-ip>`, gateway `<internal-ip>`, Wi-Fi | Đã ở trong mạng nội bộ 10.x |
| Có route tới `<internal-ip>` không | **Có**, đi qua gateway mặc định | Gói tin **có được gửi đi** |
| TCP tới `<internal-ip>:5432` | **Timeout** | Bị chặn ở firewall hoặc security group giữa đường |
| VPN client trên máy | **Không có** | Chưa cài client nào |

**Đo thêm để khoanh vùng (cùng ngày, cùng máy, cùng mạng Wi-Fi):**

| Đích | IP phân giải | Cổng | Kết quả |
|---|---|---|---|
| RDS PostgreSQL — DB UEBA `anomaly_detection` | `<internal-ip>` (nội bộ) | 5432 | **TIMEOUT** |
| ClickHouse Cloud — `v_dev_data_platform` | `52.76.211.95` (internet) | 8443 | **TIMEOUT** |
| Portal DEV `dev-app.example.local` | `104.18.0.50` (internet) | 443 | **OK** |
| GitLab nội bộ `gitlab.example.local` | `<internal-ip>` (nội bộ) | 443 | **OK** |

**Kết luận sắc hơn:** cổng 443 thông **cả chiều nội bộ lẫn chiều internet**, nhưng **cả hai cổng
database đều chết** — kể cả ClickHouse là dịch vụ nằm ngoài internet. Một nguyên nhân duy nhất giải
thích được cả hai: **chính sách firewall chặn cổng database đi ra từ dải máy nhân viên
(`<qc-subnet>`), chỉ cho phép 443.** Đây **không** phải vấn đề security group của riêng instance RDS —
nếu chỉ là RDS thì ClickHouse phải vào được.

**Bằng chứng người khác đang kết nối được:** repo `<PENTEST-REPO>` kết nối **trực tiếp, không qua tunnel**
(`automation/config/config.yaml` không có khối `ssh`/`proxy` nào; `automation/db/src/scripts/check_seq.py`
gọi thẳng `psycopg2.connect(host=...)`). Tài liệu KB của chính team — `redteam/.claude/kb/Module/UEBA/db-reference.md`
— hướng dẫn *"Mở DataGrip / psql, kết nối DB anomaly_detection (dev)"* như thể chỉ cần mở là vào.
Nghĩa là **có vị trí mạng trong công ty kết nối được**, chỉ là dải máy QC hiện tại thì không.

**Vì vậy đây là xin quyền mạng, không phải xin tài khoản.** Tài khoản DB đã có sẵn (đang nằm trong
`<PENTEST-REPO>/automation/config/config.yaml` và `automation/config/config.py`) — có mật khẩu đúng mà cổng
đóng thì vẫn không vào được, vì chưa từng tới bước xác thực.

**Vì sao QC ban đầu tưởng là “lỗi Driver”:** stack trace trong DBeaver đầy các dòng
`org.postgresql.Driver.connect`, đọc thoáng qua rất giống lỗi driver. Thực chất đó là driver đang
*báo cáo* việc kết nối thất bại, không phải driver bị hỏng.

**Hai cách xử lý, xin ưu tiên cách 1:**

1. **SSH tunnel qua bastion** *(khuyến nghị)* — cấp **host bastion, tài khoản, và file key `.pem`**.
   Đây cũng chính là cách bộ automation của team đã thiết kế sẵn: repo `<AUTOTEST-REPO>` dùng thư
   viện `sshtunnel`/`paramiko`, file `.env.example` đã có sẵn hai biến `SSH_TUNNEL_HOST` và
   `SSH_PEM_KEY_PATH`. **Không cần cài thêm phần mềm** — DBeaver có sẵn tab SSH, và máy đã có
   `ssh.exe` của Windows cho phần script.
2. **Mở firewall trực tiếp** từ dải máy QC (`<qc-subnet>`) tới `<internal-ip>:5432` — chỉ xin nếu
   cách 1 không khả thi, vì mở cổng DB ra dải client thường khó được duyệt.

**Cần xin tương tự cho các DB còn lại** mà 64 testcase Database đang dùng: MongoDB, ClickHouse,
Redis trên DEV — cùng một đường bastion.

---

## D. Sau khi IT cài xong — QC tự làm, không cần helpdesk

Ghi ở đây để helpdesk biết phạm vi ticket kết thúc ở đâu:

1. Clone workspace về `C:\Users\<user>\qa-workflow\` (**không** để trên ổ `T:`).
2. Trỏ `NODE_EXTRA_CA_CERTS` vào file cert ở mục B.1.
3. `npm ci` trong thư mục `automation/ui` của repo `<PENTEST-REPO>`.
4. `npx playwright install chromium` *(chỉ cần nếu bộ test không dùng Chrome hệ thống)*.
5. `pip install -r requirements.txt` cho các repo Python.
6. Chạy thử một bộ test nhỏ để xác nhận môi trường.

Chi tiết ở `Team/SETUP-GUIDE.md`.

---

## Kiểm tra nhanh sau khi cài — dán vào PowerShell

```powershell
node --version      # ky vong: v22.x
npm --version       # ky vong: 10.x tro len
python --version    # ky vong: Python 3.12.x  (KHONG duoc mo Microsoft Store)
pip --version
git --version       # da co san
ssh -V              # da co san
$env:NODE_EXTRA_CA_CERTS    # phai tro toi file .pem cua cert noi bo
```

Cả 6 lệnh đầu ra đúng phiên bản, và dòng cuối không rỗng → môi trường đã sẵn sàng.

---

# Mẫu email gửi các team — bản chốt 2026-08-28

## Gửi theo thứ tự nào

| # | Việc | Gửi ai | Khi nào |
|---|---|---|---|
| 0 | **Hỏi nội bộ trước, đừng gửi mail vội** — nhắn <QC Engineering Manager>: *"Em connect DB `anomaly_detection` bị timeout ở cổng 5432, chị đang vào bằng đường nào?"* | Chat nội bộ | **Trước tiên.** Repo `<PENTEST-REPO>` connect trực tiếp không tunnel → chị ấy vào được hằng ngày. Có thể xong trong 5 phút, khỏi cần mục 2 của Email A |
| 1 | **Email B — bảo mật** | DevSecOps + chủ repo, danh sách hẹp | **Ngay trong ngày.** Token PROD đang phơi |
| 2 | **Email A — môi trường** | Team Dev + Team Hạ tầng | Cùng ngày, sau khi đã hỏi mục 0 |

> **Đừng gộp B vào A.** Email A gửi rộng; nói "kubeconfig PROD nằm trong repo GitLab của QC" trong
> email broadcast là mở rộng số người biết về lỗ hổng chưa vá, và chỉ đúng chỗ cho ai muốn tìm.

---

## EMAIL A — gửi Team Dev + Team Hạ tầng

**Subject:** `[QC] Đề nghị hỗ trợ môi trường kiểm thử DEV — Sprint N, hạn 04/09`

**To:** Team Dev, Team Hạ tầng · **CC:** PM

```
Chào các anh/chị,

Team QC (4 nhân sự) đang bị chặn ở một số điểm môi trường, ảnh hưởng trực tiếp tới
tiến độ kiểm thử Sprint N (kết thúc 04/09). Em gửi tổng hợp theo đầu mối.

Toàn bộ đề nghị dưới đây chỉ liên quan môi trường DEV. QC không xin quyền trên PROD.


1. TEAM DEV

- Tài khoản QC test riêng trên DEV (dev-app.example.local), quyền View/Manage Alert
  và User Management.
  Hiện QC phải dùng tài khoản AD cá nhân nên không tách được dữ liệu test khỏi dữ
  liệu thật, và không tự động hoá được phần đăng nhập.

- Swagger / API doc của DEV, để kiểm thử tầng API.


2. TEAM HẠ TẦNG — mở đường mạng tới database DEV

Xin nói rõ trước: QC đã có tài khoản database, không cần cấp lại. Vấn đề là máy QC
không có đường tới cổng database. Kết quả đo trên máy QC ngày 28/08:

  Đích                                              Cổng    Kết quả
  ------------------------------------------------  ------  -----------
  dev-your-org...rds.amazonaws.com  (<internal-ip>)     5432    Timeout
  hlgkjipdls.ap-southeast-1.aws.clickhouse.cloud     8443    Timeout
  dev-app.example.local                             443     OK
  gitlab.example.local      (<internal-ip>)   443     OK

Cổng 443 thông cả chiều nội bộ lẫn chiều internet, nhưng cả hai cổng database đều
timeout — kể cả ClickHouse là dịch vụ nằm ngoài internet. Nên nhiều khả năng là
chính sách chặn cổng database đi ra từ dải máy nhân viên (<qc-subnet>), không phải
cấu hình của riêng instance RDS.

Đề nghị MỘT trong hai cách, không cần cả hai:

  Cách A (QC ưu tiên) — cấp quyền SSH qua bastion: host, tài khoản, file key.
    Bộ automation của QC đã hỗ trợ sẵn đường này (thư viện sshtunnel), và cách này
    không phải mở cổng database ra dải máy nhân viên.

  Cách B — mở cổng từ dải máy QC tới <internal-ip>:5432 và <analytics-host>:8443.

Cần áp dụng tương tự cho MongoDB và Redis trên DEV.

Ảnh hưởng hiện tại: 64 testcase kiểm tra dữ liệu không chạy được, nghĩa là kết quả
test đang dừng ở tầng giao diện, chưa đối chiếu được dữ liệu thật trong database.


Nếu anh/chị cần danh sách nhân sự QC hoặc chi tiết kỹ thuật, em gửi ngay trong ngày.

Cảm ơn các anh/chị.
Trân trọng,
<tên> — QA Lead, Example-Project
```

---

## EMAIL B — chỉ gửi DevSecOps + chủ repo

**Subject:** `[Bảo mật — cần xử lý trong ngày] Credential trong repo GitLab nhóm <QC-GROUP>`

**To:** DevSecOps · **CC:** chủ repo (`hientt56`, `linhln18`, <QC member>)
**Cân nhắc CC:** Giám đốc — vì có credential cấp PROD

```
Chào anh/chị,

Trong lúc kiểm kê tài sản automation của team QC ngày 28/08, em phát hiện một số
credential thật đang nằm trong lịch sử git của các repo thuộc group
<GROUP>/<QC-GROUP>.

Em không sao chép giá trị vào bất kỳ tài liệu nào, chỉ ghi đường dẫn để anh/chị
kiểm tra.


NGHIÊM TRỌNG
- qcsoc-automation/configs/kube-prd-cmc-vn-rke.yaml
  Kubeconfig cluster PRODUCTION, đủ server, certificate-authority-data và token.
- qcsoc-automation/configs/kube-dev-aws-sg-rke.yaml
  Kubeconfig cluster DEV, đủ token.

CAO
- linhln18-auto/src/data/UI/auth/state_dev_linhln18.json
  Session Playwright của người dùng thật, 28 cookie kèm JWT.
- <AUTOTEST-REPO>/.env.example
  Mật khẩu thật của một tài khoản @example.com (các biến khác cùng file đều là changeme).
- <PENTEST-REPO>/automation/config/config.yaml
  Tài khoản PostgreSQL database anomaly_detection trên DEV — cả tài khoản đọc lẫn
  tài khoản ghi — và tài khoản ClickHouse Cloud.

TRUNG BÌNH
- 2 Slack bot token: qcsoc-automation/configs/slack.yaml, qcyour-org/configs/slack.yaml
- Token trong vhtt/JsonUtils/slack_notify.py
- Chuỗi kết nối MongoDB kèm mật khẩu ở 5 file thuộc redteam, qc-agents,
  linhln18-auto, <AUTOTEST-REPO>
- JWT trong 2 file log Playwright đã commit của redteam (.playwright-mcp/console-*.log)


Đề nghị thứ tự xử lý:
  1. Thu hồi / đổi credential trước.
  2. Xoá file khỏi nhánh.
  3. Xử lý lịch sử git — xoá ở commit mới nhất là chưa đủ, vì vẫn đọc lại được từ
     lịch sử.
  4. Bổ sung .gitignore cho các repo này: .env, configs/kube-*.yaml, assets/tokens/,
     src/data/UI/auth/*.json, .idea/dataSources*.xml, .playwright-mcp/

Ghi chú: pipeline quét DevSecOps cấp group đã hoạt động (đã thấy chạy thành công
trên một merge request của <AUTOTEST-REPO> ngày 27/08), nhưng 3 trong 4 repo
automation đang push thẳng vào nhánh mặc định nên pipeline không bao giờ được kích
hoạt. Nếu bắt buộc dùng merge request cho các repo này thì lần sau quét sẽ bắt được.

Em không tự xoá hay sửa lịch sử repo của người khác nên chỉ dừng ở báo cáo.

Nhờ anh/chị không forward email này ra ngoài danh sách người nhận cho tới khi
credential được thu hồi xong.

Cảm ơn anh/chị.
Trân trọng,
<tên> — QA Lead, Example-Project
```

---

## Ba điều nên tránh khi viết ticket loại này

1. **Đừng xin thứ mình đã có.** Lần đầu bản nháp ghi *"xin tài khoản chỉ-đọc MongoDB/PostgreSQL/
   ClickHouse"* — nhưng QC đã có tài khoản, cái thiếu là đường mạng. Xin sai thứ thì team kia sẽ cấp
   lại tài khoản, báo "xong rồi", và mình vẫn không dùng được — mất thêm một vòng.
2. **Đưa số đo, đừng đưa cảm nhận.** "Bị chặn khoảng 64 test" là kết quả. "Cổng 443 OK, cổng 5432 và
   8443 timeout" là nguyên nhân — người nhận hành động được ngay và khó từ chối hơn.
3. **Nêu một phương án ưu tiên kèm một phương án thay thế**, đừng liệt kê ba thứ rồi để họ đoán mình
   cần cái nào.
