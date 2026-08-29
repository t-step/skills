#!/usr/bin/env bash
# case-003: evidence cites a branch that has since been deleted.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > discounts.py <<'EOF'
VALID_CODES = {"SAVE10"}


def apply_discount(code, amount_cents):
    if code not in VALID_CODES:
        raise ValueError("unknown discount code")
    return amount_cents * 90 // 100
EOF

git add discounts.py
GIT_AUTHOR_DATE="2026-08-01T09:00:00" GIT_COMMITTER_DATE="2026-08-01T09:00:00" \
  git commit -q -m "Initial discount handling"

git checkout -q -b feature/discount-code
cat >> discounts.py <<'EOF'


def register_code(code):
    VALID_CODES.add(code)
EOF
git add discounts.py
GIT_AUTHOR_DATE="2026-08-02T10:00:00" GIT_COMMITTER_DATE="2026-08-02T10:00:00" \
  git commit -q -m "WIP: allow registering new discount codes"

git checkout -q main
git branch -D feature/discount-code >/dev/null

mkdir -p .bindle-work
cat > bindle.toml <<'EOF'
[project]
name = "discounts"
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

INSERT INTO work_items VALUES ('task-15', 'task', 'Add discount code support', 'blocked');

INSERT INTO work_item_evidence VALUES
  (1, 'task-15', 'branch', 'feature/discount-code', 'Work-in-progress branch for registrable discount codes', '2026-08-02T10:05:00Z');
SQL

echo "done"
