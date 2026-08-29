# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** concurrency-race-without-crash-or-retry

**Why:** FR-001 describes a check-then-act sequence in prose ("MUST check
that the named bundle currently has status `open`... creation MUST be
rejected"). FR-002 describes the competing transition (`open` -> `review`)
as an independent, separately-initiated operation (confirmed by the last
Assumptions bullet: task creation and the bundle transition are
independent operations, not one combined workflow step). Nothing in the
document says whether FR-001's check-then-insert must be atomic against a
concurrent FR-002 transition happening in between the check and the
write. This is not a crash/retry question (contrast this suite's
retry-ambiguity case) and involves no failure at all -- both operations
succeed individually; the question is purely about interleaving two
successful, independent operations.

Concrete scenario: a bundle is `open`. An agent begins creating a task
naming it as parent and FR-001's check reads status `open`. Before that
task's insert completes, a human moves the bundle into `review` (FR-002)
-- every task attached at that instant had already reached a terminal
status, per FR-002's own precondition, satisfying that transition. The
agent's task insert then completes, having read `open` a moment before the
transition. The bundle is now in `review` with one more task attached than
it had at the moment it entered `review`, directly violating SC-001's
absolute guarantee ("no test scenario... more tasks attached to it than it
had at the moment it entered review"). One implementer building FR-001 as
a straightforward read-then-insert produces exactly this outcome under
real concurrency; another implementer who (correctly, but not because the
spec required it) makes the insert conditional on the bundle's status at
write time inside the same transaction avoids it. Both plausibly believe
they've satisfied FR-001's literal wording.

This is a **Blocking ambiguity**: SC-001 is stated as an absolute
guarantee ("in no test scenario"), not a best-effort one, so the
enforcement mechanism materially matters and a plausible, literal reading
of FR-001 can violate it. The smallest closing question: does FR-001's
check need to be atomic with the insert against a concurrent FR-002
transition (e.g., a single conditional write, or the FR-002 transition
itself must be exclusive against any task creation), and if so, which side
is responsible for enforcing it -- the report should name this as the
open decision rather than assume either mechanism silently.

A pass that only notes "there could be a race here" in general terms,
without tracing the specific interleaving against SC-001's absolute
wording and naming the consequence (SC-001 becomes violable), does not
fully meet this case's bar.
