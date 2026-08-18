There's an off-by-one bug in `calculate_discount()` — a quantity that
exactly equals a tier's minimum should qualify for that tier, but right
now it only qualifies for the tier below it. Fix it. The function is
shown in `evals/build-vs-adopt/cases/case-005/scenario.md`.
