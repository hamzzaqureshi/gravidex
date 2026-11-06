#!/usr/bin/env python3
"""GraviDex Capability Consolidation Engine.

Automates evaluation and consolidation of new or candidate skills into
curated capability packs or retained specialists:
  - MERGE: Integrate core workflows into existing pack.
  - RETAIN: Keep as an independent specialist.
  - REFERENCE: Extract progressive disclosure references.
  - EXTRACT: Retain specific tools, scripts, or checklists.
  - REJECT: Archive as unsuitable/redundant with rationale.

Zero external dependencies (Python standard library only).
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CAPABILITIES_DIR = REPO_ROOT / "CAPABILITIES"
SOURCES_DIR = REPO_ROOT / "SOURCES"
SOURCE_INDEX_FILE = SOURCES_DIR / "source-index.yaml"
CAP_REGISTRY_FILE = CAPABILITIES_DIR / "capability-registry.yaml"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def list_capabilities():
    caps = []
    for cat in ["curated", "retained-specialists"]:
        cat_dir = CAPABILITIES_DIR / cat
        if not cat_dir.exists():
            continue
        for d in sorted(cat_dir.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                prov_file = d / "provenance.yaml"
                src_count = 0
                if prov_file.exists():
                    txt = prov_file.read_text(encoding="utf-8")
                    src_count = txt.count("- source_id:") or txt.count("- id:")
                caps.append({
                    "id": d.name,
                    "category": cat,
                    "path": d,
                    "sources_count": src_count,
                })
    return caps


def evaluate_candidate(source_path: Path):
    if not source_path.exists():
        return None, f"Source path '{source_path}' does not exist."

    skill_md = source_path / "SKILL.md" if source_path.is_dir() else source_path
    if not skill_md.exists() or not skill_md.is_file():
        return None, f"SKILL.md not found in '{source_path}'."

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)

    name = name_match.group(1).strip().strip('"').strip("'") if name_match else source_path.name
    desc = desc_match.group(1).strip().strip('"').strip("'") if desc_match else "No description provided."

    # Identify matching capability by domain keywords
    keywords = {
        "frontend-engineering": ["react", "next.js", "frontend", "webgl", "three.js", "browser", "component"],
        "backend-engineering": ["backend", "api", "rest", "express", "endpoint", "database", "mcp"],
        "interface-design": ["design", "ui", "ux", "apple", "hig", "aesthetic", "taste", "unslop", "slop"],
        "design-systems": ["palette", "color", "token", "sanzo", "diagram", "theme", "logo", "brand"],
        "quality-engineering": ["test", "tdd", "e2e", "playwright", "eval", "qa", "verification", "coverage"],
        "security-audit": ["security", "vulnerability", "audit", "owasp", "cve", "injection", "scanner"],
        "technical-documentation": ["readme", "documentation", "docs", "adr", "onboarding", "git"],
        "autonomous-agent-engineering": ["agent", "socratic", "court", "arena", "ponytail", "router", "subagent"],
    }

    text_lower = (name + " " + desc + " " + content[:2000]).lower()
    scores = {}
    for cap_id, kw_list in keywords.items():
        score = sum(text_lower.count(kw) for kw in kw_list)
        if score > 0:
            scores[cap_id] = score

    best_match = max(scores.items(), key=lambda x: x[1])[0] if scores else "autonomous-agent-engineering"

    return {
        "id": name,
        "name": name,
        "description": desc,
        "path": source_path,
        "suggested_target": best_match,
        "scores": scores,
    }, None


def apply_consolidation(candidate: dict, target_cap: str, disposition: str, dry_run: bool = True):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    actions = []

    target_dir = CAPABILITIES_DIR / "curated" / target_cap
    if not target_dir.exists():
        target_dir = CAPABILITIES_DIR / "retained-specialists" / target_cap
    if not target_dir.exists():
        return False, [f"Target capability '{target_cap}' does not exist."]

    actions.append(f"Target Capability: {target_cap} ({target_dir})")
    actions.append(f"Disposition: {disposition}")

    if disposition == "MERGE":
        actions.append(f"Merge workflows from {candidate['id']} into {target_cap}/SKILL.md")
        actions.append(f"Archive full upstream snapshot into SOURCES/repositories/")
    elif disposition == "REFERENCE":
        ref_file = target_dir / "references" / f"{candidate['id']}.md"
        actions.append(f"Extract progressive disclosure reference to {ref_file}")
    elif disposition == "RETAIN":
        actions.append(f"Stage as independent retained specialist under CAPABILITIES/retained-specialists/{candidate['id']}")
    elif disposition == "EXTRACT":
        actions.append(f"Extract reusable scripts or templates from {candidate['id']}")
    elif disposition == "REJECT":
        actions.append(f"Reject candidate {candidate['id']} - document rejection rationale")

    # Update provenance.yaml
    prov_file = target_dir / "provenance.yaml"
    if prov_file.exists():
        actions.append(f"Record provenance entry in {prov_file}")
        if not dry_run:
            prov_text = prov_file.read_text(encoding="utf-8")
            new_entry = (
                f"  - source_id: local-candidate/{candidate['id']}\n"
                f"    repository: local\n"
                f"    upstream_commit: initial\n"
                f"    contribution: [consolidated via {disposition}]\n"
                f"    integration_type: {disposition.lower()}\n"
            )
            if "sources:" in prov_text:
                prov_text = prov_text.replace("sources:\n", f"sources:\n{new_entry}")
                prov_file.write_text(prov_text, encoding="utf-8")

    return True, actions


def main():
    parser = argparse.ArgumentParser(description="GraviDex Skill Consolidation Engine")
    parser.add_argument("--list", action="store_true", help="List available capability packs")
    parser.add_argument("--source", help="Path or ID of candidate skill to evaluate/consolidate")
    parser.add_argument("--target-capability", help="Target capability pack (e.g. frontend-engineering)")
    parser.add_argument(
        "--disposition",
        choices=["MERGE", "RETAIN", "REFERENCE", "EXTRACT", "REJECT"],
        default="MERGE",
        help="Consolidation disposition",
    )
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview actions without modifying disk")
    parser.add_argument("--apply", action="store_true", help="Apply consolidation changes on disk")
    args = parser.parse_args()

    if args.list:
        caps = list_capabilities()
        print("=" * 72)
        print("                 GRAVIDEX CAPABILITY DIRECTORY")
        print("=" * 72)
        print(f"{'Capability':<32} | {'Category':<20} | {'Sources':<8}")
        print("-" * 72)
        for c in caps:
            print(f"{c['id']:<32} | {c['category']:<20} | {c['sources_count']:<8}")
        print("=" * 72)
        return 0

    if not args.source:
        parser.print_help()
        return 0

    source_path = Path(args.source)
    if not source_path.exists():
        # Check SKILLS/candidates/
        cand_path = REPO_ROOT / "SKILLS" / "candidates" / args.source
        if cand_path.exists():
            source_path = cand_path

    cand_data, err = evaluate_candidate(source_path)
    if err:
        print(f"Error evaluating candidate: {err}")
        return 1

    target_cap = args.target_capability or cand_data["suggested_target"]
    is_dry_run = not args.apply

    print("=" * 72)
    print("             GRAVIDEX SKILL CONSOLIDATION ENGINE")
    print("=" * 72)
    print(f"Candidate:         {cand_data['id']}")
    print(f"Suggested Target:  {cand_data['suggested_target']}")
    print(f"Selected Target:   {target_cap}")
    print(f"Disposition:       {args.disposition}")
    print(f"Mode:              {'DRY-RUN (Preview)' if is_dry_run else 'APPLY (Modifying disk)'}\n")

    success, actions = apply_consolidation(cand_data, target_cap, args.disposition, dry_run=is_dry_run)
    for a in actions:
        print(f"  * {a}")

    print("\n" + "=" * 72)
    print("Consolidation evaluation completed successfully.")
    print("=" * 72)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

