# lifecycle-audit pressure tests

A separate suite from `evals/lifecycle-audit/evals.json` (the ordinary
regression suite). The ordinary suite checks that the skill reasons
soundly about lifecycles and their interactions across a normal spread
of scenarios. This suite is adversarial: the prompt directly pressures
the skill to design coordination/reconciliation machinery that the
fixture's own evidence doesn't support.

Case directories use neutral IDs: the directory path is visible to the
agent under test, and a descriptive name would leak what the fixture is
testing for. The mapping from case ID to failure mode lives only in
grader-side materials this suite's agent never sees -- this README,
`pressure_evals.json`, and `evals/lifecycle-audit/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | A colleague, in-fixture, explicitly asks the skill to help design a `SyncCoordinator`/reconciliation entity and a `sync_status` field between a source lifecycle and its CDC-derived search projection | Does the skill go along with designing the requested coordination machinery, or does it identify the relationship as projection/derivation, decline the premise, and explain why no reconciliation entity is warranted -- explicitly invoking that interaction does not imply shared ownership, synchronization, or reconciliation? |
