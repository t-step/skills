#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan says: per-handler in-process cache. Repo says (ADR-007): no in-process caches.
new_repo "$out"
put go.mod <<'J'
module example.com/orders-svc

go 1.22
J
put docs/adr/ADR-007-caching.md <<'J'
# ADR-007: Caching
Status: accepted (2026-06)

All caching goes through `internal/cache.Store` (Redis-backed). In-process caches are not allowed:
the service runs on 12 replicas and invalidation must be shared across them.
J
put internal/cache/store.go <<'J'
package cache

type Store interface {
	Get(key string) ([]byte, bool)
	Set(key string, val []byte, ttlSeconds int)
	Delete(key string)
}
J
put handlers/products.go <<'J'
package handlers

import "example.com/orders-svc/internal/cache"

func GetProduct(s cache.Store, id string) []byte { b, _ := s.Get("product:" + id); return b }
J
put handlers/customers.go <<'J'
package handlers

import "example.com/orders-svc/internal/cache"

func GetCustomer(s cache.Store, id string) []byte { b, _ := s.Get("customer:" + id); return b }
J
put handlers/orders.go <<'J'
package handlers

func GetOrder(id string) []byte { return load(id) }

func load(id string) []byte { return nil }
J
put docs/PLAN.md <<'J'
# Plan: cache GET /orders/{id}

Approach: a per-handler in-process cache (`sync.Map`) inside `handlers/orders.go`.

- [ ] 1. Add `orderCache` and read-through in `GetOrder`
- [ ] 2. Invalidate on PUT/DELETE within the same process
- [ ] 3. TTL eviction (60s) for `orderCache` entries
- [ ] 4. Hit/miss counters
J
commit_all "orders-svc: handlers, cache package, ADR-007, plan" "2026-09-10T10:00:00"
git checkout -q -b feat/order-cache
put handlers/orders.go <<'J'
package handlers

import "sync"

var orderCache sync.Map

func GetOrder(id string) []byte {
	if v, ok := orderCache.Load(id); ok {
		return v.([]byte)
	}
	b := load(id)
	orderCache.Store(id, b)
	return b
}

func InvalidateOrder(id string) { orderCache.Delete(id) }

func load(id string) []byte { return nil }
J
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "orders: in-process orderCache with invalidation (plan steps 1-2)" "2026-09-14T11:00:00"
