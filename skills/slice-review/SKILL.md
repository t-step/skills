---
name: slice-review
description: >-
  Reviews one bounded implementation slice (a diff, PR, or "I finished X"
  claim) against its stated goal, the repo's own instructions, the actual
  diff content, and verification evidence you can point to. Produces exactly
  one verdict — Ready to merge, Ready after minor corrections, Not ready to
  merge, or Unable to verify — plus findings sorted into blocking / required
  corrections / non-blocking / out-of-scope. Use this whenever you or
  another agent is about to say a change is "done", "ready", or "passing",
  before merging, before closing a task, or whenever someone asks for a
  review of a diff or PR. It exists specifically to stop premature "looks
  good" verdicts: it refuses to credit tests as passing unless their output
  was actually observed, and it checks whether an old implementation a
  change claims to replace is still reachable.
---

# Slice Review

A "slice" is one bounded chunk of implementation work — a diff, a PR, a completed
task — reviewed on its own, not as a whole-codebase audit. The habit this skill
exists to break: taking a clean-looking diff plus a claim of "tests pass" at face
value. Both the diff and the claim need to be checked against something, not just
read and nodded along to.

## Gather before judging

You need four things. If you don't have one, say so explicitly rather than
filling the gap with an assumption:

1. **The stated goal** — what this slice was supposed to accomplish. If it's
   vague ("clean up the auth module"), don't invent a sharper goal to judge
   against; note the ambiguity instead.
2. **Repo instructions** — AGENTS.md/CLAUDE.md/CONTRIBUTING or equivalent, for
   the files actually touched. Skim for conventions the diff might violate.
3. **The actual diff** — read the real lines. Don't reconstruct what changed
   from the commit message, PR description, or a summary someone gives you —
   those describe intent, not necessarily what happened.
4. **Verification evidence** — command output you personally observed, either
   by running it yourself in this session or by being shown the actual output.
   A claim of "tests pass" in a commit message or PR body is not evidence; it's
   the same kind of claim you're being asked to check.

If (3) is missing and you have no way to obtain it, the verdict is **Unable
to verify** — you can't review a change you can't read. Missing (4) is
asymmetric: without observed verification evidence you may never issue a
positive verdict (Ready to merge / Ready after minor corrections), but it
does not stop a negative one. If the diff itself demonstrates a concrete
blocking defect — a specific input or scenario you can point at that
produces wrong behavior — say **Not ready to merge** on that evidence alone;
don't retreat to "Unable to verify" when you have already proven a failure.
**Unable to verify** is for the remaining case: no observed verification
*and* nothing in the diff you can demonstrate is broken. Don't stretch thin
evidence to reach a more decisive-sounding verdict in either direction.

## Review the diff itself

Read every changed line with the stated goal in hand. Two failure modes to
actively watch for, because they're the ones a quick read misses:

- **Passing tests, wrong behavior.** Tests can pass while missing the actual
  bug — wrong edge case, untested branch, a mocked dependency that hides the
  real failure. Passing test output tells you the tests the author thought to
  write don't fail; it doesn't tell you the logic is correct. Read the logic
  itself, independent of what the test suite checks.
- **The old path is still reachable.** When a slice's goal is to replace or
  retire an implementation, grep for remaining references to the thing being
  replaced — call sites, imports, exports, registered routes, feature flags,
  config toggles. "We added the new path" is not the same claim as "the old
  path is gone"; treat them as two separate things to verify, because a
  reachable dead-and-forgotten old path is one of the most common ways a slice
  that looks finished isn't.

## Sort every finding into exactly one bucket

- **Blocking** — prevents the merge; the slice cannot ship until it is
  resolved: a correctness bug, the stated goal not actually met, an old path
  still reachable, or a violated repo instruction whose fix requires
  rethinking the approach rather than adjusting a line. An unbacked critical
  claim (like "tests pass" with no output shown) is *not* by itself a
  blocking finding — it strips the evidence a positive verdict needs, and
  the verdict rules then decide: Not ready to merge if something is
  demonstrably broken, Unable to verify if nothing is.
- **Required corrections** — must be fixed before the slice ships, but
  narrowly mechanical: the defect is precisely locatable, the fix is obvious,
  local, and low-risk (a wrong response format, a misnamed field, a missing
  required header), and it casts no doubt on whether the goal was met or the
  core logic is right. The test that separates this bucket from Blocking: can
  you write the exact corrected line(s) yourself in the review? If fixing it
  needs a decision, a design, or touching the verified logic, it's Blocking.
- **Non-blocking** — real, worth mentioning, doesn't hold up the merge and
  isn't required at all: style nits, minor inefficiencies, a TODO left behind.
- **Out-of-scope** — a real issue in code the diff does *not* touch (a
  pre-existing bug nearby, a refactor opportunity in an untouched function).
  Name it so it isn't lost, but don't let it push the verdict toward "not
  ready" — that's how review scope creeps into demanding unrelated work.
  This bucket never applies to changes the diff itself introduces: an
  unrequested, unrelated change riding along inside the diff is a finding
  about this slice (blocking, if it's untested or risky), not someone
  else's problem.

Two discipline checks before you finalize a finding:
- If it's **blocking** or a **required correction**, you should be able to
  point at a specific line and state the concrete requirement it violates or
  the input that breaks. "This could be cleaner" or "I'd have done this
  differently" is neither — if you can't articulate the failure or the
  violated requirement, it's non-blocking at most.
- If something looks wrong at first glance, check it against the surrounding
  context (types, call sites, existing tests, comments) before flagging it.
  Plenty of unusual-looking code is intentional; a false blocking finding
  costs the author real time chasing a non-problem.

## Choose the verdict

Exactly one, chosen by the findings above:

- **Ready to merge** — goal is met, no blocking findings and no required
  corrections, and you have observed verification evidence that supports it.
- **Ready after minor corrections** — goal is met, no blocking findings, and
  observed verification evidence supports the core behavior; what remains is
  one or more required corrections (the mechanical bucket above). By
  construction this verdict never contains a blocking finding — if a finding
  blocks, the verdict is Not ready to merge.
- **Not ready to merge** — at least one blocking finding: unmet goal,
  correctness bug, reachable old path, or a violated repo instruction.
  Diff evidence alone is sufficient when it demonstrates a specific, concrete
  failure — you do not need verification output to block on a defect you can
  prove by reading the change.
- **Unable to verify** — you don't have enough to reach one of the above:
  no diff to read, or no observed verification evidence *and* no defect you
  can concretely demonstrate from the diff, or a goal too ambiguous to judge
  against. This is a legitimate verdict, not a failure to finish the
  review — reaching it honestly is better than guessing toward a more
  confident-sounding one.

## Report

```
# Slice Review: <goal or slice name>

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

Leave a bucket's body as "None." rather than omitting the heading — an absent
section reads as "not checked," not "nothing found."
