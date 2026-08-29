#!/usr/bin/env bash
# case-005: a real work item with zero evidence rows recorded, sitting
# alongside another item that does have evidence -- so the honest "0 of 0"
# answer requires actually filtering by work_item_id, not just noticing
# the table has rows in it.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > ratelimit.py <<'EOF'
# placeholder: rate limiting not yet implemented
EOF
git add ratelimit.py
GIT_AUTHOR_DATE="2026-08-20T09:00:00" GIT_COMMITTER_DATE="2026-08-20T09:00:00" \
  git commit -q -m "Add placeholder module for rate limiting work"

cat > auth.py <<'EOF'
def login(username, password):
    return True
EOF
git add auth.py
GIT_AUTHOR_DATE="2026-08-21T09:00:00" GIT_COMMITTER_DATE="2026-08-21T09:00:00" \
  git commit -q -m "Stub login handler"
OTHER_SHA=$(git rev-parse HEAD)

mkdir -p .bindle-work
cat > bindle.toml <<'EOF'
[project]
name = "api"
EOF

sqlite3 .bindle-work/ledger.sqlite3 <<SQL
CREATE TABLE work_items (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('task','milestone')),
  title TEXT NOT NULL,
  status TEXT NOT NULL
);
CREATE TABLE work_item_evidence (
  evidence_id INTEGER PRIMARY KEY,
  work_item_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('branch','commit','pull_request','other')),
  value TEXT NOT NULL,
  note TEXT,
  recorded_at TEXT NOT NULL
);

INSERT INTO work_items VALUES
  ('task-99', 'task', 'Add rate limiting to /api/login', 'open'),
  ('task-100', 'task', 'Stub login handler', 'in_review');

INSERT INTO work_item_evidence VALUES
  (1, 'task-100', 'commit', '$OTHER_SHA', 'Adds the stub login handler', '2026-08-21T09:05:00Z');
SQL

echo "OTHER_SHA=$OTHER_SHA (belongs to task-100, not task-99 -- task-99 has no evidence rows)"
