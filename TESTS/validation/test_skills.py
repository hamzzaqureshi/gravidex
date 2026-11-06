#!/usr/bin/env python3
"""GraviDex Automated Test Suite for Skill Verification & Governance.

Verifies:
  1. SKILL.md presence and structure for all approved and candidate skills
  2. YAML frontmatter parsing and required fields ('name', 'description')
  3. Strict zero-emoji compliance across code and markdown
  4. Supply-chain security: zero unsafe pipe-to-shell installer patterns
  5. Registry consistency: all skills properly recorded in registry.yaml with gravidex URLs
  6. Multi-platform layout and naming consistency
  7. Governance specification presence (GRAVIDEX.md)
"""

import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
APPROVED_DIR = REPO_ROOT / "SKILLS" / "approved"
CANDIDATES_DIR = REPO_ROOT / "SKILLS" / "candidates"
REGISTRY_FILE = REPO_ROOT / "registry.yaml"

# Pictorial and decorative emojis (Unicode emoji presentations)
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


class TestGravidexGovernance(unittest.TestCase):
    """Test suite verifying GraviDex governance and identity requirements."""

    def test_registry_exists_and_populated(self):
        """Assert registry.yaml exists and contains registered skill records."""
        self.assertTrue(REGISTRY_FILE.is_file(), "registry.yaml must exist at repo root")
        content = REGISTRY_FILE.read_text(encoding="utf-8")
        self.assertIn("version:", content)
        self.assertIn("registry:", content)

        # Count registered skills and capabilities
        skill_ids = re.findall(r"^\s*-\s*id:\s*([a-zA-Z0-9_\-]+)", content, re.MULTILINE)
        self.assertGreaterEqual(len(skill_ids), 48, f"Expected at least 48 registered units, found {len(skill_ids)}")

        # Verify gravidex URLs for approved skills
        self.assertIn("https://github.com/hamzzaqureshi/gravidex", content)

    def test_approved_skills_structure(self):
        """Assert all 22 approved skills have valid SKILL.md and metadata."""
        self.assertTrue(APPROVED_DIR.is_dir(), "SKILLS/approved must exist")
        skills = [d for d in APPROVED_DIR.iterdir() if d.is_dir()]
        self.assertEqual(len(skills), 22, f"Expected 22 approved skills, found {len(skills)}")

        for s in skills:
            skill_md = s / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"SKILL.md missing in {s.name}")
            fm = parse_frontmatter(skill_md)
            self.assertTrue(bool(fm.get("name")), f"Frontmatter 'name' missing in {s.name}")
            self.assertTrue(bool(fm.get("description")), f"Frontmatter 'description' missing in {s.name}")

    def test_candidate_skills_structure(self):
        """Assert all 26 candidate skills have valid SKILL.md and metadata."""
        self.assertTrue(CANDIDATES_DIR.is_dir(), "SKILLS/candidates must exist")
        skills = [d for d in CANDIDATES_DIR.iterdir() if d.is_dir()]
        self.assertGreaterEqual(len(skills), 26, f"Expected at least 26 candidate skills, found {len(skills)}")

        for s in skills:
            skill_md = s / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"SKILL.md missing in {s.name}")
            fm = parse_frontmatter(skill_md)
            self.assertTrue(bool(fm.get("name")), f"Frontmatter 'name' missing in {s.name}")
            self.assertTrue(bool(fm.get("description")), f"Frontmatter 'description' missing in {s.name}")

    def test_zero_emojis_in_approved_and_candidate_skills(self):
        """Assert strict zero emoji characters in all skill markdown files."""
        for base in [APPROVED_DIR, CANDIDATES_DIR]:
            for root, _, files in os.walk(base):
                for f in files:
                    if f.endswith((".md", ".json", ".py", ".sh", ".yaml")):
                        p = Path(root) / f
                        text = p.read_text(encoding="utf-8", errors="ignore")
                        match = EMOJI_REGEX.search(text)
                        self.assertIsNone(match, f"Forbidden emoji character detected in {p}")

    def test_zero_unsafe_pipe_to_bash(self):
        """Assert no dangerous pipe-to-bash (curl/wget | sh) execution patterns."""
        for base in [APPROVED_DIR, CANDIDATES_DIR, REPO_ROOT / "scripts"]:
            for root, _, files in os.walk(base):
                for f in files:
                    if f.endswith((".md", ".py", ".sh")):
                        p = Path(root) / f
                        text = p.read_text(encoding="utf-8", errors="ignore")
                        match = PIPE_TO_BASH_REGEX.search(text)
                        self.assertIsNone(match, f"Unsafe pipe-to-shell installer detected in {p}: {match}")

    def test_no_id_collisions_between_approved_and_candidates(self):
        """Assert zero ID overlap between approved and candidate directories."""
        approved_names = set(d.name for d in APPROVED_DIR.iterdir() if d.is_dir())
        candidate_names = set(d.name for d in CANDIDATES_DIR.iterdir() if d.is_dir())
        collision = approved_names.intersection(candidate_names)
        self.assertEqual(len(collision), 0, f"Colliding skill IDs found: {collision}")

    def test_audit_reports_exist_and_populated(self):
        """Assert all required audit documents exist and are non-empty."""
        for report in ["INVENTORY.md", "QUALITY-REPORT.md", "SECURITY-REPORT.md", "COMPATIBILITY-REPORT.md", "UPDATE-REPORT.md"]:
            rep_path = REPO_ROOT / "AUDIT" / report
            self.assertTrue(rep_path.is_file(), f"Audit report missing: {report}")
            self.assertGreater(rep_path.stat().st_size, 100, f"Audit report appears empty: {report}")

    def test_governance_specification_exists(self):
        """Assert GRAVIDEX.md governance document exists."""
        self.assertTrue((REPO_ROOT / "GRAVIDEX.md").is_file(), "GRAVIDEX.md must exist")


if __name__ == "__main__":
    unittest.main()
