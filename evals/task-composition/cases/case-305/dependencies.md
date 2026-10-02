# Dependencies: trait-position `impl Trait` — open work as of mid-June 2023

Only what's stated or clearly inferable from the issues, pull requests,
and RFC text themselves is listed here. Several relationships are
genuinely unresolved as filed — left open below rather than resolved,
because the record itself doesn't resolve them.

## Stated or clearly inferable

- **RFC-3425-QUESTIONS's first item names RPITIT-112194 directly.** RFC
  3425's own "Unresolved questions" section lists "Should we stabilize
  this feature together with `async fn`..." immediately followed by
  "Resolution of [RPITIT-112194]" as the very next bullet — the RFC's own
  ratified text ties these two questions together, not an inference from
  thematic similarity. Nothing in that text, or anywhere else, states
  that resolving RPITIT-112194 automatically answers the
  stabilize-together question, or vice versa — the RFC lists them as two
  linked but distinct open items, not one.
- **AFIT-RPITIT-108309 is one bug, not two.** The person who filed it
  applied both the `F-async_fn_in_trait` and
  `F-return_position_impl_trait_in_trait` labels in the same minute they
  opened it, and when asked why, replied: "Because async fn in trait is
  just return position impl trait in trait, and the specialization
  problems are equally as broken with the latter?" This is a stated
  claim, from the person who filed the issue and who also authored
  nearly every AFIT/RPITIT implementation pull request, that this is one
  underlying problem manifesting through one shared mechanism — not two
  features' separate, coincidentally-similar bugs.
- **Both features' original implementation shares at least one file.**
  The pull request that gave AFIT its own separate feature gate
  (rust-lang/rust#100734) and the pull request that implemented RPITIT
  in the first place (rust-lang/rust#101224) both modify
  `compiler/rustc_ast_lowering/src/lib.rs` — the code that lowers `async
  fn` syntax into its underlying `impl Trait`-returning form. This is a
  fact about the already-landed implementation (2022), not about any of
  the open tasks above, none of which yet has a pull request.

## Open questions the record does not resolve — flag, don't guess

- **Whether AFIT-RPITIT-108304's and AFIT-RPITIT-109016's dual labels
  reflect the same kind of "one shared mechanism" claim as
  AFIT-RPITIT-108309's does, is not stated.** Both carry the same two
  feature labels, applied deliberately (by two different people, neither
  of whom commented on why, unlike AFIT-RPITIT-108309's filer). Neither
  issue's own text states or implies a shared root cause with the other,
  or with AFIT-RPITIT-108309 — AFIT-RPITIT-108304 is specifically about
  an async-lowering regression in default-body trait methods;
  AFIT-RPITIT-109016 is specifically about a missing-capture-bound
  diagnostic. Don't assume all three dual-labeled tickets are "the same
  kind of thing" just because they carry the same two labels; don't
  assume they're unrelated to each other either — the record doesn't
  settle it.
- **Whether RPITIT-112194's eventual resolution will require any change
  to AFIT's own code, or only to RPITIT's, is not stated.** The one
  substantive pre-existing comment on this question (a review comment on
  RFC 3425's own pull request, not on the issue itself) proposes changing
  RPITIT's desugaring — but nothing confirms that's the path that will be
  taken, or that it's the only one under consideration.
- **Whether RFC-3425-QUESTIONS's stabilize-together question, once
  answered, applies to anything beyond RPITIT-112194's specific
  soundness concern, is not stated.** The RFC's own text ties the
  question to that one named issue; it does not say that any of the
  other seven tasks above must also be resolved, or resolved together,
  before either feature can be proposed for stabilization.
- **Whether AFIT-104689, AFIT-RTN-110963, RPITIT-111105, or
  RPITIT-109468 are expected on any particular timeline, or are
  considered blocking anything, is not stated.** None carries a priority
  label, a milestone, or an assignee. AFIT-104689 and RPITIT-109468 in
  particular have had no comment activity in several months.

## Shared-area signal, not a stated dependency

AFIT-RPITIT-108309, AFIT-RPITIT-108304, and AFIT-RPITIT-109016 all carry
both feature labels and all involve the boundary where `async fn`'s
desugaring meets RPITIT's own mechanics — but that's a description of
*where in the compiler* each bug lives, not a stated link between the
three tickets themselves. No ticket references either of the other two.
Do not infer a shared fix, a shared owner, or a required sequencing among
these three from the shared labels alone; AFIT-RPITIT-108309's own quote
supports treating *that one ticket* as one shared-mechanism bug, not the
whole trio as a cluster.

AFIT-104689 and AFIT-RTN-110963 (the two AFIT-only/AFIT-plus-RTN tickets)
and RPITIT-111105 and RPITIT-109468 (the two RPITIT-only tickets) each
concern a distinct compiler subsystem (impl-vs-trait signature comparison
for AFIT-104689; higher-ranked-lifetime inference crossing into RTN for
AFIT-RTN-110963; borrow-checker interaction with a `Send` bound for
RPITIT-111105; lifetime-constraint checking on RPITIT impl methods for
RPITIT-109468) with no cross-reference between any of the four, or
between any of them and the three dual-labeled tickets or
RPITIT-112194. Nothing here states or implies these four must wait on,
inform, or be sequenced against each other or against the
dual-labeled/convergence items.

RPITIT-109468 and RPITIT-112194 both describe a lifetime-capture problem
specific to RPITIT — but they are textually distinct bugs (RPITIT-109468:
an impl method is wrongly *allowed* to declare an unconstrained lifetime;
RPITIT-112194: RPITIT is *inconsistent*, not wrong on its face, about
which in-scope lifetime it captures through `Self`, compared to ordinary
`-> impl Trait`). No comment or cross-reference in either ticket ties
them together. Do not conflate them into "the RPITIT lifetime bug" or
assume one blocks the other.

## No stated priority

None of these nine items carries a priority label, a milestone
assignment, or an assignee, with the partial exception of
RFC-3425-QUESTIONS, which is not itself labeled but is drawn directly
from a just-ratified RFC's own text (a real signal that these two linked
questions have institutional attention) — this is evidence that
RFC-3425-QUESTIONS and RPITIT-112194 have more institutional visibility
than the other seven items, not evidence for ranking any of the other
seven against each other.
