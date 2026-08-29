# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-file-unsafe-parallelism

**Why:** T1 and T2 both edit the same computation block in
`pricing/discount.py`, and the fixture states directly that T2's
correct value depends on T1's result. This is the negative/contrast
case for the shared-file nuance: unlike case-008, the overlap here is
semantic, not just a pathname coincidence, and no branch-isolation or
merge strategy resolves it -- T2 literally cannot be written correctly
until T1's change exists. A correct answer keeps T1 and T2 together (or
explicitly sequenced), and if it ever proposes isolated
branches/workspaces as a way to still run them concurrently, that's a
direct instance of the exact anti-pattern this skill's shared-file
wording was strengthened to refuse.
