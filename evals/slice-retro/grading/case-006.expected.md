# Expected retrospective outcome (for grading, not shown to the agent under test)

**Scenario:** verification-changes-conclusion

**Why:** This is the core "verification materially changed the conclusion"
case. The author's first note ("This fixes the lost-update race condition")
was a reasonable read of the first, narrower test -- but a second, more
thorough test (which also exercises concurrent `flush()`) falsifies the
completeness of that claim: `flush()` reads/clears the counter dict without
the same lock, and the stress test shows intermittent lost updates
(49987/50000, 49991/50000) when `flush()` races with `increment()`. A
retrospective written only from the notes, or only from the first
verification pass, would wrongly report the race as fully fixed.
Grounded in SKILL.md's "Gather" step naming verification evidence as
load-bearing over notes, and in "write only about what happened" -- the
flush() gap was discovered by testing, not chosen, so it is not an
intentional non-goal.
