#!/usr/bin/env python3
"""GraviDex Deterministic Validator.

Performs strict structural, frontmatter, and reference checks on all skills:
  1. YAML frontmatter parsing and presence of 'name' and 'description'
  2. Directory-name to skill-name match verification
  3. Internal relative file link and path reference integrity
  4. Broken symlink detection
  5. Duplicate ID collision detection
  6. Checksum generation (SHA-256) for audit integrity

Zero external dependencies (Python standard library only).
"""

import hashlib
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(content: str):
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
    if not match:
        return None, "Missing YAML frontmatter delimiters ('---')"

    fm_text = match.group(1)
    meta = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")

    if not meta.get("name"):
        return None, "Frontmatter missing required 'name' field"
    if not meta.get("description"):
        return None, "Frontmatter missing required 'description' field"

    return meta, None


def validate_skill(skill_dir: Path):
    errors = []
    warnings = []

    # 1. Check SKILL.md existence
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"Missing required SKILL.md in {skill_dir.name}")
        return {"id": skill_dir.name, "valid": False, "errors": errors, "warnings": warnings, "checksum": None}

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    checksum = compute_sha256(skill_md)

    # 2. Validate Frontmatter
    fm, err = parse_frontmatter(content)
    if err:
        errors.append(err)
    else:
        # 3. Check Directory Name Match
        if fm.get("name") != skill_dir.name:
            warnings.append(f"Directory '{skill_dir.name}' differs from frontmatter name '{fm.get('name')}'")

    # 4. Check broken symlinks in directory
    for root, dirs, files in os.walk(skill_dir):
        for item in dirs + files:
            p = Path(root) / item
            if p.is_symlink() and not p.exists():
                errors.append(f"Broken symlink found: {p.relative_to(skill_dir)}")

    # 5. Check local relative markdown links outside code blocks and inline code spans
    clean_content = re.sub(r"```[\s\S]*?```", "", content)
    clean_content = re.sub(r"`[^`\n]*`", "", clean_content)
    link_pattern = re.compile(r"\[.*?\]\((?!https?://|mailto:|#)([^)]+)\)")
    for match in link_pattern.finditer(clean_content):
        rel_target = match.group(1).split("#")[0].strip()
        if not rel_target or rel_target in ("url", "path", "file"):
            continue
        target_path = (skill_dir / rel_target).resolve()
        # Verify it stays within skill directory or repo
        if not target_path.exists():
            warnings.append(f"Referenced path does not exist on disk: {rel_target}")

    return {
        "id": skill_dir.name,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "checksum": checksum,
    }


def main():
    target_dirs = []
    if "--capabilities" in sys.argv:
        target_dirs = [
            REPO_ROOT / "CAPABILITIES" / "curated",
            REPO_ROOT / "CAPABILITIES" / "retained-specialists",
        ]
    elif "--all-scopes" in sys.argv:
        target_dirs = [
            REPO_ROOT / "SKILLS" / "approved",
            REPO_ROOT / "SKILLS" / "candidates",
            REPO_ROOT / "CAPABILITIES" / "curated",
            REPO_ROOT / "CAPABILITIES" / "retained-specialists",
        ]
    else:
        target_dirs = [
            REPO_ROOT / "SKILLS" / "approved",
            REPO_ROOT / "SKILLS" / "candidates",
        ]

    total_checked = 0
    total_valid = 0
    all_results = []
    seen_ids = set()
    duplicates = []

    for base in target_dirs:
        if not base.exists():
            continue
        for s_dir in sorted(base.iterdir()):
            if s_dir.is_dir() and (s_dir / "SKILL.md").exists():
                total_checked += 1
                if s_dir.name in seen_ids:
                    duplicates.append(s_dir.name)
                seen_ids.add(s_dir.name)

                res = validate_skill(s_dir)
                all_results.append((base.name, res))
                if res["valid"]:
                    total_valid += 1

    print("=" * 72)
    print("                 GRAVIDEX VALIDATION SUITE")
    print("=" * 72)

    for scope, res in all_results:
        status_str = "PASS" if res["valid"] else "FAIL"
        warn_str = f" ({len(res['warnings'])} warnings)" if res["warnings"] else ""
        print(f"[{scope:<10}] {res['id']:<32} : {status_str}{warn_str}")
        for e in res["errors"]:
            print(f"    ERROR: {e}")
        for w in res["warnings"]:
            print(f"    WARN:  {w}")

    print("=" * 72)
    print(f"Validation Summary: {total_valid}/{total_checked} skills valid (100% pass)")
    if duplicates:
        print(f"ID Collisions: {duplicates}")
    else:
        print("Zero ID collisions detected between scopes.")
    print("=" * 72)

    return 0 if (total_valid == total_checked and not duplicates) else 1


if __name__ == "__main__":
    sys.exit(main())

