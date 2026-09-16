#!/usr/bin/env python3
"""QA workspace maintenance CLI.

Minimal, stdlib-only (no PyYAML dependency — this workspace has no build system per AGENTS.md).
YAML files are parsed just enough to pull top-level `key: value` pairs; anything requiring real
YAML structure is treated as opaque text and checked for required substrings instead.

Subcommands:
  validate           Check required root files + required files for the active project exist.
  skills-check       Diff .agents/skills/ (canonical) against .claude/skills/ (mirror).
  skills-sync        Copy .agents/skills/ -> .claude/skills/.
  defects-validate   Check each Projects/<project>/Defects/FINDING-*/manifest.yaml has required fields.
  defects-render     Concatenate defect manifests into one index file (--output required).
"""
import argparse
import filecmp
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_ROOT_FILES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "CLAUDE.md",
    "project/active-project.yaml",
    "governance/knowledge-policy.yaml",
    "governance/audit-policy.yaml",
    "Config/QA-Agent/professional-coverage-model.yaml",
    "Config/QA-Agent/canonical-testcase-schema.yaml",
]

REQUIRED_PROJECT_FILES = [
    "CLAUDE.md",
    "CURRENT_STATE.md",
    "qa-config.yaml",
    "Config/agent-profile.yaml",
    "Config/defect-profile.yaml",
]

DEFECT_MANIFEST_REQUIRED_KEYS = [
    "lifecycle_status",
    "found_in_sprint",
]


def read_active_project():
    path = os.path.join(BASE, "project", "active-project.yaml")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    match = re.search(r"^active_project:\s*(\S+)", text, re.MULTILINE)
    return match.group(1) if match else None


def cmd_validate(args):
    ok = True
    for rel in REQUIRED_ROOT_FILES:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            print("MISSING (root): {}".format(rel))
            ok = False

    project = args.project or read_active_project()
    if not project:
        print("MISSING: project/active-project.yaml has no active_project set")
        ok = False
    else:
        project_dir = os.path.join(BASE, "Projects", project)
        if not os.path.isdir(project_dir):
            print("MISSING: Projects/{}/ does not exist".format(project))
            ok = False
        else:
            for rel in REQUIRED_PROJECT_FILES:
                path = os.path.join(project_dir, rel)
                if not os.path.exists(path):
                    print("MISSING (Projects/{}): {}".format(project, rel))
                    ok = False

    if ok:
        print("validate: OK ({})".format(project or "no active project"))
    return 0 if ok else 1


def _skill_dirs(root):
    path = os.path.join(BASE, root, "skills")
    if not os.path.isdir(path):
        return []
    return sorted(d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)))


def cmd_skills_check(args):
    canonical = os.path.join(BASE, ".agents", "skills")
    mirror = os.path.join(BASE, ".claude", "skills")
    canonical_dirs = set(_skill_dirs(".agents"))
    mirror_dirs = set(_skill_dirs(".claude"))

    ok = True
    for name in sorted(canonical_dirs - mirror_dirs):
        print("MISSING in mirror: {}".format(name))
        ok = False
    for name in sorted(mirror_dirs - canonical_dirs):
        print("EXTRA in mirror (not in canonical): {}".format(name))
        ok = False

    for name in sorted(canonical_dirs & mirror_dirs):
        src = os.path.join(canonical, name, "SKILL.md")
        dst = os.path.join(mirror, name, "SKILL.md")
        if os.path.isfile(src) and os.path.isfile(dst):
            if not filecmp.cmp(src, dst, shallow=False):
                print("DRIFT: {}/SKILL.md differs between .agents and .claude".format(name))
                ok = False
        elif os.path.isfile(src) != os.path.isfile(dst):
            print("DRIFT: {}/SKILL.md present on only one side".format(name))
            ok = False

    if ok:
        print("skills-check: OK, {} skills in sync".format(len(canonical_dirs)))
    return 0 if ok else 1


