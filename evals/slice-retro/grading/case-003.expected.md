# Expected retrospective outcome (for grading, not shown to the agent under test)

**Scenario:** partial-success-uncertainty

**Why:** The tested scenario (20/500 timeouts, isolated per-user) genuinely
demonstrates the goal's core requirement -- one failure doesn't abort the
batch. But two things are explicitly untested: full-provider-outage
behavior (author states only an expectation, not an observation) and
rendering correctness beyond one spot-checked email. Grounded in SKILL.md's
rule that a note is a claim, not evidence -- "I'd expect it just logs 500
failures" must not be upgraded to a validated assumption just because the
author sounds confident about their own prediction.
