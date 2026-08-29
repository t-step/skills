# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** readme-invariant-contradicted-by-code

**Why:** The README states a clean, plausible-sounding business rule
("once confirmed, date and room cannot change") that reads like exactly
the kind of invariant this skill is supposed to surface. It's false:
`reschedule()` in `bookings.py` changes both fields on a `Booking` in any
status, including `confirmed`, with no status check present anywhere in
the function. SKILL.md's own rule -- executable evidence outweighs prose,
and the disagreement itself is worth naming -- applies directly here. A
shallow pass that reads the README and repeats its claim as an observed
invariant, without checking `bookings.py`, fails this case even if
everything else about the report is well-formed. The correct answer
names the conflict explicitly and treats `reschedule`'s actual behavior,
not the README, as what's currently true of the system.
