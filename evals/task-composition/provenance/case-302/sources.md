# Sources (all accessed 2026-09-26)

## Primary Jira sources

- https://issues.apache.org/jira/browse/CASSANDRA-16052 -- umbrella epic
  ("CEP-7 Storage Attached Indexes (Phase 1)"). Status/resolution,
  fix versions (5.0-alpha1, 5.0), linked issues (blocks CASSANDRA-18473
  Phase 2; depends on CASSANDRA-6936 and CASSANDRA-17034; blocked by
  CASSANDRA-17973), team (Zhao Yang reporter; Caleb Rackliffe, Andres de
  la Peña, Mike Adamson, Piotr Kolaczkowski as authors/reviewers).
- https://issues.apache.org/jira/rest/api/2/issue/CASSANDRA-16052/comment
  -- full comment history on the epic. Source of: the Nov 16, 2022
  five-phase delivery plan (quoted in `context.md`/`source-notes.md`);
  the Jan 19, 2023 "phase 1 merged... next up CASSANDRA-18062" note; the
  Mar 18, 2023 rebase note about SSTable format API changes forcing
  `SSTableFlushObserver` capability removal; the Apr 13, 2023 rebase/test
  notes; the May 11, 2023 note about creating the `cep-7-sai` branch.
  Comments dated Jun 1, 2023 onward were read but excluded from
  agent-visible files as postdating the chosen cutoff.
- REST API searches against `issues.apache.org/jira/rest/api/2/search`
  with JQL `"Epic Link"=CASSANDRA-16052` and, separately,
  `component="Feature/SAI" AND created>=... AND created<=...` for the
  windows Aug 2022-Jan 2023 and Feb 2023-May 15 2023 -- used to enumerate
  candidate tasks and their creation/resolution dates. This is how the
  13-task list in `tasks.md` was assembled.
- Individual issue fetches (via the same REST endpoint, `fields=summary,
  description,status,created,resolutiondate,issuelinks,priority,
  assignee`) for: CASSANDRA-18058, 18062 (comments), 18067 (+comments),
  18112, 18165, 18166, 18167, 18216, 18217, 18280, 18345 (+comments),
  18479, 18490 (+comments), 18493, 18494, 18515, 18521, 16092 (via the
  16052 fetch), 6936, 17034, 17056, 17973 -- used for descriptions,
  dates, assignees, and stated links.

## CEP-7 design document

- https://cwiki.apache.org/confluence/display/CASSANDRA/CEP-7%3A+Storage+Attached+Index
  -- the adopted CEP-7 proposal. Source of: the numbered "Implementation
  Phases" (step 1-5), the architecture notes (numeric index built on a
  "modified one-dimensional block kd-tree from Lucene," text index as a
  trie-based inverted index), and the two named architectural challenges
  (compaction-strategy dependency, distributed-query overhead). Note:
  this page's *current* rendering shows "Status: Adopted, Released:
  5.0.0" -- that status banner reflects today's page state (added well
  after the chosen cutoff) and was excluded from all agent-visible files;
  only the technical/architecture content was used, cross-checked against
  the dated Jira comments above.

## GitHub / commit references (via Jira comments, not fetched directly)

- Feature-branch and PR references surfaced inside the Jira comment
  threads above: `github.com/maedhroz/cassandra` (Caleb Rackliffe's
  personal CASSANDRA-16052 branch/fork), `github.com/apache/cassandra`
  `cep-7-sai` branch (created ~May 11, 2023), PR references #2327, #2381,
  #2460, and commit hashes for CASSANDRA-18058
  (`b43da004b07d4434f16dcfdcf7c8427f7f78ea78`), CASSANDRA-18067
  (`de26b9089b7ae2d36452ad8e04a1d281cd127d26`), and CASSANDRA-18345
  (`5d3f257477cba2d7f33f842dba4582d0660f5738`). Used only for
  `actual-prs.md` / `historical-outcome.md` (post-cutoff outcome data),
  never for agent-visible files.

## Web search (general, for corroboration only)

- Search: "CEP-7 Storage Attached Indexes Cassandra Confluence
  CASSANDRA-16052" -- corroborated the CEP-7/16052 relationship and
  general SAI description; used only as a cross-check, not as a primary
  source for any fixture detail.
- Search: "Cassandra 5.0-alpha1 release date announcement SAI Storage
  Attached Indexes" -- used only for `historical-outcome.md` (5.0 GA
  ~September 2024). One claim from this search ("SAI initially available
  in experimental form in Cassandra 4.x") directly conflicts with two
  primary sources (the epic's fix-versions field, which lists only
  5.0-alpha1/5.0, and an explicit Feb 21, 2023 review comment on
  CASSANDRA-18062 stating the feature "will not land in any 4.x
  release") and was treated as unreliable and excluded from every file
  in this case, agent-visible or provenance.
