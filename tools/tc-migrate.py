#!/usr/bin/env python3
"""Ho tro chuyen file TC van xuoi -> khoi ```yaml case:``` may doc duoc.

BOI CANH: 108/125 file TC chua co khoi `case:` nen `tc-status.py` khong trich duoc so that.
Chuyen tay 108 file la rat lau; nhung chuyen TU DONG hoan toan thi NGUY HIEM — verdict la
ket luan chat luong, doan sai la bao cao sai.

VI VAY script nay co 3 rang buoc cung, khong duoc noi long:
  1. KHONG BAO GIO ghi de vao file TC goc. Chi sinh file canh `<ten>.case-draft.md`.
  2. KHONG BAO GIO tu che verdict. Chi chep lai token da CO SAN trong bang van xuoi.
     Khong doc duoc thi bo qua va bao cao, tuyet doi khong mac dinh NOT_RUN/PASS.
  3. Moi khoi sinh ra deu mang `state: DESIGNED` + `note` ghi ro la DRAFT phai nguoi doi chieu.
     `state` that (EXECUTED/PROVEN) chi nguoi moi dat duoc, vi no keo theo yeu cau evidence.

Dung:
  python tools/tc-migrate.py --report                 # xem ton dong, khong ghi gi
  python tools/tc-migrate.py --draft <file.md>        # sinh ban nhap cho 1 file
  python tools/tc-migrate.py --draft-all              # sinh ban nhap cho moi file chuyen duoc
"""
import argparse
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ROOT = os.path.join("Projects", "Example-Project", "Modules")

VERDICTS = ["PASS", "FAIL", "BLOCKED", "NEED_DATA", "NEED_CONFIRM", "NOT_RUN", "NOT_TESTABLE"]
# Chi nhan token DUNG Y NGUYEN trong enum. Bieu tuong (checkmark / X) KHONG duoc coi la verdict:
# chung xuat hien ca trong cot "da review", "ap dung", "bat buoc" -> doc nham la bao cao sai.
VERDICT_RE = re.compile(r"\b(" + "|".join(VERDICTS) + r")\b")
CASE_ID_RE = re.compile(r"^\|\s*\*{0,2}((?:TC|VP|SEC|CHK)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\*{0,2}\s*\|")
HAS_BLOCK_RE = re.compile(r"^```yaml\s*$", re.M)


# Khong phai moi file trong thu muc TC/ deu la SO GHI KET QUA.
# Truoc 2026-09-16 bao cao noi "108 file TC van xuoi" — con so do THOI PHONG, vi no dem ca
# tai lieu ho tro (review yeu cau, thiet ke test, du lieu test...). Nhung file do KHONG co
# case nao de ghi verdict, nen chung KHONG phai ton dong.
SUPPORT_SUFFIX = ("_requirement-review.md", "_test-design.md", "_test-data.md",
                  "_testcase-review.md", "_coverage-audit.md", "_execution-prep.md",
                  "_execution-readiness.md", "_test-plan-va-risk.md", "_retest-plan.md",
                  "_jira-subtask-drafts.md", "_jira-subtasks-draft.md", "_review-requirements.md",
                  "_testrail-import-preview.md", "_test-report.md", "_DATA-REQUEST.md")
LEDGER_SUFFIX = ("_testcases.md", "_execution-ledger.md", "_testcases-va-ledger.md",
                 "_execution-api.md", "_checklist-thuc-thi.md")


def file_kind(path):
    name = os.path.basename(path)
    if name.endswith(LEDGER_SUFFIX):
        return "LEDGER"
    if name.endswith(SUPPORT_SUFFIX):
        return "HO_TRO"
    return "KHAC"


