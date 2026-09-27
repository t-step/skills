# Source notes: trait-position `impl Trait` — open work as of mid-June 2023

**Where this came from:** the rust-lang/rust GitHub issue tracker and
pull requests, plus the text of RFC 3425 (rust-lang/rfcs, merged this
same day) and, for background, RFC 3185 and the withdrawn RFC 3193. All
task descriptions above are taken from the tickets' and RFC's own text as
filed — nothing has been reworded to sound cleaner or more decomposed
than it actually is. RPITIT-112194 in particular is genuinely that fresh
right now: an eleven-day-old bug report with zero comments, not
summarized down from a richer discussion that hasn't happened yet.

**Neither RFC ever claimed the two features were unrelated.** Even RFC
3193 (RPITIT's first, withdrawn proposal, opened 2021-11-10) describes
itself in its own opening line as "a building block for async function
support." The eventual RPITIT RFC that did merge, RFC 3425, states as
one of its own summary goals: "Allow `async fn` in traits and trait impls
to be used interchangeably with its equivalent `impl Trait` desugaring."
Both RFCs treat AFIT and RPITIT as sharing a mechanism from the start;
what changed between 2022-09-23 (when the two features' feature gates
were split) and now is not whether they're related, but whether they need
to be *scheduled* together.

**The umbrella tracking issue (rust-lang/rust#91611) has not yet been
updated to reflect RFC 3425's existence.** Its title still reads
"Tracking Issue for static async fn in traits," and its opening line
still names only RFC 3185 — even though its own "Implementation history"
section has listed RPITIT pull requests under their own subheading since
November 2022, with the caveat "Several of these include code specific to
async fn in trait." Its "Unresolved Questions" section lists one item,
rust-lang/rust#103854 ("Do we need `Send` bounds to stabilize
`async_fn_in_trait`?") — which was itself closed 2023-05-15, before this
window opens, and does not concern any of the nine items above. In short:
the tracking issue's own bookkeeping has quietly tracked both features
together for months, while its formal title and stated scope have not yet
caught up to that.

**Already landed, not remaining work:**
- Both features' initial compiler implementation (the desugaring itself,
  hidden-type inference, cross-crate serialization, and related
  internals) landed as a cluster of pull requests between 2022-08-31 and
  2022-10-23.
- The decision to give AFIT its own, separate feature gate (rather than
  continuing to share RPITIT's) — a deliberate pull request, explicitly
  because "async fn in trait doesn't need to follow the same
  stabilization schedule."
- AFIT's own previously-open design question, rust-lang/rust#103854
  ("Do we need `Send` bounds to stabilize `async_fn_in_trait`?"), closed
  2023-05-15.
- RFC 3425 itself, which merged today after being open since 2023-04-27.

Neither of these is part of the remaining work below — they're included
only so the remaining work isn't confused with, or padded by, things
that are already done.

**A related-but-separate initiative, seen in the same search and
deliberately not included as a task:** return-type notation (RTN), a
distinct, not-yet-stable feature with its own tracking issue
(rust-lang/rust#109417) for referring to an async trait method's
associated future type in a bound (e.g. `T: Trait<method(): Send>`). RTN
is named in one of the nine items above (AFIT-RTN-110963, which is
cross-labeled) and in RFC 3425's own third "Unresolved question," but RTN
itself — its design, its own open issues, its own timeline — is a
separate effort and out of scope here.

**A thematically similar but unrelated-in-the-record report, deliberately
not folded into any of the above:** RPITIT-109468 (unconstrained
lifetimes wrongly allowed on RPITIT impl methods) and RPITIT-112194
(inconsistent lifetime capture through `Self`) both concern RPITIT's
lifetime-capture rules and were both filed within about ten weeks of each
other, but nothing in either ticket's text or comment thread connects
them, and they describe different, independently-reproducible symptoms.

**No stated deadline beyond RFC 3425's own open questions.** Neither RFC
gives a target release or milestone for either feature's eventual
stabilization. No comment on any issue above states a required-by date or
a "must land before stabilization" priority for anything other than what
RFC-3425-QUESTIONS itself already names.
