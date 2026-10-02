# Sources — case-305 (Rust AFIT + RPITIT stabilization history)

All data fetched via `gh api` (REST + GraphQL, anonymous, no auth needed
for public repos/issues) against `rust-lang/rust` and `rust-lang/rfcs`,
2026-09-26. Timestamps are UTC as returned by the API. Quotes are
copy-pasted from API JSON bodies or raw RFC markdown, not paraphrased,
unless marked "paraphrased."

## rust-lang/rfcs

- `pulls/3193` ("return position impl trait in traits") — opened by
  `nikomatsakis`, 2021-11-10, closed unmerged 2021-12-09. Body: "This RFC
  describes a minimal version of return position impl trait in traits. It
  is a building block for async function support." Closing comment
  (`nikomatsakis`, 2021-12-09T17:59:29Z): "I'm going to close this RFC --
  we've been doing some thinking and I plan to open a revised version
  that's a bit more ambitious at laying out some of the overall plans."
- `pulls/3185` ("Static async fn in traits") — opened by `tmandry`,
  2021-10-26, merged **2021-12-07T18:27:36Z**. AFIT's founding, ratified
  RFC.
- `pulls/3425` ("Return position `impl Trait` in traits") — opened by
  `tmandry`, **2023-04-27T18:25:57Z**, merged **2023-06-13T10:03:08Z**
  (merge commit `254fad93e2f8a824e2fef748c9585376fe8b7dd2`). RPITIT's
  actual, ratified RFC (RFC 3193 was withdrawn; this is its eventual
  replacement, per its own body: "This RFC is a collaboration between
  myself and @compiler-errors, and is based on an earlier RFC (#3193) by
  @nikomatsakis"). Full text fetched from
  `raw.githubusercontent.com/rust-lang/rfcs/254fad93e/text/0000-return-
  position-impl-trait-in-traits.md` at the merge commit.
  - Line 16 (Summary): "Allow `async fn` in traits and trait impls to be
    used interchangeably with its equivalent `impl Trait` desugaring."
  - Lines 561-563 (Drawbacks): "This difference is pre-existing, but it's
    worth highlighting in this RFC the implications for the adoption of
    this feature. If we stabilize this feature first, people will use it
    to emulate `async fn` in traits. Care will be needed not to create
    forward-compatibility hazards for traits that want to migrate to
    `async fn` later... We leave open the question of whether to
    stabilize these two features together."
  - Lines 663-667 (Unresolved questions, verbatim, all three bullets):
    "Should we stabilize this feature together with `async fn` to
    mitigate hazards of writing a trait that is not forwards-compatible
    with its desugaring? (See [drawbacks].)" / "Resolution of [#112194:
    RPITIT is allowed to name any in-scope lifetime parameter, unlike
    inherent RPIT methods](https://github.com/rust-lang/rust/issues/112194)"
    / "Should we limit the legal positions for `impl Trait` to positions
    that are nameable using upcoming features like return-type notation
    (RTN)? (See [this comment](https://github.com/rust-lang/rfcs/pull/3425#pullrequestreview-1467880633)
    for an example.)"
  - RFC 3425's PR review thread: `aliemjay`, **2023-06-07T14:18:48Z**
    (comment id 1580917997) — identifies that the RFC's stated desugaring
    is inconsistent with treating two different lifetime instantiations'
    hidden types as equal, and proposes a desugaring-level change (a
    supertrait without the offending lifetime parameter). This comment is
    the one `tmandry` later cites (2023-06-14, post-cutoff) when adding a
    clarifying note to tracking issue #91611 — not used in the
    agent-visible fixture itself, cited here only to confirm the June 14
    edit traces back to a real, dated, pre-cutoff technical exchange, not
    an invented one.
- `pulls/3245` ("Refined trait implementations," `#[refine]`) — opened by
  `tmandry`, 2022-03-22, merged 2022-08-26T20:55:53Z. Background only;
  not part of `tasks.md`.

## rust-lang/rust — RFC-adjacent implementation history

- `pulls/100734` ("Split out `async_fn_in_trait` into a separate
  feature") — `ComputerDruid`, opened 2022-08-18, merged **2022-09-23**.
  Full body (verbatim): "PR #101224 added support for async fn in trait
  desuraging behind the `return_position_impl_trait_in_trait` feature.
  Split this out so that it's behind its own feature gate, since async fn
  in trait doesn't need to follow the same stabilization schedule." Files
  touched (`gh api .../pulls/100734/files`) include
  `compiler/rustc_ast_lowering/src/lib.rs`.
- `pulls/101224` ("Initial implementation of return-position `impl Trait`
  in traits") — `compiler-errors`, opened 2022-08-31, merged
  **2022-09-09**. 30 files touched, including
  `compiler/rustc_ast_lowering/src/lib.rs` (same file as #100734, above —
  independently confirmed via `gh api .../pulls/101224/files`).
- Remaining implementation PRs from the original research brief
  (#101614, #101615, #101676, #101679, #102152, #102161, #102164, #102244,
  #102334, #102597, #103355) — all authored by `compiler-errors`, all
  merged between **2022-09-10 and 2022-10-23**. Full date table:

  | PR | Opened | Merged |
  |---|---|---|
  | 101614 | 2022-09-09 | 2022-09-10 |
  | 101615 | 2022-09-09 | 2022-09-13 |
  | 101676 | 2022-09-11 | 2022-09-12 |
  | 101679 | 2022-09-11 | 2022-10-13 |
  | 102152 | 2022-09-22 | 2022-09-24 |
  | 102161 | 2022-09-22 | 2022-09-25 |
  | 102164 | 2022-09-23 | 2022-09-30 |
  | 102244 | 2022-09-24 | 2022-09-26 |
  | 102334 | 2022-09-26 | 2022-10-16 |
  | 102597 | 2022-10-02 | 2022-10-03 |
  | 103355 | 2022-10-21 | 2022-10-23 |

- `issues/91611` ("Tracking Issue for static async fn in traits" as of
  cutoff) — opened by `nikomatsakis`, **2021-12-06T23:34:04Z**. Body
  reconstructed via GraphQL `userContentEdits` to its **2022-11-01T23:16:58Z
  (tmandry)** snapshot, confirmed unchanged through **2023-06-14T21:49:56Z**
  (a 7.5-month gap with zero recorded body edits) — i.e. this is the exact
  text live throughout this fixture's entire candidate window:
  - Title (unchanged until 2023-06-14T21:48:31Z): "Tracking Issue for
    static async fn in traits."
  - Body opening line: "This is a tracking issue for the RFC 'static
    async fn in traits' (rust-lang/rfcs#3185)."
  - "Implementation history" section already has two subheadings as of
    this snapshot: "Return position impl Trait in trait" (11 PRs, with
    the caveat "Several of these include code specific to async fn in
    trait") and "Async fn in trait" (2 PRs).
  - "Unresolved Questions" section, single flat item: `#103854` ("Do we
    need `Send` bounds to stabilize `async_fn_in_trait`?").
  - **Not used in the agent-visible fixture:** the title rename, the
    "Unresolved Questions" split, and the #112194 cross-reference all
    happen in a 14-minute burst by `tmandry`, **2023-06-14T21:48:31Z to
    2023-06-14T22:02:13Z** — after this fixture's cutoff by design (see
    `cutoff-rationale.md`).
- `issues/103854` ("Do we need `Send` bounds to stabilize
  `async_fn_in_trait`?") — created **2022-11-01T23:06:07Z**, closed
  **2023-05-15T23:53:45Z** — resolved well before this fixture's window
  opens; presented as already-landed context, not a task.
- `issues/112194` ("RPITIT is allowed to name any in-scope lifetime
  parameter, unlike inherent RPIT methods") — opened by `tmandry`,
  **2023-06-02T01:42:22Z**; cross-referenced from RFC 3425's own PR
  within the same hour (referenced 2023-06-02T01:43:40Z,
  cross-referenced 2023-06-02T01:51:35Z). Zero comments as of this fixture's
  cutoff (its only two comments, both `compiler-errors`, are dated
  2023-06-26 — after cutoff; not used). Closed **2023-08-28T19:57:33Z**
  by PR #114489 ("Make RPITITs capture all in-scope lifetimes") —
  DIAGNOSTIC only (postdates cutoff by over two months); that PR's own
  body states it implements "the lang team decision from [a] T-lang
  meeting on opaque captures strategy," a broader policy change that also
  covered ordinary (non-trait) RPIT (#114616) — an RPITIT-only code
  change (files: `rustc_ast_lowering`, `rustc_feature`, `rustc_hir_analysis`,
  `rustc_resolve`, `rustc_span`, `rustc_trait_selection`; no AFIT-specific
  file).
- `issues/104689` ("AFIT: impl can't add extra lifetime restrictions,
  unlike non-async") — `Dirbaio`, opened **2022-11-21T20:42:11Z**, still
  open (as of 2026-09-26). Label: `F-async_fn_in_trait` only. One
  pre-cutoff comment, `compiler-errors`, 2022-11-22T01:34:29Z: "So this
  has to do with the 'return-position `impl Trait` in trait' hidden-type
  inference algorithm requiring strict equality, rather than a supertype
  relation, between the function signatures (I think)." (A second
  comment, same author, 2023-07-27, postdates cutoff — not used.)
- `issues/108309` ("Weird interaction between specialization and
  RPITITs") — `LastExceed` (per issue body's own attribution), opened
  **2023-02-21T14:11:23Z**, still open. Labels `F-async_fn_in_trait` +
  `F-return_position_impl_trait_in_trait`, both applied by
  `compiler-errors` at **2023-02-21T14:12:33Z** (same minute the issue was
  filed — not a later/bot relabel). Comment thread (all pre-cutoff):
  `compiler-errors` (2023-02-21T14:17:05Z): "I'll look into this when I
  actually wake up in a few hours lol"; `LastExceed` (2023-02-22T07:15:07Z):
  "why does this issue have the `F-return_position_impl_trait_in_trait`
  label?"; `compiler-errors` (2023-02-22T07:17:20Z): "Because async fn in
  trait is just return position impl trait in trait, and the
  specialization problems are equally as broken with the latter?"
- `issues/108304` ("Fix RPIT in default async trait method") —
  `Swatinem`, opened **2023-02-21T09:42:25Z**, closed **2023-07-31T18:21:59Z**
  (open throughout this fixture's window). Labels `F-async_fn_in_trait` +
  `F-return_position_impl_trait_in_trait`, both applied by `Noratrieb`
  within the same session, 2023-02-23. Body (verbatim): "Removing the
  `identity_future` from the async lowering in #104833 will regress the
  `tests/ui/impl-trait/in-trait/default-body-with-rpit.rs` test. This is
  deemed acceptable for now as that feature is still unstable, as long as
  we track progress to fix it, hence this issue." No pre-cutoff comments.
- `issues/109016` ("return_position_impl_trait_in_trait lifetimes on
  self") — `gilescope`, opened **2023-03-11T13:05:33Z**, closed
  **2023-07-31T20:54:09Z** (open throughout this fixture's window).
  Labels `F-async_fn_in_trait` + `F-return_position_impl_trait_in_trait`,
  both applied by `spastorino` on 2023-03-22. Pre-cutoff comment thread
  (all before 2023-03-28): reporter and `cjgillot`/`Jules-Bertholet`/
  `eholk`/`vincenzopalazzo` work out a minimal repro (a missing explicit
  `+ '_` on the trait's stated return type breaks compilation when
  called through a supertrait-default method); `eholk`
  (2023-03-27T15:50:49Z): "After discussing at wg-async triage, it looks
  like the behavior here is correct but the error messages are unclear.
  In particular, it'd be good for the error message to mention `+ '_`
  somehow to suggest how to workaround this issue and match the `async
  fn` desugaring." (Three further comments, July-August 2023, postdate
  cutoff — not used.)
- `issues/110963` ("Mysterious 'higher-ranked lifetime error' with async
  fn in trait and return-type notation") — `compiler-errors`, opened
  **2023-04-28T20:17:17Z**, still open. Labels `F-async_fn_in_trait` +
  `F-return_type_notation` (RTN — a separate, not-yet-stable feature; see
  `issues/109417` below). One pre-cutoff self-comment, same day: "Actually
  I forgot to click submit on this issue and I think I solved it in the
  mean time... edit: didn't actually solve it completely, it still exists
  for early-bound lifetimes." (Later comments, July 2023, postdate cutoff
  — not used; one of them states "This issue is not blocking async fn in
  trait stabilization, though," which is DIAGNOSTIC only, see
  `historical-outcome.md`.)
- `issues/111105` ("RPITIT with Send trait marker breaks borrow checker")
  — opened **2023-05-02T18:03:21Z**, still open. Label
  `F-return_position_impl_trait_in_trait` only (RPITIT-specific; no AFIT
  label at any point — confirmed via the issue's own label-event
  history). Two pre-cutoff comments (2023-05-02/03) work out variant
  reproductions; a repro's error text itself references a known, unrelated
  limitation (`issues/100013`, a GAT lifetime-elision issue, not part of
  this fixture).
- `issues/109468` ("Unconstrained lifetimes are allowed on
  return-position-impl-trait-in-trait impl methods") — `compiler-errors`,
  opened **2023-03-22T01:40:36Z**. Label
  `F-return_position_impl_trait_in_trait` only. Still open as of this
  fixture's cutoff (2023-06-13 EOD): its eventual fix PR, #112611, was not
  opened until **2023-06-14T05:32:19Z** (confirmed via the issue's own
  `timeline` API) and merged the same day, **2023-06-14T23:18:38Z** — both
  dates after cutoff; DIAGNOSTIC only. **Not stated or cross-referenced
  to be the same bug as #112194** — distinct symptom (permits an
  unconstrained lifetime, vs. #112194's inconsistent capture of an
  in-scope one), distinct fix, no comment or cross-reference tying them
  together found in either issue's thread.
- `issues/109417` ("Tracking Issue for return type notation") — opened
  **2023-03-20T23:18:30Z**, still open. A separate, distinct feature
  (RTN) with its own tracking issue; referenced by #110963's dual label
  and by RFC 3425's own third "Unresolved question" (limiting `impl
  Trait` positions to RTN-nameable ones). Not itself a task in this
  fixture — mentioned in `source-notes.md` as a related-but-excluded
  initiative, per the same convention case-304 used for its
  thematically-adjacent, deliberately-excluded items.
- `pulls/115822` ("Stabilize `async fn` and return-position `impl Trait`
  in trait") — `compiler-errors`, opened **2023-09-13T18:03:23Z**, merged
  **2023-10-14T09:17:28Z**. DIAGNOSTIC only (postdates cutoff by three
  months); full body fetched and used only in `historical-outcome.md`.
  Key lines: "The desirability of this desugaring being available is part
  of why RPITIT and AFIT are being proposed for stabilization at the same
  time." / History section: "Sep 9, 2022: Initial implementation of AFIT
  and RPITIT landed" (one bullet, not two) / "there was strong consensus
  in a recent lang team meeting that we should *change* these [capture]
  rules, and furthermore that new features should adopt the new rules"
  (referring to the #112194/#114489 resolution as a precondition folded
  into the joint stabilization).

## Search methodology (confirming no other substantive candidate was missed)

- `gh search issues --repo rust-lang/rust` via the GraphQL/REST search
  endpoint, `label:F-async_fn_in_trait created:2021-01-01..2023-06-13` and
  `label:F-return_position_impl_trait_in_trait created:2021-01-01..2023-06-13`
  — both run directly by the auditing session (not only the earlier
  research pass), to independently confirm the open-as-of-cutoff set.
  Every closed item in these two searches closed either well before
  cutoff (already-landed context, not tasks) or well after (not
  addressed by any pre-cutoff PR, and not included as a task since no
  open PR or design proposal exists for it at cutoff either — e.g.
  #104908, #105154, closed well before cutoff, are ordinary bugfixes with
  no bearing on this fixture's topology question).
- A broader keyword search (`RPITIT`/`impl Trait in trait`/`async fn in
  trait` combined with `dyn`/`object safe`) was run to check for a
  dyn-compatibility-specific open item pre-cutoff; it surfaced only
  already-catalogued items above plus general, unrelated `dyn Trait`
  diagnostics issues with no `F-async_fn_in_trait` or
  `F-return_position_impl_trait_in_trait` label — none added to the task
  set.

## Excluded candidates

- `issues/112626` ("AFIT: strange errors on circular impls") — `Dirbaio`,
  opened **2023-06-14T17:08:22Z** — after this fixture's cutoff (2023-06-13
  EOD) by design. Not included at all, not even as DIAGNOSTIC material,
  since it plays no role in this window's story.
- July-2023 crop of smaller AFIT/RPITIT issues (#113538, #113656,
  #113796, #114142, #113794, #113903, #113929, #114145, #114274,
  #114601) — all postdate cutoff by three-plus weeks; titles read as
  one-off ICE/diagnostic reports, not design-level items. Not included
  (see `cutoff-rationale.md`, "Task count").
- `issues/102527` ("Exponential compile times for chained RPITIT") and
  `issues/105451` ("Multiple nested `impl Trait` in trait method does not
  work") — checked directly: neither carries the
  `F-return_position_impl_trait_in_trait` label; both are filed under
  `F-impl_trait_in_assoc_type` / `F-impl_trait_in_fn_trait_return`
  respectively, genuinely distinct, related-but-separate impl-Trait
  initiatives, not RPITIT itself. Excluded.
- `issues/112047` ("`Failed to normalize` `async_fn_in_trait` ICE for
  indirect recursion of async trait method calls", `F-async_fn_in_trait`,
  created 2023-05-28, closed 2023-09-19 — open throughout this fixture's
  window), `issues/109464` ("type metadata for unique ID is already in
  the `TypeMap`!", `F-async_fn_in_trait`, created 2023-03-21, closed
  2023-06-29 — open throughout this fixture's window), and
  `issues/108580` ("ICE: no errors encountered even though
  `delay_span_bug` issued, expected ReFree to map to ReEarlyBound",
  `F-return_position_impl_trait_in_trait`, created 2023-02-28, closed
  2024-03-25 — open throughout this fixture's window) — all three found
  by re-running the full-history label searches during the audit pass
  (missed by the original research brief's search methodology above,
  which cited only already-closed-before-cutoff examples). All three
  carry `I-ICE` (and `108580`/`112047` also carry `glacier`), read as
  one-off crash/minimization reports with no design content, and are
  excluded on the same basis as the July-2023 crop below: not
  design-level items, consistent with the research brief's warning
  against turning this into "a Rust compiler trivia exam."
