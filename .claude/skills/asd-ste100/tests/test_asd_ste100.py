#!/usr/bin/env python3
"""Unit tests for ASD-STE100 Retained Specialist capability."""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ASD_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = ASD_DIR / "SKILL.md"
REFERENCES_DIR = ASD_DIR / "references"
SCRIPTS_DIR = ASD_DIR / "scripts"
LINTER_SCRIPT = SCRIPTS_DIR / "ste_lint.py"
LOOKUP_SCRIPT = SCRIPTS_DIR / "ste_lookup.py"
PROVENANCE_FILE = ASD_DIR / "provenance.yaml"

EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF]|[\u26D4\u26A1\u2764\u2728\u2705\u274C\u2B50]"
)
LINK_PATTERN = re.compile(r"\[.*?\]\((?!https?://|mailto:|#)([^)]+)\)")


class TestAsdSte100(unittest.TestCase):
    """Test suite verifying ASD-STE100 capability structure and tooling."""

    def test_skill_md_exists_and_valid_frontmatter(self):
        """Verify SKILL.md has valid name and description."""
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist in asd-ste100 capability")
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter")
        match = re.search(r"^name:\s*asd-ste100\s*$", content, re.MULTILINE)
        self.assertIsNotNone(match, "Frontmatter 'name' must be 'asd-ste100'")
        desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        self.assertIsNotNone(desc_match, "Frontmatter 'description' must be present")

    def test_references_presence(self):
        """Verify required reference markdown files exist and have content."""
        required_refs = [
            "writing-rules.md",
            "karpathy-framework.md",
            "verb-forms.md",
            "approved-words.md"
        ]
        for ref in required_refs:
            ref_path = REFERENCES_DIR / ref
            self.assertTrue(ref_path.is_file(), f"Missing reference file: {ref}")
            self.assertGreater(ref_path.stat().st_size, 500, f"Reference file {ref} too small")

    def test_provenance_integrity(self):
        """Verify provenance.yaml maps to both upstream snapshots."""
        self.assertTrue(PROVENANCE_FILE.is_file(), "provenance.yaml must exist")
        text = PROVENANCE_FILE.read_text(encoding="utf-8")
        self.assertIn("danyuchn-asd-ste100-skill", text)
        self.assertIn("jaichangpark-asd-ste100", text)
        self.assertIn("fd86652be0d5d3485c69e1529dfd1fa3c9a7a640", text)
        self.assertIn("384d7d568da6f55ee379e429f9b4e1b0bd603536", text)

    def test_zero_emojis_in_capability(self):
        """Verify strict zero-emoji compliance across all capability files."""
        for root, _, files in os.walk(ASD_DIR):
            for f in files:
                if f.endswith((".md", ".py", ".yaml", ".json", ".sh")):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    match = EMOJI_REGEX.search(text)
                    self.assertIsNone(match, f"Forbidden emoji character detected in {p}")

    def test_zero_broken_markdown_links(self):
        """Verify all local relative markdown links resolve to existing files."""
        for root, _, files in os.walk(ASD_DIR):
            for f in files:
                if f.endswith(".md"):
                    p = Path(root) / f
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    for target in LINK_PATTERN.findall(text):
                        clean_target = target.split("#")[0].strip()
                        if not clean_target:
                            continue
                        target_path = (p.parent / clean_target).resolve()
                        self.assertTrue(target_path.exists(), f"Broken link in {p.name}: {target}")

    def test_ste_linter_selftest(self):
        """Verify ste_lint.py --selftest passes with exit code 0."""
        self.assertTrue(LINTER_SCRIPT.is_file(), "ste_lint.py must exist")
        res = subprocess.run([sys.executable, str(LINTER_SCRIPT), "--selftest"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"ste_lint.py --selftest failed: {res.stderr}")
        self.assertIn("selftest OK", res.stdout)

    def test_ste_linter_clean_prose(self):
        """Verify ste_lint.py passes on valid STE text."""
        clean_text = "Make sure that the hydraulic reservoir is full before you start the operation."
        res = subprocess.run([sys.executable, str(LINTER_SCRIPT)], input=clean_text, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("0 violations", res.stdout)

    def test_ste_linter_catches_violations(self):
        """Verify ste_lint.py flags semicolons, passive voice, and phrasal verbs."""
        bad_text = "It is recommended to utilize the cache; spin up the worker."
        res = subprocess.run([sys.executable, str(LINTER_SCRIPT)], input=bad_text, capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("semicolon", res.stdout)
        self.assertIn("passive-voice", res.stdout)
        self.assertIn("phrasal-verb", res.stdout)

    def test_ste_lookup_script(self):
        """Verify ste_lookup.py dictionary queries."""
        self.assertTrue(LOOKUP_SCRIPT.is_file(), "ste_lookup.py must exist")

        # Test lookup for utilize -> USE
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "utilize"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("USE", res.stdout)

        # Test lookup for prior to -> BEFORE
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "prior to", "--json"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("BEFORE", res.stdout)

        # Test lookup all entries
        res = subprocess.run([sys.executable, str(LOOKUP_SCRIPT), "--all"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("ASD-STE100 Vocabulary Registry", res.stdout)


if __name__ == "__main__":
    unittest.main()
