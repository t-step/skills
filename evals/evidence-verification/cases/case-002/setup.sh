#!/usr/bin/env bash
# case-002: evidence cites a commit that existed, was cited, and then got
# rebased away. The object is still present as a loose object (no gc has
# run) but is reachable from nothing -- the stale-evidence case the skill
# exists to catch. Deterministic: fixed dates/content -> fixed SHAs.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf repo
mkdir repo
cd repo

git init -q -b main
git config commit.gpgsign false
git config user.name "Fixture Author"
git config user.email "fixture@example.invalid"

cat > billing.py <<'EOF'
def total_cents(amount_cents, quantity):
    return amount_cents * quantity
EOF

git add billing.py
GIT_AUTHOR_DATE="2026-08-05T09:00:00" GIT_COMMITTER_DATE="2026-08-05T09:00:00" \
  git commit -q -m "Initial billing helper"

# The commit that evidence will cite -- an off-by-one fix.
cat > billing.py <<'EOF'
def total_cents(amount_cents, quantity):
    return amount_cents * (quantity - 1)
EOF
git add billing.py
GIT_AUTHOR_DATE="2026-08-06T10:00:00" GIT_COMMITTER_DATE="2026-08-06T10:00:00" \
  git commit -q -m "Fix off-by-one in total_cents"

CITED_SHA=$(git rev-parse HEAD)

# Now the fix is discovered to be wrong and gets amended (rebased away):
# the original commit above becomes unreachable from any ref, but its
# object is still on disk since nothing has run gc.
cat > billing.py <<'EOF'
def total_cents(amount_cents, quantity):
    # quantity is already inclusive; no off-by-one adjustment needed.
    return amount_cents * quantity
EOF
git add billing.py
GIT_AUTHOR_DATE="2026-08-06T11:00:00" GIT_COMMITTER_DATE="2026-08-06T11:00:00" \
  git commit -q --amend -m "Revert accidental off-by-one change, no bug present"

echo "CITED_SHA=$CITED_SHA (now unreachable, still a loose object)"
git cat-file -e "${CITED_SHA}^{commit}" && echo "object still present"
git branch -a --contains "$CITED_SHA" || echo "not reachable from any ref (expected)"

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

INSERT INTO work_items VALUES ('task-77', 'task', 'Fix off-by-one in total_cents', 'in_review');

INSERT INTO work_item_evidence VALUES
  (1, 'task-77', 'commit', '$CITED_SHA', 'Fixes the off-by-one bug in total_cents', '2026-08-06T10:05:00Z');
SQL

echo "CITED_SHA=$CITED_SHA"
