#!/usr/bin/env bash
# Deterministically generates repo/ (git history + .bindle-work/ledger.sqlite3)
# for case-001: clean, mutually-consistent, all-resolved evidence.
# Re-running this script always reproduces the same commit SHAs.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

export GIT_AUTHOR_NAME="Fixture Author"
export GIT_AUTHOR_EMAIL="fixture@example.invalid"
export GIT_COMMITTER_NAME="Fixture Author"
export GIT_COMMITTER_EMAIL="fixture@example.invalid"

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > README.md <<'EOF'
# invoicing

Small internal invoicing helper.
EOF

cat > invoice.py <<'EOF'
def calculate_total(line_items):
    return sum(item["price"] * item["qty"] for item in line_items)
EOF

mkdir -p tests
cat > tests/test_invoice.py <<'EOF'
from invoice import calculate_total


def test_calculate_total():
    items = [{"price": 10, "qty": 2}, {"price": 5, "qty": 1}]
    assert calculate_total(items) == 25
EOF

git add README.md invoice.py tests/test_invoice.py
GIT_AUTHOR_DATE="2026-08-10T09:00:00" GIT_COMMITTER_DATE="2026-08-10T09:00:00" \
  git commit -q -m "Initial invoicing helper"

cat > invoice.py <<'EOF'
def calculate_total(line_items):
    return round(sum(item["price"] * item["qty"] for item in line_items), 2)
EOF

git checkout -q -b fix/rounding
git add invoice.py
GIT_AUTHOR_DATE="2026-08-11T14:30:00" GIT_COMMITTER_DATE="2026-08-11T14:30:00" \
  git commit -q -m "Round calculate_total to 2 decimal places"

FIX_SHA=$(git rev-parse HEAD)

git checkout -q main
git merge -q --no-ff -m "Merge fix/rounding" fix/rounding

mkdir -p .bindle-work
cat > ../bindle.toml.tmp <<EOF
[project]
name = "invoicing"
EOF
mv ../bindle.toml.tmp bindle.toml

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

INSERT INTO work_items VALUES ('task-42', 'task', 'Fix rounding bug in calculate_total', 'in_review');

INSERT INTO work_item_evidence VALUES
  (1, 'task-42', 'commit', '$FIX_SHA', 'Rounds calculate_total output to 2 decimal places', '2026-08-11T14:35:00Z'),
  (2, 'task-42', 'branch', 'fix/rounding', 'Work branch for the rounding fix', '2026-08-11T14:36:00Z');
SQL

echo "FIX_SHA=$FIX_SHA"
