// contrast-core.mjs — lõi dùng chung cho đo contrast trên UI DEV.
//
// Tách ra để probe-contrast.mjs (1 trang, cho Robot LLK gọi) và scan-contrast-routes.mjs
// (nhiều route, 1 lần login) không nhân bản logic tính màu.
//
// Xuất 3 thứ:
//   mintSessionCookie(user)      -> { value, now, username }   (Keycloak password grant -> cookie next-auth)
//   openLoggedInContext(browser, cookie) -> BrowserContext
//   scanPage(page, { sel, minNormal })   -> { url, total, violations, exemptDisabled, dimmed }
//
// CHỈ DÙNG CHO DEV. scanPage là read-only: chỉ đọc computed style, không click/submit.

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { encode } from 'next-auth/jwt';
import { jwtDecode } from 'jwt-decode';

const __dir = path.dirname(fileURLToPath(import.meta.url));
const ENV = path.join(path.resolve(__dir, '../..'), '.env');

export const KC = 'https://dev-keycloak.example.local/realms/YOUR-REALM/protocol/openid-connect/token';
export const CLIENT_ID = 'PRODUCT-APP-automation-test';
export const ORIGIN = 'https://dev-app.example.local';
export const COOKIE = '__Secure-next-auth.session-token';

export const readEnv = (key) => {
  if (!fs.existsSync(ENV)) { console.error(`[LOI] khong thay .env tai ${ENV}`); process.exit(1); }
  const line = fs.readFileSync(ENV, 'utf8').split(/\r?\n/).find(l => l.startsWith(key + '='));
  return line ? line.slice(key.length + 1).replace(/\s+#.*$/, '').trim().replace(/^["']|["']$/g, '') : '';
};

export async function mintSessionCookie(user) {
  const SECRET = readEnv('NEXTAUTH_SECRET');
  const CLIENT_SECRET = readEnv('client_secret');
  const PASSWORD = readEnv(user);
  for (const [n, v] of [['NEXTAUTH_SECRET', SECRET], ['client_secret', CLIENT_SECRET], [user, PASSWORD]]) {
    if (!v) { console.error(`[LOI] thieu ${n} trong .env`); process.exit(1); }
  }
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
  return { value, now, username: at.preferred_username || user };
}

export async function openLoggedInContext(browser, { value, now }, opts = {}) {
  const ctx = await browser.newContext({
    viewport: opts.viewport || { width: 1920, height: 1200 },
    locale: 'vi-VN', timezoneId: 'Asia/Ho_Chi_Minh', deviceScaleFactor: 1,
  });
  await ctx.addCookies([{
    name: COOKIE, value, domain: 'dev-app.example.local', path: '/',
    expires: now + 4 * 3600, httpOnly: true, secure: true, sameSite: 'Lax',
  }]);
  return ctx;
}

// ---------------------------------------------------------------------------
// Hàm chạy TRONG page. Không dùng biến ngoài (Playwright serialize sang browser).
// ---------------------------------------------------------------------------
export function scanPage(page, { sel = '', minNormal = 4.5 } = {}) {
  return page.evaluate(({ sel, minNormal }) => {
    const parseRGBA = (s) => {
      const m = String(s).match(/[\d.]+/g);
      if (!m) return null;
      const [r, g, b] = m.slice(0, 3).map(Number);
      return { r, g, b, a: m.length > 3 ? Number(m[3]) : 1 };
    };
    // dat mau co alpha len tren mau nen dac -> mau ket qua dac
    const over = (fg, bg) => ({
      r: fg.r * fg.a + bg.r * (1 - fg.a),
      g: fg.g * fg.a + bg.g * (1 - fg.a),
      b: fg.b * fg.a + bg.b * (1 - fg.a),
      a: 1,
    });
    const lum = (c) => {
      const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
    };
    const ratio = (c1, c2) => {
      const l1 = lum(c1), l2 = lum(c2);
      return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    };
    const hex = (c) => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');

    // nen hieu dung: leo cha, composite tung lop background len canvas trang.
    // Neu gap background-image/gradient thi KHONG the tinh mau nen bang CSS -> danh dau
    // hasImage, finding se xep vao nhom "indeterminate" (giong axe-core tra "incomplete"),
    // khong tinh la vi pham de tranh FAIL oan o CI gate.
    const effectiveBg = (el) => {
      const stack = [];
      let hasImage = false;
      let n = el;
      while (n && n.nodeType === 1) {
        const cs = getComputedStyle(n);
        if (cs.backgroundImage && cs.backgroundImage !== 'none') hasImage = true;
        const c = parseRGBA(cs.backgroundColor);
        if (c && c.a > 0) {
          stack.push(c);
          if (c.a === 1) break;    // gap lop dac roi thi cac cha ben tren khong con anh huong
        }
        n = n.parentElement;
      }
      let base = { r: 255, g: 255, b: 255, a: 1 };
      for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
      return { color: base, hasImage };
    };

    // opacity tich luy + filter/backdrop cua chuoi cha -> nguyen nhan "mo" khac voi mau token
    const dimChain = (el) => {
      const notes = [];
      let cumOpacity = 1, n = el;
      while (n && n.nodeType === 1 && n !== document.documentElement) {
        const s = getComputedStyle(n);
        const o = parseFloat(s.opacity);
        const cls = (typeof n.className === 'string' && n.className.trim())
          ? '.' + n.className.trim().split(/\s+/)[0] : '';
        if (!isNaN(o) && o < 1) { cumOpacity *= o; notes.push(`opacity:${o}@${n.tagName.toLowerCase()}${cls}`); }
        if (s.filter && s.filter !== 'none') notes.push(`filter:${s.filter}@${n.tagName.toLowerCase()}`);
        if (s.backdropFilter && s.backdropFilter !== 'none') notes.push(`backdrop:${s.backdropFilter}@${n.tagName.toLowerCase()}`);
        n = n.parentElement;
      }
      return { cumOpacity, notes };
    };

    const root = sel ? document.querySelector(sel) : document.body;
    if (!root) return { error: `khong thay selector ${sel}` };

    const findings = [];
    const seen = new Set();
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const txt = node.textContent.replace(/\s+/g, ' ').trim();
      if (!txt) continue;
      const el = node.parentElement;
      if (!el) continue;
      const s = getComputedStyle(el);
      if (s.display === 'none' || s.visibility === 'hidden') continue;
      const box = el.getBoundingClientRect();
      if (box.width < 1 || box.height < 1) continue;

      // Bo element KHONG thuc su nhin thay: display/visibility/content-visibility o BAT KY cha,
      // va opacity 0 (tooltip sidebar, nut chi hien khi hover). Neu khong bo, chung ra fg==bg
      // -> ratio 1:1 gia. checkVisibility co tu Chrome 105; co nhanh du phong cho engine cu.
      if (typeof el.checkVisibility === 'function') {
        if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;
      } else {
        let hidden = false, n2 = el;
        while (n2 && n2.nodeType === 1) {
          const s2 = getComputedStyle(n2);
          if (s2.display === 'none' || s2.visibility === 'hidden' || parseFloat(s2.opacity) === 0) { hidden = true; break; }
          n2 = n2.parentElement;
        }
        if (hidden) continue;
      }

      const fgRaw = parseRGBA(s.color);
      if (!fgRaw) continue;
      const { color: bg, hasImage } = effectiveBg(el);
      const { cumOpacity, notes } = dimChain(el);
      // Chu gan nhu trong suot thi khong phai loi contrast — la element an chua kip bo o tren.
      if (fgRaw.a * cumOpacity < 0.05) continue;
      const fgEff = over({ ...fgRaw, a: Math.max(0, Math.min(1, fgRaw.a * cumOpacity)) }, bg);
      const r = ratio(fgEff, bg);

      const fontPx = parseFloat(s.fontSize);
      const weight = parseInt(s.fontWeight) || 400;
      const isLarge = fontPx >= 24 || (fontPx >= 18.66 && weight >= 700);
      const need = isLarge ? 3.0 : minNormal;
      // WCAG mien tru contrast cho control disabled
      const disabled = el.closest('[disabled],[aria-disabled="true"]') != null;

      const tag = el.tagName.toLowerCase();
      const cls = (typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
      const key = `${tag}|${cls}|${s.color}|${hex(bg)}|${fontPx}|${weight}|${notes.join(',')}`;
      if (seen.has(key)) continue;
      seen.add(key);

      findings.push({
        sample: txt.slice(0, 60), tag, cls,
        ratio: +r.toFixed(2), need, pass: r >= need, disabled, indeterminate: hasImage,
        fg: s.color, fgEff: hex(fgEff), bg: hex(bg),
        fontPx, weight, isLarge, cumOpacity: +cumOpacity.toFixed(3), dim: notes,
      });
    }

    return {
      url: location.href,
      total: findings.length,
      violations: findings.filter(f => !f.pass && !f.disabled && !f.indeterminate),
      exemptDisabled: findings.filter(f => !f.pass && f.disabled),
      indeterminate: findings.filter(f => !f.pass && !f.disabled && f.indeterminate),
      dimmed: findings.filter(f => f.cumOpacity < 1 || f.dim.some(d => d.startsWith('filter') || d.startsWith('backdrop'))),
    };
  }, { sel, minNormal });
}
