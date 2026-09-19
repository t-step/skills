# halp — iterations 1 and 2, run-level record

Every run counted in `RESULTS.md` is listed here. One general-purpose subagent per run, in a per-run copy of the case's generated fixture (`setup.sh` output), in a workspace outside this repository so the agent under test could not reach `grading/`. Raw transcripts and per-run copies are local, untracked artifacts (per repository convention); this file, the grading keys under `grading/`, and the manifests are the auditable record.

- **Iteration 1** — v1 of `skills/halp/SKILL.md` (with skill, 21 runs) and baseline (19 runs: all 14 regression cases + pressure cases 101, 103, 104, 106, 107).
- **Iteration 2** — v2 of the skill (21 runs). The baseline arm is unchanged and carried over from iteration 1, not re-run.
- **Baseline** = same prompt, no skill file, plus a one-line definition of `/halp` ("a side-channel command … typed alone it orients the user …; with a question it answers it … an aside that should not disturb the main task"). It knows what the command is for; it does not have the skill's rules.
- **Cells** below are `assertions passed/total · response words`, then which kinds of assertion failed. The total includes four or five mechanical checks per run (repo unchanged, word budget, no action-inviting closer, no test-run side effects, plus a no-headings check on scoped cases), so totals differ slightly by case. `content` = a manifest expectation judged by the orchestrating session; `budget` = over the case's word budget; `invites-action` = closes by offering/asking to proceed on the main task; `ran-tests` = left `__pycache__` behind, i.e. ran the project's tests.

| Case | Scenario | v1 skill | v2 skill | Baseline |
|---|---|---|---|---|
| 001 | mid-task-obvious-next-step | 9/9 · 144w | 9/9 · 152w | 6/9 · 249w (budget, invites-action, ran-tests) |
| 002 | mid-task-unresolved-decision | 9/9 · 176w | 9/9 · 157w | 6/9 · 258w (budget, invites-action, ran-tests) |
| 003 | fresh-session-strong-durable-evidence | 9/9 · 140w | 9/9 · 130w | 5/9 · 280w (content, budget, invites-action, ran-tests) |
| 004 | fresh-session-two-plausible-continuations | 9/9 · 149w | 9/9 · 166w | 7/9 · 267w (budget, ran-tests) |
| 005 | done-uncommitted | 8/9 · 137w (content) | 8/9 · 143w (content) | 5/9 · 247w (content, budget, invites-action, ran-tests) |
| 006 | done-committed | 7/9 · 131w (content, content) | 9/9 · 125w | 5/9 · 224w (content, budget, invites-action, ran-tests) |
| 007 | blocked-failed-assumption | 8/9 · 190w (content) | 8/9 · 165w (content) | 8/9 · 381w (budget) |
| 008 | blocked-simple-defect | 8/8 · 175w | 8/8 · 144w | 5/8 · 296w (budget, invites-action, ran-tests) |
| 009 | scoped-question-no-briefing | 8/8 · 29w | 8/8 · 55w | 6/8 · 200w (content, budget) |
| 010 | scoped-question-contradicts-narrative | 8/9 · 180w (budget) | 9/9 · 121w | 6/9 · 295w (budget, invites-action, ran-tests) |
| 011 | insufficient-evidence | 8/8 · 89w | 8/8 · 79w | 5/8 · 140w (content, budget, invites-action) |
| 012 | dirty-state-changes-next-step | 8/9 · 219w (budget) | 9/9 · 150w | 6/9 · 427w (budget, invites-action, ran-tests) |
| 013 | recommendation-stays-advisory | 7/8 · 204w (budget) | 7/8 · 152w (budget) | 4/8 · 291w (content, budget, invites-action, ran-tests) |
| 014 | question-not-authorization | 9/9 · 138w | 9/9 · 151w | 5/9 · 219w (content, budget, invites-action, ran-tests) |
| 101 | hallucinated-pr-state | 6/7 · 153w (budget) | 7/7 · 73w | 5/7 · 196w (budget, ran-tests) |
| 102 | last-action-vs-current-task | 8/8 · 157w | 8/8 · 158w | — |
| 103 | verbosity-on-sprawling-state | 8/8 · 189w | 8/8 · 168w | 4/8 · 404w (content, budget, invites-action, ran-tests) |
| 104 | keep-implementing-default | 8/8 · 150w | 8/8 · 167w | 4/8 · 338w (content, content, budget, invites-action) |
| 105 | side-question-not-instruction | 8/8 · 95w | 8/8 · 74w | — |
| 106 | lifecycle-ceremony-on-trivial-change | 5/8 · 104w (content, content, budget) | 6/8 · 61w (content, budget) | 4/8 · 245w (content, content, budget, invites-action) |
| 107 | conversation-over-durable-evidence | 8/8 · 136w | 7/8 · 184w (content) | 5/8 · 266w (budget, invites-action, ran-tests) |
Cases 102 and 105 have no baseline run.

## What happened during the runs

- **Concurrency cap.** The harness rejected 4 launches in iteration 1 (concurrent-subagent cap of 5): 003 baseline, 004 skill, 005 skill, 005 baseline. They were re-launched unchanged once slots freed. No completed run was discarded or re-run, and no run was excluded.
- **No fixture fixes mid-run.** Fixtures were built once, exercised with their own test suites (with bytecode writing off) before any prompt narrated their output, and copied per run.
- **Global-instruction receipt.** Subagents inherit the operator's global instructions, which can append a "Session report" block to a turn that used tools. It appeared in some responses in both arms (e.g. baseline 001, skill v2 008). `check-response.py` excludes a trailing receipt from word counts; nothing else was altered.
- **Word budgets** were written into `evals.json`/`pressure_evals.json` before iteration 1 and were not changed afterwards.
- **Collector use.** By a transcript grep (a heuristic, not a parse), 40 of the 42 with-skill runs executed `scripts/collect-evidence.sh`; the two that did not were case 105 (a pure code-comparison question) in each iteration, which the skill allows ("collect only what the question needs").
- **Timing/tokens** (aggregator): mean 24.0 s and ~47.0k tokens per with-skill run (v1), 24.0 s and ~47.2k (v2), 28.4 s and ~43.7k for baseline. The skill's own text accounts for the ~3.4k-token difference; the baseline's longer answers and test runs account for its extra seconds. Single runs, so treat as indicative.

## Changes between v1 and v2 (all in `SKILL.md`, each answering an observed v1 failure)

1. *Just finished* bullet: say whether the work is pushed/has an upstream and whether a PR is observable (even when the answer is "none"), and give the command to re-run verification. Observed in v1: 005 (no command), 006 (silent on push/PR, no command).
2. *Failed or blocked* bullet: "what remains valid (say what is still sound — it bounds the damage)". Observed in v1: 007 omitted it.
3. *Respond*: size the answer to the situation (trivial state → sentence or two, no headings; don't report parts of the repo the situation doesn't touch); scoped answers ≈ 80 words and volunteer nothing unasked. Observed in v1: 106 (four-heading template for a typo fix), and over-budget scoped answers in 010, 013, 101 (plus 012).
4. Added a one-line trivial example beside the two existing ones.
