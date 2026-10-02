# Cutoff rationale

## Chosen cutoff: 2023-05-15

## Why this point

- Phases 1 and 2 of the stated 5-phase SAI plan (index-group interface +
  memtable indexing; on-disk string/literal index) had already merged to
  the feature branch, so there is real, settled repository state to
  reason from -- this isn't "day one" of the effort.
- Phase 3 (the on-disk numeric index, CASSANDRA-18067) had been in
  progress for nearly six months and was still unresolved for almost two
  more months after this cutoff (it merged 2023-07-04) -- so at this
  point, its scope is known and described, but its completion, and
  everything downstream of it, is genuinely still open. This is exactly
  the "how do I split what's left" moment the fixture needs: a bounded,
  real set of described tasks whose eventual grouping into PRs and
  integration order was not yet decided.
- The most recently filed ticket in the chosen window, CASSANDRA-18521,
  was filed **2023-05-11**, four days before the cutoff; the most recent
  branch-management event (creation of the official `cep-7-sai` branch)
  is also dated **2023-05-11**. The cutoff sits in a natural quiet window
  before the next filing burst (CASSANDRA-18615 in June 2023, plus two
  bug reports in July 2023), so no ticket is awkwardly split mid-filing.
- CASSANDRA-18217 (multiple-index CQL queries without `ALLOW FILTERING`)
  resolved 2023-05-12, three days before the cutoff -- treated as
  already-landed repository state (see `repository-state.md`), not as a
  remaining task, which is accurate for a 2023-05-15 snapshot.
- The task set naturally contains both of the dynamics the fixture is
  meant to pressure-test: an externally-blocked task with no path to
  resolution inside the task set (CASSANDRA-18112, blocked on a community
  DISCUSS thread) and a task whose fix reaches into shared, non-SAI-owned
  storage-engine machinery (CASSANDRA-18345, touching the SSTable
  streamed-component set) -- both grounded in the tickets' own filed
  text, not invented for the fixture.

## Honest uncertainty for the next reviewer

- **CASSANDRA-18494's title/version target.** The current, present-day
  Jira title for this issue includes a specific target version
  ("...to lucene-core 9.7.0"). I could not verify from the description
  text alone whether that specific version number was already decided at
  filing time (May 2, 2023) or was added/edited into the title later as
  the actual target firmed up during implementation. To avoid a possible
  hindsight leak, I deliberately used a generic title/description
  ("upgrade the vendored lucene-core dependency... to whatever the
  current latest stable version is") grounded only in the description
  body, which does *not* name a version. This is a conservative choice,
  but I'm not fully certain it was necessary -- it's possible the
  original title already said 9.7.0 at filing time, in which case I've
  been more conservative than strictly required, not less.

  **[Resolved by independent review audit, 2026-09-26]** Checked the
  issue's changelog directly: the title was "Upgrade lucene-core library
  to the latest stable version" from filing until it was edited to
  "Upgrade to lucene-core 9.7.0" on 2023-06-28 -- over a month after this
  fixture's 2023-05-15 cutoff. The generic title used in `tasks.md` was
  correct, not overly conservative.

- **CASSANDRA-18490's description.** The version of this issue's
  description I fetched included a trailing sentence noting that
  "ultimately three changes were implemented" (naming a specific internal
  class). That sentence is clearly a later edit describing the eventual
  outcome, not the issue as originally filed. I excluded it and kept only
  the problem-statement portion for `tasks.md`. I'm confident this
  specific exclusion was correct, but it's a reminder that Jira
  descriptions can be edited after the fact, and I did not independently
  verify (e.g. via edit history) that no *other* description text I used
  elsewhere was similarly touched up post-cutoff.

  **[Resolved by independent review audit, 2026-09-26]** The description
  "EDIT: ..." sentence was indeed added 2023-07-11 (post-cutoff),
  confirming the exclusion was correct. However, the audit found a
  *title* leak this section didn't check for: CASSANDRA-18490's Jira
  title changed four times, and the title used as this task's heading in
  `tasks.md` ("Checksum per-SSTable and per-column SAI components after
  streaming") was not set until 2023-07-11 -- the final, post-merge
  title. The title that actually existed at the 2023-05-15 cutoff was
  "Add checksum validation to all index components on startup, full
  rebuild and streaming" (set 2023-05-02, unchanged until 2023-07-05).
  `tasks.md` has been corrected to use the cutoff-accurate title. The
  same class of leak was found and fixed on CASSANDRA-18112: its title
  in `tasks.md` was the present-day title ("Support manual secondary
  index selection at the CQL level"), set 2025-01-15 -- over 2.5 years
  post-cutoff -- replacing the original filing title, "Add the feature of
  INDEX HINT for CQL," which is what existed at cutoff and is now used in
  `tasks.md`. Lesson: checking a description's edit history is not
  sufficient; a ticket's *title* field has its own independent edit
  history and needs the same check.

  A third leak was found in CASSANDRA-18216's description: the sentence
  "Notes an existing prior implementation in a downstream (DataStax)
  fork" in `tasks.md` was sourced from a description edit made
  2025-07-17 (over 2 years post-cutoff, and even post-dating this
  fixture's original authoring) that appended a DataStax fork PR link to
  the original description. This sentence has been removed from
  `tasks.md`; the description as it existed at cutoff said nothing about
  a prior downstream implementation.

  Other tickets' changelogs were also checked (18067, 18165, 18166,
  18167, 18280, 18345, 18479, 18494, 18515, 18521): 18345 had one
  description edit, but it was 2023-04-24 (before cutoff, filling in
  what had been a "TBD" placeholder) and is what `tasks.md` already
  reflects; 18515 had one description edit on 2023-05-10 (also before
  cutoff); the rest had no title or description edits at all. No further
  leaks were found in this pass, but coverage of comment threads (as
  opposed to the description/summary fields checked here) for tickets
  other than 18067/18345/18490 was not exhaustively re-checked.

- **Status labels used in tasks.md are current-day statuses**, not
  necessarily the exact status label that would have shown at the
  2023-05-15 cutoff (e.g. CASSANDRA-18167 is "Triage Needed" and
  CASSANDRA-18216 is "Review In Progress" as of today, 2026-09-26). The
  underlying facts I actually relied on for fixture content -- assignee
  (or lack of one), and the description text itself -- are stable
  historical facts from issue creation, not live status, so I believe
  this is low-risk, but I did not check each ticket's status-change
  history to confirm the state at the exact cutoff date.
- **Coverage of the task set is not exhaustive.** The 13 tasks in
  `tasks.md` were assembled from two JQL-windowed searches (`"Epic
  Link"=CASSANDRA-16052`, and `component="Feature/SAI"` within two
  overlapping creation-date windows). It's possible a small number of
  additional SAI-relevant tickets existed at the cutoff that weren't
  tagged with the `Feature/SAI` component or linked via Epic Link at the
  time (e.g. filed under a more generic component and re-tagged later),
  and so weren't surfaced by these searches.
- **The "shared vendored lucene-core" and "shared RAMIndexOutput"
  dependencies in `dependencies.md` are inferences I constructed** by
  combining two independently-filed tickets' text (plus, for the Lucene
  case, the CEP-7 design doc's architecture section) -- neither pair of
  tickets cross-references the other. I graded these as ambiguous/
  worth-checking rather than required dependencies for exactly this
  reason; a reviewer should confirm that framing doesn't overstate what
  the record actually supports.
