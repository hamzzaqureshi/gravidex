#!/usr/bin/env python3
"""Cross-Platform Installer for GraviDex Capabilities Suite.

Works on Linux, macOS, and Windows.
Supports:
  - Antigravity IDE Global (~/.gemini/config/skills) [Default]
  - Antigravity IDE Project (.agents/skills)
  - Claude Code Global (~/.claude/skills)
  - Claude Code Project (.claude/skills)
  - OpenCode Global (~/.config/opencode/skills)
  - OpenCode Project (.opencode/skills)
  - Custom target paths
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

# Active GraviDex Capabilities (8 Curated Packs + 11 Retained Specialists)
SKILLS = [
    ("autonomous-agent-engineering", "Core agent engineering: Ponytail minimal diffs, Socratic gates, Court & Arena deliberation, Model Router"),
    ("backend-engineering", "Production REST APIs, Express/Next.js routes, cross-language typed error boundaries, and MCP servers"),
    ("design-systems", "Design tokens, TypeUI 67 themes, Sanzo Wada historical palettes, SVG brand identity, and editorial diagrams"),
    ("frontend-engineering", "React/Next.js component patterns, render optimization, Three.js WebGL scenes, and Playwright browser QA"),
    ("interface-design", "Apple HIG craft, 22-framework UI/UX guidelines, 9-pass anti-slop redline, and Swiss typography"),
    ("quality-engineering", "Test-driven development (TDD, 80%+ coverage), empirical verification gates (Rigor), and formal eval harnesses"),
    ("security-audit", "OWASP Top 10 hunting, coverage ledgers, AST security analysis, and static code reviews"),
    ("technical-documentation", "README-driven development (50-point rubric), Architectural Decision Records (ADRs), onboarding guides, git workflows"),
    ("agentshield", "Security auditor for AI agent harnesses, MCP configurations, hook safety, and prompt injection detection"),
    ("asd-ste100", "Simplified Technical English (Issue 9) & Karpathy 80% Pragmatic Mode: zero-ambiguity agent instructions and linter"),
    ("awwwards", "Award-caliber website builder from one-line prompt: art direction, WebGL, page transitions, browser QA"),
    ("boardui", "React design system for agentic interfaces: 69 source components, 400+ semantic tokens, React Aria, Tailwind CSS v4"),
    ("jury", "Objective website scoring the way an Awwwards jury would: blind critic model, LCP/CLS/FPS/a11y audits, ranked fixes"),
    ("last30days", "Real-time cross-platform social consensus, crowd pulse, and temporal research engine"),
    ("lemo-opuscar", "Algorithmic film directing and production in code: 67 styles, deterministic rendering, TTS voice, procedural audio"),
    ("motionsites-web-builder", "Award-level cinematic landing pages: 40 prompt examples, media shelf, 55+ motion recipes, screenshot QA"),
    ("rev-engineer", "Reverse engineering target router and deconstruction tools for native, web, and packaged binaries"),
    ("scrapling", "Adaptive web scraping, stealth browsing, Cloudflare Turnstile bypass, and concurrent spiders"),
    ("skillforge", "Autonomous agent skill lifecycle management, specification generation, regression testing, and doctor"),
]

BUNDLES = {
    "curated": [
        "autonomous-agent-engineering",
        "backend-engineering",
        "design-systems",
        "frontend-engineering",
        "interface-design",
        "quality-engineering",
        "security-audit",
        "technical-documentation",
    ],
    "specialists": [
        "agentshield",
        "asd-ste100",
        "awwwards",
        "boardui",
        "jury",
        "last30days",
        "lemo-opuscar",
        "motionsites-web-builder",
        "rev-engineer",
        "scrapling",
        "skillforge",
    ],
    "design": [
        "design-systems",
        "interface-design",
        "frontend-engineering",
        "awwwards",
        "boardui",
        "jury",
        "motionsites-web-builder",
        "lemo-opuscar",
    ],
    "engineering": [
        "autonomous-agent-engineering",
        "backend-engineering",
        "quality-engineering",
        "security-audit",
        "technical-documentation",
        "agentshield",
        "asd-ste100",
        "rev-engineer",
        "scrapling",
        "skillforge",
    ],
}

SCRIPT_DIR = Path(__file__).resolve().parent

IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo", ".DS_Store", "node_modules",
    ".court", ".impeccable", ".rigor", ".artist", "dist"
)


def resolve_skill_source(name: str) -> Path:
    candidates = [
        SCRIPT_DIR / "CAPABILITIES" / "curated" / name,
        SCRIPT_DIR / "CAPABILITIES" / "retained-specialists" / name,
        SCRIPT_DIR / ".agents" / "skills" / name,
        SCRIPT_DIR / ".claude" / "skills" / name,
        SCRIPT_DIR / ".opencode" / "skills" / name,
        SCRIPT_DIR / "skills" / name,
        SCRIPT_DIR / name,
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def list_skills():
    print(f"\nAvailable Capabilities ({len(SKILLS)} total):")
    print("-" * 72)
    for idx, (name, desc) in enumerate(SKILLS, 1):
        print(f"  {idx:>2}. {name:<30} - {desc}")
    print("\nCurated Bundles:")
    print(f"  - curated     (8 packs): {', '.join(BUNDLES['curated'])}")
    print(f"  - specialists (11 skills): {', '.join(BUNDLES['specialists'])}")
    print(f"  - design      (8 skills): {', '.join(BUNDLES['design'])}")
    print(f"  - engineering (10 skills): {', '.join(BUNDLES['engineering'])}")
    print("-" * 72)
    sys.exit(0)


def copy_skill(src: Path, dest: Path, dry_run: bool = False):
    if dry_run:
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=IGNORE_PATTERNS)
    # Set execution permissions on scripts if on POSIX
    if os.name == "posix":
        for folder in ["scripts", "bin"]:
            target_dir = dest / folder
            if target_dir.is_dir():
                for p in target_dir.rglob("*"):
                    if p.is_file() and p.suffix in (".py", ".sh", ".cjs", ".js", ""):
                        try:
                            p.chmod(p.stat().st_mode | 0o755)
                        except OSError:
                            pass


def prompt_selection(all_names):
    """Interactive selector for target directory and skills."""
    print("=" * 72)
    print("       GraviDex Capabilities Suite - Guided Installer")
    print("=" * 72)

    # 1. Target Directory
    print("\nStep 1: Choose destination:")
    print("  1) Antigravity Global        (~/.gemini/config/skills) [Recommended]")
    print("  2) Current Project Workspace (./.agents/skills)        [Project-scoped]")
    print("  3) Claude Code Global        (~/.claude/skills)        [Claude CLI]")
    print("  4) Claude Code Project       (./.claude/skills)")
    print("  5) OpenCode Global           (~/.config/opencode/skills)")
    print("  6) OpenCode Project          (./.opencode/skills)")
    print("  7) Custom Directory\n")

    t_choice = input("Select destination [1-7] (default: 1): ").strip() or "1"
    home = Path.home()

    if t_choice == "1":
        target_dir = home / ".gemini" / "config" / "skills"
    elif t_choice == "2":
        target_dir = Path(".").resolve() / ".agents" / "skills"
    elif t_choice == "3":
        target_dir = home / ".claude" / "skills"
    elif t_choice == "4":
        target_dir = Path(".").resolve() / ".claude" / "skills"
    elif t_choice == "5":
        target_dir = home / ".config" / "opencode" / "skills"
    elif t_choice == "6":
        target_dir = Path(".").resolve() / ".opencode" / "skills"
    elif t_choice == "7":
        custom_input = input("Enter custom path: ").strip()
        if not custom_input:
            print("Error: Target path cannot be empty.", file=sys.stderr)
            sys.exit(1)
        target_dir = Path(custom_input).resolve()
    else:
        target_dir = home / ".gemini" / "config" / "skills"

    # 2. Scope Selection
    print("\nStep 2: Choose capabilities to install:")
    print("  1) Install All 19 Capabilities [Recommended - Complete Suite]")
    print("  2) Curated Capability Packs    (8 packs: autonomous-agent, backend, design, frontend...)")
    print("  3) Retained Specialists        (11 skills: agentshield, asd-ste100, boardui, jury...)")
    print("  4) Design & Frontend Bundle    (8 skills: design-systems, interface-design, boardui...)")
    print("  5) Engineering Bundle          (10 skills: autonomous-agent, backend, quality, security...)")
    print("  6) Custom Pick                 (select by numbers e.g. 1, 8, 15)\n")

    s_choice = input("Select skills [1-6] (default: 1): ").strip() or "1"

    if s_choice == "1":
        selected = all_names
    elif s_choice == "2":
        selected = BUNDLES["curated"]
    elif s_choice == "3":
        selected = BUNDLES["specialists"]
    elif s_choice == "4":
        selected = BUNDLES["design"]
    elif s_choice == "5":
        selected = BUNDLES["engineering"]
    elif s_choice == "6":
        print("\nAvailable capabilities:")
        for idx, (name, _) in enumerate(SKILLS, 1):
            print(f"  {idx:>2}) {name}")
        raw_picks = input("\nEnter numbers or names separated by commas: ").strip()
        selected = []
        for token in raw_picks.split(","):
            token = token.strip()
            if not token:
                continue
            if token.isdigit():
                num = int(token)
                if 1 <= num <= len(SKILLS):
                    selected.append(SKILLS[num - 1][0])
            elif token in all_names:
                selected.append(token)
            else:
                print(f"Warning: Ignoring unknown token '{token}'")
        if not selected:
            print("No valid skills selected. Defaulting to all.")
            selected = all_names
    else:
        selected = all_names

    return target_dir, selected


def main():
    parser = argparse.ArgumentParser(
        description="Install GraviDex Capabilities Suite locally or globally."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-g", "--global", dest="is_global", action="store_true",
        help="Install globally for Antigravity IDE (~/.gemini/config/skills)"
    )
    group.add_argument(
        "-p", "--project", nargs="?", const=".", metavar="DIR",
        help="Install locally into project repository (.agents/skills)"
    )
    group.add_argument(
        "-c", "--claude", action="store_true",
        help="Install globally for Claude Code (~/.claude/skills)"
    )
    group.add_argument(
        "--claude-project", nargs="?", const=".", metavar="DIR",
        help="Install locally for Claude Code project (.claude/skills)"
    )
    group.add_argument(
        "--opencode", action="store_true",
        help="Install globally for OpenCode (~/.config/opencode/skills)"
    )
    group.add_argument(
        "--opencode-project", nargs="?", const=".", metavar="DIR",
        help="Install locally for OpenCode project (.opencode/skills)"
    )
    group.add_argument(
        "--custom", metavar="DIR",
        help="Install into custom destination path"
    )

    parser.add_argument(
        "-a", "--all", action="store_true",
        help="Install all 19 capabilities without prompting"
    )
    parser.add_argument(
        "-b", "--bundle", choices=["curated", "specialists", "design", "engineering"],
        help="Install a curated bundle of capabilities"
    )
    parser.add_argument(
        "-s", "--skills", metavar="LIST",
        help="Comma-separated subset of skills to install"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="List available capabilities and bundles"
    )
    parser.add_argument(
        "-t", "--test", action="store_true",
        help="Run verification test runner after install"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true",
        help="Simulate installation without writing files"
    )

    args = parser.parse_args()

    if args.list:
        list_skills()

    all_names = [s[0] for s in SKILLS]

    # Resolve selected skills from CLI
    if args.skills:
        selected = [s.strip() for s in args.skills.split(",") if s.strip()]
        for s in selected:
            if s not in all_names:
                print(f"Error: Unknown skill '{s}'. Available: {', '.join(all_names)}", file=sys.stderr)
                sys.exit(1)
    elif args.bundle:
        selected = BUNDLES[args.bundle]
    elif args.all:
        selected = all_names
    else:
        selected = None

    home = Path.home()
    target_dir = None

    if args.is_global:
        target_dir = home / ".gemini" / "config" / "skills"
    elif args.project:
        target_dir = Path(args.project).resolve() / ".agents" / "skills"
    elif args.claude:
        target_dir = home / ".claude" / "skills"
    elif args.claude_project:
        target_dir = Path(args.claude_project).resolve() / ".claude" / "skills"
    elif args.opencode:
        target_dir = home / ".config" / "opencode" / "skills"
    elif args.opencode_project:
        target_dir = Path(args.opencode_project).resolve() / ".opencode" / "skills"
    elif args.custom:
        target_dir = Path(args.custom).resolve()

    # If neither target nor skills were fully specified, run interactive mode
    if target_dir is None or selected is None:
        if sys.stdin.isatty():
            t_prompt, s_prompt = prompt_selection(all_names)
            if target_dir is None:
                target_dir = t_prompt
            if selected is None:
                selected = s_prompt
        else:
            if target_dir is None:
                target_dir = home / ".gemini" / "config" / "skills"
            if selected is None:
                selected = all_names

    print(f"\nTarget Directory: {target_dir}")
    print(f"Selected ({len(selected)}/{len(SKILLS)}): {', '.join(selected)}")

    if args.dry_run:
        print("\n[Dry Run] No files written.")
        sys.exit(0)

    target_dir.mkdir(parents=True, exist_ok=True)

    installed_count = 0
    for name in selected:
        src = resolve_skill_source(name)
        if not src or not src.is_dir():
            print(f"  Warning: Skipping missing capability: {name}")
            continue
        dest = target_dir / name
        print(f"  Installing {name}...")
        copy_skill(src, dest, dry_run=args.dry_run)
        installed_count += 1

    print(f"\nSuccessfully installed {installed_count} capability(ies) into {target_dir}\n")

    if args.test:
        test_script = SCRIPT_DIR / "test_all.py"
        if test_script.is_file():
            print("Running test suite verification...")
            subprocess.run([sys.executable, "-B", str(test_script)], check=False)


if __name__ == "__main__":
    main()
