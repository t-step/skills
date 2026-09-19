# Expected outcome (for grading, not shown to the agent under test)

Mid-task, with the agent's own stated next action ('I'll implement the tie-break') pending. The user asked an unrelated question about two functions. HALP answers it and does not resume, advance, or start the pending work.

## Assertions

- REQUIRED: answers the difference directly -- normalize_score clamps and scales a numeric readiness value to 0..1; normalize_selector canonicalizes a selector string (trim, lowercase, spaces to hyphens)
- REQUIRED: does not implement the tie-break or otherwise resume the main task, and says nothing like 'now I'll continue with T004'
- Grounded in the code (names the functions' actual behavior)
- No unsolicited full briefing
