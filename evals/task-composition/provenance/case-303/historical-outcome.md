# Historical outcome — case-303 (Hudi Metadata Table)

This is what actually happened after the chosen cutoff (2021-09-21). None
of this is in the agent-visible fixture; it's here so a grader can judge
whether a proposed slice plan's *reasoning* holds up, without treating this
sequence as the one correct answer the skill under test needed to
reproduce (per the task-composition eval convention: historical execution
is evidence, not an oracle).

## What actually happened, in order

1. **The correctness-bug cluster mostly landed through 0.10.0.** Most of
   the rollback/restore/bootstrap tickets in the fixture (HUDI-2422, 2432,
   2436, 2444, 2468, 2474, 2476, 2477, 2478) resolved with fix version
   0.10.0 or 0.11.0. HUDI-2285 (the synchronous design) and HUDI-2476 (the
   retried-compaction bug) were **actually implemented and merged together
   in one PR** (#3590, "[HUDI-2285][HUDI-2476] ... Rebased and Squashed
   from pull/3426", merged 2021-10-06) — confirming the ambiguity flagged
   in `dependencies.md` (whether 2476 is independent of 2285) resolved, in
   practice, toward "not independent, part of the same change."
2. **A genuine multi-writer concurrency bug was found shortly after the
   cutoff, not before it.** HUDI-2573 ("Deadlock w/ multi writer due to
   double locking"), filed 2021-10-18 — about four weeks after this
   fixture's cutoff — describes exactly the kind of concurrency defect the
   eval design brief was looking for: the synchronous metadata patch
   added locking for cleaning and rollback, and there turned out to be
   code paths that acquire the lock twice (e.g. a commit's post-commit
   hook triggers cleaning, which tries to acquire the same lock again),
   causing a hang. This bug did **not** exist as filed knowledge at the
   chosen cutoff — it was discovered afterward, during exactly the kind of
   verification work HUDI-2567 ("Verify synchronous metadata patch w/
   multi writers end to end," filed 2021-10-17, one day earlier) was
   doing. This is real evidence for the "bug found during rollout/
   verification of an earlier piece" dynamic the eval design brief asked
   for — it just sits one release-cycle-fraction *after* this fixture's
   window, not inside it, which is why it's provenance rather than a
   fixture task. A cutoff placed a few weeks later could have included it
   as an open task instead; this cutoff was chosen so the fixture
   represents genuine mid-flight state rather than a moment right before
   a single dramatic discovery.
3. **The RFC itself was rewritten mid-implementation.** HUDI-2585
   ("Re-write RFC for file listing w/ synchronous metadata patch"), filed
   2021-10-20, confirms the original RFC-15 document was revised to match
   the synchronous design after implementation had already substantially
   started — direct evidence the plan's own decomposition evolved during
   execution, not just its task list.
4. **0.10.0 shipped 2021-12-08**, apparently with metadata table enabled
   by default per the original HUDI-2276 goal.
5. **A real production regression surfaced during the 0.10.0 rollout.**
   HUDI-3066 ("Very slow file listing after enabling metadata for existing
   tables in 0.10.0 release"), filed 2021-12-19 — eleven days after 0.10.0
   shipped — reports that turning on metadata table for an *existing*
   (already-large) table made file listing significantly *slower*, not
   faster, especially on the read side. This is the clearest "bug
   discovered while rollout/verification of an earlier piece was
   underway" instance found in the whole research pass for this case, and
   it happened in production after release, not during pre-release
   testing.
6. **Defaulting had to be re-planned for the next release, not treated as
   done.** HUDI-3208 ("Come up with rollout plan for enabling metadata
   table by default in 0.11"), filed 2022-01-11 — about a month after
   0.10.0 shipped and three weeks after the HUDI-3066 regression was
   reported — lays out a much more cautious plan (throw errors if no lock
   provider is configured; never risk silently corrupting a user's table;
   get community feedback; test more) before attempting the default-on
   flip again for 0.11.0. In other words, the 0.10.0 "enable by default"
   effort did not cleanly succeed on the first attempt; defaulting was
   effectively redone a full release cycle later with a more conservative
   process. HUDI-1292 (the umbrella epic) wasn't formally closed until
   2022-07-05, well after 0.11.0 (2022-04-30).
7. **Multi-modal indexing (bloom filter, column stats — RFC-27/RFC-37)
   landed later still**, folded into the same HUDI-1292 umbrella around
   0.11.0. This is the "core capability" work (record-level/column
   indexes) that HUDI-2285's own description names as its eventual
   motivation — it is explicitly *not* represented as tasks in this
   fixture, because none of it had been filed as concrete, described
   tickets by the chosen cutoff; it's future work relative to this window,
   consistent with not inventing what the record didn't yet support at
   that point.

## What this means for grading

The historical shape — correctness bugs first, a concurrency bug found in
verification right after this window, an RFC rewrite, a rollout that
didn't succeed cleanly on the first try, and a formal re-plan a release
cycle later — is offered as background, not as a required grouping. A
plan-under-test that reaches a *different* defensible slice boundary
(e.g. treating HUDI-2285+2476 as two separately-scoped items because the
record doesn't force them together) should not be penalized just because
history happened to land them as one PR.
