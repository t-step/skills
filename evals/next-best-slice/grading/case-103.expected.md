# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** recency-bias

**Failure mode:** staying in the same file/module because it's fresh,
instead of following the evidence

**Why:** The footer-alignment fix and the shipping-label mojibake fix are
both in the same module, but only one is backed by real evidence: support
ticket #4471, filed three months ago and closed as "can't reproduce," now
reads as an exact match for the bug this slice just fixed on invoices —
the new UTF-8 helper is a direct, evidence-grounded dependency unlock for
that ticket. The footer misalignment has no reported user impact at all.
"We're already in this code" is not itself a reason per SKILL.md's
criteria; the response should recommend the shipping-label fix and ground
it in the ticket, not in proximity to the just-edited file.
