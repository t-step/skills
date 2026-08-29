---
name: comment-cleanup
description: >-
  Report-first comment cleanup: classifies each comment remove/correct/
  preserve by what information would be lost if it disappeared. Default
  output is the report only, no edits; applying its high-confidence
  removals/corrections is a separate, explicit step. Removes clutter
  (restates code, narrates obvious flow, or stale) while preserving
  rationale, invariants, concurrency/compat/security constraints, history,
  still-relevant TODOs, API docs, and tooling directives. Preserved
  comments get a recommended better home (test, docstring, decision log,
  issue) — recommendation only, never performed. Use to clean up or reduce
  comment clutter, or remove stale/dead comments. Requires inspecting code
  and call sites; never classifies from text alone. False-positive
  deletion is far worse than a redundant comment left in place, so
  uncertain comments stay flagged, not guessed away. Refuses to become a
  refactor, style rewrite, TODO purge, or relocation of preserved
  information, or to optimize for comment count/diff size.
---

# Comment Cleanup

A comment pass is not a tidiness exercise. The habit this skill exists to
break: treating comments as clutter by default and pruning toward a smaller,
cleaner-looking file. That habit deletes exactly the comments that were
worth the most — the ones explaining a decision, a constraint, or a danger
that the code itself doesn't say. This skill goes the other way: comments
are removed only when removing them provably loses nothing, and everything
else is left alone, even if it looks redundant, even if it's ugly, even if
deleting it would make the diff smaller.

## Report first, apply only on request

The default invocation of this skill produces the classification report
below and nothing else — no comment is removed, corrected, or otherwise
edited as part of producing it. Applying the report's dispositions is a
separate, explicit second step:

- **Default.** Gather evidence, classify every candidate comment, sort into
  high-confidence and needs-judgment, and produce the report. Stop there.
