#!/usr/bin/env bash
# GraviDex Inventory Shell Wrapper
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "${SCRIPT_DIR}/inventory.py" "$@"

