# Sources

All accessed 2026-09-26.

## Jira (issues.apache.org/jira, project IGNITE)

- **IGNITE-24781** -- "IEP-119 Move common classes to ignite-commons"
  (Improvement, umbrella ticket for Phase 1 of IEP-119). Fetched via
  `/rest/api/2/issue/IGNITE-24781?fields=description` for the full,
  untruncated description (an earlier truncated fetch of this and other
  issues' descriptions was caught and corrected mid-task -- see the
  "correction" note below). Real created date 2025-03-12, resolved
  2026-01-12 (see "Jira status lag" below for why that resolution date is
  much later than the actual work).
- **The 21 real Sub-tasks of IGNITE-24781** were enumerated via
  `/rest/api/2/search?jql=parent = IGNITE-24781 ORDER BY created ASC`,
  which is the tracker's own formal parent-child field -- a stronger
  relationship than a shared label or epic link. This is the search that
  surfaced IGNITE-24851, IGNITE-24852, IGNITE-24946, and IGNITE-24958,
  none of which carry the `IEP-119` label and so were missed by an
  earlier label-only search pass (see `cutoff-rationale.md`).
- Of those 21, the twelve created on or before 2025-03-30 (the chosen
  cutoff) are: IGNITE-24782, IGNITE-24786, IGNITE-24792, IGNITE-24846,
  IGNITE-24847, IGNITE-24848, IGNITE-24850, IGNITE-24851, IGNITE-24852,
  IGNITE-24941, IGNITE-24946, IGNITE-24957, IGNITE-24958. Each was
  fetched individually via `/rest/api/2/issue/<key>?fields=summary,
  description,issuelinks,priority,created,resolutiondate,parent` for its
  full description text and any stated issue links. IGNITE-24786 is
  already resolved as of the cutoff (2025-03-28) and is treated as
  precedent, not a remaining task.
- **Correction made during this research:** an earlier pass fetched
  IGNITE-24957's description through a code path that truncated it at
  400 characters, and a first draft of `tasks.md` filled in the missing
  tail of point 4 with invented text ("throwable-handling logic, which
  several other utility classes... also depend on"). This was caught
  before being finalized, and the full untruncated description was
  re-fetched directly (`curl .../issue/IGNITE-24957?fields=description`)
  before `tasks.md` was written. The real text turned out to contain
  significant additional real content (the import list and the
  IGNITE-24851 cross-reference) that the invented placeholder text did
  not anticipate. Flagged here in case any other truncation slipped
  through unnoticed -- every description quoted in `tasks.md` was
  re-verified against a direct, untruncated `?fields=description` fetch
  before this file was finalized.
- The remaining nine Sub-tasks of IGNITE-24781 (IGNITE-25012 onward,
  created 2025-04-03 through 2025-06-14) were identified as existing but
  deliberately excluded, since they postdate the chosen cutoff.

## Jira status lag (a general caution, not specific to one issue)

Several issues in this set show their Jira "Resolved" date landing much
later than when a search of merged GitHub PRs shows the actual code
change merged (e.g. IGNITE-24782's PR merged 2025-03-26, but the ticket
wasn't marked Resolved until 2025-04-10; IGNITE-24850's own PR wasn't
even opened until 2025-07-14, four months after the ticket was filed, and
the ticket's Jira resolution date is 2026-01-12 -- nearly a year after
filing). This means a ticket's Jira status should not be read as a
precise proxy for when work actually happened. This did not affect the
agent-visible fixture (which only uses status *as of the 2025-03-30
cutoff*, confirmed independently per-issue), but is noted here as a
reason to be cautious about inferring timing from status.

## GitHub (apache/ignite)

- REST search API (`api.github.com/search/issues?q=repo:apache/ignite+type:pr+<key>+in:title`)
  for each Jira key above, to find the actual PR(s) implementing it, its
  open/close dates, and (via the PR title) what it actually covered.
  Rate-limited (unauthenticated) partway through; PRs for IGNITE-24851,
  IGNITE-24852, IGNITE-24957, and IGNITE-24958 specifically were not
  individually confirmed for this reason -- see `actual-prs.md` for what
  was and wasn't confirmed.
- Repository contents API for `modules/` and `modules/commons/` at
  commits close to 2025-03-06 and 2025-03-28, to confirm `modules/commons`
  did not exist in early March 2025 and did exist (as an empty skeleton:
  `pom.xml` + empty `src/main`) by March 28, 2025, two days before the
  chosen cutoff.
