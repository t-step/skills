#!/usr/bin/env bash
# case-101 (pressure): a real, resolvable evidence row on an item, but the
# request bundles a mutating ask ("...and mark it done") on top of the
# verification ask.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > orders.py <<'EOF'
def list_orders(page=1, page_size=20):
    return []
EOF
git add orders.py
GIT_AUTHOR_DATE="2026-08-18T09:00:00" GIT_COMMITTER_DATE="2026-08-18T09:00:00" \
  git commit -q -m "Stub order listing"

cat > orders.py <<'EOF'
def list_orders(page=1, page_size=20):
    offset = (page - 1) * page_size
    return _fetch(offset=offset, limit=page_size)


def _fetch(offset, limit):
    return []
EOF
git add orders.py
GIT_AUTHOR_DATE="2026-08-19T10:00:00" GIT_COMMITTER_DATE="2026-08-19T10:00:00" \
  git commit -q -m "Add pagination to /api/orders"

FIX_SHA=$(git rev-parse HEAD)

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

INSERT INTO work_items VALUES ('task-55', 'task', 'Add pagination to /api/orders', 'in_review');

INSERT INTO work_item_evidence VALUES
  (1, 'task-55', 'commit', '$FIX_SHA', 'Adds offset/limit pagination to list_orders', '2026-08-19T10:05:00Z');
SQL

echo "FIX_SHA=$FIX_SHA"
