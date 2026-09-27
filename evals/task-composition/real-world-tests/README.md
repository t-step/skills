# task-composition real-world fixtures

A third suite, distinct from `evals.json` (author-designed synthetic
regression cases), `pressure-tests/` (adversarial refusal discipline), and
`triggering-tests/` (description triggering). This suite is built from
completed public open-source engineering work rather than author-designed
plans, on the theory that a synthetic plan -- however carefully designed
-- can be too clean to pressure-test the specific judgment calls this
skill exists to make (a plausible-but-wrong execution shape, not just an
obviously-wrong one).

Each case reconstructs a point-in-time snapshot of a real, already
partially-decomposed Jira/GitHub initiative, cut off before the outcome
(final PR structure, discovered bugs, actual merge order) was known. The
agent-visible fixture under `evals/task-composition/cases/case-3xx/`
contains only what was knowable at that cutoff. Everything else --
sources, the full historical outcome, actual PRs, and the exact
cutoff rationale -- lives under `evals/task-composition/provenance/
case-3xx/`, which a tested agent must never see.

| Case | Source | Cutoff | Shape | What it pressures |
|---|---|---|---|---|
| 301 | Apache Ignite IEP-119 Phase 1 ("move common classes to ignite-commons," IGNITE-24781 and its Sub-tasks) | 2025-03-30 | 13 tasks | A real multi-consumer horizontal enabler (module creation) vs. a task that *sounds* foundational but is actually gated, not gating (IGNITE-24850); two same-class shared-file pairs with no stated link; one genuinely tangled, only-partly-resolved pair (IGNITE-24957/IGNITE-24851) |
| 302 | Apache Cassandra CEP-7 / Storage-Attached Indexes (CASSANDRA-16052), Phase-3-era window | 2023-05-15 | 13 tasks | Distinguishing an externally-blocked task (community DISCUSS gate) and a task reaching into shared non-SAI storage-engine machinery from ordinary in-set dependencies; a real three-way convergence point; resisting layer-batching-by-label and a manufactured enabler with no named consumer |
| 303 | Apache Hudi metadata-table initiative (HUDI-1292/RFC-15 lineage), Aug-Sep 2021 window | 2021-09-21 | 19 tasks | The messiest/largest case: several genuinely unresolved ambiguities the tickets themselves don't settle, an undifferentiated priority label that looks informative but isn't, a correctness-bug cluster with a textually-recoverable (not formally declared) shared mechanism, and a singular-consumer pseudo-enabler drawn from real ticket wording |
| 304 | Kubernetes KEP-753 Sidecar Containers, post-alpha resource-manager fallout (kubernetes/kubernetes#119442 and related issues/PRs), Jul-Aug 2023 window | 2023-08-30 | 9 tasks | A historically real, comment-thread-traceable shared root cause (resource-manager coalescing) across three-to-four tickets that does not, by itself, determine a unique slice topology; an asymmetric-readiness trap inside one umbrella issue's title (four "manager" items named side by side but not equally staffed or scoped); a same-day, same-author, multi-draft investigation that must not be fragmented into invented tasks; a cross-binary independent item (HPA/autoscaler) that shares vocabulary but no dependency with the manager cluster |
| 305 | Rust `async fn` in trait (AFIT) + return-position `impl Trait` in trait (RPITIT) stabilization history (rust-lang/rust#91611 and related issues, RFC 3425), mid-June 2023 window | 2023-06-13 | 9 tasks | The mirror image of case-304's axis: real, textually strong mechanism-level coupling (a stated desugaring relationship, a verified shared implementation file, a core-team "X is just Y" quote) plus a ratified RFC's own explicit, named convergence pairing, across nine tickets -- tests whether a run over-merges everything on that coupling, or correctly keeps a stated two-item convergence pairing from bleeding outward into unrelated feature-specific bugs |

## Grading philosophy

Unlike the synthetic suite, historical execution here is evidence, not an
answer key. `grading/case-3xx.expected.md` for each case separates:

- **REQUIRED** -- topology facts the historical record (cited by
  provenance file) actually establishes. A response that contradicts one
  of these is wrong.
- **DEFENSIBLE EITHER WAY** (case-302 only, so far) -- a genuine open
  question the record doesn't resolve; both answers are acceptable as
  long as the choice is stated, not silently assumed.
- **DIAGNOSTIC / HISTORICAL COMPARISON** -- purely informational facts
  about how the work actually shipped. Never pass/fail. A response is
  never scored against reproducing the historical PR/commit split.

Each case's grading key was drafted by the same research pass that built
the fixture, then audited by a separate, fresh reviewer agent instructed
to check for hindsight leakage (agent-visible content that could only be
known after the stated cutoff) and unsupported grading assumptions, with
authority to fix defects directly against live primary sources (the
Apache Jira and GitHub REST APIs) rather than trusting the first draft's
provenance narrative. All three cases had at least one real defect found
and fixed at that stage (see each case's `provenance/case-3xx/
cutoff-rationale.md` for specifics) -- this is recorded here because it's
relevant to how much to trust the fixtures, not because it reflects on
the skill itself.

## Manifest

`real_world_evals.json` holds one entry per case in the same shape as the
top-level `evals.json`, with `expectations` drawn from each case's
REQUIRED list (condensed). The full REQUIRED/DEFENSIBLE/DIAGNOSTIC
reasoning and provenance citations live only in
`evals/task-composition/grading/case-3xx.expected.md` -- treat the
manifest's `expectations` as a checklist, not a replacement for reading
the grading file when actually grading a run.

## Running these cases

Same harness convention as the rest of this skill's eval suite (see
`evals/task-composition/RESULTS.md`): a fresh subagent per run, cwd'd or
scoped so it can see only the named case's `cases/case-3xx/` directory
(never `provenance/`, never a sibling case, never this README or the
grading file), with-skill runs additionally instructed to read and follow
`skills/task-composition/SKILL.md`. Raw outputs go under
`evals/task-composition/runs/<date>-real-world-iteration-1/` (gitignored,
per the repository's existing convention for raw per-run transcripts);
only the hand-written summary in `runs/<date>-real-world-runs.md` is
tracked.
