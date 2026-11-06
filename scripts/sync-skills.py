#!/usr/bin/env python3
"""GraviDex Multi-Platform Synchronizer.

Deploys and synchronizes canonical skills from SKILLS/approved/ and SKILLS/candidates/
to supported AI agent platforms:
  - Google Antigravity IDE (Workspace: .agents/skills/, Global: ~/.gemini/config/skills/)
  - OpenCode (Workspace: .opencode/skills/, Global: ~/.config/opencode/skills/)
  - Claude Code (Workspace: .claude/skills/, Global: ~/.claude/skills/)

Zero external dependencies (Python standard library only).
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PLATFORM_TARGETS = {
    "antigravity-ws": REPO_ROOT / ".agents" / "skills",
    "antigravity-global": Path(os.path.expanduser("~/.gemini/config/skills")),
    "opencode-ws": REPO_ROOT / ".opencode" / "skills",
    "opencode-global": Path(os.path.expanduser("~/.config/opencode/skills")),
    "claude-ws": REPO_ROOT / ".claude" / "skills",
    "claude-global": Path(os.path.expanduser("~/.claude/skills")),
}


def sync_skill(src_dir: Path, dest_base: Path, dry_run: bool = False):
    dest_dir = dest_base / src_dir.name
    action = "CREATE" if not dest_dir.exists() else "SYNC"

    if dry_run:
        print(f"  [DRY-RUN] {action}: {src_dir.name} -> {dest_dir}")
        return True

    try:
        dest_base.mkdir(parents=True, exist_ok=True)
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(src_dir, dest_dir)
        print(f"  [SUCCESS] {action}: {src_dir.name} -> {dest_dir}")
        return True
    except PermissionError:
        print(f"  [PERMISSION] Cannot write to {dest_dir} (sandbox read-only mount). Run with BypassSandbox if host target.")
        return False
    except Exception as e:
        print(f"  [ERROR] Failed to sync {src_dir.name} to {dest_dir}: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    scope = "approved"
    if "--capabilities" in sys.argv or "--curated" in sys.argv:
        scope = "capabilities"
    elif "--all" in sys.argv:
        scope = "all"
    elif "--candidates" in sys.argv:
        scope = "candidates"

    selected_target = "all"
    for arg in sys.argv:
        if arg.startswith("--target="):
            selected_target = arg.split("=", 1)[1]

    sources = []
    if scope == "capabilities":
        cur_dir = REPO_ROOT / "CAPABILITIES" / "curated"
        spec_dir = REPO_ROOT / "CAPABILITIES" / "retained-specialists"
        if cur_dir.exists():
            sources.extend([d for d in sorted(cur_dir.iterdir()) if d.is_dir()])
        if spec_dir.exists():
            sources.extend([d for d in sorted(spec_dir.iterdir()) if d.is_dir()])
    else:
        if scope in ("approved", "all"):
            app_dir = REPO_ROOT / "SKILLS" / "approved"
            if app_dir.exists():
                sources.extend([d for d in sorted(app_dir.iterdir()) if d.is_dir()])

        if scope in ("candidates", "all"):
            cand_dir = REPO_ROOT / "SKILLS" / "candidates"
            if cand_dir.exists():
                sources.extend([d for d in sorted(cand_dir.iterdir()) if d.is_dir()])

    targets_to_run = PLATFORM_TARGETS if selected_target == "all" else {selected_target: PLATFORM_TARGETS[selected_target]}

    print("=" * 72)
    print("                 GRAVIDEX MULTI-PLATFORM SYNCHRONIZER")
    print("=" * 72)
    print(f"Source Scope:   {scope} ({len(sources)} skills)")
    print(f"Target Scope:   {selected_target}")
    print(f"Execution Mode: {'DRY-RUN' if dry_run else 'LIVE SYNC'}\n")

    for t_name, t_path in targets_to_run.items():
        print(f"--- Synchronizing to target: {t_name} ({t_path}) ---")
        success_count = 0
        for s in sources:
            if sync_skill(s, t_path, dry_run=dry_run):
                success_count += 1
        print(f"Finished {t_name}: {success_count}/{len(sources)} synchronized.\n")

    print("=" * 72)
    print("Synchronization pipeline execution completed.")
    print("=" * 72)


if __name__ == "__main__":
    main()

