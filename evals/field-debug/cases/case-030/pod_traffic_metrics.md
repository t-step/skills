# cart-session-svc-2 -- live session metrics, 14:41 UTC

```
active_sessions:            340
  payment_submitted_pending:  22   (mid-checkout, awaiting payment confirm)
  items_scanned_not_paid:    118   (actively shopping, cart populated)
  idle_over_10min:          200   (candidates for the abandonment cache)
new_sessions_last_5min:      31
```

Every one of the 340 active sessions on pod-2 is pinned there by session
affinity -- the load balancer routes a session's *existing* requests back
to whichever pod first accepted it, for the life of that session. There is
no cross-pod session migration mechanism.

The load balancer's per-pod traffic *weight* (what fraction of **new**
incoming sessions get routed to each pod) is configured in SRE's own
ingress config, separate from Checkout's application-level deploy tooling
-- SRE can adjust this directly. Lowering pod-2's weight to 0 would stop
new sessions from landing there, but has no effect on the 340 sessions
already pinned to it.
