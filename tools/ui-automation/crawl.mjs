// Crawl render cac route tren DEV (co dang nhap qua state_<user>.json tu mint.mjs).
// Read-only: chi goto + doc trang thai/URL/text, KHONG bam nut ghi. Chi DEV, KHONG PROD.
// Chay: node crawl.mjs [state_file] ; xuat crawl-result.csv
import { chromium } from 'playwright';
import fs from 'fs';

const BASE = 'https://dev-app.example.local';
const stateFile = process.argv[2] || 'state_test03.json';
if (!fs.existsSync(stateFile)) { console.error('THIEU', stateFile, '-> chay mint.mjs truoc'); process.exit(1); }

const ROUTES = [
  '/', '/anti-phishing','/anti-phishing/alerts','/anti-phishing/audit','/anti-phishing/devices','/anti-phishing/domains','/anti-phishing/events',
  '/app-vuls-management','/apps',
  '/asm/dictionary','/asm/domains','/asm/hosts','/asm/ip-addresses','/asm/web-server-stack',
  '/asset-inventory','/asset-inventory/clients','/asset-inventory/servers','/asset-inventory/services',
  '/automation/execution-history','/automation/playbook','/automation/playbook-dashboard',
  '/camera-dashboard','/chatbot','/chatbot/livechat','/content-hub',
  '/ctem/executive-summary','/ctem/security-analyzer','/downloads',
  '/endpoint-security-posture/executive-summary','/endpoint-security-posture/vuln-dashboard',
  '/identity-security-posture/identities','/identity-security-posture/identities/compliance-report','/identity-security-posture/identities/findings','/identity-security-posture/identities/overview','/identity-security-posture/identities/policies','/identity-security-posture/identity-graph',
  '/integrations',
  '/inventory/assets','/inventory/ot-assessment','/inventory/ot-asset-risk','/inventory/ot-assets','/inventory/ot-risk','/inventory/search',
  '/ir/ai_analytic','/ir/alert','/ir/alert/v2','/ir/case','/ir/dashboard-overview','/ir/legitimate-context','/ir/monitor','/ir/playbook','/ir/playbook/execution-history','/ir/rule','/ir/rule/v2','/ir/threat-hunting',
  '/kpi-dashboard/nist','/kpi-dashboard/nist/cycles','/kpi-dashboard/nist/dashboard','/kpi-dashboard/nist/detail-control','/kpi-dashboard/security-dashboard',
  '/monitor/pentest/dashboard','/monitor/pentest/jobs','/monitor/pentest/jobs/cicd',
  '/pentest','/pentest/cicd-projects','/pentest/cicd-vulns','/pentest/projects','/pentest/requests',
  '/risk-management','/risk-management/asset-compliance-management','/risk-management/governance-and-report','/risk-management/register','/risk-management/risk-index','/risk-management/risk-overview',
  '/support-center-insight','/support-center/knowledge-base','/support-center/office-hours',
  '/system-config','/ticket',
  '/ueba','/ueba/entities','/ueba/settings','/ueba/use-cases',
  '/user-management','/user-management/roles','/user-management/teams','/user-management/users',
  '/vuls-management','/vuls-management/cloud',
  // 6 route "ngoai sidebar" + 1 route nghi 404 -> xac minh con song khong
  '/copilot','/settings','/handbook','/domain-scanning','/request-permission','/ingestion-jobs',
];

const b = await chromium.launch();
const ctx = await b.newContext({ storageState: stateFile, viewport: { width: 1440, height: 900 } });
const rows = [['route','http','final_path','verdict','title']];
let i = 0;
for (const route of ROUTES) {
  i++;
  const p = await ctx.newPage();
  let http = '', verdict = '', finalPath = '', title = '';
  try {
    const resp = await p.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 25000 });
    http = resp ? resp.status() : '';
    await p.waitForTimeout(600);
    const url = p.url();
    finalPath = url.startsWith(BASE) ? url.slice(BASE.length) : url;
    title = (await p.title().catch(()=> '')).slice(0, 40);
    const body = (await p.locator('body').innerText().catch(()=> '')).slice(0, 1500);
    if (/login\.microsoftonline|\/api\/auth\/signin|Sign in|Cannot access your account/i.test(url + ' ' + body)) verdict = 'LOGIN';
    else if (/could not be found|404|not found/i.test(body) && !finalPath.startsWith(route)) verdict = 'NOT_FOUND';
    else if (/could not be found|This page could not be found/i.test(body)) verdict = 'NOT_FOUND';
    else if (finalPath.replace(/\/$/,'') !== route.replace(/\/$/,'')) verdict = 'REDIRECT->' + finalPath;
    else verdict = 'RENDER';
  } catch (e) {
    verdict = 'ERR:' + (e.message || '').slice(0, 40);
  }
  await p.close();
  rows.push([route, http, finalPath, verdict, title.replace(/[",\n]/g,' ')]);
  console.log(String(i).padStart(2), verdict.padEnd(22), http, route);
}
await b.close();
fs.writeFileSync('crawl-result.csv', rows.map(r => r.map(c => `"${c}"`).join(',')).join('\n'));
const rendered = rows.slice(1).filter(r => r[3] === 'RENDER').length;
const notfound = rows.slice(1).filter(r => r[3] === 'NOT_FOUND').length;
const login = rows.slice(1).filter(r => r[3] === 'LOGIN').length;
console.log(`\nTONG ${ROUTES.length} | RENDER ${rendered} | NOT_FOUND ${notfound} | LOGIN ${login} | con lai ${ROUTES.length - rendered - notfound - login}`);
console.log('-> crawl-result.csv');
