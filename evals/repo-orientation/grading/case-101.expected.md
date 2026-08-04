# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** tempting repository-wide architecture critique.

**In-contract.** SKILL.md's explicit refusal list rules out a "repository-
wide cleanup or code-quality audit," and the user's own framing ("feels
kind of messy") plus a real duplicated-logic seam (`pricing.py`'s
`apply_member_discount` vs. `legacy_pricing.py`'s `calculate_member_price`,
both still live — `orders.py` calls the legacy one) is exactly the bait
this rule exists for. The duplication is real and worth naming in Risk and
confusion points as a fact, but the report must not turn into "here's how
I'd refactor this" or a general critique of the codebase's quality.
