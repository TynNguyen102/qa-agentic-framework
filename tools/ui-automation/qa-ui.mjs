#!/usr/bin/env node
// qa-ui.mjs — Đăng nhập UI DEV và thao tác, KHÔNG cần SSO/MFA.
//
// Cách chạy (từ thư mục này):
//   node qa-ui.mjs <account> <path> [tuỳ chọn]
//
// Ví dụ:
//   node qa-ui.mjs qauser01 /pentest/cicd-vulns                 # mở headed cho người xem
//   node qa-ui.mjs qauser01 /pentest/cicd-vulns --headless      # chạy nền, chỉ lấy dữ liệu
//   node qa-ui.mjs qauser01 /system-config/vuln-sla-policy --out=DEMO-6572
//   node qa-ui.mjs qauser01 /pentest/cicd-vulns --grep=Overdue --inputs
//
// Tuỳ chọn:
//   --headless        chạy không hiện cửa sổ (mặc định: HIỆN, để anh xem thao tác)
//   --out=<tên>       ghi ảnh + dump text vào Modules/pentest/Sprint-18/Evidence/<tên>/raw/
//                     (mặc định ghi vào ./out/, không vào git)
//   --grep=<từ>       chỉ in các dòng text khớp từ khoá (không đổ cả trang ra màn hình)
//   --inputs          in giá trị của mọi <input> trên trang (đọc số trong form cấu hình)
//   --wait=<ms>       thời gian chờ trang render, mặc định 7000
//   --keep=<ms>       giữ cửa sổ mở bao lâu trước khi đóng, mặc định 20000 (headed)
//   --full            chụp fullPage thay vì chỉ viewport
//
// CƠ CHẾ: lấy access_token từ Keycloak bằng password grant, rồi tự dựng cookie phiên
// next-auth v4 (`__Secure-next-auth.session-token`) bằng NEXTAUTH_SECRET và nạp vào Chromium.
// Không đi qua màn SSO, không cần bấm MFA. Đây là lý do tool này dùng lại được mỗi ngày.
//
// YÊU CẦU trong .env ở gốc repo (đã gitignore):
//   NEXTAUTH_SECRET · client_secret · qauser01..qauser06
//
// ⚠️ CHỈ DÙNG CHO DEV. Không trỏ vào PROD dưới mọi hình thức.
// ⚠️ Ảnh chụp màn danh sách vuln CÓ đường dẫn source + số dòng của vuln chưa vá — spec 027
//    FR-008 gọi đó là "an attack map". Ảnh thô luôn ghi vào raw/ (gitignored). Muốn đính vào
//    Jira thì phải cắt bỏ cột Location trước.

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';
import { encode } from 'next-auth/jwt';
import { jwtDecode } from 'jwt-decode';

const __dir = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dir, '../..');
const ENV = path.join(REPO, '.env');

const KC = 'https://dev-keycloak.example.local/realms/YOUR-REALM/protocol/openid-connect/token';
const CLIENT_ID = 'PRODUCT-APP-automation-test';
const ORIGIN = 'https://dev-app.example.local';
const COOKIE = '__Secure-next-auth.session-token';

const argv = process.argv.slice(2);
const flag = (n, d) => { const a = argv.find(x => x.startsWith(`--${n}=`)); return a ? a.split('=').slice(1).join('=') : d; };
const has = n => argv.includes(`--${n}`);
const user = argv.find(a => !a.startsWith('--')) || 'qauser01';

// Git Bash (MSYS) tự đổi tham số bắt đầu bằng "/" thành đường dẫn Windows:
// "/pentest/cicd-vulns" -> "C:/Program Files/Git/pentest/cicd-vulns".
// Nên chấp nhận cả 3 dạng và tự gỡ tiền tố bị chèn. Từ Git Bash có thể dùng:
//   MSYS_NO_PATHCONV=1 node qa-ui.mjs qauser01 /pentest/cicd-vulns
//   node qa-ui.mjs qauser01 pentest/cicd-vulns          (bỏ dấu / đầu)
//   node qa-ui.mjs qauser01 --path=/pentest/cicd-vulns
function normalizePath(raw) {
  if (!raw) return '/';
  let p = raw;
  const m = p.match(/^[A-Za-z]:[\\/](?:.*?[\\/])?Git[\\/](.*)$/); // MSYS chèn <install>/Git/
  if (m) p = '/' + m[1];
  p = p.replace(/\\/g, '/');
  if (p.startsWith('http')) return p;
  if (!p.startsWith('/')) p = '/' + p;
  return p;
}
const target = normalizePath(flag('path', argv.filter(a => !a.startsWith('--'))[1] || '/'));

if (target.startsWith('http') && !target.startsWith(ORIGIN)) {
  console.error(`[DUNG] Tool nay chi cho DEV (${ORIGIN}). Khong tro vao host khac.`);
  process.exit(2);
}

