## field-debug checkpoint: checkout-bff -> payments-svc intermittent timeouts

**Objective**: find why ~8% of requests from checkout-bff to payments-svc
have been timing out since 14:02 UTC today.

**Current system model**: checkout-bff (our service) makes synchronous
HTTPS calls to payments-svc (owned by the Payments team, reachable only
over the internal network -- no shell or log access to it from here).
Requests either complete normally or hang until checkout-bff's own 5s
client-side timeout fires with no response.

**Observations**:
- checkout-bff's own HTTP client pool metrics: ~30% utilization, no
  queueing, no pool-exhaustion signal.
- checkout-bff's outbound call metric to payments-svc: ~8% of calls hang
  until the 5s client timeout; the remaining ~92% complete in under
  200ms.
- Failures started sharply at 14:02 UTC -- no ramp, no gradual onset.
- No application-level errors or exceptions logged by checkout-bff for
  the timed-out calls; they simply never get a response.

**Active hypotheses**:
- H1: checkout-bff's own HTTP client pool is exhausted or misconfigured.
  (weakening -- pool metrics look normal, but not yet eliminated)
- H2: something between checkout-bff and payments-svc is dropping the
  connection before it's established (network/firewall/security group).
- H3: payments-svc itself is slow or unhealthy for a subset of requests.

**Ruled-out hypotheses**: none yet. H1 is weakened by the pool metrics
but not eliminated.

**Assumptions**: assuming payments-svc's own health dashboard looked
normal around 13:50 UTC -- told secondhand by a teammate, not
independently checked by me.

**Unknowns**: whether the failing requests ever reach payments-svc's
host at all; whether the fault is application-level, network-level, or
on payments-svc's own side.

**Constraints**: I don't have shell, log, or firewall/security-group
access to anything between checkout-bff and payments-svc -- that's
NetOps' and the Payments team's territory. No one from Payments is
reachable right now.

**Last known-good / first known-bad boundary**: last known-good is
14:01 UTC (baseline latency, zero failures in the preceding hour);
first known-bad is 14:02 UTC (failures begin abruptly).

**Next discriminating move**: delegated to NetOps on-call (see below) to
check whether the failing connection attempts ever reach payments-svc's
host at all, since that discriminates H2 (would not reach it) from
H1/H3 (would reach it, then either queue or hang on the destination
side).

**Time-sensitive evidence that should be revalidated on resume**: the
30% pool-utilization reading and the ~8% failure rate are both
point-in-time snapshots taken around 14:10 UTC -- confirm they still
hold before relying on them further; traffic and pool state can shift
within the hour.

---

## field-debug delegation: checkout-bff -> payments-svc packet-level reachability

**QUESTION**: during the 14:02+ failure window, do checkout-bff's
connection attempts to payments-svc ever reach payments-svc's host, or
are they being dropped before arrival?

**WHY**: discriminates H2 (network/security-group -- dropped before
arrival) from H1/H3 (pool exhaustion or destination-side slowness --
would reach the host, then either queue on our side or hang on theirs).

**KNOWN**: failures started sharply at 14:02 UTC with no ramp;
checkout-bff's own connection-pool metrics look normal; no app-level
exception is logged for the failing calls.

**REQUEST**: run a packet capture (or equivalent) on checkout-bff's
egress during a live failure, and check whether SYNs addressed to
payments-svc's host are being ACKed.

**CONSTRAINTS**: don't restart or redeploy anything -- this is affecting
live checkout traffic.

**RETURN**: whether the SYNs reach payments-svc's host, and
payments-svc's own observed request latency/error rate during the same
window, if visible from your side.

I'm off-shift as of 14:20 UTC. Whoever picks this up: NetOps' answer
should already be in `delegation_response.md`.
