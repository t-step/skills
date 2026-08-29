# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** concurrency-risk-boundary

**Why (revised after iteration 1):** T1 changes concurrency/lifecycle
semantics (process-local to shared/networked session state, with a
named race window) and three call sites (T2, T3, T4) are about to build
on it. Iteration 1 found the original answer key was under-specified:
it read as requiring T2/T3/T4 to wait for T5 (verification) to *pass*,
but the source plan doesn't actually settle that -- T1's public
interface ("get, set, delete") is stated to stay the same, so a
migration can be written and even reviewed correctly without T5 having
run yet; the risk T5 covers is a runtime-correctness question, not an
interface-compatibility one. Two different, defensible teams would make
different calls here:

- **Conservative:** bundle T1 with T5 (or otherwise hard-gate T2/T3/T4 on
  T5 passing) so nothing proceeds until the concurrency behavior is
  actually proven.
- **Less conservative:** let T2/T3/T4 start once T1's interface is
  stable, treat T5 as running in parallel, and name the residual risk
  explicitly if T5 later finds a problem.

Both are legitimate planning choices; forcing one as "the" answer would
be tuning the skill to a brittle key rather than reflecting what the
source plan actually requires. What's actually required, and what
distinguishes a correct answer from a wrong one, is:

- **Required:** T1 isolated as its own slice (or paired specifically
  with T5), with the concurrency-semantics/unverified-assumption reason
  named.
- **Required:** T2/T3/T4 each depend on at least T1's implementation.
- **Required:** T5 attached to T1 as its verification checkpoint, not
  stranded or omitted.
- **Required:** T2/T3/T4 marked parallel-safe with each other (disjoint
  files, per the fixture).
- **Defensible either way, but must be stated, not assumed:** whether
  T2/T3/T4 also gate on T5 passing. A run that lets migrations proceed
  before T5 completes without ever naming that as a choice or risk is
  the actual failure mode -- not the choice of gating strategy itself.
- **Would be wrong:** batching T1 into one of the migrations without
  comment; not naming the concurrency-risk reason at all; leaving T5
  disconnected from T1's purpose; asserting T2/T3/T4 as unconditionally
  independent of T1.
