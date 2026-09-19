# Expected outcome (for grading, not shown to the agent under test)

A sprawling state: a long branch, 12 modified files, 5 untracked drafts, a 20-item task list (15 ticked), three undecided open questions. A useful answer prioritizes and summarizes; it does not inventory.

## Assertions

- REQUIRED: gives the position (branch; 15 of 20 tasks done, T016-T020 open) and the uncommitted volume in summary form (about a dozen modified files, five untracked drafts)
- REQUIRED: does not enumerate the files one by one (names at most a handful) and does not reproduce git or log output
- REQUIRED: surfaces the undecided open questions (OQ-1..OQ-3) at summary level
- Prioritizes what matters for orientation rather than covering everything
