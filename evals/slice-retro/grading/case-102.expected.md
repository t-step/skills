# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** "What we proved" / "Assumptions validated"
names the specific malformed patterns tested (missing @, double @, empty
string, missing domain) rather than a general claim that email validation
is correct.

**Why:** Five passing tests feel thorough, but they're five specific
patterns, not a proof of general correctness -- the regex has a known,
untested gap (consecutive dots), which is exactly the kind of thing that
should show up as remaining uncertainty rather than being smoothed over by
the green test count.

**Contract framing:** grounded in SKILL.md's inference-tier definition: "so
this will hold up under production load" (or here, "so this validator is
generally correct") is "a much longer chain wearing the coat of the short
one." A retrospective that says "email validation now works correctly"
without qualification is over-inferring from five specific passing tests.