- **Apply, when requested.** Happens only when the user approves the
  report (e.g. "apply it," "go ahead," "make those changes") or when the
  original invocation itself already carried explicit apply intent (e.g.
  "clean up the comments and make the edits," "remove the dead comments
  now"). Even then, do the full gather-and-classify pass and produce the
  report first — apply intent changes what happens *after* the report,
  not whether one gets produced.
- **What apply does.** Performs only the report's high-confidence
  removals and corrections — never a needs-judgment item, never anything
  the report didn't already list — then runs "Verify after editing"
  below.
- **What apply never does.** Relocate a preserved comment's information to
  its recommended home (see "What this skill refuses to do"), or touch
  anything beyond the high-confidence removals and corrections the report
  already named.

This is a restructuring of *when* edits happen, not of the judgment rules
below: the same evidence discipline, taxonomy, and refusals govern the
report whether or not an apply step ever follows it.

## The one question that decides everything

For every candidate comment, ask: **what information would be lost if this
comment disappeared?**

- If the honest answer is "nothing — the code already says this, as plainly
  or more plainly than the comment does" — the comment is safe to remove.
- If the answer is anything else — a reason, a constraint, a warning, a
  piece of history, a fact about some other system — the comment is carrying
  information the code doesn't, and it survives. Rewrite it only if it's
  factually wrong (stale); never delete it for containing real information,
  and never delete it merely because the information is hard to phrase well.

Everything in this skill is a way of answering that question rigorously
instead of by gut feel about how a comment reads.

## Gather before judging — never classify from the comment's text alone

A comment's fate depends on what's true of the code around it, not on how
the comment sounds. Before deciding anything:

1. **Read the code the comment is attached to**, not just the comment. A
   comment that looks like it's merely restating the next line might be
   restating a *different* line, or the one true thing distinguishing this
   implementation from the obvious one.
2. **Trace call sites and definitions** for anything the comment claims
   about behavior elsewhere — a "this must run before X" comment is checked
   against where X is actually called, not taken on faith; a comment
   describing a function's contract is checked against how callers actually
   use it.
3. **Check tests** for evidence of what behavior is actually depended on.
   A test that pins an edge case the comment describes is corroborating
   evidence; a test that contradicts the comment's claim is a stale-comment
   signal.
4. **Check whether the comment is actually code**, not prose, before
   touching it — lint suppressions (`# noqa`, `// eslint-disable-line`),
   type-checker directives (`# type: ignore`, `// @ts-expect-error`),
   coverage pragmas (`# pragma: no cover`), doc-generator tags (`/// <doc>`,
   JSDoc, Sphinx directives), license/copyright headers, and generated-code
   markers (`// Code generated by ... DO NOT EDIT`) are machine-significant
   even when they're syntactically comments and read like ordinary
   sentences. Never delete or "clean up" one of these on the assumption it's
   just decoration — confirm what reads it (a linter config, a build
   pipeline, a codegen tool) before treating it as prose, and when you
   can't confirm, treat it as significant.
5. **Check version-control history when it's available and cheap** (`git
   log`/`git blame` on the file) for context a comment's date or wording
   references — but see the next point on where that evidence can and can't
   take you.

Information that exists only in an external system you cannot read right
now — an issue tracker, a PR description, a chat thread — is not a reason to
delete a comment. The comment may be the *only* copy of that information
actually reachable from the code. Not being able to independently confirm a
comment's claim is a reason to preserve it under uncertainty, not a reason
to remove it.

## Evidence discipline

Every classification rests on one of three tiers. Say, at least to
yourself, which tier a judgment sits in before acting on it:

- **Observed** — directly supported by code you actually read, tests you
  actually read, configuration or documentation in the repo, or history
  available in the repo (commit messages, changelogs, ADRs).
- **Inference** — a conclusion strongly suggested by observed evidence, one
  short logical step away. "This lock is acquired in every other call site
  and this comment says why — the invariant is real" is inference from
  observed evidence. "This was probably written by someone unfamiliar with
  the codebase, so it's probably safe to ignore" is not a short step from
  anything you observed.
- **Speculation** — plausible but not established by anything you actually
  looked at.

**A comment must not be deleted primarily on speculation.** When you're
unsure which tier a judgment belongs in, treat it as the weaker tier — that
means preserving the comment, not removing it. This is the same asymmetry a
retrospective or a code review applies to overclaiming: under-acting on a
comment costs a future reader a few extra words; over-acting on it can
delete a warning that would have stopped a real bug.

## Classify every candidate comment

- **Restates the adjacent code.** Says in words exactly what the next line
  already says in code, with no added reasoning, constraint, or context.
  → Remove.
- **Narrates straightforward control flow or mechanics.** Describes *what*
  a loop, conditional, or standard library call does when that's already
  obvious from reading it — not *why* it's there. → Remove.
- **Stale.** No longer accurately describes the implementation it sits
  next to. → If the true, current behavior is establishable from the code
  and tests in front of you, correct the comment to match. If it isn't
  (you'd be guessing at what the comment was ever trying to say), delete it
  rather than invent a replacement — a wrong comment is worse than none.
  Watch for the partial case: a comment can have one fixable surface detail
  (a variable name that no longer exists, a function that was renamed)
  sitting next to a substantive claim that isn't establishable at all (a
  specific bug, an "edge case" never defined anywhere, a feature nothing in
  the repo shows was ever built). Patching only the fixable surface detail
  while leaving the unverifiable claim standing produces a comment that
  *looks* corrected but still asserts something you can't confirm — that's
  the same mistake as inventing a replacement, just harder to notice
  because part of the edit was legitimate. Judge the comment's core claim,
  not just its easiest-to-fix detail: if the substance isn't establishable,
  delete the whole comment even when a smaller piece of it technically was.
- **Explains why an unusual implementation exists.** The code doesn't look
  like the "obvious" way to do the thing, and the comment is the only
  record of why. → Preserve, even if the reason looks self-evident to you
  right now — see "What this skill refuses to do" below.
- **Documents an invariant, ordering requirement, concurrency constraint,
  compatibility requirement, security boundary, external-system behavior,
  or non-obvious failure mode.** The kind of fact that isn't visible from
  reading the immediate lines, only from knowing something about how the
  system is used, deployed, or attacked. → Preserve. Treat this category as
  the one most worth spending extra investigation on before concluding a
  comment is "merely" redundant.
- **Preserves historical context still needed to understand why changing
  the code would be dangerous.** Not general archaeology — specifically,
  context that changes what a future editor would do. → Preserve. Compare
  against the next category, which looks similar but isn't.
- **Historical archaeology that no longer matters.** Explains a past state,
  decision, or bug that doesn't constrain anything about the current code
  or a future edit. → Remove — but only once you've confirmed (not
  assumed) that nothing downstream still depends on the reasoning; if in
  doubt, this is a "needs judgment" case, not a clear delete.
- **Actionable, still-relevant TODO/FIXME/HACK.** Names real, undone work
  that still applies to the code as it stands. → Preserve. Age alone is
  never a reason to remove one of these; check whether the work described
  is done or obsolete, not how old the marker is.
- **Vague, obsolete, or already-completed TODO/FIXME/HACK.** Either the
  described work is verifiably done (check the code — don't just take a
  nearby comment's word for it), or the marker names nothing concrete
  enough to ever be actioned. → Remove.
- **Public API or developer-facing contract documentation.** Part of what
  callers, consumers, or generated docs rely on — even when it states
  something that looks obvious to someone who already knows the
  implementation. → Preserve. "Obvious to the author" and "part of the
  contract" are independent properties; a docstring can be both.
- **Required by tooling or generated-code conventions.** Lint/type/coverage
  directives, license headers, codegen markers — see step 4 above. →
  Preserve, always; these aren't a judgment call once confirmed
  machine-significant.
- **Large explanatory comment compensating for confusing code.** The
  comment itself may be entirely accurate and even well-written, and the
  code underneath it may be genuinely hard to follow. → Flag it in the
  report as a code-quality observation. Do not refactor the code to try to
  make the comment unnecessary — that's a different, larger task than
  comment cleanup, and doing it unasked risks changing behavior. The
  correct output here is a flag, not a diff.
- **Redundant-looking locally but carrying information unavailable
  elsewhere in the repo.** Two comments can say similar things while only
  one is actually redundant — the one whose information is fully
  reconstructable from something else nearby (a docstring, a type
  signature, a well-named constant). Check whether the *specific*
  information in each survives without it, not whether the two comments
  sound alike. → Preserve whichever one is load-bearing; remove the other
  only if its content is genuinely a strict subset of what remains.

## Sort into high-confidence and needs-judgment before touching anything

For every candidate you've classified:

- **High-confidence** means both the classification and the "what
  information is lost" answer are clear from what you actually inspected —
  observed evidence, not inference stacked on inference. These are the
  dispositions the apply step acts on, when and if it runs: delete the
  clearly redundant/mechanical/obsolete ones, correct the
  stale-with-an-establishable-truth ones. List them in the report as
  proposed dispositions regardless of whether apply ever follows.
- **Needs judgment** means real uncertainty remains — about whether the
  reasoning still applies, about whether something else in the repo still
  depends on the history, about whether a "vague TODO" secretly refers to
  work tracked somewhere you can't see. These are never applied, even
  during an apply step. Preserving a comment under uncertainty is a
  correct, complete outcome, not a deferred task — say so plainly in the
  report along with the specific reason for the uncertainty, so a human
  reader can resolve it with information you didn't have.

A report that proposes removing nothing because nothing cleared the
high-confidence bar is a legitimate, successful result. Do not lower the
bar to have something to show for the pass.

## What this skill refuses to do

- **Delete a "why" comment because the current implementation happens to
  make the reason look obvious.** That's frequently *because* the comment
  worked — the reasoning became load-bearing enough that the code now looks
  natural. Judge whether the reasoning is still true and still needed, not
  whether it currently reads as necessary.
- **Rewrite a preserved comment to sound better.** Style, concision, and
  tone are out of scope. Fix a comment's wording only when its content is
  factually wrong (the stale case above) — never to make a correct comment
  read more cleanly.
- **Refactor code that a comment is compensating for.** A long comment
  propping up confusing code is a flag, not a mandate to simplify the code.
  Restructuring the implementation is a different task with a different
  risk profile (it can change behavior); don't fold it into a comment pass
  even when the fix looks small and tempting.
- **Remove a TODO/FIXME/HACK because it's old.** Age is not evidence the
  work is done or no longer wanted. Only verified completion or verified
  irrelevance justifies removal.
- **Assume an annotation-shaped comment is prose without checking.** A
  string that looks like a sentence can still be a pragma, directive, or
  marker a tool depends on. When you can't confirm which, preserve it.
- **Delete a comment because its information also lives in an issue,
  PR, chat log, or other place you can't currently read.** The comment
  is the only copy actually available to a reader of this code; treat it
  accordingly.
- **Optimize for comment count, lines removed, or diff size.** None of
  those are the goal, and none of them justify a deletion that the
  evidence doesn't otherwise support.
- **Produce a large, speculative cleanup diff.** Every change should be
  individually explainable by the evidence gathered for that specific
  comment. If a pass would touch many comments on thin evidence, narrow it
  to the high-confidence subset instead of shipping the whole thing.
- **Relocate a preserved comment's information to its recommended home.**
  Recommending a better home for the information in a preserved comment (a
  test/assertion, a docstring, the repo's decision log/ADR, an issue
  reference) is part of the report. Actually moving the information there
  is separate, human-approved work this skill never performs during a
  cleanup pass — not during the report, and not during apply — even when
  the destination is obvious and the edit looks small.

## Verify after editing

This step belongs to the apply step only — it runs after edits are made,
never during the report-only default (there is nothing to verify when
nothing was edited). Run whatever exists for the language/repo you're in
and is cheap to run: tests, linter, type checker, documentation
build/lint, doc-comment extraction. A comment-only change should never
alter behavior, but a misjudged "stale" correction or an
accidentally-deleted tooling directive can still break a build or silence
a real check — catching that is exactly what this step is for. If nothing
runnable is available, say so in the apply-step report rather than
implying verification happened.

## Report

Use this exact structure:

```
# Comment Cleanup: <file(s) or scope reviewed>

**No edits were made in this pass.** Applying this report would make
<N> removal(s) and <N> correction(s) — see below. Say so explicitly even
when both counts are zero. If this report is being produced as the tail
end of an apply step that already ran, replace this line with a one-line
statement of what was actually applied instead.

## Removed
<Comment text or location, and the one-line reason nothing was lost. This
is a proposed disposition, not yet applied unless this report accompanies
a completed apply step. "None." if nothing qualified.>

## Corrected
<Location, what the comment currently says, what it would become, and the
evidence (code/tests) that established the correction. Proposed, not yet
applied unless this report accompanies a completed apply step. "None." if
nothing qualified.>

## Preserved — unique information
<Location, briefly what would have been lost, and a recommended better
home for that information: an invariant or ordering constraint → an
assertion or test; a caller-facing contract → the docstring/API doc; a
decision rationale → the repo's decision log/ADR; a workaround for an
external system → an issue reference alongside the comment. "The comment
itself is the right home" is an explicitly valid recommendation when
nothing else fits better. A recommendation is not a move — see "What this
skill refuses to do." Group by category (invariant, compatibility
constraint, historical necessity, contract, tooling directive, etc.) when
it helps a reader scan. "None flagged explicitly." if everything preserved
was simply left untouched without needing a call-out.>

## Left ambiguous
<Location and the specific open question that kept this from being
high-confidence either way. "None." if nothing was ambiguous.>

## Flagged, not addressed
<Large comments compensating for confusing code, or other code-quality
issues a comment revealed — named, not fixed, with a one-line note on why
fixing it is out of scope for this pass. "None." if nothing applies.>

## Verification
<Part of the apply step only. What you ran (tests/lint/typecheck/doc
build) and its result, or an explicit statement that nothing was run and
why. In a report-only pass, state "N/A — no edits were made in this pass"
rather than leaving this blank.>
```

Leave a section's body as "None." rather than omitting it — an absent
section reads as "not checked," not "nothing found."
