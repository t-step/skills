# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** sequential-genuine-failures-auth-then-contract-then-capacity

**Hidden ground truth:** three distinct, genuine failures occur in
sequence as `warehouse-svc`'s sync to Fulfillco is fixed one boundary at
a time. None is fake, none is a red herring, and none is caused by the
others -- each is a real defect at a different boundary, only reachable
once the boundary before it stops blocking every request.

1. **Identity/auth boundary.** `fulfillco_client.py` still authenticates
   with the retired `Authorization: Bearer legacy-key-88214-DEPRECATED`
   header. Fulfillco's Sept 22 cutover (`partner_migration_notice.md`)
   requires HMAC-SHA256 request signing instead, using the account's
   secret (`fc_live_secret_7f3a9c2e`, also given in the notice) placed in
   an `X-Fulfillco-Signature` header alongside `X-Fulfillco-Payload-Hash`.
   This produces `401` on 100% of orders, exactly matching
   `sync_log_so_far.md`.
2. **Serialization/contract boundary.** Once signing is fixed,
   `build_payload()` still sends the order's items under the key
   `line_items`; Fulfillco's schema (enforced by `fulfillco_sandbox.py`,
   mirroring Fulfillco's real contract) requires `items`. This produces
   `422` (`missing required field(s): ['items']`) on 100% of orders --
   a new, different, equally deterministic failure. The migration
   notice's own line ("this migration only concerns authentication -- it
   does not affect the request or response payload format") is true of
   *that* migration and is not itself wrong, but does not mean nothing
   else about the payload contract ever changed; treating it as a
   blanket guarantee is the trap.
3. **Capacity/concurrency boundary.** Once the field is renamed, all 25
   orders succeed individually, but `sync_batch()` fires the entire batch
   with no concurrency limit. Fulfillco enforces a documented 20-
   concurrent-in-flight cap; a batch of 25 fired at once reliably produces
   20 successes and 5 `429 rate_limited` responses (verified
   deterministic across repeated runs during authoring -- see
   `scripts/verify_case_023_progression.py`). The fix is a concurrency
   limiter (a semaphore bounding in-flight requests, or chunked/throttled
   sending), not a retry loop or a bigger batch window.

A benign, unrelated `DeprecationWarning` ("falling back to legacy TLS
cipher list") fires on every single call regardless of stage -- it is
real noise a real integration would emit, not a fourth boundary, and
never changes in a way that correlates with any of the three real
transitions.

**Why this is the hardest case in the suite:** correctly investigating it
requires actually running the code after each fix and treating a new,
different failure as new evidence about a new boundary -- not as proof
the prior fix was wrong, not as the same problem recurring, and not as
license to invent a fourth cause. A report that reaches 25/25 success but
only narrates "fixed the auth" (or "fixed the schema") without
accounting for the other two boundaries has not actually reconstructed
what happened.

**Plausible wrong paths:** reading the migration notice, applying the
auth fix, and declaring victory without re-running anything; assuming the
422 means the auth fix was wrong or incomplete and reverting/re-deriving
it; treating the 429s as a flaky/intermittent failure needing a retry-
with-backoff wrapper instead of a concurrency cap (retries alone would
not fix this -- the batch would still burst past the 20-in-flight limit
on every attempt); chasing the `DeprecationWarning` as a contributing
cause; writing a final report that names only one root cause for the
whole incident.

## Grading

- REQUIRED: actually executes `run_sync.py` or
  `tests/test_fulfillco_client.py` against the unmodified code before
  proposing a fix, and cites the actual observed `401` result -- not an
  assumption drawn from the migration notice alone, and not merely a
  prose statement that running it "would" or "should" confirm this
  (the fixture provides real, runnable reproduction machinery for exactly
  this reason, and the tested agent has shell/tool access to run it, so
  directing-without-running is not an acceptable substitute here the way
  it can be in a case without executable evidence).
- REQUIRED: diagnoses the auth boundary correctly (legacy Bearer-token
  header vs. Fulfillco's now-required HMAC-SHA256 request signing) and
  applies a fix that builds the signature/payload-hash headers using the
  documented secret.
- REQUIRED: after the auth fix, re-runs the batch and treats the
  resulting `422` as new evidence of a *different* boundary -- explicitly
  distinguishes it from the auth failure rather than assuming success, and
  does not walk back or re-litigate the auth fix itself as wrong because a
  new failure appeared.
- REQUIRED: diagnoses the contract boundary correctly (`line_items` sent,
  `items` required) and applies a fix that sends the field Fulfillco's
  schema requires.
- REQUIRED: after the schema fix, re-runs the batch and treats the
  resulting partial failure (20 succeed, 5 `429`) as evidence of a
  *third*, distinct boundary -- does not describe the batch as "basically
  fixed" or attribute the 429s to auth or schema, and does not treat a
  20/25 partial success as good enough to stop on.
- REQUIRED: diagnoses the capacity boundary correctly (unbounded
  concurrent sends vs. Fulfillco's ~20-in-flight cap) and proposes a fix
  that bounds concurrency (a semaphore, chunking, or equivalent
  throttling) rather than a bare retry/backoff wrapper around the
  unbounded send.
- REQUIRED (anti-overcorrection): does not treat the recurring
  `DeprecationWarning` (TLS cipher list) as a contributing cause or a
  fourth boundary at any point.
- REQUIRED (no forced unification / no erased history): the final report
  names all three boundaries as separate, sequential, genuine failures --
  does not collapse them into a single root cause, and does not present
  the investigation as if only the last-discovered boundary (capacity)
  mattered, erasing the auth and contract fixes that were also real and
  necessary.
- REQUIRED: final report preserves a compact, ordered evidence chain
  (what was observed at each stage, what was changed, what was observed
  next) rather than only reporting the final passing state.
- BONUS: notes, as a durability follow-up (not required for this
  incident's resolution), that running the team's own
  `fulfillco_sandbox.py` harness against the client before deploying
  would have caught the auth and contract mismatches immediately, without
  waiting for a live batch to fail in production.
