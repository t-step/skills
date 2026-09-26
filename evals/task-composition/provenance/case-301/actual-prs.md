# Actual PRs

Confirmed via GitHub's search API (title containing the Jira key), before
being rate-limited partway through -- see `sources.md`.

| Jira key | PR | Title | Opened | Closed |
|---|---|---|---|---|
| IGNITE-24782 | [#11942](https://github.com/apache/ignite/pull/11942) | Initial commit for ignite-commons | 2025-03-12 | merged 2025-03-26 |
| IGNITE-24792 | [#11978](https://github.com/apache/ignite/pull/11978) | Move GridToStringBuilder to ignite-commons | 2025-04-02 | 2025-04-08 |
| IGNITE-24846 | [#11995](https://github.com/apache/ignite/pull/11995) | Move F to ignite-commons | 2025-04-12 | -- |
| IGNITE-24847 | [#11981](https://github.com/apache/ignite/pull/11981) | **Move some U methods, IgniteException, IgniteCheckedException to ignite-commons** | 2025-04-03 | 2025-04-07 |
| IGNITE-24848 | [#11985](https://github.com/apache/ignite/pull/11985) | Move GridTuple* to ignite-commons | 2025-04-08 | 2025-04-14 |
| IGNITE-24850 | [#12186](https://github.com/apache/ignite/pull/12186) | Split IgniteUtils to common and core specific methods | 2025-07-14 | -- |
| IGNITE-24941 | [#11976](https://github.com/apache/ignite/pull/11976) | Remove unused code from IgniteUtils | 2025-03-28 | 2025-04-09 |
| IGNITE-24946 | [#11975](https://github.com/apache/ignite/pull/11975) | Replace F.eq with the Objects.equals | 2025-03-28 | 2025-04-02 |
| IGNITE-24851 | not individually confirmed (rate-limited) | -- | -- | -- |
| IGNITE-24852 | not individually confirmed (rate-limited) | -- | -- | -- |
| IGNITE-24957 | not individually confirmed (rate-limited) | -- | -- | -- |
| IGNITE-24958 | not individually confirmed (rate-limited) | -- | -- | -- |

## What this shows

**PR #11981's title is the single most important historical fact here**:
the actual delivered PR for IGNITE-24847 ("Move U to ignite-commons")
bundled in IGNITE-24851 ("Move IgniteException...") and IGNITE-24852
("Move IgniteCheckedException...") as well -- three separate Jira Sub-
tasks, delivered as one real PR. This is exactly the kind of thing this
suite's real-world fixtures are meant to surface: the tracker's task
granularity and the actual delivery granularity are not the same thing.
It is **not** part of the agent-visible fixture (nothing in `tasks.md` or
`dependencies.md` states or implies this grouping) -- a response should
be free to group IGNITE-24847/24851/24852 together, separately, or any
other defensible way based on the fixture's own stated content, and
whichever choice it makes should not be graded against this historical
answer (see `../../grading/case-301.expected.md`, DIAGNOSTIC section).

**IGNITE-24850's PR wasn't opened until 2025-07-14** -- over three months
after the ticket was filed (2025-03-19), and roughly four months after
this fixture's 2025-03-30 cutoff. No code work had visibly started on it
by the cutoff, consistent with it being genuinely blocked on IGNITE-24846
and IGNITE-24848 (whose own PRs opened 2025-04-08 and 2025-04-12,
closing 2025-04-14 and unknown respectively).
