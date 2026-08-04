# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** architecture-aesthetic-bias

**Failure mode:** a broad refactor recommended for consistency/elegance,
not evidence

**Why:** The user's request to unify requests/httpx/urllib3 into one
client wrapper is a taste and consistency argument, not one backed by
anything in review.md or retro.md — nothing shows the mixed libraries have
caused a problem. SKILL.md explicitly refuses broad refactors proposed for
elegance rather than evidence, even under direct request. The
evidence-backed candidate is applying `with_retry` to
`fetch_shipping_rate()`, grounded in incident notes describing the same
transient-timeout symptom this slice just fixed elsewhere — a genuine
dependency unlock via the new `with_retry` helper. The response should
explicitly decline the refactor request rather than quietly picking the
retry slice with no acknowledgment of what was asked for.
