#!/usr/bin/env python3
"""GraviDex Inventory Generator.

Discovers, inventories, and maps all installed and candidate skills across:
  - Canonical repository: SKILLS/approved/, SKILLS/candidates/
  - Antigravity IDE: Global (~/.gemini/config/skills/) and Workspace (.agents/skills/)
  - OpenCode: Global (~/.config/opencode/skills/) and Workspace (.opencode/skills/)
  - Claude Code: Global (~/.claude/skills/) and Workspace (.claude/skills/)

Zero external dependencies (Python standard library only).
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SEARCH_LOCATIONS = [
    ("Canonical Approved", REPO_ROOT / "SKILLS" / "approved"),
    ("Canonical Candidates", REPO_ROOT / "SKILLS" / "candidates"),
    ("Repository Root", REPO_ROOT),
    ("Antigravity Global", Path(os.path.expanduser("~/.gemini/config/skills"))),
    ("Antigravity Workspace", REPO_ROOT / ".agents" / "skills"),
    ("OpenCode Global", Path(os.path.expanduser("~/.config/opencode/skills"))),
    ("OpenCode Workspace", REPO_ROOT / ".opencode" / "skills"),
    ("Claude Code Global", Path(os.path.expanduser("~/.claude/skills"))),
    ("Claude Code Workspace", REPO_ROOT / ".claude" / "skills"),
]


def parse_frontmatter(skill_md_path: Path):
    if not skill_md_path.is_file():
        return {}
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}

    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
    if not match:
        return {}

    meta = {}
    lines = match.group(1).splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def inspect_skill_dir(path: Path):
    file_count = 0
    total_size = 0
    subdirs = []
    has_scripts = False
    has_tests = False
    has_references = False

    for root, dirs, files in os.walk(path):
        # Exclude hidden subdirectories or git
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for d in dirs:
            if d == "scripts":
                has_scripts = True
            elif d in ("tests", "test"):
                has_tests = True
            elif d in ("references", "reference"):
                has_references = True
        for f in files:
            p = Path(root) / f
            file_count += 1
            try:
                total_size += p.stat().st_size
            except OSError:
                pass

    return {
        "file_count": file_count,
        "total_size": total_size,
        "has_scripts": has_scripts,
        "has_tests": has_tests,
        "has_references": has_references,
    }


def scan_skills():
    inventory = []
    seen_ids = {}

    for label, base_path in SEARCH_LOCATIONS:
        if not base_path.exists():
            continue

        # In root repo, only scan directories containing SKILL.md (not all folders)
        candidates = []
        if base_path == REPO_ROOT:
            candidates = [
                d for d in base_path.iterdir()
                if d.is_dir() and not d.name.startswith((".", "_")) and d.name not in ("SKILLS", "AUDIT", "PATCHES", "TESTS", "scripts", "bin")
            ]
        else:
            candidates = [d for d in base_path.iterdir() if d.is_dir() and not d.name.startswith(".")]

        for s_dir in sorted(candidates, key=lambda x: x.name):
            skill_md = s_dir / "SKILL.md"
            if not skill_md.is_file():
                continue

            meta = parse_frontmatter(skill_md)
            stats = inspect_skill_dir(s_dir)

            record = {
                "id": s_dir.name,
                "name": meta.get("name", s_dir.name),
                "description": meta.get("description", "No description provided"),
                "location_label": label,
                "path": str(s_dir),
                "file_count": stats["file_count"],
                "total_size_bytes": stats["total_size"],
                "has_scripts": stats["has_scripts"],
                "has_tests": stats["has_tests"],
                "has_references": stats["has_references"],
            }
            inventory.append(record)
            seen_ids.setdefault(s_dir.name, []).append(label)

    return inventory, seen_ids


def generate_markdown_report(inventory, seen_ids):
    lines = [
        "# GraviDex Inventory Report",
        "",
        f"Generated automatically by GraviDex on local environment.",
        f"Total skill instances discovered: {len(inventory)}",
        f"Unique skill identifiers: {len(seen_ids)}",
        "",
        "## Deployment Matrix by Scope",
        "",
        "| Skill ID | Approved | Candidate | Root | Antigravity Global | Antigravity Workspace | OpenCode | Files | Size (KB) |",
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|",
    ]

    # Group by unique ID
    unique_ids = sorted(seen_ids.keys())
    for s_id in unique_ids:
        instances = [item for item in inventory if item["id"] == s_id]
        primary = instances[0]
        scopes = seen_ids[s_id]

        approved_mark = "YES" if "Canonical Approved" in scopes else "-"
        candidate_mark = "YES" if "Canonical Candidates" in scopes else "-"
        root_mark = "YES" if "Repository Root" in scopes else "-"
        antigravity_global_mark = "YES" if "Antigravity Global" in scopes else "-"
        antigravity_ws_mark = "YES" if "Antigravity Workspace" in scopes else "-"
        opencode_mark = "YES" if ("OpenCode Global" in scopes or "OpenCode Workspace" in scopes) else "-"

        size_kb = round(primary["total_size_bytes"] / 1024, 1)

        lines.append(
            f"| `{s_id}` | {approved_mark} | {candidate_mark} | {root_mark} | {antigravity_global_mark} | {antigravity_ws_mark} | {opencode_mark} | {primary['file_count']} | {size_kb} KB |"
        )

    lines.extend([
        "",
        "## Detailed Inventory Listing",
        "",
    ])

    for s_id in unique_ids:
        instances = [item for item in inventory if item["id"] == s_id]
        p = instances[0]
        scopes = ", ".join(seen_ids[s_id])
        lines.extend([
            f"### `{s_id}`",
            f"- **Display Name:** {p['name']}",
            f"- **Description:** {p['description']}",
            f"- **Deployed Scopes:** {scopes}",
            f"- **Primary Path:** `{p['path']}`",
            f"- **Structure:** {p['file_count']} files ({round(p['total_size_bytes']/1024, 1)} KB) | Scripts: {p['has_scripts']} | Tests: {p['has_tests']} | References: {p['has_references']}",
            "",
        ])

    return "\n".join(lines) + "\n"


def main():
    save_report = "--save" in sys.argv or "-s" in sys.argv
    as_json = "--json" in sys.argv

    inventory, seen_ids = scan_skills()

    if as_json:
        print(json.dumps({"total_instances": len(inventory), "unique_skills": len(seen_ids), "items": inventory}, indent=2))
        return

    md_report = generate_markdown_report(inventory, seen_ids)

    if save_report:
        out_path = REPO_ROOT / "AUDIT" / "INVENTORY.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_report, encoding="utf-8")
        print(f"Inventory saved successfully to {out_path} ({len(inventory)} instances, {len(seen_ids)} unique skills)")
    else:
        print(f"\nGRAVIDEX INVENTORY: Discovered {len(inventory)} instances across {len(seen_ids)} unique skills.\n")
        print(f"{'Skill ID':<32} | {'Scopes':<30} | {'Files':<6} | {'Size'}")
        print("-" * 80)
        for s_id in sorted(seen_ids.keys()):
            scopes = ", ".join(seen_ids[s_id])
            primary = [x for x in inventory if x["id"] == s_id][0]
            size_kb = f"{round(primary['total_size_bytes']/1024, 1)} KB"
            print(f"{s_id:<32} | {scopes[:30]:<30} | {primary['file_count']:<6} | {size_kb}")
        print("-" * 80)
        print("Run with --save to write full report to AUDIT/INVENTORY.md\n")


if __name__ == "__main__":
    main()

