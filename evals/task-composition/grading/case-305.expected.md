# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-rust-afit-rpitit (case-305)

**Nature of this case:** like cases 301-304, this is a real, messy
backlog pulled from public rust-lang/rust and rust-lang/rfcs history (see
`evals/task-composition/provenance/case-305/`), not an author-designed
fixture. It is graded on topology facts the record actually supports, not
on reproducing the historical PR/RFC grouping or timeline. **The central
design lesson for this case is the mirror image of case-304's**: where
case-304 pressured a run not to over-merge several tickets that share a
discovered root cause, this case pressures a run not to over-merge a
much larger set of tickets that share a real, textually-established,
mechanism-level relationship (RPITIT is what `async fn` in a trait
desugars to) plus a real, RFC-text-explicit convergence pairing, into one
indivisible blob — while still correctly recognizing the one place the
record actually does draw a convergence line. Several REQUIRED items
below are written as "does not do X" for exactly this reason.

## REQUIRED

These are facts the record in `tasks.md`/`dependencies.md`/
`repository-state.md`/`source-notes.md` genuinely supports. A run that
violates one of these is wrong, not just less thorough.

1. **Does not treat already-landed work as remaining work.** Both
   features' original 2022 implementation, the pull request that split
   AFIT onto its own feature gate, RFC 3425's own ratification, and
   AFIT's already-resolved "Do we need `Send` bounds" question
   (rust-lang/rust#103854, closed 2023-05-15) must not appear in the plan
   as open tasks needing a slice.
   *(source-notes.md, "Already landed, not remaining work")*

2. **Does not present AFIT and RPITIT as two fully unrelated features
   that merely happen to be discussed together.** `context.md` and
   `repository-state.md` establish real mechanism-level coupling: `async
   fn` in a trait desugars to RPITIT's own return-type mechanism; the
   original implementation of both shares a file
   (`compiler/rustc_ast_lowering/src/lib.rs`); AFIT-RPITIT-108309's own
   filer states "async fn in trait is just return position impl trait in
   trait." A plan that claims the two features are fully independent
   implementations with no shared mechanism at all is contradicted by the
   record.
   *(context.md; repository-state.md; dependencies.md, "Stated or clearly
   inferable")*

3. **Does not collapse all nine items into one indivisible "AFIT/RPITIT"
   slice on the strength of that shared mechanism.** Recognizing real
   coupling (REQUIRED #2) is not the same as concluding every open item
   must be composed as one unit. AFIT-104689, AFIT-RTN-110963,
   RPITIT-111105, and RPITIT-109468 each concern a distinct compiler
   subsystem with no stated cross-reference to each other, to the
   dual-labeled cluster, or to RPITIT-112194/RFC-3425-QUESTIONS — a plan
   must keep at least these four visibly separable from a merged
   "everything AFIT/RPITIT" grouping, even if it also composes some subset
   of the remaining five items together.
   *(dependencies.md, "Shared-area signal, not a stated dependency";
   repository-state.md)*

4. **Treats AFIT-RPITIT-108309 as one piece of work, not as a separate
   AFIT sub-task and RPITIT sub-task.** Its own filer's stated reasoning
   ("async fn in trait is just return position impl trait in trait, and
   the specialization problems are equally as broken with the latter?")
   is a claim about one shared mechanism and one bug, not two features'
   separate manifestations. Splitting it in two would manufacture task
   identity from label identity — the two labels describe one bug filed
   once.
   *(dependencies.md, "Stated or clearly inferable", second bullet;
   tasks.md, AFIT-RPITIT-108309 entry)*

5. **Does not assume AFIT-RPITIT-108304 and AFIT-RPITIT-109016 share
   AFIT-RPITIT-108309's "one shared mechanism, one bug" status merely
   because all three carry the same two feature labels.** Neither
   ticket's own text states a shared root cause with AFIT-RPITIT-108309
   or with each other — AFIT-RPITIT-108304 is a specific async-lowering
   regression in default-body methods; AFIT-RPITIT-109016 is a specific
   missing-capture-bound diagnostic question, already triaged by a
   working group as "correct behavior, unclear error message." A plan
   may still choose to slice them however it reasons is best (see
   DEFENSIBLE below) — what's required is not silently assuming they're
   all "the same kind of thing" as AFIT-RPITIT-108309 without saying so.
   *(dependencies.md, "Open questions the record does not resolve", first
   bullet; tasks.md, AFIT-RPITIT-108304/AFIT-RPITIT-109016 entries)*

6. **Shows RFC-3425-QUESTIONS's stabilize-together question as
   textually linked to RPITIT-112194's resolution**, not as a fully
   separate, unrelated item. RFC 3425's own ratified "Unresolved
   questions" section lists both, back to back, as two named but distinct
   open items. A plan that treats RFC-3425-QUESTIONS as having no
   connection at all to RPITIT-112194 contradicts the RFC's own text; a
   plan that treats resolving RPITIT-112194 as automatically settling the
   stabilize-together question (or vice versa) overclaims what that same
   text actually says (they are listed as two linked, separately unsettled
   items, not one).
   *(dependencies.md, "Stated or clearly inferable", first bullet;
   tasks.md, RFC-3425-QUESTIONS entry)*

7. **Does not extend RFC-3425-QUESTIONS's or RPITIT-112194's scope to any
   of the other seven items.** Nothing in the record ties the
   stabilize-together question, or RPITIT-112194's resolution, to
   AFIT-104689, AFIT-RTN-110963, AFIT-RPITIT-108309, AFIT-RPITIT-108304,
   AFIT-RPITIT-109016, RPITIT-111105, or RPITIT-109468. A plan that
   serializes any of these seven behind "resolving the stabilization
   question first," or folds them into the same slice as
   RPITIT-112194/RFC-3425-QUESTIONS without stating a specific reason
   tied to that item, is inventing a dependency the record doesn't
   support — the reverse failure mode from REQUIRED #3, and the sharpest
   instance of this case's central lesson.
   *(dependencies.md, "Open questions the record does not resolve", third
   bullet)*

8. **Does not present RFC 3425's stabilize-together question, or
   RPITIT-112194, as already resolved or decided.** Both are listed,
   verbatim, under RFC 3425's own "Unresolved questions" heading; the RFC
   states the relevant hazard and the linked issue without answering
   either. A plan that says the RFC "decided" to stabilize the features
   together, or invents a resolution for RPITIT-112194, contradicts the
   record.
   *(tasks.md, RFC-3425-QUESTIONS entry)*

9. **Does not conflate RPITIT-109468 and RPITIT-112194 into one
   "RPITIT lifetime bug," or invent a dependency between them.** Both
   concern RPITIT's lifetime-capture rules and were filed about ten
   weeks apart, but they describe textually distinct symptoms (one
   wrongly *allows* an unconstrained lifetime; the other is *inconsistent*
   about which in-scope lifetime it captures) with no comment or
   cross-reference in either thread connecting them.
   *(dependencies.md, "Shared-area signal, not a stated dependency", last
   paragraph)*

10. **Does not invent a merge-order or blocking dependency among
    AFIT-104689, AFIT-RTN-110963, RPITIT-111105, and RPITIT-109468**, or
    between any of these four and the dual-labeled/convergence items.
    `repository-state.md` states each concerns a distinct compiler
    subsystem with no cross-reference to the others.
    *(repository-state.md; dependencies.md, "Shared-area signal, not a
    stated dependency", second paragraph)*

11. **Does not invent a priority ranking, urgency signal, or deadline for
    any of the nine items beyond what the record states.** None of the
    nine carries a priority label, milestone, or assignee. A plan may
    note that RFC-3425-QUESTIONS and RPITIT-112194 carry more
    institutional visibility (they come from a just-ratified RFC's own
    text, authored by a compiler-team member) than the other seven — the
    record supports that much — but must not invent a formal priority
    label, a required-by date, or a ranking among the other seven purely
    from filing date, issue number, or the fact that most implementation
    PRs share one author.
    *(dependencies.md, "No stated priority"; repository-state.md)*

12. **Does not pull return-type notation (RTN) into scope as a task or
    dependency beyond what AFIT-RTN-110963 and RFC-3425-QUESTIONS's own
    third bullet state.** RTN is explicitly named as a separate,
    not-yet-stable feature with its own tracking issue
    (rust-lang/rust#109417); a plan that invents RTN-specific work items,
    or treats RTN's own stabilization as in scope here, goes beyond what
    the record supports.
    *(source-notes.md, "A related-but-separate initiative")*

## DEFENSIBLE EITHER WAY

Genuine open questions the record doesn't resolve. Both answers are
acceptable as long as the choice is stated, not silently assumed, and
doesn't cross into a REQUIRED violation above.

- **Whether RFC-3425-QUESTIONS and RPITIT-112194 are composed as one
  combined "stabilization-readiness" slice, or kept as two separate but
  explicitly linked slices** (one for the specific soundness fix, one for
  the broader stabilize-together policy question). Either is fine as
  long as REQUIRED #6's stated link is preserved.
- **Whether the three dual-labeled tickets (AFIT-RPITIT-108309,
  AFIT-RPITIT-108304, AFIT-RPITIT-109016) are grouped into one slice, or
  kept as three separate ones.** The record supports either — it
  establishes a shared-mechanism claim for AFIT-RPITIT-108309 specifically
  (REQUIRED #4) without establishing the same for the other two
  (REQUIRED #5). A plan may reasonably group all three (stating that the
  grouping is a convenience, not a confirmed shared root cause for all
  three) or keep them fully separate; either is defensible.
- **Whether AFIT-104689, AFIT-RTN-110963, RPITIT-111105, and
  RPITIT-109468 are composed as four separate slices, grouped by feature
  side (an AFIT-side pair and an RPITIT-side pair), or otherwise.**
  Nothing in the record mandates a specific grouping among these four
  genuinely independent items.
- **Whether AFIT-RTN-110963 is treated as fully in-scope AFIT work with
  an RTN caveat noted, or flagged as partially outside this plan's scope
  given RTN's separate tracking.** Either is fine as long as REQUIRED
  #12 isn't violated.

## DIAGNOSTIC / HISTORICAL COMPARISON (informational only — not pass/fail)

- The umbrella tracking issue (rust-lang/rust#91611) was itself
  restructured the very next day (2023-06-14) to name both features and
  formally cross-reference RPITIT-112194 — mirroring RFC 3425's own
  already-ratified text almost verbatim. This happened after this
  fixture's cutoff and is not something a cutoff-time plan could have
  observed; it is not evidence that the convergence pairing needed to be
  "discovered" rather than read directly off RFC 3425's own text, which
  already stated it.
- RPITIT-109468 closed within about 24 hours of cutoff, via an unrelated
  rollup PR with no connection to RPITIT-112194 or the stabilize-together
  question — consistent with REQUIRED #9's requirement not to conflate
  the two.
- RPITIT-112194 was resolved about ten weeks after cutoff via a pure
  RPITIT-side code change, driven by a broader lang-team policy decision
  that also covered ordinary (non-trait) `impl Trait` — not a change
  invented specifically to reconcile it with AFIT.
- AFIT-RPITIT-108304 and AFIT-RPITIT-109016 both resolved on their own
  separate timelines about six weeks after cutoff, each via its own PR,
  with no stated tie to RPITIT-112194's resolution or to each other —
  consistent with REQUIRED #5's caution not to assume all three
  dual-labeled tickets share one root cause.
- AFIT-RPITIT-108309 was never resolved — it remains open more than three
  years after being filed and more than two years after both features
  stabilized. AFIT-104689, AFIT-RTN-110963, and RPITIT-111105 were also
  never resolved. A later comment on AFIT-RTN-110963 (postdating cutoff,
  not agent-visible) states directly: "This issue is not blocking async
  fn in trait stabilization, though" — confirming that not every
  feature-labeled open bug was treated as a stabilization blocker, even
  by the person who triaged RPITIT-112194 as one (a different person
  from RPITIT-112194's own filer).
- The actual joint stabilization pull request (#115822, opened
  2023-09-13, three months after this fixture's cutoff) states plainly
  that "the desirability of this desugaring being available is part of
  why RPITIT and AFIT are being proposed for stabilization at the same
  time," and its own retrospective "History" section describes both
  features' original 2022 implementation as one bullet, not two. This is
  background on how the story ended, not something a cutoff-time plan
  could have used, and not a basis for requiring a specific slice count
  in this fixture's own composition (see REQUIRED #3/#7 and DEFENSIBLE
  above).

## Why

This fixture pressures the skill along the mirror image of the axis
case-304 sharpened. Case-304 gave a run a textually real, comment-thread-
traceable *shared discovered bug* across several tickets and tested
whether a run would over-merge them into one slice on that basis alone.
This case gives a run something structurally stronger — a *stated design
goal* (interchangeable desugaring), a *verified shared implementation
file*, a *direct core-team quote* ("async fn in trait is just return
position impl trait in trait"), and a *ratified RFC's own explicit,
named convergence pairing* — across a much larger set of tickets (nine,
versus case-304's four-item cluster), and tests whether a run can still
tell the difference between:

- **Real, textually established coupling that must be named** (REQUIRED
  #2, #6, #8) — this case does not reward pretending AFIT and RPITIT are
  unrelated, or pretending RFC 3425's own explicit convergence pairing
  doesn't exist.
- **Coupling that does not license collapsing everything into one slice**
  (REQUIRED #3, #7, #9, #10) — the sharpest version of this suite's
  now-recurring lesson (case-303's corrected REQUIRED #8; case-304's own
  central design note) that historical/textual evidence can constrain a
  slice topology without determining a unique one. Where case-304 tested
  this lesson on a small, symmetric four-item cluster, this case tests it
  on a nine-item backlog with real internal texture: one bug
  (AFIT-RPITIT-108309) that genuinely is one shared-mechanism item
  (REQUIRED #4), two more that carry the same labels without the same
  stated backing (REQUIRED #5), and a specific, named, two-item
  convergence pairing (RFC-3425-QUESTIONS + RPITIT-112194, REQUIRED #6)
  that must not bleed outward into the other seven (REQUIRED #7) — a
  distinction this suite has not previously tested at this scale or with
  this much genuine textual pull toward over-merging.
- **A convergence question the record poses but does not answer**
  (REQUIRED #8) — distinct from case-304's fully-unresolved REGR-120247,
  this case's convergence point is explicitly named, in a ratified
  governing document, as an open question — testing whether a run
  correctly reads "the RFC names this as unresolved" rather than either
  inventing an answer or claiming no such question exists.

This case does not exercise, and should not be graded on, a numeric-order
illusion (issue numbers here interleave both features' filings
chronologically with no dependency riding on that order), a
community-external process blocker comparable to case-302's mailing-list
DISCUSS gate (RFC 3425 had already merged by this fixture's cutoff), or
a resource-manager-style "one discovered bug, several separately-fixable
per-component instances" cluster shape identical to case-304's — see
`provenance/case-305/cutoff-rationale.md` for why these aren't well
supported at this cutoff and should not be treated as something a correct
run was expected to surface.
