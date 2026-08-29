# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** sufficiently-constrained-no-material-finding

**Why:** This fixture was deliberately written to close every one of the
seven pressure categories the skill is supposed to check, on purpose,
including the exact traps other cases in this suite plant:

- State/transition: only two terminal outcomes per `event_id` (rejected or
  recorded), no orphan or unreachable state.
- Invariants/enforcement: uniqueness is enforced by a database constraint
  (FR-003), not by a component that merely hopes to enforce it via a
  read-then-write check -- the enforcement mechanism matches the boundary
  making the guarantee.
- Ownership: exactly one authoritative record per `event_id`, created
  once, never modified afterward (FR-005) -- no second representation to
  disagree with it.
- Concurrency: the exact same race this suite's retry/concurrency cases
  exploit elsewhere is explicitly closed here (Acceptance Scenario 3,
  FR-003, SC-001) via database-level arbitration, not application-level
  locking.
- Failure/partial outcome: the crash-before-responding case (this suite's
  case-001 trap) is explicitly named in Edge Cases and explicitly resolved
  -- the system doesn't need to distinguish "caller never got a response"
  from "unrelated duplicate delivery" because both produce the same
  correct outcome by construction.
- Composition/boundary: the ordering between an external dependency
  (signature validation) and this feature's own state is pinned exactly
  (FR-001/FR-004), including the easy-to-miss detail that a rejected
  delivery must not reserve the `event_id`.
- Cardinality/identity: uniqueness scope is stated, and the one case this
  specification does *not* handle (sender reusing an `event_id` for two
  genuinely different events) is named as an explicit, deliberate
  Assumption rather than a silent gap.

A correct pass reaches **Ready to implement**, with no Blocking findings
and no fabricated Material findings that re-litigate something this
document already closes (in particular: no finding claiming retry/crash
behavior, concurrent-delivery arbitration, or event-id reservation-on-
rejection is unspecified -- all three are explicitly and correctly
resolved in the text above). A report that manufactures a Blocking or
Material finding restating any of these already-closed points fails this
case, regardless of how the finding is phrased.

A pass may legitimately surface up to two minor, genuinely open points as
**Material gaps** without changing the verdict or being required to pass --
for example: (a) FR-006 doesn't specify whether the recorded-duplicate
response includes the original event's payload or `recorded_at` timestamp
(an obvious defensible default: the outcome classification alone satisfies
FR-006 as written), and (b) FR-006's "exactly three outcomes" doesn't
actually have a home for an infrastructure failure (a database write
failure/timeout, or the signature-validation dependency itself failing)
that is neither a signature rejection nor a completed recording -- this is
a real, independently-confirmed gap (found by more than one independent
read of this fixture) and is legitimate to raise as Material, since it
doesn't threaten the recording invariant itself (no row is created on such
a failure, so a retry is still safe) but does mean FR-006's completeness
claim isn't literally satisfiable. Neither point is required for the case
to pass. What is required is that no Blocking finding appears and that
nothing already resolved in the document (state/transition, invariant
enforcement, ownership, the concurrent-insert race, the crash-before-
responding case, signature-vs-recording ordering, or `event_id` uniqueness
scope) is reported as open.
