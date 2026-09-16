#!/usr/bin/env python3
"""defects-index.py — canh giu bat bien: moi thu muc Defects/FINDING-* PHAI co dung 1 dong trong INDEX.md.

Vi sao co file nay (bang chung, 2026-09-09):
  - commit 9b61cb5 them FINDING-20260907-003 + -004 (co manifest.yaml) nhung KHONG sua INDEX.md
    -> 2 finding CONFIRMED_DEFECT vo hinh voi recall-gate cua skill 01 tu 07/09, khong ai phat hien
       vi khong co gi kiem.
  - cung ngay, mot phien khac them 2 dong INDEX (FINDING-20260909-001/-002) ma KHONG tao thu muc
    -> dong chi muc tro vao manifest khong ton tai.
  INDEX.md la INPUT DUY NHAT cua recall-gate. Bang chep tay thi luon troi. Day la thu de kiem.

Nguyen tac:
  - Thu muc + manifest.yaml la NGUON SU THAT. INDEX.md la chi muc.
  - Script KHONG tu sinh lai ca bang: cot "Regression / anh huong can nho" la kien thuc da chat loc,
    KHONG ton tai duoi dang field trong manifest (manifest khong dong nhat: `module` chi co o 7/20).
    Tu sinh se lam MAT kien thuc do. Nen script chi doi chieu CAU TRUC va tao dong stub de nguoi/agent
    dien noi dung that.

Khong phu thuoc thu vien ngoai (pyyaml KHONG duoc cai trong workspace nay — da kiem 2026-09-09).

Dung:
  python3 tools/defects-index.py --check      # doi chieu, exit 1 neu lech (dung cho hook Stop)
  python3 tools/defects-index.py              # nhu --check nhung luon exit 0 (xem cho biet)
  python3 tools/defects-index.py --stub        # them dong skeleton cho finding thieu dong
  python3 tools/defects-index.py --fix-header  # sua lai so dem trong dong "_Cap nhat: ... N finding_"
"""
from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Bo sung 2026-09-16: chap nhan them DOAN MA NGUOI LAM giua ngay va so thu tu, vd
# FINDING-20260910-TUY-003. Ly do: hai luong QC chay song song cung mint ID tu mot day so
# theo ngay, dan toi 6 ma TRUNG cho 6 lo hoan toan khac nhau (phat hien khi thu merge len main
# 16/09). Doan ma nguoi lam tach khong gian so cho tung nguoi. Dang CU (khong co doan ma) van
# hop le de khong pha 42 finding lich su.
ROW_RE = re.compile(r"^\|\s*(FINDING-\d{8}(?:-[A-Z]{2,6})?-\d{3})\s*\|", re.M)
ID_RE = re.compile(r"^FINDING-(\d{8})(?:-([A-Z]{2,6}))?-(\d{3})$")
HEADER_RE = re.compile(r"^(_Cập nhật:\s*)(\d{4}-\d{2}-\d{2})(\s*·\s*)(\d+)(\s*finding)", re.M)
TABLE_SEP_RE = re.compile(r"^\|-{3}\|.*$", re.M)


