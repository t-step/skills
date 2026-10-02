# Context: Rust trait-position `impl Trait` — open work as of mid-June 2023

Two related, long-in-development Rust language features let a trait
method's return type be written as an opaque `impl Trait` (or, for async
methods, as plain `async fn` syntax, which desugars to the same
mechanism) instead of requiring an explicit, named associated type:

- **`async fn` in trait (AFIT)** — lets a trait declare `async fn foo(...)`
  directly. Its own RFC (rust-lang/rfcs#3185, "Static async fn in traits")
  merged 2021-12-07. Feature gate: `#![feature(async_fn_in_trait)]`.
- **Return-position `impl Trait` in trait (RPITIT)** — lets a trait
  method's return type be written `fn foo(...) -> impl SomeTrait`. Its
  first proposed RFC (rust-lang/rfcs#3193) was withdrawn unmerged in
  December 2021; a replacement, rust-lang/rfcs#3425, was opened
  2023-04-27 and merged **2023-06-13**. Feature gate:
  `#![feature(return_position_impl_trait_in_trait)]`.

`async fn` in a trait desugars internally to RPITIT's own mechanism — an
`async fn` trait method is, under the hood, a method returning
`impl Future<Output = ...>`. Both features' initial compiler
implementation (the desugaring, hidden-type inference, and related
compiler-internals work) landed as a cluster of pull requests between
2022-08-31 and 2022-10-23, under their two separate feature gates (the
gates were deliberately split into two on 2022-09-23, five weeks after
RPITIT's initial implementation landed, "since async fn in trait doesn't
need to follow the same stabilization schedule" per that pull request's
own description).

Both features have been tracked together, since December 2021, under one
umbrella tracking issue (rust-lang/rust#91611), and both have accumulated
their own open, unfixed compiler bugs and open design questions in the
time since their initial implementation landed. RFC 3425's own text (the
RPITIT RFC that just merged) explicitly states, as one of its design
goals, that `async fn` in a trait should remain usable interchangeably
with the equivalent hand-written `-> impl Future` form — and separately
lists, in its own "Unresolved questions" section, a specific open
compiler issue that bears on whether that goal is actually achievable
without further changes.

This is the current state of that open work as of right now (2023-06-13,
end of day) — pulled directly from the issue tracker, the two RFCs' own
text, and the tracking issue, not cleaned up or pre-sorted into a
roadmap. Some items are old and dormant; one was only filed eleven days
ago and has no comments yet.
