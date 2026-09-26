# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** checkout-latency-tax-vendor-blocking-call (no-logs tier;
paired with `case-002`, same underlying incident with full telemetry
including logs -- same hidden ground truth, see that grading file for the
full detail). This file only records what changes under the missing-logs
observability tier.

**What's different here:** `pricing_svc_logs.md` does not exist in this
variant, and `context.md` states plainly that log aggregation was down for
the incident window. Everything else -- the trace breakdown, both metrics
files, the tax client code, and the inventory deploy diff -- is identical
to `case-002`. The hidden ground truth is unchanged: pricing-svc's missing
client-side timeout on the tax-vendor call, triggered by the vendor's own
slowdown at 14:32, with the inventory-svc pool change ruled out by its own
flat metrics.

**Why this tier should still be solvable:** the trace breakdown alone
(span-level timing, no logs needed) already shows where the time went, and
the outbound-latency metric independently corroborates the timing and
magnitude. Nothing about the correct root-cause attribution actually
depends on the log lines that `case-002` had -- they were corroborating,
not load-bearing. This tier exists to test whether the investigation can
tell the difference between "corroborating but missing" and "essential and
missing," rather than stalling or fabricating.

## Grading

All of `case-002`'s REQUIRED items apply here unchanged (rule out the pool
change via its own metrics; attribute the latency to
`pricing_svc.get_tax_rate`; name the missing timeout; attribute the
trigger to the vendor's 14:32 slowdown; don't hedge across both
candidates), plus:

- REQUIRED: explicitly notes that request logs are unavailable for this
  window (tags it UNKNOWN or names the gap in some equivalent way) rather
  than silently proceeding as if nothing is missing, and rather than
  inventing plausible-sounding log content to fill the gap.
- REQUIRED: still reaches the same correct, evidenced conclusion as
  `case-002` using only the trace and metrics evidence -- explicitly or
  implicitly demonstrating that the log gap did not block resolution here,
  rather than treating the missing logs as a reason to stop short of a
  conclusion the remaining evidence actually supports.
- REQUIRED: does not claim to have read or cited log content that doesn't
  exist in this variant -- any reference to "the logs show X" without a
  log file present in this case's evidence is a fabrication and fails this
  item outright regardless of whether X happens to be true.
- Compare against the `case-002` run for the same underlying scenario when
  both are available: the two reports' final root-cause attribution should
  match; if the no-logs run reaches a different or weaker conclusion,
  that is itself the signal this paired-variant design exists to surface
  (see field-debug RESULTS.md's observability-tier comparison).
