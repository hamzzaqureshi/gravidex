#!/usr/bin/env python3
"""Unit tests for Lemo-Opuscar Retained Specialist capability."""

import os
import re
import unittest
from pathlib import Path

LEMO_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = LEMO_DIR / "SKILL.md"
REFERENCES_DIR = LEMO_DIR / "references"
SCRIPTS_DIR = LEMO_DIR / "scripts"
LOOKUP_SCRIPT = SCRIPTS_DIR / "style_lookup.py"

EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)
LINK_PATTERN = re.compile(r"\[.*?\]\((?!https?://|mailto:|#)([^)]+)\)")


class TestLemoOpuscar(unittest.TestCase):
    """Test suite verifying Lemo-Opuscar capability structure and tooling."""

    def test_skill_md_exists_and_valid_frontmatter(self):
        """Verify SKILL.md has valid name and description."""
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist in lemo-opuscar capability")
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        match = re.search(r"^name:\s*lemo-opuscar\s*$", content, re.MULTILINE)
        self.assertIsNotNone(match, "Frontmatter 'name' must be 'lemo-opuscar'")
        desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        self.assertIsNotNone(desc_match, "Frontmatter 'description' must be present")

    def test_references_presence(self):
        """Verify required reference markdown files exist."""
        required_refs = ["director.md", "technique.md", "agents.md", "styles.md", "my-styles.md"]
        for ref in required_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference file: {ref}")
            self.assertGreater(ref_path.stat().st_size, 500, f"Reference file {ref} too small")

    def test_zero_emojis_in_capability(self):
        """Verify strict zero-emoji compliance across all capability files."""
        for root, _, files in os.walk(LEMO_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".yaml", ".json", ".sh")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")

    def test_zero_broken_markdown_links(self):
        """Verify all local relative markdown links resolve to existing files."""
        for root, _, files in os.walk(LEMO_DIR):
            for f in files:
                if f.endswith(".md"):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    for target in LINK_PATTERN.findall(text):
                        target_path = (p.parent / target).resolve()
                        self.assertTrue(target_path.exists(), f"Broken link in {p.name}: {target}")

    def test_style_lookup_script(self):
        """Verify style_lookup.py functions correctly."""
        self.assertTrue(LOOKUP_SCRIPT.is_file(), "style_lookup.py must exist")

        import subprocess
        import sys

        # Test director rules
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "--rules"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("LEMO-OPUSCAR DIRECTOR RULES", res.stdout)

        # Test search
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "-s", "watercolor"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Watercolor Brush", res.stdout)

        # Test categories
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "--categories"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Evidence Films", res.stdout)


if __name__ == "__main__":
    unittest.main()

