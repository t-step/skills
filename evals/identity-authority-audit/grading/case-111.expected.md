# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** step-up-freshness-vs-mfa-already-upstream

**Why:** This fixture pairs a correct step-up implementation with a
correct *absence* of one, and the compliance question specifically invites
treating the absence as a gap by default. A correct report distinguishes
the two rather than "fixing" the one that isn't broken:

- **`/api/wire-transfers` -- correct step-up (assurance) transition.**
  `create_wire_transfer()` checks both `auth_time` freshness (within 5
  minutes) and that `amr` includes `webauthn`. This is checking something
  ordinary session presence doesn't guarantee: recency of a
  phishing-resistant authentication event, not merely that one happened
  at some point in this session's lifetime. Name this as a correctly
  implemented step-up transition.
- **`/api/billing-history` -- correctly requires nothing more, given the
  evidence.** `idp_tenant_config.yaml` states this tenant's IdP enforces
  WebAuthn as the sole primary factor for every login, with no
  password-only fallback -- meaning MFA is handled entirely upstream, and
  every session the app ever sees already used a phishing-resistant
  factor. Given that, requiring only `session.get("user_id")` for a
  read of billing history is not a gap to fix; it's the correct
  conclusion that this specific control (factor strength) is already
  satisfied upstream for every session, with nothing left for the app to
  add on that dimension. A report that recommends adding a step-up check
  to `billing_history()` "to be safe," or treats its absence as
  inherently a compliance gap, is manufacturing a finding the evidence
  doesn't support -- exactly what `SKILL.md` says not to do.

A precise report may still note that `billing_history()` has no
*freshness* requirement (an old, still-valid session with no forced
re-auth interval could view billing history indefinitely) -- if raised,
this should be framed as, at most, a distinct, low-to-medium observation
about session lifetime/freshness policy generally, clearly separated from
the MFA-factor-strength question the ticket actually asks about, not
conflated with "MFA is missing here." Do not accept a report that treats
`billing_history()`'s lack of step-up as equivalent in nature to a genuine
missing-MFA finding, and do not accept a report that fails to notice
`idp_tenant_config.yaml` establishes upstream MFA at all (i.e., treats the
tenant as if password-only login might be possible).
