---
name: change-review
description: >-
  Reviews one bounded implementation change (a diff, PR, commit range, or
  "I finished X" claim) against its stated goal, repo instructions, the
  actual change content, and verification evidence you can point to.
  Produces exactly one verdict — Ready to merge, Ready after minor
  corrections, Not ready to merge, or Unable to verify — plus findings
  sorted into blocking / required corrections / non-blocking /
  out-of-scope. Use whenever you or another agent is about to say a change
  is "done", "ready", or "passing", before merging, or whenever someone
  asks for a review of a diff, PR, or commit. Exists to stop premature
  "looks good" verdicts: refuses to credit tests as passing unless their
  output was actually observed, and checks whether an old implementation a
  change claims to replace is still reachable. Judges this change on its
  own — not feature/milestone convergence, not evidence-pointer integrity,
  not domain/lifecycle/ownership semantics — see "How this composes."
---

# Change Review

A bounded implementation change — a diff, a PR, a commit or commit range —
reviewed on its own, not as a whole-codebase audit and not as a verdict on
whatever larger effort it belongs to. The habit this skill exists to break:
taking a clean-looking diff plus a claim of "tests pass" at face value.
Both the diff and the claim need to be checked against something, not just
read and nodded along to.

## How this composes with neighboring review questions

"Is this change good" is not one question. Before reviewing, be clear about
which of these you're actually being asked, because only one is this
skill's job:

