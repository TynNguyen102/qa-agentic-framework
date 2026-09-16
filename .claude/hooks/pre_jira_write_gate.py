#!/usr/bin/env python3
"""pre_jira_write_gate.py — PreToolUse hook: bom checklist 6 cong truoc moi lenh GHI Jira,
va CHAN (exit 2) khi payload vi pham nhung thu kiem duoc bang may.

Lich su (quan trong, dung xoa):
  Cac phien truoc 2026-09-09 tin rang hook nay DA TON TAI va dang cuong che 6 cong.
  Thuc te: file khong co trong repo va `git log --all -- *pre_jira_write_gate.py` TRONG
  => chua tung duoc commit. Nen 6 cong THUC TE CHUA TUNG duoc cuong che. Hau qua that:
  phien 09/09 ghi 2 FINDING ma bo cong G5 (kiem trung tren Jira) va khong bi chan.
  Dong thoi muc `pre_log_gate` cung chua ton tai trong defect-profile.yaml — da bo sung 09/09.

Ranh gioi trung thuc cua hook nay:
  - KIEM DUOC bang may (chan neu truot): title khop `title_format`; description co du
    `description_sections`; bug phai neu `related_story_link` (Relates -> Story).
  - KHONG kiem duoc bang may: G1..G6 phan lon la phan doan (vd "da trich duoc dong spec chua").
    Voi phan nay hook chi BOM checklist vao context. Dung tin la da an toan chi vi co hook.

Doc cau hinh tu Projects/<ACTIVE_PROJECT>/Config/defect-profile.yaml (parser regex, KHONG dung
pyyaml — workspace nay khong cai pyyaml, da kiem 2026-09-09).

An toan: moi loi bat thuong (khong parse duoc stdin, thieu config...) deu KHONG chan —
in canh bao roi exit 0. Hook khong bao gio duoc lam dut phien vi loi cua chinh no.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

# Tool ghi Jira can gac. Doc/search thi KHONG gac.
WRITE_TOOLS = re.compile(
    r"(createJiraIssue|editJiraIssue|addCommentToJiraIssue|transitionJiraIssue"
    r"|createIssueLink|addWorklogToJiraIssue)$"
)
CREATE_TOOL = re.compile(r"createJiraIssue$")
# [<TANG>][<LOAI>] <Module> / <Chuc nang> - <Mo ta ngan loi>
TITLE_RE = re.compile(r"^\[[^\]\[]+\]\[[^\]\[]+\]\s*.+\s+/\s+.+\s+-\s+.+")


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent.parent


def active_project(root: pathlib.Path) -> str:
    f = root / "project" / "active-project.yaml"
    if f.exists():
        m = re.search(r"^active_project:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return "Example-Project"


def load_profile(root: pathlib.Path) -> tuple[str, list[str], list[tuple[str, str]]]:
    """-> (title_format, description_sections, [(gate_id, gate_name)])"""
    p = root / "Projects" / active_project(root) / "Config" / "defect-profile.yaml"
    if not p.exists():
        return "", [], []
    t = p.read_text(encoding="utf-8", errors="replace")

    tf = ""
    m = re.search(r"^title_format:\s*\"([^\"]+)\"", t, re.M)
    if m:
        tf = m.group(1)

    secs: list[str] = []
    m = re.search(r"^description_sections:\s*\n((?:\s*-\s*.+\n)+)", t, re.M)
    if m:
        secs = [x.strip().strip('"').strip("'")
                for x in re.findall(r"^\s*-\s*(.+)$", m.group(1), re.M)]

    gates: list[tuple[str, str]] = []
    blk = re.search(r"^pre_log_gate:\s*\n(.*?)(?=\n[a-z_]+:|\Z)", t, re.M | re.S)
    if blk:
        for gid, gname in re.findall(r"-\s*id:\s*(\S+)\s*\n\s*name:\s*\"([^\"]+)\"", blk.group(1)):
            gates.append((gid, gname))
    return tf, secs, gates


def main() -> int:
    try:  # dam bao tieng Viet trong config khong bi mangle khi console la cp1252
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    say = lambda *a: print(*a, file=sys.stderr)  # noqa: E731

    # PHAI doc stdin dang BYTE roi decode UTF-8: tren Windows sys.stdin mac dinh cp1252,
    # doc truc tiep se lam MEO tieng Viet -> moi heading trong description_sections deu
    # "khong tim thay" -> hook CHAN oan MOI bug hop le. Da gap that khi test 2026-09-09.
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    except Exception:
        raw = ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    tool = str(payload.get("tool_name") or payload.get("toolName") or "")
    if not WRITE_TOOLS.search(tool):
        return 0  # khong phai lenh ghi Jira -> im lang

    root = repo_root()
    title_format, sections, gates = load_profile(root)
    tin = payload.get("tool_input") or payload.get("toolInput") or {}
    if not isinstance(tin, dict):
        tin = {}
    blob = json.dumps(tin, ensure_ascii=False)

    # ---------- BOM CHECKLIST (moi lenh ghi Jira) ----------
    say("=" * 72)
    say(f"[pre-jira-gate] {tool} — 6 CONG TRUOC KHI GHI JIRA (defect-profile.yaml: pre_log_gate)")
    if gates:
        for gid, gname in gates:
            say(f"   [ ] {gid:22s} {gname}")
    else:
        say("   !! khong doc duoc muc pre_log_gate — kiem defect-profile.yaml")
    say("   Nhac: doc code/spec/MR KHONG phai bang chung runtime. MR merged != da fix.")
    say("   Nhac: G5 phai tra CA Defects/INDEX.md VA Jira live (JQL) — khong chi local.")
    say("   Nhac: khong chac thi GHI FINDING local o PENDING roi hoi Lead, dung log.")
    # Nhac FORMAT — Lead chot 15/09 qua ban sua DEMO-7516 (defect-profile.yaml: jira_rich_format_2026_09_15)
    say("   Nhac FORMAT (mau chuan: DEMO-7516, DEMO-7512 — defect-profile.yaml muc jira_rich_format_2026_09_15):")
    say("      - Khoi dau (khong heading): dong `**Nhan:** gia tri` in dam; **API:** khai full https://host/path 1 LAN.")
    say("      - Du lieu dang bang (ma tran tai khoan/quyen, so lieu lech, danh sach case) -> markdown TABLE, khong viet thanh cau.")
    say("      - Mot dong `---` ngan khoi dau; moi muc la heading `#### <Ten muc>`; token ky thuat boc `inline code`; status code in **bold**.")
    say("      - Sau khi khai full host o dau, cac buoc dung path tuong doi cho gon. KHONG dung `_italic_` heading phang kieu cu.")

    # ---------- KIEM MAY MOC (chi voi createJiraIssue) ----------
    blockers: list[str] = []
    # field that cua createJiraIssue la `issueTypeName` (schema MCP, xac nhan 2026-09-09).
    # Chap nhan ca bien the issuetype / issueType / issueTypeName va ca dang nested {"name":"Bug"}.
    is_bug = bool(re.search(
        r'"issue_?type[a-z]*"\s*:\s*(?:"[^"]*Bug[^"]*"|\{[^}]*Bug[^}]*\})', blob, re.I))
    if CREATE_TOOL.search(tool) and is_bug:
        summary = ""
        for k in ("summary", "title"):
            m = re.search(rf'"{k}"\s*:\s*"((?:[^"\\]|\\.)*)"', blob)
            if m:
                summary = m.group(1)
                break
        if summary and not TITLE_RE.match(summary):
            blockers.append(
                f"TITLE_FORMAT: summary khong khop title_format.\n"
                f"      can:  {title_format or '[<TANG>][<LOAI>] <Module> / <Chuc nang> - <Mo ta ngan loi>'}\n"
                f"      dang: {summary[:120]}")

        missing = [s for s in sections if s and s not in blob]
        if sections and missing:
            blockers.append("DESCRIPTION_SECTIONS: thieu heading bat buoc -> " + ", ".join(missing))

        if not re.search(r"relate", blob, re.I):
            say("   [!] Chua thay dau hieu related_story_link trong payload. defect-profile.yaml")
            say("       `related_story_link_rule` (CONFIRMED 2026-09-06): MOI bug BAT BUOC 1 issue link")
            say("       'Relates' -> Story. Neu tao link bang lenh rieng ngay sau day thi bo qua canh bao nay.")

    if blockers:
        say("-" * 72)
        say("[pre-jira-gate] CHAN — payload vi pham defect-profile.yaml:")
        for b in blockers:
            say("   x " + b)
        say("   Sua payload roi goi lai. (Day la phan kiem duoc bang may; G1..G6 van thuoc trach nhiem QC.)")
        say("=" * 72)
        return 2

    say("=" * 72)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # tuyet doi khong lam dut phien vi loi cua hook
        print(f"[pre-jira-gate] hook loi, KHONG chan: {e}", file=sys.stderr)
        sys.exit(0)
