# Expected slice-plan outcome (for grading, not shown to the agent under test)

**Scenario:** invariant-across-boundary

**Why:** serializers.py's own docstring states the exact contract at
stake: the returned key set is a public API boundary depended on
outside app/. A plan that just says "add last_login_at" without also
naming that the existing four keys must not move or disappear, and that
password_hash must keep being excluded, is treating the file as if it
had no existing contract -- exactly the failure this skill's Invariants
section exists to prevent. client_consumer.py's REQUIRED_KEYS set and
the existing test's explicit `"password_hash" not in payload` assertion
are both concrete, discoverable grounding for this -- a plan should cite
something like this, not just assert the invariant in the abstract.
