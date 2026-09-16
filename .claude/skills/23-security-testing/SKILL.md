---
name: 23-security-testing
description: Plan or perform authorized security testing for web, API, identity, authorization, sessions, tenant isolation, input handling, secrets, abuse controls, and auditability. Use only within an explicit scope and rules of engagement.
---

# Security Testing

Security work requires an authorized target, environment, time window, accounts, permitted techniques, data rules, stop conditions, and escalation contact.
Read `Config/QA-Agent/professional-coverage-model.yaml`, `Config/QA-Agent/api-coverage-profile.yaml` for API scope, and the approved version in `standards-profile.yaml`.

## Procedure

1. Record the rules of engagement and assets in scope.
2. Threat-model entry points, trust boundaries, sensitive data, roles, tenants, integrations, and abuse cases.
3. Cover applicable OWASP web/API risks. For API scope, map API1–API10 individually to evidence or `N/A_WITH_REASON`: object/auth/property/function authorization, resource consumption, sensitive-flow abuse, SSRF, configuration, inventory/version management and unsafe upstream API consumption. Also cover session lifecycle, tenant isolation, injection, file handling, secrets, headers and audit logging.
   - Record the approved standard/version and project policy. Do not import another project's assets, fixed severities, security-header expectations or finding categories as this project's truth.
4. Prefer safe validation. Do not run intrusive scanners, destructive payloads, persistence, denial-of-service, credential attacks, or exfiltration without explicit authorization.
   - Use approved mock/canary targets for SSRF and deterministic, bounded payloads for injection/fuzzing; do not contact cloud metadata endpoints merely to prove reachability.
   - `Projects/<ACTIVE_PROJECT>/Knowledge-Base/QA-Checklists/security-payloads.draft.md` collects safe, defensive-only payload strings (SQLi test strings, SSRF encoding-bypass, XXE, JWT none-algorithm, security-header checklist, basic NoSQL/LDAP/XPath injection). It is `status: DRAFT` borrowed cross-project (cross-project) reference (see `governance/knowledge-policy.yaml`), usable ONLY within the authorized scope + ROE recorded above, on DEV, with redacted evidence, safe-validation only (no destructive/DoS/exfil/persistence, and never contact real cloud-metadata endpoints to prove reachability) — never a PASS/FAIL oracle by itself; resolve expected control and severity against this project's confirmed policy/contract.
5. Redact secrets and personal data from evidence. Validate impact without increasing blast radius.

## Output Contract

Return scope and authorization, coverage-unit/OWASP mapping, attack surface and inventory limits, prerequisites, safe reproduction, expected control, observed behavior, evidence, impact, likelihood, severity, remediation, untested risks and retest guidance.

Treat exposed documentation, a missing header, or a 5xx as a finding candidate until the environment policy and contract establish the expected control.
