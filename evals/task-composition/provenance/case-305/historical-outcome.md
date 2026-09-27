# Historical outcome — case-305 (Rust AFIT + RPITIT stabilization history)

This is what actually happened after the chosen cutoff (2023-06-13 EOD
UTC). None of this is in the agent-visible fixture; it's here so a grader
can judge whether a proposed slice plan's *reasoning* holds up, without
treating this sequence as the one correct answer a tested run needed to
reproduce (per this suite's own convention: historical execution is
evidence, not an oracle).

## What actually happened, in order

1. **The very next day, the tracking issue formally caught up to what its
   own bookkeeping had implied for months.** In a 14-minute burst
   (2023-06-14T21:48-22:02 UTC), `tmandry` renamed #91611's title to name
   both `async_fn_in_trait` and `return_position_impl_trait_in_trait`,
   split its "Unresolved Questions" section to explicitly ask "Should we
   stabilize this feature together with `async fn`..." and "Resolution of
   #112194," and cross-referenced #112194 into the tracking issue
   directly. This mirrors RFC 3425's own already-ratified "Unresolved
   questions" text (merged the previous day) almost verbatim — the
   tracking issue was updated to match the RFC, not the other way around.
2. **#109468 (a separate, dormant RPITIT lifetime bug, open since March
   2023) closed within about 24 hours of cutoff**, via a rollup PR
   (#112611, opened 2023-06-14T05:32 UTC, merged the same day at
   23:18 UTC) — on its own timeline, with no connection to #112194 or the
   tracking-issue restructuring. Confirms this suite's now-familiar
   pattern (case-304's REGR-120247 vs. resource-manager cluster): two
   textually similar "RPITIT lifetime bug" tickets, one dormant and
   independently resolved, one fresh and RFC-linked, staying genuinely
   unconnected.
3. **#112194 was resolved 2023-08-28**, via PR #114489 ("Make RPITITs
   capture all in-scope lifetimes"). The fix is RPITIT-only in its file
   list (`rustc_ast_lowering`, `rustc_feature`, `rustc_hir_analysis`,
   `rustc_resolve`, `rustc_span`, `rustc_trait_selection` — no
   AFIT-specific file touched) and is explicitly framed, in its own PR
   body, as implementing a broader lang-team "opaque captures" policy
   decision that also covered ordinary (non-trait) RPIT (#114616) — i.e.
   the actual fix mechanism came from a wider initiative, not something
   invented specifically to answer the AFIT/RPITIT convergence question.
4. **#108304 and #109016 (two of the three dual-labeled tickets) both
   closed 2023-07-31**, each via its own, separate PR, on their own
   timelines, roughly six weeks after cutoff and roughly seven weeks
   before the joint stabilization PR — resolved as ordinary bug fixes,
   with no stated connection to #112194's resolution or to each other.
5. **#108309 (the third dual-labeled ticket, with the "async fn in trait
   is just return position impl trait in trait" quote) was never fixed.**
   As of this research (2026-09-26), it is still open — over three years
   after being filed, and more than two years after both features
   stabilized. Joint stabilization did not require resolving it.
6. **#104689, #110963, and #111105 (two AFIT-only/AFIT-adjacent tickets
   and the remaining RPITIT-only ticket) were also never fixed.** All
   three remain open as of this research. For #110963 specifically, a
   2023-07-27 comment (`compiler-errors`, postdating cutoff) states
   directly: "This issue is not blocking async fn in trait stabilization,
   though" — a plain, dated confirmation that not every open,
   feature-labeled bug was treated as a stabilization blocker, even by
   the same person (`compiler-errors`) who triaged #112194 as one — a
   different person from #112194's own filer (`tmandry`).
7. **The joint stabilization PR, #115822, opened 2023-09-13 and merged
   2023-10-14** — three months after this fixture's cutoff, and about six
   weeks after #112194's resolution. Its own body states plainly: "The
   desirability of this desugaring being available is part of why RPITIT
   and AFIT are being proposed for stabilization at the same time," and
   its "History" section describes "Sep 9, 2022: Initial implementation
   of AFIT and RPITIT landed" as a single, undifferentiated bullet — the
   retrospective account of the people who built both features does not
   itself distinguish "AFIT's implementation" from "RPITIT's
   implementation" as two separate historical events, even though they
   ran under separate feature gates throughout.

## What this means for grading

The historical shape here is a genuine double edge, not a clean
confirmation of either the "independent" or the "convergent" framing
alone: a real, RFC-text-explicit convergence pairing (the stabilize-
together question and #112194) got resolved and acted on jointly within
about six months of this fixture's cutoff — but five of the fixture's
other seven bug tickets (#104689, #110963, #111105, and, more strikingly,
two of the three dual-labeled tickets, #108304/#109016, which resolved on
their own separate timelines with no stated tie to #112194's resolution,
plus #108309, never resolved at all) were never folded into that
convergence, joint stabilization or not. **A plan-under-test that
composes RFC-3425-QUESTIONS and #112194 together as a shared convergence
consideration is tracking something the record — and the actual outcome —
supports. A plan that extends that same reasoning to conclude the other
seven tickets, or "everything AFIT/RPITIT," needed to converge into that
same slice would be overclaiming what either the cutoff-time record or the
eventual outcome actually shows.** What a plan *should* get right is
recognizable without any of this hindsight: RFC 3425's own ratified text
already names the stabilize-together question and #112194 as a specific,
linked pair — nothing in the cutoff-visible record ties the other seven
tickets into that same pairing, and the eventual outcome (this section,
DIAGNOSTIC only) confirms that most of them never needed to be.
