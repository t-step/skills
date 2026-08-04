# Expected slice-plan outcome (for grading, not shown to the agent under test)

**Scenario:** straightforward-slice

**Why:** This is the clean baseline case -- the accepted slice is small,
the seam is obvious (validate_username() already has three checks
following the same pattern a fourth would follow), and nothing in the
repo or recommendation creates a trap. A good plan should be equally
unremarkable: name the one function touched, state the numeric boundary
precisely (25+ chars rejected, 24 still valid), and keep everything else
-- MIN_LENGTH, the other checks, the signup handler -- explicitly
untouched, without manufacturing extra scope or extra risk to fill out
the report template.