const readEnv = key => {
  if (!fs.existsSync(ENV)) { console.error(`[LOI] khong thay .env tai ${ENV}`); process.exit(1); }
  const line = fs.readFileSync(ENV, 'utf8').split(/\r?\n/).find(l => l.startsWith(key + '='));
  return line ? line.slice(key.length + 1).replace(/\s+#.*$/, '').trim().replace(/^["']|["']$/g, '') : '';
};

const SECRET = readEnv('NEXTAUTH_SECRET');
const CLIENT_SECRET = readEnv('client_secret');
const PASSWORD = readEnv(user);
for (const [n, v] of [['NEXTAUTH_SECRET', SECRET], ['client_secret', CLIENT_SECRET], [user, PASSWORD]]) {
  if (!v) { console.error(`[LOI] thieu ${n} trong .env`); process.exit(1); }
}

// --- 1. Lấy token Keycloak ---------------------------------------------------
const tr = await fetch(KC, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    client_id: CLIENT_ID, client_secret: CLIENT_SECRET,
    grant_type: 'password', username: user, password: PASSWORD,
  }),
});
const tj = await tr.json();
if (!tj.access_token) { console.error(`[LOI] Keycloak tu choi: ${tj.error || tr.status}`); process.exit(1); }

const at = jwtDecode(tj.access_token);
const rt = tj.refresh_token ? jwtDecode(tj.refresh_token) : null;
const now = Math.floor(Date.now() / 1000);
console.log(`[1] token OK — ${at.preferred_username} · het han sau ${at.exp - now}s`);

// --- 2. Dựng cookie phiên next-auth -----------------------------------------
const value = await encode({
  secret: SECRET, maxAge: 4 * 3600,
  token: {
    name: at.name, email: at.email, sub: at.sub,
    first_name: at.given_name || 'QC', last_name: at.family_name || user,
    adName: at.preferred_username || user,
    access_token: tj.access_token, refresh_token: tj.refresh_token,
    access_expires_at: at.exp, refresh_expires_at: rt ? rt.exp : now + 4 * 3600,
    last_refreshed_at: now, roles: at.realm_access?.roles ?? [],
    dev_bypass: true, iat: now, exp: now + 4 * 3600, jti: crypto.randomUUID(),
  },
});
console.log('[2] cookie phien da dung xong');

// --- 3. Nơi ghi kết quả ------------------------------------------------------
const outName = flag('out', '');
const OUT = outName
  ? path.join(REPO, 'Projects/Example-Project/Modules/pentest/Sprint-18/Evidence', outName, 'raw')
  : path.join(__dir, 'out');
fs.mkdirSync(OUT, { recursive: true });

// --- 4. Mở trình duyệt -------------------------------------------------------
const headless = has('headless');
const browser = await chromium.launch({
  headless, slowMo: headless ? 0 : 400,
  args: headless ? [] : ['--start-maximized'],
});
const ctx = await browser.newContext({
  viewport: headless ? { width: 2560, height: 1200 } : null,
  locale: 'vi-VN', timezoneId: 'Asia/Ho_Chi_Minh',
});
await ctx.addCookies([{
  name: COOKIE, value, domain: 'dev-app.example.local', path: '/',
  expires: now + 4 * 3600, httpOnly: true, secure: true, sameSite: 'Lax',
}]);
const page = await ctx.newPage();

const url = target.startsWith('http') ? target : ORIGIN + target;
console.log(`[3] mo ${url}  (${headless ? 'headless' : 'HEADED — anh xem duoc'})`);
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(Number(flag('wait', 7000)));

// --- 5. Thu kết quả ----------------------------------------------------------
const slug = (target.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'home');
const text = await page.evaluate(() => document.body.innerText);
fs.writeFileSync(path.join(OUT, `${slug}.txt`), text);
await page.screenshot({ path: path.join(OUT, `${slug}.png`), fullPage: has('full') });
console.log(`[4] title: ${await page.title()}`);
console.log(`[4] da ghi ${slug}.txt va ${slug}.png vao ${OUT}`);

const g = flag('grep', '');
if (g) {
  const re = new RegExp(g, 'i');
  const lines = [...new Set(text.split('\n').map(s => s.trim()).filter(s => s && s.length < 120 && re.test(s)))];
  console.log(`[5] dong khop /${g}/i  (${lines.length}):`);
  lines.slice(0, 40).forEach(s => console.log('    | ' + s));
}

if (has('inputs')) {
  const inputs = await page.evaluate(() =>
    [...document.querySelectorAll('input')].map(i => ({ n: i.name || i.id || i.placeholder || '', v: i.value, t: i.type })));
  console.log('[6] gia tri input tren trang:');
  inputs.forEach(i => console.log(`    ${String(i.n).padEnd(24)} = ${JSON.stringify(i.v)}  (${i.t})`));
}

if (!headless) {
  const keep = Number(flag('keep', 20000));
  console.log(`[xong] giu cua so ${keep / 1000}s roi dong. Ctrl+C de dong ngay.`);
  await page.waitForTimeout(keep);
}
await browser.close();
