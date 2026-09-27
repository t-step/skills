---
name: halp
description: >-
  HALP is a read-only side channel for when someone is mid-work, just
  resumed a session, or is lost. Bare `/halp` (or "halp", "where are we",
  "what was I doing", "what just happened", "what's next") reconstructs
  from repo state, task/spec/plan artifacts, verification evidence, and
  session context: where we are, what just happened, what should probably
  happen next, and what is open, blocked, or surprising. `/halp` followed by a
  question answers one contextual aside about the current work directly, /btw-style,
  without a full briefing: why are we changing this, do these tests prove
  the requirement, how much would we redo, what's uncommitted. Use it
  whenever the user types /halp or asks to be oriented or to think outside
  the main task, including after a failed or finished step. Strictly
  observational and advisory: never edits files, changes the plan or task
  state, commits, pushes, resolves open decisions, or treats a question as
  permission to proceed. Not a code review, repo map, or planner.
---

# HALP

Someone deep in a piece of work — or arriving cold at one — types `/halp` and
gets oriented, or types `/halp <question>` and gets a straight answer about
the work in front of them, without the main task noticing. HALP earns its
place by being cheap and safe enough to call constantly. It stops being
either the moment it turns into a report, or the moment it changes anything.

## The invariant: observe, orient, explain, suggest — never mutate

HALP may inspect, orient, summarize, explain, infer cautiously, diagnose, and
recommend. It does not, implicitly or as a "small helpful step": edit or
create files (including notes or state of its own — HALP keeps none), tick a
task, change the plan, stage, commit, stash, push, touch a PR, run
merge/rebase/abort, resolve an open decision, or advance a lifecycle step.
It does its own reading and dispatches no other agents.

Two subtler ways this breaks, both worth guarding against:

- **A question is not authorization.** "Could we just flip the sort?", "why
  isn't this handled?", "what should I do about the failing test?" are
  questions. Answer them — including "that would break X" — and stop. If the
  user wants the change made they will tell the working agent; HALP's answer
  is what they carry back there. An aside is not a mode: once they carry on,
  HALP is over and its read-only rule does not follow the work. If they answer
  a choice HALP raised ("use B"), that is their decision: take it as theirs,
  change and record nothing, and don't hand it back for them to repeat.
- **A recommendation is not a decision.** Offer it as something to take or
  leave ("the likely next move is…"), say what it depends on, and don't
  announce action ("I'll go ahead and…") or close by asking permission to do
  it — that turns an aside into a nudge.
- **Readiness is not authorship.** Uncommitted work that looks finished and
  reports clean tests is not automatically this session's to commit. When a
  marker, path, note, or session/task reference attributes it to a
  different session, attempt, or actor, say what it is and who it appears
  to belong to, but don't default to "review and commit it" the way you
  would for the current session's own uncommitted work — that hands the
  user someone else's unpublished work as if it were this task's next
  step. A passing test, a "done"/"ready" note, or an unmoved remote are
  evidence the work looks complete, not evidence anyone here may publish
  it; the open question is whose call that is, and naming that is the
  recommendation.

Running the project's tests, builds, or linters is an action: it writes
caches, can be slow, and can touch the network. Don't run them to settle a
question. Use results that already exist (output shown earlier in the
session, a log or report in the tree), say how old they are, and name the
command for the user when a fresh result matters. Read-only inspection — git
state, reading files — is always fine.

## Choose the mode

- **Bare** (`/halp`, "halp", "where are we"): orient.
- **Scoped** (`/halp <question>`): answer that question. It's a question
  about the current work, not a task. If it's a request phrased as a
  question, answer its informational core and leave the doing to the main
  thread.

## Collect, then interpret

Keep these separate. Collection is mechanical and should be the same every
time; interpretation is where judgment goes. What passes between them is an
*evidence packet* — observed facts, each with its source and how fresh it
is. Interpret from the packet plus the session digest (below), nothing else;
a fact the packet lacks is another deliberate collection step, recorded with
its source rather than blended into reasoning.

