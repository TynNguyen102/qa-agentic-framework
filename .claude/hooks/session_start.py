#!/usr/bin/env python3
"""SessionStart hook — auto-load skill router so it doesn't depend on being remembered.

Ported from a sibling QA workspace's same-purpose hook. Prints
SKILL.md in full (the router, load-bearing almost every task) plus a short pointer
(not a full dump) to the active project's OPERATING_CONTRACT/CURRENT_STATE.md, which
are large/session-specific and only needed for specific tasks.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_file(rel_path):
    path = os.path.join(BASE, rel_path)
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "[Không đọc được {}: {}]".format(rel_path, e)


def active_project():
    raw = read_file(os.path.join("project", "active-project.yaml"))
    match = re.search(r"^active_project:\s*(\S+)", raw, re.MULTILINE)
    return match.group(1) if match else None


def find_operating_contract(project_dir):
    path = os.path.join(BASE, "Projects", project_dir)
    if not os.path.isdir(path):
        return None
    for name in os.listdir(path):
        if name.upper().endswith("OPERATING_CONTRACT.md"):
            return "Projects/{}/{}".format(project_dir, name)
    return None


def main():
    skill_md = read_file("SKILL.md")
    project = active_project()

    if project:
        contract_path = find_operating_contract(project) or "Projects/{}/<PROJECT>_OPERATING_CONTRACT.md".format(project)
        reminders = (
            "- Active project: `{p}` (from `project/active-project.yaml`; ask if this session is about a different one).\n"
            "- Trước khi kết luận SIT DONE / defect / QMetry status: đọc `{c}`.\n"
            "- Trước khi bắt đầu việc thật trong session (US mới, retest...): đọc `Projects/{p}/CURRENT_STATE.md`"
            " (trạng thái sprint/US hiện tại) và `governance/knowledge-policy.yaml`.\n"
            "- Không dùng business rule/permission matrix/test data của project khác làm expected behavior cho `{p}`"
            " trừ khi đã approved rõ ràng.\n"
        ).format(p=project, c=contract_path)
    else:
        reminders = (
            "- `project/active-project.yaml` không xác định được active project — hỏi anh đang làm project nào"
            " trong `Projects/` trước khi đọc CURRENT_STATE/OPERATING_CONTRACT.\n"
        )

    context = (
        skill_md
        + "\n\n---\n"
        + "📋 Nhắc đầu session (tự động, không dump toàn bộ để tiết kiệm token):\n"
        + reminders
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
