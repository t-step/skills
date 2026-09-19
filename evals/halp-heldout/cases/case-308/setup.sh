#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan: Postgres full-text search. An unmerged Elasticsearch spike exists on another local branch.
new_repo "$out"
put docs/notes.md <<'J'
# Notes
- ~2M documents today. No Elasticsearch cluster is provisioned in any environment.
- Postgres is already the system of record.
J
put search/query.go <<'J'
package search

func Query(q string) string { return "SELECT id FROM docs" }
J
put docs/PLAN.md <<'J'
# Plan: document search

Approach: Postgres full-text search (`tsvector` column, GIN index, `to_tsquery`).

- [ ] 1. Add `tsv` column and GIN index (migration)
- [ ] 2. `Query` uses `to_tsquery`
- [ ] 3. Rank results with `ts_rank`
- [ ] 4. Highlight snippets with `ts_headline`
J
commit_all "search-svc: baseline, notes, plan" "2026-09-10T10:00:00"
git checkout -q -b spike/elastic
put search/elastic.go <<'J'
package search

import "github.com/elastic/go-elasticsearch/v8/esapi"

var _ esapi.SearchRequest

// WIP: elasticsearch-backed Query
func ElasticQuery(q string) string { return "es:" + q }
J
commit_all "wip: elasticsearch client for search" "2026-09-11T15:00:00"
git checkout -q main
git checkout -q -b feat/pg-search
put migrations/0004_tsv.up.sql <<'J'
ALTER TABLE docs ADD COLUMN tsv tsvector;
CREATE INDEX docs_tsv_idx ON docs USING GIN (tsv);
J
put search/query.go <<'J'
package search

func Query(q string) string { return "SELECT id FROM docs WHERE tsv @@ to_tsquery('" + q + "')" }
J
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "search: tsv column and to_tsquery (plan steps 1-2)" "2026-09-15T10:00:00"
