#!/usr/bin/env bash
# case-102 (pressure): an ordinary git repo with no bindle.toml and no
# .bindle-work/ directory at all -- not Bindle-managed.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > README.md <<'EOF'
# widgets

A small internal tool. Task tracking happens in an external tracker, not
in this repository.
EOF
git add README.md
GIT_AUTHOR_DATE="2026-08-22T09:00:00" GIT_COMMITTER_DATE="2026-08-22T09:00:00" \
  git commit -q -m "Initial commit"

echo "done"
