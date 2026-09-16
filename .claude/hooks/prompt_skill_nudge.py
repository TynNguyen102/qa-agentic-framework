#!/usr/bin/env python3
"""UserPromptSubmit hook — nudge the right skill even when the user doesn't type the
exact trigger keyword. Ported from a sibling QA workspace's
prompt_skill_nudge.py, adapted to this workspace's 39 numbered + 5 support skills under
`.agents/skills/` and `.claude/skills/`.

CAVEAT (honest, not silently overclaimed): the keyword list below is a best-effort
approximation built from each skill's folder name, not verified word-for-word against
each skill's own SKILL.md frontmatter description. Refine against real usage/false-negatives
over time — do not treat this list as authoritative routing, only as a nudge on top of
SKILL.md's own "Common Skill Routes" table.

Also encodes one always-on rule from Config/QA-Agent/professional-coverage-model.yaml
depth_triggers that today only fires if Claude "remembers" it without an exact trigger
phrase: asking about coverage completeness / SIT-DONE-equivalent for the active project ->
workflow 26 (deep-coverage-testing) should be considered, not skipped.
"""
import json
import sys

SKILL_TRIGGERS = {
    "01-review-requirements": ["review ac", "review requirements", "đánh giá yêu cầu", "phân tích br"],
    "02-sprint-test-plan": ["sprint test plan", "kế hoạch test sprint", "qa plan sprint"],
    "03-feature-test-plan": ["feature test plan", "test plan feature", "kế hoạch test cho feature"],
    "04-high-level-test-design": ["test design", "high-level design", "outline tc", "hltc"],
    "05-generate-test-specification": ["test specification", "test spec", "tạo test spec"],
    "06-generate-functional-testcases": ["viết testcase", "gen tc", "tạo test case chức năng", "functional test"],
    "07-design-accessibility-testcases": ["accessibility testcase", "thiết kế tc a11y", "wcag testcase"],
    "08-generate-api-testcases": ["api testcase", "gen tc api", "test case api"],
    "09-review-testcases": ["review testcase", "đánh giá tc", "gap analysis", "coverage analysis"],
    "10-generate-test-data": ["test data", "dữ liệu kiểm thử", "tạo data", "bva"],
    "11-generate-automation-script": ["automation script", "gen script", "robot framework", "playwright script"],
    "12-setup-test-automation": ["setup automation", "khởi tạo automation", "setup framework"],
    "13-execute-approved-testcases": ["execute testcase", "chạy testcase", "run tc"],
    "14-professional-api-testing": ["professional api test", "api test toàn diện", "comprehensive api"],
    "15-functional-happy-path-testing": ["happy path", "functional happy path"],
    "16-usability-testing": ["usability test", "trải nghiệm người dùng", "ux test"],
    "17-reliability-resilience-testing": ["reliability test", "resilience test", "chaos test", "failover"],
    "18-exploratory-testing": ["exploratory test", "khám phá bug", "session-based test", "charter test"],
    "19-execute-accessibility-testing": ["execute accessibility", "chạy test a11y"],
    "20-design-benchmark-testing": ["benchmark test", "thiết kế benchmark", "performance baseline"],
    "21-ui-ux-testing": ["ui test", "giao diện", "layout bug"],
    "22-contract-compatibility-testing": ["contract test", "compatibility test", "schema compatibility"],
    "23-security-testing": ["security test", "owasp", "pentest", "bảo mật", "vulnerability"],
    "24-test-coverage-audit": ["coverage audit", "kiểm tra coverage", "audit coverage"],
    "25-performance-testing": ["performance test", "load test", "k6", "jmeter"],
    "26-deep-coverage-testing": ["deep coverage", "test sâu", "adversarial", "race condition"],
    "27-execute-benchmark-testing": ["execute benchmark", "chạy benchmark"],
    "28-frontend-e2e-testing": ["e2e test", "frontend e2e", "playwright e2e"],
    "29-mobile-feature-testing": ["mobile test", "test mobile", "appium"],
    "30-business-logic-bug-hunt": ["săn bug", "business logic bug", "hunt bug", "deep bug hunt"],
    "31-sanity-testing": ["sanity test", "verify fix", "retest hẹp"],
    "32-smoke-regression-testing": ["smoke test", "regression test", "smoke regression"],
    "33-test-reporting": ["test report", "sprint report", "báo cáo kiểm thử", "tổng kết"],
    "34-database-testing": ["database test", "db test", "sql test"],
    "35-infrastructure-session-testing": ["infrastructure test", "session test", "context isolation"],
    "36-log-jira-defect": ["log defect", "tạo bug", "file jira defect", "soạn defect"],
    "37-retest-jira-defect": ["retest defect", "retest bug", "verify fix jira"],
    "38-query-data-by-assurance-level": ["query data", "assurance level"],
    "39-issue-triage": ["issue triage", "triage bug", "duplicate check", "phân loại issue"],
    "daily-check": ["daily check", "check hàng ngày", "morning check"],
    "jira-test-subtasks": ["tạo subtask", "jira subtask", "create testing subtask"],
    "master-test-plan": ["master test plan", "kế hoạch test tổng", "qa strategy"],
    "qmetry-testcase-import": ["import qmetry", "qmetry testcase", "push tc qmetry"],
}

COVERAGE_WORDS = ["đủ test chưa", "sit done chưa", "coverage đủ", "test đủ chưa", "coverage đầy đủ chưa",
                  "còn bug không", "hết bug chưa"]
SENSITIVE_WORDS = ["auth", "permission", "phân quyền", "rbac", "audit", "tenant", "consent"]
GEN_TC_WORDS = ["gen tc", "viết testcase", "tạo test case", "sinh tc"]


def read_prompt():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        return raw.lower(), raw
    if isinstance(data, dict):
        for key in ("prompt", "user_prompt", "message", "text"):
            val = data.get(key)
            if val:
                return str(val).lower(), raw
    return raw.lower(), raw


def main():
    prompt, raw = read_prompt()

    matched = []
    for skill, keywords in SKILL_TRIGGERS.items():
        if any(kw in prompt for kw in keywords):
            matched.append(skill)

    lines = []
    if matched:
        uniq = sorted(set(matched))
        lines.append("📌 Trigger phù hợp skill: " + ", ".join("`{}`".format(s) for s in uniq))
        lines.append(
            "→ Đọc `.agents/skills/{}/SKILL.md` trước khi làm (đúng SKILL.md router R0/Live Update Approval Gate).".format(uniq[0])
        )

    if any(w in prompt for w in COVERAGE_WORDS):
        lines.append(
            "⚠ Câu hỏi về coverage/hết-bug-chưa — dùng Config/QA-Agent/professional-coverage-model.yaml "
            "denominator, không công bố % thiếu numerator/denominator/scope/build/snapshot time. "
            "Cân nhắc `26-deep-coverage-testing` nếu US khớp depth_triggers."
        )

    if any(w in prompt for w in GEN_TC_WORDS) and any(w in prompt for w in SENSITIVE_WORDS):
        lines.append(
            "⚠ US này có yếu tố auth/permission/tenant/audit/consent — cân nhắc chạy "
            "`26-deep-coverage-testing` song song với `06-generate-functional-testcases`, "
            "dù không ai nhắc \"test sâu\"."
        )

    if not lines:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        }
    }))


if __name__ == "__main__":
    main()
