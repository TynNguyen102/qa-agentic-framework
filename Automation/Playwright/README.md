# Playwright

Lưu UI/E2E browser automation khi một dự án cần Playwright. Hiện thư mục chưa có `playwright.config` hoặc test source, nên chưa có evidence capture thực tế.

> **ĐÍNH CHÍNH 2026-09-03 — workspace đã rời ổ `T:` hoàn toàn.** Anh chốt: **chỉ làm việc trên ổ
> `C:`, không làm trên `T:` nữa; mọi thao tác git đi từ `C:` lên GitLab.** Workspace chính thức:
> `C:\Users\<user>\qa-workflow-agentskill-main`. Do đó phần ghi chú 26/08 bên dưới nói
> "`package.json`/source ở đây (trên `T:`) vẫn là bản gốc để track/edit" **KHÔNG còn đúng** — không
> còn bản gốc nào trên `T:`, và bước "copy từ `T:` sang bản local trước khi chạy" đã bỏ.
>
> Hai điều dưới đây **vẫn còn hiệu lực**, vì là chính sách máy công ty chứ không phụ thuộc ổ nào:
> (1) `npm install` và chạy script phải ở path local — bản thật hiện tại là
> `C:\Users\<user>\AppData\Local\qc-tools\pw` (Playwright 1.62.1 + Chromium, kiểm live 03/09),
> **không** phải `qa-automation\Example-Project-Playwright` như ghi chú cũ (thư mục đó không tồn tại);
> (2) `NODE_EXTRA_CA_CERTS` bắt buộc cho mọi lệnh `npm`/`node` gọi HTTPS ra ngoài.
>
> Node hiện có thật: **v24.20.0** tại `AppData\Local\qc-tools\node-v24.20.0-win-x64` — **không nằm
> trên `PATH`**, phải gọi bằng đường dẫn tuyệt đối. **Python thì vẫn chưa có** (chỉ có stub
> WindowsApps báo lỗi), nên mọi validator `.py` vẫn chưa chạy được từ máy này.

> **QUAN TRỌNG — môi trường 2026-08-26:** `T:\` là network drive
> (`\\<file-server>\<share>\<user>`), và path này (`Automation/Playwright/...`) bị một
> chính sách path-based (AppLocker/EDR — chưa xác định chính xác cái nào) chặn ghi file thực thi
> (`.js`, `.ps1`) — `npm install` ở đây luôn báo `TAR_ENTRY_ERROR EPERM` cho `cli.js`, `index.js`
> và các file .ps1 của Playwright, kể cả khi trỏ `node_modules` qua junction về ổ local (chính sách
> khớp theo path logic, không phải path vật lý). Đã thử: xoá cài lại (2 lần), tắt sandbox của tool,
> junction `node_modules` — đều thất bại giống hệt nhau. Cài trực tiếp ở `%TEMP%` hoặc bất kỳ path
> local nào khác thì chạy sạch, không lỗi.
>
> **Giải pháp:** `package.json`/source ở đây (trên `T:`) vẫn là bản gốc để track/edit, nhưng
> **`npm install` và chạy script thực tế phải làm ở bản copy local**:
> `C:\Users\<user>\qa-automation\Example-Project-Playwright\` (đã setup, Playwright 1.62.1 +
> Chromium). Sau khi sửa script ở đây, copy sang thư mục local đó trước khi chạy. Nếu ai đó có thể
> gỡ được chính sách path này cho `T:\WorkFlow Project\...` thì báo lại — lúc đó có thể bỏ bước copy.
>
> **Cert SSL nội bộ:** mọi request HTTPS ra ngoài (bao gồm `npx playwright install`) đi qua proxy
> inspect SSL "<CORPORATE-PROXY>", ký bởi root CA nội bộ `<INTERNAL-ROOT-CA>`. Windows tự
> trust cert này nhưng Node.js thì không (dùng CA bundle riêng) → mọi lệnh `npm`/`node` gọi HTTPS
> ra ngoài cần set `NODE_EXTRA_CA_CERTS` trỏ tới cert đã export:
> `$env:NODE_EXTRA_CA_CERTS = "C:\Users\<user>\qa-automation\YOUR-ORG-enterprise-ca.pem"`
> (cert này là public root CA, không phải secret — nhưng đường dẫn máy-cụ-thể nên không track vào
> `.env` chung của repo).
>
> **Atlassian/Jira session KHÔNG portable qua Playwright storageState** (thử 2026-08-26, 2 lần,
> đăng nhập tương tác thật cả 2 lần): sau khi đăng nhập thành công và xác nhận URL ổn định trên
> board Jira thật, `context.storageState()` chỉ lưu được 5 cookie phụ (XSRF token, banner
> consent...), KHÔNG có cookie phiên đăng nhập thật — dùng lại storageState ở context mới bị đá về
> trang login ngay. Kết luận: cơ chế auth của Atlassian Cloud cho org này không dựa hoàn toàn vào
> cookie bền vững theo cách storageState nắm được (nghi ngờ: token ràng buộc thiết bị, hoặc
> partitioned cookie). Không tiếp tục debug hướng này nữa trừ khi có thông tin mới — dùng thao tác
> tay trong Jira UI cho các việc liên quan Jira. Playwright vẫn dùng tốt cho web app thông thường
> (vd Example-Project DEV/PROD, login qua `/api/auth/signin`) — vấn đề chỉ nằm ở riêng Atlassian SSO.

Evidence policy khi framework được cấu hình:

- Dùng `test.step` cho từng business step/checkpoint để trace đọc được theo nghiệp vụ.
- `standard`: trace khi failure/first retry, screenshot khi failure, video retain-on-failure.
- `audit`: trace/video luôn bật và screenshot sau mỗi business checkpoint cùng failure.
- Không chụp sau mọi click mặc định vì làm artifact phình và khó đọc.
- Giữ console/network diagnostics khi fail; che token, cookie, credential, response nhạy cảm và PII.
- Artifact lớn lưu ở CI/artifact storage; report trong Git chỉ giữ link/checksum đã làm sạch.

Chỉ được nói “đã ghi màn hình/trace” khi config đã bật và execution thực sự sinh artifact.

## DEV authentication (mint-cookie)

Không hardcode username, password, cookie hoặc token trong script. Bộ Playwright THẬT của dự án nằm ở `Projects/Example-Project/Automation/ui` (thư mục `Automation/Playwright` này chỉ là scaffold). Đăng nhập DEV qua cơ chế **mint-cookie** (`tools/ui-automation/mint.mjs`): lấy token Keycloak (password grant, client `PRODUCT-APP-automation-test`) rồi dựng cookie next-auth `__Secure-next-auth.session-token` → storageState, nạp vào Chromium — KHÔNG qua SSO/MFA/Cloudflare.

Credential đặt trong `.env` (đã gitignore: `PLATFORM_DEV_USERNAME`/`PLATFORM_DEV_PASSWORD`, `NEXTAUTH_SECRET`, `client_secret`), không commit. storageState là session secret, mode `0600`, không đính kèm evidence. **Chỉ áp dụng DEV; PROD tuyệt đối không test.**
