# Actual PRs / commits

Verified from Jira comment threads (see `sources.md`); not independently
cross-checked against the GitHub PRs/commits themselves in this session
(no direct GitHub fetch was performed -- all PR/commit identifiers below
are as reported inside Jira comments).

| Issue | Scope | PR / commit | Merged |
|---|---|---|---|
| CASSANDRA-18058 | In-memory index and query path | commit `b43da004b07d4434f16dcfdcf7c8427f7f78ea78` (maedhroz fork) | ~2023-01-19 |
| CASSANDRA-18062 | On-disk string/literal index + query path | PR `github.com/maedhroz/cassandra/pull/9`; exact merge commit not captured | ~mid-April 2023 (comments run through 2023-04-13; issue resolved 2023-04-14) |
| CASSANDRA-18067 | On-disk numeric index | commit `de26b9089b7ae2d36452ad8e04a1d281cd127d26`, committed to `cep-7-sai` by Andres de la Peña | 2023-07-04 |
| CASSANDRA-18345 | Streaming SAI components as part of repair | commit `5d3f257477cba2d7f33f842dba4582d0660f5738`, committed to `cep-7-sai` by Caleb Rackliffe | 2023-06-29 |
| CASSANDRA-18490 | Checksum SAI components after streaming | referenced GitHub PR #2460; exact merge commit not captured ("Committing..." final comment) | ~2023-07-11 |
| `cep-7-sai` branch (created) | New official ASF-repo branch for the SAI feature work, mirroring Caleb Rackliffe's personal CASSANDRA-16052 branch | PR #2327 | branch created ~2023-05-11 |
| `cep-7-sai` branch (rebase pulling CEP-25 trie components) | Routine rebase | PR #2381 | ~2023-06-01 |
| `cep-7-sai` branch merged to trunk | Full feature integration | -- | 2023-07-26 |

## Not individually tracked down

Resolution *dates* for the remaining tickets (18112, 18165, 18166, 18167,
18216, 18280, 18479, 18494, 18515, 18521) were taken from Jira issue
metadata (a primary source, queried directly), which is reliable for
status/date. Specific PR numbers or commit hashes for these were **not**
individually looked up in this session -- only the five rows above (plus
the branch-level events) have a concrete PR/commit identifier attached.
Treat any PR-number-level claim about those ten tickets as not verified
here.
