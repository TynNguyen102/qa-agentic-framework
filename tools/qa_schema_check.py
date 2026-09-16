#!/usr/bin/env python3
"""Kiểm tra bổ sung cho control-plane, chạy được cả trong CI lẫn local.

Ba việc:
  1. Parse mọi YAML trong Config/QA-Agent/ + governance/ (bắt lỗi cú pháp trước khi merge).
  2. Cảnh báo eval-suite đã stale so với lần sửa router/config gần nhất.
  3. Cảnh báo skill có SKILL.md nhưng thiếu frontmatter name/description (router route bằng description).

Thiết kế có chủ đích:
  - Việc 1 là HARD FAIL (exit 1) — lỗi cú pháp YAML là lỗi thật, chặn được bằng máy.
  - Việc 2 và 3 chỉ CẢNH BÁO (exit 0) — chúng là phán đoán, không nên chặn merge của người khác.
  - PyYAML không có (vd mạng công ty chặn PyPI) -> bỏ qua việc 1 và NÓI RÕ là đã bỏ qua,
    không im lặng báo PASS. Xem AI_RESULT_ASSURANCE_MODEL.md: NOT_CHECKED khác PASS.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_DIRS = ["Config/QA-Agent", "governance", "evals"]
SKILL_DIR = ".agents/skills"


def collect_yaml():
    out = []
    for d in YAML_DIRS:
        root = os.path.join(BASE, d)
        for dirpath, _, files in os.walk(root):
            for f in files:
                if f.endswith((".yaml", ".yml")):
                    out.append(os.path.join(dirpath, f))
    return sorted(out)


def check_yaml_syntax():
    try:
        import yaml
    except ImportError:
        print("SKIP  yaml-parse: PyYAML khong co. NOT_CHECKED (khong phai PASS).")
        print("      Trong CI thi buoc 'Install validator dependency' phai cai PyYAML truoc buoc nay.")
        return None

    bad = 0
    files = collect_yaml()
    for p in files:
        try:
            with open(p, encoding="utf-8") as fh:
                yaml.safe_load(fh)
        except Exception as exc:
            print("FAIL  yaml-parse: {}\n      {}".format(os.path.relpath(p, BASE), exc))
            bad += 1
    if bad:
        print("yaml-parse: {} file loi / {} file".format(bad, len(files)))
        return False
    print("OK    yaml-parse: {} file".format(len(files)))
    return True


def check_eval_freshness():
    """Canh bao neu router/config moi hon lan chay eval gan nhat."""
    eval_path = os.path.join(BASE, "evals", "qa-agent", "eval-suite.yaml")
    if not os.path.exists(eval_path):
        print("WARN  eval-suite.yaml khong ton tai.")
        return
    with open(eval_path, encoding="utf-8") as fh:
        text = fh.read()
    if re.search(r"baseline_freshness:\s*STALE", text):
        print("WARN  eval-suite: baseline dang duoc danh dau STALE.")
        print("      Xem runs: -> ban ghi gan nhat. Chay lai truoc khi tuyen bo baseline moi.")
    runs = re.findall(r"run_id:\s*\"([^\"]+)\"", text)
    if runs:
        print("      Lan chay gan nhat: {}".format(runs[-1]))
    # Chi soi LAN CHAY GAN NHAT. Truoc 2026-09-16 check nay bat moi occurrence cua chu
    # "PARTIAL" trong file nen van canh bao sai ngay ca khi da chay full suite.
    last_run_block = text.rsplit("run_id:", 1)[-1] if "run_id:" in text else ""
    m = re.search(r"scope:\s*\"([A-Z_]+)", last_run_block)
    last_scope = m.group(1) if m else "?"
    print("      Pham vi lan chay gan nhat: {}".format(last_scope))
    # Truoc 2026-09-16 check nay chi soi chu "PARTIAL" nen mot lan chay DELTA (chay bu vai case)
    # van duoc bao "phu het case" — bao OK SAI. Nay xet theo ten pham vi.
    if last_scope in ("PARTIAL", "DELTA"):
        print("      Luu y: lan chay gan nhat KHONG tu no phu het suite —")
        print("      do phu phai cong don voi lan FULL truoc do. Doc muc runs: de doi chieu.")
    if re.search(r"baseline_freshness:\s*CURRENT", text):
        print("OK    eval-suite: baseline dang duoc danh dau CURRENT.")
    else:
        print("WARN  eval-suite: baseline chua duoc danh dau CURRENT.")


def check_skill_frontmatter():
    root = os.path.join(BASE, SKILL_DIR)
    if not os.path.isdir(root):
        return
    missing = []
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, "SKILL.md")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            head = fh.read(2000)
        if not re.search(r"^name:\s*\S", head, re.M) or not re.search(r"^description:\s*\S", head, re.M):
            missing.append(name)
    if missing:
        print("WARN  skill thieu frontmatter name/description (router route bang description):")
        for m in missing:
            print("        - {}".format(m))
    else:
        print("OK    skill-frontmatter: tat ca skill co name + description")


HARDCODED_TOOLS = ["playwright", "selenium", "cypress", "robot framework", "robotframework",
                   "newman", "postman", "jmeter", "k6", "rest assured", "appium"]


def check_tool_hardcoding():
    """Canh bao skill nhac ten tool cu the ma khong nhac tool-adapters.yaml.

    KHONG phai loi: nhieu skill BUOC phai nhac ten tool (vd 11-generate-automation-script sinh code
    Robot that su). Check nay chi de NHIN THAY danh sach, phuc vu viec migrate dan sang khai
    capability. Vi vay no chi WARN, khong bao gio fail.
    """
    root = os.path.join(BASE, SKILL_DIR)
    if not os.path.isdir(root):
        return
    hits = []
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, "SKILL.md")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read().lower()
        tools = sorted({t for t in HARDCODED_TOOLS if t in body})
        if tools and "tool-adapters" not in body:
            hits.append((name, tools))
    if hits:
        print("WARN  skill nhac ten tool cu the ma chua tham chieu Config/QA-Agent/tool-adapters.yaml:")
        for name, tools in hits:
            print("        - {:38s} {}".format(name, ", ".join(tools)))
        print("      => Khong phai loi. Dung de theo doi tien do chuyen sang khai capability.")
        print("      => Tong: {} skill.".format(len(hits)))
    else:
        print("OK    tool-hardcoding: khong skill nao nhac ten tool ma bo qua tool-adapters.yaml")


AUDIT_REQUIRED = ["schema_version", "event_id", "timestamp", "actor_alias",
                  "skill", "status", "scope"]


def _enforced_from():
    """Doc moc cuong che tu governance/audit-policy.yaml (resolved_divergence.enforced_from)."""
    p = os.path.join(BASE, "governance", "audit-policy.yaml")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        m = re.search(r'enforced_from:\s*"(\d{4}-\d{2}-\d{2})"', fh.read())
    return m.group(1).replace("-", "") if m else None


def check_audit_events():
    """Audit event tu enforced_from tro di phai co du truong bat buoc (audit-policy quyet dinh A).

    Event CU hon moc do chi WARN — audit la bat bien, khong sua nguoc lai duoc.
    """
    cutoff = _enforced_from()
    if not cutoff:
        print("WARN  audit-events: khong doc duoc enforced_from trong governance/audit-policy.yaml")
        return True

    root = os.path.join(BASE, "Projects")
    if not os.path.isdir(root):
        return True

    old_missing, new_missing, checked = [], [], 0
    for dirpath, _, files in os.walk(root):
        if "audit-events" not in dirpath.replace("\\", "/"):
            continue
        for f in sorted(files):
            if not f.endswith((".yaml", ".yml")):
                continue
            full = os.path.join(dirpath, f)
            with open(full, encoding="utf-8") as fh:
                body = fh.read()
            missing = [k for k in AUDIT_REQUIRED if not re.search(r"^{}:".format(k), body, re.M)]
            checked += 1
            if not missing:
                continue
            m = re.match(r"(\d{8})T", f)
            stamp = m.group(1) if m else "00000000"
            (new_missing if stamp >= cutoff else old_missing).append((f, missing))

    print("      audit-events: da kiem {} file, moc cuong che tu {}".format(checked, cutoff))
    if old_missing:
        print("WARN  {} event TRUOC moc thieu truong (khong sua — audit bat bien):".format(len(old_missing)))
        for f, miss in old_missing[:5]:
            print("        - {}  thieu: {}".format(f, ", ".join(miss)))
        if len(old_missing) > 5:
            print("        ... con {} file nua".format(len(old_missing) - 5))
    if new_missing:
        print("FAIL  {} event TU moc {} tro di thieu truong bat buoc:".format(len(new_missing), cutoff))
        for f, miss in new_missing:
            print("        - {}  thieu: {}".format(f, ", ".join(miss)))
        print("      => audit-policy.yaml resolved_divergence: decision A. Bo sung roi chay lai.")
        return False
    if not old_missing:
        print("OK    audit-events: tat ca event co du truong bat buoc")
    return True


def main():
    print("== qa_schema_check ==")
    yaml_ok = check_yaml_syntax()
    check_skill_frontmatter()
    check_tool_hardcoding()
    check_eval_freshness()
    audit_ok = check_audit_events()
    if yaml_ok is False or audit_ok is False:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
