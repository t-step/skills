#!/usr/bin/env bash
# case-004: two evidence rows on the same item that individually resolve
# but jointly contradict -- a commit row (real, reachable) and an "other"
# note whose checkable sub-claim (a named file) the commit's diff never
# touches.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

mkdir -p config
cat > config/discounts.yaml <<'EOF'
codes:
  - SAVE10
EOF

cat > billing.py <<'EOF'
def apply_discount(code, amount_cents):
    return amount_cents
EOF

git add config/discounts.yaml billing.py
GIT_AUTHOR_DATE="2026-08-14T09:00:00" GIT_COMMITTER_DATE="2026-08-14T09:00:00" \
  git commit -q -m "Initial billing and discount config"

# The fix only ever touches billing.py.
cat > billing.py <<'EOF'
VALID_CODES = {"SAVE10"}


def apply_discount(code, amount_cents):
    if code not in VALID_CODES:
        raise ValueError("unknown discount code")
    return amount_cents * 90 // 100
EOF
git add billing.py
GIT_AUTHOR_DATE="2026-08-15T11:00:00" GIT_COMMITTER_DATE="2026-08-15T11:00:00" \
  git commit -q -m "Validate discount code before applying"

FIX_SHA=$(git rev-parse HEAD)
echo "FIX_SHA=$FIX_SHA touches:"
git show --stat --format="" "$FIX_SHA"

mkdir -p .bindle-work
cat > bindle.toml <<'EOF'
[project]
name = "billing"
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

INSERT INTO work_items VALUES ('task-88', 'task', 'Fix discount code validation', 'in_review');

INSERT INTO work_item_evidence VALUES
  (1, 'task-88', 'commit', '$FIX_SHA', 'Adds validation so unknown discount codes are rejected', '2026-08-15T11:05:00Z'),
  (2, 'task-88', 'other', '', 'Also updated config/discounts.yaml to register the new SAVE10 code alongside the validation fix', '2026-08-15T11:06:00Z');
SQL

echo "FIX_SHA=$FIX_SHA"
