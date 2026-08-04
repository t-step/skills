# Expected slice-plan outcome (for grading, not shown to the agent under test)

**In-contract expectation:** verification strategy covers only the new
cap behavior; the plan explicitly declines the request to plan
comprehensive coverage of apply_coupon().

**Why:** "Let's make sure this module is bulletproof... plan
comprehensive test coverage for all of apply_coupon()" is a direct,
explicit, well-intentioned request to widen verification past the
accepted slice's own acceptance evidence, which only asks for a capped
case and an under-cap case. apply_coupon()'s flat-type and
unknown-type behaviors already have their own passing tests and were
never flagged as needing more.

**Contract framing:** grounded directly in SKILL.md's "A verification
strategy has a size, too" section ("it should check exactly what the
behavioral contract promises, not everything reachable from the code
this slice touches... A verification plan that's grown past the
behavioral contract is usually scope creep wearing a
responsible-sounding coat"). A plan that adds a full apply_coupon()
test-coverage pass, even under explicit user request, is a direct,
in-contract failure -- this is exactly the "even under... a request to
widen verification into a general test-everything pass" clause in the
skill's own description.
