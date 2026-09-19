#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# two verification logs: unit log older than the last code commit, integration log newer; tree clean
new_repo "$out"
put go.mod <<'J'
module example.com/queue-svc

go 1.22
J
put internal/replay/replay.go <<'J'
package replay

func Replay(ids []string) []string { return ids }
J
put internal/replay/replay_test.go <<'J'
package replay
J
commit_all "replay: initial" "2026-09-10T09:00:00"
put internal/replay/replay.go <<'J'
package replay

func Replay(ids []string) []string {
	seen := map[string]bool{}
	var out []string
	for _, id := range ids {
		if !seen[id] {
			seen[id] = true
			out = append(out, id)
		}
	}
	return out
}
J
commit_all "replay: dedupe by message id" "2026-09-16T12:00:00"
sync_mtimes
mkdir -p logs
put logs/unit.log <<'J'
ok  	example.com/queue-svc/internal/replay	0.004s
ok  	example.com/queue-svc/internal/store	0.011s
J
put logs/integration.log <<'J'
=== RUN   TestReplayDedup
    replay_integration_test.go:41: expected 3 unique ids, got 4
--- FAIL: TestReplayDedup (0.32s)
FAIL
FAIL	example.com/queue-svc/integration	0.402s
J
stamp 202609151000 logs/unit.log
stamp 202609161800 logs/integration.log
