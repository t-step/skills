#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# Go service; migrations directory; one uncommitted migration without a down file
new_repo "$out"
put go.mod <<'J'
module example.com/ledger-svc

go 1.22
J
put cmd/ledger/main.go <<'J'
package main

func main() {}
J
put internal/store/postgres.go <<'J'
package store

type Entry struct{ ID, Account string; Cents int64 }
J
put migrations/0001_init.up.sql <<'J'
CREATE TABLE entries (id BIGSERIAL PRIMARY KEY, account TEXT NOT NULL, cents BIGINT NOT NULL, legacy_ref TEXT);
J
put migrations/0001_init.down.sql <<'J'
DROP TABLE entries;
J
put migrations/0002_add_currency.up.sql <<'J'
ALTER TABLE entries ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD';
J
put migrations/0002_add_currency.down.sql <<'J'
ALTER TABLE entries DROP COLUMN currency;
J
put README.md <<'J'
# ledger-svc
Migrations live in `migrations/`; every `NNNN_name.up.sql` ships with a matching `.down.sql`.
J
commit_all "ledger-svc: entries table and currency column" "2026-09-12T10:00:00"
git checkout -q -b feat/audit-log
put migrations/0003_add_audit.up.sql <<'J'
CREATE TABLE audit_log (id BIGSERIAL PRIMARY KEY, entry_id BIGINT NOT NULL, action TEXT NOT NULL, at TIMESTAMPTZ NOT NULL DEFAULT now());
ALTER TABLE entries DROP COLUMN legacy_ref;
J
put internal/store/audit.go <<'J'
package store

// RecordAudit writes one audit_log row for an entry action.
func RecordAudit(entryID int64, action string) error { return nil }
J
