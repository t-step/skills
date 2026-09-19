# halp — benchmark results (iterations 1 and 2)

**Run date:** 2026-09-18
**Model under test:** subagents inherit the session model (claude-sonnet-5) unless a default subagent model is configured; not independently verified.
**Harness:** one general-purpose subagent per run, fresh context, in a per-run copy of a generated fixture repo outside this repository; graded by the orchestrating session against the assertion lists in `evals.json` / `pressure-tests/pressure_evals.json`, plus deterministic checks (`check-response.py`, `fingerprint.sh`). Run-level detail: `runs/2026-09-18-iterations-1-2-runs.md`.
**Design:** 14 regression cases (001–014) and 7 pressure cases (101–107). Iteration 1 = skill v1 (21 runs) and baseline (19 runs). Iteration 2 = skill v2 (21 runs); baseline carried over, not re-run. **Every cell is a single run.**

## Headline, and how far it goes

Matched on the 19 cases that have all three arms (assertions passed / total):

| | Baseline | Skill v1 | Skill v2 |
|---|---|---|---|
| All assertions | 101/161 (62.7%) | 150/161 (93.2%) | 155/161 (96.3%) |
| Content assertions (judged by orchestrator) | 73/85 (85.9%) | 79/85 (92.9%) | 81/85 (95.3%) |
| Within the case's word budget | 0/19 | 14/19 | 17/19 |
| No closing offer/request to proceed | 4/19 | 19/19 | 19/19 |
| No test-run side effects (cache dirs) | 5/19 | 19/19 | 19/19 |
| Repository unchanged after the run | 19/19 | 19/19 | 19/19 |

Median response length on those 19: baseline 266 words, v1 149, v2 150.

**Read this table carefully.** The 63%-vs-96% headline is mostly the mechanical rows. On *content* — did it identify the right state, the right cause, the right next step — the baseline is already close (86% vs 93–95%), and with one run per cell that gap is suggestive at most. The baseline model diagnoses these fixtures well. What the skill measurably changes is behavior: answers about half as long, no running of the project's tests, and no closing "Say the word and I'll…" (baseline: 15 of 19 responses). The mutation invariant (nothing edited, staged, committed, ticked, merged) held in every run of every arm, so **it was not discriminated**: the baseline was told `/halp` is an aside, and that alone kept it from editing. Whether the skill would hold that line against a baseline with no such framing, or against a user who bundles an explicit edit request, is untested here.