def active_project() -> str:
    f = ROOT / "project" / "active-project.yaml"
    if f.exists():
        m = re.search(r"^active_project:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return "Example-Project"


def scalar(text: str, key: str) -> str | None:
    """Doc 1 scalar top-level (bo comment duoi va nhay)."""
    m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    if not m:
        return None
    v = m.group(1).split(" #")[0].strip().strip('"').strip("'").strip()
    return v or None


def jira_key(text: str) -> str | None:
    """Uu tien SP-xxxx trong khoi `jira:`, neu khong thi lay SP-xxxx dau tien."""
    m = re.search(r"^jira:\s*(.*)$", text, re.M)
    if m:
        inline = re.search(r"SP-\d+", m.group(1) or "")
        if inline:
            return inline.group(0)
        tail = text[m.end():]
        blk = re.match(r"((?:\n[ \t]+.*)+)", tail)
        if blk:
            nested = re.search(r"SP-\d+", blk.group(1))
            if nested:
                return nested.group(0)
    any_key = re.search(r"SP-\d+", text)
    return any_key.group(0) if any_key else None


def collect(defects_dir: pathlib.Path) -> tuple[list[dict], list[str]]:
    findings, problems = [], []
    for d in sorted(p for p in defects_dir.glob("FINDING-*") if p.is_dir()):
        man = d / "manifest.yaml"
        if not man.exists():
            problems.append(f"NO_MANIFEST      {d.name}: thu muc co nhung THIEU manifest.yaml")
            findings.append({"id": d.name, "lifecycle": None, "jira": None, "module": None, "us": None})
            continue
        t = man.read_text(encoding="utf-8", errors="replace")
        lid = scalar(t, "local_id")
        if not lid:
            problems.append(f"NO_LOCAL_ID      {d.name}: manifest thieu `local_id`")
        elif lid != d.name:
            problems.append(f"ID_MISMATCH      {d.name}: local_id='{lid}' KHAC ten thu muc")
        findings.append({
            "id": d.name,
            "lifecycle": scalar(t, "lifecycle_status"),
            "jira": jira_key(t),
            "module": scalar(t, "module") or scalar(t, "module_label"),
            "us": scalar(t, "found_in_sprint"),
            "title": scalar(t, "title") or scalar(t, "summary"),
        })
    return findings, problems


def reconcile(index_path: pathlib.Path, findings: list[dict]) -> tuple[list[str], list[str], list[str]]:
    text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    rows = ROW_RE.findall(text)
    folder_ids = [f["id"] for f in findings]
    missing = [i for i in folder_ids if i not in rows]                 # co thu muc, thieu dong
    dangling = [r for r in rows if r not in folder_ids]                # co dong, thieu thu muc
    dupes = sorted({r for r in rows if rows.count(r) > 1})
    return missing, dangling, dupes


def header_count(index_path: pathlib.Path) -> int | None:
    if not index_path.exists():
        return None
    m = HEADER_RE.search(index_path.read_text(encoding="utf-8"))
    return int(m.group(4)) if m else None


def next_id(defects_dir: pathlib.Path, member: str, day: str) -> str:
    """Cap ma FINDING ke tiep cho `member` trong ngay `day` (YYYYMMDD).

    QUAN TRONG: quet CA cac nhanh remote, khong chi thu muc local. Ngay 16/09 hai luong QC
    chay song song, moi luong chi nhin thu muc cua minh, nen ca hai cung cap FINDING-20260909-001
    cho hai lo khac nhau. Chi quet local la KHONG du de tranh trung.
    """
    member = member.upper()
    used = set()
    for p in defects_dir.glob("FINDING-*"):
        m = ID_RE.match(p.name)
        if m and m.group(1) == day and (m.group(2) or "") == member:
            used.add(int(m.group(3)))

    # Quet remote. Khong co mang thi bao ro la CHUA QUET DUOC, khong im lang bo qua.
    rel = defects_dir.as_posix()
    if ROOT.as_posix() in rel:
        rel = rel[len(ROOT.as_posix()):].lstrip("/")
    scanned_remote = False
    try:
        branches = subprocess.run(["git", "for-each-ref", "--format=%(refname)", "refs/remotes/"],
                                  cwd=ROOT, capture_output=True, text=True, timeout=30)
        for ref in [b for b in branches.stdout.split() if b and not b.endswith("/HEAD")]:
            out = subprocess.run(["git", "ls-tree", "-d", "--name-only", ref, rel + "/"],
                                 cwd=ROOT, capture_output=True, text=True, timeout=30)
            for line in out.stdout.splitlines():
                m = ID_RE.match(line.rsplit("/", 1)[-1])
                if m and m.group(1) == day and (m.group(2) or "") == member:
                    used.add(int(m.group(3)))
            scanned_remote = True
    except Exception as exc:
        print(f"CANH BAO: khong quet duoc nhanh remote ({exc}). Ma cap ra CHI dua tren thu muc local.")

    if not scanned_remote:
        print("CANH BAO: chua quet duoc nhanh remote nao. Chay `git fetch --all` roi goi lai "
              "truoc khi dung ma nay, neu khong van co the trung voi luong khac.")

    n = 1
    while n in used:
        n += 1
    return f"FINDING-{day}-{member}-{n:03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Doi chieu Defects/FINDING-* voi INDEX.md")
    ap.add_argument("--next-id", metavar="MEMBER",
                    help="in ra ma FINDING ke tiep cho nguoi lam do (vd TUY), quet ca nhanh remote")
    ap.add_argument("--day", default=None, help="ngay YYYYMMDD cho --next-id (mac dinh: hom nay)")
    ap.add_argument("--check", action="store_true", help="exit 1 neu lech (dung cho hook)")
    ap.add_argument("--stub", action="store_true", help="them dong skeleton cho finding thieu dong")
    ap.add_argument("--fix-header", action="store_true", help="sua so dem trong dong _Cap nhat:_")
    ap.add_argument("--hook", action="store_true",
                    help="che do hook Stop: in ra stderr, exit 2 (CHAN) neu lech")
    ap.add_argument("--project", default=None)
    a = ap.parse_args()

    out = sys.stderr if a.hook else sys.stdout

    def say(*x):
        print(*x, file=out)

    proj = a.project or active_project()
    defects = ROOT / "Projects" / proj / "Defects"
    index = defects / "INDEX.md"
    if not defects.is_dir():
        say(f"[defects-index] KHONG thay {defects} - bo qua.")
        return 0

    if a.next_id:
        day = a.day or _dt.date.today().strftime("%Y%m%d")
        say(next_id(defects, a.next_id, day))
        return 0

    findings, problems = collect(defects)
    missing, dangling, dupes = reconcile(index, findings)
    hcount = header_count(index)

    say(f"[defects-index] project={proj} | thu muc={len(findings)} | dong INDEX={len(findings) - len(missing) + len(dangling)}")

    if a.stub and missing:
        text = index.read_text(encoding="utf-8")
        sep = TABLE_SEP_RE.search(text)
        if not sep:
            say("  !! khong tim thay dong phan cach bang trong INDEX.md - khong stub duoc")
        else:
            add = ""
            for fid in missing:
                f = next(x for x in findings if x["id"] == fid)
                add += (f"| {fid} | {f['jira'] or 'NEED_FILL'} | {f['module'] or 'NEED_FILL'} | "
                        f"{'NEED_FILL'} | {f['lifecycle'] or 'NEED_FILL'} / NEED_FILL | NEED_FILL | "
                        f"**NEED_FILL — dong stub tu defects-index.py, phai dien noi dung that** "
                        f"(title: {(f.get('title') or '')[:150]}) |\n")
            text = text[:sep.end() + 1] + add + text[sep.end() + 1:]
            index.write_text(text, encoding="utf-8")
            say(f"  + da them {len(missing)} dong stub - PHAI dien noi dung that thay cho NEED_FILL")
            findings, problems = collect(defects)
            missing, dangling, dupes = reconcile(index, findings)

    if a.fix_header:
        text = index.read_text(encoding="utf-8")
        n = len(findings)
        today = _dt.date.today().isoformat()
        new, cnt = HEADER_RE.subn(lambda m: f"{m.group(1)}{today}{m.group(3)}{n}{m.group(5)}", text, count=1)
        if cnt:
            index.write_text(new, encoding="utf-8")
            say(f"  + header -> '{today} | {n} finding'")
            hcount = n
        else:
            say("  !! khong tim thay dong '_Cap nhat: ... N finding_' de sua")

    bad = False
    for p in problems:
        say("  " + p)
        bad = True
    for i in missing:
        say(f"  MISSING_ROW      {i}: co thu muc + manifest nhung KHONG co dong trong INDEX.md "
              f"-> recall-gate skill 01 KHONG THAY finding nay")
        bad = True
    for i in dangling:
        say(f"  DANGLING_ROW     {i}: co dong trong INDEX.md nhung KHONG co thu muc/manifest "
              f"-> chi muc tro vao nguon rong")
        bad = True
    for i in dupes:
        say(f"  DUPLICATE_ROW    {i}: xuat hien nhieu lan trong INDEX.md")
        bad = True
    if hcount is not None and hcount != len(findings):
        say(f"  HEADER_COUNT     header ghi {hcount} finding nhung thuc te co {len(findings)} thu muc "
              f"(chay --fix-header)")
        bad = True

    if not bad:
        say("  OK - INDEX.md khop 100% voi Defects/. Khong co finding nao vo hinh.")
        return 0

    say("\n  => LECH. Cach sua: tao thu muc+manifest cho dong mo coi, hoac chay --stub roi DIEN NOI DUNG THAT,")
    say("     roi --fix-header. Dung xoa dong de 'cho het loi' - se lam mat vet finding.")
    if a.hook:
        say("     (hook Stop CHAN vi bat bien Defects/ <-> INDEX.md bi vo - sua roi ket thuc lai)")
        return 2
    return 1 if a.check else 0


if __name__ == "__main__":
    sys.exit(main())
