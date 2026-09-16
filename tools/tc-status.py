#!/usr/bin/env python3
"""tc-status.py — trich trang thai testcase tu khoi ```yaml `case:` trong CHINH file TC.

Lich su (dung xoa):
  `CURRENT_STATE.md` (chot 04/09) ghi "file MD + tc-status.py la source-of-truth cho testcase &
  PASS/FAIL, thay TestRail". Nhung den 2026-09-09 moi phat hien: `tools/tc-status.py` KHONG
  TON TAI va `git log --all -- tools/tc-status.py` TRONG => chua tung duoc commit. Muc schema
  cho khoi thuc thi cung khong ton tai (`git log --all -S execution_result` tren
  canonical-testcase-schema.yaml cung TRONG). Ca hai da duoc dung lai 09/09 va commit ngay.

Nguon schema: Config/QA-Agent/canonical-testcase-schema.yaml muc `execution_block`.
Khong dung pyyaml (workspace khong cai — da kiem 2026-09-09): parser tap con YAML du cho khoi nay.

Dung:
  python3 tools/tc-status.py                          # bang tong hop moi story
  python3 tools/tc-status.py --check                  # exit 1 neu sai schema (gan CI/hook)
  python3 tools/tc-status.py --story DEMO-7019          # loc theo story
  python3 tools/tc-status.py --root Projects/Example-Project/Modules/pentest
  python3 tools/tc-status.py --adoption               # file TC nao CHUA dung khoi `case:`
  python3 tools/tc-status.py --json                   # xuat JSON
  python3 tools/tc-status.py --csv out.csv            # xuat CSV
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FENCE_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.S)
VERDICTS = ["PASS", "FAIL", "BLOCKED", "NEED_DATA", "NEED_CONFIRM", "NOT_RUN", "NOT_TESTABLE"]
STATES = ["DESIGNED", "REVIEWED", "AUTOMATED", "EXECUTED", "PROVEN"]
STATE_ORDER = {s: i for i, s in enumerate(STATES)}
REQUIRED = ["case", "verdict", "state"]


def active_project() -> str:
    f = ROOT / "project" / "active-project.yaml"
    if f.exists():
        m = re.search(r"^active_project:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return "Example-Project"


def load_enums() -> tuple[list[str], list[str]]:
    """Doc enum tu canonical-testcase-schema.yaml; fallback ve hang so tren."""
    p = ROOT / "Config" / "QA-Agent" / "canonical-testcase-schema.yaml"
    if not p.exists():
        return VERDICTS, STATES
    t = p.read_text(encoding="utf-8", errors="replace")
    blk = re.search(r"^execution_block:\s*\n(.*?)(?=\n[a-z_]+:|\Z)", t, re.M | re.S)
    if not blk:
        return VERDICTS, STATES
    b = blk.group(1)

    def enum(name: str) -> list[str]:
        m = re.search(rf"^\s*{name}:\s*\n((?:\s*-\s*\S+.*\n)+)", b, re.M)
        if not m:
            return []
        return [x.strip() for x in re.findall(r"^\s*-\s*([A-Z_]+)", m.group(1), re.M)]

    return enum("verdict") or VERDICTS, enum("state") or STATES


def parse_block(raw: str) -> dict:
    """Parser tap con YAML: scalar `k: v` + list `k:` -> `- item`. Du cho execution_block."""
    out: dict = {}
    key = None
    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)-\s*(.*)$", line)
        if m and key:
            # BUG FIX 2026-09-09: `defect:` / `evidence:` co gia tri TRONG roi moi den cac dong "- item".
            # Truoc day dong "k:" trong set out[k]=None, va setdefault() KHONG ghi de None ->
            # moi item bi bo -> tool bao SAI la "defect rong" (da gap that voi TC-7060-07).
            if out.get(key) is None:
                out[key] = []
            if isinstance(out[key], list):
                out[key].append(m.group(2).strip().strip('"').strip("'"))
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).split(" #")[0].strip()
            if val in ("", "[]"):
                out[key] = [] if val == "[]" else None
            else:
                out[key] = val.strip('"').strip("'")
    return out


def story_of(path: pathlib.Path, blk: dict) -> str:
    m = re.search(r"(SP-\d+)", path.name)
    if m:
        return m.group(1)
    m = re.search(r"(SP-\d+)", str(blk.get("case") or ""))
    return m.group(1) if m else path.stem[:28]


def scan(root: pathlib.Path, enum_v: list[str], enum_s: list[str]):
    cases, problems, tc_files, files_with_blocks = [], [], [], set()
    for f in sorted(root.rglob("*.md")):
        if "/TC/" not in f.as_posix() and "\\TC\\" not in str(f):
            continue
        # Bo sung 2026-09-16: KHONG dem 2 loai file phu, neu khong so bi thoi len.
        #  - *.case-draft.md : ban nhap do tools/tc-migrate.py sinh, CHUA co nguoi doi chieu.
        #    Dem chung vao la bao cao coverage bang ket qua chua ai xac nhan.
        #  - _baseline-coverage.md : tai lieu tong hop, khong phai so ghi ket qua.
        if f.name.endswith(".case-draft.md") or f.name == "_baseline-coverage.md":
            continue
        tc_files.append(f)
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(ROOT).as_posix()
        for raw in FENCE_RE.findall(text):
            if not re.search(r"^\s*case:\s*\S", raw, re.M):
                continue
            files_with_blocks.add(rel)
            b = parse_block(raw)
            cid = b.get("case") or "<THIEU>"
            for k in REQUIRED:
                if not b.get(k):
                    problems.append(f"{rel} :: {cid} :: THIEU key bat buoc `{k}`")
            v, st = b.get("verdict"), b.get("state")
            if v and v not in enum_v:
                problems.append(f"{rel} :: {cid} :: verdict '{v}' KHONG thuoc enum {enum_v}")
            if st and st not in enum_s:
                problems.append(f"{rel} :: {cid} :: state '{st}' KHONG thuoc enum {enum_s}")
            if v == "PASS" and st in STATE_ORDER and STATE_ORDER[st] < STATE_ORDER["EXECUTED"]:
                problems.append(f"{rel} :: {cid} :: verdict PASS nhung state '{st}' chua toi EXECUTED "
                                f"-> chua chay thi khong the PASS")
            if st == "PROVEN" and not b.get("evidence"):
                problems.append(f"{rel} :: {cid} :: state PROVEN nhung `evidence` rong")
            if v == "FAIL" and not b.get("defect"):
                problems.append(f"{rel} :: {cid} :: verdict FAIL nhung `defect` rong -> no chua ghi")
            b["_file"], b["_story"] = rel, story_of(f, b)
            cases.append(b)
    return cases, problems, tc_files, files_with_blocks


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Trang thai testcase tu khoi `case:` trong file TC")
    ap.add_argument("--check", action="store_true", help="exit 1 neu sai schema")
    ap.add_argument("--story", default=None)
    ap.add_argument("--root", default=None)
    ap.add_argument("--adoption", action="store_true", help="liet ke file TC CHUA dung khoi case:")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()

    root = pathlib.Path(a.root) if a.root else ROOT / "Projects" / active_project() / "Modules"
    if not root.is_absolute():
        root = ROOT / root
    if not root.is_dir():
        print(f"[tc-status] KHONG thay {root}")
        return 0

    enum_v, enum_s = load_enums()
    cases, problems, tc_files, with_blocks = scan(root, enum_v, enum_s)
    if a.story:
        cases = [c for c in cases if c["_story"].upper() == a.story.upper()]

    if a.json:
        print(json.dumps({"cases": cases, "problems": problems}, ensure_ascii=False, indent=2))
        return 1 if (problems and a.check) else 0

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["story", "case", "verdict", "state", "priority", "run_at", "build", "file"])
            for c in cases:
                w.writerow([c["_story"], c.get("case"), c.get("verdict"), c.get("state"),
                            c.get("priority"), c.get("run_at"), c.get("build"), c["_file"]])
        print(f"[tc-status] da ghi CSV: {a.csv} ({len(cases)} case)")

    print(f"[tc-status] root={root.relative_to(ROOT).as_posix()} | file TC={len(tc_files)} "
          f"| file co khoi case:={len(with_blocks)} | case={len(cases)}")

    if cases:
        by_story: dict[str, dict[str, int]] = {}
        for c in cases:
            d = by_story.setdefault(c["_story"], {})
            d[c.get("verdict") or "?"] = d.get(c.get("verdict") or "?", 0) + 1
        print("\n  Story        | Tong | " + " | ".join(v[:11].ljust(11) for v in enum_v))
        print("  " + "-" * (15 + 7 + 14 * len(enum_v)))
        for st, d in sorted(by_story.items()):
            tot = sum(d.values())
            print(f"  {st:12s} | {tot:4d} | " + " | ".join(str(d.get(v, 0)).ljust(11) for v in enum_v))

    if a.adoption:
        missing = [f.relative_to(ROOT).as_posix() for f in tc_files
                   if f.relative_to(ROOT).as_posix() not in with_blocks]
        print(f"\n  [adoption] {len(with_blocks)}/{len(tc_files)} file TC dung khoi `case:`. "
              f"CHUA dung ({len(missing)}):")
        for m in missing:
            print("     - " + m)
        print("  => Nhung file nay KHONG doc duoc bang may, nen 'MD la source-of-truth cho PASS/FAIL'")
        print("     chi dung voi phan da co khoi `case:`. Chuyen dan sang khoi nay moi dong duoc.")

    if problems:
        print(f"\n  SAI SCHEMA ({len(problems)}):")
        for p in problems:
            print("   x " + p)
        print("  Nguon schema: Config/QA-Agent/canonical-testcase-schema.yaml muc `execution_block`")
        return 1 if a.check else 0

    print("\n  OK - khong co khoi `case:` nao sai schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
