# Sources — case-303 (Hudi Metadata Table)

All accessed 2026-09-26. Apache Jira and GitHub are public; no auth used
(anonymous REST access to `issues.apache.org/jira/rest/api/2/...` and
`api.github.com/repos/apache/hudi/...` worked directly).

## Jira

- `https://issues.apache.org/jira/rest/api/2/issue/HUDI-<id>?expand=changelog`
  (all 19 tickets, fetched during an independent review pass, also
  2026-09-26) — used to check every ticket's description-edit history
  against the 2021-09-21 cutoff. Findings and the fixture fixes made as a
  result are recorded in `cutoff-rationale.md`'s "Post-hoc changelog
  verification" section; the headline result is that HUDI-2475's entire
  design write-up and part of HUDI-2458's did not exist at cutoff and had
  to be trimmed back to what was actually filed by then.
- `https://issues.apache.org/jira/browse/HUDI-1292` — the RFC-15 umbrella
  epic. Confirmed: created 2020-09-23, closed 2022-07-05, fix version
  0.11.0, reporter Vinoth Chandar. Told me this epic's *formal* Jira
  parent-child links only list 8 direct children (HUDI-1592, 2017, 1717,
  2013, 2016, 842, 1256, 1312) — far fewer than the issues actually
  associated with the metadata-table effort via the "Epic Link" field.
- `https://issues.apache.org/jira/rest/api/2/search?jql=parent=HUDI-1292 OR "Epic Link"=HUDI-1292` —
  returned 205 total issues spanning 2020-06 through 2024-10, confirming
  the metadata-table initiative is a multi-year, still-partially-active
  effort, not a bounded project — this is what forced picking a bounded
  window rather than using "everything linked to the epic."
- `https://issues.apache.org/jira/rest/api/2/search?jql=key in (HUDI-2276,...)` —
  full field fetch (description, status, created, priority, fixVersions,
  issuelinks) for the 19 tickets used in this fixture, plus HUDI-2567,
  2573, 2585, 2595, 3066, 3208 (used only for historical-outcome.md,
  below, not the fixture itself). All descriptions and field values in
  this provenance and in the fixture are taken verbatim or paraphrased
  directly from this data.
- `https://issues.apache.org/jira/rest/api/2/project/HUDI/versions` —
  confirmed release dates: 0.7.0 (2021-01-25), 0.8.0 (2021-04-06), 0.9.0
  (2021-08-26), 0.10.0 (2021-12-08), 0.11.0 (2022-04-30). Used to place
  the cutoff relative to the actual release cadence.

## GitHub (apache/hudi)

- `api.github.com/repos/apache/hudi/pulls/3411` — PR for HUDI-2276,
  opened 2021-08-05, never merged (superseded by later work). Confirmed
  the description text used in HUDI-2276.
- `api.github.com/repos/apache/hudi/pulls/3651` — PR for HUDI-2422
  ("Adding rollback plan and rollback requested instant"), merged
  2021-09-16. File list confirmed the rollback-plan mechanism described
  in the ticket (new `HoodieRollbackPlan.avsc`,
  `BaseRollbackPlanActionExecutor.java`, etc.) — used only to sanity-check
  the ticket's own prose, not quoted into the fixture as a file list.
- `api.github.com/repos/apache/hudi/pulls/3590` — PR titled
  "[HUDI-2285][HUDI-2476] Metadata table synchronous design. Rebased and
  Squashed from pull/3426", merged 2021-10-06. This is the concrete
  evidence that HUDI-2285 and HUDI-2476 actually landed together in one
  PR historically — used in historical-outcome.md and the grading key's
  diagnostic section, and it's what grounded the dependencies.md flag
  that 2476 might not be independently verifiable from 2285.
- `api.github.com/repos/apache/hudi/pulls/3843` (HUDI-2468, merged
  2021-10-23), `4518` (HUDI-2477, merged 2022-01-10), `4605` (HUDI-2432,
  merged 2022-02-10), `3678` (HUDI-2444, merged 2021-09-20), `3695`
  (HUDI-2395, merged 2021-09-23), `3698` (HUDI-2474, merged 2021-09-28) —
  used for actual-prs.md and to confirm real shared-file overlap
  (`HoodieTable.java`, `BaseRollbackActionExecutor.java`,
  `BaseRestoreActionExecutor.java`,
  `HoodieBackedTableMetadataWriter.java` all appear in more than one of
  these PRs' diffs). This overlap evidence is NOT stated in the
  agent-visible fixture as file names, because most of these PRs merged
  well after the chosen cutoff and would be hindsight; it only supports
  the "shared-area signal" language in `dependencies.md`, which is phrased
  in terms of what the tickets' own text describes, not the PR diffs.

## RFC / docs

- `https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=147427331` —
  RFC-15 text (via WebFetch summary). Confirmed the `.hoodie/metadata`
  location, MOR-table design, and the original stated ambition to also
  eventually support column-indexed queries — used for `context.md`'s
  framing paragraph.

## Web search (general orientation only, not directly quoted)

- Searches for "HUDI-1292", "hoodie.metadata.enable default", "bloom
  filter index column stats jira", "concurrent writers metadata table
  lock jira" — used to orient on the overall multi-year shape of the
  initiative (multi-modal indexing landed in 0.11.0; defaulting had
  further trouble even after 0.10.0) before narrowing to the bounded
  window actually used in the fixture. None of this later material is in
  the agent-visible fixture.
