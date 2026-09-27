# Tasks: trait-position `impl Trait` — open work as of mid-June 2023

This is the current state of the open work, pulled from the
rust-lang/rust issue tracker and from RFC 3425's own just-merged text,
sorted by issue number. There is no other roadmap document for this work
beyond what's written here and in the umbrella tracking issue referenced
below.

- **AFIT-104689** — `async fn` in trait rejects a lifetime restriction an
  ordinary (non-async) trait impl is allowed to add. Filed as
  rust-lang/rust#104689 (labeled `F-async_fn_in_trait` only): a non-async
  trait impl may legally add an extra lifetime parameter that forces two
  of its arguments to share a lifetime; the equivalent `async fn` impl is
  rejected with "`impl` item signature doesn't match `trait` item
  signature." One diagnostic comment exists (a maintainer suggesting the
  cause is that RPITIT's hidden-type inference algorithm requires strict
  equality between signatures rather than a looser supertype relation).
  No pull request exists, and no one is assigned. Open since
  2022-11-21, seven months with no further movement.

- **AFIT-RTN-110963** — A "mysterious higher-ranked lifetime error" when
  `async fn` in trait is combined with return-type notation (RTN, a
  separate, not-yet-stable feature for referring to an async trait
  method's associated future type — tracked in its own issue,
  rust-lang/rust#109417). Filed as rust-lang/rust#110963 (labeled
  `F-async_fn_in_trait` and `F-return_type_notation`). The reporter's own
  follow-up comment, the same day it was filed, says they thought they'd
  solved it but hadn't — "it still exists for early-bound lifetimes." No
  pull request exists. Open since 2023-04-28.

- **AFIT-RPITIT-108309** — Specialization doesn't work correctly through
  polymorphic indirection when a trait method uses `async fn` (or,
  equivalently, RPITIT). Filed as rust-lang/rust#108309, reproduced with a
  `default async fn` in a specializing impl that isn't properly
  specialized when called through a generic function. Labeled both
  `F-async_fn_in_trait` and `F-return_position_impl_trait_in_trait`
  (applied by the same person, in the same minute, as filing) — when the
  reporter asked why the RPITIT label was present, the compiler team
  member who filed it replied: "Because async fn in trait is just return
  position impl trait in trait, and the specialization problems are
  equally as broken with the latter?" No pull request exists. Open since
  2023-02-21.

- **AFIT-RPITIT-108304** — A test regression in RPITIT's default-body
  trait-method handling, introduced by an unrelated async-lowering
  cleanup PR (#104833) that removed an internal `identity_future` step.
  Filed as rust-lang/rust#108304 (labeled both `F-async_fn_in_trait` and
  `F-return_position_impl_trait_in_trait`). The issue's own text: "This is
  deemed acceptable for now as that feature is still unstable, as long as
  we track progress to fix it, hence this issue." No pull request exists.
  Open since 2023-02-21.

- **AFIT-RPITIT-109016** — Confusing diagnostics (not a compiler bug per
  se) when a default trait method built on RPITIT/`async fn` needs an
  explicit `+ '_` capture bound that the trait's own declared return type
  doesn't spell out. Filed as rust-lang/rust#109016 (labeled both
  `F-async_fn_in_trait` and `F-return_position_impl_trait_in_trait`).
  After discussion at a working-group triage meeting, a team member
  commented: "it looks like the behavior here is correct but the error
  messages are unclear. In particular, it'd be good for the error message
  to mention `+ '_` somehow to suggest how to workaround this issue and
  match the `async fn` desugaring." No pull request exists. Open since
  2023-03-11.

- **RPITIT-111105** — A `Send` bound on an RPITIT return type breaks the
  borrow checker in a way that doesn't happen without the `Send` bound
  present, or when the same return type is written using `Pin<Box<dyn
  Future + Send>>` instead. Filed as rust-lang/rust#111105 (labeled
  `F-return_position_impl_trait_in_trait` only — no `async_fn_in_trait`
  label at any point). No pull request exists. Open since 2023-05-02.

- **RPITIT-109468** — RPITIT impl methods are wrongly allowed to declare
  an unconstrained lifetime parameter that the trait's own stated return
  type doesn't require. Filed as rust-lang/rust#109468 (labeled
  `F-return_position_impl_trait_in_trait` only). No pull request exists.
  Open since 2023-03-22, three months with no further movement.

- **RPITIT-112194** — RPITIT is inconsistent about which in-scope
  lifetime parameters it captures through `Self`, compared to how an
  ordinary (non-trait) `-> impl Trait` method handles the same case.
  Filed as rust-lang/rust#112194 by one of the two people who wrote RFC
  3425, eleven days ago (2023-06-02), while responding to a review
  comment on that RFC's own pull request. No pull request exists yet to
  fix it, and no comments have been added to the issue since it was
  filed.

- **RFC-3425-QUESTIONS** — RFC 3425 (RPITIT's own RFC, merged this same
  day, 2023-06-13) lists three items, verbatim, in its own "Unresolved
  questions" section: (1) "Should we stabilize this feature together with
  `async fn` to mitigate hazards of writing a trait that is not
  forwards-compatible with its desugaring?"; (2) "Resolution of
  [rust-lang/rust#112194]"; (3) "Should we limit the legal positions for
  `impl Trait` to positions that are nameable using upcoming features
  like return-type notation (RTN)?" None of the three has an answer as of
  this writing.

No priority has been marked or stated on any of these issues beyond
Rust's ordinary `T-compiler`/`C-bug`/area labels. rust-lang/rust#91611 is
itself not a task — it's the umbrella tracking issue for both features,
listing implementation-history pull requests under two subheadings (one
per feature) — see `source-notes.md` for its own stated scope and
question-tracking history.