def tc_files(root):
    out = []
    for dirpath, _, files in os.walk(os.path.join(BASE, root)):
        if os.sep + "TC" not in dirpath + os.sep:
            continue
        for f in files:
            if f.endswith(".md") and not f.endswith(".case-draft.md"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def scan(path):
    """Tra ve (da_co_block, [(case_id, verdict_hoac_None, dong_goc)])."""
    text = read(path)
    if HAS_BLOCK_RE.search(text):
        return True, []
    rows = []
    for line in text.splitlines():
        m = CASE_ID_RE.match(line)
        if not m:
            continue
        case_id = m.group(1)
        # Chi tim verdict trong PHAN CON LAI cua dong, sau cot ID.
        rest = line[m.end():]
        vm = VERDICT_RE.search(rest)
        rows.append((case_id, vm.group(1) if vm else None, line.strip()))
    return False, rows


def classify(rows):
    if not rows:
        return "KHONG_DOC_DUOC_CASE"
    with_v = sum(1 for _, v, _ in rows if v)
    if with_v == 0:
        return "CO_CASE_KHONG_CO_VERDICT"
    if with_v < len(rows):
        return "CO_VERDICT_MOT_PHAN"
    return "CHUYEN_DUOC"


def report(root):
    files = tc_files(root)
    done, buckets = [], {}
    for p in files:
        has, rows = scan(p)
        if has:
            done.append(p)
            continue
        buckets.setdefault(classify(rows), []).append((p, rows))

    pending = [p for p in files if p not in done]
    kinds = {}
    for p in pending:
        kinds.setdefault(file_kind(p), []).append(p)

    print("== tc-migrate --report ==")
    print("root: {}".format(root))
    print("Tong file trong thu muc TC/ : {}".format(len(files)))
    print("Da co khoi `case:`          : {}".format(len(done)))
    print("Chua co khoi `case:`        : {}".format(len(pending)))
    print()
    print("Trong so chua co, phan theo LOAI FILE:")
    print("  LEDGER (so ghi ket qua)   : {:3d}  <== DAY moi la ton dong that".format(len(kinds.get("LEDGER", []))))
    print("  HO_TRO (review/thiet ke)  : {:3d}      khong co case de ghi verdict — KHONG phai ton dong".format(len(kinds.get("HO_TRO", []))))
    print("  KHAC  (can mat nguoi xem) : {:3d}".format(len(kinds.get("KHAC", []))))
    print()
    order = ["CHUYEN_DUOC", "CO_VERDICT_MOT_PHAN", "CO_CASE_KHONG_CO_VERDICT", "KHONG_DOC_DUOC_CASE"]
    meaning = {
        "CHUYEN_DUOC": "moi dong case deu co verdict hop le -> sinh nhap duoc",
        "CO_VERDICT_MOT_PHAN": "mot so case co verdict -> sinh nhap phan doc duoc, phan con lai de trong",
        "CO_CASE_KHONG_CO_VERDICT": "doc ra case nhung KHONG co verdict -> phai nguoi dien, script khong doan",
        "KHONG_DOC_DUOC_CASE": "khong nhan ra dong case nao -> phai chuyen tay hoan toan",
    }
    for k in order:
        items = buckets.get(k, [])
        print("[{}] {} file  — {}".format(k, len(items), meaning[k]))
        for p, rows in items[:8]:
            nv = sum(1 for _, v, _ in rows if v)
            print("     {}  ({} case, {} co verdict)".format(os.path.relpath(p, BASE), len(rows), nv))
        if len(items) > 8:
            print("     ... con {} file nua".format(len(items) - 8))
        print()
    print("LUU Y: script KHONG tu dien verdict. Nhom CO_CASE_KHONG_CO_VERDICT va")
    print("       KHONG_DOC_DUOC_CASE bat buoc phai nguoi lam — do la ket luan chat luong.")
    return 0


def draft(path):
    has, rows = scan(path)
    rel = os.path.relpath(path, BASE)
    if has:
        print("BO QUA  {} — da co khoi `case:`".format(rel))
        return None
    usable = [(c, v) for c, v, _ in rows if v]
    if not usable:
        print("BO QUA  {} — khong doc duoc verdict nao, script khong duoc phep doan".format(rel))
        return None

    out = path[:-3] + ".case-draft.md"
    lines = [
        "<!-- BAN NHAP do tools/tc-migrate.py sinh tu bang van xuoi cua {}.".format(os.path.basename(path)),
        "     CHUA DUOC MERGE khi chua co nguoi doi chieu tung case voi ket qua chay that.",
        "     - verdict duoi day la CHEP LAI tu bang van xuoi, khong phai chay lai.",
        "     - state de DESIGNED cho moi case: state EXECUTED/PROVEN keo theo yeu cau evidence,",
        "       chi nguoi moi dat duoc sau khi doi chieu bang chung.",
        "     - case khong doc duoc verdict thi KHONG co mat o day (xem --report). -->",
        "",
    ]
    for case_id, verdict in usable:
        lines += [
            "#### {}".format(case_id),
            "```yaml",
            "case: {}".format(case_id),
            "verdict: {}".format(verdict),
            "state: DESIGNED",
            'note: "DRAFT tc-migrate — chep tu bang van xuoi, QC phai doi chieu bang chung truoc khi merge."',
            "```",
            "",
        ]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    skipped = len(rows) - len(usable)
    print("SINH    {}  ({} case{})".format(
        os.path.relpath(out, BASE), len(usable),
        ", bo qua {} case khong co verdict".format(skipped) if skipped else ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--draft")
    ap.add_argument("--draft-all", action="store_true")
    a = ap.parse_args()

    if a.draft:
        p = a.draft if os.path.isabs(a.draft) else os.path.join(BASE, a.draft)
        if not os.path.isfile(p):
            print("Khong thay file: {}".format(a.draft))
            return 1
        draft(p)
        return 0
    if a.draft_all:
        n = 0
        for p in tc_files(a.root):
            if draft(p):
                n += 1
        print("\nDa sinh {} ban nhap. KHONG file TC goc nao bi sua.".format(n))
        return 0
    return report(a.root)


if __name__ == "__main__":
    sys.exit(main())
