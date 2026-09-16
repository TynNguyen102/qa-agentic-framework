#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lam sach / kiem chung dau vet project trong khung QA.

Chay `python tools/sanitize-check.py --apply` de thay the theo bang luat ben duoi.
Chay `python tools/sanitize-check.py` (khong co --apply) de CHI QUET va bao cao,
khong sua gi — dung sau khi lam sach de kiem chung con sot khong.

Vi sao giu lai file nay trong khung: moi lan fork khung cho mot project moi, chay
lai `--apply` voi bang luat cua rieng project do la don gian nhat, va lan nao cung
co bao cao "con sot gi" thay vi tin tuong bang cam tinh.
"""
import argparse
import collections
import io
import os
import re
import sys

# Bang thay the. THU TU QUAN TRONG: mau dai/cu the phai dung TRUOC mau chung,
# neu khong "tutus.security" se bi "tutus" nuot mat phan duoi.
RULES = [
    # --- host / URL day du ---
    (r"https://dev-app\.tutus\.security", "https://dev-app.example.local"),
    (r"https://dev-api\.tutus\.security", "https://dev-api.example.local"),
    (r"https://dev-keycloak\.tutus\.security", "https://dev-keycloak.example.local"),
    (r"dev-app\.tutus\.security", "dev-app.example.local"),
    (r"dev-api\.tutus\.security", "dev-api.example.local"),
    (r"dev-keycloak\.tutus\.security", "dev-keycloak.example.local"),
    (r"app\.vinsoc\.ai", "app.example.com"),
    (r"vinsoc-ai\.atlassian\.net", "YOUR-SITE.atlassian.net"),
    (r"gitlab\.vinsmartfuture\.tech", "gitlab.example.local"),
    (r"vinsmartfuture\.tech", "example.local"),
    # --- email / nguoi ---
    (r"v\.[a-z]+[0-9]*@vinsoc\.vn", "qa-lead@example.com"),
    (r"@vinsoc\.vn", "@example.com"),
    # --- repo / group ---
    (r"vinsoc-ai/soc-platform", "YOUR-GROUP/YOUR-SUBGROUP"),
    (r"vinsoc-ai%2Fsoc-platform", "YOUR-GROUP%2FYOUR-SUBGROUP"),
    (r"vinsoc-spec", "SPEC-REPO"),
    (r"soc-portal-be", "BACKEND-SERVICE"),
    (r"soc-portal", "PRODUCT-APP"),
    (r"soc-eco", "PRODUCT-REPO"),
    (r"tutus-automation", "AUTOMATION-REPO"),
    (r"\bsoc-ai\b", "YOUR-REALM"),
    # --- ten project / to chuc ---
    (r"TUTUS[-\s]Platform", "Example-Project"),
    (r"TUTUS", "Example"),
    (r"Tutus", "Example"),
    (r"tutus", "example"),
    (r"(?i)vin\s?soc", "YOUR-ORG"),
    (r"VinSOC", "YOUR-ORG"),
    (r"VINSOC", "YOUR-ORG"),
    (r"vinsoc", "your-org"),
    # --- ma ticket ---
    (r"\bSP-(\d{3,5})\b", r"DEMO-\1"),
    (r"project\s*=\s*SP\b", "project = DEMO"),
    (r"jira_project_key:\s*SP\b", "jira_project_key: DEMO"),
    # --- tai khoan test ---
    (r"\btest(0[1-9]|1[0-2])\b", r"qauser\1"),
    (r"automationtest", "automation-user"),
    # --- squad / sprint ---
    (r"Squad[-\s]?4", "Squad-D"),
    (r"Squad[-\s]?2", "Squad-B"),
    (r"Sprint\s+1[0-9]\b", "Sprint N"),
    (r"SP\s+Sprint\s+\d+", "DEMO Sprint N"),
]

# Sau khi --apply, khong duoc con dau vet nao khop cac mau nay.
LEAK_PATTERNS = [
    ("ten san pham", r"(?i)tutus"),
    ("ten to chuc", r"(?i)vinsoc"),
    ("ten ha tang", r"(?i)vinsmartfuture"),
    ("jira site that", r"vinsoc-ai\.atlassian\.net"),
    ("ma ticket that", r"\bSP-\d{3,5}\b"),
    ("repo san pham", r"soc-(eco|portal|ai)\b"),
    ("tai khoan test that", r"\btest(0[1-9]|1[0-2])\b"),
    ("id trang Confluence", r"\b3[0-9]{8}\b"),
    ("IP noi bo", r"\b10\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b"),
    # --- bo sung sau khi lam sach lan dau: cac lop TUNG lot luoi ---
    ("ten cong ty", r"(?i)vin\s?group"),
    ("ten may that", r"\b[A-Z]{2,6}--[A-Z0-9]{4,}\b"),
    ("repo noi bo", r"(?i)\b(qc_soc_autotest|quality-control/|vinsoc-spec)\b"),
    ("ten nguoi Viet co dau", r"(?:Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Đào|Đinh|Tạ|Ly)\s+[A-ZÀ-ỹ][a-zà-ỹ]+\s+[A-ZÀ-ỹ][a-zà-ỹ]+"),
    ("email that", r"[a-zA-Z0-9._%+-]+@(?!example\.com)[a-zA-Z0-9.-]+\.(?:vn|ai|com|net)\b"),
    ("UNC share noi bo", r"\\\\\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\"),
    ("token co ve that", r"(?<![A-Za-z])(glpat-|xoxb-|ghp_|gho_|github_pat_|sk-[a-zA-Z0-9]{20})[A-Za-z0-9_-]{16,}"),
]

SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll",
    ".ico", ".woff", ".woff2", ".ttf", ".mp4", ".webm",
}
SKIP_DIR = {".git", "node_modules", "__pycache__", ".venv", "out"}


def walk_files(root="."):
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR]
        for fn in files:
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            yield os.path.join(cur, fn)


def rel(p):
    return p.replace(os.sep, "/").lstrip("./")


def apply_rules():
    compiled = [(re.compile(p), r) for p, r in RULES]
    hits = collections.Counter()
    touched = []
    for p in walk_files():
        if rel(p).endswith("tools/sanitize-check.py"):
            continue  # khong tu sua chinh minh
        try:
            s = io.open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        orig = s
        for rx, rep in compiled:
            s, n = rx.subn(rep, s)
            if n:
                hits[rx.pattern] += n
        if s != orig:
            io.open(p, "w", encoding="utf-8", newline="").write(s)
            touched.append(rel(p))
    print("File da sua: %d" % len(touched))
    print("\nSo lan thay the theo luat:")
    for pat, n in hits.most_common():
        print("  %5d  %s" % (n, pat))
    return touched


def scan_leaks():
    compiled = [(name, re.compile(p)) for name, p in LEAK_PATTERNS]
    found = collections.defaultdict(list)
    for p in walk_files():
        if rel(p).endswith("tools/sanitize-check.py"):
            continue  # file nay CHUA bang luat nen dinh mau la dung
        try:
            lines = io.open(p, encoding="utf-8").read().split("\n")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            for name, rx in compiled:
                m = rx.search(line)
                if m:
                    found[name].append((rel(p), i, line.strip()[:110]))
    if not found:
        print("SACH: khong con dau vet nao khop bang kiem chung.")
        return 0
    total = 0
    for name, rows in sorted(found.items()):
        print("\n### %s — %d cho" % (name, len(rows)))
        for f, i, line in rows[:25]:
            print("  %s:%d  %s" % (f, i, line))
        if len(rows) > 25:
            print("  ... con %d dong nua" % (len(rows) - 25))
        total += len(rows)
    print("\nTONG CON SOT: %d cho — phai xem tay tung cho." % total)
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Thuc su sua file. Khong co co nay thi chi quet va bao cao.")
    a = ap.parse_args()
    if a.apply:
        apply_rules()
        print("\n" + "=" * 70)
        print("KIEM CHUNG SAU KHI SUA")
        print("=" * 70)
    return 1 if scan_leaks() else 0


if __name__ == "__main__":
    sys.exit(main())
