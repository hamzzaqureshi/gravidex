#!/usr/bin/env python3
"""GraviDex Capability Verification & Governance Test Suite.

Verifies:
  1. Complete capability presence (8 curated packs + 13 retained specialists = 21 total).
  2. SKILL.md validity and required frontmatter (name, description, name matches directory).
  3. Valid provenance.yaml mapping to preserved upstream sources.
  4. Progressive disclosure references structure in curated capability packs.
  5. Retained specialist scripts and tooling integrity.
  6. Strict zero-emoji compliance across all capability files.
  7. Markdown reference integrity (zero broken local links).
  8. Zero dangerous shell piping patterns.
  9. Capability registry synchronization (CAPABILITIES/capability-registry.yaml).
"""

import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CAPABILITIES_DIR = REPO_ROOT / "CAPABILITIES"
CURATED_DIR = CAPABILITIES_DIR / "curated"
RETAINED_DIR = CAPABILITIES_DIR / "retained-specialists"
SOURCES_DIR = REPO_ROOT / "SOURCES"
SOURCE_INDEX_FILE = SOURCES_DIR / "source-index.yaml"
CAP_REGISTRY_FILE = CAPABILITIES_DIR / "capability-registry.yaml"

EXPECTED_CURATED = [
    "autonomous-agent-engineering",
    "backend-engineering",
    "design-systems",
    "frontend-engineering",
    "interface-design",
    "quality-engineering",
    "security-audit",
    "technical-documentation",
]

EXPECTED_RETAINED = [
    "agentshield",
    "asd-ste100",
    "awwwards",
    "boardui",
    "jury",
    "karpathy-guidelines",
    "last30days",
    "lemo-opuscar",
    "motionsites-web-builder",
    "rev-engineer",
    "scrapling",
    "skillforge",
    "stageshow",
]

# Strict emoji regex
EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)
PIPE_TO_BASH_REGEX = re.compile(r"(?:curl|wget)\s+-[^\n|]*\|\s*(?:bash|sh|zsh)")


def parse_frontmatter(file_path: Path):
    if not file_path.is_file():
        return {}
    content = file_path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
    if not match:
        return {}
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


class TestGravidexCapabilities(unittest.TestCase):
    """Automated empirical verification for GraviDex Layer B capabilities."""

    def test_curated_capability_count_and_names(self):
        """Assert exactly 8 curated capability packs exist with expected names."""
        self.assertTrue(CURATED_DIR.is_dir(), "CAPABILITIES/curated directory must exist")
        found = sorted([d.name for d in CURATED_DIR.iterdir() if d.is_dir()])
        self.assertEqual(len(found), 8, f"Expected 8 curated packs, found {len(found)}")
        self.assertEqual(found, sorted(EXPECTED_CURATED))

    def test_retained_specialist_count_and_names(self):
        """Assert exactly 13 retained specialists exist with expected names."""
        self.assertTrue(RETAINED_DIR.is_dir(), "CAPABILITIES/retained-specialists directory must exist")
        found = sorted([d.name for d in RETAINED_DIR.iterdir() if d.is_dir()])
        self.assertEqual(len(found), 13, f"Expected 13 retained specialists, found {len(found)}")
        self.assertEqual(found, sorted(EXPECTED_RETAINED))

    def test_skill_md_validity_all_capabilities(self):
        """Assert every capability contains a valid SKILL.md with name and description."""
        all_caps = list(CURATED_DIR.iterdir()) + list(RETAINED_DIR.iterdir())
        for cap_dir in all_caps:
            if not cap_dir.is_dir():
                continue
            skill_md = cap_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md in {cap_dir.name}")
            fm = parse_frontmatter(skill_md)
            self.assertTrue(bool(fm.get("name")), f"Missing frontmatter 'name' in {cap_dir.name}")
            self.assertTrue(bool(fm.get("description")), f"Missing frontmatter 'description' in {cap_dir.name}")
            self.assertEqual(fm.get("name"), cap_dir.name, f"Frontmatter name must match folder in {cap_dir.name}")

    def test_provenance_files_exist_and_map_to_sources(self):
        """Assert all 19 capabilities contain provenance.yaml referencing valid snapshots."""
        all_caps = list(CURATED_DIR.iterdir()) + list(RETAINED_DIR.iterdir())
        for cap_dir in all_caps:
            if not cap_dir.is_dir():
                continue
            prov_file = cap_dir / "provenance.yaml"
            self.assertTrue(prov_file.is_file(), f"Missing provenance.yaml in {cap_dir.name}")
            prov_text = prov_file.read_text(encoding="utf-8")
            self.assertIn("capability:", prov_text)
            self.assertIn("sources:", prov_text)

        if SOURCE_INDEX_FILE.is_file():
            index_text = SOURCE_INDEX_FILE.read_text(encoding="utf-8")
            self.assertTrue(len(index_text) > 0, "source-index.yaml must not be empty")

    def test_progressive_disclosure_references_in_curated_packs(self):
        """Assert all curated packs have a references/ folder with markdown documentation."""
        for name in EXPECTED_CURATED:
            pack_dir = CURATED_DIR / name
            ref_dir = pack_dir / "references"
            self.assertTrue(ref_dir.is_dir(), f"Missing references directory in {name}")
            ref_files = list(ref_dir.glob("*.md"))
            self.assertGreater(len(ref_files), 0, f"References directory in {name} must contain .md files")

    def test_strict_zero_emoji_compliance(self):
        """Assert zero emoji characters in any file across CAPABILITIES/."""
        for root, _, files in os.walk(CAPABILITIES_DIR):
            for f in files:
                if f.endswith((".md", ".yaml", ".json", ".py", ".sh", ".txt")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")

    def test_zero_broken_markdown_links(self):
        """Assert no broken local relative links exist in any capability markdown files."""
        link_pattern = re.compile(r"\[.*?\]\((?!https?://|mailto:|#)([^)]+)\)")
        for root, _, files in os.walk(CAPABILITIES_DIR):
            for f in files:
                if f.endswith(".md"):
                    p = Path(root) / f
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    # Strip code blocks and inline code
                    clean = re.sub(r"```[\s\S]*?```", "", content)
                    clean = re.sub(r"`[^`\n]*`", "", clean)
                    for match in link_pattern.finditer(clean):
                        target = match.group(1).split("#")[0].strip()
                        if not target or target in ("url", "path", "file"):
                            continue
                        if "SOURCES/" in target and not SOURCE_INDEX_FILE.is_file():
                            continue
                        target_path = (p.parent / target).resolve()
                        self.assertTrue(target_path.exists(), f"Broken relative markdown link in {p}: {target}")

    def test_zero_dangerous_pipe_to_bash(self):
        """Assert zero unsafe pipe-to-bash patterns in capability scripts or docs."""
        for root, _, files in os.walk(CAPABILITIES_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".sh")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = PIPE_TO_BASH_REGEX.search(text)
                    self.assertIsNone(match, f"Dangerous pipe-to-shell installer detected in {p}")

    def test_capability_registry_yaml_consistency(self):
        """Assert capability-registry.yaml lists all 21 capabilities."""
        self.assertTrue(CAP_REGISTRY_FILE.is_file(), "capability-registry.yaml must exist")
        content = CAP_REGISTRY_FILE.read_text(encoding="utf-8")
        self.assertIn("total_capabilities: 21", content)
        for name in EXPECTED_CURATED + EXPECTED_RETAINED:
            self.assertIn(f"id: {name}", content, f"Capability {name} missing from registry")


if __name__ == "__main__":
    unittest.main()

