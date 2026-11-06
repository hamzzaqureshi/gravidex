#!/usr/bin/env python3
"""Unit tests for Karpathy Guidelines Retained Specialist capability."""

import os
import re
import unittest
from pathlib import Path

KARPATHY_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = KARPATHY_DIR / "SKILL.md"
REFERENCES_DIR = KARPATHY_DIR / "references"
PROVENANCE_FILE = KARPATHY_DIR / "provenance.yaml"

EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)


class TestKarpathyGuidelines(unittest.TestCase):
    """Test suite verifying Karpathy Guidelines capability structure and compliance."""

    def test_skill_md_exists_and_valid_frontmatter(self):
        """Verify SKILL.md has valid name and description."""
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist in karpathy-guidelines capability")
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        match = re.search(r"^name:\s*karpathy-guidelines\s*$", content, re.MULTILINE)
        self.assertIsNotNone(match, "Frontmatter 'name' must be 'karpathy-guidelines'")
        desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        self.assertIsNotNone(desc_match, "Frontmatter 'description' must be present")

    def test_core_pillars_presence(self):
        """Verify all 4 core pillars are documented in SKILL.md."""
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("1. Think Before Coding", content)
        self.assertIn("2. Simplicity First", content)
        self.assertIn("3. Surgical Changes", content)
        self.assertIn("4. Goal-Driven Execution", content)

    def test_references_presence(self):
        """Verify required reference markdown files exist."""
        required_refs = ["examples.md", "claude.md", "cursor.md"]
        for ref in required_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference file: {ref}")
            self.assertGreater(ref_path.stat().st_size, 200, f"Reference file {ref} too small")

    def test_provenance_validity(self):
        """Verify provenance.yaml exists and maps to upstream source."""
        self.assertTrue(PROVENANCE_FILE.is_file(), "provenance.yaml must exist")
        content = PROVENANCE_FILE.read_text(encoding="utf-8")
        self.assertIn("multica-ai/andrej-karpathy-skills", content)
        self.assertIn("2c606141936f1eeef17fa3043a72095b4765b9c2", content)

    def test_zero_emojis_in_capability(self):
        """Verify strict zero-emoji compliance across all capability files."""
        for root, _, files in os.walk(KARPATHY_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".yaml", ".json", ".sh")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")


if __name__ == "__main__":
    unittest.main()
