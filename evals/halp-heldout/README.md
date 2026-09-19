# halp held-out suites

Two manifests over `cases/`, generated fixtures (`cases/*/setup.sh` -> `repo/`), and grader-only keys in `grading/`:

- `evals.json` — generalization cases 201–219 (fresh fixtures, none shared with `evals/halp/`).
- `steering-tests/steering_evals.json` — steering-boundary cases 301–308.

These are held out: do not tune `skills/halp/SKILL.md` against them. A failure here becomes a new, distinct case in a development or regression suite before any skill change.

## Steering protocol (301–308)

Each case is two turns of one conversation:

1. The case prompt: the active direction A is in progress and the user types a `/halp <aside>` that examines an alternative B.
2. The user says `ok thanks, carry on`.

Turn 2 must be sent to the same conversation that produced the HALP aside. A fresh, independent invocation cannot show whether the aside contaminated the resumed agent, so it does not test steering. Turn 1 is graded like any other case (`expectations`, `checks`, repo unchanged). Turn 2 is graded mechanically with `check-direction.py <run-dir> grading/case-NNN.direction.json`, which looks at the lines the resumed agent added. Report steering separately from ordinary correctness.
