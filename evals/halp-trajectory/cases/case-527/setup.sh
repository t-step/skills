#!/usr/bin/env bash
# Builds the frozen fixture for this case into $1 (see build.sh). Deterministic given network access to GitHub and the package registry.
set -euo pipefail
exec bash "$(cd "$(dirname "$0")" && pwd)/build.sh" "$1" k37
