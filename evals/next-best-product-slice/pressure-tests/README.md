# next-best-product-slice pressure tests

This is a separate suite from `evals/next-best-product-slice/evals.json` (the
ordinary regression suite). The ordinary suite checks that the skill picks
well given a normal spread of product-value scenarios. This suite is
adversarial: each fixture targets one specific way a product-value
recommendation can drift away from evidence, usually under some kind of
pressure -- a tempting idea, a refactor request, a bundled bug, an explicit
demand for a ranked list.

## What's here

Eleven cases, one per failure mode, in
`evals/next-best-product-slice/cases/case-101/` through `case-111/`. Case
directories use neutral IDs deliberately -- a descriptive name would leak
what the fixture is testing.

| Case | Failure mode | What it tests |
|---|---|---|
| 101 | Discoverability of an existing capability vs. architectural continuation, under direct pressure | Does an explicit push toward the cheap, dependency-unlocked candidate override a real gap in discoverability of an already-working capability? |
| 102 | Existing-but-inaccessible capability vs. speculative new feature | Does an exciting, unevidenced feature pitch get chosen over exposing a capability that already exists and is demonstrably intended? |
| 103 | Stored information not surfaced vs. cosmetic polish | Does a "make it feel more modern" request override surfacing already-correct, already-tracked information a user needs but can't currently see? |
| 104 | Confusing state transition vs. cleanup/refactor | Does a consistency-refactor request, framed as good hygiene, override a real state-legibility gap, when the refactor has no concrete near-term product connection? |
| 105 | Demonstrated intent vs. attractive invention | Does an invented, ungrounded persona-style pitch ("operators would probably love X") override a candidate traceable to an established role and observed workflow friction? |
| 106 | Bug/reliability work competing with a genuine product slice | Does a real, separate bug get silently folded into the product recommendation, or silently dropped, instead of named and set aside? Deliberately at the bug/product boundary -- see note below. |
| 107 | Technical work with a concrete product connection vs. "eventually useful" cleanup | Does a data-model fix with a stated, immediate link to what users see get preferred over a vaguer "will help us build faster later" refactor? Deliberately at the technical-cleanup/product boundary -- see note below. |
| 108 | Backend/algorithmic product value vs. superficial UI | Does a non-UI (search-ranking) fix, evidence-backed and materially more useful, get chosen over an unevidenced cosmetic UI tweak? |
| 109 | Insufficient product evidence | With no traceable user, role, or evidenced gap -- only a speculative wishlist -- does the skill say so instead of manufacturing a pick? |
| 110 | Genuine product-candidate tie | Two candidates, identical in size, reversibility, and evidence, whose value depends on the same unresolved fact (which channel buyers want) -- does the skill name the tie instead of guessing? |
| 111 | Roadmap/list request | Does an explicit "top 3 ranked" ask get fulfilled instead of declined down to one recommendation? |

Each case directory has `prompt.md` (the verbatim eval prompt, kept as its
own file since the wording of the request is itself part of the pressure
being tested) plus the case's evidence files (`review.md`/`retro.md`/
`backlog.md`/`issues.md`/`product-state.md` as appropriate). Answer keys
live outside the case directories, in
`evals/next-best-product-slice/grading/case-1XX.expected.md`.

## Deliberate boundary cases: 106 and 107

Every fixture in this suite was audited against one question: is the
"positive" candidate correct relative to its own actual, current behavior
but materially limited in usefulness (clean product territory), or does it
involve behavior that's actually wrong relative to what the system already
does (reliability territory)? Fixtures 101-105 and 108-111 were built, and
where an early draft blurred this line (a "should always" requirement
framed as failing, paired with concrete-harm/incident language), rewritten
to keep the positive candidate's underlying behavior correct and the gap
purely one of missing capability, legibility, or access.

Cases 106 and 107 are the deliberate exceptions, kept at the boundary on
purpose:

- **106** pairs a genuine, unrelated bug (duplicate confirmation emails
  under retry) with a genuine, separately-evidenced product candidate
  (real-time sales count for event organizers). The correct behavior is to
  keep them apart -- recommend the product slice, name the bug plainly as
  real but out of scope for this skill, and neither silently absorb it
  into the recommendation nor silently drop it.
- **107** is designed so the "technical" candidate's connection to product
  value is a correctness fix (a timezone-aggregation mismatch that makes
  monthly totals wrong for non-UTC teams) -- deliberately testing
  `SKILL.md`'s stated exception: technical work is eligible specifically
  when the fix itself is what unlocks the user-visible outcome. This case
  exists to confirm the skill can tell that exception apart from ordinary
  cleanup, not to test the clean-vs-reliability boundary the other cases
  were tightened against.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation and
explains what part of `skills/next-best-product-slice/SKILL.md` it's
grounded in. A failure on any of these cases is a real finding worth
evaluating for `SKILL.md`, following this repository's evidence-first
convention -- a single suspected miss gets evaluated before any wording
change, not patched immediately.

## Not a with/without-skill benchmark

Like the ordinary suite, results are worth comparing against an
unstructured baseline, but this suite's primary purpose is to probe where
the skill's stated contract actually breaks under pressure. Committed
results live in `evals/next-best-product-slice/RESULTS.md`.
