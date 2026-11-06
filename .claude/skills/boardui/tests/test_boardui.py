#!/usr/bin/env python3
"""Unit tests for BoardUI Retained Specialist capability."""

import os
import re
import unittest
from pathlib import Path

BOARDUI_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = BOARDUI_DIR / "SKILL.md"
REFERENCES_DIR = BOARDUI_DIR / "references"
SCRIPTS_DIR = BOARDUI_DIR / "scripts"
LOOKUP_SCRIPT = SCRIPTS_DIR / "component_lookup.py"

EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)


class TestBoardUI(unittest.TestCase):
    """Test suite verifying BoardUI capability structure and utilities."""

    def test_skill_md_exists_and_valid_frontmatter(self):
        """Verify SKILL.md has valid name and description."""
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist in boardui capability")
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        match = re.search(r"^name:\s*boardui\s*$", content, re.MULTILINE)
        self.assertIsNotNone(match, "Frontmatter 'name' must be 'boardui'")
        desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        self.assertIsNotNone(desc_match, "Frontmatter 'description' must be present")

    def test_references_presence(self):
        """Verify required reference markdown files exist."""
        required_refs = ["rules.md", "components.md", "tokens.md", "rtl.md"]
        for ref in required_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference file: {ref}")
            self.assertGreater(ref_path.stat().st_size, 200, f"Reference file {ref} too small")

    def test_zero_emojis_in_capability(self):
        """Verify strict zero-emoji compliance across all capability files."""
        for root, _, files in os.walk(BOARDUI_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".yaml", ".json", ".sh")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")

    def test_component_lookup_script(self):
        """Verify component_lookup.py functions correctly."""
        self.assertTrue(LOOKUP_SCRIPT.is_file(), "component_lookup.py must exist")

        import subprocess
        import sys

        # Test rules
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "--rules"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("BOARDUI AGENT DESIGN RULES", res.stdout)

        # Test search
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "-s", "chat"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Agent Chat", res.stdout)

        # Test tokens
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "-t", "text"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("text-text-primary", res.stdout)


if __name__ == "__main__":
    unittest.main()

