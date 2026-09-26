# case-026: producer -> consumer handoff round trip

**This case is authored and frozen for a two-phase, two-agent run. It has
not been run. Running it requires a small amount of live orchestration
by whoever executes it -- read this file fully before starting either
phase.**

## What this case tests

Whether a field-debug Handoff artifact, on its own, carries enough state
for a completely fresh agent to continue an investigation without
either (a) needing anything from the producing agent's raw transcript,
or (b) discarding correctly-preserved state and redoing settled work.

## How to run it

1. **Phase A.** Give a tested agent (with the field-debug skill
   available) only `phase_a/context.md` and the other files directly
   inside `phase_a/`. Let it investigate. The fixture is built so that a
   competent investigation reaches a genuine Handoff -- if the agent
   does not produce one, that is itself a finding (grade it as a
   production failure, per `grading/case-026.expected.md`).
2. **Capture only the produced handoff artifact** -- the block of output
   matching the skill's `## field-debug handoff: <target>` template (or
   materially equivalent content, however it's formatted). Save it
   verbatim as `phase_b/handoff_artifact.md`, replacing the placeholder
   file already there. Do **not** carry over anything else from Phase A:
   no raw transcript, no scratch reasoning, no tool-call log, no restated
   summary written by the orchestrator. If Agent A produced other
   commentary around the handoff block, it is excluded -- only the
   handoff block itself is the artifact.
3. **Run `scripts/verify_case_026_round_trip_isolation.py`** against this
   case directory before starting Phase B. It confirms `phase_b/`
   contains no leaked content from `phase_a/`'s other evidence files
   beyond what `handoff_artifact.md` legitimately carries forward as
   prose, and that no transcript-shaped file has been dropped in by
   mistake.
4. **Phase B.** Start a completely fresh agent (no memory of Phase A, no
   access to the orchestrator's own reasoning about Phase A) and give it
   only `phase_b/context.md`, the now-replaced `phase_b/handoff_artifact.md`,
   and the other files directly inside `phase_b/`. Let it continue the
   investigation to a conclusion, or say plainly what's still needed.
5. Grade both phases and the round trip together against
   `grading/case-026.expected.md`.

`phase_a/` and `phase_b/` are evidence for two *different* agents at two
different points in time and must never both be shown to the same
agent.
