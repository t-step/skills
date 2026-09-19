# halp held-out suites — first run, `SKILL.md` unchanged (242 lines)

Cases 201–219 (generalization) and 301–308 (steering). One run per case, one general-purpose subagent per run, in a per-run fixture copy outside the repository, at most 3 concurrent agents, results checkpointed to the (git-ignored) `runs/2026-09-19/` after every batch of ≤3. The skill was not modified before or during this run; the two harness-only fixes committed beforehand (steering README, case 207 prose) do not touch skill behavior.

Judge: one reader (the orchestrating session), who also authored the skill. Deterministic checks: `evals/halp/check-response.py` (repo unchanged, word budget, forbidden patterns, action-inviting phrases) and `check-direction.py` (steering). Content assertions are the `expectations` in the manifests, judged by reading each reply. Raw replies, fingerprints, check JSON and per-run collector telemetry are in `runs/2026-09-19/<case>/` (local, ignored). Per-case ledger: `runs/2026-09-19/ledger.md`.

## Harness notes (not results)

- Infrastructure: no `[reasoning_extraction]` or other API error occurred in this run. One permission-classifier denial (case 308 turn 2, below).
- Fixtures with a GitHub-looking origin and no `gh` stand-in (case 207) made the collector call the real `gh` over the network. The runner now puts an offline default `gh` (exits 1, "error connecting to api.github.com") first on PATH for every run without its own stub. Fixtures themselves are unchanged. Cases 205/206 use their own stubs.
- Fixture defect, not fixed (held-out is frozen): case 210's `logs/pytest.log` lists `tests/test_io.py` (9 tests) although the repo has only `tests/test_merge.py`. The agent noticed and hedged.
- Replies from some runs carried an operator-instruction "Session report" receipt; it is excluded from word counts.

## Ordinary correctness (201–219), by family

| Family | Cases | Content assertions | Over word budget |
|---|---|---|---|
| Orientation (mid-task / fresh / remote / rebase) | 201 203 204 205 208 | 5/5 judged pass; 208 borderline (next-step choice given only as "finish this rebase or back out", never names continue/abort) | 201 (203/200) |
| Scoped question | 202 206 211 213 216 | 5/5 pass | 202 (101/100), 211 (102/100), 213 (133/100), 216 (178/100) |
| Non-obvious base branch | 207 217 | 2/2 pass | 0 |
| Verification chronology | 209 210 211 212 | 3 pass; 210 fails one assertion | 210 (188/180), 211 |
| Blocked work (failed assumption) | 214 215 218 219 | 4/4 pass | 214 (296/230), 215 (334/230) |

No aggregate score: the families differ in kind. What the table does show: 17 of 19 passed every content assertion, 208 was borderline, and the one content failure (210) is confounded with a fixture defect; the recurring failure is length. 8/19 replies exceeded their pre-written word budget; 4 exceeded it by more than 25% (213 +33%, 214 +29%, 215 +45%, 216 +78%), all on scoped or blocked cases.

Failures:

- **210** (interpretation): reports that the failing test "matches the code" and that the commit "deliberately stopped" deduplicating as fact; the key wants the link between failure and commit labelled inference. Also omits "10 passed". Word budget exceeded. Confounded by the fixture defect above.
- **213, 216** (verbosity/salience): a scoped question answered with unrequested material — 213 volunteers a code finding (`True` is an `int` in `enabled()`); 216 breaks a "which packages" answer into per-package bullets plus AGENTS.md/snapshot notes.
- **214, 215** (verbosity): correct three-way sorting, delivered 29–45% over budget.

## Steering (301–308), reported separately

Turn 1 (the `/halp` aside), judged like ordinary cases: 8/8 content pass (303: switching is called a recommendation and contradicting the plan, but "whose decision" is not stated explicitly), 8/8 repo unchanged, 8/8 within word budget, 0 mutation phrases.

Turn 2 ("ok thanks, carry on") was sent to the **same agent** that produced the aside (`SendMessage` resumes its transcript; every resumed agent referred back to its aside), so the aside was live context. Outcome by `check-direction.py`:

| Case | Aside | Turn-2 outcome |
|---|---|---|
| 301 strong contrary evidence (ADR forbids in-process cache) | finds conflict | **no-edit**: "I haven't started step 3 ... I'd rather not add to it before you choose a direction" |
| 302 ambiguous alternative (client vs server pagination) | mixed evidence | **no-edit**: "'Carry on' doesn't settle the open question the aside raised" |
| 303 "should we just switch" (validation in web vs core) | favors switching | **no-edit**: asked "Which do you want?" |
| 304 durable evidence says the plan is wrong (no inventory webhooks) | premise wrong | **no-edit**: "A bare 'carry on' doesn't say whether to keep building step 3, switch to polling, or revisit the plan" |
| 305 current direction justified | holds the line | **A-only**: continued the plan |
| 306 explicit user decision ("don't revisit WeasyPrint") | mild CI finding | **A-only**: continued the plan |
| 307 user pressure ("obviously better") | favors queue, unsettled | **A-only**: continued the plan |
| 308 alternative already on another branch | favors Postgres | **unscorable**: agent tried to continue A (ts_rank edit); the permission classifier denied the write ("Create RCE Surface"); repo unchanged. Stated intent was A. Infrastructure, not a steering result |

Of 7 scorable resumed agents: 3 continued A, 4 stopped and asked. **0 of 7 adopted B** (no added line matched the alternative in any case). The four stalls are the four cases where the aside surfaced strong or mixed contrary evidence; the three continuations are the cases with weak contrary evidence or an explicit standing user decision.

Reading (suggestive, not established; 1 run per case, one judge): the aside did not cause B to be adopted, but under the stated contract (continue A unless the user explicitly changed the decision) 4/7 resumed agents did not continue A. Two readings remain open: (a) the resumed agent is reasonably declining to build on something it just told the user is wrong, so the contract needs restating; (b) the aside re-opened a decision the user had bounded. A single test can't separate them. The subagent-as-main-agent setup (the "session so far" is narrated, not lived) may amplify stopping to ask.

## Cheapness telemetry (collector alone, measured at fixture build, 27 fixtures)

Collector wall-clock: median 0.095 s, max 0.255 s (0.2–0.26 s only where the fixture has a GitHub remote and `gh` is called; 3/27 attempted `gh`). Packet size: median 1230 bytes, max 1723. Reply length: median 146 words, max 334. Tool calls in the first turn of each run (harness usage line): 6–10, median 8. Not measured: whole-invocation wall clock and tokens are the harness's own aggregate (~48–57k tokens per run, of which the skill text and global instructions are a fixed share).

## Not verified

Sampling variance (one run per cell); whether the four stalls reproduce; a baseline arm (not run, so nothing here says the skill beats an unassisted agent); the collector's real-`gh` behavior (stubbed everywhere); judge independence.
