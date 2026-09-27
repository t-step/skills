# Repository state

- Both feature gates (`#![feature(async_fn_in_trait)]` and
  `#![feature(return_position_impl_trait_in_trait)]`) are separately
  tracked and have been since 2022-09-23. Both are nightly-only; neither
  feature is available on stable Rust. None of the behavior described in
  `tasks.md` affects any user who hasn't opted into one or both gates.

- The pull request that split AFIT onto its own gate
  (rust-lang/rust#100734) and the pull request that implemented RPITIT in
  the first place (rust-lang/rust#101224) both modify the same file,
  `compiler/rustc_ast_lowering/src/lib.rs` — the code responsible for
  lowering `async fn` syntax into the underlying `impl Trait`-returning
  form both features share. This is a fact about the already-landed 2022
  implementation. **None of the nine open items in `tasks.md` has a pull
  request yet**, so there is no current evidence about which files any of
  their eventual fixes will touch — a plan should not assume any of them
  will or won't touch this same file.

- Almost all of both features' original implementation pull requests (12
  of the 13 non-stabilization implementation PRs found in the tracker)
  were authored by the same person, a compiler-team member who also filed
  AFIT-RPITIT-108309 above and commented on AFIT-104689. RPITIT-112194
  was filed by a different person, not this same implementer. This is a
  fact about who has historically worked on this area, not a stated
  assignment for any of the nine open items — none of the nine has an
  assignee.

- AFIT-104689's underlying mechanism (RPITIT's hidden-type-inference
  algorithm) and RPITIT-112194's underlying mechanism (RPITIT's
  lifetime-capture rules) are both part of the same general
  `rustc_hir_analysis`/trait-resolution area of the compiler, per the
  one diagnostic comment on AFIT-104689 and RPITIT-112194's own title.
  Neither ticket states or implies that fixing one has any bearing on the
  other; no comment or cross-reference links them.

- rust-lang/rust#91611, the umbrella tracking issue for both features, is
  not itself a pull request or a code change — it is a checklist/status
  document. Its own "Implementation history" section links to pull
  requests that have already merged (see `source-notes.md`); none of the
  nine items in `tasks.md` is currently linked from it.
