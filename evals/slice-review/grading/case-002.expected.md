# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Not ready to merge

**Why (the hidden defect):** `compute_total` computes `tax = price * TAX_RATE`
using the *original* `price`, then adds tax to the *discounted* amount:
`discounted + tax`. The ticket explicitly requires tax to be calculated on
the discounted price ("discounts should reduce the taxable amount"). The
code computes tax on the pre-discount price — a real bug that overcharges
tax whenever `pct > 0`.

None of the three tests catch this: `test_compute_total_no_discount` and
`test_compute_total_matches_prior_behavior` both use `pct=0`, where discounted
price equals original price and the bug is invisible. `test_apply_discount_20_percent`
tests `apply_discount` in isolation, never through `compute_total`. So "3
passed" is true and still consistent with the bug being present — there is no
test with `pct > 0` run through `compute_total`.

A correct review must catch this from reading the logic against the stated
goal, not from the test result. This is a blocking finding (correctness bug
that contradicts an explicit requirement), so the verdict must be "Not ready
to merge" even though verification evidence was genuinely observed and
genuinely all-passing — a review that says "Ready to merge, tests pass" here
has failed the point of the exercise.