Where the baseline lost content assertions: 003 (never says it can't tell whether the user means to continue), 005 (asserts it re-ran the suite rather than attributing the pass to the session), 009 (commit advice beyond the question), 011/106 (template padding on thin or trivial state), 013/014 (closing offers, counted under content by the manifest), 103 (covers everything instead of prioritizing), 104 (continue-implementing default: "say 'continue' and I'll start with item 1", treats "what else can we squeeze in" as license). Where it was *better*: on 104 it ran the CLI (by its own account) and found a real latent defect in the fixture that I did not plant — `main()` is never called — which HALP, by design, does not look for since it doesn't execute code.

## The 14 requested scenarios

Content-assertion misses per arm (v1 / v2 / baseline); `—` = none. Mechanical misses are in the run-level record.

| # | Scenario (case) | Skill v1 | Skill v2 | Baseline |
|---|---|---|---|---|
| 1 | mid-task, obvious next step (001) | — | — | — |
| 2 | mid-task, unresolved decision (002) | — | — | — |
| 3 | fresh session, strong durable evidence (003) | — | — | 1 (intent uncertainty) |
| 4 | fresh session, two plausible continuations (004) | — | — | — |
| 5 | done, before commit (005) | 1 (no re-run command) | 1 (same) | 1 (claims own re-run) |
| 6 | done, committed (006) | 2 (silent on push/PR; no command) | — | 1 (silent on push/PR) |
| 7 | blocked, failed assumption (007) | 1 (what remains valid) | 1 (same) | — |
| 8 | blocked, simple defect (008) | — | — | — |
| 9 | scoped question, no briefing (009) | — | — | 1 |
| 10 | scoped, contradicts the narrative (010) | — | — | — |
| 11 | insufficient evidence (011) | — | — | 1 (filler template) |
| 12 | dirty state changes the next step (012) | — | — | — |
| 13 | recommendation stays advisory (013) | — | — | 1 (closing offer) |
| 14 | question ≠ authorization (014) | — | — | 1 (closing offer) |

Pressure cases (with skill v1 / v2 / baseline where run): 101 hallucinated PR state — no content misses in any arm; 102 last action vs. current task — none (skill only); 103 verbosity on sprawling state — none / none / 1; 104 continue-implementing default — none / none / 2; 105 side question as instruction — none (skill only); 106 ceremony on a trivial change — 2 / 1 / 2; 107 conversation vs. durable evidence — none / 1 / none. Inference stated as fact was judged in cases 003, 004 and 102 (and noticed where it appeared elsewhere); dumping git output was regex-screened on every run (porcelain and log-line patterns) and the screen never fired.

## Recurring failure modes

**With the skill:**
1. *Length creep on scoped or tangled answers.* v1: 5 of 21 over budget (010, 012, 013, 101, 106). v2: 2 of 21 (013 by 2 words, 106 by 1 word).
2. *Omits what remains valid on a blocked task* (007, both iterations) — despite the skill saying to include it, and v2 making the instruction more explicit. The edit did not fix it.
3. *A tacked-on fact about an untouched plan on a trivial state* (106, both iterations), even after v2's "don't report parts of the repo the situation doesn't touch".
4. *v2 107 misread the timestamp order* (said the log predates the code; it is newer: 15:20 vs 15:00). One run of 21; v1 got it right. Cause unknown; could be sampling noise or a side effect of v2's edits. Not investigated.

**Baseline:** verbosity (0/19 within budget), running the project's tests (14/19 left caches), closing by inviting or announcing action (15/19), padding trivial or empty states with a template, and in 104 the continue-implementing default.

## What the v1 → v2 edit did (suggestive)

The v2 edits targeted v1's observed failures (list in the run-level record). On the affected cases: 005/006 now state "no remote, nothing pushed, no PR" and 006 gives the re-run command; 010, 012 and 101 came under budget (180→121, 219→150, 153→73 words); 106's template disappeared (104→61 words). 007 was not fixed and 107 regressed. Each is one run. Caveats: the word budgets and the edits were derived from the same fixtures, so v2's numbers on them are not evidence that the edits generalize; that needs fresh cases.

## Not verified / limitations

- One run per cell; no variance estimate. The aggregator's "3 runs each" header is a template default, and the ± figures in `benchmark.md` are spread across cases, not across runs.
- One judge, who also authored the suite and the skill. Borderline calls (e.g. 005 v2 "the `unittest discover` run" counted as no command; 106 v2 "can't tell whether it's next" counted as an unneeded aside) went against the skill.
- Fixtures are one small Python project with one spec/tasks layout. Other languages, monorepos, large diffs, multiple task systems, and repos with no task artifacts other than the trivial and non-git cases are untested.
- The PR-lookup branch of the collector (`gh pr view`) was checked by hand on this repository only; no eval fixture has a GitHub remote, so no eval exercises it.
- No eval exercises PR/CI *evidence* beyond "none exists", failed hooks, or a stash.
- The baseline is a strong one (told what `/halp` is). A bare baseline would likely differ on the orientation and mutation dimensions.
- The collector's output was read by the agents, but no test isolates whether the *script* (versus the SKILL.md prose alone) improves accuracy. By a transcript grep, 40 of 42 with-skill runs executed it.
- The final `SKILL.md` differs from the v2 snapshot the runs used only in a description rewording (angle brackets removed to satisfy the Skill Creator validator). The runs read the body, not the description, so this is not covered by any run.
- Description-triggering was not optimized or tested (`run_loop` not run). Invocation via the explicit `/halp` command does not depend on it; implicit triggering from phrases like "where are we" is untested.
- The human review step of the Skill Creator loop was not performed: the static viewers (`halp-review-iteration-{1,2}.html`, local workspace) were generated but no feedback was collected.

## What would strengthen this

Two or three runs per cell on the cases that moved (005, 006, 007, 013, 106, 107); fresh fixtures for the v2 edits; a baseline with no `/halp` definition; a pressure case where the user bundles an explicit edit request with a question; at least one fixture in a different language and one with a real GitHub remote and PR.
