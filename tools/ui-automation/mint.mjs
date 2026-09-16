// Mint NextAuth session cookie tu Keycloak token — QC test UI tren DEV.
// KHONG in secret/token ra log; chi xuat file state_<user>.json cho Playwright.
import { encode } from 'next-auth/jwt';
import { jwtDecode } from 'jwt-decode';
import fs from 'fs';
import crypto from 'crypto';
import path from 'path';
import { fileURLToPath } from 'url';

// .env nam o goc workspace, script nay o tools/ui-automation/ -> len 2 cap.
// Duong dan tuong doi theo vi tri script nen chay dung du workspace o o nao (C, T...).
const __dir = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = path.resolve(__dir, '../../.env');
function readEnv(key) {
  const line = fs.readFileSync(ENV_PATH, 'utf8').split(/\r?\n/).find(l => l.startsWith(key + '='));
  return line ? line.slice(key.length + 1) : '';
}
const SECRET = readEnv('NEXTAUTH_SECRET');
if (!SECRET) { console.error('THIEU NEXTAUTH_SECRET trong .env'); process.exit(1); }
const CLIENT_SECRET = readEnv('client_secret');
if (!CLIENT_SECRET) { console.error('THIEU client_secret trong .env'); process.exit(1); }

const KC = 'https://dev-keycloak.example.local/realms/YOUR-REALM/protocol/openid-connect/token';
const user = process.argv[2] || 'qauser03';
// Mat khau doc tu .env theo ten user (key = ten user, vi du qauser03=...). Truoc 03/09 dong nay
// hardcode san mat khau qauser03 — da bo, vi file nay KHONG duoc .gitignore bao ve.
const pass = process.argv[3] || readEnv(user);
if (!pass) { console.error('THIEU mat khau cua ' + user + ' trong .env (key = ten user)'); process.exit(1); }

const body = new URLSearchParams({
  client_id: 'PRODUCT-APP-automation-test',
  client_secret: CLIENT_SECRET,
  grant_type: 'password', username: user, password: pass,
});
const r = await fetch(KC, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
const j = await r.json();
if (!j.access_token) { console.error('login fail:', j.error || r.status); process.exit(1); }

const at = jwtDecode(j.access_token);
const rt = j.refresh_token ? jwtDecode(j.refresh_token) : null;
const now = Math.floor(Date.now() / 1000);

const token = {
  name: at.name, email: at.email, sub: at.sub,
  first_name: at.given_name || 'QC', last_name: at.family_name || user,
  adName: at.preferred_username || user,
  access_token: j.access_token, refresh_token: j.refresh_token,
  access_expires_at: at.exp,
  refresh_expires_at: rt ? rt.exp : now + 4 * 3600,
  last_refreshed_at: now,
  roles: at.realm_access?.roles ?? [],
  dev_bypass: true,
  iat: now, exp: now + 4 * 3600, jti: crypto.randomUUID(),
};

const cookieName = '__Secure-next-auth.session-token';
// server getToken() decode voi salt="" -> encode cung phai salt="" (bo salt)
const value = await encode({ token, secret: SECRET, maxAge: 4 * 3600 });

const state = {
  cookies: [{
    name: cookieName, value, domain: 'dev-app.example.local', path: '/',
    expires: now + 4 * 3600, httpOnly: true, secure: true, sameSite: 'Lax',
  }],
  origins: [],
};
fs.writeFileSync(`state_${user}.json`, JSON.stringify(state));
console.log('OK ->', `state_${user}.json`,
  '| user:', at.preferred_username,
  '| roles:', (at.realm_access?.roles || []).join(',') || '(rong)',
  '| access token het han sau', at.exp - now, 'giay');
