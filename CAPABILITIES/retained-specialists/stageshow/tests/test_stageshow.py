#!/usr/bin/env python3
"""Unit tests for Stageshow Retained Specialist capability."""

import os
import re
import unittest
from pathlib import Path

STAGESHOW_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = STAGESHOW_DIR / "SKILL.md"
REFERENCES_DIR = STAGESHOW_DIR / "references"
KIT_DIR = STAGESHOW_DIR / "kit"
SCRIPTS_DIR = STAGESHOW_DIR / "scripts"
PROVENANCE_FILE = STAGESHOW_DIR / "provenance.yaml"

EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)


class TestStageshow(unittest.TestCase):
    """Test suite verifying Stageshow capability structure and compliance."""

    def test_skill_md_exists_and_valid_frontmatter(self):
        """Verify SKILL.md has valid name and description."""
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist in stageshow capability")
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        match = re.search(r"^name:\s*stageshow\s*$", content, re.MULTILINE)
        self.assertIsNotNone(match, "Frontmatter 'name' must be 'stageshow'")
        desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        self.assertIsNotNone(desc_match, "Frontmatter 'description' must be present")

    def test_kit_and_references_presence(self):
        """Verify kit and references directories exist with core modules."""
        self.assertTrue(KIT_DIR.is_dir(), "stageshow/kit must exist")
        self.assertTrue(REFERENCES_DIR.is_dir(), "stageshow/references must exist")
        self.assertTrue(SCRIPTS_DIR.is_dir(), "stageshow/scripts must exist")

    def test_provenance_validity(self):
        """Verify provenance.yaml exists and maps to upstream source."""
        self.assertTrue(PROVENANCE_FILE.is_file(), "provenance.yaml must exist")
        content = PROVENANCE_FILE.read_text(encoding="utf-8")
        self.assertIn("benjitaylor/skills", content)
        self.assertIn("299140fafd08df55a9c234e610c3f64af3f45531", content)

    def test_zero_emojis_in_capability(self):
        """Verify strict zero-emoji compliance across all capability files."""
        for root, _, files in os.walk(STAGESHOW_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".yaml", ".json", ".sh", ".ts", ".tsx", ".js", ".mjs")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")


if __name__ == "__main__":
    unittest.main()
