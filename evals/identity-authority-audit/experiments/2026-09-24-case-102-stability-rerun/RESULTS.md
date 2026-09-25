# identity-authority-audit — case-102 stability rerun (2026-09-24)

**Status:** complete — 10 fresh with-skill runs, frozen artifacts, graded
against the unedited grading key. **Separate experiment artifact.** This
does not overwrite or supersede `evals/identity-authority-audit/RESULTS.md`
(iteration-1), `../2026-09-24-reliability-baseline/RESULTS.md` (the
original 80-run with-skill/baseline experiment), or
`../2026-09-24-review-findings-fix/RESULTS.md` (the first post-fix rerun,
n=5 per case). All four remain authoritative for what they cover. This
is a measurement pass only — nothing in `skills/identity-authority-audit/`
was edited during or as a result of this experiment.

## What this experiment is

`../2026-09-24-review-findings-fix/RESULTS.md` found case-102 at 3/5
(60%) with-skill after the Review-mode Findings/Open-questions admission
rule was added, against an 8/10 (80%) pre-fix baseline, and reported it
honestly as "most plausibly sampling noise rather than a regression" —
explicitly flagging that n=5 was too small to separate the two
possibilities. This experiment reruns case-102 at n=10, under the exact
same frozen skill and prompt already used for that n=5 rerun, to get a
tighter read.

## Setup

- **PR:** #58 (`identity-authority-audit`)
- **Head SHA tested:** `63af571d7f8273d45224abcc1d220f792930e9a5`
  (`fix(identity-authority-audit): route unresolved existence-questions
  out of Findings`) — verified via `git rev-parse HEAD` before, and
  re-verified unchanged after, all 10 runs; working tree clean throughout
  (`git status`).
- **Frozen artifacts** (see `FREEZE-MANIFEST.md` and `CHECKSUMS.sha256`
  for exact SHA-256 hashes, re-verified against the live repo after the
  last run completed): `skills/identity-authority-audit/SKILL.md`, both
  references (`framework-signals.md`, `organization-profile-template.md`),
  all 5 case-102 fixture files, `evals/identity-authority-audit/grading/case-102.expected.md`,
  and the exact run prompt (`prompts/case-102-with-skill.md` — confirmed
  byte-identical to the prompt already used for the n=5 rerun in
  `../2026-09-24-review-findings-fix/prompts/case-102-with-skill.md`,
  which itself already embeds this exact post-fix `SKILL.md` verbatim).
  Nothing under `frozen/` was edited before, during, or after the 10 runs.
- **Isolation method:** each run was a freshly spawned, independent
  general-purpose subagent (no shared context with this session, each
  other, or any prior run). Each subagent was instructed to read only
  the one frozen prompt file and no other file in the repository, and
  the prompt itself instructs the model not to call any tool for the
  review — the case evidence and skill text are fully self-contained in
  the prompt. No run saw the grading key, sibling outputs, or any prior
  experiment's summary. No run received interactive correction; each
  run's raw response was captured as its final answer and saved
  unedited to `runs/102-stability-NN.md`.
- **N=10**, IDs `102-stability-01` through `102-stability-10`.

## Results

- **Raw pass count: 2/10 (20%)** — `102-stability-03`, `102-stability-07`.
- **Required-expectation results:** R1 (BFF→API A clean), R2 (raw
  forwarding confirmed), R3 (`verify_aud=False` confirmed), and R6/R7 (no
  blanket verdict) were met in **10/10** runs. **R4 (downstream
  exploitability capped at Likely/Ambiguity) failed in 8/10 runs** — this
  is the entire driver of the low pass rate. R5 (hops 2-3 treated as one
  sustained issue) failed in **1/10** runs.
- **Failure-signature counts** (full run-by-run reasoning in
  `grading_out/case-102-stability.md`):
  - **A — Absence-as-proof:** 3/10 (runs 01, 04, 10)
  - **B — Structural/consequence collapse:** 5/10 (runs 02, 05, 06, 08, 09)
  - **C — Over-demotion:** 0/10
  - **E — Chain-shape error:** 1/10 (run 06)
  - **F — Other:** 0/10
