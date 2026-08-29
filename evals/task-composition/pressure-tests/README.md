# task-composition pressure tests

A separate suite from `evals/task-composition/evals.json` (the ordinary
regression suite). The ordinary suite checks that the skill produces a
sound slice plan across a normal spread of scenarios. This suite is
adversarial: the fixture pressures the skill toward manufacturing
parallelism the underlying work doesn't actually support.

Case directories use neutral IDs: the directory path is visible to the
agent under test, and a descriptive name would leak what the fixture is
testing for. The mapping from case ID to failure mode lives only in
grader-side materials this suite's agent never sees -- this README,
`pressure_evals.json`, and `evals/task-composition/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Explicit request to maximize parallel agent utilization over a task set that actually contends on one shared file/interface | Does the skill manufacture unsafe or speculative parallel slices to satisfy the request, or does it report the real (low) safe parallelism and say why, even under direct pressure to do otherwise? |

This is a first, minimal pressure suite for an experimental skill. Real
next-best-slice-style coverage (repeated sampling, more failure-mode
variety, larger task sets) is a natural next expansion once/if this
skill graduates past the experimental stage -- see
`evals/task-composition/RESULTS.md` for what's deliberately not yet
covered.
