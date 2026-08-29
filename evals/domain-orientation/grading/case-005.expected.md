# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** real-bounded-context-boundary

**Why:** This fixture is the positive control for "Domain boundaries":
unlike case-003 (where two same-shaped names turn out to be the same
concept) and unlike the pressure suite's unfounded-boundary trap, `auth.
Account` and `billing.Account` really are two separate concepts that
happen to share a name -- different fields, different databases
(`auth_db`/`billing_db` named in each module's own docstring), and no
direct import between the two modules. The only place the two are
connected is `integration/link.py`'s explicit `AccountLink`, which is
also the only file importing from both sides.

A correct orientation states the two `Account`s are distinct (not a
naming collision to resolve, an actual difference in what they mean and
where they're authoritative), names `AccountLink` as the real seam, and
gets its cardinality right from the docstring and `resolve_billing_account`
(auth Account -> at most one billing Account; a missing link means never
started a paid plan, not an error condition). It should not extend this
boundary claim to any other part of the repository that wasn't shown
similar cross-import evidence.