- **Unsupported-finding count: 0/10.** Every finding in every run cites a
  specific fixture fact; no run fabricated evidence. All 8 failures are
  calibration failures, not evidentiary ones.
- **Confidence-contradiction count: 5/10** (runs 02, 05, 06, 08, 09) — a
  Confirmed/HIGH finding's own "Unresolved uncertainty" text explicitly
  concedes that reachability/exploitability (exactly what HIGH's own
  definition requires — "reachable... without appropriate authorization")
  is unresolved, without the tier or severity being downgraded to match.
  The other 3 failing runs (01, 04, 10) do not self-contradict; they
  resolve the same uncertainty confidently and wrongly (absence-as-proof)
  rather than naming the tension and leaving it unresolved.
- **Mode-drift count: 0/10.**

## Run-by-run table

| Run | Required met/7 | Verdict | Failure reason (if applicable) |
|---|---|---|---|
| 102-stability-01 | 6/7 | FAIL | A — treats the repo's stated absence of gateway config as settling production reality ("downgraded to Likely" only in "an engagement with an incomplete repository") |
| 102-stability-02 | 6/7 | FAIL | B — Confirmed/HIGH on the audience gap while its own hedge says exploitability is exactly what's unresolved |
| 102-stability-03 | 7/7 | **PASS** | — Confirmed/MEDIUM structural fact ("missing defense in depth"), reachability correctly routed to its own Open Questions entry |
| 102-stability-04 | 6/7 | FAIL | A — most explicit instance: states `api_b.py`'s own handling "is the complete picture of what happens to a request before this code runs" as unhedged fact |
| 102-stability-05 | 6/7 | FAIL | B — "independent of anything else that may or may not exist around it" used to keep HIGH while conceding exactly that dependency is unresolved |
| 102-stability-06 | 5/7 | FAIL | E — API B and MCP presented as three non-adjacent, non-connected findings (with an unrelated scope finding interleaved); also B (secondary) |
| 102-stability-07 | 7/7 | **PASS** | — Likely/HIGH, explicit hedge, explicitly cites the skill's own tier logic for choosing Likely over Confirmed |
| 102-stability-08 | 6/7 | FAIL | B — explicit "either way... directly observed... regardless of that fact" reasoning used to justify keeping Confirmed/HIGH despite conceding severity could be lower |
| 102-stability-09 | 6/7 | FAIL | B — "Why it matters" asserts an unhedged "will be reachable" claim directly contradicted by its own "Unresolved uncertainty" line |
| 102-stability-10 | 6/7 | FAIL | A — most blatant instance: explicitly names and dismisses "the usual 'maybe a gateway checks it' hedge" as foreclosed |

## Comparison

| Stage | Skill state | n | Pass rate |
|---|---|---|---|
| Original reliability experiment | pre-fix | 10 | 8/10 (80%) |
| First post-fix rerun | post-fix | 5 | 3/5 (60%) |
| **This stability rerun** | post-fix (same SHA as the n=5 rerun) | 10 | **2/10 (20%)** |

These three numbers are reported separately, not pooled into one rate —
the first used a materially different `SKILL.md` (pre-admission-rule);
the latter two used the identical post-fix skill and the identical run
prompt, so they are the directly comparable pair.

## Interpretation

Per the predeclared bands: **2/10 falls in the 0–5/10 band — a credible
regression signal, calling for inspection of the failure signature before
deciding what, if anything, is warranted** (not a statistical-confidence
claim; a practical decision rule, applied here as predeclared before
these results were seen).

Read alongside the n=5 rerun, the post-fix skill's combined case-102
with-skill record is now 15 runs: 3 pass in the n=5 batch (60%), 2 pass
in this n=10 batch (20%) — pooled, 5 passes / 15 runs (33%), 10 fails /
15 (67%). Both post-fix batches were sampled independently, under the
byte-identical frozen skill and prompt, and both land well below the
pre-fix 80% baseline rather than either one looking like a one-off
outlier of the other — which weighs against "pure sampling noise around
the pre-fix 80% baseline" as the full explanation, and toward a real,
reproducible drop in this specific tier-discipline behavior under the
post-fix skill text, even though (per the section below) the mechanism
responsible does not appear to be the new admission-rule/Open-Questions
routing itself.

