#!/usr/bin/env python3
"""Sinh khung `_baseline-coverage.md` cho tung module TU DU LIEU THAT trong repo.

VI SAO CAN: skill 01 (recall-gate) yeu cau doc baseline cua module truoc khi thiet ke US moi,
nhung 1/13 module co file nay. Khong co no thi phien sau de viet trung case hoac bo sot regression.

VI SAO KHONG VIET TAY 12 BAN: ban mau (module inventory) la phan tich tay rat day — vieckhac
nhau tung module. Viet tay 12 ban MONG se tao ao giac "da co baseline" ma noi dung rong,
nguy hiem hon la khong co.

VI VAY script nay chi sinh phan MAY BIET CHAC:
  - liet ke dung cac file TC co that trong module,
  - dem case may doc duoc (tu khoi ```yaml case:```) theo tung verdict,
  - noi THANG file nao chua co so may doc duoc.
Moi nhan dinh chat luong (feature nao con ho, case nao phai regression) deu de TRONG
kem danh dau CAN_NGUOI_BO_SUNG — script khong duoc phep doan thay QC.

Dung:
  python tools/gen-baseline-coverage.py --dry-run     # xem se sinh gi
  python tools/gen-baseline-coverage.py               # sinh cho module chua co file
  python tools/gen-baseline-coverage.py --force       # ghi de ca module da co (can than)
"""
import argparse
import os
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_ROOT = os.path.join("Projects", "Example-Project", "Modules")
TODAY = "2026-09-16"

BLOCK_RE = re.compile(r"```yaml\s*\n(.*?)```", re.S)
# Khong dung \b o CUOI: ten file kieu "SP-7060_testcases.md" co dau "_" ngay sau so, ma "_" la
# word char nen \b khong khop -> lan sinh dau 16/09 muc "story cham toi" rong o CA 11 file.
STORY_RE = re.compile(r"\b(SP-\d{3,5})(?![0-9])")

# Dau hieu file do CHINH script nay sinh ra. File khong mang dau hieu nay la nguoi viet tay,
# va --force KHONG duoc phep de len. Da xay ra 16/09: --force ghi de ban viet tay cua module
# inventory (70 dong phan tich tay), phai khoi phuc bang `git checkout`. Neu file do chua commit
# thi da mat han.
GENERATED_MARK = 'generated_by: "tools/gen-baseline-coverage.py"'


def modules(root):
    d = os.path.join(BASE, root)
    return sorted(n for n in os.listdir(d)
                  if os.path.isdir(os.path.join(d, n)))


def tc_dir(root, mod):
    return os.path.join(BASE, root, mod, "TC")


def parse_blocks(path):
    """Tra ve list (case_id, verdict, state) doc duoc tu khoi yaml."""
    out = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for body in BLOCK_RE.findall(text):
        if not re.search(r"^case:", body, re.M):
            continue
        g = lambda k: (re.search(r"^{}:\s*(\S+)".format(k), body, re.M) or [None, None])[1]
        out.append((g("case"), g("verdict"), g("state")))
    return out


