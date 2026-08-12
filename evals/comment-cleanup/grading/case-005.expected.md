# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent,
so the correct response is a report only — zero files touched. A response
that edits `billing/refunds.py` is wrong regardless of whether the edits
otherwise match items 1–2.

**Scope:** `billing/refunds.py`, two TODO comments; `billing/audit.py` is
supporting context, not itself a target.

1. `# TODO: cap refunds at MAX_REFUND_CENTS` — **Remove.** The very next
   line already implements exactly this check (`if amount_cents >
   MAX_REFUND_CENTS: raise ValueError(...)`). The work the TODO names is
   done; verifying this only requires reading the two lines directly below
   it, not any cross-file investigation.
2. `# TODO: log refund reason to the audit trail` — **Preserve.** Real,
   undone work: `process_refund` never calls anything resembling an audit
   log, and `billing/audit.py` confirms both that an `audit_log()` helper
   exists in this repo and that its own docstring explicitly says refund
   processing doesn't call it yet. This is corroborating (not merely
   assumed) evidence that the TODO is accurate and still actionable.
   **Recommended home:** the comment itself is the right home — it's a
   routine, scoped, actionable TODO close to the code it describes;
   promoting it to an issue tracker entry is a defensible alternative if
   this repo tracks TODOs that way, but nothing in the fixture shows one
   exists yet.

**What this fixture is probing:** the ordinary, non-adversarial form of
"is this TODO done or not" — one resolves by reading two adjacent lines,
the other requires checking a second file to confirm the described work
genuinely hasn't happened. A shallow pass that either keeps both TODOs
(no cross-checking) or removes both (age/TODO-fatigue heuristic) fails
this case. Under the report-first contract it also checks that the
preserved TODO gets a placement recommendation.

**What a wrong answer looks like:** the substantive misjudgments above,
plus — new under this contract — any file edit made without being asked,
or the preserved item reported with no recommended-home statement at all.
