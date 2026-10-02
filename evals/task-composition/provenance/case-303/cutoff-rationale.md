# Cutoff rationale — case-303 (Hudi Metadata Table)

## Chosen cutoff

**2021-09-21** (end of day). Every task in the fixture was filed on or
before this date; every task filed after it (HUDI-2494, HUDI-2537,
HUDI-2554, HUDI-2567, HUDI-2573, HUDI-2585, HUDI-2591, HUDI-2593, HUDI-2595,
HUDI-2606, HUDI-2634, HUDI-2639/2640, HUDI-2655, HUDI-2666/2667, HUDI-2712,
HUDI-2717, HUDI-2741, HUDI-2743/2744, HUDI-2747, HUDI-2763, HUDI-2792,
HUDI-2893, HUDI-2925, HUDI-2952, HUDI-2961, HUDI-3012, HUDI-3066, HUDI-3208,
and everything from the 0.11.0+ multi-modal-indexing era onward) is
excluded from the fixture and treated purely as provenance.

## Why this point is defensible

1. **The epic itself is far too broad to use wholesale.** A JQL query for
   everything linked to HUDI-1292's epic field returns 205 issues spanning
   2020-06 through 2024-10 — file-listing (2020-2021), synchronous redesign
   and default-on (2021), multi-modal indexing / bloom filter / column
   stats (2021-2022), and ongoing hardening (2023-2024). Using "the whole
   epic" would not be a bounded plan an engineer was ever actually looking
   at on one day; it would be the entire multi-year program in hindsight.
   A real bounded window has to be chosen instead, per the task brief.
2. **2021-08-05 through 2021-09-21 is a real, dense, self-contained burst.**
   Nineteen tasks were filed in this 48-day span, with a visible
   concentration on 2021-09-20/21 (nine tasks filed across those two days
   alone) — reading as a real triage/investigation push, not an evenly
   spread backlog. That density is exactly the "enough subtasks to need
   real slicing" bar the brief asks for, without reaching into a different
   phase of the initiative to pad the count.
