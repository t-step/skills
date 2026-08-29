# Simulated projectmem search output

## Search: "multi-agent orchestrator" / "agent-to-agent communication" / "centralized dispatch"

No matches in any project.

## Search: "squash merge" / "stacked PR" / "commit history"

**Project: skills (current)**
> decision (2026-07-20): adopted the gh-stack skill/workflow for
> multi-PR features specifically to keep each dependent PR reviewable on
> its own commit, rather than squash-merging a feature into one commit at
> the end — stated reason: per-task review quality matters more here than
> a clean single-commit history, and the stacked-PR workflow lets a
> reviewer bisect to the exact task that introduced a problem.

## Search: "reversibility" / "rollback cost" / "blast radius"

**Project: skills (current)**
> Multiple SKILL.md sections (next-best-slice, slice-plan) weigh "how
> expensive would this be to undo" as one informal factor among several
> when judging a candidate slice or a known risk — consistently present as
> a consideration across both skills' revisions, but never turned into a
> named, rated scale, and never used to gate how much review rigor a
> change gets.

**Project: Valence** (cross-project)
> note (2026-07-18): a migration was deliberately sequenced as
> additive-only (new nullable column, no backfill-and-drop in the same
> release) specifically because a same-release destructive migration would
> have been expensive to reverse if the new code path had problems —
> reasoning was ad hoc to this one migration, not derived from any
> documented team-wide rule.

## Search: "LLM-as-judge" / "grading variance" / "judge disagreement" / "single-pass grading"

**Project: skills (current)**
> Two separate, real instances logged: (1) slice-review's case-009
> materiality-filter conclusion was revised from "disproven" to "not
> observed" after review found the original single-pass framing overstated
> what a small sample showed; (2) slice-retro's case-107 pressure case
> "had one non-reproducing single-run miss, confirmed via rerun" —
> i.e., a single grading pass produced a result that didn't replicate.
> Both are documented as reasons this repo's AGENTS.md now requires
> re-deriving conclusions from raw data rather than trusting one pass.

## Search: "IDE plugin" / "AI assistant product"

No matches in any project (not applicable — product launch, not a
practice).
