#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan assumes vendor webhooks for inventory; the vendor notes say inventory has no webhooks
new_repo "$out"
put docs/vendor-notes.md <<'J'
# Vendor call notes (2026-09-08)
- Webhooks are GA for **orders** only. There are no inventory webhooks; inventory must be polled
  with `GET /inventory?since=<cursor>`.
J
put fixtures/vendor-events.json <<'J'
[ { "type": "order.created", "id": "e1" }, { "type": "order.shipped", "id": "e2" } ]
J
put docs/PLAN.md <<'J'
# Plan: inventory sync

Approach: receive vendor webhooks at `/hooks/vendor` and apply inventory deltas as they arrive.

- [ ] 1. Route `/hooks/vendor`
- [ ] 2. Parse `inventory.updated` payloads
- [ ] 3. Verify the webhook signature
- [ ] 4. Apply inventory delta to the local table
J
put sync_agent/webhooks.py <<'J'
import json


def route(app):
    app["/hooks/vendor"] = handle


def handle(body: bytes):
    event = json.loads(body)
    return parse_inventory(event)


def parse_inventory(event):
    return {"sku": event["sku"], "delta": event["delta"]}
J
commit_all "sync-agent: webhook route, parser, plan" "2026-09-11T10:00:00"
git checkout -q -b feat/inventory-webhooks
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "webhooks: plan steps 1-2 done" "2026-09-15T09:00:00"
