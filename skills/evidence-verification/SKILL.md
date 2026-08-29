---
name: evidence-verification
description: >-
  Mechanically verifies evidence attached to a Bindle work item -- a
  commit, branch, pull request, or other pointer in Bindle's SQLite work
  ledger -- against actual repo/git state before anyone trusts a "done"
  claim. Checks whether each pointer still resolves, is stale after a
  rebase/force-push, or contradicts another evidence row -- reports
  resolved/unresolved/unverifiable per row plus a fraction, never a
  rounded-up verdict. Use whenever asked to verify evidence, sanity-check
  a `bindle milestone review`/`bindle work` output, or before
  accepting/declining a milestone -- even phrased as "does this evidence
  hold up" without naming Bindle. Refuses to judge implementation
  correctness/completeness/architecture (human territory) and never
  marks anything done or edits an evidence row.
---

# Evidence Verification (Bindle)

Bindle verifies mechanical evidence. Humans resolve semantic uncertainty.

Bindle's work ledger lets someone attach evidence to a work item -- a
commit SHA, a branch name, a pull request number, a free-text note -- and
lets a milestone reviewer see that evidence before accepting the work.
But recording a pointer and the pointer being *true* are different
things: Bindle's own ledger records evidence as a flat, append-only,
content-blind table -- a `commit` row is validated only by a `CHECK
(kind IN ('branch','commit','pull_request','other'))`, never against
whether that commit still exists. Nothing stops someone from citing a
commit that's since been rebased away, a branch that's been deleted, or
a PR that never contained the change it's cited for. The milestone
reviewer is being asked to trust unverified pointers.

This skill's only job: for a given work item, determine what can be
**mechanically** established about its evidence from the current
repository and ledger state, and report that -- plainly, per-row, without
rounding up. It does not decide whether the work itself is good. A
passing check establishes that the check passes, not that the
requirement is satisfied; a resolved commit establishes that a change
happened, not that it was the right change.

## Ground first

1. **Confirm you're looking at a Bindle-managed repo** (a `bindle.toml`
   at the repo root, or a `.bindle-work/` directory). If neither exists,
   say so and stop -- there is nothing to verify.
