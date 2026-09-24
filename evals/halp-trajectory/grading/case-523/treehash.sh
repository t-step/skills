#!/usr/bin/env bash
# Usage: treehash.sh <repo>  -- hash of HEAD + tracked diff + untracked (non-ignored) file contents
set -euo pipefail; cd "${1:?}"
{ git rev-parse HEAD; git diff --binary; git ls-files -o --exclude-standard -z | sort -z | xargs -0 -r shasum; } | shasum | cut -d' ' -f1
