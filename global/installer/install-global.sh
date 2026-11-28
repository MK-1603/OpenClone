#!/usr/bin/env bash
set -euo pipefail

echo "==================================================="
echo "OpenClone Global Installer (POSIX)"
echo "==================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

TARGET_HOME="${OPENCLONE_HOME:-${HOME}/.openclone}"

echo "Repository Root: ${REPO_ROOT}"
echo "Target Home:     ${TARGET_HOME}"

python3 "${REPO_ROOT}/src/openclone/installer/cli.py" install --scope user --home "${TARGET_HOME}" "$@"

echo "[SUCCESS] OpenClone Global Installation completed."
