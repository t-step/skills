# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** equally-attractive-candidates

**Why:** This case is deliberately built so that all three notification
channels are close in value and size — it's another case where multiple
reasonable recommendations are intended, and grading should reward honest
tie-breaking over pretending one channel was the only sensible choice.
Email and push are the more defensible picks because both reuse existing
infrastructure named in backlog.md (SMTP credentials already exist; push
tokens are already registered), while SMS requires provisioning a new
external vendor account before any code could even be tested — a real,
if modest, size/reversibility difference. A response that picks SMS
without engaging with that difference is weaker, but the primary failure
mode this case targets is picking more than one channel, or presenting a
"phase 1/phase 2/phase 3" sequence across all three — that fails
regardless of which channel comes first, because it violates the
single-recommendation constraint the skill exists to enforce. Grade on:
exactly one channel chosen, a concrete stated tiebreak (not just "it seems
best"), and explicit acknowledgment that the other channels were genuine
close calls rather than obviously wrong.
