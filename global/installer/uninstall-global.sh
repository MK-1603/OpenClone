#!/usr/bin/env bash
set -euo pipefail

echo "==================================================="
echo "OpenClone Global Uninstaller (POSIX)"
echo "==================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

TARGET_HOME="${OPENCLONE_HOME:-${HOME}/.openclone}"

echo "Target Home: ${TARGET_HOME}"

python3 "${REPO_ROOT}/src/openclone/installer/cli.py" uninstall --scope user --home "${TARGET_HOME}" "$@"

echo "[SUCCESS] OpenClone Global Uninstallation completed."
