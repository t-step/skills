#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# Go payout service; retry logic built on an idempotency assumption the vendor notes contradict
new_repo "$out"
put go.mod <<'J'
module example.com/payout-svc

go 1.22
J
put docs/PLAN.md <<'J'
# Plan: resilient transfers

Assumptions
- A2: The provider's `POST /transfers` is idempotent, so a failed call can simply be retried.

Tasks
- [x] 1. Request builder and signing (`internal/provider/request.go`)
- [x] 2. Metrics counters (`internal/metrics/metrics.go`)
- [x] 3. Queue consumer calls the provider client (`internal/queue/consumer.go`)
- [ ] 4. Provider client with retry on failure (`internal/provider/client.go`)
J
put docs/vendor-notes.md <<'J'
# Provider notes (from the 2026-09-03 call)
- `POST /transfers` is NOT idempotent by default. Resending the same body creates a second transfer.
- Send an `Idempotency-Key` header to make a retry safe; keys are honored for 24h.
J
put internal/provider/request.go <<'J'
package provider

import "net/http"

func BuildTransfer(base string, amount int64, to string) (*http.Request, error) {
	return http.NewRequest("POST", base+"/transfers", nil)
}

func Sign(r *http.Request, secret string) { r.Header.Set("X-Signature", secret) }
J
put internal/metrics/metrics.go <<'J'
package metrics

var Transfers, Failures int
J
put internal/queue/consumer.go <<'J'
package queue

import "example.com/payout-svc/internal/provider"

func Handle(c *provider.Client, amount int64, to string) error { return c.Transfer(amount, to) }
J
commit_all "payout-svc: request builder, metrics, consumer" "2026-09-13T10:00:00"
put internal/provider/client.go <<'J'
package provider

import "net/http"

type Client struct {
	HTTP    *http.Client
	BaseURL string
}

// Transfer retries up to 3 times on any failure.
func (c *Client) Transfer(amount int64, to string) error {
	var err error
	for i := 0; i < 3; i++ {
		req, _ := BuildTransfer(c.BaseURL, amount, to)
		var resp *http.Response
		if resp, err = c.HTTP.Do(req); err == nil && resp.StatusCode < 500 {
			return nil
		}
	}
	return err
}
J
put internal/provider/client_test.go <<'J'
package provider

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestRetryDoesNotDuplicate(t *testing.T) {
	posts := 0
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		posts++ // the provider records the transfer, then answers 500
		w.WriteHeader(500)
	}))
	defer srv.Close()
	c := &Client{HTTP: srv.Client(), BaseURL: srv.URL}
	_ = c.Transfer(100, "acct_1")
	if posts != 1 {
		t.Fatalf("expected 1 transfer recorded by fake provider, got %d", posts)
	}
}
J
