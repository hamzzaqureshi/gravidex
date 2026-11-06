#!/usr/bin/env python3
"""Distribution Packager for GraviDex Capabilities Suite.

Builds clean, self-contained, ready-to-share release archives and plugin bundles:
  - dist/gravidex.zip (Universal ZIP archive containing all 19 capabilities + installer)
  - dist/gravidex.tar.gz (Gzip tarball)
  - dist/gravidex-pack/ (Direct Antigravity Plugin structure)
  - dist/checksums.sha256 (Verification checksums)

Strictly excludes internal provenance archives, git clones, and governance infrastructure
(SOURCES/, QUARANTINE/, AUDIT/, GOVERNANCE/, DEPLOYMENT/, PATCHES/, SKILLS/).
"""

import hashlib
import json
import os
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    "node_modules",
    ".court",
    ".impeccable",
    ".rigor",
    ".artist",
    "dist",
    "SOURCES",
    "QUARANTINE",
    "AUDIT",
    "GOVERNANCE",
    "DEPLOYMENT",
    "PATCHES",
    "SKILLS",
    "bin",
}

EXCLUDE_FILES = {
    "registry.yaml",
    "GRAVIDEX.md",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
    ".log",
    ".tmp",
    ".bak",
}

SKILLS = [
    # 8 Curated Capability Packs
    "autonomous-agent-engineering",
    "backend-engineering",
    "design-systems",
    "frontend-engineering",
    "interface-design",
    "quality-engineering",
    "security-audit",
    "technical-documentation",
    # 11 Retained Independent Specialists
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
]

CORE_FILES = [
    "README.md",
    "SHARING.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".gitignore",
    "install.sh",
    "install.py",
    "test_all.py",
    "package.py",
]


def should_include(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    if parts & EXCLUDE_DIRS:
        return False
    if rel_path.name in EXCLUDE_FILES:
        return False
    if rel_path.suffix in EXCLUDE_EXTS:
        return False
    if rel_path.name.startswith(".#"):
        return False
    return True


def resolve_skill_path(name: str) -> Path:
    candidates = [
        ROOT / "CAPABILITIES" / "curated" / name,
        ROOT / "CAPABILITIES" / "retained-specialists" / name,
        ROOT / ".agents" / "skills" / name,
        ROOT / "skills" / name,
        ROOT / name,
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def gather_files():
    files = []
    # Core public files
    for cf in CORE_FILES:
        p = ROOT / cf
        if p.is_file():
            files.append(p)

    # Capability files
    cap_dir = ROOT / "CAPABILITIES"
    if cap_dir.is_dir():
        for p in cap_dir.rglob("*"):
            if p.is_file():
                rel = p.relative_to(ROOT)
                if should_include(rel):
                    files.append(p)

    # Workspace skills files
    ws_skills = ROOT / ".agents" / "skills"
    if ws_skills.is_dir():
        for p in ws_skills.rglob("*"):
            if p.is_file():
                rel = p.relative_to(ROOT)
                if should_include(rel):
                    files.append(p)

    # Test suite files
    test_dir = ROOT / "TESTS"
    if test_dir.is_dir():
        for p in test_dir.rglob("*"):
            if p.is_file():
                rel = p.relative_to(ROOT)
                if should_include(rel):
                    files.append(p)

    # De-duplicate files while preserving order
    seen = set()
    unique_files = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    return unique_files


def make_zip(files, out_path: Path):
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arcname = f.relative_to(ROOT)
            zf.write(f, arcname=arcname)


def make_tar(files, out_path: Path):
    with tarfile.open(out_path, "w:gz") as tf:
        for f in files:
            arcname = f.relative_to(ROOT)
            tf.add(f, arcname=str(arcname))


def make_plugin_bundle(plugin_dir: Path):
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    plugin_dir.mkdir(parents=True)

    # Manifest for Antigravity Plugin
    manifest = {
        "name": "gravidex-pack",
        "description": "Curated suite of GraviDex modular AI coding capabilities (19 skills)",
        "version": "2.0.0",
        "author": "GraviDex Project",
        "skills": SKILLS
    }
    with open(plugin_dir / "plugin.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # Copy skills into plugin/skills/
    skills_dest = plugin_dir / "skills"
    skills_dest.mkdir(parents=True)
    for skill in SKILLS:
        src = resolve_skill_path(skill)
        dest = skills_dest / skill
        if src and src.is_dir():
            shutil.copytree(
                src, dest,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "node_modules")
            )

    # Copy README, sharing and license
    for item in ("README.md", "SHARING.md", "LICENSE"):
        src = ROOT / item
        if src.is_file():
            shutil.copy2(src, plugin_dir / item)


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    print("=" * 72)
    print("           GraviDex Capabilities Suite - Distribution Packager")
    print("=" * 72)

    DIST.mkdir(parents=True, exist_ok=True)
    files = gather_files()
    print(f"\nDiscovered {len(files)} files across {len(SKILLS)} active capabilities.")

    zip_file = DIST / "gravidex.zip"
    tar_file = DIST / "gravidex.tar.gz"
    plugin_folder = DIST / "gravidex-pack"

    print("\nBuilding universal ZIP archive...")
    make_zip(files, zip_file)
    zip_size = zip_file.stat().st_size / (1024 * 1024)
    print(f"  Created {zip_file.name} ({zip_size:.2f} MB)")

    print("\nBuilding Gzip tarball archive...")
    make_tar(files, tar_file)
    tar_size = tar_file.stat().st_size / (1024 * 1024)
    print(f"  Created {tar_file.name} ({tar_size:.2f} MB)")

    print("\nBuilding Antigravity Plugin package...")
    make_plugin_bundle(plugin_folder)
    print(f"  Created {plugin_folder.name}/ (Ready for ~/.gemini/config/plugins/)")

    # Checksums
    checksums = [
        f"{compute_sha256(zip_file)}  {zip_file.name}",
        f"{compute_sha256(tar_file)}  {tar_file.name}",
    ]
    checksum_file = DIST / "checksums.sha256"
    with open(checksum_file, "w", encoding="utf-8") as f:
        f.write("\n".join(checksums) + "\n")
    print(f"\n  Wrote SHA-256 checksums to {checksum_file.name}")

    print("\n" + "=" * 72)
    print("                      PACKAGE SUMMARY")
    print("=" * 72)
    print(f"Directory: {DIST}")
    print(f"  - {zip_file.name:<28} ({zip_size:.2f} MB) -> Universal Zip Archive")
    print(f"  - {tar_file.name:<28} ({tar_size:.2f} MB) -> Standard Unix Tarball")
    print(f"  - {plugin_folder.name:<28} (Folder)     -> Drop into ~/.gemini/config/plugins/")
    print(f"  - {checksum_file.name:<28} (Text)       -> Verification Hashes")
    print("=" * 72)
    print("\nTo share with friends:")
    print("  1. Send them 'dist/gravidex.zip'")
    print("  2. Or publish this repository to GitHub so friends can clone or curl!")
    print()


if __name__ == "__main__":
    main()