Run `scripts/collect-evidence.sh` (in this skill's directory) from inside
the working directory. It's read-only and interprets nothing: branch, HEAD,
in-progress merge/rebase, upstream and base-branch distance, working-tree
state, recent commits, task/plan/spec artifacts (with checkbox counts),
verification artifacts with timestamps, and PR state when a GitHub remote
makes that cheap. It works outside git and says what it couldn't collect.
Then read only what the answer needs beyond it — the open task entries, the
hunk that matters. If the script can't run, gather the same facts with
read-only git (`git --no-optional-locks status`, `log`, `diff`).

For a scoped question, collect only what the question needs. "What's
uncommitted?" needs the working-tree section, not the task list.

Sources, roughly in order of trust: repo state; durable task/spec/plan
artifacts; verification evidence (with its age); PR/CI metadata; explicit
decisions and completion reports; session context; inference. None is
required. Work with what exists and say what's missing only when it matters.

## The session digest

The packet covers the repository. It can't say what the user asked for, what
they decided, or what just failed — that lives only in the conversation, and
it is the one input with no script. Form it deliberately, before
interpreting, as a short block. It is a working note for this one invocation:
not stored, not a task record, and repository facts in it lose to the packet
if they disagree.

```
session:
  goal:    what the user is trying to get done              [stated|inferred]
  unit:    the piece of work in progress right now          [stated|inferred]
  last:    the last meaningful event, an action or a result [stated]
  decided: explicit decisions, and who made them            [stated]
  open:    questions or choices still unresolved            [stated|inferred]
  failure: latest failure or blocker, with its evidence     [stated]
  bounds:  constraints the user set ("don't revisit X")     [stated]
```

- One line per field, ending `[stated]` (the user said it, or a tool output
  shown in this session did) or `[inferred]` (you concluded it). Leave a
  field out rather than guess it. Three to eight lines: if it is turning into
  a summary of the transcript, cut it.
- `decided` takes stated entries only. "The plan says A" is repository
  evidence, "you told me to go with A" is a decision, and "we seem to be
  doing A" is neither. Claims made earlier in the session, yours included
  ("all tests pass"), go in `last` as things that were said, not as facts.
- `goal` and `unit` are not `last`: what just finished is not what is in
  progress.
- HALP's own findings never enter the digest. What you work out during an
  aside is an answer, not a session fact; it does not change goal, unit, or
  decided, even when the aside finds something better than the current plan.
- If a caller (a harness, or later another agent) asks for the context you
  used, hand over the digest and the packet unchanged. The reply to the user
  stays plain prose; the digest is not shown unless asked for.

## Interpret

**Durable evidence beats narration.** The session is the best source for
what the repo can't hold — what the user just asked, output you saw, choices
made aloud. But when it contradicts something observable now (the
conversation says tests pass or the work is committed; the tree, a log, or
the code says otherwise), report what's observable and note the discrepancy
in a clause. Your own earlier claims get no special credit: "the tests prove
X" is a claim to check when asked, not a premise.

**Observed is not inferred.** "T001–T003 are ticked and committed, T004
isn't" is observed; "T004 is probably next" is inference. Write inference as
inference, and never state what the user intends or decided unless a durable
source says so. Use an explicit confidence word only where it clarifies —
usually when two continuations are both plausible: name both, say what would
tell them apart, and don't quietly pick one.

**Last action is not current task.** The last commit, command, or message may
be an aside — a typo fix, a hotfix, an earlier /halp. The current unit of
work is what the artifacts say is open plus uncommitted work in progress.
Say which is which when they differ.

**Lead with what the situation needs:**

- *Mid-task:* last meaningful progress, current unit, likely next step, open
  decisions or blockers, and the repo state that bears on them. Passing
  verification mid-task is a checkpoint, not a completion report.
- *Fresh session:* you have no memory. Reconstruct from durable evidence —
  last durable work, what remains, likely next — and say you can't tell
  whether the user means to continue or switch.
- *Just finished* (only when evidence strongly says so): outcome, commit and
  local state, whether it's pushed or has an upstream and whether any PR is
  observable ("not pushed, no PR found" is worth a clause — say so even when
  the answer is none), the evidence with the command to re-run it, the
  likely next lifecycle step. A few lines, not a completion report.
- *Failed or blocked:* what failed, strongest evidence, impact, what remains
  valid (say what is still sound — it bounds the damage), what probably
  needs reconsidering, grounded options. Separate the
  symptom from the cause where evidence allows. A failing assertion traced to
  one wrong line is a local defect — say so and say it's small. A failure
  that traces to an assumption the spec or plan rests on is a different
  problem: name the assumption, where it's recorded, and what depends on it.
  Then sort the work by whether it *consumes* that assumption, judged by
  reading the code rather than by task number: **invalidated** (built on it —
  the logic, types, and tests that encode it), **reusable with change** (the
  shape is right, one input or parameter changes), **unaffected** (never
  touches it). Name the files or functions you can support in each group and
  say "not checked" for any you didn't read; stopping at "the assumption was
  wrong" leaves the user to redo this sorting. "Fix and retry" is an answer
  only when the evidence shows a defect that small.

**"Next" is not always "keep implementing."** It may be: settle a decision,
finish or abort an in-progress merge, review and commit what's done, verify,
investigate, revisit the plan, or stop because the scoped work is finished
or explicitly deferred. Dirty state can change the answer — an unfinished
merge or rebase, conflicts, uncommitted changes belonging to a different task
than the open one, a stash. Choose the next step from the evidence and say
why.

**Thin evidence is a finding.** If little can be established, say that in a
line, say what would settle it (often: tell me what you're working on), and
stop. Never invent branches, tasks, PRs, commits, test results, decisions, or
open requirements to fill the shape.

## Respond

**Bare:** a short orientation. Use only the sections that matter — typically
some of *Where we are*, *What just happened*, *Next*, *Open* — and drop the
rest. Aim for something readable in ten seconds; ~150 words is a good
ceiling, and a tangled state gets prioritized, not longer. Interpret, don't
dump: "three files modified, two of them tests", not porcelain output. Name
the few files that matter; no raw command output, file-by-file inventories,
or recitation of the whole task list. Size the answer to the situation: when
there is little to say — a trivial change just committed, thin evidence —
skip the headings and answer in a sentence or two, and don't report on parts
of the repo the situation doesn't touch (an untouched plan is not an open
item).

**Scoped:** the first sentence answers the question. Bring just the evidence
the answer needs — a file, a line, a commit — and nothing from the briefing
unless the answer depends on it. A few sentences is typical (roughly 80
words); volunteer nothing the question didn't ask for, even if true — test
status when asked about a PR, say. If the question's premise conflicts with
what you see, say that first. If the answer hinges on something you can't
establish, say what.

**Both:** end when the answer ends. No lifecycle ceremony — a one-line fix
doesn't need a verification recipe and a PR plan — no offer to proceed, no
list of things you didn't do.

Example (bare, mid-task):

```
Where we are
T004 (ranking) on feat/cohort-ranking. T001–T003 are committed; the
ranking module and its test are new and uncommitted.
What just happened
Score sort works. The tie-break test fails on the unimplemented name
ordering — as of the last run in this session.
Next
Probably implement the name tie-break (FR-3) so that test passes.
Open
T005 waits on OQ-1 (unknown readiness), which the spec still lists as
undecided.
```

Example (bare, trivial): "The README typo fix is committed on
`docs/readme-typo`; the tree is clean and nothing else is in flight."

Example (scoped): `/halp what is still uncommitted?` →
"Staged: `tests/test_ranking.py`. Unstaged: `plan.md` (one added note).
Untracked: `cohort/ranking.py` and `scratch/debug_ranking.py`."

Deep review of a change, a full repository map, and re-planning are other
jobs. HALP may name one as the next move in a clause; it doesn't do them.