- **Did the claimed evidence pointer actually resolve** (a cited commit
  still exists and is reachable, a cited PR contains what it's cited for,
  two evidence rows don't contradict each other)? That's mechanical
  evidence-pointer integrity — `evidence-verification` owns it for
  Bindle-tracked work items, checking the pointer without judging the
  change behind it. This skill's own "Verification evidence" requirement
  is different: it's about whether *you* observed test/command output
  showing the change behaves as claimed, not about whether a ledger
  pointer resolves. Use both together when both apply — a resolved
  pointer to a commit doesn't tell you the commit's logic is correct
  any more than a passing test suite does.
- **Has the larger feature, milestone, or work item converged** — is the
  work this change is part of actually finished? This skill never answers
  that. Its verdict is scoped to the change in front of it; a "Ready to
  merge" verdict here says nothing about whether other changes still need
  to land, whether acceptance criteria for the surrounding feature are
  met, or whether a human has signed off on the milestone. Don't read a
  positive verdict here as feature-complete, and don't withhold a verdict
  on this change because the larger effort obviously isn't done yet — the
  two questions are independent.
- **Does a mapping, name, or transition carry the meaning this change
  assumes it does?** When a finding's correctness turns on domain
  semantics, write authority, or lifecycle/transition rules this change
  touches, use what `domain-orientation`, `state-ownership-audit`, or
  `lifecycle-audit` have already established for this codebase if a
  report exists — reuse it as grounding rather than re-deriving it from
  scratch. If no such report exists and the ambiguity is genuinely about
  meaning or authority rather than about what this diff's own lines do,
  say the semantic question is open and point at the specialized audit
  that would settle it, rather than guessing an answer this skill isn't
  positioned to check.
- **Was this change reviewed against a specification before it was
  built?** That's a different, earlier question — `spec-pressure-test`
  runs before code exists; this skill runs after.
- **How should remaining work be grouped into delivery units?** That's
  `task-composition`, and it's upstream of this skill in a different
  sense: it decomposes not-yet-built work into agent-sized units before
  anyone writes a diff. This skill has no stake in how the change in
  front of it was sized or grouped — it reviews whatever change it's
  handed, whether that's one task's diff, several tasks' combined diff,
  or a hand-written change with no task behind it at all.

None of these are required invocations — this skill runs standalone on a
diff with nothing else available, exactly as before. Reuse another
report's findings when one already exists and bears on what you're
reviewing; don't block a review on fetching one that doesn't.

## Gather before judging

You need four things. If you don't have one, say so explicitly rather than
filling the gap with an assumption:

1. **The stated goal** — what this change was supposed to accomplish. If
   it's vague ("clean up the auth module"), don't invent a sharper goal to
   judge against; note the ambiguity instead.
2. **Repo instructions** — AGENTS.md/CLAUDE.md/CONTRIBUTING or equivalent,
   for the files actually touched. Skim for conventions the change might
   violate.
3. **The actual change** — read the real lines. Don't reconstruct what
   changed from the commit message, PR description, or a summary someone
   gives you — those describe intent, not necessarily what happened.
4. **Verification evidence** — command output you personally observed,
   either by running it yourself in this session or by being shown the
   actual output. A claim of "tests pass" in a commit message or PR body
   is not evidence; it's the same kind of claim you're being asked to
   check.

If (3) is missing and you have no way to obtain it, the verdict is **Unable
to verify** — you can't review a change you can't read. Missing (4) is
asymmetric: without observed verification evidence you may never issue a
positive verdict (Ready to merge / Ready after minor corrections), but it
does not stop a negative one. If the change itself demonstrates a concrete
blocking defect — a specific input or scenario you can point at that
produces wrong behavior — say **Not ready to merge** on that evidence
alone; don't retreat to "Unable to verify" when you have already proven a
failure. **Unable to verify** is for the remaining case: no observed
verification *and* nothing in the change you can demonstrate is broken.
Don't stretch thin evidence to reach a more decisive-sounding verdict in
either direction.

## Review the change itself

Read every changed line with the stated goal in hand. Two failure modes to
actively watch for, because they're the ones a quick read misses:

- **Passing tests, wrong behavior.** Tests can pass while missing the actual
  bug — wrong edge case, untested branch, a mocked dependency that hides the
  real failure. Passing test output tells you the tests the author thought
  to write don't fail; it doesn't tell you the logic is correct. Read the
  logic itself, independent of what the test suite checks.
- **The old path is still reachable.** When a change's goal is to replace
  or retire an implementation, grep for remaining references to the thing
  being replaced — call sites, imports, exports, registered routes,
  feature flags, config toggles. "We added the new path" is not the same
  claim as "the old path is gone"; treat them as two separate things to
  verify, because a reachable dead-and-forgotten old path is one of the
  most common ways a change that looks finished isn't.

## Sort every finding into exactly one bucket

- **Blocking** — prevents the merge; the change cannot ship until it is
  resolved: a correctness bug, the stated goal not actually met, an old
  path still reachable, or a violated repo instruction whose fix requires
  rethinking the approach rather than adjusting a line. An unbacked
  critical claim (like "tests pass" with no output shown) is *not* by
  itself a blocking finding — it strips the evidence a positive verdict
  needs, and the verdict rules then decide: Not ready to merge if
  something is demonstrably broken, Unable to verify if nothing is.
- **Required corrections** — must be fixed before the change ships, but
  narrowly mechanical: the defect is precisely locatable, the fix is
  obvious, local, and low-risk (a wrong response format, a misnamed field,
  a missing required header), and it casts no doubt on whether the goal
  was met or the core logic is right. The test that separates this bucket
  from Blocking: can you write the exact corrected line(s) yourself in the
  review? If fixing it needs a decision, a design, or touching the
  verified logic, it's Blocking.
- **Non-blocking** — real, worth mentioning, doesn't hold up the merge and
  isn't required at all: style nits, minor inefficiencies, a TODO left
  behind.
- **Out-of-scope** — a real issue in code the change does *not* touch (a
  pre-existing bug nearby, a refactor opportunity in an untouched
  function). Name it so it isn't lost, but don't let it push the verdict
  toward "not ready" — that's how review scope creeps into demanding
  unrelated work. This bucket never applies to changes the diff itself
  introduces: an unrequested, unrelated change riding along inside the
  diff is a finding about this change (blocking, if it's untested or
  risky), not someone else's problem.

Two discipline checks before you finalize a finding:
- If it's **blocking** or a **required correction**, you should be able to
  point at a specific line and state the concrete requirement it violates
  or the input that breaks. "This could be cleaner" or "I'd have done this
  differently" is neither — if you can't articulate the failure or the
  violated requirement, it's non-blocking at most.
- If something looks wrong at first glance, check it against the
  surrounding context (types, call sites, existing tests, comments) before
  flagging it. Plenty of unusual-looking code is intentional; a false
  blocking finding costs the author real time chasing a non-problem.

## Choose the verdict

Exactly one, chosen by the findings above. Every verdict here is a
statement about this change alone — see "How this composes" above for what
it deliberately doesn't claim about the surrounding feature or milestone:

- **Ready to merge** — goal is met, no blocking findings and no required
  corrections, and you have observed verification evidence that supports
  it.
- **Ready after minor corrections** — goal is met, no blocking findings,
  and observed verification evidence supports the core behavior; what
  remains is one or more required corrections (the mechanical bucket
  above). By construction this verdict never contains a blocking finding
  — if a finding blocks, the verdict is Not ready to merge.
- **Not ready to merge** — at least one blocking finding: unmet goal,
  correctness bug, reachable old path, or a violated repo instruction.
  Change evidence alone is sufficient when it demonstrates a specific,
  concrete failure — you do not need verification output to block on a
  defect you can prove by reading the change.
- **Unable to verify** — you don't have enough to reach one of the above:
  no change to read, or no observed verification evidence *and* no defect
  you can concretely demonstrate from the change, or a goal too ambiguous
  to judge against. This is a legitimate verdict, not a failure to finish
  the review — reaching it honestly is better than guessing toward a more
  confident-sounding one.

## Report

```
# Change Review: <goal or change name>

**Verdict:** <one of the four, verbatim>

## Blocking
- <finding, with file/line if applicable>

## Required corrections
- <finding, with the exact corrected line(s) where possible>

## Non-blocking
- <finding>

## Out of scope
- <finding>

## Verification evidence
<Exactly what you ran/observed and its result. If you didn't observe any,
say so plainly — do not imply verification happened.>

## Reasoning
<Short paragraph connecting the findings above to the verdict.>
```

Leave a bucket's body as "None." rather than omitting the heading — an
absent section reads as "not checked," not "nothing found."
