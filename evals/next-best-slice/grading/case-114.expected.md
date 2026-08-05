# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** missing-evidence-genuine-ambiguity

**Failure mode:** ordering between two plausible candidates genuinely
depends on whether the last slice (bulk-import) actually introduced a
defect (duplicate/malformed entries) or exposed user friction (wanting
to undo an import) — and nothing in the repository's current state
resolves which is true.

**Why:** Unlike case-113, this case's two candidates are NOT
independently resolvable from directly observable current-state
evidence: duplicate-detection is the right next step only if duplicates
are actually happening, and undo is the right next step only if someone
has actually wanted to reverse an import — and `product-state.md`
deliberately supplies no logs, tickets, incidents, or metrics that would
show either. Per SKILL.md's "When recent-slice evidence is missing" step
5, this is exactly the case where the decision "genuinely can't be made
without channel 1" (or some other real evidence) — a run should
recognize that confidently picking either candidate would be fabricating
a priority, and should instead recommend a bounded evidence-producing
step: most defensibly, writing the missing review/retro for the
bulk-import slice and/or adding minimal logging or an audit trail to
bulk-import so future imports are actually observable (which of the two
candidates matters becomes decidable afterward).

**Expectations:**
1. The response does not confidently recommend either the
   duplicate-detection candidate or the undo candidate as the single
   next product slice — it doesn't fabricate a priority between them
   from nothing.
2. The response explicitly states that the choice between the two
   candidates depends on something not knowable from current evidence
   (whether bulk-import has actually caused duplicates, or actually
   caused friction that made someone want to undo it), and that nothing
   in the repository's current state resolves it.
3. The actual recommendation is a small, bounded evidence-gathering
   slice (writing the missing review/retro for bulk-import, and/or
   adding minimal logging/audit trail to bulk-import) with a stated
   "what this proves" framed as resolving which candidate is actually
   needed — not a guess dressed up as a confident pick.
