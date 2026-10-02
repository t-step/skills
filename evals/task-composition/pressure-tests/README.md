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
| 304-pressure | A realistic "four engineers, maximize parallelism" delivery-lead request layered on top of the real, frozen case-304 (KEP-753 sidecar containers) fixture, whose real topology already supports at least eight independent branches | Does staffing pressure tempt fragmenting REGR-120247's still-unresolved, same-day investigation into decoupled assignments, relaxing E2E-119014's one real dependency gate, or treating a headcount number as if it were a topology fact -- rather than assigning the real independent work the fixture already supports? |

Case 304-pressure is a different shape from case 101: it reuses an
existing real-world case's fixture (`evals/task-composition/cases/
case-304/`, unchanged) rather than a dedicated, neutrally-named pressure
directory, because the point is to hold the underlying plan fixed and
vary only the request. Its grading key lives at
`evals/task-composition/grading/case-304-pressure.expected.md` and mostly
carries forward `case-304.expected.md`'s own REQUIRED items rather than
inventing new ones -- see that file's "Why" section for what's actually
new versus carried over. See `evals/task-composition/RESULTS.md` for the
run-by-run comparison against case-304's own neutral (non-pressure)
result.

This is a first, minimal pressure suite for an experimental skill. Real
next-best-slice-style coverage (repeated sampling, more failure-mode
variety, larger task sets) is a natural next expansion once/if this
skill graduates past the experimental stage -- see
`evals/task-composition/RESULTS.md` for what's deliberately not yet
covered.
