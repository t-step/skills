# Historical outcome

## What actually happened

Real code work on this task set started almost immediately for some
tasks and lagged for months on others. IGNITE-24782 (create the
`ignite-commons` module) merged within two weeks of being filed
(2025-03-26). IGNITE-24941 (remove unused code from `IgniteUtils`) and
IGNITE-24946 (replace `F.eq` with `Objects.equals`) both had PRs opened
the same day, 2025-03-28 -- two days before this fixture's chosen cutoff
-- and merged within two weeks.

The most notable real-world wrinkle: **the actual PR for IGNITE-24847
("Move U to ignite-commons") also delivered IGNITE-24851 ("Move
IgniteException...") and IGNITE-24852 ("Move IgniteCheckedException...")
in the same change** (PR #11981's own title names all three). Three
separate Jira Sub-tasks, filed on the same day under the same umbrella,
ended up as one real delivered unit. Nothing in the tracker predicted
this grouping in advance -- none of the three issues carry a stated link
to either of the other two.

IGNITE-24850 ("Split IgniteUtils...") sat with no PR at all until
2025-07-14, roughly four months after being filed and after this
fixture's cutoff -- consistent with real, and apparently binding,
dependence on IGNITE-24846 and IGNITE-24848 (its two stated blockers)
actually landing first (their own PRs opened 2025-04-08 and 2025-04-12).
IGNITE-24850's own Jira ticket was not marked Resolved until 2026-01-12,
alongside the umbrella ticket IGNITE-24781 itself -- both stamped
Resolved in the same minute, suggesting an administrative batch closeout
of lingering Phase 1 tickets roughly nine months after the code side of
this phase had substantially finished, rather than that being when the
actual work happened.

## What this proves and doesn't

This is one bounded window of one real initiative, observed once. What
it does show clearly: real Jira Sub-task boundaries here did not
predict real PR boundaries (IGNITE-24847/24851/24852 example above);
a ticket whose own tracker links show it blocked by concrete, named
tasks (IGNITE-24850) genuinely sat idle until those blockers cleared,
which is a real (if single-instance) confirmation that the fixture's
"is blocked by" links reflect a real execution constraint, not just
paperwork; and a ticket's Jira status (especially "Resolved") can lag
the actual code change by months, which is a caution about over-reading
tracker metadata rather than a finding specific to this initiative.
None of this was knowable from the tracker as of the 2025-03-30 cutoff,
and none of it appears in the agent-visible fixture.
