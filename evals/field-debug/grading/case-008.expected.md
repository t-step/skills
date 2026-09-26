# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** checkpoint-resume-delegation-assimilation-firewall-cidr-mismatch

**Hidden ground truth:**

Marco's checkpoint correctly narrowed the problem to "does the connection
ever reach payments-svc's host" and correctly delegated that question to
NetOps. NetOps's packet capture (an actual observation: SYNs sent, never
ACKed, no response traffic from payments-svc at all) is genuine and
sufficient to eliminate H1 (checkout-bff's own pool) and H3
(payments-svc-side slowness) -- if the connection never reaches
payments-svc, neither can be the cause. But NetOps's own conclusion
("looks like a networking issue... probably a firewall or security-group
rule, I'd guess a stale rule") is an unverified guess they explicitly
flag as unverified ("haven't had time to dig into it further").

The two attachments NetOps includes almost in passing -- the deploy log
and the current security-group config -- actually pin down the specific
mechanism, more precisely than NetOps's own guess:

- The 13:55-13:58 UTC gateway redeploy (routine cert rotation, no app
  code change) reassigned checkout-bff's gateway pods from
  `10.4.2.0/24` to `10.4.5.0/24`.
- `payments-svc`'s inbound security group only allows `10.4.2.0/24`
  (added 2025-11-03) -- it was never updated for the new pod IP range.
- So every connection attempt from the new pods (10.4.5.0/24) is
  silently dropped by the security group before reaching payments-svc,
  which is exactly consistent with NetOps's packet-capture observation
  (SYN sent, never ACKed, no response seen).
- The timing is consistent with the causal story: redeploy completes at
  13:57:41-13:58:10 UTC (old pods fully drained by 13:58:10), and failures
  begin at 14:02 UTC. The ~4-minute gap itself is not explained by any
  evidence in the case files -- nothing here establishes connection-pool
  cycling or any other specific mechanism for the delay -- so it should be
  named as an unexplained residual, not resolved away as "plausibly
  explained."

The correct root cause is therefore more specific than "a networking
issue": the security group protecting payments-svc was scoped to a
static CIDR block that the cert-rotation redeploy silently invalidated
by reassigning checkout-bff's gateway pods to a different IP range.
"Networking issue, probably a firewall rule" is directionally right but
not itself the root cause -- it's NetOps's INFERRED guess, offered
without having checked the two attachments that would confirm or refute
it.

**What a good resumed investigation does NOT do:** restart from zero
(re-litigating whether the pool is exhausted from scratch, ignoring that
Marco's checkpoint already weakened H1 with real metrics), fabricate its
own packet capture or claim access it doesn't have, or stop at "NetOps
confirmed it's a networking issue" without using the attachments to get
more specific.

## Grading

- REQUIRED: explicitly loads and builds on Marco's checkpoint rather than
  re-investigating already-established points from scratch (e.g.,
  references the existing hypotheses and/or the pool-utilization finding
  as prior context, not as something it just discovered independently).
- REQUIRED: separates NetOps's actual observation (SYNs sent, never
  ACKed, no response from payments-svc) from NetOps's own conclusion
  ("looks like a networking issue... probably a firewall rule") --
  treats the conclusion as an unconfirmed hypothesis NetOps itself
  flagged as a guess, not as a settled root cause.
- REQUIRED: uses `deploy_log.md` and `security_group_config.md` to reach
  the more specific mechanism -- the 13:55-13:58 UTC redeploy moved
  checkout-bff's pods from `10.4.2.0/24` to `10.4.5.0/24`, and
  payments-svc's security group only allows `10.4.2.0/24` -- rather than
  stopping at "NetOps says it's networking."
- REQUIRED: correctly retires or clearly weakens H1 (pool exhaustion) and
  H3 (payments-svc-side slowness) using NetOps's observation that the
  connection never reaches payments-svc at all -- does not continue to
  present all three original hypotheses as equally live.
- REQUIRED: flags at least one of the checkpoint's explicitly-named
  time-sensitive facts (the 30% pool-utilization reading and/or the ~8%
  failure rate) as something to revalidate rather than reusing it
  uncritically as still-current in the final conclusion -- while not
  re-litigating the stable facts (topology, ownership boundary, the
  request path) that don't need re-checking.
- REQUIRED: does not fabricate its own access to payments-svc, the
  network path, or the security group beyond what NetOps already
  provided (e.g., does not claim to have run its own packet capture or
  independently confirmed the security-group change).
- BONUS: notes the timing correlation between the redeploy completing
  (13:57:41-13:58:10 UTC) and the first-known-bad boundary (14:02 UTC)
  as consistent with the causal story, AND explicitly flags the ~4-minute
  gap itself as unexplained by any evidence in hand, rather than asserting
  a specific mechanism (e.g. "pool cycling") for it that nothing in the
  case files supports.
