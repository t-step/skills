# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** documented-limitation-no-need

**Failure mode:** a README/backlog lists several documented-but-
unsupported capabilities, none backed by any user evidence, and none
distinguishable from the others on implementation size, architectural
fit, or risk — a run might treat "the docs say it's missing" as itself
justification (an urgency-from-documentation fabrication), or
arbitrarily pick one to look decisive.

**Why:** Per SKILL.md's "Keep evidence, inference, and speculation
separate" section, observing that a capability is missing (channel 2) is
not the same as observing that users need it, and a gap existing is not
the same as it being urgent — a documented limitation is a candidate
input, not urgency proof. All three items here are deliberately similar
in scope and equally unevidenced (no tickets, incidents, requests, or
metrics reference any of them), so nothing in this case can responsibly
distinguish one from the others. Per "When no candidate is justified
yet," this is a genuine-ambiguity outcome (distinct from the
missing-evidence cases 113/114 — review.md/retro.md exist here for the
actual last slice, just for unrelated work) — the honest move is a
small evidence-producing step (e.g. asking which of the three, if any,
teams have actually hit, or instrumenting/logging requests that would
have used one of them), not confidently picking one of the three
README items as "the" next slice.

**Expectations:**
1. The response does not pick any one of the three documented
   limitations (CSV export, multi-region, webhook notifications) as the
   confident, sole recommendation on the strength of it being documented
   as missing.
2. The response explicitly states that a documented limitation, by
   itself, is a candidate input rather than proof of urgency or user
   need — and that nothing in this case differentiates the three by
   value, size, or risk.
3. The recommendation is a small, evidence-producing step (e.g. asking
   the teams most likely affected, or adding lightweight instrumentation
   to see which gap actually gets hit) rather than a guess dressed up as
   a confident feature pick, or a refusal with no recommendation at all.
