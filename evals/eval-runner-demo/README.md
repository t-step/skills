# eval-runner-demo

Not a product skill. This is the self-test fixture for
`scripts/eval-divergence.py` — it exists to prove the runner's mechanics
(fresh independent baseline/skill runs, isolation, output capture, diffing,
deterministic verification), not to evaluate a real skill idea.

- **case-001** — a deterministic-verification case. `report.py` prints one
  debug-looking line (`STATUS: total=42`) that `check_status.py` actually
  depends on. `divergence.json` declares a `verify` command
  (`python3 check_status.py`) that fails if the line is removed or changed.
  Whether baseline and skill actually diverge here depends on what each run
  does — this fixture doesn't force a particular outcome, it just makes a
  wrong deletion mechanically detectable.
- **case-002** — a no-oracle, human-judged case. `cleanup.py` has a debug
  print gated behind `VERBOSE_CLEANUP`, documented in `runbooks/cleanup.md`
  as something on-call greps for. Nothing executes to check this; a human
  reads the diff and the captured transcript to judge whether it was
  preserved.

`SKILL.md` here is a narrow, made-up instruction (check for a dependency on
a print line's exact output before deleting it) — enough to plausibly
change agent behavior on these two fixtures, nothing more.

## `divergence.json` contract (iteration-1, this runner only)

Each case's `"files"` is exactly one directory entry — the fixture repo
root, copied fresh into an isolated scratch copy per condition. No
multi-file or multi-root fixtures are supported; `scripts/eval-divergence.py`
rejects a case with zero, more than one, or a non-directory `files` entry
before running anything. This is not a claim that the field is compatible
with other skills' `evals.json`/`pressure_evals.json` shapes.

`"verify"[].cmd` (case-001 only here) is trusted repository configuration —
it runs via the shell from inside that case's isolated scratch copy, not
the source fixture. It is not sandboxed or escaped beyond that filesystem
isolation.
