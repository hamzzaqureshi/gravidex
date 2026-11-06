#!/usr/bin/env bash
# GraviDex Check Updates Shell Wrapper
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "${SCRIPT_DIR}/check-updates.py" "$@"

