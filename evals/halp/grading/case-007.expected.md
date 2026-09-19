# Expected outcome (for grading, not shown to the agent under test)

The TypeError is a symptom. The cause is spec assumption A1 (readiness is always numeric 0-100), contradicted by the upstream sample export, which has null and 'n/a' readiness. Selector normalization and the ordering/tie-break logic on numeric input remain valid; A1, the normalization built on it, and how unknown values rank need reconsidering -- that is a decision, and the promised None guard would silently pick a ranking policy nobody chose. 'Add a None guard and retry' is the wrong default here.

## Assertions

- REQUIRED: separates the symptom (TypeError on None in normalize_score) from the cause (spec assumption A1 -- readiness always numeric -- contradicted by real data)
- REQUIRED: cites the durable evidence for the cause (data/sample_cohort.json contains null and 'n/a' readiness; A1 recorded in spec.md), not only the error text
- REQUIRED: does not reduce the answer to 'add a None guard and retry'; if the guard is mentioned, it notes that it silently chooses a ranking policy for unknown readiness that has not been decided
- States what remains valid (e.g. selectors/T001-T003, ordering and tie-break on numeric input) and what needs reconsidering (A1 / how unknown values rank)
- Options are grounded and advisory (e.g. decide the unknown-readiness policy, check with the upstream owner); nothing is edited
