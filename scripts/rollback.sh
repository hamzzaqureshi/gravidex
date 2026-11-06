#!/usr/bin/env bash
# GraviDex Rollback Script
# Restores quarantined legacy runtime installations from QUARANTINE/legacy-runtime-backup/

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUARANTINE_DIR="$REPO_ROOT/QUARANTINE/legacy-runtime-backup"

echo "========================================================================"
echo "                   GRAVIDEX ROLLBACK PROCEDURE"
echo "========================================================================"

if [ ! -d "$QUARANTINE_DIR" ]; then
    echo "ERROR: Quarantine directory not found at $QUARANTINE_DIR"
    exit 1
fi

echo "Restoring root skill directories..."
if [ -d "$QUARANTINE_DIR/root-skills" ]; then
    cp -r "$QUARANTINE_DIR/root-skills/"* "$REPO_ROOT/"
    echo "  Root skills restored."
fi

echo "Restoring .agents/skills/..."
if [ -d "$QUARANTINE_DIR/workspace-agents-skills" ]; then
    mkdir -p "$REPO_ROOT/.agents/skills"
    cp -r "$QUARANTINE_DIR/workspace-agents-skills/"* "$REPO_ROOT/.agents/skills/"
    echo "  .agents/skills restored."
fi

echo "Restoring .opencode/skills/..."
if [ -d "$QUARANTINE_DIR/workspace-opencode-skills" ]; then
    mkdir -p "$REPO_ROOT/.opencode/skills"
    cp -r "$QUARANTINE_DIR/workspace-opencode-skills/"* "$REPO_ROOT/.opencode/skills/"
    echo "  .opencode/skills restored."
fi

echo "========================================================================"
echo "Rollback completed successfully."
echo "========================================================================"

