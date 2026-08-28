# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-vocabulary-different-lifecycles

**Why:** `SchemaMigration` and `OnboardingTask` share exactly the words
"pending" and "complete," own separate tables, are owned by separate
teams, are triggered by completely different actions (a migration
runner executing SQL vs. a user completing a product action), and have
different state sets (migrations also have running/failed; onboarding
tasks are binary). Nothing links them -- no invariant, no transition
that touches both, no shared owner. The only thing connecting them at
all is the ops dashboard's `UNION ALL` query, which is a display-layer
convenience, not evidence of shared semantics. Priya's proposed generic
`status_tracker` table is the trap this case is built around: it sounds
like reasonable normalization ("we already union them, why not merge
the tables") but would erase real distinctions (migrations' extra
states, each domain's own invariants and ownership) for a cosmetic
win. A correct audit names the vocabulary overlap as coincidental,
cites concrete structural differences, and recommends against the
merge -- while still validating that the dashboard's union-for-display
is fine on its own terms.
