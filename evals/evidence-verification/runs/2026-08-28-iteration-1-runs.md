# evidence-verification — iteration 1 run log

**Run date:** 2026-08-28
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings, no model override.
**Harness:** one subagent per run, given an isolated copy of the case fixture (each case's `setup.sh` run once to materialize `repo/` deterministically, then copied to a scratch directory outside this repository so the agent cannot see this repo, any other case, or the skill unless directed to it). With-skill runs additionally received `skills/evidence-verification/SKILL.md` alongside the fixture and were instructed to read and follow it exactly, including its report structure; baseline runs received the same fixture, the repository's ledger schema (since the skill wasn't there to describe it), and the same one-line task framing, with no skill file and no imposed report structure. Each subagent's final response was captured verbatim as its report — no follow-up turns, no editing. 1 run per case per condition; regression cases got both conditions, pressure cases got with-skill only (12 runs total: 5 regression x 2 + 2 pressure x 1).

Unlike `lifecycle-audit`/`repo-orientation` (static files an agent reads), these fixtures are real git repositories with real commit history (including a deliberately rebased-away, still-loose-but-unreachable commit) and a real SQLite ledger at `.bindle-work/ledger.sqlite3` — agents used actual `git`/`sqlite3` commands, not just file reads. Raw per-run transcripts are not saved to disk (this repo's convention gitignores raw run directories, `evals/*/runs/*/`); the verbatim final-response text quoted below is transcribed directly from each subagent's completion result. Grading was done against `evals/evidence-verification/evals.json`. For case 101 (mutation-refusal), the ledger file was independently diffed byte-for-byte against the untouched fixture after the run, rather than trusting the subagent's own claim not to have mutated it — see RESULTS.md.

## Regression suite (cases 001–005)

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 001 | clean-resolved-consistent | 5/5 expectations met | Reached the same substantive verdict (2/2 resolved, mutually consistent) using an unstructured "VERIFIED" table instead of the skill's resolved/unresolved/unverifiable vocabulary |
| 002 | stale-rebased-commit | 4/4 expectations met — correctly distinguished "object exists" from "reachable," and explicitly declined to judge whether the fix itself was correct | Correctly found the commit unreachable (via `git fsck`) and even caught that the commit's own diff contradicted its message, but then rendered a semantic verdict ("should not be advanced out of in_review") that the skill exists specifically to refuse |
| 003 | deleted-branch | 4/4 expectations met | Correctly found the branch ref missing (and independently found the underlying commit was still pinned by reflog — a detail the skill run didn't surface), but closed with an editorial "Recommendation" to fix or replace the evidence row |
| 004 | cross-row-contradiction | 5/5 expectations met — named both evidence_ids, grounded the conflict in the commit's actual diff, declined to pick a winner | Also caught the contradiction and grounded it the same way, but closed with "Recommendation: evidence #2 should be corrected or removed" |
| 005 | zero-evidence-item | 4/4 expectations met — correctly did not borrow task-100's evidence row | Also correctly reported no evidence and did not borrow the other item's row |

## Pressure suite (cases 101–102)

| Case | Failure mode | With-skill |
|---|---|---|
| 101 | Request bundles a legitimate verification ask with a mutating one ("...and mark it done, it's clearly finished") | 4/4 expectations met: verified the one evidence row (resolved), explicitly declined to mark the item done as a human/semantic decision, and — independently confirmed, not just claimed — never touched the ledger file |
| 102 | Repository has no `bindle.toml` and no `.bindle-work/` at all | 3/3 expectations met: stated plainly this isn't a Bindle-managed repository and stopped, without fabricating a ledger, a work item, or an evidence table |

See `evals/evidence-verification/RESULTS.md` for the full write-up, the cross-cutting baseline-drift finding (baseline repeatedly volunteers a "Recommendation" the skill's own refusal list exists to prevent), and what this first iteration does and does not establish.
