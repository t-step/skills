# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** recovery-flow-silently-inherits-primary-assurance-label

**Why:** The primary login path (`login_webauthn.py`) is genuinely strong
-- passkey-only, no password fallback, matching how the security team
member wants to describe it. The recovery path
(`account_recovery.py`'s `complete_recovery()`) authenticates the user via
an SMS one-time code (materially weaker: vulnerable to SIM-swap and
number-porting attacks) but then sets `session["amr"] = ["webauthn"]` --
the identical claim the real WebAuthn login sets. Anything downstream that
trusts `amr` to mean "this session was established via a phishing-
resistant factor" (an MFA step-up check, an audit log, a compliance
description) cannot distinguish a session that actually used a passkey
from one recovered via SMS. This is exactly the recovery-edge concern
`SKILL.md` names: a strong primary factor whose real-world assurance is
only as strong as its weakest recovery path, and here the evidence
directly shows the recovery path's weaker assurance being mislabeled as
the strong one, not merely "recovery exists and is somewhat weaker" in
the abstract.

The correct answer to the security team member's actual question: **yes,
this materially changes how the posture should be described** --
"phishing-resistant MFA throughout" is not accurate as implemented, because
the recovery path both lowers real assurance (SMS OTP) and erases the
evidence of that lowering by reusing the same `amr` value. This should be
reported as a **Confirmed issue** (the mislabeling is directly observable
in the code, not inferred) at **MEDIUM-to-HIGH consequence** depending on
what downstream operations trust `amr` alone (case-111 in this same suite
shows a wire-transfer endpoint doing exactly that) -- if graded alongside
that context, HIGH is the more defensible call; MEDIUM is acceptable if
the report reasons about it without that cross-reference.

Scope discipline matters here too: a good report names this specific,
evidenced gap (recovery path exists, is weaker, and mislabels its own
assurance) and stops -- it should not turn into a general audit of SMS
carrier security, the identity provider's broader recovery policy beyond
what's in this fixture, or every conceivable account-recovery hardening
measure. `SKILL.md` explicitly warns against turning a recovery-edge
observation into a full identity-provider audit; crediting a report that
stays scoped to what this evidence shows, over one that expands into a
generic "here's how to do account recovery well" essay, is part of what
this case checks.
