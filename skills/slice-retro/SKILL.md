---
name: slice-retro
description: >-
  Writes a retrospective for one completed implementation slice (a commit,
  branch, PR, or finished task) — what it actually proved, which assumptions
  it validated or falsified, what remains uncertain, what was deliberately
  deferred, and what architectural consequence follows, strictly from the
  slice's own diff and verification evidence. Every claim is scoped to
  observed evidence, tight inference, or flagged as speculation — it never
  lets an author's notes, a confident request, or a passing test suite
  inflate what was actually shown. Use whenever the user asks to write a
  retro, a postmortem-style writeup, or a "what did we learn" summary for
  finished work, or says a slice/PR/commit is done and asks what it proved
  or what's now uncertain. Deliberately refuses to choose the next slice,
  redesign the system, run a repo-wide architecture review, rewrite docs,
  or produce a project plan — push back and redirect to a scoped
  retrospective if asked for any of those, even as a "bonus" on the ask.
---

# Slice Retrospective

A "slice" is one bounded implementation change — a commit, a branch, a PR, a
completed task — looked at after the fact, on its own terms, not as an
excuse to plan what's next. The habit this skill exists to break: writing a
retrospective that quietly turns into a status update dressed as learning,
or a pitch for the next piece of work. A retrospective's job is narrower and
harder than that: say exactly what this slice, as implemented and verified,
actually demonstrated — and stop there.

## Gather before writing

Ground the retrospective in what's actually available, not in what you
assume must be true of a "typical" slice:

1. **What the slice set out to do** — the goal, ticket, or plan it worked
   from, if one exists. If none is available, say so; don't invent an
   implied goal to score against.
2. **What actually shipped** — the real diff. Read it; don't reconstruct it
   from a commit message, PR description, or someone's summary of it.
3. **Verification evidence** — command output, test results, benchmarks, or
   behavior someone actually observed. This is the load-bearing material for
   the whole retrospective: a claim not backed by something in this category
   can only ever be inference or speculation, never "what we proved."
4. **Implementation notes and commentary** — the author's account of what
   happened, code comments, PR descriptions. Useful context, and often the
   exact place an overstatement first appears — but never evidence on their
   own. A note is a claim, and claims are what a retrospective checks, not
   what it repeats.

If any of these is missing, don't fill the gap with a plausible-sounding
assumption. Note the absence in the relevant section instead —
"remaining uncertainty" and "not determinable from available evidence" are
legitimate, common outcomes here, not failures to produce a complete
retrospective.

## Three tiers of claim — keep them separate

Every sentence you write belongs to exactly one of these. Mixing them is the
single most common way a retrospective overstates itself:

- **Observed evidence** — something you can point to directly: a test that
  actually ran and its actual output, a specific line in the diff, a
  concrete behavior someone demonstrated. This is the only tier that can
  support "What we proved" or an assumption being validated/falsified.
- **Inference** — a conclusion that follows tightly from observed evidence,
  one short logical step away, and no further. "The test exercises the
  boundary condition and passed, so the boundary case is handled" is
  inference from evidence. "So this will hold up under production load" is
  not — that's a much longer chain wearing the coat of the short one.
- **Speculation** — anything beyond what evidence or a tight inference
  supports: predictions, hopes, generalizations, "this probably also
  fixes...", "this should scale to...". Speculation isn't forbidden —
  genuine open questions are one of this skill's required outputs — but it
  belongs only in **Follow-up questions**, phrased as a question, never
  smuggled into an earlier section as a conclusion.

When you're unsure which tier a claim belongs in, write it as the weaker
tier. A retrospective that under-claims is a minor inconvenience; one that
over-claims is the exact failure this skill exists to prevent. This applies
just as much to a confident implementation note or a fully green test run as
it does to your own reasoning — a note that says "this is production-ready"
or a test suite that passed is a fact about what was written or run, not
proof of the broader claim riding along with it. Check what the evidence in
front of you actually covers before crediting the claim it's attached to.

## Write only about what happened

Stay inside the boundary of the completed slice:

- Judge the slice against what it actually set out to do and what the diff
  actually contains — not against a better version of the slice you can
  imagine, and not against the rest of the codebase.
- **Assumptions validated / falsified** means assumptions the slice's own
  goal or implementation depended on, not general assumptions about the
  system that happen to be adjacent. If the evidence genuinely doesn't
  settle a given assumption either way, that assumption belongs in
  Remaining uncertainty, not forced into one of these two buckets to fill
  them.
- **Intentional non-goals** are things the slice deliberately did not
  attempt — stated out of scope, or clearly deferred on purpose, in the
  goal/plan or the author's own notes. Don't confuse these with things that
  are simply missing, broken, or discovered too late to fix: a gap the
  evidence reveals rather than one the slice chose is a finding for
  Remaining uncertainty (or nothing this skill flags at all, if the
  evidence doesn't speak to it), never a retroactively "intentional" one.
  A note's own deferral language ("filed as a follow-up," "noted for
  later," "not fixing now") does not by itself qualify — that phrasing
  describes what happens *after* a gap is found, and reads the same
  whether the gap was chosen in advance or stumbled into. Check what came
  first: if a test, benchmark, or repro run *during this slice* is what
  surfaced the gap, it belongs in Remaining uncertainty even if the note
  discussing it uses deferral wording; only a scope boundary that was
  already named — in the goal, the plan, or the notes — *before* the
  evidence that would have revealed it as a problem counts as intentional.
- **Architectural consequences** describes what capability, seam, or
  simplification now exists *because this slice landed* — grounded in the
  diff, not a survey of what could theoretically now be built on top of it.
  One or two concrete, load-bearing sentences beat a speculative list.
- **Follow-up questions** are genuine open questions this slice's evidence
  raised — not a disguised recommendation, priority call, or "the next
  slice should be X." A follow-up question ends in a question mark and
  doesn't answer itself.

## What this skill refuses to do

Even when asked directly, this retrospective does not:

- Choose or recommend the next slice of work.
- Redesign the system or propose an alternative architecture.
- Conduct a repository-wide architecture review — its evidence is this
  slice's diff and verification, not the rest of the codebase.
- Rewrite project documentation.
- Produce a project plan, roadmap, or set of implementation recommendations.

If a request bundles one of these in with the retrospective — "also tell me
what to build next," "while you're in there, review our whole
architecture" — write the retrospective as scoped above and say plainly
that the rest is out of scope for this skill, rather than quietly complying
to be agreeable. That kind of scope-creep pressure is exactly what this
boundary exists to hold against, whether it arrives as a direct request, a
speculative comment left in the diff, or wording that pushes for a bigger
conclusion than the evidence supports.

## Report

Use this exact structure:

```
# Slice Retrospective: <slice name or goal>

## What we proved
<Observed evidence only. If nothing was conclusively proved, say so.>

## Assumptions validated
<Assumptions the slice depended on that evidence actually confirmed.
"None." if none were genuinely tested.>

## Assumptions falsified
<Assumptions evidence actually contradicted. "None." if none were.>

## Remaining uncertainty
<What the evidence doesn't settle — named specifically, not a generic
disclaimer.>

## Intentional non-goals
<What was deliberately out of scope or deferred, per the goal/plan or
explicit notes. "None stated." if nothing was.>

## Architectural consequences
<What new seam, capability, or simplification now exists because this
slice landed — grounded in the diff.>

## Follow-up questions
<Genuine open questions, each ending in "?". Not recommendations, not a
plan.>
```

Leave a section's body as "None." or an explicit "not determinable from
available evidence" rather than omitting it — an absent section reads as
"not considered," which is worse than an honest empty result.
