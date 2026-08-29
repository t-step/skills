# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** internal-capability-not-user-facing

**Why:** This plan has no user-facing or product surface at all -- no
endpoint, no UI, nothing a person interacts with directly -- but it
still establishes an independently meaningful, independently verifiable
system property: a worker that crashes mid-job no longer silently loses
that job, because another worker reclaims and reprocesses it once its
heartbeat goes stale. That property is directly verified by T5 without
needing any product-facing framing. The correct composition keeps
T1-T5 together as one vertical slice (they are small and tightly
coupled: the heartbeat column, the loop that updates it, the reclaim
function, and its wiring), states "Delivers" in system-property terms
close to the sentence above rather than "adds heartbeat column and
reclaim function," and does not refuse or downgrade this as a valid
vertical delivery slice merely because nothing about it is user-facing.
It also should not invent user-facing framing the fixture doesn't
support (e.g. a dashboard showing reclaimed jobs). Separately, T1 (the
migration) should not be pulled out as its own horizontal enabler: the
fixture states nothing else in the plan or codebase depends on it, so
isolating it would unlock no additional parallelism and avoid no
duplication.