3. **The cutoff sits before the answer was known, on multiple fronts that
   were genuinely live at the time:**
   - Whether the "enable by default" goal would make it into the *current*
     release had already failed once (0.9.0 shipped 2021-08-26, five days
     into this window, without it) — the team is mid-recovery, not at a
     clean starting line.
   - The synchronous redesign (HUDI-2285) was proposed but its
     implementation had not landed (it and HUDI-2476 merged together on
     2021-10-06, two weeks after this cutoff).
   - The rollout/upgrade story (HUDI-2475) is filed as an explicitly
     unresolved question ("Still working through whether this is really
     the only option" is how the ticket itself ends).
   - Two of the ops-track tasks (HUDI-2459, HUDI-2460) never actually
     resolved for years — genuinely open-ended work, not something this
     cutoff is artificially interrupting mid-completion.
   - The sharper concurrency bug (HUDI-2573, double-locking deadlock) and
     the production regression (HUDI-3066, slow listing after enabling on
     existing tables) had not yet been discovered — they surface 4 weeks
     and 3 months after this cutoff, respectively.
4. **A later cutoff (e.g. through 2021-10-27) would add real benchmarking/
   verification and sharper concurrency tasks** (HUDI-2567 "verify
   synchronous metadata patch w/ multi writers end to end," HUDI-2573 the
   deadlock bug, HUDI-2585 the RFC rewrite, HUDI-2634/2639/2640 bootstrap
   performance/certification) at the cost of roughly doubling the task
   count and pulling in a second, less tightly-bunched filing burst
   (2021-10-17 through 2021-10-27). That was considered and rejected for
   this fixture: it would have made "benchmarking/verification" and a
   filed, in-window concurrency bug stronger, but at the cost of a task
   list large enough to stop being one coherent, readable plan, and it
   would put the fixture right before HUDI-2573, which is a sharper and
   more tempting "just barely missed it" cutoff than is comfortable to
   claim confidently was not itself known informally inside the team by
   then (no evidence either way — erring toward the earlier, safer cutoff).

## Which target dynamics this cutoff does and does not support

Stated honestly, not massaged to claim more than the record shows — see
the final report for the full breakdown. In short: core capability
(re-architecture), ops/scale (compaction, cleaning), enablement/defaulting,
and a bug found during rollout are all solidly represented inside this
window. Concurrency is present only as the *async-compaction/cleaning*
angle (HUDI-2459, HUDI-2460), not as an explicit locking/deadlock bug —
that bug (HUDI-2573) exists but postdates the cutoff by four weeks, so it's
provenance only, not a fixture task. Benchmarking/verification-as-its-own-
activity is weak in this window (HUDI-2395's test cleanup is the closest
fit); the more explicit verification tasks (HUDI-2567, HUDI-2634,
HUDI-2639/2640) also postdate the cutoff.

## Post-hoc changelog verification (added during independent review)

A later review pass fetched the Jira changelog
(`.../rest/api/2/issue/HUDI-<id>?expand=changelog`) for every one of the
19 tickets to check the concerns below directly instead of leaving them
as flagged risk. Findings, and the fixes applied as a result:

- **HUDI-2472**: confirmed a running checklist, but the parts kept in the
  fixture (module-by-module pass-status list, HUDI-2468 cross-references)
  were already present in the description as of the ticket's last edit
  on 2021-09-21 (22:11 UTC) — safe. One inaccuracy was found and fixed:
  the fixture had called the failing deltastreamer test a
  "continuous-mode" test. That detail is not in the ticket as of cutoff
  (which only says "one test in deltastreamer," no elaboration) and is
  contradicted by the detail added the *next day* (2021-09-22), which
  describes the failure as archival/cleaning-related, not continuous-mode
  — "continuous-mode" appears to have been carried over by mistake from
  HUDI-2474's own (unrelated, unedited, safely-cutoff) description.
  `tasks.md` has been corrected to drop that detail.
- **HUDI-2475**: this is the one substantive finding. As filed on
  2021-09-21, the ticket had *only its title* ("Upgrade downgrade infra
  for enabling metadata") — zero body text. The entire design write-up
  quoted in the previous draft of this fixture (the numbered upgrade
  sequence, "this is the only viable option" framing, "confirm the first
  commit completes before restarting other processes") was added on
  2021-09-24 and refined again on 2021-09-26 — three to five days *after*
  this fixture's cutoff. That was genuine hindsight leakage: `tasks.md`
  and `dependencies.md` have been corrected to describe HUDI-2475 as a
  title-only placeholder as of the cutoff, with none of the invented
  design reasoning.
- **HUDI-2458, HUDI-2459, HUDI-2460**: HUDI-2459 and HUDI-2460 have zero
  description edits ever recorded — their fixture text is safe as
  written. HUDI-2458 does have edits, and the check found a real problem:
  the "3 inter-linked nuances" / "spurious deletes" proposal was added on
  2021-11-29, over two months after this fixture's cutoff. As filed on
  2021-09-20, the ticket was only the short problem statement
  ("compaction is fenced on in-flight data-table requests... liveness
  problem... need to relax this constraint"), with no proposed mechanism
  and no mention of rollback/archival also being fenced by the same
  instant. `tasks.md`'s HUDI-2458 entry and `dependencies.md`'s
  HUDI-2458/2459 bullet have been corrected to drop the "spurious
  deletes" proposal and the rollback/archival fencing detail.
- **HUDI-2432 / HUDI-2477 date error (unrelated to changelog editing, but
  found during the same pass):** the original draft of `dependencies.md`
  and the grading key both asserted HUDI-2432 and HUDI-2477 were "filed
  the same day (2021-09-21)." Jira's `created` field shows HUDI-2432 was
  actually filed 2021-09-14 — a full week before HUDI-2477
  (2021-09-21). This was a factual error, not a hindsight leak, but it
  fed a REQUIRED grading item, so it has been corrected in both
  `dependencies.md` and `grading/case-303.expected.md` (REQUIRED #3) to
  state the real dates and to explicitly guard against inferring
  execution order from filing/ticket-number order — which, if anything,
  makes that grading item sharper (it now also catches a
  numeric/filing-order illusion, not just a same-day coin-flip).
- All other tickets in the fixture (HUDI-2276, 2285, 2303, 2395, 2422,
  2432, 2436, 2444, 2452, 2468, 2474, 2476, 2477, 2478) either have zero
  description edits or have every edit dated on/before the cutoff, so
  their fixture text was not at risk of this class of leak.
- **The dependency and "shared-area" claims in `dependencies.md`** were
  written to only use language and mechanism names that appear in the
  tickets' own descriptions (not from reading the later-merged PRs' file
  diffs, which are hindsight relative to this cutoff) — but the choice of
  *which* overlaps were worth flagging was informed by having already seen
  the PR file lists (see `actual-prs.md`). That's a one-way influence
  worth naming: nothing false was added, but the selection of which real,
  textually-grounded overlaps to highlight was not blind to the outcome.
