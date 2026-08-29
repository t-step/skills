# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** apparent-ambiguity-already-resolved-elsewhere

**Why:** A shallow read of `spec.md` alone would flag Acceptance Scenario
3 (two reviewers claiming the same batched item at once) as an
underspecified concurrency question -- `spec.md` never restates claim
arbitration itself. But `spec.md`'s own Baseline section and Assumptions
explicitly point at `baseline-contract.md` and state plainly that claim
acquisition/release/override is inherited unchanged from
`review-queue-core`. `baseline-contract.md`'s "Claim guarantees" section
resolves the concurrency question completely (single atomic
insert-if-absent, exactly one winner, no window). A correct pass reads
`baseline-contract.md` before concluding anything about claim concurrency
is open, and reports this as **Already constrained**, citing the baseline
contract's claim-guarantees section by name -- not as a Blocking or
Material finding, and not silently ignored either (it should be visible in
the report, in the Already Constrained bucket, precisely so a reviewer can
see it was checked rather than missed).

A pass that flags Acceptance Scenario 3 as a genuine open concurrency gap
because `spec.md` itself is silent about it -- without reading
`baseline-contract.md`, or having read it but not connecting it to the
scenario -- fails this case, even if every other part of the report is
sound.
