# Source notes

This case set is built from real Apache Ignite Jira issues (project key
`IGNITE`), as they existed as of the stated cutoff. Every task ID above
is a real issue key, formally filed as a Jira Sub-task of IGNITE-24781
(confirmed via the tracker's own `parent` field, not just a shared label
or epic link).

## Where this task set came from

IGNITE-24781 ("Move common classes to ignite-commons") is the umbrella
ticket for Phase 1 of a longer-running internal effort tracked under the
label `IEP-119`. As of this cutoff it has 12 Sub-tasks filed; this task
set is exactly those 12, plus the umbrella ticket itself. One additional
Sub-task, IGNITE-24786 ("Clean up GridFunc"), already exists under the
same umbrella but is already resolved as of this cutoff -- it is treated
as settled precedent, not remaining work (see `repository-state.md`),
consistent with how a task a plan lists that's already done should be
handled.

Further Sub-tasks of IGNITE-24781 exist in the tracker today but were
filed after this cutoff -- they are not part of this task set and are not
referenced here, since they weren't yet knowable at this point. This
umbrella ticket should not be assumed closed out by the twelve tasks
listed here.

## Stated priority

Every issue in this set carries Jira's default "Major" priority. Nothing
states a priority or ordering of one task over another within this set.

## Repository state

See `repository-state.md`.
