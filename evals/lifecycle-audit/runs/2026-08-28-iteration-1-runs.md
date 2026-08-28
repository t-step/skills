# lifecycle-audit — iteration 1 run log

**Run date:** 2026-08-28
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings, no model override.
**Harness:** one subagent per run, given only an isolated copy of the case fixture (its files copied to a scratch directory outside the repo so the agent cannot see this repository, any other case, or the skill unless directed to it). With-skill runs additionally received `skills/lifecycle-audit/SKILL.md` alongside the fixture and were instructed to read and follow it exactly, including its report structure; baseline runs received the same fixture and the same one-line task framing with no skill file and no imposed structure. Each subagent's final response was captured verbatim as its report — no follow-up turns, no editing. 1 run per case per condition (10 cases × 2 conditions = 20 runs total); this is a first iteration, not a repeated-sampling benchmark.

Raw outputs were saved verbatim under `evals/lifecycle-audit/runs/2026-08-28-iteration-1/case-<id>-{baseline,skill}.md` during grading (that directory is gitignored per `evals/*/runs/*/`, matching this repo's convention of not committing raw per-run transcripts). Grading was done against `evals/lifecycle-audit/evals.json` and `evals/lifecycle-audit/pressure-tests/pressure_evals.json`, cross-checked against the actual saved output files, not against a paraphrase — see `evals/lifecycle-audit/RESULTS.md` for the full write-up, the per-expectation grading detail, the interaction-taxonomy pressure-test findings, and the one eval-spec fix made after this run.

## Regression suite (cases 001–009)

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 001 | false-lifecycle-projection-and-cache | 5/5 expectations met (after one eval-spec key fix, see RESULTS.md) | Reached the same conclusion (one real lifecycle, two derived views) independently |
| 002 | one-way-trigger-mistaken-for-sync-need | 5/5 expectations met | Reached the same shape but hedged the "no sync field needed" conclusion as unresolved rather than stating it directly |
| 003 | transfer-conservation-genuine-reconciliation | 5/5 expectations met | Reached the same conclusion, independently found the same unreached-`RECONCILED`-state defect |
| 004 | cdc-index-lag-not-peer-sync | 5/5 expectations met | Reached the same conclusion, framed as "one lifecycle, two representations" |
| 005 | grace-window-and-cache-lag-both-tolerable | 5/5 expectations met | Reached the same two-way distinction and the same "alert is miscalibrated" conclusion |
| 006 | shared-vocabulary-different-lifecycles | 5/5 expectations met | Reached the same conclusion with equally concrete structural differences cited |
| 007 | underspecified-approval-ownership | 5/5 expectations met | Reached the same disciplined "mark it Unknown" outcome, carried the same open questions forward |
| 008 | recomputed-score-not-a-lifecycle | 5/5 expectations met | Reached the same conclusion and the same critique of the PR comment's broken analogy |
| 009 | shared-invariant-separately-owned | 5/5 expectations met | Reached the same conclusion, correctly separated "invariant held" from "retry gap still real" |

## Pressure suite (case 101)

| Case | Failure mode | With-skill | Baseline |
|---|---|---|---|
| 101 | A colleague, in-fixture, directly asks for a SyncCoordinator service and a `sync_status` field between a source lifecycle and its CDC-derived projection | 6/6 expectations met, cleanly, explicitly invoking the central principle | Also declined the request, independently, with a comparably strong alternative (source-version field + DLQ alerting + read-only reconciliation job) |

See `evals/lifecycle-audit/RESULTS.md` for the full write-up, including what this iteration does and does not establish, the interaction-taxonomy pressure test (cases 003 and 009), and why no `SKILL.md` change was made this iteration.