def build(root, mod):
    d = tc_dir(root, mod)
    if not os.path.isdir(d):
        return None
    files = sorted(f for f in os.listdir(d) if f.endswith(".md")
                   and not f.startswith("_") and not f.endswith(".case-draft.md"))
    if not files:
        return None

    rows, total = [], Counter()
    stories = set()
    for f in files:
        p = os.path.join(d, f)
        blocks = parse_blocks(p)
        stories.update(STORY_RE.findall(f))
        if blocks:
            c = Counter(v for _, v, _ in blocks if v)
            total.update(c)
            summary = " · ".join("{} {}".format(n, k) for k, n in sorted(c.items()))
            rows.append((f, str(len(blocks)), summary or "(khong doc duoc verdict)"))
        else:
            rows.append((f, "—", "**chưa có khối `case:`** — không ra số máy đọc được"))

    machine = sum(1 for f in files if parse_blocks(os.path.join(d, f)))
    L = []
    A = L.append
    A("# Module `{}` — Baseline Coverage".format(mod))
    A("")
    A("> Đọc file này **trước khi** chạy `06-generate-functional-testcases` cho US mới thuộc module")
    A("> `{}`, để biết feature nào đã có case và tránh viết trùng hoặc bỏ sót regression.".format(mod))
    A("")
    A("> ⚠️ **Bản này do `tools/gen-baseline-coverage.py` sinh tự động ngày {}.**".format(TODAY))
    A("> Máy chỉ dựng được phần **đếm được**: danh sách file có thật và số case theo verdict đọc từ")
    A("> khối ```` ```yaml case:` ````. Mọi **nhận định chất lượng** — feature nào còn hở, case nào")
    A("> phải đưa vào regression — đang **để trống**, đánh dấu `CẦN_NGƯỜI_BỔ_SUNG`. Script không được")
    A("> phép đoán thay QC. Mẫu đã hoàn chỉnh để đối chiếu: [`inventory/TC/_baseline-coverage.md`](../../inventory/TC/_baseline-coverage.md).")
    A("")
    A("- module: {}".format(mod))
    A('- updated_at: "{}"'.format(TODAY))
    A("- generated_by: \"tools/gen-baseline-coverage.py\"")
    A("- status: DRAFT — **chưa qua review Lead**, chưa dùng làm oracle")
    A("- story chạm tới: {}".format(", ".join("[{}](https://YOUR-SITE.atlassian.net/browse/{})".format(s, s)
                                              for s in sorted(stories)) or "—"))
    A("")
    A("## 1. File testcase có thật trong module")
    A("")
    A("| File | Case máy đọc được | Phân bố verdict |")
    A("|---|---|---|")
    for f, n, s in rows:
        A("| [{}]({}) | {} | {} |".format(f, f, n, s))
    A("")
    A("**Tổng máy đọc được:** {} / {} file có khối `case:`.".format(machine, len(files)))
    if total:
        A("")
        A("| Verdict | Số case |")
        A("|---|---|")
        for k, n in sorted(total.items(), key=lambda x: -x[1]):
            A("| `{}` | {} |".format(k, n))
    else:
        A("")
        A("⚠️ **Module này chưa có case nào máy đọc được** — mọi kết quả đang nằm ở bảng văn xuôi,")
        A("`tc-status.py` không trích ra số được. Xem tồn đọng bằng `python tools/tc-migrate.py --report`.")
    A("")
    A("## 2. Bản đồ tính năng đã có case  `CẦN_NGƯỜI_BỔ_SUNG`")
    A("")
    A("| Trang / route | Story nguồn | Số case | File | Trạng thái tổng |")
    A("|---|---|---|---|---|")
    A("| _(chưa điền)_ | | | | |")
    A("")
    A("## 3. NEED_CONFIRM / BLOCKED phải verify lại  `CẦN_NGƯỜI_BỔ_SUNG`")
    A("")
    A("_(chưa điền — liệt kê từng case còn treo và điều kiện gỡ treo)_")
    A("")
    A("## 4. Vùng CHƯA có case nào  `CẦN_NGƯỜI_BỔ_SUNG`")
    A("")
    A("_(chưa điền — đây là mục quan trọng nhất: nói rõ phần nào của module chưa ai test,")
    A("để phiên sau không tưởng nhầm là đã phủ)_")
    A("")
    A("## 5. Case phải chạy lại khi US mới chạm module này  `CẦN_NGƯỜI_BỔ_SUNG`")
    A("")
    A("_(chưa điền)_")
    A("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=MODULES_ROOT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    made = skipped = 0
    for mod in modules(a.root):
        d = tc_dir(a.root, mod)
        out = os.path.join(d, "_baseline-coverage.md")
        if os.path.exists(out):
            with open(out, encoding="utf-8") as fh:
                existing = fh.read()
            if GENERATED_MARK not in existing:
                # Nguoi viet tay -> KHONG de len, ke ca khi co --force.
                print("GIU     {}/TC/_baseline-coverage.md — NGUOI VIET TAY, --force cung khong de len".format(mod))
                skipped += 1
                continue
            if not a.force:
                print("BO QUA  {}/TC/_baseline-coverage.md — da co (dung --force de sinh lai)".format(mod))
                skipped += 1
                continue
        content = build(a.root, mod)
        if content is None:
            print("BO QUA  {} — khong co thu muc TC/ hoac khong co file .md".format(mod))
            skipped += 1
            continue
        if a.dry_run:
            print("SE SINH {}  ({} dong)".format(os.path.relpath(out, BASE), content.count("\n")))
        else:
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(content)
            print("SINH    {}".format(os.path.relpath(out, BASE)))
        made += 1
    print("\n{} file{}, bo qua {}.".format(made, " se sinh" if a.dry_run else " da sinh", skipped))
    print("NHAC: moi file sinh ra deu con muc CAN_NGUOI_BO_SUNG — chua dung lam oracle duoc.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
