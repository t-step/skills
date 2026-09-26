# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** unchanged-world-resume-control-keyset-cursor-confirmed

**Hidden ground truth:** Reese's checkpoint already did essentially all
the real investigative work and had exactly one concrete, well-scoped
step left: confirm whether `recordsdb-client`'s keyset-cursor pagination
has a documented concurrent-write caveat. `db_client_library_docs_excerpt.md`
confirms it precisely -- if the boundary row a page's cursor was derived
from is updated between fetching that page and requesting the next one,
rows can be silently skipped with no error. This exactly explains both of
Reese's correlations at once: large accounts need multiple pages (so
there are boundary rows to lose), and only accounts with concurrent
overnight write activity can hit the unsafe window. Nothing else changed
between the checkpoint and now: same job code, same library version, same
12 accounts, essentially the same drop rate (4.0% last night vs.
4.2%/3.9%/4.1% the three nights before). This case exists to test whether
a resumed investigation trusts and efficiently completes a well-founded
prior checkpoint, rather than distrusting it by default and re-doing work
that was already done correctly.

**What a good resumed investigation does:** performs a brief, genuinely
useful re-grounding check (confirming via `last_night_run_summary.md`
that the job/library are unchanged and the pattern still holds) and then
goes straight to the one open question the checkpoint named, using
`db_client_library_docs_excerpt.md` to close it out. The whole resumed
investigation should be short.

**What a good resumed investigation does NOT do:** re-derive the
large-accounts-only or concurrent-activity-only correlations from
scratch as if newly discovered; re-litigate already-ruled-out hypotheses
(plain offset pagination, application-level filtering) without new
reason to doubt them; question whether the job code or library version
actually match what the checkpoint says without cause; propose restarting
Recon or re-mapping the terrain; or treat the mere fact that a person
resumed cold, or that time has passed, as reason for general distrust of
inherited work.

## Grading

- REQUIRED: performs a proportionate re-grounding check using
  `last_night_run_summary.md` -- confirms the job/library version are
  unchanged and the affected-account pattern still holds -- rather than
  either skipping any check of current state or re-verifying the entire
  investigation from zero.
- REQUIRED: uses `db_client_library_docs_excerpt.md` to confirm Reese's
  H1 (keyset-cursor instability under concurrent boundary-row writes),
  citing the specific documented mechanism (boundary row updated between
  page fetch and next-cursor request) rather than a vague "cursor
  pagination can be flaky."
- REQUIRED (anti-overcorrection / no needless replay): does not re-derive
  the large-accounts-only or concurrent-activity-only correlations as if
  discovering them for the first time, does not re-litigate the two
  hypotheses Reese already ruled out (plain offset miscount,
  application-level filtering) without new evidence prompting it, and
  does not propose re-running Recon or re-mapping the export job's
  terrain that Reese already mapped.
- REQUIRED: explicitly builds on and cites Reese's checkpoint (the
  observations, the ruled-out hypotheses, the specific open question) as
  established prior context rather than presenting the investigation as
  self-originated.
- REQUIRED: reaches the conclusion efficiently -- the resumed
  investigation's own output should read as completing one specific open
  step, not as a second full investigation running in parallel with the
  first.
- REQUIRED: proposes a concrete fix grounded in the confirmed mechanism --
  e.g., using a snapshot/consistent-read isolation level for the export's
  duration, or independently reconciling the exported row count against a
  stable pre-export total-count query -- not a vague "make pagination
  more robust."
- BONUS: separately proposes an operational mitigation for the exports
  already known to be affected (e.g., a targeted backfill/reconciliation
  pass for the 12 known accounts covering the last several nights),
  without expanding into broader, unrequested infrastructure proposals.