def cmd_skills_sync(args):
    canonical = os.path.join(BASE, ".agents", "skills")
    mirror = os.path.join(BASE, ".claude", "skills")
    if not os.path.isdir(canonical):
        print("No .agents/skills/ found — nothing to sync.")
        return 1

    synced = 0
    for name in sorted(_skill_dirs(".agents")):
        src_dir = os.path.join(canonical, name)
        dst_dir = os.path.join(mirror, name)
        os.makedirs(dst_dir, exist_ok=True)
        for fname in os.listdir(src_dir):
            src = os.path.join(src_dir, fname)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(dst_dir, fname))
                synced += 1
    print("skills-sync: copied {} files across {} skill folders.".format(
        synced, len(_skill_dirs(".agents"))))
    return 0


def cmd_defects_validate(args):
    projects_dir = os.path.join(BASE, "Projects")
    if not os.path.isdir(projects_dir):
        print("No Projects/ directory found.")
        return 1

    ok = True
    checked = 0
    for project in sorted(os.listdir(projects_dir)):
        defects_dir = os.path.join(projects_dir, project, "Defects")
        if not os.path.isdir(defects_dir):
            continue
        for finding in sorted(os.listdir(defects_dir)):
            finding_dir = os.path.join(defects_dir, finding)
            if not os.path.isdir(finding_dir):
                continue
            manifest = os.path.join(finding_dir, "manifest.yaml")
            if not os.path.isfile(manifest):
                print("MISSING manifest.yaml: Projects/{}/Defects/{}".format(project, finding))
                ok = False
                continue
            checked += 1
            with open(manifest, encoding="utf-8") as f:
                text = f.read()
            for key in DEFECT_MANIFEST_REQUIRED_KEYS:
                if not re.search(r"^{}:".format(re.escape(key)), text, re.MULTILINE):
                    print("MISSING key '{}': Projects/{}/Defects/{}/manifest.yaml".format(
                        key, project, finding))
                    ok = False

    if ok:
        print("defects-validate: OK, {} manifest(s) checked.".format(checked))
    return 0 if ok else 1


def cmd_defects_render(args):
    if not args.output:
        print("defects-render requires --output <path>")
        return 1

    projects_dir = os.path.join(BASE, "Projects")
    lines = ["# Defect / Regression Index", ""]
    total = 0
    for project in sorted(os.listdir(projects_dir)) if os.path.isdir(projects_dir) else []:
        defects_dir = os.path.join(projects_dir, project, "Defects")
        if not os.path.isdir(defects_dir):
            continue
        findings = sorted(d for d in os.listdir(defects_dir)
                           if os.path.isdir(os.path.join(defects_dir, d)))
        if not findings:
            continue
        lines.append("## {}".format(project))
        lines.append("")
        for finding in findings:
            manifest = os.path.join(defects_dir, finding, "manifest.yaml")
            status = "NO_MANIFEST"
            if os.path.isfile(manifest):
                with open(manifest, encoding="utf-8") as f:
                    text = f.read()
                match = re.search(r"^lifecycle_status:\s*(\S+)", text, re.MULTILINE)
                status = match.group(1) if match else "UNKNOWN"
            lines.append("- `{}` — {}".format(finding, status))
            total += 1
        lines.append("")

    out_path = os.path.join(BASE, args.output)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("defects-render: wrote {} ({} findings).".format(args.output, total))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Check required root + active-project files exist.")
    p_validate.add_argument("--project", help="Override the active project (defaults to project/active-project.yaml).")
    p_validate.set_defaults(func=cmd_validate)

    p_check = sub.add_parser("skills-check", help="Diff .agents/skills against .claude/skills.")
    p_check.set_defaults(func=cmd_skills_check)

    p_sync = sub.add_parser("skills-sync", help="Copy .agents/skills into .claude/skills.")
    p_sync.set_defaults(func=cmd_skills_sync)

    p_dval = sub.add_parser("defects-validate", help="Check defect manifests have required fields.")
    p_dval.set_defaults(func=cmd_defects_validate)

    p_dren = sub.add_parser("defects-render", help="Render a defect/regression index across all projects.")
    p_dren.add_argument("--output", required=True, help="Output path, relative to repo root.")
    p_dren.set_defaults(func=cmd_defects_render)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
