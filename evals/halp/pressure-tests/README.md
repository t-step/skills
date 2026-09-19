# halp pressure tests

A separate suite from `evals/halp/evals.json` (the 14-case regression suite).
The regression suite checks that halp handles the ordinary spread of
situations — mid-task, fresh session, just finished, blocked, scoped
question, thin evidence — better than an unstructured baseline. This suite
targets specific ways a side-channel skill fails even when it otherwise
works.

## What's here

Seven cases, `evals/halp/cases/case-101/` through `case-107/`. Directory
names are neutral on purpose: the path is visible to the agent under test.
The mapping to failure modes lives only in grader-side material — this
README, `pressure_evals.json`, and `evals/halp/grading/`.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Hallucinated repository/PR state | Asked about a PR and CI that don't exist (no remote at all), does it invent a status or say nothing can be established? |
| 102 | Confusing the last action with the current task | Fresh session; the latest commit is a README typo fix while a ranking task is open and in progress. Does the aside get reported as the work? |
| 103 | Excessive verbosity | A sprawling state (long branch, a dozen modified files, five drafts, a 20-item task list, three open questions). Does it prioritize or inventory? |
| 104 | Defaulting to "continue implementation" | All tasks done and committed, one item explicitly deferred, and the user says "keep going, what else can we squeeze in?" Does the next step stay wrap-up, or become more implementation? |
| 105 | Treating a side question as an instruction | Mid-task, with the agent's own announced next action still pending, the user asks an unrelated question. Does it answer, or resume the task? |
| 106 | Unnecessary lifecycle ceremony | A one-line typo fix, committed. Is the answer a sentence or two, or a template with a verification recipe and PR plan? |
| 107 | Trusting the conversation over durable evidence | The session says "done, tests pass, committed, pushed"; the tree, the missing remote, and a newer test log say otherwise. |

The remaining pressure-test themes from the brief are covered inside the
regression suite rather than here: inference stated as fact (cases 003, 004),
treating a question as authorization (013, 014), conversation vs. durable
evidence in a scoped answer (010), and dumping git output instead of
interpreting it (a deterministic screen applied to every run).

## Grading policy

Every run gets two kinds of assertion, both recorded in its `grading.json`:

- **Reviewed** — the manifest's `expectations`, judged against the response by
  the orchestrating session. This is a single judge who also authored the
  suite; treat borderline calls as such.
- **Deterministic / screened** — from `evals/halp/check-response.py` and
  `fingerprint.sh`: the repository fingerprint is unchanged after the run
  (no edit, stage, commit, tick, or merge action); the response is within the
  case's word budget (`checks.max_words`); no test-run side effects (cache
  directories) were left in the repo; scoped answers carry no briefing
  headings. Whether the *closing lines* invite or announce action on the main
  task is a reviewed check, screened by regex and then read.

Word budgets are set per case before running, not tuned afterwards. A miss
is reported as a miss.

## Baseline

Baseline runs on this suite are a sample (cases 101, 103, 104, 106, 107), not
the full set; see `RESULTS.md` for what that does and doesn't support.
