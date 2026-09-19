#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan: synchronous notifications in the handler. A task queue is already in the repo and the latency notes point at it.
new_repo "$out"
put requirements.txt <<'J'
flask==3.0.0
celery==5.4.0
J
put docs/perf.md <<'J'
# Handler latency (p95, last week)
- POST /orders: 800ms total, of which 600ms is the notification send.
J
put app/tasks.py <<'J'
from celery import Celery

app = Celery("app")


@app.task
def send_email(to, body):
    return True
J
put app/orders.py <<'J'
def create_order(payload):
    order = {"id": 1, **payload}
    return order
J
put app/notify.py <<'J'
def send(to, body):
    return True
J
put docs/PLAN.md <<'J'
# Plan: order notifications

Approach: send the notification synchronously inside the request handler (`create_order`).

- [ ] 1. `notify.send` helper
- [ ] 2. Call `notify.send` from `create_order`
- [ ] 3. Retry `notify.send` up to 3 times on failure
- [ ] 4. Log notification failures
J
commit_all "notif-svc: baseline, latency notes, plan" "2026-09-11T10:00:00"
git checkout -q -b feat/order-notify
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
put app/orders.py <<'J'
from . import notify


def create_order(payload):
    order = {"id": 1, **payload}
    notify.send(payload.get("email"), "order received")
    return order
J
commit_all "orders: call notify.send in create_order (plan steps 1-2)" "2026-09-15T10:00:00"
