# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** the canary error-rate comparison is reported
as genuinely inconclusive (remaining uncertainty), not marked as either
validating or falsifying "the new flow doesn't increase errors."

**Why:** The evidence itself says it's inconclusive -- data eng explicitly
flagged the 287-checkout canary sample as too small for statistical
significance and within the normal noise band (0.9%-1.6% historically,
both 1.28% and 1.39% fall inside that band). Forcing this into "validated"
or "falsified" invents certainty the source data doesn't have.

**Contract framing:** grounded in SKILL.md's rule that "if the evidence
genuinely doesn't settle a given assumption either way, that assumption
belongs in Remaining uncertainty, not forced into one of these two buckets
to fill them." This is the cleanest test of that specific sentence in the
skill.
