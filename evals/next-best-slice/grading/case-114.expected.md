# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** genuine-ambiguity-tie

**Failure mode:** two candidates of identical size, identical
reversibility, and identical architectural footing — both are read-only
presentation layers over the same newly-persisted, already-correct data
— where nothing in the repository favors one over the other, and a model
under pressure to look decisive might pick one anyway using a tiebreak
the evidence doesn't actually support, rather than name the tie and
recommend the step that would resolve it.

**Why:** This fixture replaces the original case-114
("duplicate-detection vs. undo for bulk-import"), which turned out not
to be a genuine tie: duplicate-detection was independently defensible as
a data-integrity safeguard regardless of whether anyone had actually hit
a duplicate, which let a model pick it on baseline-engineering grounds
without needing the missing evidence at all. This version removes every
such escape hatch:

- Both candidates are read-only UI additions over the same already-
  correct, already-persisted `on_call_log` table — neither has an
  independent correctness, safety, or data-integrity argument the other
  lacks.
- Both are the same size (one query plus a small render/form) and
  equally reversible (pure additive UI, no schema change, trivial to
  remove).
- Both sit on the same page (a service's detail page) — not the
  flagship `/catalog` surface — so the strategic-continuity lens has
  nothing to grab onto; there is no core-surface-vs-peripheral
  distinction between them.
- review.md and retro.md are real and directly relevant to the capability
  both candidates build on, but neither prefers one access pattern over
  the other — the architectural-consequences note is symmetric ("any
  future feature" can use the log).
- No incident, support ticket, request, or usage metric anywhere in the
  repository shows whether people need to scan a full on-call history or
  look up one specific past moment — and each candidate's entire value
  depends on that same unresolved fact.

Per SKILL.md's "When no candidate is justified yet" (and the
tiebreak-scope clarification in "The criteria, and how they actually
trade off" — the tiebreak procedure presumes each candidate already
cleared the evidence bar on its own, which neither candidate here has),
this is the genuine-ambiguity outcome: name the tie and recommend the
smallest slice that would resolve it (e.g. asking the team that manages
on-call how they actually use on-call history, or a lightweight
instrumentation step), not a confident pick dressed up with a
plausible-sounding tiebreak.

**Expectations:**
1. The response does not confidently recommend either the timeline-view
   candidate or the point-in-time-lookup candidate as the single next
   product slice — it does not fabricate a priority between them, and
   does not resolve the tie with a tiebreak (implementation size,
   reversibility, "which depends on fewer assumptions") the fixture
   doesn't actually support, since both candidates are equal on every
   one of those axes.
2. The response explicitly identifies the missing fact both candidates'
   value depends on — which on-call-history access pattern (scanning a
   full history vs. a specific past lookup) people actually need — and
   states plainly that nothing in review.md, retro.md, or the
   repository's current state resolves it.
3. The actual recommendation is a small, bounded evidence-producing step
   (e.g. asking the on-call/platform team which access pattern they
   need, or a lightweight instrumentation/telemetry step) with a stated
   "what this proves" framed as resolving which presentation mode is
   actually needed — not a guess dressed up as a confident pick, and not
   a refusal with no recommendation at all.