## New-structure regression check

**Did the new Findings/Open-questions admission structure cause the
case-102 behavior to worsen?**

**No — not by the mechanism the structural change actually touches.**
The specific risk Task 1/2 of the prior experiment was built to prevent
— a genuinely Confirmed structural fact getting laundered into a hedged
Confirmed/Likely finding, or conversely a real defect getting demoted
into `## Open questions / ambiguities` to dodge the admission rule — did
not occur in any of the 10 runs (T3: 0/10). In every run, the raw
`api_a.py`→`api_b.py` forwarding and `api_b.py`/`mcp_gateway.py`'s
`verify_aud=False` were reported as Confirmed facts inside `## Findings`,
exactly where they belong, and the genuinely unresolved items each run
did surface (new-tool sensitivity, deliberate-vs-oversight, BFF scope
narrowing, `supplier_notes_tool`'s internal authorization) were correctly
routed to `## Open questions / ambiguities` rather than either omitted or
smuggled into Findings. The new report structure is doing its intended
job everywhere it was exercised in this batch.

The actual failure driving the 2/10 rate — an unhedged or
self-contradicting Confirmed/HIGH tier on the **downstream-exploitability
consequence** specifically (R4) — is the same failure signature the
original pre-fix 80-run experiment already documented once (run-07,
1/10) and the first post-fix rerun documented twice (2/5). It is a
Confirmed-vs-Likely tier-selection question the admission-rule text does
not address: that rule governs whether an item may appear in `##
Findings` under any tier at all; it says nothing about how a run should
choose between Confirmed and Likely for an item it has already decided
belongs there. There is no sentence in the `SKILL.md` diff
(`git diff` between the pre-fix and post-fix `SKILL.md`, reviewed at the
top of this experiment) that plausibly loosens that specific choice.

**What the evidence does support:** this specific tier-discipline
behavior on this specific case is measurably worse under the post-fix
skill (10/15 fails across the two post-fix batches, 67%) than it was
under the pre-fix skill (1/10, 10%) — a real, reproducible-across-batches
gap, not explained by the admission-rule mechanism itself, and not yet
explained by anything else this experiment isolated. That gap is reported
here as an open, unresolved finding rather than either dismissed as noise
or wrongly pinned on the mechanism this rerun was asked to investigate
first.

## Recommendation

**Unstable but no clear structural regression tied to the new
Findings/Open-questions admission mechanism; carry this limitation into
real-repo trials.**

The admission-rule/Open-Questions change itself is not implicated by the
failure signatures observed (0/10 over-demotion, 0/10 misrouted
structural facts) and should not be reverted or further edited on the
strength of this experiment. Case-102's Confirmed-vs-Likely tier
discipline on the downstream-exploitability consequence is a real,
independent, and now well-evidenced fragility (67% fail rate across 15
post-fix with-skill runs, versus 10% pre-fix) that predates this
structural change and is not resolved by it — worth a dedicated look at
some point (most plausibly a case-102-specific rubric/example
clarification, or accepting this as this case's genuine difficulty
ceiling for the current model), but that is a distinct investigation
from "did this PR's structural fix regress anything," which this
experiment answers no to.

## PR hygiene

This is the only file this pass adds to the repository, alongside its
own `frozen/`, `prompts/`, `runs/`, `grading_out/`, `FREEZE-MANIFEST.md`,
and `CHECKSUMS.sha256` under this experiment's own directory. No prior
`RESULTS.md`, run file, or grading file anywhere in
`evals/identity-authority-audit/` was modified, moved, or deleted. No
skill, reference, fixture, or grading-key file was edited. The existing
PR narrative and its prior-reported case-110/case-102/case-106 results
are left exactly as previously written — this result does not change
the PR's headline finding (the case-110 self-contradiction fix), and is
added as a named, citable follow-up rather than folded into or smoothing
over the prior n=5 case-102 report.