2. **Everything you do here is read-only.** Never run a Bindle command
   that mutates ledger state (`claim`, `release`, `done`,
   `enter-review`, `accept`, `decline`) and never open the ledger for
   writing. If the task also asks you to act on the result ("verify this
   and mark it done"), perform and report the verification, then refuse
   the mutating step and say plainly that a human decision belongs
   there -- don't silently drop the mutation request or silently perform
   it.
3. **Identify the work item and load its evidence.** For a milestone,
   `bindle milestone review <id>` already surfaces per-child status,
   evidence, and blocked state -- read that first rather than
   re-deriving it. For a task, or for evidence detail the CLI doesn't
   expose (there is currently no `bindle work evidence list` command),
   read Bindle's SQLite ledger directly, **read-only**
   (`.bindle-work/ledger.sqlite3` at the Git common directory, unless
   the repo's own tooling reports a different path -- don't assume,
   confirm), using something like:
   ```
   sqlite3 -readonly .bindle-work/ledger.sqlite3 \
     "SELECT evidence_id, kind, value, note, recorded_at
      FROM work_item_evidence WHERE work_item_id = '<id>';"
   ```
   As of Bindle's current schema, `kind` is one of `branch`, `commit`,
   `pull_request`, `other`. If a query against these table/column names
   fails, run `.schema work_item_evidence` and trust what you see over
   this document -- Bindle's own tracked ledger is authoritative, this
   skill's description of it is not.

## Classify every claim before you check it

Don't let a check answer a bigger question than it actually can. Sort
each thing you're being asked about into exactly one bucket:

- **Mechanical fact** -- independently reproducible right now: a named
  file exists (at HEAD or at a cited commit); a cited commit touched a
  named file; a named function/class/test is actually defined where
  claimed; a named command, re-run, exits with a given code; a
  commit/branch/PR resolves; a row already in the ledger says what it
  says; two evidence rows assert facts that can't both be true.
- **Derived mechanical conclusion** -- follows deterministically from
  mechanical facts, still not a quality judgment: "this pointer doesn't
  resolve," "this commit's diff doesn't touch the file the note claims
  it fixed," "all evidence on this item resolves and is mutually
  consistent." That last one is a statement about corroboration, not
  correctness -- never write "verified" when you mean "the pointers
  check out."
- **Semantic claim** -- always out of scope here: whether the change is
  architecturally right, whether a passing test means the requirement is
  met, whether the diff is complete, whether the evidence is
  *sufficient* for what's being claimed. If a request asks you to render
  one of these, say plainly that it's outside this skill and stop before
  answering it.
- **Unverifiable claim** -- the environment genuinely can't settle it:
  no network/API access to check a PR's state, a claim that requires
  credentials you must not touch, or a reference to a human judgment
  already made elsewhere with no artifact to check ("reviewed in
  Slack," "approved by the lead"). Unverifiable is not a euphemism for
  unresolved -- don't downgrade a claim you simply didn't try to check
  into "unverifiable"; only use it when no mechanical check applies at
  all.

## Check each evidence row

- **`commit`** -- first confirm the object exists (`git cat-file -e
  <sha>^{commit}`), then confirm it's actually reachable from some
  current ref, not just present as a dangling object
  (`git branch -a --contains <sha>` or `git rev-list --all | grep -qx
  <full-sha>`). A commit that still exists as a loose object after a
  rebase but is reachable from nothing is exactly the stale-evidence
  case this skill exists to catch -- a bare existence check alone would
  miss it.
- **`branch`** -- check the local ref
  (`git show-ref --verify --quiet refs/heads/<name>`) and, if the note
  or context implies a remote branch, the remote-tracking ref too. If
  checking the remote requires a fetch you weren't asked to perform,
  say the local-only result plainly rather than fetching unasked or
  assuming the remote matches.
- **`pull_request`** -- requires a forge API (e.g. `gh pr view <num>
  --json state,commits,mergeCommit` if `gh` is authenticated for this
  repo). No access is `unverifiable`, not `unresolved` -- you didn't
  find a problem, you couldn't look. If the PR's merged commit or
  commit list is available, cross-check it against any co-cited
  `commit` evidence on the same item.
- **`other`** -- free text. Extract only the sub-claims that are
  actually checkable (a named file, symbol, test, or command) and check
  those; the rest of the note is context, not a claim to adjudicate. If
  the note names a command someone claims they ran, treat "it was run
  and passed" as unverifiable by default -- re-running it yourself to
  reproduce the claim is a real, sometimes costly action, so only do it
  when you were explicitly asked to reproduce, and say clearly that
  that's what you're doing and why the result might differ (different
  working tree state, environment, timing).

## Cross-check evidence rows against each other

An item with more than one evidence row can have rows that individually
resolve but jointly contradict: a `pull_request` row and a `commit` row
where the cited commit was never part of that PR; a `commit` row and an
`other` row whose note names a file the commit's diff never touched.
Report the contradiction by naming both evidence rows and what
specifically conflicts. Do not pick a winner -- deciding which piece of
evidence is authoritative is exactly the semantic call this skill
doesn't make.

## Outcomes: three states, not five

Report each evidence row as exactly one of:

- **resolved** -- the pointer mechanically checks out.
- **unresolved** -- it doesn't, for any reason: it never existed, it
  existed and no longer resolves (stale), or it contradicts another row
  on the same item. These collapse into one state on purpose -- staleness
  and contradiction are different *reasons* a pointer failed a check,
  but they lead a human to the same next action ("don't trust this
  line, go look"), so the reason belongs in the finding's text, not in
  a separate top-level state that wouldn't change what anyone does next.
- **unverifiable** -- no mechanical check could be applied at all,
  whether because the environment lacks access or because the checker
  itself couldn't run. Both mean the same thing to a human reading the
  report: no mechanical answer was possible here, look yourself.

Resist the temptation to add more states back in ("stale" separate from
"contradicted," a fourth bucket for "the check errored"). More states
here would describe *why* something failed in more detail than the
report needs, at the cost of a taxonomy a reader has to learn before
they can act on it. If a specific case genuinely needs the extra detail,
put it in the row's reason text, not in a new top-level state.

## Never round up

State the item's evidence summary as a count, not a verdict: "3 of 4
evidence rows resolved; evidence_id=17 unresolved (branch deleted)" --
never "verified" or "evidence checks out" for the item as a whole when
any row didn't resolve. This applies even when Bindle's own readiness
gate (`is_review_ready` / the milestone's `review_ready` state) already
says yes -- that gate checks whether evidence *exists* for every child,
not whether it *resolves*. Your fraction is a second, independent data
point sitting alongside it, not a competing gate and not something that
overrides or blocks Bindle's own transition logic. If asked whether a
milestone is "ready," answer only for the evidence-mechanics question
this skill owns; point at `bindle milestone review` for the readiness
gate itself.

## What this skill refuses to do

Even when a request bundles it in:

- Decide whether the implementation is correct, complete, architecturally
  sound, or faithful to intent.
- Mark a task done, or accept/decline/claim/release a milestone or task.
- Add, edit, or delete an evidence row.
- Pick a winner when two evidence rows contradict -- report both and
  stop.
- Treat "no mechanical check exists for this yet" as license to guess an
  answer -- say unverifiable and move on.
- Silently re-run a command a piece of evidence merely references, or
  silently fetch a remote to check a branch, without being asked.
- Push a verification result into Bindle's Symphony projection or any
  other external surface -- nothing in Bindle's task-coordination
  projection carries an evidence field today, and inventing one is a
  design decision for a human, not a side effect of running this skill.
- Produce a single collapsed "this is good to merge/accept" signal. This
  skill's report is evidence for a human decision, never the decision.

If a request bundles a legitimate ask here with one of these -- "verify
the evidence and accept the milestone," "check this and mark it done" --
do the verification, report it fully, and say plainly that the rest is
a human call this skill won't make.

## Report

```
# Evidence Verification: <work item id / title>

## Item
<type (task/milestone), current status, and how it was located
(bindle milestone review output vs. direct ledger read)>

## Evidence checked
| evidence_id | kind | value | outcome | reason |
|---|---|---|---|---|
| ... | ... | ... | resolved / unresolved / unverifiable | <one line> |

## Cross-row consistency
<Any contradiction found, naming both evidence_ids and what conflicts.
"None found" if none -- that's a real, useful result, not an omission.>

## Summary
<n> of <total> resolved. <List unresolved and unverifiable rows by id.>
This is a statement about the evidence's mechanics, not about whether
the work itself is correct or complete.

## What remains for a human
<The specific decision(s) this report doesn't make: whether unresolved
or unverifiable evidence is acceptable to proceed on, how to resolve
any contradiction, and whether the underlying work actually satisfies
the requirement.>
```

Leave a section's body as "None found." rather than omitting the
heading -- an absent section reads as "not checked," not "nothing
found." A work item with no evidence rows at all is fully and honestly
reported by an empty table and a summary of "0 of 0 -- no evidence
recorded on this item."
