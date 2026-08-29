# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** genuinely-permitted-implementation-divergence

**Why:** FR-002 requires specific fields to be present in the report but
says nothing about layout, column order, or exact formatting -- two
competent implementers would genuinely produce visibly different reports
(a table vs. one-line-per-item vs. grouped-by-owner) while both fully
satisfying every FR and SC. This is the target finding, and it should be
classified as **Intentional freedom**, not Blocking or Material.

The correct disposition requires more than noticing the silence -- it
requires the positive-evidence check the skill's own disposition
definition calls for: the Key Entities section and Assumptions both state
explicitly that the report is human-facing/interactive, that nothing else
in scope parses its structure, and that a `grep` pipeline (the one
plausible-sounding downstream use mentioned) only needs the required text
present, not any particular order -- so nothing downstream actually
depends on which layout is chosen. A pass that classifies this only
because the spec is silent, without checking (or without being able to
point to) that nothing downstream cares, has reached the right label by
the wrong process; a pass that instead treats the `grep`-piping mention as
evidence a machine consumer might care about field order, and elevates
this to Material or Blocking, has overreached past what the fixture
actually supports (grep does not require or benefit from a particular
field order).

This case should not produce a Blocking finding. It is a legitimate,
minor pass if the report also separately (and correctly) notes this
freedom is worth surfacing in the report precisely so a reviewer can
confirm it was left open on purpose.
