# case-004 — weak-preference-evidence

**In-contract expectation:** `NotificationDispatcher.send()` is a
hand-rolled retry loop — the same commodity pattern as case-001 — but
unlike case-001, this fixture has a comment: "Custom retry loop here --
simpler than adding a dependency just for this one call site." Per
SKILL.md's tightened evidence bar, this is a **preference-only**
comment: it states an outcome/preference (simpler, avoided a dependency)
without showing that a real constraint or tradeoff was actually weighed
(no mention of a licensing conflict, a technical mismatch, a specific
requirement the alternative couldn't meet, etc.). This should still be
flagged as a finding — the comment does not clear the candidate — but
the finding must characterize the evidence honestly as preference-only,
not report "none found," and must not use the weak evidence as license
to assert the custom code is wrong.

**Pass requires:**
1. Still flags `app/notifications/dispatcher.py`'s retry loop as a
   finding — the comment does not clear it.
2. The "decision evidence checked" content accurately describes what was
   found: a comment exists, but it states a preference/outcome rather
   than showing a considered tradeoff — not "no evidence found" and not
   treated as a decision that clears the candidate.
3. The recommendation is still to re-run the build-vs-adopt evaluation
   for this capability, not a prescribed replacement, and does not assert
   the existing implementation is wrong or should be deleted.

**Fails if:** the response treats the comment as sufficient to clear the
candidate (i.e. lists it under "considered, not flagged"), or reports
"no decision evidence found" without acknowledging the comment exists, or
uses the weak evidence to conclude the custom code should be replaced.
