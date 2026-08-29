# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** business-rules-beyond-schema

**Why:** `models.py` alone would let a shallow pass produce a plausible-
looking but shallow "domain model" (Employee/Expense/Report/Approval with
their fields). The actual domain rules -- the receipt-over-threshold
requirement and the self-approval/management-chain restriction -- exist
only in `rules.py`, invisible to anyone who reads schema and stops. A
correct orientation reads `rules.py` and its tests, not just `models.py`,
and grounds the invariants there.

`AuditEvent` is designed to look like a fifth domain entity (it's a
dataclass sitting right next to the real ones) but is a generic
implementation artifact -- every mutating rule writes one, it enforces
nothing, and nothing reads it to make a decision. A correct orientation
names it without giving it a peer entry.

`Report.status` has real transition guards (`RuleViolation` raised on
invalid transitions) and should be flagged as a lifecycle-audit candidate,
not have its own transition table built inline here -- that would be
duplicating a job this skill explicitly hands off.

**Bonus, not required for a pass:** `models.py` also declares an
`Approval` dataclass that `rules.py` imports but never constructs --
`approve()`/`reject()` only mutate `Report.status` and log an
`AuditEvent`. A strong response may notice and name this schema/code
disagreement (an entity declared but never written by any visible code);
that's a legitimate additional finding this skill's own evidence
discipline would produce, but it isn't one of the three required
expectations and its absence shouldn't be scored as a miss.
