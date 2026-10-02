# What actually happened

All dates/facts below postdate the chosen cutoff (2023-05-15) and were
excluded from every agent-visible file.

## The 18067 / 18345 / 18490 convergence was real, not manufactured

- On **June 19, 2023**, reviewing CASSANDRA-18345 (streaming SAI
  components), Caleb Rackliffe wrote: "Intending to review this, although
  it may make sense to wait to merge until CASSANDRA-18067 merges so we
  can test this w/ numeric indexes..." -- i.e. the team explicitly chose
  to hold 18345's *merge* until the numeric on-disk index (18067) was
  also ready, specifically so streaming could be exercised against both
  index types, not just the already-merged string index.
- On **June 20, 2023**, the same reviewer noted: "We have a couple
  outstanding failures around checksum validation, but we can hit those
  in CASSANDRA-18490" -- checksum-validation problems found while
  reviewing 18345 were explicitly deferred into 18490's own scope,
  confirming the two tickets were being tracked together in practice.
- CASSANDRA-18067 (numeric index) was committed to the `cep-7-sai` branch
  on **July 4, 2023**. CASSANDRA-18345 (streaming) had already been
  committed on **June 29, 2023** -- so in the end, 18345 merged *before*
  18067, not after; the "wait for 18067" plan from June 19 was
  apparently superseded once J17/J11 CI results came back clean for
  18345 on its own. CASSANDRA-18490 (checksumming) was committed on
  **July 11, 2023**, after both.
- This is a useful nuance for grading: the real-world resolution was
  parallel development with a *deliberated, then partially revised*
  merge-order decision -- not a strict "18067 must finish before 18345
  starts" gate. A fixture answer that names the convergence concern (SAI
  components across index types need streaming + checksumming to work
  together) should not be penalized for not predicting the exact
  eventual merge order, which even the reviewers themselves changed their
  minds about.

## CASSANDRA-18112 (CQL index hints) stayed blocked for years

- 18112 was not resolved until **August 1, 2025** -- over two years after
  this fixture's cutoff -- and only after several *later*-filed, more
  narrowly scoped tickets (CASSANDRA-20213, CASSANDRA-18782,
  CASSANDRA-20334, CASSANDRA-21715) were filed against it or split off
  from it. This corroborates the fixture's framing: the original,
  broadly-scoped request genuinely needed external design consensus
  before it could move, and that consensus took a long time to form.

## CASSANDRA-18216 (in-memory index sharding) never merged

- As of this writing, CASSANDRA-18216 is still in "Review In Progress"
  status -- it was never merged. This is a real example of a
  concretely-scoped, seemingly straightforward vertical improvement that
  simply stalled; it doesn't affect this fixture's grading (nothing
  depends on it), but it's a useful honesty check against assuming every
  filed, assigned ticket in a real backlog actually lands.

## The 5-phase plan didn't survive unchanged

- Phase 5 ("LIKE support"), placeholder-epic CASSANDRA-18493 at cutoff,
  was later restructured under a different, later epic
  (CASSANDRA-19224) with a substantially expanded set of child issues
  (CASSANDRA-19574, CASSANDRA-17198, CASSANDRA-19240, CASSANDRA-21063,
  and others) -- none of which existed at the chosen cutoff. This
  confirms the fixture's choice to exclude Phase 5 entirely from the
  task list was correct: it was genuinely undecided at cutoff, and its
  eventual shape bears little resemblance to the placeholder that existed
  in May 2023.

## Branch merge and release

- The `cep-7-sai` branch was merged to trunk on **July 26, 2023**
  (per Jira comments on CASSANDRA-16052).
- SAI shipped with fix versions **5.0-alpha1** and **5.0**. Apache
  Cassandra 5.0 reached general availability in **September 2024** (web
  search corroboration only, not independently verified against a
  primary Apache announcement in this session).
