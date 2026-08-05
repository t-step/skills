# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** carried-forward-evidence

**Failure mode:** a concern raised several completed slices ago is absent
from the newest retrospective and must not silently lose standing or gain
automatic priority

**Why:** The signature-verification observability gap was named in
cycle-1's retro (three completed slices before the one that just landed)
and is still listed as `[OPEN]` in follow-ups.md — never addressed,
falsified, or retired. Cycles 2 through 4 worked on unrelated things and
their own retros never restate it. A response that only looks at cycle-4
(or even cycles 2-4) in isolation would miss it entirely and default to
one of the fresher, weaker cycle-4/backlog candidates (page-size
configurability, the unrequested retry button). The correct read pulls it
back in via follow-ups.md (or by reading cycle-1's retro directly, since
it's within the most-recent-three-retros window even without the
maintained artifact) and weighs it on its own merits: it's a real,
demonstrated risk-reduction and learning-value case (an unresolved
question about distinguishing probing/misconfiguration from ordinary
errors on a payment webhook endpoint), not a large or speculative one —
small, bounded, reversible (add a distinct log tag/metric). The DLQ
threshold item is a real but weaker alternative (no concrete demonstrated
harm yet, just "untuned"). Per-consumer filtering must NOT appear as a
candidate at all — it was explicitly retired in cycle-3 and follow-ups.md
says so; recommending it (or reviving it as a live alternative) is a
miss. The page-size and manual-retry backlog items are legitimate but
weaker: fresh, cheap, and explicitly unrequested/unevidenced.

A good response should not treat the age of the signature-verification
concern as itself the reason it wins — it should tie the pick to risk
reduction and learning value (the retro's own follow-up question), the
same criteria used everywhere else in this skill, and should be able to
name the newer cycle-4 finding as a real alternative that waits rather
than ignoring it.
