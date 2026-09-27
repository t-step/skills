# field-debug — eval suite

This suite exercises `skills/field-debug/SKILL.md`, an investigation
protocol for systems whose true behavior extends beyond the checked-out
repository (a gateway, a queue, an identity provider, a vendor console, a
colleague's terminal, a prior engineer's handoff note). Each case is a
static snapshot of evidence — files an investigating agent can read, with
no live system behind them — plus a sealed grading key describing the
hidden ground truth and what a correct investigation must and must not
claim.

Cases are agent-visible; grading keys are not. Nothing under `cases/`
should ever reveal a scenario's verdict, and `scripts/check-eval-isolation.py`
(at the repo root, if present alongside this suite) enforces that
mechanically. Two of the multi-phase cases below carry their own
additional isolation scripts for the same reason — see "Multi-phase and
resume cases."

## Layout

- `cases/case-NNN/` — the complete evidence set for one investigation.
  Nothing outside this directory should be needed to attempt the case.
- `grading/case-NNN.expected.md` — the hidden ground truth, the evidence
  chain a correct answer must cite, and the wrong turns a plausible
  investigation might take.
- `pressure-tests/pressure_evals.json` — a machine-readable manifest of
  the same cases (prompt text, file lists, pass/fail expectations) for
  automated eval-harness runs.
- `scripts/` — isolation/correctness checks for the fixtures that need
  more than a read to validate (see below).

## What this suite covers

This is a representative, non-exhaustive set: each retained case exercises
a distinct investigative behavior rather than a distinct domain, and nearly
identical variants of an already-covered behavior are left out. Grouped by
the behavior each primarily pressures:

- **Observation vs. inference vs. unknown, and refusing absence-as-proof**
  (`case-001`, `case-007`, `case-029`) — a component behaving exactly as
  its own convention specifies, an absent in-app control that's actually
  enforced upstream, and a crash that happens *after* an external call
  already returned: in each, the correct move is recognizing what the
  evidence does and doesn't establish, not treating a local absence as
  proof of a global one.
- **Reasoning under incomplete or fragmented observability**
  (`case-002`/`case-003` pair, `case-022`) — the same underlying incident
  with and without a key telemetry source, and a case where two systems'
  own acknowledgments describe different scopes of "success."
- **Changing access or credentials between participants**
  (`case-004`, `case-013`, `case-015`, `case-023` stage 1) — a secret
  rotated everywhere except one long-running process's cached copy, a
  personal account standing in for a service identity, a stalled rollout
  leaving most of a fleet on a revoked key, and a retired auth scheme
  encountered mid-investigation.
- **Ownership and handoff boundaries** (`case-007`, `case-013`,
  `case-024`, `case-028`) — enforcement living at a boundary the repo
  doesn't show, identity/audit ownership crossing a tooling boundary, a
  vendor-side processing wall that cannot be resolved from this side, and
  a tenant-owned configuration decision that looks like a bug but isn't.
- **Resuming an investigation after context or the system has changed**
  (`case-020`/`case-021` pair) — a matched changed-world/unchanged-world
  pair: one where a resumed investigation must detect that a
  runtime-perishable fact moved since the checkpoint was written, and a
  control where it correctly doesn't.
- **Preserving evidence and next actions through handoff**
  (`case-008`, `case-025`, `case-026`) — assimilating a delegate's
  conclusion without adopting it as ground truth, recovering from a
  handoff note that omits something the prior investigator actually knew,
  and a full producer/consumer round trip graded on whether a gap is a
  production loss or a consumption failure.
- **Avoiding unjustified certainty** (`case-005`, `case-008`) — two
  independent, unrelated failures that share a tempting single
  explanation but don't share a cause, and a delegate's own conclusion
  ("probably a firewall rule") going further than what they actually
  observed.
- **Decomposing and recomposing investigative work** (`case-011`,
  `case-023`, `case-026`) — a real defect that explains the *mechanism*
  of a gap but not its full *magnitude*, three genuine, sequential,
  unrelated failures at three different boundaries, and two independently
  investigating agents whose work must recompose correctly through a
  single handoff artifact.

## Multi-phase and resume cases

- `case-020` / `case-021` are a checkpoint/resume pair validated together
  by `scripts/verify_checkpoint_resume_isolation.py`: it confirms neither
  case's checkpoint leaks a fact only present in the post-resume state,
  and that no raw prior-investigator transcript (as opposed to the
  checkpoint itself) is agent-visible.
- `case-023` is a three-stage progression (`401` → `422` → `429`)
  validated by `scripts/verify_case_023_progression.py`, which actually
  runs the fixture's code through each stage to confirm the sequence is
  real and deterministic, not scripted narrative.
- `case-026` splits evidence across `phase_a/` (given only to the
  producing agent) and `phase_b/` (given only to the consuming agent),
  with the only permitted channel between them being
  `phase_b/handoff_artifact.md`. `scripts/verify_case_026_round_trip_isolation.py`
  checks that boundary mechanically, both before and after
  `handoff_artifact.md` is filled in with a real agent's output.

## Running the suite

Each case in `cases/` is self-contained: hand its directory to an agent
with `skills/field-debug/SKILL.md` loaded, using the prompt in the
matching `pressure-tests/pressure_evals.json` entry (or a case's own
`context.md`/`README.md` where one exists). Grade the result against
`grading/case-NNN.expected.md`, which states both what must be found and
what a plausible wrong answer would look like. For the three cases with
dedicated scripts above, run those scripts before trusting the fixture
itself.
