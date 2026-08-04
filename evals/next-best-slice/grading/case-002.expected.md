# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** user-value-vs-prerequisite

**Why:** This case is deliberately built to allow more than one defensible
answer — it's one of the cases where multiple reasonable recommendations
are intended, and grading should weigh the quality of the reasoning over
matching one specific pick. Two candidates are legitimately strong: the
FTS5 swap (addresses a real, review-flagged growth risk — 380ms at 500
rows against a ~118k-row and growing catalog — with a bounded, contained
change) and the production-latency-instrumentation slice (the smallest
possible way to get a real number before committing to a swap that isn't
strictly proven necessary yet, since nothing has actually broken). Both
engage honestly with the flagged scale numbers using the skill's own
criteria (risk reduction and architectural momentum favor the swap; size
and evidence-thinness favor instrumentation first). What should NOT pass:
picking result-highlighting or filters while ignoring the scale risk
entirely (user value alone, unweighed against anything else), or jumping
to something bigger than a bounded FTS5 swap (e.g. "migrate to
Elasticsearch," "rebuild the whole catalog data layer") — both trip this
skill's own refusal list. Grade on whether the response explicitly weighs
the two legitimate options against each other using stated criteria, picks
one, and gives an evidence-grounded reason for the other waiting — not on
which of the two it picked.
